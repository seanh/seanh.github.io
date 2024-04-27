Title: Arrange, Act, Assert
Tags: Python Unit Tests at Hypothesis
Alias: /post/arrange-act-assert/

The tests that we've written so far (see [Writing Simple Python Unit Tests](2017-01-28-writing-tests.md)) have been simple enough to fit in a single
line of code:

```python
def test_validate_url_returns_an_http_url_unmodified():
    assert validate_url('http://github.com/jimsmith') == 'http://github.com/jimsmith'
```

This line of code actually does three things:

1. It creates a string to be passed to `validate_url()` as argument.
2. It calls `validate_url()`, passing the string argument.
3. It asserts something about the results of calling `validate_url()`.

Here's the function with the three steps separated out:

```python
def test_validate_url_returns_an_http_url_unmodified():
    url = 'http://github.com/jimsmith'

    validated_url = validate_url(url)
    
    assert validated_url == 'http://github.com/jimsmith'
```

For tests as simple as this one we would normally collapse the three steps into
a single line. But for more complex tests the test code will be clearer if it's
separated into three steps, with an empty line between each step:

1. **Arrange**: create and setup any objects that you need for the test
   (for example, arguments that you need to pass to the function under test).

2. **Act**: call the function under test, once only.

3. **Assert**: use Python's `assert` to test something about the result of
   calling the function.

For example, [remove_nipsa_action()](https://github.com/hypothesis/h/blob/8d11e918005581f35f97268e9470eb3c34a6b416/h/tasks/nipsa.py#L24)
is a function that takes an Elasticsearch index name and an annotation and
returns an Elasticsearch action that removes the NIPSA flag from the
annotation. For the purposes of this tutorial it doesn't really matter what a
"remove nipsa action" is, just know that `remove_nipsa_action()` takes an
annotation (in the form of a dictionary) as argument and returns an
Elasticsearch action (also a dictionary) in an expected format.

Here's one of the [tests for this function](https://github.com/hypothesis/h/blob/8d11e918005581f35f97268e9470eb3c34a6b416/tests/h/tasks/nipsa_test.py):

```python
def test_remove_nipsa_action():
    # 1. Arrange: create the annotation dict that we need to pass to
    #    remove_nipsa_action().
    annotation = {"_id": "test_id", "_source": {"nipsa": True, "foo": "bar"}}

    # 2. Act: call remove_nipsa_action(), once only.
    action = remove_nipsa_action("bar", annotation)

    # 3. Assert something about the result.
    assert action == {
        "_op_type": "index",
        "_index": "bar",
        "_type": "annotation",
        "_id": "test_id",
        "_source": {"foo": "bar"},
    }
```

This test still only creates a single object in the _arrange_ step, and only
makes a single assertion in the _assert_ step. Even more complex tests may need
to create multiple objects before calling the function, and then make
multiple assertions at the end.

Almost all Hypothesis tests follow the arrange, act, assert recipe.
This three step recipe is usually a good way to write a test.
The consistency makes the tests easier to understand, and the recipe also
clearly separates setup, what is being tested (the function call), and
verification.

Arrange act assert also discourages the writing of complex tests that try to do
too many things at once. If a test is complicated it can become hard to understand
what the test is for, what it's supposed to be testing, especially when a future
change to the code causes the test to start failing.

For more, see [Arrange Act Assert on wiki.c2.com](http://wiki.c2.com/?ArrangeActAssert).

**Tip**: Try writing the assert part of a test first, and then filling in the
first two steps.

Naming tests
------------

As well as following the arrange act assert recipe, it can really help to make
the intent of your test clear if you give the test function a good name.
[The name of a test method should clearly explain the intent of the test](http://docs.pylonsproject.org/en/latest/community/testing.html#rule-name-tcms-to-indicate-what-they-test).
The names of failing tests are printed out when the test fails, if they're
named well then the developer can often tell what has gone wrong from the names
of the failing tests alone, without having to look into the test code.
When you do have to look into the code, a good name helps to communicate what
the test is intended to be testing.

Long function names are fine for test functions, since we don't write code
that calls our test functions (pytest calls them automatically for us) there's
no benefit to excessive terseness.

`test_validate_url()` or `test_validate_url_1()` are poor test names.
`test_validate_url_with_a_valid_http_url()` is better.
`test_validate_url_returns_a_valid_http_url_unmodified()` may be even better.
