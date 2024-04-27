Title: Designing Python Exception Classes
Tags: Python

It isn't [wonderfully well documented](https://docs.python.org/3/library/exceptions.html#BaseException) in Python that the
builtin `Exception` class takes any number of positional arguments (pargs) and uses them to provide `__str__()` and 
`__repr__()` methods and pickling support. If you understand how `Exception`'s pargs work then you can use it as a base
class correctly and inherit these features for your custom exception classes.

`Exception` with a single parg
------------------------------

If you give `Exception` a single parg, for example an error message string, this string become's the exception's informal
string representation (the `BaseException.__str__()` method):

```pycon
>>> e = Exception("Something went wrong")
>>> print(e)
Something went wrong
```

`__str__()` is meant to return a [concise and convenient string representation of the object](https://docs.python.org/3/reference/datamodel.html?highlight=__str__#object.__str__),
it's called by the `print()` and `format()` builtins.

The parg string will also be used along with the class name in the exception's formal string representation (the
`BaseException.__repr__()` method):

```pycon
>>> e = Exception("Something went wrong")
>>> repr(e)
>>> "Exception('Something went wrong')"
```

`__repr__()` is meant to return an [information-rich and unambiguous string representation of the object](https://docs.python.org/3/reference/datamodel.html?highlight=__str__#object.__repr__)
for debugging. Whenever possible it's supposed to be a valid expression for recreating the object with the same value,
that's why it looks like Python code for creating a new `Exception`.

`Exception` with multiple pargs 
-------------------------------

You can pass any number of pargs to `Exception`. If you pass it more than one parg then `Exception.__str__()` and
`Exception.__repr__()` change to using a tuple representation of the pargs. The pargs don't all have to be strings:

```pycon
>>> e = Exception("Something Error", 42, "Something went wrong")
>>> print(e)
('Something Error', 42, 'Something went wrong')
>>> repr(e)
"Exception('Something Error', 42, 'Something went wrong')"
```

Note that `__str__()` returns _a string representation of a tuple_, not an actual tuple. The pargs are also readable from
the `Exception.args` property, which is an actual tuple. `args` is always a tuple regardless of whether one or more
than one parg was given:

```pycon
>>> e.args
('Something Error', 42, 'Something went wrong')
```

`Exception` doesn't accept any kwargs
--------------------------------------

`Exception` does not accept any keyword arguments (kwargs):

```pycon
>>> e = Exception(error_message="Something went wrong")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: Exception() takes no keyword arguments
```

Custom exception classes inherit `__str__()` and `__repr__()`
-------------------------------------------------------------

If you write your own `Exception` subclass then you get the variable number of `__init__()` pargs and the `__str__()` and
`__repr__()` for free. This is Python giving us a hint that most exception classes should work with a small number of
positional arguments, rather than keyword arguments:

```pycon
>>> class MyError(Exception):
...     """My custom error class."""
... 
>>> e = MyError(500, "Internal Server Error")
>>> print(e)
(500, 'Internal Server Error')
>>> repr(e)
"MyError(500, 'Internal Server Error')"
>>> e.args
(500, 'Internal Server Error')
```

If you want to name your custom error class's pargs, and force every instance of it to have the same number of pargs, then
you can add an `__init__()` method:

```pycon
>>> class MyError(Exception):
...     def __init__(self, status_code, reason):
...         pass
... 
>>> e = MyError(500, "Internal Server Error")
>>> print(e)
(500, 'Internal Server Error')
>>> repr(e)
"MyError(500, 'Internal Server Error')"
>>> e.args
(500, 'Internal Server Error')
```

Note that I didn't do anything with `status_code` or `reason` (for example I didn't save them on `self`), and I didn't call
`super().__init__()`, and this still worked.

You need to call `super().__init__()`
-------------------------------------

Pylint will complain that you didn't call the base class's `__init__()` and for good reason: by naming the `__init__()`
arguments we've enabled user code to pass them to `MyError` as kwargs rather than pargs, and this breaks `BaseException`'s
`args`, `__str__()` and `__repr__()`:

```pycon
>>> e = MyError(status_code=500, reason="Internal Server Error")
>>> print(e)

>>> repr(e)
'MyError()'
>>> e.args
()
```

`Exception` isn't meant to accept kwargs, and as we saw above you _can't_ pass kwargs to `Exception` directly, but with our
custom `__init__()` we've enabled them.

Fortunately this is easy to fix -- just call `super().__init__()` as Pylint wants us to and pass the arguments to it as
pargs. Let's also provide easy access to `status_code` and `reason` (`e.status_code` instead of `e.args[0]`) by adding them 
to `self`:

```pycon
>>> class MyError(Exception):
...     def __init__(self, status_code, reason):
...         super().__init__(status_code, reason)
...         self.status_code = status_code
...         self.reason = reason
... 
>>> e = MyError(status_code=500, reason="Internal Server Error")
>>> print(e)
(500, 'Internal Server Error')
>>> repr(e)
"MyError(500, 'Internal Server Error')"
>>> e.args
(500, 'Internal Server Error')
>>> e.status_code
500
>>> e.reason
'Internal Server Error'
```

Now we have a custom exception class with a fixed number of named arguments and a nice `__str__()` and `__repr__()`
inherited from `Exception`. Of course you can still pass `status_code` and `reason` as pargs as well:
`MyError(500, "Internal Server Error")`.

The `BaseException` source code is better than the docs
-------------------------------------------------------

[The C source code for `BaseException`](https://github.com/python/cpython/blob/0c48618cc0d28caf3db191879715e519546857fd/Objects/exceptions.c#L32-L294)
contains the implementation of the pargs-based `__str__()` and `__repr__()` methods, as well as other `BaseException`
properties such as `__cause__` (the other exception that the exception was raised from, if
`raise SomeError from other_error` was used) and pickling support.
