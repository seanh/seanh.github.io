Title: The Hypothesis Development Environment
Status: draft

At Hypothesis we've strived to create a friendly and consistent development
environment across all our projects, including apps, shared libraries, API
clients and command line tools, and frontend and backend projects. Different
types of projects have different requirements, but our approach to development
environments is able to adapt to them all.

All our projects have the same installation steps, use the same tools, and have
the same commands for using the development environment.

This post documents the overall approach, as an introduction for new Hypothesis
developers and to help us keep things in rhythm as we evolve our development
setup in future.

Installation
------------

The standard installation procedure for a Hypothesis project is to install some
prerequisites if you don't have them already (git, Docker and Docker Compose,
Make, pyenv, ... they'll all be listed at the top of the project's README) and
then do:

    #!console
    $ git clone https://github.com/hypothesis/EXAMPLE_PROJECT.git
    $ cd EXAMPLE_PROJECT
    $ make dev

You've now installed the EXAMPLE_PROJECT's development environment and you're
running the app in the development web server.

`make dev` will have taken a while to start up the first time because it was
installing the necessary versions of Python, creating virtualenvs, and
installing dependencies. Next time it'll start much faster because, unless
there's been a change in the project's requirements, it won't need to install
anything. (And if the requirements have changed it only installs the new and
upgraded ones.)

For apps that require services (like Postgres or Elasticsearch etc) it's
currently necessary to run `make services` first, before running `make dev`, to
start the services. This can be automated in time.

If the project isn't an app (for example if it's a shared library, API client,
command line tool, etc) then it might not have a dev server so `make dev` won't
work. Try `make test` to run the tests instead, or `make lint` to run the linters.

If you <kbd><kbd>Ctrl</kbd> + <kbd>c</kbd></kbd> the `make dev` command and
then run `make help`, you'll see the full list of dev environment commands that
EXAMPLE_PROJECT has available. These can vary a little between projects but for
the most part all Hypothesis projects have the same set of commands:

    #!console
    $ make help
    make help              Show this help message
    make services          Run the services that `make dev` requires
                           (Postgres, Elasticsearch, etc) in Docker Compose
    make dev               Run the app in the development server
    make shell             Launch a Python shell in the dev environment
    make sql               Connect to the dev database with a psql shell
    make lint              Run the code linter(s) and print any warnings
    make format            Correctly format the code
    make checkformatting   Crash if the code isn't correctly formatted
    make test              Run the unit tests
    make coverage          Print the unit test coverage report
    make codecov           Upload the coverage report to codecov.io
    make docs              Build docs website and serve it locally
    make docstrings        View all the docstrings locally as HTML
    make pip-compile       Compile requirements.in to requirements.txt
    make docker            Make the app's Docker image
    make clean             Delete development artefacts (cached files, 
                           dependencies, etc)

For the rest of this guide we'll go through the tools that we use to implement
all these commands, and what we use each tool for.

Our general approach to tools is to choose lightweight "**do one thing and do
it well**" tools, and then use the Makefile to glue them all together.

For the most part you don't need to understand these tools, or interact with
them directly, in order to use the development environment. Make provides all
the basic commands for you. But it can be interesting and useful to know how
it's all put together.

I'll link to real examples from <https://github.com/hypothesis/h> throughout.

Docker Compose
--------------

Config file: `docker-compose.yml`

We use Docker Compose for one thing in development: installing services and
running them in the background. Specifically, PostgreSQL, Elasticsearch and
RabbitMQ are used by some of our apps at the time of writing. Installing and
running each of these yourself used to be a nightmare. With Docker Compose you
just run `make services` (which runs `docker-compose up -d`) and it installs
and starts them for you.

Docker is the heaviest thing you have to install on your computer to do
Hypothesis development, but it's worth it. Our Makefile and tox will then
install Docker Compose automatically. Once it's installed developers never have
to interact with Docker directly -- it's all handled by the Makefile.

### Docker Compose Crash Course

TODO

pyenv
-----

Config file: `.python-version`
Owns directory: `~/.pyenv`
Manages: `$PATH`

pyenv installs multiple exact patch versions of Python into `~/.pyenv/` and
automatically switches between them (taking them in and out of your `$PATH`) as
you `cd` into different project directories.

pyenv is how we make sure that each developer has the needed versions of Python
for each project installed on their machine, that they're running each project
with exactly the right version of Python (the same version as used in
production), and how we install new versions of Python as our projects upgrade
to them.

A key feature of pyenv is that it can provide **multiple versions of Python**
for a single project. App or library that has to support multiple versions; or
is transitioning; or needs to run some dev environment command with a different
version of Python; etc.

pyenv makes Python version upgrades invisible to developers. When the
version(s) of Python that a project requires change we simply change the
`.python-version` file and commit it to git. When each developer `git pull`s
this commit, the next time they run `make <something>` a script that Makefile
calls will install the new versions of Python if they aren't installed already.

Aside from installing pyenv itself Hypothesis developers never have to interact
with pyenv directly -- we have scripts, called by the Makefile, that automate
installing and activating Python versions.

tox
---

Config file: `tox.ini`
Owns directory: `.tox`

tox is our virtualenv manager and Python development task automator, and it's
**awesome**.

Because of tox developers never have to (re-)create Python virtualenvs or
install and update Python dependencies. You needn't even know that virtualenvs
and Python dependencies exist. And you don't even need to install or call tox --
Makefile does it for you.

Honcho
------

Config file: `Procfile`

Honcho **runs multiple processes at once in a single terminal**, and
interleaves their stdouts into that one terminal. So when an app has a web
server, a background worker, an assets builder, etc, you don't need to open
multiple tabs and start multiple different commands in them.

This is all we use Honcho for -- so that you don't have to open more than one
window or tab per app if you don't want to.

Hypothesis developers don't need to install Honcho or use it directly, it's
installed and called by the Makefile and tox. You needn't know it exists.

Make
----

Config file: `Makefile`

Finally, GNU Make is the frontend to our development environment, providing
commands for interacting with all the components (both backend and frontend).
Running `make help` in any project will print out a list of that project's
commands.

You can still call tox, honcho, docker-compose, gulp, and everything directly
if you want to. Make just provides a map, a single source of truth, and
convenient access to common commands.

### Shell Scripts

Some things are just easier to write as standalone shell scripts, rather than
in the Makefile. These can be found in the project's `bin/` directory. You
don't really need to know about these or call them yourself -- Makefile calls
them.

Other Commands in Makefile
--------------------------

* All backend projects have a `make shell` command that starts a Python shell in the
  project's development environment for experimenting and trying things out.

  All the project's Python dependencies are available to import and useful
  objects like a request and a database session are provided.

* All projects that have an SQL database have a `make sql` command that connects to that
  database with a `psql` shell so that you can inspect it. (`psql` will be installed for
  you.)

* `make format` runs the Python and JavaScript code formatters and the project's entire
  codebase.

* `make coverage` prints out a file-by-file test coverage report, with uncovered lines
  numbers listed.

* Projects that have a Sphinx documentation site have a `make docs` command for building
  the docs previewing them locally, with live reloading.

* Python projects have a `make docstrings` command that renders the Python docstrings
  using Sphinx's autodoc extension and serves them locally so that you can check them.

* Python projects have a `make pip-compile` command that re-compiles the `requirements.txt`
  file from `requirements.in`, when you've added a new dependency to `requirements.in`
  (or removed a dependency). (The `pip-compile` tool that this uses will be installed
  automatically.)

  TODO: A command for upgrading a dependency.

* Every app has `make docker` and `make run-docker` commands for building the production
  Docker image and running it locally, so that you can test the `Dockerfile`.
