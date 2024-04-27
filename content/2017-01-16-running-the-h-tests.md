Title: Running the Hypothesis Python Tests
Tags: Python Unit Tests at Hypothesis
Alias: /post/running-the-h-tests/

This post covers [running the tests](http://h.readthedocs.io/en/latest/developing/install/website/#running-h-s-tests)
and if you want to try out the example commands you should have a
[Hypothesis dev install](http://h.readthedocs.io/en/latest/developing/install/).

The easiest way to run all of the tests in the
[hypothesis/h repo](https://github.com/hypothesis/h) (including both
Python and JavaScript tests) is by running the `make test` command:

```console
$ make test
```

This will run all of the Python and JavaScript tests at once.
This is the command that is run on [Travis CI](https://travis-ci.org/hypothesis/h)
to verify each new commit that's pushed to GitHub.
But when working on the Python code I usually run the tests using one of these
two commands instead:

```console
# To run the h tests:
$ tox -e py27-h tests/h
... (test output)

# To run the memex tests:
$ tox -e py27-memex tests/memex
... (test output)
```

The reason to use these commands instead of `make test` is that you can pass
lots of useful options to them (see below) that you can't pass to `make test`,
for example to only run certain tests rather than all of them.
I might run `make test` once as a final check before submitting a pull request,
or after setting up a new development environment, but the rest of the time I
use the tox commands above.

Before we have a look at all the useful options you can pass to tox, lets first
dig in to how we get from `make test` to `tox -e py27-h tests/h`.


### make

The `make test` command is provided by
[h's Makefile](https://github.com/hypothesis/h/blob/2fda3f382a4b9563a4a3e4c8d8713fc2771edd1f/Makefile) (see [GNU Make](https://www.gnu.org/software/make/)). 
If you look inside h's `Makefile` you can see that the command that
`make test` runs to run the Python part of the tests is `tox`...


### tox

You can run the tox command that `make test` runs manually, this will run all
all the Python tests but not the JavaScript ones:

```console
$ tox
(Runs all the Python tests)
```

[tox](https://tox.readthedocs.io/) is a tool that creates and manages clean room
[Python virtual environments](https://virtualenv.pypa.io/) for running the
tests in. When you run `tox` it creates virtual environments in the
`.tox` directory, installs h and memex's dependencies in the virtualenvs, and
then runs the tests in them.

Sometimes a development environment has older or newer versions of h's
dependencies installed than what is actually specified in h's requirements, or
has additional packages installed. tox's use of clean virtual environments to
run the tests in avoids differences between different developers' environments,
or between dev envs and production, from producing different test results.

You can see the virtualenvs that tox has created by running `tox --listenvs` or
by looking in the `.tox` directory:

```console
$ ls .tox
dist/  log/  py27-h/  py27-memex/
```

`dist` and `log` are used by tox internally, `py27-h` and `py27-memex` are the
two test environments that h uses. tox runs the tests in the
[tests/h](https://github.com/hypothesis/h/tree/9f2602d10dc11f3cc5765cc9d3e4454a8629a94e/tests/h)
directory in the `py27-h` environment and runs the tests in
[tests/memex](https://github.com/hypothesis/h/tree/9f2602d10dc11f3cc5765cc9d3e4454a8629a94e/tests/memex)
in the `py27-memex` environment.

(There's also an environment called `functional` for the functional tests but
`make test` and `tox` don't run the functional tests by default. To run the
functional tests locally do `tox -e functional tests/functional`.)

The full configuration for tox is in the
[tox.ini file](https://github.com/hypothesis/h/blob/2fda3f382a4b9563a4a3e4c8d8713fc2771edd1f/tox.ini).
This is where we define the different test virtualenvs, which dependencies to
install into each, and which tests to run in each, among other things. In this
file you can see that the command that tox actually runs in order to run the
tests is `pytest`. Pytest is the test framework that we use to write h's
Python tests.

**Tip**: To save time tox doesn't normally recreate these virtualenvs each time
you run the tests. It creates the virtualenvs once, installs the
dependencies, and then reuses them each time. If h's specified dependencies
change then tox is supposed to update the virtualenv but sometimes it
doesn't and you'll have tests failing because of a missing or out of date
dependency. If this happens you can force tox to recreate the virtualenvs
by running `tox --recreate`. (Alternatively just delete the `.tox` directory
then run `tox`.)


### pytest

`pytest` is the command that actually runs the Python tests.
Pytest is the framework that we use to write Python
tests in Hypothesis. If you're looking for documentation on how to write
Hypothesis tests, [the pytest docs](http://docs.pytest.org/en/latest/) are the
main place to look.

Since we're running pytest via tox rather than directly we have to pass
arguments to pytest through tox. Anything after a standalone `--` in the tox command
will be passed to pytest. For example `tox --help` is going to print tox's
help documentation, not pytest's, to print pytest's help you would do:

```console
$ tox -- --help
```

Any arguments that you give to tox or pytest on the command line will
_override_ the default arguments given in the `tox.ini` file. By default the
`tox.ini` file runs two commands, `tox -e py27-h tests/h` and then
`tox -e py27-memex tests/memex`. The `-e py27-h` tells tox to use the
`py27-h` test virtualenv, and the `tests/h` part tells tox to tell pytest to
run only the tests in the `tests/h` directory. You can't run the `tests/h`
tests in the `py27-memex` virtualenv because that virtualenv has the
dependencies for the `tests/memex` tests installed in it, not the dependencies
for the `tests/h` tests, so `tox -e py27-memex tests/h` will crash.
So when passing custom options on the command line you always need to pass the
virtualenv name and the path to the tests as well, it's always either
`tox -e py27-h tests/h` or `tox -e py27-memex tests/memex`.
(**Tip**: create aliases for these commands in your shell configuration.)

**Tip**: Some people like to run pytest directly because it starts up quicker
than tox and because it's easier to pass arguments to pytest this way.
The easiest way to do this is to run one of the copies of pytest that tox has
installed in one of its virtualenvs, for example:
`.tox/py27-h/bin/pytest tests/h/`. (If you use this command often then it's
probably worth creating a shell alias for it too.)


### Useful command line options for pytest

To run just the h tests (and not the memex ones):

```console
$ tox -e py27-h tests/h
```

To run just a single test package just change the path:

```console
$ tox -e py27-h tests/h/views
```

Run just a single test module give the path to the module file including the
`.py` ending:

```console
$ tox -e py27-h tests/h/views/predicates_test.py
```

Run just a single test class add `::` followed by the name of the test class:

```console
$ tox -e py27-h tests/h/views/predicates_test.py::TestHasPermissionPredicate
```

To run just a single test method add another `::` before the name of the
method:

```console
$ tox -e py27-h tests/h/views/predicates_test.py::TestHasPermissionPredicate::test_text
```

**Tip**: Running the tests with the `--verbose` argument to pytest will print
out all the test method names in a format suitable for copy-pasting into the
above command to run a single test individually:

```console
$ tox -e py27-h tests/h -- --verbose
...
tests/h/assets_test.py::test_environment_lists_bundle_files PASSED
tests/h/assets_test.py::test_environment_generates_bundle_urls PASSED
tests/h/assets_test.py::test_environment_url_returns_cache_busted_url PASSED
...
```

The `-k` argument to pytest lets you specify a string pattern and pytest will
run only the tests whose name matches that pattern. This can be more convenient
than typing in the full path. For example to run just one test class:

```console
$ tox -e py27-h tests/h -- -k TestHasFeatureFlagPredicate
```

You can also use logic like `not`, `and` and `or` in with `-k`, for details see
[the -k docs](http://docs.pytest.org/en/latest/example/markers.html#using-k-expr-to-select-tests-based-on-their-name).

The `--failed-first` / `--ff` argument runs the tests that failed the last time
first, and then runs the rest of the tests. It works well in combination with
`--exitfirst` / `-x` which causes pytest to stop after the first test fail.
As long as you have a failing test it'll run just that test and then stop,
as soon as the failing test passes it'll continue running the rest of the
tests:

```console
$ tox -e py27-h tests/h -- --failed-first --exitfirst
```

Some other useful arguments to pass after the `--`:

* `--maxfail=n` to stop after n test fails

* `--pdb` to drop into a debugger when a test fails

* `--showlocals` / `-l` to print out the values of all local variables in
  tracebacks when tests fail

To specify a default set of options to always pass to pytest you can set the
`PYTEST_ADDOPTS` environment variable, for example:

```console
$ export PYTEST_ADDOPTS="--verbose --exitfirst --failed-first --showlocals"
```

(This works well in combination with [direnv](https://direnv.net/).)
