Title: The Problem with Mocks
Tags: Python Unit Tests at Hypothesis
Alias: /post/the-problem-with-mocks/

[The first post about mocks](2017-03-17-mock.md) covered the basics of how to use
[Python's mock library](http://www.voidspace.org.uk/python/mock/).
Using mocks has many advantages (which we'll discuss in
[When and When Not to Use Mocks](/2017/04/25/when-to-use-mocks/)
but they also have a downside: mocks can get out of sync with the real code
that they're mocking, which can mean that
**the tests might pass, even if the code is wrong**. In this post we'll explain
how this problem with mocks works, and some advanced features of the `mock`
library that you can use to minimize the problem.

Consider this class `Bar`, a class `Foo` that uses it, and a test for `Foo`:

```pycon
>>> import mock
>>> 
>>> class Bar(object):
...     def some_method(self, some_arg):
...         pass
... 
>>> class Foo(object):
...     def __init__(self, bar):
...         # Foo calls a method that does not exist on Bar.
...         bar.a_method(an_arg=23)
... 
>>> def test_foo_does_not_crash():                                              
...     Foo(mock.MagicMock())
... 
>>> # The test passes, even though the code is wrong:
>>> test_foo_does_not_crash()
>>> 
>>> # In production, when a real Bar object is used, Foo would crash:
>>> Foo(Bar())
Traceback (most recent call last):
  ...
AttributeError: 'Bar' object has no attribute 'a_method'
```

The `Foo` class is wrong - it calls a `Bar` method that doesn't exist, passing
in an argument that doesn't exist. In production `Foo` will crash. But the test
for `Foo` passes because it uses a `MagicMock` in place of a `Bar` object. You
can call any method with any arguments on a `MagicMock`, so `Foo` doesn't
crash.

This was a simple example, but there are all sorts of ways that mock objects
can be out of sync with the real objects they replace, causing tests to pass
even though the code is wrong:

* The mock may have **attributes**, **methods** or **arguments** that the real
  object doesn't
* The mock's **return values** may differ from the real object's, for example
  it may return a different type of object that has different attributes
* The mock's **side effects** and **behavior** may differ from the real object's,
  for example maybe the mock fails to raise an exception when the real object
  would do

These problems are most likely to occur when dependency code is modified and
you forget to update the code that uses it - the user code goes out of sync
with the dependency code but the tests still pass because they use mocks.

Autospeccing - a partial solution to the problem with mocks
-----------------------------------------------------------

To avoid the problem with mocks we want an automatic way to create mock objects
that have only the attributes, methods and arguments that the real objects
have, that have the same return values, side effects and behaviors as the real
objects, and that are updated automatically when the real classes are changed.

Unfortunately there's no perfect solution to this, but Python's mock library
does have a feature called 
[autospeccing](http://www.voidspace.org.uk/python/mock/helpers.html#autospeccing)
that gets us some of the way there.

Mock's [`create_autospec()`](http://www.voidspace.org.uk/python/mock/helpers.html?highlight=create_autospec#mock.create_autospec)
function creates an object that has only the attributes, methods and arguments
that the real objects would have, and that crashes just like the real objects
would if you try to access something that doesn't exist:

```pycon
>>> # Create a mock version of the Bar class by passing the real Bar class to
>>> # create_autospec():
>>> MockBar = mock.create_autospec(Bar, spec_set=True)                                         
>>>
>>> # Now use the mock bar class to make a mock bar object:
>>> mock_bar = MockBar()
>>>
>>> # You can call methods that real Bar objects would have, passing arguments
>>> # that real Bar objects have:
>>> mock_bar.some_method(some_arg=23)
<MagicMock name='mock().some_method()' id='139778195937360'>
>>>
>>> # Passing an argument that doesn't exist crashes:
>>> mock_bar.some_method(some_arg=23, another_arg=True)
Traceback (most recent call last):
  ...
TypeError: too many keyword arguments {'another_arg': True}
>>>
>>> # Passing too many positional arguments also crashes:
>>> mock_bar.some_method(23, True)                                                             
Traceback (most recent call last):
  ...
TypeError: too many positional arguments
>>>
>>> # Passing too few arguments or missing a required argument also crashes:
>>> mock_bar.some_method()                                                                     
Traceback (most recent call last):
  ...
TypeError: 'some_arg' parameter lacking default value
>>>
>>> # Calling a method that doesn't exist crashes:
>>> mock_bar.a_method()                                                                        
Traceback (most recent call last):
  ...
AttributeError: Mock object has no attribute 'a_method'
```

As well as calling methods, accessing attributes that don't exist will also
crash.

Trying to _call_ the mock object, as in `mock_bar()`, will work if a real `Bar`
object would be callable (and will accept only the arguments the real objects
do). If real `Bar` objects aren't callable then calling a mock bar object will
also crash.

Notice that **we never specified the method name `some_method` or its argument
`some_arg`**. `create_autospec()` figured these out automatically from the
real `Bar` class. Tests that use `create_autospec()` aren't coupled to the
dependencies that they mock - if the `Bar` class changes then the next time you
run the tests `create_autospec()` will create mocks that match the new `Bar`
code, without any changes to the test code.

The `spec_set=True` in the `MockBar = mock.create_autospec(Bar, spec_set=True)`
call prevents you from **writing** the value of an attribute
that doesn't exist on the real class, `mock_bar.does_not_exist = True` will
crash with `AttributeError`. Without `spec_set=True` **reading** attributes
that don't exist will crash but **writing** them will succeed.

In this case we used `create_autospec()` to create a `MockBar` _class_, and
then created our own `mock_bar` object from the mock class: `mock_bar = MockBar()`.
You can also create a mock object directly by passing `instance=True` to
`create_autospec()`:

```python
mock_bar = mock.create_autospec(Bar, spec_set=True, instance=True)
```

Autospeccing is **recursive**: if the real class has attributes then those
attributes will also be autospecced. For example here the `Foo` class has a
string attribute named `some_attribute`, a mock `Foo`'s `some_attribute` has
only those methods that a real `Foo`'s `some_attribute` would have:

```pycon
>>> class Foo(object):
...     some_attribute = "a_string"
>>>
>>> mock_foo = mock.create_autospec(Foo, spec_set=True, instance=True)
>>>
>>> # Calling a method that exists works:
>>> mock_foo.some_attribute.decode()
<MagicMock name='mock.some_attribute.decode()' id='139778195402064'>
>>>
>>> # But calling a method that doesn't exist crashes:
>>> mock_foo.some_attribute.does_not_exist()
Traceback (most recent call last):
  ...
AttributeError: Mock object has no attribute 'does_not_exist'
>>>
>>> # Accessing an attribute that doesn't exist also crashes:
>>> mock_foo.some_attribute.does_not_exist
Traceback (most recent call last):
  ...File "<stdin>", line 1, in <module>
AttributeError: Mock object has no attribute 'does_not_exist'
```

Trying to **call** an attribute will also crash if the real class's attribute
isn't callable.

`create_autospec()` actually isn't used much in the Hypothesis tests currently,
but it probably should be. If you're going to make a mock object, you should
probably make it using `create_autospec()` if you can.

### spec_set

The Hypothesis tests often use a mock feature called `spec_set` that is similar
to `create_autospec()` but not as good. Instead of calling `create_autospec()`
you just instantiate a `mock.MagicMock()` (or more often a `mock.Mock()` in the
Hypothesis tests) and pass the class being mocked as a `spec_set` argument to
the mock constructor. As with autospec, mocks created in this way only have the
attributes and methods that the real object would have. Unlike with autospec,
you can still pass any arguments that don't exist without crashing:

```pycon
>>> class Foo(object):
...     def some_method(some_arg):
...         pass
... 
>>> mock_foo = mock.MagicMock(spec_set=Foo)
>>> mock_foo.some_method(some_arg=23)
<MagicMock name='mock.some_method()' id='140189369916688'>
>>>
>>> # Calling a method that doesn't exist crashes:
>>> mock_foo.method_that_does_not_exist()
Traceback (most recent call last):
  ...
AttributeError: Mock object has no attribute 'method_that_does_not_exist'
>>>
>>> # But passing arguments that don't exist still passes:
>>> mock_foo.some_method(arg_that_does_not_exist=23)
<MagicMock name='mock.some_method()' id='140189369916688'>
```

Class variables aren't recursively autospec'd either.

There's also a `spec` argument (`mock.MagicMock(spec=Foo)`), it works the
same as `spec_set` but allows attributes that don't exist to be written.

#### Passing a list of strings to `spec_set`

Instead of a class you can pass a list of strings as the value to the `spec_set`
or `spec` argument. Only those names given in the list will be accessible on
the mock object. Each name is accessible either as an attribute or callable as
a method, and returns an unconstrained `MagicMock`:

```python
>>> mock_foo = mock.MagicMock(spec_set=['bar', 'gar'])
>>> mock_foo.bar
<MagicMock name='mock.bar' id='140189369594896'>
>>> mock_foo.bar()
<MagicMock name='mock.bar()' id='140189369788624'>
>>> mock_foo.boo
Traceback (most recent call last):
  ...File "<stdin>", line 1, in <module>
AttributeError: Mock object has no attribute 'boo'
```

Passing a list of strings to `spec_set` or `spec` is an even weaker form of
specification, and it introduces duplication between the test code that creates
the mock and the real code that's being mocked. If the real code is changed
then the mocks may need to be updated, otherwise the tests that use the mocks
may still pass even if the code they're testing is wrong.

Limitations of autospeccing
---------------------------

Unfortunately `create_autospec()` isn't a perfect solution to the problem with mocks.
It has a few limitations:

* **Instance variables** created in `__init__()` methods don't work.

    For example here a real `Foo` object would have a `bar` attribute, but a mock
    `Foo` object from `create_autospec()` **doesn't** have `bar`:

        #!pycon
        >>> class Foo(object):
        ...     def __init__(self):
        ...         self.bar = 'BAR'
        ... 
        >>> real_foo = Foo()
        >>> real_foo.bar
        'BAR'
        >>> mock_foo = mock.create_autospec(Foo, spec_set=True, instance=True)
        >>> mock_foo.bar
        Traceback (most recent call last):
          ...
        AttributeError: Mock object has no attribute 'bar'

    Mock would have to actually _execute_ the `Foo.__init__()` method in order
    to know about `self.bar`, and it doesn't.

    One way around this is for the tests to tell `create_autospec()` about `bar`
    by passing it as an argument:

        #!pycon
        >>> mock_foo = mock.create_autospec(Foo, instance=True, bar='BAR')
        >>> mock_foo.bar
        'BAR'

    Note that we had to drop the `spec_set=True`. This works but has the downside
    that the tests are now coupled to `Foo` - if the `Foo` class changes, for
    example to remove, rename or change the type of `Foo.bar`, then the above
    mock will need to be updated (otherwise tests for the code that uses `Foo`
    could still be passing even if the code is wrong because it still uses 
    `Foo.bar` which no longer exists on the real `Foo`).

    Another way around this is to make `bar` a class variable:

        #!pycon
        >>> class Foo(object):
        ...     bar = 'BAR'
        ...     def __init__(self):
        ...         pass
        ... 
        >>> mock_foo = mock.create_autospec(Foo, spec_set=True, instance=True)
        >>> mock_foo.bar
        <NonCallableMagicMock name='mock.bar' spec_set='str' id='139778195499216'>

    This works but it isn't the best way to design classes in Python because
    [there can be surprising effects when class variables are mutable objects](https://docs.python.org/2/tutorial/classes.html#class-and-instance-variables).

    A third workaround is to make `bar` a `@property` on the `Foo` class:

        #!pycon
        >>> class Foo(object):
        ...     def __init__(self):
        ...         self.bar = 'BAR'
        ...     @property
        ...     def bar(self):
        ...         return self.bar
        ... 
        >>> mock_foo = mock.create_autospec(Foo, spec_set=True, instance=True)
        >>> mock_foo.bar
        <MagicMock name='mock.bar' id='139778195521488'>

    This makes the `Foo` code a little more verbose than it otherwise needed to be,
    and note that `mock_foo.bar` now returns a `MagicMock` (not the string `BAR`),
    so if the code under test were to call a non-string method on `bar` it would
    not crash in the tests (but would crash with the real `Foo` in production).

    Finally, one more way to workaround this issue is to create a real `Foo`
    object and pass that to `create_autospec()` instead of the `Foo` class:

        #!pycon
        >>> class Foo(object):
        ...     def __init__(self):
        ...         self.bar = 'BAR'
        ... 
        >>> foo = Foo()
        >>> mock_foo = mock.create_autospec(foo, spec_set=True, instance=True)
        >>> mock_foo.bar
        <NonCallableMagicMock name='mock.bar' spec_set='str' id='139778195570640'>

    `mock_foo.bar` is now a mock spec'd to have only those methods that a real
    `foo.bar` attribute has (in this case - only string methods).

    Of course, this workaround is only applicable if your tests can quickly and
    easily instantiate real `Foo` objects.

* **Return values** of methods are still unspecified `MagicMock`s.

    For example the code won't crash in the tests if it tries to call a method
    that doesn't exist on _the return value_ of an autospec'd mock's method:

        #!pycon
        >>> class Foo(object):
        ...     def some_method():
        ...         return 23
        ... 
        >>> mock_foo = mock.create_autospec(Foo, spec_set=True, instance=True)
        >>> mock_foo.some_method()
        <MagicMock name='mock.some_method()' id='139778195517520'>
        >>>
        >>> # This should crassh but doesn't:
        >>> mock_foo.some_method().method_that_does_not_exist()
        <MagicMock name='mock.some_method().method_that_does_not_exist()' id='139778195121168'>

    Tests can fix this by specifying the return value:

        #!pycon
        >>> mock_foo.some_method.return_value = 23
        >>> mock_foo.some_method()
        23
        >>> mock_foo.some_method().method_that_does_not_exist()
        Traceback (most recent call last):
          ...
        AttributeError: 'int' object has no attribute 'method_that_does_not_exist'

    But now some duplication between the tests and `Foo` has been introduced.
    Again, if the real `Foo.some_method()` is changed then the above mock code
    would also need to be updated otherwise the tests for the code that uses
    `Foo` could still be passing even though the code is now wrong.

* Autospec doesn't automatically mock the **behavior** of the real class.

    Your tests still need to use `return_value` and `side_effect` to simulate
    raising exceptions and other behaviors of dependency objects. Again, this
    introduces duplication between the tests and the dependencies being mocked -
    if the dependency code is changed then the mocks may need to be updated, or
    the tests could still be passing while the code is wrong.

Conclusion
-----------

As you can see, autospeccing in Python is a battle to write your code and
create your mocks in a way that minimizes the possibility of false-positive
test passes creeping in.

Most of the autospec limitations above can be avoided most of the time, but it
can't always be done perfectly: there's no way to automate simulating the
`return_value`s, `side_effect`s and behaviors of real classes without
introducing some amount of duplication between the real classes and the tests
that mock them. Duplication between real code and test mocks introduces the
possibility that over time, as the real code changes, the mocks will go out of
sync with the real code and false-positive test passes may creep in.

Now that we know how to use mocks, and what the dangers with using mocks are,
the next post will cover
[When and When Not to Use Mocks](/2017/04/25/when-to-use-mocks/).
