Title: Functional Core, Imperative Shell
Subheading: How to write very testable code using the functional core, imperative shell technique.
Alias: /post/functional-core-imperative-shell/

_Testability_ is the idea that code should be designed so that it's easy to
write tests for. In
[Boundaries](https://www.destroyallsoftware.com/talks/boundaries) Gary
Bernhardt introduces a programming technique he calls
_functional core, imperative shell_ that (among other advantages) helps to
make code very easy to test.

I tried to apply the approach to some real-world code: an OAuth 2.0 plugin for
[CKAN](http://ckan.org/).


<!--more-->


The idea is that each function or method in your code is one of two types:

Functional core

: These are functions that take values in as parameters, and give values out
  as return values. They use explicit parameters instead of implicit
  dependencies. They have few or no side effects, and each one of these
  functions is very well isolated from the rest of the code.

    You try to put all the logic and decisions of your code into these
    "pure functions", so there are many potential paths through one of these
    functions. But you try to keep things like the network, the database,
    rendering to the screen, disk, etc out of these functions.

Imperative shell

: These "shell functions" are where all the side effects and persistent state
  go: the network and database etc. They are highly integrated with the rest
  of your code and with other code that you're using (e.g. your web framework).

    You try to keep logic and decisions out of the shell functions, there
    should be few possible paths through a shell function (ideally only one).
    If possible, they should be trivial one-liner functions.

Writing code in this way has many advantages. All the logic is in the pure
functions which are very modular and easy to understand. They're also *much*
easier to test, and you can get 99% coverage by just testing your pure
functions and ignoring the shell.


## An OAuth 2.0 Plugin for CKAN

[ckanext-oauth2waad](https://github.com/ckan/ckanext-oauth2waad) is
a [CKAN](http://ckan.org/) plugin that lets users login to a CKAN site using
their Windows Azure Active Directory (WAAD) account instead of creating a new
username and password for the site.

The way it works is:

<figure>
    <img style="border: none;" src="{static}/images/waad_signin.png" alt="Logging into CKAN using Persona" title="Logging into CKAN using Persona">
    <figcaption>Logging into CKAN using Persona</figcaption>
</figure>

1. On the CKAN login page the user clicks a "Login with WAAD" link that
   sends them to the WAAD login server.
   This link's URL contains a **redirect URI** as a URL parameter that tells
   the WAAD server where to redirect the user's browser to after a successful
   login:
   `?redirect_uri=http://demo.ckan.org/_waad_redirect_uri`.

2. The user enters their WAAD username and password into the WAAD login page
   and clicks sign in. After a successful sign in the WAAD server redirects
   the user's browser to the redirect URI.
   The server appends an
   **authorization code** to the redirect URI as a URL param:
   `?code=ffhjkl434387jlkmdfsas`.

3. CKAN receives the request with the authorization code. The `oauth2waad`
   plugin's `login()` method is called, and handles the request in four steps:

    1. It makes a request to the WAAD server for the user name corresponding
       to the given authorization code, and receives the user name back from the
       WAAD server.

    2. It finds the user account with the given user name in CKAN's database.
       If no account exists, it silently creates a new account.

    3. It logs the user in to CKAN by saving the user name in CKAN's session.

    4. It redirects the user's browser to the dashboard page for the account
       they've just logged in to.

There's also a cross-site request forgery (CSRF) check, but we'll ignore that
for this explanation.

This is how the "login experience" looks, from the user's point of view:

<figure>
    <img style="border: none;" src="{static}/images/oauth2waad.gif" alt="Logging into CKAN with Windows Azure Active Directory" title="Logging into CKAN with Windows Azure Active Directory">
    <figcaption>Logging into CKAN with Windows Azure Active Directory</figcaption>
</figure>

The `oauth2waad` plugin's `login()` method that handles actually logging the
user into CKAN is the method we're going to try to test using a functional
core, imperative shell approach.


## A Naïve Implementation

Here's a naïve implementation of the `login()` method:

```python
class WAADRedirectController(toolkit.BaseController):

    def login(self):
        """Handle a login request from the WAAD server.

        When the WAAD server wants to log a user into our CKAN site, it
        redirects the user's browser to a CKAN URL that routes to this
        login() method.

        The URL params contain an auth code which we can use to get the
        user's name from the WAAD server, and then log the user in to CKAN
        by saving the name in CKAN's session.

        """
        # Look for the auth code in the URL that the WAAD server requested
        # from CKAN.
        auth_code = pylons.request.params['code']

        # The data that we're going to post to the WAAD server.
        # This includes a secret client ID from CKAN's config file
        # (which we access via the pylons.config object).
        data = {
            'client_id': pylons.config['client_id'],
            'code': auth_code,
            }

        # Use the requests library to make an HTTP POST request to the WAAD
        # server.
        response = requests.post(
            pylons.config['waad_server_url'], data=data)

        # Parse the response to get the user's name.
        name = response.json()['name']

        # Find the CKAN user account corresponding to this WAAD user account.
        try:
            user = toolkit.get_action('user_show')(data_dict = {'id': name})
        except toolkit.ObjectNotFound:
            # The user doesn't exist in CKAN yet, create it by calling the
            # CKAN API.
            user = toolkit.get_action('user_create')(
                context={'ignore_auth': True}, data_dict={'name': name})

        # Log the user in to CKAN by adding their name to the Pylons
        # session.
        pylons.session['user'] = name
        pylons.session.save()

        # Finally, show the user their dashboard page.
        toolkit.redirect_to(controller='user', action='dashboard',
                            id=name)
```

(This is a simplified version of the method, the production code contains a lot
of error-handling and other details, but the above code is closely based on the
real thing.)


## Testing the Naïve Implementation

***TLDR**: The naïve implementation is very difficult to test because it
requires a lot of mocking patching and simulating. The test code takes a long
time to write and is complicated, tightly coupled to CKAN internals, and slow.
The rest of this section details the problems with testing the naïve
implementation. Skip to [A better implementation](#better) to see the results.*

The code is quite simple, straightforward and readable. But the naïve
implementation is *very* difficult to test. Some of the things you'll have to
do to write a test for this include:

* Resetting CKAN's test database before each test, because the CKAN API
  functions that the method calls write things to the database that may change
  the outcome of the next tests.

* Running CKAN inside a test web server that can simulate HTTP requests for us.
  (We can do this using a [webtest](http://webtest.pythonpaste.org/) `TestApp`
  object.)

    You can't just initialize a `WAADRedirectController` object and call its
    `login()` method. `WAADRedirectController` inherits from
    `ckan.plugins.toolkit.BaseController` which means it depends on a bunch of
    CKAN and Pylons internals and will crash if initialized outside of a Pylons
    HTTP request. If you do this:

        #!python
        import ckanext.oauth2waad.plugin as plugin

        def test_login():
            controller = plugin.WAADRedirectController()
            controller.login()

    You'll get this:

        TypeError: No object (name: request) has been registered for this thread

* Inserting test values into the Pylons config.

    Simply initializing a `TestApp` for CKAN won't work because the `oauth2waad`
    plugin won't be activated, and the various config settings that the plugin
    needs will be missing. Each test function needs to insert the particular
    settings that it needs into the `pylons.config` first and then create the
    test app.

* Mocking the WAAD server, because when we request CKAN's login URL the
  `login()` method tries to make an HTTP request to the WAAD server to get
  the user's name.

    We need to mock the response to this HTTP request, which we can do using the
    [HTTPretty](http://falcao.it/HTTPretty/) library.

* Mocking the Pylons session.

    Our test needs to access the Pylons session so that it can check that the
    `login()` method did what it was supposed to do: save the user's name in
    the session.

    We can't simply `import pylons` and access the Pylons session from our test
    function. If we try to do this at the end of our test function:

        #!python
        assert pylons.session['user'] == 'fred', (
            "login() should add the user's name to the Pylons session")

    We'll get:

        TypeError: No object (name: session) has been registered for this thread

    The Pylons session is only available during an HTTP request. To get around
    this, we'll have to use the [mock](https://pypi.python.org/pypi/mock)
    library to patch `pylons.session` and replace it with a mock session object.

    If we simply do `@mock.patch(pylons.session)` we'll get mock objects leaking
    into CKAN's internals and a variety of confusing error messages from CKAN,
    Pylons and SQLAlchemy (as SQLAlchemy tries to save mock objects into database
    tables, for example).

    The reason for this leakage is that `pylons.session` has many different names
    in different parts of CKAN (which is poor design in CKAN, imho). Lots of CKAN
    modules do this:

        #!python
        from pylons import session

    When `ckan/lib/base.py` does that, for example, we now need to patch both
    `pylons.session` _and_ `ckan.lib.base.session`.

    We have to find each different name for `pylons.session` that our test
    happens to hit and patch each of them separately. This tightly couples our
    test code to CKAN internal details in a way that will be difficult to debug
    when those internals change.

It takes hours to write a test for this and find ways around all of these
obstacles, and it requires deep knowledge of CKAN and Pylons, as well as using
test libraries for mocking, patching and simulating. The test code that you'll
finally end up with will look something like this:

```python
import json
import webtest
import httpretty
import mock
import pylons.config as config
import ckan.config.middleware
import ckan.model as model

@mock.patch('pylons.session')
@mock.patch('ckan.lib.helpers.session')
@mock.patch('ckan.lib.base.session')
@httpretty.activate
def test_login(mock_base_session, mock_helpers_session, mock_session):
    """login() should add the user's name to the session."""
    # Reset the database contents before each test.
    model.Session.close_all()
    model.repo.rebuild_db()

    # Mock the Pylons session.
    session_dict = {}
    def getitem(name):
        return session_dict[name]
    def get(name):
        return session_dict.get(name)
    def setitem(name, val):
        session_dict[name] = val
    mock_session.__getitem__.side_effect = getitem
    mock_session.get.side_effect = get
    mock_session.__setitem__.side_effect = setitem

    # Mock the WAAD server.
    waad_server_url = 'https://fake.auth.endpoint/tenant/token'
    def request_callback(request, url, headers):
        """Our mock WAAD server response."""
        # The params that will go in the response's JSON body.
        params = {'name': 'fred'}

        body = json.dumps(params)
        return (200, headers, body)
    httpretty.register_uri(httpretty.POST, waad_server_url,
                        body=request_callback)

    # Insert the settings we need into the Pylons config.
    config['ckan.plugins'] = 'oauth2waad'
    config['client_id'] = 'mock_client_id'
    config['waad_server_url'] = waad_server_url

    # Make a CKAN test app.
    app = ckan.config.middleware.make_app(config['global_conf'],
                                            **config)
    app = webtest.TestApp(app)

    # Make a simulated HTTP POST request to the login URL.
    app.post('/_waad_redirect_uri', {'code': 'mock_auth_code'})

    # Test that the login() method added the user name into the mock Pylons
    # session.
    assert mock_session['user'] == 'fred'
```

This single test takes about *twenty seconds* to run, mostly because of the
time needed to boot the whole CKAN web app inside the test web server and
initialize its database. Even after this initialization the test isn't
particularly fast, it's exercising the full CKAN app.

This is a simplified version of the test, for a simplified version of the
`login()` method. The real test would be much longer, and you'd need many such
tests to test all the paths through the real `login()` method with all its
error handling and everything.

<h2 id="better">A Better Implementation</h2>

Let's try an alternative implementation of the `login()` method that moves most
of the code into pure, standalone functions and leaves only a minimal
imperative shell.

We'll factor two kinds of dependencies out of our pure functions:

**Incoming dependencies** are things that call us: the controller class and
method that we need to create in order to get CKAN to call our code.

We factor out the incoming dependencies by moving our code out of the class's
`login()` method and into a standalone `_login()` function, and turning the
original `login()` method into a one-liner that calls the `_login()` function.

We can now test the `_login()` function by importing our plugin module and
calling the function directly - we don't need to initialize a
`WAADRedirectController` object.

**Outgoing dependencies** are things that we call: the `pylons.request.params`
object that we get the auth code from, the `pylons.config` object that we get
config settings from, the `requests.post()` function (from the
[requests](http://docs.python-requests.org/) library) that we use to make the
HTTP request to the WAAD server, the `pylons.session` object that we save
the user's name to, and the `ckan.plugins.toolkit.redirect_to()` function
that we call to redirect the browser to the user's dashboard.

We factor these out by having the `_login()` function take them as parameters.
Instead of calling `requests.post()` directly for example, it takes a callable
as a `post` param and calls that. The `login()` method passes a
`requests.post()` wrapper function as the argument to this post param. When we
come to writing our tests, we can simply pass in a mock post function.

Here's the refactored code:

```python
def _post(endpoint, data):
    """Make an HTTP POST request and return the JSON from the response."""
    return requests.post(endpoint, data).json()

class WAADRedirectController(toolkit.BaseController):

    def login(self):
        """Handle requests to the WAAD redirect_uri."""
        _login(
            pylons.request.params,
            pylons.config['client_id'],
            pylons.config['waad_server_url'],
            _post,
            pylons.session,
            toolkit.redirect_to)

def _login(params, client_id, waad_server_url, post, session, redirect):

    name = _get_user_name_from_waad(params, client_id, waad_server_url,
                                    post)

    user = _log_the_user_in(session, name)

    redirect(controller='user', action='dashboard', id=name)

def _get_user_name_from_waad(params, client_id, waad_server_url, post):
    """Request the user's name from the WAAD server and return it."""

    data = {'client_id': client_id, 'code': params['code']}
    response_json = post(waad_server_url, data=data)
    return response_json['name']

def _log_the_user_in(...):
    ...
```


## Testing the Better Implementation

With the code refactored so, we can now write our tests like this:

```python
import ckanext.oauth2waad.plugin as plugin

def test_get_user_name_from_waad():
    """get_user_name_from_waad() should return the user name from the WAAD server."""

    def post(endpoint, data):
        """A mock HTPP post() function.

        Just returns a mock response from the WAAD server containing a mock
        user name, without actually making any HTTP request.

        """
        return {'name': 'fred'}

    # The params of the request to CKAN's redirect URI.
    params = {'code': 'fake_auth_code'}

    name = plugin._get_user_name_from_waad(
        params, 'fake client id', 'fake waad server url', post)

    assert name == 'fred'
```

This test code is *much* shorter and simpler, much quicker and easier to
write, and the test runs in 0.008s.

The only bit of code that can't be covered by unit testing
`_get_user_name_from_waad()` and the other pure functions directly is the
`WAADRedirectController`'s `login()` method, which contains just a single
function call. We could either leave this untested and settle for 99% coverage,
or we could add a single integration test for the simplest happy path through
the code, and leave all the details to be covered by the unit tests.


## Epilogue: Mocking the CKAN API

The `_log_the_user_in()` function not shown above has to find the CKAN user
corresponding to the name from the WAAD server, create the user if it
doesn't already exist, and then log the user in by adding the user to the
Pylons session.

`_log_the_user_in()` can be written and tested in the same way as we've done
for `_get_user_name_from_waad()` above.
But this function has a couple of outgoing dependencies that we haven't seen yet.
It has to call two CKAN API methods: `user_show()` and `user_create()` (both
must be called via `ckan.plugins.toolkit.get_action()`). If the function tries
to call these API functions when it's being run by our tests, that's going to
be slow (those API functions pull in all sorts of CKAN code, and they access
the database) and it's probably going to crash with some weird CKAN, Pylons
or SQLAlchemy error because they expect to be called during a Pylons HTTP
request.

It would be fairly simple to use mock to patch
`ckan.plugins.toolkit.get_action()` during our tests, replacing it with a mock
`get_action()` function that returns mock `user_show()` and `user_create()`
functions. But that would tightly couple our test code to internal details of
both our plugin and CKAN. Our test now needs to know about three implicit
dependencies of `_log_the_user_in()`: `get_action()`, `user_show()` and
`user_create()`, and it needs to know that the mock `get_action()` function
should return the mock `user_show()` or the mock `user_create()` if called with
the argument `'user_show'` or `'user_create'` respectively, and that
`_log_the_user_in()` shouldn't call `get_action()` with any other arguments.

It's much simpler and better to add `user_show` and `user_create` arguments to
the `_log_the_user_in()` function and have the `login()` shell method
pass in CKAN's real `user_show()` and `user_create()`
functions as arguments, just like we did with `requests.post()` when testing
`_get_user_name_from_waad()`. Then our test function can simply pass in its
own mock functions.

This dependency injection approach makes for long parameter lists, but
it keeps the dependencies of our functions nice and explicit and it lets us
avoid the mock library entirely.


## Conclusion

Following this technique might feel like refactoring our production code
"just" to make the test code nicer. It can seem obtuse at first to have a
`login()` method that calls a `_login()` function with a long list of
parameters, instead of just putting the code directly in the `login()` method.
Passing in `requests.post()` as a parameter instead of just calling it directly
also feels needlessly indirect at first.

But I'd argue that testability is a very good reason to design your code in a
particular way. Tests are important, and if you're testing thoroughly then
you're going to be spending just as much time writing tests as writing
production code (or more, if your tests are hard to write because your
production code isn't easy to test!).

Designing for testability with a _functional core, imperative shell_ approach
also tends to make your code very modular, which is great for readability and
reuse as well.
