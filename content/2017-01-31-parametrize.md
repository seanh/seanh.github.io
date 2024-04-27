Title: Parametrizing Python Tests
Tags: Python Unit Tests at Hypothesis
Alias: /post/parametrize/

This post covers testing multiple test cases at once using
`@pytest.mark.parametrize()`.
In [Writing Simple Tests](/posts/writing-tests) we tested the `validate_url()`
function that validates the links that users add to their profiles.
`util.py` also contains a [validate_orcid()](https://github.com/hypothesis/h/blob/8d11e918005581f35f97268e9470eb3c34a6b416/h/accounts/util.py#L36)
function for validating the [ORCID](https://orcid.org/) ID's that users add
to their profiles (an ORCID is a unique identifier for a scientific author):

<img src="{static}/images/user-profile-form.png">

```python
def validate_orcid(orcid):
    """
    Validate an ORCID.

    Verify that an ORCID conforms to the structure described at
    http://support.orcid.org/knowledgebase/articles/116780-structure-of-the-orcid-identifier

    Returns the normalized ORCID if successfully parsed or raises a ValueError
    otherwise.
    """
    ...
```

We want to test that validation succeeds (returning the string unmodified,
without raising an exception) for a variety of valid ORCIDs.
We could test this by writing a separate test method for each valid ORCID that
we want to test, but that would be a lot of duplication - each test method
would be exactly the same except for the ORCID used.
Another way we could do this is with a `for` loop in a single test method:

```python
def test_validate_orcid_accepts_valid_ids():
    for orcid_id in ['0000-0002-1825-0097', '0000-0001-5109-3700', '0000-0002-1694-233X']:,
        assert validate_orcid(orcid_id) == orcid_id
```

This is better - there's no duplication in the test code.
You could say that this breaks the [arrange, act, assert](/posts/arrange-act-assert)
pattern because it calls the method under test three times, not once. But there
is only one line of code that calls the method under test, it just happens to
be a line inside a loop, so I think it's okay.
This approach does have the disadvantage that it clutters up the body of our
test method with a `for` loop. If the function we were testing had more than
one parameter and we wanted to test it with different combinations of multiple
parameters then the loop and the clutter would be more complicated.

Pytest gives us a better way to write this kind of test -
[@pytest.mark.parametrize()](http://doc.pytest.org/en/latest/parametrize.html):
 
```python
@pytest.mark.parametrize('orcid', [
    '0000-0002-1825-0097',
    '0000-0001-5109-3700',
    '0000-0002-1694-233X',
])
def test_validate_orcid_accepts_valid_ids(orcid):
    assert validate_orcid(orcid) == orcid
```

The `parametrize()` causes pytest to run this function three times, each time
passing the next one of the ORCIDs as the `orcid` argument to the test.

The first argument to `parametrize()`, called the `argnames` argument, is the
string `'orcid'`:

<pre><code>@pytest.mark.parametrize(<strong>'orcid'</strong>, [
    '0000-0002-1825-0097',
    '0000-0001-5109-3700',
    '0000-0002-1694-233X',</code></pre>

This tells pytest the name of the test parameter that we're going to be
parametrizing. Pytest finds the test method parameter with the matching name:

<pre><code>@pytest.mark.parametrize('<strong>orcid</strong>', [
    '0000-0002-1825-0097',
    '0000-0001-5109-3700',
    '0000-0002-1694-233X',
])
def test_validate_orcid_accepts_valid_ids(<strong>orcid</strong>):
    assert validate_orcid(orcid) == orcid</code></pre>

The second argument to `parametrize()` is the `argvalues` argument, this is
the list of values that pytest will pass to the test function's `orcid` parameter:

<pre><code>@pytest.mark.parametrize('orcid', <strong>[
    '0000-0002-1825-0097',
    '0000-0001-5109-3700',
    '0000-0002-1694-233X',
]</strong>)
def test_validate_orcid_accepts_valid_ids(orcid):
    assert validate_orcid(orcid) == orcid</code></pre>

Pytest takes the first argument from this list and calls
`test_validate_orcid_accepts_valid_ids('0000-0002-1825-0097')`, then it takes
the second argument and calls
`test_validate_orcid_accepts_valid_ids('0000-0001-5109-3700')`,
and so on.

So essentially we've got three separate tests in one.
This separates test data (in this case, the different ORCIDs being tested)
from test logic (the code in the body of the test method), and avoids
cluttering up the method body with a `for` loop.


### parametrize() with multiple parameters

In the example above we parametrized just a single parameter - `orcid`.
Where `parametrize()` really comes into its own is when you have a test
function with multiple parameters. You can reduce what might have been many
separate tests down to just one.

As an example, let's look at the tests for the
[update_web_uri()](https://github.com/hypothesis/h/blob/a62e378eb45a8bdef2dff17c2ed4d16d8310b64d/src/memex/models/document.py#L52) method. (Here's [the real tests for this method](https://github.com/hypothesis/h/blob/a62e378eb45a8bdef2dff17c2ed4d16d8310b64d/tests/memex/models/document_test.py#L131).)

When someone annotates a document using Hypothesis we collect many URIs for that
document. The URL from the browser's location bar is one URI (which we call a
"self-claim" URI). Some web pages contain canonical links in the HTML, like:

```html
<link rel="canonical" href="http://example.com/wordpress/seo-plugin/">
```

We collect these and call them "rel-canonical" URIs for the document.
There can also be `rel="alternate"` and `rel="shortlink"` URIs in an HTML
document. And there are many other kinds of document URIs that we collect as well.

When we want to display the domain name of a document (e.g. `www.example.com`)
on a Hypothesis page, or render a link to a document, we need to consider all
of the different URIs for that document that we've collected into our database
and select the "best" one to use.

We call this best URI the document's `web_uri`, and the `update_web_uri()`
method is responsible for updating it whenever we receive new URIs for a
document:

```python
def update_web_uri(self):
    """
    Update the value of the self.web_uri field.

    Set self.web_uri to the "best" http(s) URL from self.document_uris.

    Set self.web_uri to None if there's no http(s) DocumentURIs.

    """
```

We want to test the behaviour of `update_web_uri()` with many different
combinations of URIs that a document might have - when we have just one URI
for a document it should just choose that one URI, for different possible
combinations of multiple types of URI it should choose the one that we think is
best in each case. Here's what the tests for `update_web_uri()` could look
like:

```python
class TestDocumentWebURI(object):

    def test_given_a_single_http_or_https_uri_it_returns_it(self, factories):
        document = factories.Document()
        uri = 'http://example.com'
        factories.DocumentURI(uri=uri, type='self-claim', document=document)

        document.update_web_uri()

        assert document.web_uri == uri

    def test_if_there_are_no_http_or_https_uris_it_returns_None(self, factories):
        document = factories.Document()
        factories.DocumentURI(uri='ftp://example.com', type='self-claim',
                              document=document)
        factories.DocumentURI(uri='android-app://example.com',
                              type='rel-canonical', document=document)
        factories.DocumentURI(uri='urn:x-pdf:example',
                              type='rel-alternate', document=document)
        factories.DocumentURI(uri='doi:http://example.com',
                              type='rel-shortlink', document=document)

        document.update_web_uri()

        assert document.web_uri is None

    ...
```

... and so on, there were several more tests for the expected results given
different combinations of URIs. All of these tests have the same test logic:

1. Create a `Document` with some `DocumentURI`s
2. Call `update_web_uri()`
3. Check that `web_uri` is equal to the expected URI

They differ only in the list of `DocumentURI`s that's created and in the value
that we expect `web_uri` to have at the end. With `parametrize()` we can
combine all of these into a single test.

Here's what the beginning of a `parametrize()` call for this test might look
like:

```python
@pytest.mark.parametrize('document_uris,expected_web_uri', [
    # Given a single http or https URL it just uses it.
    ([('http://example.com',  'self-claim')],    'http://example.com'),
    ([('https://example.com', 'self-claim')],    'https://example.com'),
    ...
])
def test_update_web_uri(self, document_uris, factories, expected_web_uri):
    document = factories.Document()

    for docuri_tuple in document_uris:
        factories.DocumentURI(uri=docuri_tuple[0], type=docuri_tuple[1],
                              document=document)

    document.update_web_uri()

    assert document.web_uri == expected_web_uri
```

Here we're parametrizing **two** arguments to the test method, not just one
as before. The `argnames` argument to `parametrize()` gives two argument names
separated by a comma:

<pre><code>@pytest.mark.parametrize('<strong>document_uris,expected_web_uri</strong>', [
    # Given a single http or https URL it just uses it.
    ([('http://example.com',  'self-claim')],    'http://example.com'),
    ([('https://example.com', 'self-claim')],    'https://example.com'),
    ...
])
def test_update_web_uri(self, <strong>document_uris</strong>, factories, <strong>expected_web_uri</strong>):
    ...</code></pre>

Notice that the test function also has a third argument, `factories`.
This is the same factories for creating test objects that [we saw earlier](/posts/factories).
Having this argument in there doesn't do any harm - it doesn't confuse parametrize.
And it doesn't even matter that the `factories` argument appears in-between
`document_uris` and `expected_web_uri` - the order of the parameters doesn't
matter, pytest looks at their names to figure out what they are.

Since we're now parametrizing two parameters instead of one, the `argvalues`
argument to `parametrize()` becomes a list of two-tuples:

<pre><code>@pytest.mark.parametrize('document_uris,expected_web_uri', <strong>[
    # Given a single http or https URL it just uses it.
    ([('http://example.com',  'self-claim')],    'http://example.com'),
    ([('https://example.com', 'self-claim')],    'https://example.com'),
    ...
])</strong>
def test_update_web_uri(self, document_uris, factories, expected_web_uri):
    ...</code></pre>

Pytest will first call the test function passing the values from the first
two-tuple as arguments:

<pre><code>@pytest.mark.parametrize('document_uris,expected_web_uri', [
    # Given a single http or https URL it just uses it.
    <strong>([('http://example.com',  'self-claim')],    'http://example.com')</strong>,
    ([('https://example.com', 'self-claim')],    'https://example.com'),</code></pre>

it'll call:

<pre><code>test_update_web_uri(<strong>[('http://example.com',  'self-claim')]</strong>, factories, <strong>'http://example.com'</strong>):</code></pre>

It'll then take the second two-tuple:

<pre><code>@pytest.mark.parametrize('document_uris,expected_web_uri', [
    # Given a single http or https URL it just uses it.
    ([('http://example.com',  'self-claim')],    'http://example.com'),
    <strong>([('https://example.com', 'self-claim')],    'https://example.com')</strong>,</code></pre>

and run the test with those arguments:

<pre><code>test_update_web_uri(<strong>[('https://example.com',  'self-claim')]</strong>, factories, <strong>'https://example.com'</strong>):</code></pre>

and so on.

Here's the full, final version of the test with all parametrized cases:

```python
@pytest.mark.parametrize('document_uris,expected_web_uri', [
    # Given a single http or https URL it just uses it.
    ([('http://example.com',  'self-claim')],    'http://example.com'),
    ([('https://example.com', 'self-claim')],    'https://example.com'),
    ([('http://example.com',  'rel-canonical')], 'http://example.com'),
    ([('https://example.com', 'rel-canonical')], 'https://example.com'),
    ([('http://example.com',  'rel-shortlink')], 'http://example.com'),
    ([('https://example.com', 'rel-shortlink')], 'https://example.com'),

    # Given no http or https URLs it sets web_uri to None.
    ([], None),
    ([
        ('ftp://example.com',              'self-claim'),
        ('android-app://example.com',      'rel-canonical'),
        ('urn:x-pdf:example',              'rel-alternate'),
        ('doi:http://example.com',         'rel-shortlink'),
     ], None),

    # It prefers self-claim URLs over all other URLs.
    ([
        ('https://example.com/shortlink',  'rel-shortlink'),
        ('https://example.com/canonical',  'rel-canonical'),
        ('https://example.com/self-claim', 'self-claim'),
     ], 'https://example.com/self-claim'),

    # It prefers canonical URLs over all other non-self-claim URLs.
    ([
        ('https://example.com/shortlink',  'rel-shortlink'),
        ('https://example.com/canonical',  'rel-canonical'),
     ], 'https://example.com/canonical'),


    # If there's no self-claim or canonical URL it will return an https
    # URL of a different type.
    ([
        ('ftp://example.com',              'self-claim'),
        ('urn:x-pdf:example',              'rel-alternate'),

        # This is the one that should be returned.
        ('https://example.com/alternate',  'rel-alternate'),

        ('android-app://example.com',      'rel-canonical'),
        ('doi:http://example.com',         'rel-shortlink'),
     ], 'https://example.com/alternate'),

    # If there's no self-claim or canonical URL it will return an http
    # URL of a different type.
    ([
        ('ftp://example.com',              'self-claim'),
        ('urn:x-pdf:example',              'rel-alternate'),

        # This is the one that should be returned.
        ('http://example.com/alternate',   'rel-alternate'),

        ('android-app://example.com',      'rel-canonical'),
        ('doi:http://example.com',         'rel-shortlink'),
     ], 'http://example.com/alternate'),
])
def test_update_web_uri(self, document_uris, factories, expected_web_uri):
    document = factories.Document()

    for docuri_tuple in document_uris:
        factories.DocumentURI(uri=docuri_tuple[0], type=docuri_tuple[1],
                              document=document)

    document.update_web_uri()

    assert document.web_uri == expected_web_uri
```

Parametrize is a great feature of pytest that can really help to test many
cases while minimising the amount of test code. You should always be on the
look out for groups of test methods that could be reduced to a single method
by using parametrize, and use if as often as possible.
