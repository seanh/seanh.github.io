Title: Testing that an Exception is Raised with pytest.raises
Tags: Python Unit Tests at Hypothesis
Alias: /post/testing-that-exceptions-are-raised/

[Previously](/posts/writing-tests) we tested that the
[validate_url() function](https://github.com/hypothesis/h/blob/8d11e918005581f35f97268e9470eb3c34a6b416/h/accounts/util.py#L9)
returns the given URL if it's a valid URL. If the given URL is _not_ valid then
`validate_url()` is supposed to raise a `ValueError` exception.
To test this we need to use [pytest.raises()](https://docs.pytest.org/en/latest/reference.html#pytest.raises).
Here is a test that _expects_ `validate_url()` to raise a `ValueError`:

```python
def test_validate_url_rejects_urls_without_domains():
    with pytest.raises(ValueError):
        validate_url('http:///path')
```

This test will fail if the block of code inside the `with` statement _doesn't_
raise `ValueError`, otherwise the test will pass.

It's often a good idea to use the `match` argument to `pytest.raises` to
ensure that the exception raised was the one you expected, and not some other
exception of the same class. `match` is a regular expression that has to match
against the string representation of the exception or the test will fail:

<pre><code>def test_validate_url_rejects_urls_without_domains():
    with pytest.raises(ValueError, <strong>match="^Not a valid URL\: .*"</strong>):
        validate_url('http:///path')</code></pre>

Alternatively, if your code raises a specific [custom exception class](../../_posts/2019-06-20-python-custom-exception-classes.md)
then `match` may be unnecessary because that type of exception wouldn't be
raised for any other reason.

There's also [`pytest.warns()`, for testing that code raises a warning](https://docs.pytest.org/en/latest/reference.html#pytest.warns)
in the same way.

Testing that a certain message was logged works differently: use [pytest's builtin `caplog` fixture](https://docs.pytest.org/en/latest/logging.html#caplog-fixture).
