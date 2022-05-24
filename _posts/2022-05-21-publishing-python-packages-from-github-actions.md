How to Publish a Python Package from GitHub Actions
===================================================

<p class="lead" markdown="1">A simple way to use
[GitHub Actions](https://github.com/actions) to build your Python package, bump the
version number, and publish it to [GitHub releases](https://github.com/seanh/gha-python-packaging-demo/releases)
and [PyPI.org](https://pypi.org/project/gha-python-packaging-demo/) all with a
single click of a button in the web interface.</p>

<div class="warning" markdown="1">
**Warning:** I haven't tested this much with real Python packages yet so your
mileage may vary.  It seems to work with the demo project.
</div>

When I want to publish a new release of one of my Python packages
I just browse to
[my `release.yml` workflow in the **Actions** tab](https://github.com/seanh/gha-python-packaging-demo/actions/workflows/release.yml)
and click the <kbd>Run workflow</kbd> button:

![Running the release workflow]({{ "/assets/images/run_workflow_button.png" | relative_url }} "Running the release workflow")

This runs a GitHub Actions workflow that increments the patch version number,
creates a new [GitHub release](https://github.com/seanh/gha-python-packaging-demo/releases)
with a generated changelog, creates a corresponding git tag, and
[publishes the release to PyPI](https://pypi.org/project/gha-python-packaging-demo/#history).

If I feel like it I can create a new release manually using GitHub's web
interface instead. This allows me to choose my own version number (in case I
want to bump the major or minor version instead of the patch version) and lets
me write my own release notes. Manually-created releases still trigger the
GitHub Actions workflow that builds the package and uploads it to PyPI:

![Publishing a GitHub release]({{ "/assets/images/github_release.png" | relative_url }} "Publishing a GitHub release")

In fact GitHub releases created by **any** means trigger the package build and
upload workflow.  For example I could run GitHub CLI's [`gh release
create` command](https://cli.github.com/manual/gh_release_create) from any
directory on my local machine. This doesn't require me to have a local copy of
the project or to have anything setup locally other than GitHub CLI itself.
The `--generate-notes` automatically generates a title and notes for the
release:

```terminal
$ gh release create 0.0.1 --repo seanh/gha-python-packaging-demo --generate-notes
https://github.com/seanh/gha-python-packaging-demo/releases/tag/0.0.1
```

The rest of this post will walk through setting this up. It's all very simple
and easy...

* This unordered list will be replaced with a table of contents.
{:toc}

The demo repo
-------------

We're going to be using [github.com/seanh/gha-python-packaging-demo/](https://github.com/seanh/gha-python-packaging-demo)
as an example. The example repo contains a Python package with all the
tooling needed to implement our GitHub Actions-based release process:

    python-packaging-demo/
      pyproject.toml
      setup.cfg
      src/
        python_packaging_demo/
          __init__.py
          app.py
      .github/
        workflows/
          release.yml
          publish.yml
        scripts/
          release.py

setup.cfg
---------

I'm gonna skip over [`setup.cfg`](https://github.com/seanh/gha-python-packaging-demo/blob/main/setup.cfg)
because it's just a normal `setup.cfg` file, it doesn't contain anything relevant to our GitHub Actions-based
packaging solution. The demo package's `setup.cfg` is exactly like
[the `setup.cfg` from the Python Packaging User Guide's packaging tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/#configuring-metadata)
except that I added a console script entry point (which we'll be using later to
demonstrate [how to implement `--version`](#the---version-command)).

One thing worth saying is that your package's name needs to be unique across all of PyPI,
so visit [pypi.org/project/YOUR_PROJECT_NAME/](https://pypi.org/project/YOUR_PROJECT_NAME/)
and make sure your name isn't already taken.

`pyproject.toml` and setuptools_scm
-----------------------------------

Here's the contents of
[`pyproject.toml`](https://github.com/seanh/gha-python-packaging-demo/blob/main/pyproject.toml):

<pre><code>[build-system]
requires = ["setuptools>=45"<b>, "setuptools_scm[toml]>=6.2"</b>]
build-backend = "setuptools.build_meta"

<b>[tool.setuptools_scm]</b></code></pre>

This is the same as the
[`pyproject.toml` from the Python Packaging User Guide's packaging tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/#creating-pyproject-toml)
but with the two parts in bold added. These two additions add
[setuptools_scm](https://github.com/pypa/setuptools_scm/) (following the
[instructions in their README](https://github.com/pypa/setuptools_scm/#pyprojecttoml-usage)).

setuptools_scm extracts the version number from the project's git tags during
the build process and injects it into the package that gets built.
This means **there's no version number anywhere in the source tree**.
There's no version number in `pyproject.toml` or `setup.cfg` or in the Python code.
The git tags are the single source for version numbers.
This is crucial to the packaging scripts we'll be using below because it means
you don't need to create and push a git commit in order to do a release.
You just need to create a new git tag.
And GitHub does that for you when you create a GitHub release.

setuptools_scm should be a solid dependency:
it's [mentioned](https://packaging.python.org/en/latest/guides/single-sourcing-package-version/?highlight=setuptools_scm#single-sourcing-the-package-version)
in the Python Packaging User Guide, it's owned by the [Python Packaging Authority](https://github.com/pypa)
on GitHub, at the time as writing it's on version 6.4.2, its been around since
2010 and it's still actively maintained.

Create a PyPI API token
-----------------------

The `publish.yml` workflow below needs a PyPI API token to upload releases of
your package to PyPI.

[Create a free PyPI.org account](https://pypi.org/account/register/) if you don't already have one,
log in,
go to your account settings,
and go to the [Add API Token](https://pypi.org/manage/account/token/) page.
You need to create an **unscoped** API token.
You can't scope the API token to the project yet because the project doesn't
exist on PyPI yet so it doesn't appear as an option in the scopes dropdown.
You can [replace the token with a scoped one](#replace-the-pypi-token-with-a-scoped-one)
after publishing the project's first release.

![Creating a PyPI API token]({{ "/assets/images/creating_a_pypi_api_token.png" | relative_url }} "Creating a PyPI API token")

Add the PyPI API token to the GitHub project's secrets
------------------------------------------------------

You need to add the PyPI API token to your GitHub project's secrets to make it
available to the `publish.yml` workflow.

Go to the GitHub project's <samp>Settings</samp> tab, go to
<samp>Secrets &rarr; Actions</samp>, and click
<kbd>New repository secret</kbd>.
Enter `PYPI_API_TOKEN` as the name and paste in the PyPI API token as the value
then click <kbd>Add secret</kbd>:

![Pasting the PyPI API token into GitHub secrets]({{ "/assets/images/github_secret.png" | relative_url }} "Pasting the PyPI API token into GitHub secrets")

The `publish` workflow
--------------------

[`publish.yml`](https://github.com/seanh/gha-python-packaging-demo/blob/main/.github/workflows/publish.yml)
is a GitHub Actions workflow that triggers whenever a GitHub release is
created. It builds the Python package and uploads it to PyPI. It's 17 lines:

```yaml
name: Publish to PyPI.org
on:
  release:
    types: [published]
jobs:
  pypi:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - run: python3 -m pip install --upgrade build && python3 -m build
      - name: Publish package
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: {% raw %}${{ secrets.PYPI_API_TOKEN }}{% endraw %}
```

Some notes:

* This part:

  ```yaml
  on:
    release:
      types: [published]
  ```

  causes the workflow to be automatically triggered whenever a new GitHub
  release is published. See [Events that trigger workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)
  in the GitHub Actions docs.

* The `fetch-depth: 0` causes the [checkout action](https://github.com/marketplace/actions/checkout)
  to fetch all branches and tags instead of only fetching the ref/SHA that
  triggered the workflow. This is necessary for setuptools_scm to work,
  otherwise it wouldn't be able to find the version number from the git tags.

* The `python3 -m pip install --upgrade build && python3 -m build` is what
  actually builds the Python package. These are the standard Python packaging
  commands, straight from the
  [Python Packaging User Guide's tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives).

* Finally, we use the [pypa/gh-action-pypi-publish](https://github.com/marketplace/actions/pypi-publish)
  GitHub Action from the Python Packaging authority to actually upload the
  package to PyPI.

  The `{% raw %}${{ secrets.PYPI_API_TOKEN }}{% endraw %}` passes the API token
  that you added to the project's GitHub secrets through to
  `gh-action-pypi-publish` which will use it to authenticate to PyPI.

Create the first release
------------------------

You can now create a GitHub release and it'll trigger the publish workflow to
build the package and upload it to PyPI.

Go to the GitHub project's <samp>Releases</samp> page and click the
<kbd>Create a new release</kbd> button.
In the <samp>Choose a tag</samp> field enter `0.0.1` and click
<samp>Create new tag: 0.0.1 on publish</samp>.
Click <kbd>Publish release</kbd>:

![Publishing a GitHub release]({{ "/assets/images/github_release.png" | relative_url }} "Publishing a GitHub release")

Alternatively, instead of using the web interface you can install
[GitHub CLI](https://cli.github.com/) on your local machine and run:

```terminal
$ gh release create 0.0.1 --repo seanh/gha-python-packaging-demo --title "First release!" --notes "This is the first release!"
```

Either way publishing a release will trigger the `publish.yml` workflow and the
package will be built and uploaded to PyPI.  You can browse to the **Publish to
PyPI.org** workflow on the project's **Actions** page and view
[the logs](https://github.com/seanh/gha-python-packaging-demo/runs/6557828531).

You should also be able to browse to [the project's release history on PyPI](https://pypi.org/project/gha-python-packaging-demo/#history)
and see that the package release has been uploaded.

Replace the PyPI token with a scoped one
----------------------------------------

Now that you've published the first release the project will start appearing in
the list of scopes when creating an API token on PyPI.  You can go back to your
PyPI account settings, delete the unscoped token, create a new token scoped to
the project, and update the value of the `PYPI_API_TOKEN` GitHub secret with
the new token.

![Creating a scoped PyPI API token]({{ "/assets/images/scoped_pypi_api_key.png" | relative_url }} "Creating a scoped PyPI API token")

That's it!
----------

From now on each time you create a new GitHub release using either the GitHub
web UI or GitHub CLI your Python package will be built and uploaded to PyPI.

You could stop here
-------------------

We've gotten as far as being able to create a GitHub release with either the
GitHub web UI or GitHub CLI and having that release be automatically built and
published to PyPI. And all we needed was setuptools_scm in `pyproject.toml`,
a 17-line GitHub Actions workflow
and a PyPI API token in the project's GitHub secrets.
This is really very simple and you could just stop here and keep using it.

But having to manually enter the version number for every release could be error prone,
especially if you release a lot of packages.
It'd be nice if GitHub CLI could generate the version number for you.
Until then, we can implement that ourselves by adding just a little more code...

Automatically generating the next version number
------------------------------------------------

### The `release.py` script

[`release.py`](https://github.com/seanh/gha-python-packaging-demo/blob/main/.github/scripts/release.py)
is a short Python script that generates a version number and calls GitHub CLI
to create a new release. If the project doesn't have any releases yet it'll use
`0.0.1` as the first version number.  Otherwise it'll +1 the patch number of
the last release: `0.0.2`, `0.0.3`, and so on.

Make sure you mark this script as executable:

```terminal
$ chmod u+x .github/workflows/scripts/release.py
```

As long as you have GitHub CLI installed you can run this script locally to
create releases with auto-incrementing version numbers. It should be compatible
with your operating system's version of Python and it doesn't have any
dependencies, so it should just work:

```terminal
$ .github/scripts/release.py
https://github.com/seanh/gha-python-packaging-demo/releases/tag/0.0.3
```

[The release](https://github.com/seanh/gha-python-packaging-demo/releases/tag/v0.0.3)
will get a **Full Changelog** that links to a view of the new commits that were
included in the release. I think the auto-generated changelogs look better if
you actually use pull requests, which I haven't been doing in these
screenshots:

![A GitHub release generated by release.py]({{ "/assets/images/release.png" | relative_url }} "A GitHub release generated by release.py")

![A GitHub release generated by release.py]({{ "/assets/images/commits.png" | relative_url }} "A GitHub release generated by release.py")

And of course creating a release with this script will trigger the publish
workflow to upload the package to PyPI, just like creating a release in the web
interface or by using GitHub CLI would do.

If you want to increment the major or minor version number you have to create a
release manually to do that, then you can go back to using `release.py` and
it'll start generating patch numbers on top of your new major or minor numbers.
(It would be easy to add `--major` and `--minor` arguments to `release.py` if
you want to be able to use it to generate major and minor releases as well.)

### The release workflow

If you want to be able to run `release.py` on GitHub Actions you need to add a
workflow for it.
[`release.yml`](https://github.com/seanh/gha-python-packaging-demo/blob/main/.github/workflows/release.yml)
is a 12-line manually-triggered workflow that runs the `release.py` script on
GitHub Actions:

```yml
name: Create a new patch release
on: [workflow_dispatch]
jobs:
  github:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Create new patch release
        run: .github/scripts/release.py
        env:
          GITHUB_TOKEN: {% raw %}${{ secrets.PERSONAL_ACCESS_TOKEN }}{% endraw %}
```

Note:

* The `on: [workflow_dispatch]` means that this workflow never runs
  automatically, it can only be triggered by the <kbd>Run workflow</kbd>
  button:

  ![Running the release workflow]({{ "/assets/images/run_workflow_button.png" | relative_url }} "Running the release workflow")

* The `{% raw %}${{ secrets.PERSONAL_ACCESS_TOKEN }}{% endraw %}` passes a
  personal access token through to GitHub CLI to use to authenticate to the
  GitHub API.

To get this to work you need to [create a GitHub personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
and add it to the project's GitHub secrets.

<details markdown="1">
<summary>Why not just use <code>GITHUB_TOKEN</code>?</summary>
The normal way to use GitHub CLI from GitHub actions would be to just use the
[`{% raw %}${{ secrets.GITHUB_TOKEN }}`{% endraw %}](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)
that GitHub makes available to actions by default.
That won't work in this case because we're counting on the GitHub release that
the release workflow creates to trigger the separate publish workflow, and
[events triggered when using `GITHUB_TOKEN` don't trigger new workflow runs.](https://docs.github.com/en/actions/using-workflows/triggering-a-workflow#triggering-a-workflow-from-a-workflow)
So we have to use a personal access token instead.
</details>

Go to your GitHub account settings,
go to [Developer settings &rarr; Personal access tokens](https://github.com/settings/tokens),
and click <kbd>Generate new token</kbd>. The token needs to have the **repo**
scopes but doesn't need any of the others.

![Creating a GitHub personal access token]({{ "/assets/images/creating_pat.png" | relative_url }} "Creating a GitHub personal access token")

Then go to the project's GitHub Actions secrets and create a new secret named
`PERSONAL_ACCESS_TOKEN` with the value of the token you just generated:

![Adding the personal access token to GitHub secrets]({{ "/assets/images/pasting_pat.png" | relative_url }} "Adding the personal access token to GitHub secrets")

With the personal access token in place you can now trigger the release
workflow from the project's GitHub Actions page.
Go to the **Create a new patch release** workflow and click the <kbd>Run workflow</kbd> button:

![Running the release workflow]({{ "/assets/images/running_the_release_workflow.png" | relative_url }} "Running the release workflow")

When the release workflow finishes there'll be a new GitHub release in the
project and a new run of the publish workflow will start. When the publish
workflow finishes there'll be a new release on PyPI:

![The release workflow triggering the publish workflow]({{ "/assets/images/release_and_publish.png" | relative_url }} "The release workflow triggering the publish workflow")

You just generated a new version number, created a GitHub release, built your
Python package, and uploaded it to PyPI with a single click of a <kbd>Run
workflow</kbd> button!

The `--version` command
-----------------------

What if you want to add a `--version` command to app that prints the version
number? How can you get access to the version number from the Python code?

You just call `importlib.metadata.version()`. Here's the relevant code from
[`app.py`](https://github.com/seanh/gha-python-packaging-demo/blob/main/src/gha_python_packaging_demo/app.py):

```python
import sys
from argparse import ArgumentParser
from importlib.metadata import version


def entry_point():
    parser = ArgumentParser()
    parser.add_argument("-v", "--version", action="store_true")

    args = parser.parse_args()

    if args.version:
        print(version("gha_python_packaging_demo"))
        sys.exit()
```

If you install `gha-python-packaging-demo` and run
`gha_python_packaging_demo --version` it'll print the version number:

```terminal
$ pipx install gha-python-packaging-demo
  installed package gha-python-packaging-demo 0.0.6, installed using Python 3.10.4
  These apps are now globally available
    - gha_python_packaging_demo
done! ✨ 🌟 ✨
$ gha_python_packaging_demo --version
0.0.6
```

What about tests?
-----------------

There's nothing in the demo to prevent broken code from being uploaded to PyPI.
The demo app doesn't even have any tests.
This shouldn't be difficult to fix: just have the publish workflow run your tests before uploading to PyPI.

Known issues
------------

### setuptools_scm causes all git-tracked files to be included in the sdist

If you download one of the source dist packages from PyPI and open the
`.tar.gz` file you'll see that it has a lot of unnecessary files in it:
the `.github` directory (containing the GitHub Actions workflows),
the `.gitignore` file, etc. Those files don't need to be and shouldn't be in there.

This is a [known issue with setuptools_scm](https://github.com/pypa/setuptools_scm/issues/190):
using setuptools_scm causes all git-tracked files to be included in the sdist
(thankfully the `.git` directory itself isn't included).
There's nothing we can do about this (a `MANIFEST.in` file won't work) and it doesn't really matter:
the files don't cause any problems being there.

### setuptools_scm misbehaves if a commit has multiple tags

If you have more than one version number tag attached to the same commit
[setuptools_scm won't always pick the right tag](https://github.com/pypa/setuptools_scm/issues/521)
(the newest one) to be the current version number. This can cause problems. For
example if one of the version numbers has already been published to PyPI and
the other hasn't the publish workflow can end up trying to publish the
already-published version number and getting an error from PyPI.

This is an edge case (why would you try to release the same commit twice with
two different version numbers?) so it's probably not important.

