Title: pyramid_tm, pyramid_retry, SQLAlchemy and Sentry
Status: draft

Unhandled Errors
----------------

Here's a view that raises an unhandled error (meaning an error not handled by
any of the app's Pyramid
[exception views](https://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-exception-view):

<script src="https://gist.github.com/0ed527f9c6fb394fe22d3056d1e1083c.js?file=unhandled_error.py"></script>

You can send a request to this view like this:

```console
$ tox -qq http://localhost:6544/errors/unhandled
HTTP/1.1 500 Internal Server Error
Connection: close
Content-Length: 141
Content-Type: text/html

<html>
  <head>
    <title>Internal Server Error</title>
  </head>
  <body>
    <h1><p>Internal Server Error</p></h1>

  </body>
</html>
```

<details markdown="1">
<summary>Where did this HTML error page come from?</summary>
The HTML error response body above is actually [gunicorn's default error template](https://github.com/benoitc/gunicorn/blob/29f0394cdd381df176a3df3c25bb3fdd2486a173/gunicorn/util.py#L320-L330)
that it uses when the underlying Pyramid app raises an exception. The "Internal
Server Error" text comes from
[Pyramid's `HTTPServerError` exception class](https://github.com/Pylons/pyramid/blob/0fa20105b012ba29558656b1576fc426f91604f5/src/pyramid/httpexceptions.py#L1183-L1192).
</details>

In the app's logs you'll see this:

```
2019-09-19 14:56:54,414 DEBUG [txn.140214296838464:110][MainThread] new transaction
2019-09-19 14:56:54,415 DEBUG [root:8][MainThread] unhandled_error() view was called
2019-09-19 14:56:54,415 DEBUG [txn.140214296838464:526][MainThread] abort
2019-09-19 14:56:54,436 ERROR [gunicorn.error:277][MainThread] Error handling request /errors/unhandled
Traceback (most recent call last):
  ...
  File ".../pyramid/view.py", line 779, in invoke_exception_view
    raise HTTPNotFound
pyramid.httpexceptions.HTTPNotFound: The resource could not be found.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  ...
  File ".../retrydemo/unhandled_error.py", line 11, in unhandled_error
    raise RuntimeError("Unhandled error")
RuntimeError: Unhandled error
2019-09-19 14:56:54,437 DEBUG [urllib3.connectionpool:815][raven-sentry.BackgroundWorker] Starting new HTTPS connection (1): sentry.io:443
2019-09-19 14:56:54,944 DEBUG [urllib3.connectionpool:396][raven-sentry.BackgroundWorker] https://sentry.io:443 "POST /api/1730871/store/ HTTP/1.1" 200 41
```

<details markdown="1">
<summary>Why is there an HTTPNotFound in that traceback?</summary>
The traceback above is a little confusing. The response from the app was a 500
Server Error, but the logs read as if a 400 Not Found happened and _then_,
during the handling of the Not Found, our `RuntimeError("Unhandled error")`
occurred. But this is just an artefact of how Pyramid's code works. Specifically:

1. Pyramid's `DefaultViewMapper` [calls our app's `unhandled_error()` view](https://github.com/Pylons/pyramid/blob/0fa20105b012ba29558656b1576fc426f91604f5/src/pyramid/viewderivers.py#L144)
   which raises `RuntimeError`.

2. The `RuntimeError` gets caught by Pyramid's [`excview_tween`](https://github.com/Pylons/pyramid/blob/0fa20105b012ba29558656b1576fc426f91604f5/src/pyramid/tweens.py#L39-L46)
   which responds to the exception by attempting to call an exception view by [calling `invoke_exception_view()`](https://github.com/Pylons/pyramid/blob/0fa20105b012ba29558656b1576fc426f91604f5/src/pyramid/tweens.py#L13).
   This is where the 404 Not Found comes in: since our app has no exception view for `RuntimeError` `invoke_exception_view()` [raises `HTTPNotFound`](https://github.com/Pylons/pyramid/blob/0fa20105b012ba29558656b1576fc426f91604f5/src/pyramid/view.py#L779).

3. The `HTTPNotFound` exception gets caught by the `excview_tween` that called `invoke_exception_view()`, and the `excview_tween` [re-raises the original `RuntimeError`](https://github.com/Pylons/pyramid/blob/0fa20105b012ba29558656b1576fc426f91604f5/src/pyramid/tweens.py#L14-L17).

   So the app's original `RuntimeError` that was raised by the view is later re-raised during the handling of the later `HTTPNotFound` that was raised by `invoke_exception_view()`.
   That's why Python's traceback describes a top-level `HTTPNotFound` exception with a `RuntimeError` that was raised during the handling of the `HTTPNotFound`.
   There's no actual 404 Not Found HTTP response here: what happened in the end was that the view raised an unhandled `RuntimeError` and this ended up causing a 500 Server Error response.
</details>

**The request didn't get re-tried** by pyramid_retry. You can see this from the
logging output above: the `unhandled_error() view was called` log message is
printed only once:

```
2019-09-19 14:56:54,415 DEBUG [root:8][MainThread] unhandled_error() view was called
```

That's because `RuntimeError` isn't a `RetryableException` subclass and we
haven't marked either the `RuntimeError` class or this particular
`RuntimeError` object instance as retryable using `mark_error_retryable()`.
pyramid_retry only retries requests that raise a retryable error and most types
of error aren't retryable by default (but note that [`pyramid_tm` automatically
marks certain "transient" errors as retryable, including
`ZODB.POSException.ConflictError`,
`psycopg2.extensions.TransactionRollbackError`, any
`transaction.interfaces.TransientError` subclass, and
others](https://docs.pylonsproject.org/projects/pyramid-tm/en/latest/#retries)).

**The `RuntimeError` did get reported to Sentry**.  You can see this in the
logging output above also:

```
2019-09-19 14:56:54,437 DEBUG [urllib3.connectionpool:815][raven-sentry.BackgroundWorker] Starting new HTTPS connection (1): sentry.io:443
2019-09-19 14:56:54,944 DEBUG [urllib3.connectionpool:396][raven-sentry.BackgroundWorker] https://sentry.io:443 "POST /api/1730871/store/ HTTP/1.1" 200 41
```

[sentry-sdk's Pyramid integration](https://docs.sentry.io/platforms/python/pyramid/)
does its job automatically: an unhandled exception that causes a 500 Server
Error gets reported to Sentry:

![RuntimeError in Sentry]({static}/images/runtimeerror-in-sentry.png)

<details markdown="1">
<summary>How do unhandled errors get reported to Sentry?</summary>
[Sentry's Pyramid integration](https://github.com/getsentry/sentry-python/blob/0.12.1/sentry_sdk/integrations/pyramid.py)
works by monkey patching Pyramid in a few places. In the case of an unhandled exception Sentry's
[monkey patching of Pyramid's `Router.__call__()`](https://github.com/getsentry/sentry-python/blob/79985b28df74963230cc53f977219b791d2bc508/sentry_sdk/integrations/pyramid.py#L102-L121)
is what's relevant. `Router.__call__()` is Pyramid's top-level WSGI method,
that Gunicorn calls in order to get a response to a request.
Sentry's patched `__call__` catches any exceptions that Pyramid raises
and [reports the exception to Sentry then re-raises the exception](https://github.com/getsentry/sentry-python/blob/79985b28df74963230cc53f977219b791d2bc508/sentry_sdk/integrations/pyramid.py#L114-L115)
so that the exception gets caught by Gunicorn as it would with a non-patched Pyramid.
</details>

Unhandled, Retryable Errors
---------------------------

Here's a view that raises an unhandled `RuntimeError` just like the previous
view above, but that marks the error as retryable using
`pyramid_retry.mark_error_retryable()`:

<script src="https://gist.github.com/0ed527f9c6fb394fe22d3056d1e1083c.js?file=unhandled_retryable_error.py"></script>

You can send a request to this view the same way as to the other view, just
with a different path. The response looks the same:

```console
$ tox -qq http://localhost:6544/errors/unhandled/retryable
HTTP/1.1 500 Internal Server Error
Connection: close
Content-Length: 141
Content-Type: text/html

<html>
  <head>
    <title>Internal Server Error</title>
  </head>
  <body>
    <h1><p>Internal Server Error</p></h1>

  </body>
</html>
```

In the app's logging you'll see this:

```
2019-09-19 15:08:00,560 DEBUG [txn.140444074512704:110][MainThread] new transaction
2019-09-19 15:08:00,561 DEBUG [root:9][MainThread] unhandled_retryable_error() view was called
2019-09-19 15:08:00,561 DEBUG [txn.140444074512704:526][MainThread] abort
2019-09-19 15:08:00,561 DEBUG [txn.140444074512704:110][MainThread] new transaction
2019-09-19 15:08:00,561 DEBUG [root:9][MainThread] unhandled_retryable_error() view was called
2019-09-19 15:08:00,562 DEBUG [txn.140444074512704:526][MainThread] abort
2019-09-19 15:08:00,562 DEBUG [txn.140444074512704:110][MainThread] new transaction
2019-09-19 15:08:00,562 DEBUG [root:9][MainThread] unhandled_retryable_error() view was called
2019-09-19 15:08:00,562 DEBUG [txn.140444074512704:526][MainThread] abort
2019-09-19 15:08:00,583 ERROR [gunicorn.error:277][MainThread] Error handling request /errors/unhandled/retryable
Traceback (most recent call last):
  ...
  File ".../pyramid/view.py", line 779, in invoke_exception_view
    raise HTTPNotFound
pyramid.httpexceptions.HTTPNotFound: The resource could not be found.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  ...
  File ".../retrydemo/unhandled_retryable_error.py", line 13, in unhandled_retryable_error
    raise error
RuntimeError: Unhandled error
2019-09-19 15:08:00,583 DEBUG [urllib3.connectionpool:815][raven-sentry.BackgroundWorker] Starting new HTTPS connection (1): sentry.io:443
2019-09-19 15:08:01,124 DEBUG [urllib3.connectionpool:396][raven-sentry.BackgroundWorker] https://sentry.io:443 "POST /api/1730871/store/ HTTP/1.1" 200 41
```

The traceback is the same as with the non-retryable error. But in the logging
before the traceback you can see that the request was re-tried twice. Three new
transactions were created, the view was called three times (and raised
`RuntimeError` each time), and the transaction was aborted three times:

```
2019-09-19 15:08:00,560 DEBUG [txn.140444074512704:110][MainThread] new transaction
2019-09-19 15:08:00,561 DEBUG [root:9][MainThread] unhandled_retryable_error() view was called
2019-09-19 15:08:00,561 DEBUG [txn.140444074512704:526][MainThread] abort
2019-09-19 15:08:00,561 DEBUG [txn.140444074512704:110][MainThread] new transaction
2019-09-19 15:08:00,561 DEBUG [root:9][MainThread] unhandled_retryable_error() view was called
2019-09-19 15:08:00,562 DEBUG [txn.140444074512704:526][MainThread] abort
2019-09-19 15:08:00,562 DEBUG [txn.140444074512704:110][MainThread] new transaction
2019-09-19 15:08:00,562 DEBUG [root:9][MainThread] unhandled_retryable_error() view was called
2019-09-19 15:08:00,562 DEBUG [txn.140444074512704:526][MainThread] abort
```

The third `RuntimeError` was allowed to bubble up to gunicorn which turned it
into the 500 Server Error response. The two earlier `RuntimeError`'s are
lost---they're neither logged nor reported to Sentry.

You can also see from the logs after the traceback that the error was reported
to Sentry, as before. Even though the request was tried three times it only
gets reported to Sentry once:

```
2019-09-19 15:08:00,583 DEBUG [urllib3.connectionpool:815][raven-sentry.BackgroundWorker] Starting new HTTPS connection (1): sentry.io:443
2019-09-19 15:08:01,124 DEBUG [urllib3.connectionpool:396][raven-sentry.BackgroundWorker] https://sentry.io:443 "POST /api/1730871/store/ HTTP/1.1" 200 41
```

<details markdown="1">
<summary>How is the exception only reported once?</summary>
Even though the request was tried three times only the exception raised by the
third attempt gets reported to Sentry.
This is because the reporting to Sentry is handled by Sentry's patched version
of Pyramid's top-level `Router.__call__` method which catches and reports the
exception. pyramid_retry's retrying happens at a slightly lower level than this
in Pyramid (in the execution policy) and only exceptions that aren't going to
be retried bubble up to this patched `__call__` method.
</details>

### Marking an entire exception class as retryable

Instead of marking individual exception object instances as retryable, you can
mark an entire exception _class_ as retryable:

<script src="https://gist.github.com/0ed527f9c6fb394fe22d3056d1e1083c.js?file=mark_error_class_retryable.py"></script>

After `mark_error_retryable(IOError)` has been called *all* requests that raise
`IOError` will be retryable, including future requests, and no matter where in
the code `IOError` is raised from.

Of course you wouldn't mark something as generic as `IOError` as retryable.
The example that [pyramid_retry's docs use](https://docs.pylonsproject.org/projects/pyramid-retry/en/latest/#custom-retryable-errors)
is `requests.Timeout`.

HTTP Errors
-----------

Pyramid comes with a set of [built-in HTTP exceptions](https://docs.pylonsproject.org/projects/pyramid/en/latest/api/httpexceptions.html)
to represent different HTTP response codes. A view can raise
`HTTPInsufficientStorage`, for example, to tell Pyramid to send a [507
Insufficient Storage](https://httpstatuses.com/507) response.
See [Using Special Exceptions in View Callables](https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/views.html#special-exceptions-in-callables)
in the Pyramid docs for details on how Pyramid handles these built-in HTTP
exceptions when views raise them.

Here's a view that raises an `HTTPInsufficientStorage` exception:

<script src="https://gist.github.com/0ed527f9c6fb394fe22d3056d1e1083c.js?file=http_error.py"></script>

Calling this view returns a 507 Insufficient Storage response with an HTML body:

```console
$ tox -qq http://localhost:6544/errors/http
HTTP/1.1 507 Insufficient Storage
Connection: close
Content-Length: 189
Content-Type: text/html; charset=UTF-8
Date: Thu, 19 Sep 2019 17:11:38 GMT
Server: gunicorn/19.9.0

<html>
 <head>
  <title>507 Insufficient Storage</title>
 </head>
 <body>
  <h1>507 Insufficient Storage</h1>
  There was not enough space to save the resource<br/><br/>



 </body>
</html>
```

<details markdown="1">
<summary>Where did this HTML error page come from?</summary>
Unlike with the uncaught `RuntimeError` above (where Pyramid re-raised the
error and it was caught and turned into an HTML response by Gunicorn) HTTP
exceptions are caught and turned into HTML responses by Pyramid itself, using a
built-in HTML template:

1. Built-in Pyramid HTTP exceptions like `HTTPInsufficientStorage` [are also response objects](https://github.com/Pylons/pyramid/blob/0fa20105b012ba29558656b1576fc426f91604f5/src/pyramid/httpexceptions.py#L68)
   and as such, [they're callable](https://github.com/Pylons/pyramid/blob/0fa20105b012ba29558656b1576fc426f91604f5/src/pyramid/httpexceptions.py#L341-L350)
2. When an exception response object is called it ends up [rendering](https://github.com/Pylons/pyramid/blob/0fa20105b012ba29558656b1576fc426f91604f5/src/pyramid/httpexceptions.py#L328)
   an [HTML body template](https://github.com/Pylons/pyramid/blob/0fa20105b012ba29558656b1576fc426f91604f5/src/pyramid/httpexceptions.py#L210-L221)
3. When a view raises one of these built-in HTTP exception response objects,
   Pyramid's router (the top-level object in the Pyramid framework: Pyramid's
   WSGI app that Gunicorn calls, and that routes requests to view code)
   [calls the exception](https://github.com/Pylons/pyramid/blob/0fa20105b012ba29558656b1576fc426f91604f5/src/pyramid/router.py#L270)
   and gets the HTML body and response headers
</details>

And this is what the app logs:

```
2019-09-19 18:11:38,545 DEBUG [txn.139799203021120:110][MainThread] new transaction
2019-09-19 18:11:38,546 DEBUG [root:9][MainThread] http_error() view was called
2019-09-19 18:11:38,546 DEBUG [txn.139799203021120:526][MainThread] abort
```

The request's transaction was aborted because the request ended in an error response.


**The request was not reported to Sentry**: sentry-sdk considers HTTP
exceptions to be deliberately raised and handled responses, so it
[doesn't report them to Sentry](https://github.com/getsentry/sentry-python/blob/79985b28df74963230cc53f977219b791d2bc508/sentry_sdk/integrations/pyramid.py#L126-L127).

**The request was not retried**: HTTP exceptions aren't marked retryable by
default. You could call `mark_error_retryable()` on one if you wanted to, the
request would then be retried and still nothing would be reported to Sentry.

Reporting HTTP Exceptions to Sentry with Custom Exception Views
---------------------------------------------------------------

You can change how an HTTP exception raised by a view is handled (e.g. to
change the response body template), and report it to Sentry, by using a
[custom exception view](https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/views.html#custom-exception-views).

Here's a file with a custom exception view for `HTTPNotImplemented` exceptions,
and a view that raises an `HTTPNotImplemented` exception:

<script src="https://gist.github.com/0ed527f9c6fb394fe22d3056d1e1083c.js?file=custom_exception_view.py"></script>

The custom exception view calls `sentry_sdk.capture_exception()` to report the
`HTTPNotImplemented` exception to Sentry. Otherwise, the exception wouldn't be
reported.

Calling the view returns a 501 Not Implemented response with a custom body:

```console
$ tox -qq http://localhost:6544/errors/handled/custom-exception-view
HTTP/1.1 501 Not Implemented
Connection: close
Content-Length: 23
Content-Type: text/plain; charset=UTF-8
Date: Fri, 20 Sep 2019 12:59:46 GMT
Server: gunicorn/19.9.0

My custom error message
```

### Retryable `HTTPException`'s get triple-reported

If you have a custom exception view like the one above for an `HTTPException`
subclass that reports the exception to Sentry then, if you also mark the
`HTTPException` as retryable, the exception can end up getting reported to
Sentry three times.

pyramid_retry attempts to get a response to the request three times and on each
of the three times both the view **and the exception view** are called. So your
custom exception view gets called three times and reports the exception to
Sentry three times.

It's not actually the same exception instance being reported three times.
pyramid_retry made three attempts to respond to the request. Each of the three
attempts raised an exception. This could have been three different types of
exception, if the three attempts had different results. Or the same thing could
have happened three times (as is the case with our example views). Each of the
three exceptions raised by each of the three attempts is reported.

Still, this is undesirable behaviour. If a failed request is going to be
re-tried you probably don't want any exceptions to be reported to Sentry unless
all three attempts fail and an error response is sent back to the caller. And
even when that happens you probably only want a single event to be reported to
Sentry, not three separate events.

You can filter out retryable exceptions from Sentry reporting globally using a
sentry-sdk `before_send` function. See below for an example of how to do that.
Or you can do so on a per-view basis by checking `is_error_retryable()` in your
exception view like this:

<script src="https://gist.github.com/0ed527f9c6fb394fe22d3056d1e1083c.js?file=custom_exception_view_retryable.py"></script>

Handled Exceptions
------------------

You can also add exception views for non-HTTP exceptions: for your own custom
exception classes, for built-in Python exceptions like `RuntimeError`, or for
exception classes from third-party libraries.

Here's a file that defines a custom error class, an exception view for that
type of exception, and a view that raises the custom error. The exception view
sets the error response status to 501 (it would default to 200 OK otherwise):

<script src="https://gist.github.com/0ed527f9c6fb394fe22d3056d1e1083c.js?file=handled_exception.py"></script>

Here's what gets logged when this view is called:

```
2019-09-20 14:13:08,323 DEBUG [txn.139929976435008:110][MainThread] new transaction
2019-09-20 14:13:08,324 DEBUG [root:21][MainThread] handled_exception() view was called
2019-09-20 14:13:08,324 DEBUG [root:12][MainThread] my_error() exception view was called
2019-09-20 14:13:08,334 DEBUG [txn.139929976435008:526][MainThread] abort
```

You can see from the logs that:

1. **Exceptions don't get retried by default**, `MyError` hasn't been marked as retryable
2. **Handled exceptions don't get reported to Sentry automatically**

### Handled exceptions with status 500 do get reported

If your view raises an exception then, even if the exception is handled by an exception view,
sentry-sdk does catch the exception and [reports it to Sentry if the response has status 500](https://github.com/getsentry/sentry-python/blob/79985b28df74963230cc53f977219b791d2bc508/sentry_sdk/integrations/pyramid.py#L88-L94).
This doesn't apply to `HTTPException` subclasses, those are
[filtered out from being reported](https://github.com/getsentry/sentry-python/blob/79985b28df74963230cc53f977219b791d2bc508/sentry_sdk/integrations/pyramid.py#L126-L127)
by the `_capture_exception()` function itself. So an `HTTPInternalServerError` or subclass won't be reported.
But if the response status is 500 and the exception is not an `HTTPException` or subclass then it gets reported to Sentry.

Handled, Retryable Errors
-------------------------

If a non-HTTP exception that is handled by an exception view is also marked as
retryable then pyramid_retry will retry the request up to two times:

<script src="https://gist.github.com/0ed527f9c6fb394fe22d3056d1e1083c.js?file=handled_retryable_exception.py"></script>

When you call this view the view and exception view are each called three
times, and nothing is reported to Sentry:

```
2019-09-20 18:05:59,487 DEBUG [txn.140402321711424:110][MainThread] new transaction
2019-09-20 18:05:59,487 DEBUG [root:22][MainThread] handled_retryable_exception() view was called
2019-09-20 18:05:59,487 DEBUG [root:13][MainThread] my_retryable_error() exception view was called
2019-09-20 18:05:59,488 DEBUG [txn.140402321711424:526][MainThread] abort
2019-09-20 18:05:59,488 DEBUG [txn.140402321711424:110][MainThread] new transaction
2019-09-20 18:05:59,488 DEBUG [root:22][MainThread] handled_retryable_exception() view was called
2019-09-20 18:05:59,488 DEBUG [root:13][MainThread] my_retryable_error() exception view was called
2019-09-20 18:05:59,488 DEBUG [txn.140402321711424:526][MainThread] abort
2019-09-20 18:05:59,488 DEBUG [txn.140402321711424:110][MainThread] new transaction
2019-09-20 18:05:59,488 DEBUG [root:22][MainThread] handled_retryable_exception() view was called
2019-09-20 18:05:59,488 DEBUG [root:13][MainThread] my_retryable_error() exception view was called
2019-09-20 18:05:59,488 DEBUG [txn.140402321711424:526][MainThread] abort
```

### Custom retryable exceptions with status 500 get triple reported

Due to an unfortunate interaction between sentry-sdk's Pyramid integration and
pyramid_retry, if a view raises a non-`HTTPException` exception that is marked
as retryable and the response has status code 500 then the exception will be
reported to Sentry three times.

For example here's a view that raises a custom, retryable exception and an
error view that handles the exception and sets the response status to 500:

<script src="https://gist.github.com/0ed527f9c6fb394fe22d3056d1e1083c.js?file=handled_retryable_500_exception.py"></script>

When you call this view three exceptions are reported to Sentry, one for each
attempt that pyramid_retry made:

<pre><code>2019-09-20 18:16:19,569 DEBUG [txn.140269457391936:110][MainThread] new transaction
2019-09-20 18:16:19,569 DEBUG [root:22][MainThread] handled_retryable_500_exception() view was called
2019-09-20 18:16:19,569 DEBUG [root:13][MainThread] my_retryable_500_error() exception view was called
2019-09-20 18:16:19,579 DEBUG [txn.140269457391936:526][MainThread] abort
2019-09-20 18:16:19,579 DEBUG [txn.140269457391936:110][MainThread] new transaction
2019-09-20 18:16:19,579 DEBUG [root:22][MainThread] handled_retryable_500_exception() view was called
2019-09-20 18:16:19,579 DEBUG [root:13][MainThread] my_retryable_500_error() exception view was called
2019-09-20 18:16:19,580 DEBUG [urllib3.connectionpool:815][raven-sentry.BackgroundWorker] Starting new HTTPS connection (1): sentry.io:443
2019-09-20 18:16:19,585 DEBUG [txn.140269457391936:526][MainThread] abort
2019-09-20 18:16:19,586 DEBUG [txn.140269457391936:110][MainThread] new transaction
2019-09-20 18:16:19,586 DEBUG [root:22][MainThread] handled_retryable_500_exception() view was called
2019-09-20 18:16:19,586 DEBUG [root:13][MainThread] my_retryable_500_error() exception view was called
2019-09-20 18:16:19,592 DEBUG [txn.140269457391936:526][MainThread] abort
<strong>2019-09-20 18:16:20,101 DEBUG [urllib3.connectionpool:396][raven-sentry.BackgroundWorker] https://sentry.io:443 "POST /api/1730871/store/ HTTP/1.1" 200 41
2019-09-20 18:16:20,250 DEBUG [urllib3.connectionpool:396][raven-sentry.BackgroundWorker] https://sentry.io:443 "POST /api/1730871/store/ HTTP/1.1" 200 41
2019-09-20 18:16:20,398 DEBUG [urllib3.connectionpool:396][raven-sentry.BackgroundWorker] https://sentry.io:443 "POST /api/1730871/store/ HTTP/1.1" 200 41</strong></code></pre>

As with the `HTTPException` that was being triple-reported above, these are
actually three different exceptions raised by pyramid_retry's three attempts to
get a response to the request. See below for how to filter retryable exceptions
from Sentry...

Preventing Retryable Exceptions from being reported to Sentry
-------------------------------------------------------------

You can prevent any retryable exceptions from being reported to Sentry by using
sentry-sdk's
[`before_send`](https://docs.sentry.io/error-reporting/configuration/?platform=python#before-send)
hook. This will work both when your own view or exception view code calls
`sentry_sdk.capture_exception()` and then pyramid_retry retries the request,
and when a retryable non-`HTTPException` is raised and the response status is
500 (triggering sentry_sdk's own Pyramid integration to report three events).
No retryable exceptions will ever be reported to Sentry.  Just add this
`before_send` hook to your `sentry_sdk.init()` call:

```python
import logging

from pyramid.threadlocal import get_current_request
from pyramid_retry import is_error_retryable
import sentry_sdk
import sentry_sdk.integrations.pyramid

def before_send(event_dict, hint_dict):
    """
    Return event_dict if the exception should be reported to Sentry.

    Return None to filter out the exception from being reported to Sentry.
    """
    exception = hint_dict["exc_info"][1]
    request = get_current_request()

    if request is None:
        # get_current_request() returns None if we're outside of Pyramid's
        # request context. This happens when sentry_sdk's Pyramid integration
        # catches an exception that Pyramid is going to raise to the WSGI
        # server (Gunicorn, in our case).
        # Always allow these uncaught exceptions to be reported to Sentry:
        return event_dict

    if is_error_retryable(request, exception):
        # Don't report the exception to Sentry if the request is going to be
        # re-tried.
        #
        # Note: is_error_retryable() returns *False* if the error is marked as
        # retryable but the request is on its last attempt and is not going to
        # be re-tried again.
        logging.debug("Filtering retryable exception from Sentry")
        return None

    return event_dict

sentry_sdk.init(
    <YOUR_SENTRY_DSN>,
    integrations=[sentry_sdk.integrations.pyramid.PyramidIntegration()],
    before_send=before_send,
)
```

Adding previous retry failures to Sentry reporting
--------------------------------------------------

If a request fails on its final attempt the exception from this final attempt
will be reported to Sentry but the exceptions from the previous failed
attempts, which caused the app to reach the final attempt in the first place,
don't get reported. This can make debugging difficult.

To help you can add a pyramid_retry [`IBeforeRetry` subscriber](https://docs.pylonsproject.org/projects/pyramid-retry/en/latest/#receiving-retry-notifications)
function to your app. pyramid_retry will call this function each time it's
about to *re*-try a request. So if a request is attempted three times, for
example, an `IBeforeRetry` subscriber will be called twice: once after the
first failure to serve the request (before the first retry) and once after the
second failure (before the third and final retry).

You can use sentry-sdk's [extra context](https://docs.sentry.io/enriching-error-data/context/?platform=python#extra-context)
API to add information about the failure of earlier attempts to the Sentry
event that will be sent if the final attempt fails:

<script src="https://gist.github.com/0ed527f9c6fb394fe22d3056d1e1083c.js?file=subscribers.py"></script>

With an `IBeforeRetry` subscriber like this:

1. Nothing is reported to Sentry unless the a request gets all the way to its
   final attempt and that final attempt fails. If earlier attempts fail but
   then a later attempt to process the request succeeds, nothing is reported

2. If the final attempt fails only a single event is reported to Sentry, an
   event for the exception raised by the final attempt

3. But that Sentry event for the final attempt also contains the exceptions and
   tracebacks from each failed earlier attempt, in the <samp>Additional
   Data</samp> section:

   ![Additional Data in Sentry]({static}/images/additional-data.png)

Handling SQLAlchemy IntegrityErrors
-----------------------------------

### Session rollback

### tm rollback

### Retry request

