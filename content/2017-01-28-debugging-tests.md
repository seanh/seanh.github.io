Title: Debugging Failing Tests with pytest
Tags: Python Unit Tests at Hypothesis
Alias: /post/debugging-tests/

This post briefly covers some tools for debugging failing tests when using pytest.

If looking at the traceback from a test failure isn't enough there are a few
tools to help debug a failing test:

1. The `--showlocals` argument to pytest will print out the values of all local
   variables after the traceback whenever a test fails. Sometimes this can be
   enough extra information to find the problem:

        #!console
        $ tox -e py27-h tests/h -- --showlocals

2. Pytest will capture the output of any Python `print` statements and
   print it after the traceback for the failing test. The output of `print`
   statements in the test code or in the code under test is printed (but print
   statements from tests that passed are not printed).

      Add `print` statements to the tests and to the code under test to print
      out information that can help you to figure out what's going wrong - the
      values of arguments and local variables, which lines of code are called (and
      in which order), etc.

      Just remember to delete the `print`s again before committing the code!

      **Tip**: Try wrapping a `print` statement in an `if` clause, so that
      something is printed out only if some expression is true. This can be useful
      for only printing out the valuable information, and not a lot of noise, if
      the `print` statement needs to be on a line of code that's executed many
      times during the test.

3. The `--pdb` argument to pytest will drop into a
   [pdb](https://pymotw.com/2/pdb/) debugger shell whenever a test fails, at
   the line of code that fails:

        #!console
        $ tox -e py27-h tests/h -- --pdb

      From this shell you can inspect the values of variables and arguments,
      evaluate expressions, step through code one line at a time, etc. For some
      tips see [pdb on pymotw](https://pymotw.com/2/pdb/).

4. `ipdb` is an enhanced debugger shell based on ipython, with syntax
   highlighting, tab completion, etc. To use it you first need to install
   ipdb into tox's virtual environment:

        #!console
        $ .tox/py27-h/bin/pip install robpol86-pytest-ipdb

    We're using `robpol86-pytest-ipdb` because the `pytest-ipdb` package is
    broken.

    Then run the tests with the `--ipdb` argument instead of `--pdb`:

        #!console
        $ tox -e py27-h tests/h -- --ipdb

    There are many more Python debuggers that you can try, for example
    [pdb++](https://pypi.python.org/pypi/pdbpp/) and
    [pudb](https://pypi.python.org/pypi/pudb).


5. `set_trace()` lets you drop into a debugger shell on any line of code,
   whether in a test or in the code under test, rather than just when a test
   fails. Put this line anywhere in the Python code:

        #!console
        import pdb; pdb.set_trace()

    and you'll drop into pdb whenever execution hits that line.

    For ipdb you would use `import ipdb; ipdb.set_trace()`.

    As with `print` statements, wrapping `set_trace()` lines in `if` statements
    can be a useful trick.

    As with `print` statements, remember to delete the `set_trace()` lines again
    before committing the code. Fortunately you can easily
    [grep](https://en.wikipedia.org/wiki/Grep) the entire codebase for
    `set_trace`, since this should never appear in production code.
