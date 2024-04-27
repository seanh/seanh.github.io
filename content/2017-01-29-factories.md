Title: Python Test Factories with factory_boy
Tags: Python Unit Tests at Hypothesis
Alias: /post/factories/

**Factories** are a really quick and easy way to create realistic objects to
use in your tests. For example if you're testing the code for editing user
accounts your tests may need some `User` objects to test with, if you're
testing groups you may need to create a lot of `Group` objects, tests for
the annotations API may need to create `Annotation` objects to test updating
and deleting them, etc.

It's not always easy to create these kinds of objects, their classes in the h
code may require a lot of different arguments that would take time to write,
clutter up your test code, and make tests easy to break.  In some cases there
are dependencies, for example that you can't have two users with the same
username, and other complexities. Factories exist to make all this really
simple and easy.

For example, let's look at the tests for
[tag_uri_for_annotation()](https://github.com/hypothesis/h/blob/51f07c93b4cd2313118b8ba7625337c9586011cc/h/feeds/util.py#L10).
This is a function that takes a [memex.models.Annotation](https://github.com/hypothesis/h/blob/51f07c93b4cd2313118b8ba7625337c9586011cc/src/memex/models/annotation.py#L18)
object and returns a [tag URI](https://tools.ietf.org/html/rfc4151) for it.
Here's (a slightly simplified version of) one of the tests for it:

```python
def test_tag_uri_for_annotation(factories):
    annotation = factories.Annotation(
        created=datetime.datetime(year=2015, month=3, day=19),
        target_uri="http://www.example.com/example_page")

    tag_uri = util.tag_uri_for_annotation(annotation)

    assert tag_uri == "tag:example.com,2015-09:" + annotation.id
```

`factories.Annotation()` creates an `Annotation` object for us to pass into
the `tag_uri_for_annotation()` function that we're testing. Since we care about
the `created` date and `target_uri` of the annotation (they form parts of the
expected tag URI) we pass those in to `factories.Annotation()` as arguments,
but we leave all of the other `Annotation` fields unspecified and `factories`
automatically generates suitable values for us. This makes the test easier to
write (we only have to type out the fields that we're interested in) and easier
to read (the test isn't cluttered up with the values of fields that are
necessary to create an `Annotation` but that aren't relevant to this particular
test).

Note that we also use `annotation.id` in our assertion. The `id` for an
`Annotation` object isn't generated until that annotation is added to the
database, so our test would need to get a db connection and add the annotation
to it. `factories` does that for us, as well.

As I said, we can simply omit any of the fields of the `Annotation` class and
`factories` will generate suitable values for them. Here's another test that
specifies the `created` date but doesn't care about the `target_uri`:

```python
def test_feed_from_annotations_item_guid(factories):
    """Feed items should use the annotation's tag URI as their GUID."""
    annotation = factories.Annotation(
        created=datetime.datetime(year=2015, month=3, day=11))

    feed = rss.feed_from_annotations([annotation])

    assert feed['entries'][0]['guid'] == (
        'tag:hypothes.is,2015-09:' + annotation.id)
```

If we just want an annotation and don't care about the values of _any_ of its
fields than we can just call `factories.Annotation()` with no arguments. If we
want more than one annotation, we just call it multiple times:

```python
def test_feed_from_annotations_with_3_annotations(factories):
    """If there are 3 annotations it should return 3 entries."""
    annotations = [factories.Annotation(), factories.Annotation(),
                   factories.Annotation()]

    feed = rss.feed_from_annotations(annotations)

    assert len(feed['entries']) == 3
```

factory_boy
-----------

`factories` is implemented using the [factory_boy](https://factoryboy.readthedocs.io/)
library, and h comes with factories for creating users, documents, annotations,
groups, and others. See [tests/common/factories.py](https://github.com/hypothesis/h/blob/51f07c93b4cd2313118b8ba7625337c9586011cc/tests/common/factories.py)
and [tests/memex/factories.py](https://github.com/hypothesis/h/blob/51f07c93b4cd2313118b8ba7625337c9586011cc/tests/memex/factories.py)
for all the available classes.

Let's take a quick tour of factory_boy features in a Python shell:

```pycon
$ hypothesis --dev shell
>>> from tests.common import factories
>>> 
```

Each time you call `factories.User()` (for example) it returns a new `User`
object with different, realistic but randomly generated values for all of its
fields:

```pycon
>>> first_user = factories.User()
>>> first_user.__class__
h.models.user.User
>>> first_user.username
u'pamela72'
>>> second_user = factories.User()
>>> second_user.username
u'christopher86'
```

You can specify the values for any fields you want as keyword arguments, and
the other fields will still be automatically generated:

```pycon
>>> user = factories.User(email='example@email.com', nipsa=True)
>>> user.email
'example@email.com'
>>> user.nipsa
True
>>> user.username
u'jonathanmathis'
```
Sometimes an object from one factory can be passed as an argument to another
factory. For example every annotation has a document. Normally the annotation
factory would generate a new random document for each annotation:

```pycon
>>> annotation = factories.Annotation()
>>> annotation.document
<Document 1>
>>> annotation_2 = factories.Annotation()
>>> annotation_2.document
<Document 2>
```

To create a test annotation of a particular test document you can pass the
test document as an argument to the annotation factory:

```pycon
>>> document = factories.Document()
<Document 3>
>>> annotation = factories.Annotation(document=document)
>>> annotation.document
<Document 3>
>>> second_annotation = factories.Annotation(document=document)
>>> second_annotation.document
<Document 3>
```

Here's a test that makes use of this technique:

```python
def test_feed_from_annotations_item_titles(factories):
    """Feed items should include the annotation's document's title."""
    document = factories.Document(title='Hello, World')
    annotation = factories.Annotation(document=document)

    feed = rss.feed_from_annotations([annotation])

    assert feed['entries'][0]['title'] == 'Hello, World'
```

Creating objects without adding them to the database
----------------------------------------------------

Normally, `factories` adds objects that you create to the test database:

```pycon
>>> annotation = factories.Annotation()  # This adds annotation to the db.
```

This shouldn't do any harm (the database is wiped after each test, before
running the next test function) but it can make the tests unnecessarily slow if
they don't really need to be writing to the db. Tests for a `models.py` file
probably do really need to use the db. But tests for a `views.py` file,
though they may need model objects such as `User`s and `Annotation`s to test
with, probably _don't_ really need these objects to be written to the db.

To create a factory object without writing it to the db, use the `build()`
method. This works with any factory class:

```pycon
>>> annotation = factories.Annotation.build()  # A real Annotation object is
                                               # created but not added to the
                                               # database.
```

It's probably best to use `build()` whenever you can, as the tests will be a
tiny bit faster (and this will add up over time as more and more tests are
written).

One thing to be aware of is that the values of some fields are generated
_when the object is added to the database_. For example annotation `id`s are
generated like this. An annotation created with `build()` has no `id`:

```pycon
>>> annotation = factories.Annotation.build()
>>> annotation.id is None
True
```

If you need an `id`, you can probably get away with specifying a fake one:

```pycon
>>> annotation = factories.Annotation.build(id='test_id')
>>> annotation.id is None
'test_id'
```

You'll find `factories` used all over the Hypothesis tests, and you should try
to use it whenever possible to create the test objects that you need.
