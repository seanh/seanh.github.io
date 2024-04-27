Title: Managing a Project's Virtualenvs with tox
Subheading: A comprehensive beginner's introduction to tox.
Tags: tox, Hypothesis
Alias: /post/tox-tutorial/

tox is a great tool for standardising and automating any development task that
benefits from being run in an isolated virtualenv. But tox suffers from an
educational problem: tox appears to be just for running tests, and that's all that
many projects use it for. It can also be unclear how best to use the `tox.ini`
file format at first. This tutorial aims to clear up the confusion and teach
you how to automate a project's development tasks with tox. It covers
everything you need to know to understand the real [hypothesis/h tox.ini file](https://github.com/hypothesis/h/blob/471cf3e620cb0ff1a6ec8ccca710727b1e20e0e6/tox.ini).

<div class="toc"></div>

Why tox is confusing at first
-----------------------------

tox can appear to be just a tool for running tests, rather than for development
tasks in general:

* tox was originally for running your tests in an isolated virtual
  environment, but has grown into a more general project virtualenv /
  command management tool.

* For many developers their first introduction to tox will be when they come
  across it being used in some project to run the tests, while the project
  confusingly uses manually-created virtualenvs for other things that tox
  could be used for, like building the documentation and running the
  development server.
* tox's own documentation is unclear on the scope of tox too, stating tox's vision as
  <q>to automate and standardize testing in Python</q>. But the same docs later describe tox
  as <q>a generic virtualenv management and test command line tool</q> and
  include examples of using tox to build documentation and to run development environments.
  tox's GitHub project's description is <q>Command line driven CI frontend
  and development task automation tool</q>.
* Internal terminology used by tox also suggests that it's just for testing:
  tox refers to the virtualenvs that it creates as <q>testenvs</q>.
  We'll be using both <q>testenv</q> and <q>virtualenv</q> in this guide too.
  Eventually we'll [get around to explaining exactly what a testenv is](#factors-and-conditionals)
  relative to a virtualenv.

In addition:

* The `tox.ini` file format is just complicated enough that it requires some
  knowledge of how tox works to understand how to write a good one.

* The relationship between tox and similar tools such as Docker, GNU Make,
  virtualenv, virtualenvwrapper, etc is unclear.

So what is tox and what is it for?
----------------------------------

tox is a **project virtualenv management and development task automation tool**.
You create a `tox.ini` file for your project, and in this file you define
virtualenvs (tox calls them <q>testenvs</q>) for all your project tasks that
you want to standardize and automate with tox: running the tests, running the
development server, running the linters, building the documentation, publishing
a release, etc. Here's an example `tox.ini` file that'll be explained in detail
later:

```ini
[tox]
envlist   = tests
skipsdist = true

[testenv]
deps =
    tests: -r requirements.txt
    lint:  flake8
    docs:  sphinx-autobuild
commands =
    tests: pytest tests/
    lint:  flake8 src
    docs:  sphinx ...
```

You run tox telling it which of your testenvs to run, e.g. `tox -e docs` to
build the documentation or `tox -e tests,lint` to run the tests followed by
the linter, and tox creates a virtualenv, installs the
dependencies that you've listed in `tox.ini` into it, and runs the commands
that you've listed in `tox.ini` in it.

### tox's workflow

More concretely, tox is a tool that automates a certain workflow, as described in
the [System overview](https://tox.readthedocs.io/en/latest/#system-overview) in the
tox docs:

1. Read tox config settings from a `tox.ini` file, command line options and environment variables.
2. Optionally create a Python package (sdist) of your project. (We skip this step for Hypothesis projects.)
3. Create a Python virtual environment using the version of Python selected in `tox.ini`.
4. Install any Python dependencies listed in `tox.ini` (the `deps` setting) into the virtualenv.
   If an `sdist` of your project was created in step 2 install that too.
5. Run the commands listed in `tox.ini` (the `commands` setting) in the virtualenv.
   By default fail if any of the commands exit with a non-zero exit code.
6. Print out a report of the virtualenvs that were run and whether each succeeded or failed.

So tox is really just a tool for creating virtualenvs and running commands in them, and any development task that can be
automated by running commands in virtualenvs can be automated with tox.

If you ask tox to run more than one virtualenv at once it will loop repeating steps 3, 4 and 5 for each virtualenv, and finally report on them all in step 6.

If you run the same virtualenv again tox will speed things up by reusing the previously created virtualenv. It'll skip 
steps 3 and 4 and avoid unnecessarily recreating the virtualenv or reinstalling the dependencies unless you pass the
`tox --recreate` option or unless tox knows that the virtualenv needs to be recreated (for example because the `deps` in
`tox.ini` have changed).

### Benefits of using tox

By defining all of your project's tasks in a `tox.ini` file tox **simplifies things
for developers**. A developer only needs to install and run tox, they don't need
to bother with creating and activating virtualenvs and installing dependencies
themselves.

tox also **simplifies CI integration**: CI scripts that just run tox are much
simpler than scripts that handle virtualenvs and dependencies themselves.

tox also standardizes things, **reducing differences between different
development environments** and between dev envs and CI and production.
The `tox.ini` file defines exactly what dependencies to install into each
virtualenv and tox takes extra steps to isolate its virtualenvs from the
outside system.

tox can also **reduce the chance of dependency conflicts** by using a separate
virtualenv for each task, rather than installing everything in one big
virtualenv. The packages needed to build your documentation or run your linters
don't need to be installed in the virtualenv that runs your dev server.

Finally, tox provides **one place to define and document all of the
available projects tasks** -- in the `tox.ini` file -- with a simple and
consistent command line interface for running those tasks.

I call tox <q>project</q> virtualenv management because it uses a per-project
configuration file, the `tox.ini` file, that you add to your project's version
control repository. This is different than other tools, such as
virtualenvwrapper, that are more personal-use virtualenv managers. Your text
editor is your personal text editing tool and text editor configuration or
standardizing on one particular text editor isn't usually part of a project.
GNU Make on the other hand is a _project_ build automation tool because its
`Makefile` is tracked as part of the project. tox is a project tool, like Make.

tox's original use-case
-----------------------

The original purpose of tox was to run tests in isolated environments and (later) to
automate running tests with multiple combinations of different versions of
Python and different versions of different dependencies. It uses some more
recent tox features, but this example partial `tox.ini` file for
[Compressing a dependency matrix](https://tox.readthedocs.io/en/latest/example/basic.html#compressing-dependency-matrix)
from tox's docs illustrates tox's originally intended use-case:

```ini
[tox]
envlist = py{27,34,36}-django{15,16}-{sqlite,mysql}

[testenv]
deps =
    django15: Django>=1.5,<1.6
    django16: Django>=1.6,<1.7
    py34-mysql: PyMySQL     ; use if both py34 and mysql are in an env name
    py27,py36: urllib3      ; use if any of py36 or py27 are in an env name
    py{27,36}-sqlite: mock  ; mocking sqlite in python 2.x
```

Running the command `tox` with this `tox.ini` file will generate the "cross product"
of the different vetsions of Python, Django and SQLite or MySQL and run the project's
tests many times over: with Python 2.7, Django 15, and SQLite, then with Python 2.7,
Django 15 and MySQL, then with Python 2.7, Django 16, and SQLite, and so on,
for all combinations. More on this ["generative envlist" feature](#generative-envlists)
below. The `deps` setting defines how the dependencies to be
installed should change depending on the versions of Python and Django being
tested and on SQLite or MySQL.

We don't have a need at Hypothesis to test our code against many different
versions like this. We're writing a web application that gets deployed to a
production environment that we control, with pinned versions of Python and all
dependencies. We use tox instead for its isolation and task automation features.

Where we're going: our use-case for tox
---------------------------------------

Here's an excerpted version of [Hypothesis's `tox.ini` file](https://github.com/hypothesis/h/blob/master/tox.ini).
It defines a few different testenvs named `dev` (for running the dev server),
`tests` (for running the tests), `docs` (for building the docs), etc. One
testenv for each development task. And tells tox what dependencies to install
and what commands to run in each testenv. The rest of this tutorial will cover
everything you need to understand this `tox.ini` file in detail.

```ini
[tox]
envlist = tests
skipsdist = true
requires = tox-pip-extensions
tox_pip_extensions_ext_venv_update = true

[testenv]
skip_install = true
deps =
    dev:   -r requirements-dev.in
    tests: -r requirements.txt
    lint:  flake8
    docs:  sphinx-autobuild
whitelist_externals =
    dev:   sh
commands =
    dev:   sh bin/hypothesis devserver
    tests: pytest -Werror tests/h/
    lint:  flake8 h
    docs:  sphinx-autobuild -BqT -b dirhtml -d {envtmpdir}/doctrees . {envtmpdir}/html
```

Installing tox
--------------

tox is like both GNU Make and your text editor in that you should install tox
system-wide and use that one single copy of tox for each project that you work
on. You don't install tox in your project's virtualenv, or list it as a
dependency in your project's requirements files. tox is the thing that
_creates_ your project virtualenvs and installs their dependencies for you.

On Ubuntu, just install tox once system-wide and be done with it:

```console
$ sudo pip install tox
```

Getting started: a minimal `tox.ini` file
-----------------------------------------

Here's the smallest possible `tox.ini` file that will run without crashing:

```ini
[tox]
skipsdist = true
```

If you save this as `tox.ini` in an empty directory and then run the command
`tox` in that directory you should see something like this:

```console
$ tox
python create: /home/seanh/Dropbox/Desktop/tox/.tox/python
python run-test-pre: PYTHONHASHSEED='3201412928'
__________________________________________________________________ summary ___________________________________________________________________
  python: commands succeeded
  congratulations :)
$ 
```

tox created a virtualenv (at `.tox/python`) using the default version of Python
on your system (Python 2.7 on my Ubuntu system). Since the `tox.ini` file
didn't list any dependencies or commands tox didn't install any dependencies or
run any commands in the virtualenv. It just did nothing.

The [`skipsdist = true`](https://tox.readthedocs.io/en/latest/config.html#conf-skipsdist)
tells tox not to try and build an sdist (source distribution) of your project.
An sdist is a way of packaging up a Python project so that it can be installed
on a system, published to <https://pypi.org/>, etc. Since our project at this
point is an empty directory there's nothing to package up. At Hypothesis we
don't build and publish installable Python packages anyway -- we build web apps
that we deploy to production environments -- so we always use
`skipsdist = true`.

Commands
--------

Lets add a command to our `tox.ini` file using the [`commands` setting](https://tox.readthedocs.io/en/latest/config.html#conf-commands).
We'll make it print out the version of Python being used:

```ini
[tox]
skipsdist = true

[testenv]
commands = python --version
```

Now if you run `tox` you'll see the output of our command that it ran in the virtualenv:

<pre><code>$ tox
python run-test-pre: PYTHONHASHSEED='3697789845'
python runtests: commands[0] | python --version
<b>Python 2.7.15rc1</b>
__________________________________________________________________ summary ___________________________________________________________________
  python: commands succeeded
  congratulations :)
$ </code></pre>

We've now split the `tox.ini` file into two sections `[tox]` and `[testenv]`.
The `[tox]` section contains [global settings](https://tox.readthedocs.io/en/latest/config.html#tox-global-settings)
that affect the global behavior of tox itself, such as whether or not to build
an sdist, the minimum version of tox that this `tox.ini` file requires, etc.

The `[testenv]` section defines the testenv(s) that we want tox to create for
us: what versions of Python to use to create the testenvs, what dependencies to
install into them, what environment variables, what commands to run in the
testenvs, etc.
We're gonna cover the most important settings that you can put in the
`[testenv]` section of your `tox.ini` file, starting with `commands`. For full
documentation of all the available settings run `tox --help-ini` or see
[the docs](https://tox.readthedocs.io/en/latest/config.html#tox-environment-settings).

### External commands and `whitelist_externals`

One of the things that tox does to isolate testenvs from the system is to
prepend the virtuenv's `bin` directory onto the `PATH` envvar in the subshell
that the testenv's commands are run in. You can see this by having tox run a
command that prints out the value of `PATH`:

<pre><code>[tox]
skipsdist = true

[testenv]
<b>commands = sh -c "echo $PATH"</b></code></pre>

<pre><code>$ tox
python run-test-pre: PYTHONHASHSEED='3100919638'
python runtests: commands[0] | sh -c 'echo $PATH'
WARNING: test command found but not installed in testenv
  cmd: /bin/sh
  env: /home/seanh/Dropbox/Desktop/tox/.tox/python
Maybe you forgot to specify a dependency? See also the whitelist_externals envconfig setting.
<b>/home/seanh/Dropbox/Desktop/tox/.tox/python/bin</b>:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
__________________________________________________________________ summary ___________________________________________________________________
  python: commands succeeded
  congratulations :)
$ </code></pre>

The `PATH` envvar in the testenv's subshell is my usual `PATH` envvar but with
the `.tox/python/bin` dir prepended to the front. This is so that executables
in the virtualenv's `bin` are always chosen instead of any executables with the
same name elsewhere on the system `PATH`. This is why when we've been putting
`python --version` in our `tox.ini` file its been printing out the version of
Python installed in the virtualenv instead of the system version of Python:
it's running the copy of `python` at `.tox/python/bin/python`. Similarly `pip`
in a `tox.ini` file (or any file run by a `tox.ini` file) will be the
virtualenv's copy of pip, and the same goes for any executables that your
package installs.

Notice that tox printed out a `test command found but not installed in testenv`
warning. This is because the `tox.ini` file is running the executable `sh`
which is a system executable -- there's no `sh` in the virtualenv. By default
tox allows executables from the system `PATH` to be run if they aren't shadowed
by a virtualenv executable, but it prints this warning. We can silence it with
the [`whitelist_externals`](https://tox.readthedocs.io/en/latest/config.html#conf-whitelist_externals)
setting, which is a list of allowed system executables:

<pre><code>[tox]
skipsdist = true

[testenv]
<b>whitelist_externals = sh</b>
commands = sh -c "echo $PATH"</code></pre>

Now tox will run `sh` without a warning:

```console
$ tox
python run-test-pre: PYTHONHASHSEED='3100919638'
python runtests: commands[0] | sh -c 'echo $PATH'
/home/seanh/Dropbox/Desktop/tox/.tox/python/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
__________________________________________________________________ summary ___________________________________________________________________
  python: commands succeeded
  congratulations :)
$
```

### Running multiple commands in sequence

You can easily have tox run a sequence of commands in order by using multiple
commands in the `commands` setting, one command per line:

<pre><code>[tox]
skipsdist = true

[testenv]
whitelist_externals = echo
<b>commands =
    echo This is the first command
    echo This is the second command
    echo This is the third command</b></code></pre>

Many settings in tox can take a list of lines like this, including
`whitelist_externals`, `deps`, `passenv` and `setenv`, etc.

### Command exit codes and tox's exit code

If one of the commands exits with a non-zero exit code tox will stop there
and not continue on to the next commands. For example the UNIX command `false`
exits with code 1. This `tox.ini` file will stop at `false` and not continue
on to the final command:

```ini
[tox]
skipsdist = true

[testenv]
whitelist_externals =
    echo
    false
commands =
    echo This is the first command
    false
    echo This is the third command
```

tox _will_ move on to the next testenv and run that though, if multiple
testenvs are given in [`envlist` / `-e` / `TOXENV` setting](#envlist).

When a command from any one of the testenvs run exits with nonzero then tox
itself will also exit with nonzero, whereas if all commands exited with zero
tox will exit with zero.

You can tell tox to ignore the exit code of a command -- continuing on to the
next command even if that command exits with zero, and not failing the `tox`
command itself if that command fails -- by prepending the command with a `-`.
This `tox.ini` file will run all three commands and exit with zero:

```ini
[tox]
skipsdist = true

[testenv]
whitelist_externals =
    echo
    false
commands =
    echo This is the first command
    -false
    echo This is the third command
```

### Passing command line arguments to commands using `posargs`

You can use tox's `posargs` substitution to allow the user to pass command line
arguments through to the command(s) that tox is running. This is particularly
useful when using tox to run a test runner, such as `pytest`, that has many
useful command line arguments. The user can run `tox -- -x` to run `pytest`
with pytest's `-x` option, for example.

Here's a `tox.ini` file that installs and runs `pytest` and passes any command
line args through:

```ini
[tox]
skipsdist = true

[testenv]
deps = pytest
commands = pytest {posargs} tests/
```

(Here we're using the `deps` setting to tell tox to install `pytest` into the
virtualenv before running the command(s). [More on `deps` later.](#dependencies))

If you just run `tox` this will have pytest run all the tests in your `tests/`
dir (it'll run `pytest tests/`). If you want to pass any command line arguments
to pytest you put them after a `--` in the `tox` command. If no `--` is given
then `{posargs}` evaluates to the empty string. For example to have pytest
print out all its command line arguments and options:

```console
$ tox -- --help
```

You can also give a default value for `posargs` following a `:` within the `{…}`.
When no `--` is used on the command line the default value will be substituted in place of
the `{posargs:DEFAULT_VALUE}`. For example this will run `pytest tests/` by
default but allow the user to narrow down what tests to run with a command like
`tox -- tests/foo/bar`:

```ini
commands = pytest {posargs:tests/}
```

`{posargs}` can be used anywhere in in `tox.ini` and can even be used multiple
times to pass the same positional arguments to multiple commands.

`{posargs}` is an example of a tox **substitution**, [more on substitution later](#substitutions).

`envlist`
---------

So far tox has just been creating a single virtualenv for us named `python`,
using the system's default version of Python. By adding the [`envlist` setting](https://tox.readthedocs.io/en/latest/config.html#conf-envlist)
we can get it to create virtualenvs using different versions of Python and to
create and run multiple testenvs at once:

<pre><code>[tox]
skipsdist = true
<b>envlist = py36</b>

[testenv]
commands = python --version</code></pre>

If you run `tox` with _this_ `tox.ini` file it'll create a `.tox/py36`
virtualenv and run the commands using Python 3.6:

```console
$ tox
py36 create: /home/seanh/Dropbox/Desktop/tox/.tox/py36
py36 run-test-pre: PYTHONHASHSEED='2938378655'
py36 runtests: commands[0] | python --version
Python 3.6.6
__________________________________________________________________ summary ___________________________________________________________________
  py36: commands succeeded
  congratulations :)
$ 
```

This requires Python 3.6 to be installed on the system where `tox` is run. You
need Python 3.6 to create a Python 3.6 virtualenv. The `envlist` setting is a
comma-separated list of testenvs that will be run when you run `tox`. If you
want to run your commands in multiple versions of Python at once you can just
give an `envlist` with multiple Pythons:

<pre><code>[tox]
skipsdist = true
<b>envlist = py27,py36,py37</b>

[testenv]
commands = python --version</code></pre>

`tox` will create `py27`, `py36` and `py37` virtualenvs in `.tox` and run your
commands in each of them in turn (in my case the Python 3.7 testenv fails
because I don't have Python 3.7 on my system):

```console
$ tox
py27 create: /home/seanh/Dropbox/Desktop/tox/.tox/py27
py27 run-test-pre: PYTHONHASHSEED='3564108623'
py27 runtests: commands[0] | python --version
Python 2.7.15rc1
py36 run-test-pre: PYTHONHASHSEED='3564108623'
py36 runtests: commands[0] | python --version
Python 3.6.6
py37 create: /home/seanh/Dropbox/Desktop/tox/.tox/py37
ERROR: InterpreterNotFound: python3.7
__________________________________________________________________ summary ___________________________________________________________________
  py27: commands succeeded
  py36: commands succeeded
ERROR:  py37: InterpreterNotFound: python3.7
$ 
```

The `envlist` setting is the _default_ testenv(s) to run when `tox` is run with
no `-e` argument. `envlist` can be overridden using the `-e` command line
argument. `tox -e py27,py36` will run the `py27` and `py36` testenvs
regardless of what the `envlist` setting in `tox.ini` says.

You can also override `envlist` by setting the `TOXENV` environment variable,
and you can set the envvsr `TOX_SKIP_ENV` to a regular expression and any testenvs
that match the regex will be skipped.

`py27`, `py36`, etc are builtin "factors" that set the version of Python to
use. [These'll be explained properly later](#factors-and-conditionals),
for now they'll have to remain a little mysterious.

Dependencies
------------

You can have tox install the dependencies that your commands need into the
virtualenvs before running the commands, using the [`deps` setting](https://tox.readthedocs.io/en/latest/config.html#conf-deps)
in `tox.ini`.  For example this `tox.ini` file will install `pytest` and all
the requirements listed in your app's `requirements.txt` file and then run
`pytest`:

```ini
[tox]
skipsdist = true

[testenv]
deps =
    pytest
    -r requirements.txt
commands = pytest {posargs:tests/}
```

If the `deps` setting in your `tox.ini` file changes tox will automatically
recreate the virtualenv and reinstall the dependencies the next time you run
it.

By default, though, tox doesn't detect changes to dependencies listed in files when things like
`-r requirements.txt` are used. You would have to tell tox to recreate the virtualenv (with the `tox -r` option)
whenever `requirements.txt` changes. Fortunately the `venv_update` extension, part of the
[`tox-pip-extensions` package](https://github.com/tox-dev/tox-pip-extensions/), automates this.

Environment variables
---------------------

Another thing tox does to help isolate testenvs from the system is that it
removes most of your shell's environment variables from the subshell that it
runs the testenv commands in. You can see this by having a `tox.ini` file print
out all the environment variables available in the testenv using the standard
UNIX `env` command:

```ini
[tox]
skipsdist = true

[testenv]
whitelist_externals = env
commands = env
```

The output of running `tox` will be something like this:

<pre><code>$ tox
python run-test-pre: PYTHONHASHSEED='3478754311'
python runtests: commands[0] | env
<b>LANG=en_GB.UTF-8
VIRTUAL_ENV=/home/seanh/Dropbox/Desktop/tox/.tox/python
TOX_WORK_DIR=/home/seanh/Dropbox/Desktop/tox/.tox
TOX_ENV_NAME=python
TOX_ENV_DIR=/home/seanh/Dropbox/Desktop/tox/.tox/python
PYTHONHASHSEED=3478754311
PATH=/home/seanh/Dropbox/Desktop/tox/.tox/python/bin:...</b>
___________________________________ summary ____________________________________
  python: commands succeeded
  congratulations :)
$ </code></pre>

A handful of environment variables are allowed to pass through by default,
including `PATH` (with the virtuenv's `bin` dir prepended). You can also see
that
[tox injects a few environment variables of its own](https://tox.readthedocs.io/en/latest/config.html#injected-environment-variables)
that you can make use of, such as `TOX_ENV_NAME` (the name of the testenv being run).

If you want to pass more envvars from your shell through, for example to
configure your application, you can do this using the [`passenv` setting](https://tox.readthedocs.io/en/latest/config.html#conf-passenv)
which is a list of additional envvars that can be set in the environment where
`tox` is being run and will be passed in to the testenv where the commands are
run:

```ini
[testenv]
passenv = 
    DATABASE_URL
    ELASTICSEARCH_URL
    PYTEST_ADDOPTS
…
```

You can also use [`setenv`](https://tox.readthedocs.io/en/latest/config.html#conf-setenv)
to set the values of additional envvars in the `tox.ini` file, rather than
reading them from the outside environment:

```ini
[testenv]
setenv =
    DATABASE_URL = postgresql://postgres@localhost/postgres
    ELASTICSEARCH_URL = …
…
```

Substitutions
-------------

As well as being available to the commands that get run, environment variable
values can also be used in the `tox.ini` file itself by using [tox substitution.](https://tox.readthedocs.io/en/latest/config.html#substitutions)

Anywhere in `tox.ini` (for example in a dependency, or in a command) you can
use `{env:ENVVAR_NAME}` to substitute the value of an environment variable.

For example this `tox.ini` file allows you to set the command to be run by setting an environment variable named `COMMAND`.
Test it out with a command like `env COMMAND="echo hi" tox`:

```ini
[tox]
skipsdist = true

[testenv]
passenv = COMMAND
commands = {env:COMMAND}
```

If no `COMMAND` envvar is present tox will exit with an error. You can provide
a default value for this case using a second `:`:

```ini
commands = {env:COMMAND:pytest}
```

Substitutions can be nested, which can allow one envvar to be used as a fallback for another.
This will read the command from the `COMMAND` envvar or, failing that, from `FALLBACK_COMMAND`,
or finally default to `pytest` if neither envvar is set:

```ini
commands = {env:COMMAND:{env:FALLBACK_COMMAND:pytest}}
```

As well as environment variables,
[tox provides a bunch of builtin variables that can be used in substitution](https://tox.readthedocs.io/en/latest/config.html#globally-available-substitutions).
For example `{envtmpdir}` is the path to the virtuenv's temporary directory (which is automatically deleted after each run of `tox`).

This `tox.ini` file uses Sphinx to build a project's documentation (located in
the `docs` dir) and serve it locally for previewing.  It uses `{envtmpdir}` as
the directory for Sphinx's output files (the built documentation HTML files) to
avoid messing up the user's working directory, and so that those files are
automatically cleaned up each run:

<pre><code>[tox]
skipsdist = true

[testenv]
skip_install = true
deps =
    sphinx-autobuild
    sphinx
    sphinx_rtd_theme
changedir = docs
commands =
    sphinx-autobuild -BqT -b dirhtml -d <b>{envtmpdir}/doctrees</b> . <b>{envtmpdir}/html</b></code></pre>

Factors and conditionals
------------------------

[tox's <q>factors</q>](https://tox.readthedocs.io/en/latest/config.html#generating-environments-conditional-settings)
and the conditional settings they enable are one of the most useful and flexible features
of tox. They're the basis of [our `tox.ini` file at Hypothesis](https://github.com/hypothesis/h/blob/master/tox.ini).
But to understand them you have to grock a few tox concepts first:

<dl>
<dt>Testenvs</dt>
<dd><p>A tox <b>testenv</b> is a bunch of settings that define how to create and run
a virtuenv: what version of Python to use, what dependencies to install, what
environment variables to set and to pass through, what commands to run in the
venv once it's ready, etc.</p>

<p>Whenever you run <code>tox</code> you're <q>running</q> one or more testenvs
(the testenvs listed in the <code>envlist</code> setting, <code>-e</code> command line
argument, or <code>TOXENV</code> environment variable).</p></dd>

<dt>Testenv names are lists of factors</dt>
<dd>A testenv name is a <b>minus-separated list of factors</b>.
A testenv named <code>py27</code> contains a single factor, <code>py27</code>.
A more complex testenv name like <code>py27-tests</code> contains two factors
<code>py27</code> and <code>tests</code>.</dd>

<dt>Factors</dt>
<dd><p>A <b>factor</b> is a collection of testenv settings. A testenv like
<code>py27-tests</code> pulls in all of the settings from the <code>py27</code>
factor and the <code>tests</code> factor, and those settings combined become the
testenv's settings.</p>

<p><code>py27</code>, <code>py36</code> etc are <b>builtin factors</b>.
tox comes with builtin factors for all the versions of Python, and you can just
use these in your <code>tox.ini</code> files.
These are factors that contain a single setting: the version of Python to use to
create the virtualenv with
(the <a href="https://tox.readthedocs.io/en/latest/config.html#conf-basepython"><code>basepython</code> setting</a>).

<p>You can also define custom factors in your <code>tox.ini</code> file. <code>test</code> in the
testenv name <code>py27-test</code> is a custom factor.</p></dd>

<dt>Conditionals</dt>
<dd><p>Whenever you give a list of things in your <code>tox.ini</code> file (for
example the lists of environment variables to pass through, dependencies to
install, and commands to run) items in the list can be made conditional on a factor
by prefixing them with <code>factorname: </code>.
For example in this <code>tox.ini</code> snippet:</p>

<pre><code>[testenv]
deps = 
    tests: pytest</code></pre>

<p>the <code>tests: pytest</code> implicitly creates a custom factor named <code>tests</code>
and tells tox to install the <code>pytest</code> dependency only when the <code>tests</code> factor
is invoked. <code>tox -e py27-tests</code> will install pytest but <code>tox -e py27-docs</code> won't.</p></dd>
</dl>

Below is a simplified version of [the Hypothesis `tox.ini` file](https://github.com/hypothesis/h/blob/master/tox.ini)
that uses factors and conditionals to define separate testenvs for running the
dev server, running the linter, running the tests, and building the docs. This
enables the following `tox` commands:

* `tox` runs the tests in Python 2.7 (`py27-tests` is the default `envlist`)

* You can run the tests in any version of Python (as long as you have that version
  of Python installed on your system) by using different testenv names:
  `tox -e py27-tests` runs the tests in Python 2.7, whereas `tox -e py36-tests`
  or `tox -e py37-tests` run the tests in Python 3.6 or 3.7. 

* `tox -e py27-dev` runs the dev server in Python 2.7.
  As with the tests you can run the dev server in any version of Python using
  commands like `tox -e py36-dev`.

* `tox -e py36-lint` runs the linter, and `tox -e py36-docs` builds the docs
  and serves them locally.

As you can see the `tox.ini` file is designed to enable `pyXY-COMMAND`
testenvs, where `pyXY` is any version of Python and `COMMAND` is any of the
provided commands (`tests`, `dev`, `lint`, etc). It can be extended by adding
as many commands as you like, automating all of your development tasks.

Here's the `tox.ini` file:

```ini
[tox]
envlist = py27-tests
skipsdist = true
requires = tox-pip-extensions
tox_pip_extensions_ext_venv_update = true

[testenv]
skip_install = true
passenv =
    dev:   AUTHORITY
    dev:   BOUNCER_URL
    dev:   CLIENT_OAUTH_ID
    dev:   CLIENT_RPC_ALLOWED_ORIGINS
    dev:   CLIENT_URL
    dev:   SENTRY_DSN
    dev:   USE_HTTPS
    dev:   WEBSOCKET_URL
    tests: TEST_DATABASE_URL
    tests: ELASTICSEARCH_URL
    tests: PYTEST_ADDOPTS
deps =
    dev:   ipython
    dev:   ipdb
    dev:   -r requirements-dev.in
    lint:  flake8
    lint:  flake8-future-import
    tests: coverage
    tests: pytest
    tests: factory-boy
    tests: mock
    tests: hypothesis
    tests: -r requirements.txt
    docs:  sphinx-autobuild
    docs:  sphinx
    docs:  sphinx_rtd_theme
whitelist_externals = dev: sh
changedir = docs: docs
commands =
    python --version
    dev:   sh bin/hypothesis --dev init
    dev:   sh bin/hypothesis devserver {posargs}
    lint:  flake8 src tests
    tests: pytest {posargs:tests/h/}
    docs:  sphinx-autobuild -BqT -b dirhtml -d {envtmpdir}/doctrees . {envtmpdir}/html
```

To explain how this works, consider how tox treats the `commands` section of
the `tox.ini` file when you run `tox -e py36-dev`:

<pre><code>commands =
    <b>python --version</b>
    dev:   <b>sh bin/hypothesis --dev init</b>
    dev:   <b>sh bin/hypothesis devserver {posargs}</b>
    lint:  flake8 src tests
    tests: pytest {posargs:tests/h/}
    docs:  sphinx-autobuild -BqT -b dirhtml -d {envtmpdir}/doctrees . {envtmpdir}/html</code></pre>

tox reads the `commands` list from top to bottom and runs only the commands
that match the testenv name. `python --version` is an unconditional command (no
`factor:` prefix), so that always gets run. The two `dev:` commands match the `dev`
factor in <code>py36-<b>dev</b></code> so they get run. The other commands
conditions don't match so they're ignored. The matching commands are run in the
order that they appear in the file.

This same matching procedure is applied to all lists in the `tox.ini` file:
`passenv`, `deps`, etc. When you run `tox -e py36-dev` tox first collects all
the settings in the builtin `py36` factor (the Python version: 3.6), then it
parses the `tox.ini` file and collects all settings that are either
unconditional or whose condition matches one of the factors `py36` or `dev`.
These collected settings form the testenv definition, and tox runs it.

More complex conditions are also possible. The most useful of these is to
reduce duplication by making a single line match multiple factors by giving a
comma-separated list of factors in `{…}`'s. This will install
`requirements.txt` if either the `tests` or the `dev` factor is invoked:

```ini
deps =
    {tests,dev}: -r requirements.txt
```

Negation, logic, etc are also possible. See [Complex factor conditions](https://tox.readthedocs.io/en/latest/config.html#complex-factor-conditions)
in the tox docs for details.

Debugging your `tox.ini` file with `--showconfig`
-------------------------------------------------

Once you've started adding conditionals to your `tox.ini` file it can be useful
to have a good way to debug it. Given a `tox.ini` file like the one above, and
a command like `tox -e py27-dev`, adding the `--showconfig` option will get tox
to print out the entire collected `py27-dev` testenv definition instead of
running the testenv's commands:

```console
$ tox -e py27-dev --showconfig
tool-versions: tox-3.5.2 virtualenv-16.0.0
config-file: 
toxinipath: /home/seanh/Projects/h/tox.ini
toxinidir:  /home/seanh/Projects/h
toxworkdir: /home/seanh/Projects/h/.tox
setupdir:   /home/seanh/Projects/h
distshare:  /home/seanh/.tox/distshare
skipsdist:  True

[testenv:py27-dev]
  envdir          = /home/seanh/Projects/h/.tox/py27-dev
  setenv          = SetenvDict: {'TOX_ENV_NAME': 'py27-dev', 'TOX_ENV_DIR': '/home/seanh/Projects/h/.tox/py27-dev', 'PYTHONHASHSEED': '2540689914'}
  basepython      = python2.7
  description     = 
  envtmpdir       = /home/seanh/Projects/h/.tox/py27-dev/tmp
  envlogdir       = /home/seanh/Projects/h/.tox/py27-dev/log
  downloadcache   = None
  changedir       = /home/seanh/Projects/h
  args_are_paths  = True
  skip_install    = True
  ignore_errors   = False
  recreate        = False
  passenv         = set(['LANG', 'PIP_INDEX_URL', 'LANGUAGE', 'TOX_WORK_DIR', 'SENTRY_DSN', 'CLIENT_URL', 'AUTHORITY', 'CLIENT_RPC_ALLOWED_ORIGINS', 'WEBSOCKET_URL', 'USE_HTTPS', 'BOUNCER_URL', 'CLIENT_OAUTH_ID', 'PATH', 'LD_LIBRARY_PATH', 'TMPDIR'])
  whitelist_externals = ['sh']
  platform        = .*
  sitepackages    = False
  alwayscopy      = False
  pip_pre         = False
  usedevelop      = False
  install_command = [u'pip-faster', u'install', u'{opts}', u'{packages}', 'venv-update>=2.1.3']
  list_dependencies_command = ['python', '-m', 'pip', 'freeze']
  deps            = [ipython, ipdb, -rrequirements-dev.in]
  commands        = [['python', '--version'], ['sh', 'bin/hypothesis', '--dev', 'init'], ['sh', 'bin/hypothesis', 'devserver']]
  commands_pre    = []
  commands_post   = []
  ignore_outcome  = False
  extras          = []
```

Generative envlists
-------------------

So far we've mostly ran one or two testenvs at a time with commands like `tox
-e py36-tests` or default `envlist` settings like `envlist = py27-tests,py36-tests`.
It isn't much use to us at Hypothesis but for completeness sake tox also has a
[Generative envlist](https://tox.readthedocs.io/en/latest/config.html#generative-envlist)
feature that allows you to run many testenvs at once without having to spell
out every single testenv name. This is useful for projects that need to support
a lot of combinations of different versions of Python, different versions of
dependencies, and different platforms at once. A single `tox` command can run
your tests in with all the different combinations. Here's an example from the docs:

```ini
envlist = {py27,py36}-django{15,16}, docs, flake
```

With this `envlist` setting a single `tox` command will generate the
"cross product" of the different versions of Python and Django and run
each possible combination. It will run all of these testenvs:

* `py27-django15`
* `py27-django16`
* `py36-django15`
* `py36-django16`
* `docs`
* `flake`

Defining testenvs using `[testenv:NAME]` sections
----------------------------------------------

So far we've had a single `[testenv]` section in our `tox.ini` and we've used
conditionals to define multiple testenvs. There's also an entirely different
way to define your testenvs in your `tox.ini`: using a separate `[testenv:NAME]`
section for each testenv. Here's an example of a `tox.ini` file that supports
`tox` or `tox -e py27` to run the tests in Python 2.7, and `tox -e py27-dev`
and `tox -e py36-dev` to run the dev server in Python 2.7 or 3.6:

```ini
[tox]
envlist = py27-tests
skipsdist = true

[testenv]
skip_install = true

[testenv:py27-tests]
description = Run the tests in Python 2.7
deps =
    coverage
    mock
    …
    -rrequirements.txt
passenv =
    TEST_DATABASE_URL
    ELASTICSEARCH_URL
    PYTEST_ADDOPTS
commands =
    coverage run --parallel --source h,tests/h -m pytest -Werror {posargs:tests/h/}

[dev]
deps = -rrequirements-dev.in
passenv =
    ALLOWED_ORIGINS
    AUTHORITY
    BOUNCER_URL
    …
whitelist_externals = sh
commands =
    sh bin/hypothesis --dev init
    {posargs:sh bin/hypothesis devserver}

[testenv:py27-dev]
description = Run the dev server in Python 2.7
deps = {[dev]deps}
passenv = {[dev]passenv}
whitelist_externals = {[dev]whitelist_externals}
commands = {[dev]commands}

[testenv:py36-dev]
description = Run the dev server in Python 3.6
deps = {[dev]deps}
passenv = {[dev]passenv}
whitelist_externals = {[dev]whitelist_externals}
commands = {[dev]commands}
```

Any settings in the `[testenv]` section apply to all testenvs, unless
overridden. You then define each testenv in its own section, for example the
`[testenv:py27-tests]` section contains the settings for the `py27-tests` env
(`tox -e py27-tests`).

The `[dev]` section doesn't define a testenv and isn't used by tox. It's just a bag of settings
to be used in substitution by the `[testenv:py27-dev]` and `[testenv:py36-dev]` sections below.
For example when `[testenv:py27-dev]` does `deps = {[dev]deps}` that means pull
in all the deps from the `[dev]` section. You can also pull in some deps and then add more:

```ini
[testenv:py27-dev]
deps =
    {[dev]deps}
    ipython
    ipdb
```

These are called [section substitutions](https://tox.readthedocs.io/en/latest/config.html#substitution-for-values-from-other-sections).
Using substitutions like this is a way to avoid duplication. It's almost like
inheritance, where `[testenv:py27-dev]` and `[testenv:py36-dev]` are child
sections and `[dev]` is the base section they inherit from. But there's no way
to automatically inherit all the settings from a base section at once: you have
to inherit each section individually with a substitution.

One advantage of writing your `tox.ini` file this way is that you can add a
`description` to each testenv, and if you run `tox -av` it'll list all the
available testenvs and their descriptions:

```console
$ tox -av
using tox.ini: /home/seanh/Projects/h/tox.ini
using tox-3.5.2 from /usr/local/lib/python2.7/dist-packages/tox/__init__.pyc
default environments:
py27-tests      -> Run the tests in Python 2.7

additional environments:
py27-dev        -> Run the dev server in Python 2.7
py36-dev        -> Run the dev server in Python 3.6
```

Overall, though, we found this way of writing `tox.ini` files produced much
larger files that contained a lot more boilerplate and duplication, and were
more difficult to read and to work with. The file above only supports running
the dev server in Pythons 2.7 and 3.6, for example. To run it in Python 3.7
you'd have to add a new `[testenv:py37-dev]` section.

The factors and conditionals approach produces a much smaller `tox.ini` file
while also enabling any command to be run with any version of Python.

You can also [combine both approaches in a single `tox.ini`](https://tox.readthedocs.io/en/latest/config.html#factors-and-values-substitution-are-compatible).

Grab bag
--------

Some other cool stuff that tox can do:

* [Interactive shell substitution](https://tox.readthedocs.io/en/latest/config.html#interactive-shell-substitution).
  You can use substitutions like `{tty:ON_VALUE:OFF_VALUE}` to have `ON_VALUE` be used when tox
  is run in an interactive shell (e.g. on a developer's laptop) and `OFF_VALUE` be used when its
  run non-interactively (e.g. on CI). You could use this, for example, to pass the `--pdb` argument
  to `pytest` to make it drop in to a debugger prompt when a test fails, but only when tox is
  being run interactively.
  
* Jenkins support. You can add a `[tox:jenkins]` section containing global settings
  overrides that should be used only when tox is running in Jenkins.
  See [Jenkins override](https://tox.readthedocs.io/en/latest/config.html#jenkins-override).

* Force a particular version of a dependency just once with [`--force-dep`](https://tox.readthedocs.io/en/latest/config.html#cmdoption-tox-force-dep).

