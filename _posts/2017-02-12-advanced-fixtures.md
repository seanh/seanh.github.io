---
tags: [Python Unit Tests at Hypothesis]
redirect_from:
  - /post/advanced-fixtures/
---

Advanced pytest Fixtures
========================

In [Basic pytest Fixtures](2017-02-02-fixtures.md) we saw that fixtures are pytest's
alternative to `setup()` and `teardown()` methods or to test helper functions.
This post will try to show that pytest fixtures are much more than just a more
convenient alternative to helper functions, by explaining some of their more
advanced features.

Fixtures can use other fixtures
-------------------------------

We saw in [Basic pytest Fixtures](2017-02-02-fixtures.md) that if a test wants to use a
fixture it simply takes that fixture as an argument, by name. Here's a test
that uses the `pyramid_request` fixture:

```python
def test_current_page_defaults_to_1(pyramid_request):
    ...
```

Pytest runs the `pyramid_request()` fixture function and passes the fixture
function's **return value** into
`test_current_page_defaults_to_1(pyramid_request)` as the `pyramid_request`
argument.

What if a _fixture function_ wants to have access to another fixture object?
It can just take that other fixture as argument, by name, exactly like a test
function would.

As an example we'll look at
[the tests for `UserSearchController`](https://github.com/hypothesis/h/blob/7d02ed90a1f3e6e38de30266dc5fcc31abef9f91/tests/h/views/activity_test.py#L563).
[`UserSearchController`](https://github.com/hypothesis/h/blob/7d02ed90a1f3e6e38de30266dc5fcc31abef9f91/h/views/activity.py#L270)
is the [Pyramid view class](http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/viewconfig.html?highlight=view_defaults#view-defaults-class-decorator)
for the "user search" page, which is the page that lets you search and browse
all of a user's annotations, for example <https://hypothes.is/users/jeremydean>.

The `factories` fixture (see [this tutorial's post on factories](2017-01-29-factories.md))
is often used by other fixtures. For example,
[the `user` fixture in `TestUserSearchController`](https://github.com/hypothesis/h/blob/7d02ed90a1f3e6e38de30266dc5fcc31abef9f91/tests/h/views/activity_test.py#L755)
uses it to return a `User` object with a registration date, URI and ORCID:

```python
class TestUserSearchController(object):

    ...

    @pytest.fixture
    def user(self, factories):
        return factories.User(
            registered_date=datetime.datetime(year=2016, month=8, day=1),
            uri='http://www.example.com/me',
            orcid='0000-0000-0000-0000',
        )
```

Now test methods in `TestUserSearchController` can just take `user` as argument
and get this `User` object, rather than each individual test using the
`factories` fixture and constructing the `User` itself:

```python
    def test_something(self, user):
        # Some test code that uses `user`.
```

Since the `user()` fixture method takes the `factories` fixture as argument,
pytest knows that it needs to call `factories()` and get its return value before
it can call `user()`. Pytest does something like this for each test that uses
the `user` fixture:

<pre><code>
test_obj          = TestSearchController()
<strong>factories_fixture</strong> = conftest.factories()
user_fixture      = test_obj.user(factories=<strong>factories_fixture</strong>)
test_obj.test_something(user=user_fixture)
</code></pre>

Note that by using the `user` fixture the test has indirectly caused the
`factories` fixture function to be called as well.

A fixture can use multiple other fixtures
-----------------------------------------

Just like a test method can take multiple fixtures as arguments, a fixture
can take multiple other fixtures as arguments and use them to create the
fixture value that it returns.

In order to test one of `UserSearchController`'s methods the test first needs
to create a `UserSearchController` object. `UserSearchController.__init__()`
requires a user as argument, so the test will use the `user` fixture from
above. `__init__()` also requires a Pyramid request as argument, so the test
will also use the `pyramid_request` fixture. A first pass at a test might look
like this:

```python
class TestUserSearchController(object):

    def test_some_search_controller_method(self, user, pyramid_request):
        controller = activity.UserSearchController(user, pyramid_request)

        # Test something using `controller`.

    @pytest.fixture
    def user(self, factories):
        ...

    @pytest.fixtureÎ
    def pyramid_request(self):
        ...
```

But `controller = activity.UserSearchController(user, pyramid_request)` would
be duplicated in every `UserSearchController` test, and every test would need
both the `user` and `pyramid_request` arguments. We can get rid of this
duplication by making a fixture for `controller`:

<pre><code>
class TestUserSearchController(object):

    def test_some_search_controller_method(self, <strong>controller</strong>):
        # Test something using `controller`.

    def test_some_other_search_controller_method(self, <strong>controller</strong>):
        # Test something else using `controller`.

    @pytest.fixture
    def <strong>controller</strong>(self, user, pyramid_request):
        return activity.UserSearchController(user, pyramid_request)

    @pytest.fixture
    def user(self, factories):
        ...

    @pytest.fixture
    def pyramid_request(self):
        ...
</code></pre>

The `controller` fixture takes the `user` and `pyramid_request` fixtures as
arguments and returns the `UserSearchController` object. Now each test method
can just receive the `UserSearchController` as the `controller` argument and
use it directly.

Since `controller` takes both `user` and `pyramid_request` as arguments
pytest knows that, for each test that uses `controller`, it needs to run the
`user` and `pyramid_request` fixtures first before it can pass their results
into the `controller` fixture. What pytest does for each test method that uses
`controller` is something like this:

<pre><code>
test_obj                = TestSearchController()
factories_fixture       = conftest.factories()
<strong>user_fixture</strong>            = test_obj.user(factories=factories_fixture)  
<strong>pyramid_request_fixture</strong> = test_obj.pyramid_request()
controller_fixture      = test_obj.controller(user=<strong>user_fixture</strong>,
                                              pyramid_request=<strong>pyramid_request_fixture</strong>)
test_obj.test_something(controller=controller_fixture)
</code></pre>

Note that the `user` and `pyramid_request` fixtures _will_ be called, even
though the test doesn't directly use those fixtures (either as arguments or
via `usefixtures`) - the test uses the `controller` fixture, which uses the
`user` and `pyramid_request` fixtures, so the test indirectly uses the
`user` and `pyramid_request` fixtures as well.

Fixtures override other fixtures with the same name
---------------------------------------------------

In [Basic pytest Fixtures](2017-02-02-fixtures.md) we saw that `@pytest.fixture` functions
can be defined in `conftest.py` files, in the test modules themselves, or as
methods on the test classes. A fixture defined in a class overrides any fixtures
with the same name defined higher up in the module or in a `conftest.py` file.
Any test methods in that class that use that fixture will call the fixture
method from the class rather than the one defined elsewhere.
In the same way a fixture defined in a module overrides any fixtures with the
same name defined higher up in a `conftest.py` file.

By overriding fixtures a certain group of tests (a test class or a test module)
can use its own different version of that fixture, without having to come up
with a different fixture name. Another class or module can use another version.
And others can just use the "default" version defined higher up.

In the Hypothesis tests you'll often see fixture overriding used with the
`pyramid_request` fixture.
[A generic `pyramid_request` fixture is defined in `conftest.py`](https://github.com/hypothesis/h/blob/7d02ed90a1f3e6e38de30266dc5fcc31abef9f91/tests/h/conftest.py#L224)
and many tests simply use that generic fixture. But often tests need something
different - for example a request object that represents a request from a
logged-in user. [The `TestUserSearchController` class](https://github.com/hypothesis/h/blob/7d02ed90a1f3e6e38de30266dc5fcc31abef9f91/tests/h/views/activity_test.py#L563)
provides its own `pyramid_request` fixture that returns a logged-in request
from the user represented by the `user` fixture:

<pre><code>
class TestUserSearchController(object):

    def test_something(self, <strong>pyramid_request</strong>):
        ...

    ...

    @pytest.fixture
    def user(self, factories):
        return ...

    @pytest.fixture
    def <strong>pyramid_request</strong>(self, user):
        request = testing.DummyRequest(db=db_session, feature=fake_feature)
        request.auth_domain = text_type(request.domain)
        request.create_form = mock.Mock()
        request.matched_route = mock.Mock()
        request.registry.settings = pyramid_settings
        request.is_xhr = False

        pyramid_request.matchdict['username'] = user.username
        pyramid_request.authenticated_user = user

        return pyramid_request
</code></pre>

For `test_something(self, pyramid_request)` pytest will call
`TestSearchController.pyramid_request()` rather than the `pyramid_request`
fixture function in `conftest.py`.

An overriding fixture can take the "parent" fixture as argument
---------------------------------------------------------------

The problem with `TestUserSearchController`'s custom `pyramid_request` fixture
above is that it duplicates all the code from the generic `pyramid_request`
fixture in `conftest.py`. The first half a dozen lines of the method are the
same as from the other `pyramid_request`, and only the last couple of lines
contain code specific to `TestUserSearchController`.

Every test module or class that overrides `pyramid_request` with its own
custom version is going to duplicate the same lines.

To get around this, an overriding `pyramid_request` fixture can simply take the
higher up `pyramid_request` fixture by name as argument.
This is how [the real `TestUserSearchController.pyramid_request`](https://github.com/hypothesis/h/blob/7d02ed90a1f3e6e38de30266dc5fcc31abef9f91/tests/h/views/activity_test.py#L750)
works:

<pre><code>
class TestUserSearchController(object):

    ...

    @pytest.fixture
    def pyramid_request(self, <strong>pyramid_request</strong>, user):
        <strong>pyramid_request</strong>.matchdict['username'] = user.username
        <strong>pyramid_request</strong>.authenticated_user = user
        return <strong>pyramid_request</strong>
</code></pre>

The `pyramid_request` argument that pytest passes to this `pyramid_request`
fixture method will be the next higher up `pyramid_request` fixture that it
finds - a `pyramid_request` fixture defined in the test module or in a
`conftest.py` file. In this example it happens to be in `conftest.py`.
When a test method in `TestSearchController` uses the `pyramid_request`
feature, pytest does something like this:

<pre><code>
test_obj                       = TestUserSearchController()
factories_fixture              = conftest.factories()
user_fixture                   = test_obj.user(factories=factories_fixture)
<strong>higher_pyramid_request_fixture</strong> = conftest.pyramid_request()
<strong>lower_pyramid_request_fixture</strong>  = test_obj.pyramid_request(
    user=user_fixture,
    pyramid_request=<strong>higher_pyramid_request_fixture</strong>
)
test_obj.test_something(pyramid_request=<strong>lower_pyramid_request_fixture</strong>)
</code></pre>

Try not to over-reuse fixtures
------------------------------

We introduced fixtures by pointing out that they're an effective way to avoid
coupling test methods together like `setup()` and `teardown()` methods can - 
each test method just depends on whichever fixtures _that_ test method needs
and nothing else, rather than having a single `setup()` method that's run for
every test method in the class.

It's important to remember then, especially when using fixture overriding, not
to make a fixture method more complicated by trying to make a single complex
fixture that can be shared between many test methods with different requirements.

For example a test class may contain some test methods that require a Pyramid
request for a logged-in user, some that require an unauthenticated request,
some that require a request from a group administrator or a request with certain
query parameters, etc.

Don't struggle to build a complex `pyramid_request` fixture method in the class
that can meet all these needs, perhaps by returning multiple request objects or
a customizable request object etc.

It's easier just to write separate, independent fixtures and have each test
just use the one it needs:

```python
class TestUserSearchController(object):

    def test_with_unauthorized_request(self, unauthorized_request):
        ...

    def test_with_request_from_group_admin(self, group_admin_request):
        ...

    ...

    @pytest.fixture
    def unauthorized_request(self, pyramid_request):
        ...

    @pytest.fixture
    def group_admin_request(self, pyramid_request):
        ...
```

Both the `unauthorized_request` and the `group_admin_request` fixtures depend
on the generic `pyramid_request` fixture and then do different customization
to it. Each test that needs an unauthorized request uses that fixture, each
test that needs a group admin request uses that fixture. This is a clean and
simple way to avoid duplication while also not coupling tests together.

In the above example, if a single test method used _both_ the
`unauthorized_request` _and_ the `group_admin_request` fixtures it might not
work as you'd expect it to. Can you guess why?
Both of those fixtures depend on the same `pyramid_request` fixture, let's look
at what happens when a fixture gets used multiple times...

A test and a fixture can both use the same fixture
--------------------------------------------------

We've seen that test methods use fixtures by taking the fixture as an argument,
and that fixtures can also use other fixtures in the same way.
A useful technique can be to have a fixture that is both used by other fixtures
_and_ used by the test method itself.

For example, consider
[a test that the _Back_ link redirects back to the user page](https://github.com/hypothesis/h/blob/7d02ed90a1f3e6e38de30266dc5fcc31abef9f91/tests/h/views/activity_test.py#L706):

<pre><code>
class TestUserSearchController(object):

    ...

    def test_back_redirects_to_user_search(self, controller, <strong>user</strong>, pyramid_request):
        """It should redirect and preserve the search query param."""
        pyramid_request.params = {'q': 'foo bar', 'back': ''}

        result = controller.back()

        assert isinstance(result, httpexceptions.HTTPSeeOther)
        assert result.location == (
            'http://example.com/users/{username}?q=foo+bar'.format(
                username=<strong>user</strong>.username))

    @pytest.fixture
    def <strong>user</strong>(self, factories):
        return ...

    @pytest.fixture
    def pyramid_request(self, <strong>user</strong>):
        ...
        return pyramid_request
</code></pre>

In order to do its work `test_back_redirects_to_user_search()` needs both a
`pyramid_request` object representing an HTTP request from a logged-in user,
and it needs the `user` object for that logged-in user itself, so it takes both as arguments.
This means that the `user` fixture is used twice - once by the `pyramid_request`
fixture, and then again by the test itself. The important thing to understand
is that **the `user` fixture is only called once**, and the same user object
is passed first to the `pyramid_request` fixture and then to the test.
This is what pytest does:

<pre><code>
test_obj                = TestUserSearchController()
factories_fixture       = conftest.factories()
<strong>user_fixture</strong>            = test_obj.user(factories=factories_fixture)
pyramid_request_fixture = test_obj.pyramid_request(user=<strong>user_fixture</strong>)
controller_fixture      = test_obj.controller()
test_obj.test_back_redirects_to_user_search(
    controller=controller_fixture,
    user=<strong>user_fixture</strong>,
    pyramid_request=pyramid_request_fixture)
</code></pre>

Multiple fixtures can both use the same fixture
-----------------------------------------------

Just as a test and a fixture can both use the same other fixture,
multiple fixtures can all use the same other fixture as well.
You can see an example of this in
[`TestSearchController`'s `controller` and `pyramid_request` fixtures](https://github.com/hypothesis/h/blob/7d02ed90a1f3e6e38de30266dc5fcc31abef9f91/tests/h/views/activity_test.py#L745),
both of which depend on its `user` fixture:

<pre><code>
class TestUserSearchController(object):

    ...

    @pytest.fixture
    def controller(self, <strong>user</strong>, pyramid_request):
        return activity.UserSearchController(user, pyramid_request)

    @pytest.fixture
    def pyramid_request(self, <strong>user</strong>):
        ...
        return pyramid_request

    @pytest.fixture
    def <strong>user</strong>(self):
        return ...
</code></pre>

Again, the `user` fixture will be called only once and the one user object that
it returns will be passed to both the `pyramid_request` and `controller` fixtures
(as well as any other fixtures that the test uses, directly or indirectly,
that take the `user` fixture, and to the test itself if it takes the `user`
fixture directly).

Pytest figures out what order it needs to call the fixtures in according to
their dependencies - it knows that it needs to call the `user` fixture first
in order to get the user object to pass in to the `pyramid_request` and
`controller` fixtures. Notice that the `controller` fixture actually depends on
the `pyramid_request` fixture as well - so pytest knows that it has to call
_both_ `user` and `pyramid_request` before it can call `controller`.

Conclusion
----------

These last couple of posts have covered most of the fixture-related techniques
that you'll find in the Hypothesis Python tests. We haven't covered _everything_,
check out [pytest's documentation on fixtures](http://docs.pytest.org/en/latest/fixture.html)
for all the details (for example:
[parametrizing fixtures](http://docs.pytest.org/en/latest/fixture.html#parametrizing-fixtures)
and [inspecting the fixture request context](http://docs.pytest.org/en/latest/fixture.html#fixtures-can-introspect-the-requesting-test-context)),
but you should now have enough of a basis to figure out what's going on with
all these fixtures in our tests.
