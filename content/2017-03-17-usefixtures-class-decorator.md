Title: usefixtures as a Class Decorator
Tags: Python Unit Tests at Hypothesis
Alias: /post/usefixtures-class-decorator/

In [the fixtures post](/posts/fixtures) we saw that
[`usefixtures`](https://docs.pytest.org/en/latest/fixture.html?#using-fixtures-from-classes-modules-or-projects)
is a way for a test to use a fixture without taking it as an argument:

```python
@pytest.mark.usefixtures('routes')
def test_something():
    ...
```

The test doesn't take the `routes` fixture as a method argument, and doesn't
need access to the `routes` fixture in the test body, but the test _does_ need
pytest to call the `routes` fixture function for it before calling the test.
The `@pytest.mark.usefixtures('routes')` decorator on the test function tells
pytest to do that.

You also can put a `@pytest.mark.usefixtures(...)` decorator on a test **class**
and pytest will automatically call those fixtures for every test method in the
class, even if the methods themselves don't take the fixtures as arguments.

We often use this with [`patch`-based fixtures](/posts/patch) when **all**
tests for a given function should ensure that the function under test uses a
mock version of an imported library and it would be a mistake for any one of
this function's tests to be missing the fixture and use the real library.

For example, [h/views/api.py::create()](https://github.com/hypothesis/h/blob/ca1681203aff5ee176fd880cb01fb04f1c7e1a5a/h/views/api.py#L207)
is the view function that's called when someone `POST`s a new annotation to the
`https://hypothes.is/api/annotations` URL. It calls the `storage` module
to save the new annotation to the database. `storage` has its own tests and we
never want any of the tests for `create()` to be accessing the real database,
so we always want to ensure that `storage` is replaced with a mock object for
all of `views.py::create()`'s tests. This is done with a `usefixtures()` on the
test class:

```python
@pytest.mark.usefixtures('storage')
class TestCreate(object):

    def test_something(self):
        # The storage fixture will be used in this test, even though the test
        # method itself didn't declare it.

    # If some tests _do_ want to use the mock storage object in their test
    # method bodies, they can just take the fixture as an argument as usual.
    def test_it_creates_the_annotation_in_storage(self, storage):
        ... # (Call the create() view to create an annotation)

        # Test that it would have saved the annotation to storage.
        storage.create_annotation.assert_called_once_with(...)

    @pytest.fixture
    def storage(self, patch):
        return patch('h.views.api.storage')
```

The `@pytest.mark.usefixtures('storage')` class decorator means that
pytest will automatically call the `storage()` fixture before **every** test
method in the `TestCreate` class, whether the test method declares the fixture
itself or not. If any particular test method wants to use the fixture value it
can just have an argument named `storage`, as with any other fixture, but test
methods that don't need to use the fixture value don't need to have the
argument.

Using `usefixtures` as a test class decorator reduces the number of boilerplate
and duplicate lines by not having to put a `usefixtures` decorator on every
test method, reduces the chances of a mistake where one test method that should
be using a mock is instead using the real dependency because it's missing a
`usefixtures` decorator, and is one more reason to group test methods into
classes.

In the next and last post in the tutorial we'll cover one final technique used
in the Hypothesis Python tests - [matcher objects](/2017/05/12/matchers/).
