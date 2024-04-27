# seanh.github.io

## Hacking

To run the site locally you will need:

1. [Git](https://git-scm.com/)
1. [GNU Make](https://www.gnu.org/software/make/)
2. [pyenv](https://github.com/pyenv/pyenv)
3. [tox](https://tox.wiki/)

On Ubuntu run:

```terminal
sudo apt install --yes git make tox
```

Then follow pyenv's [Basic GitHub Checkout](https://github.com/pyenv/pyenv#basic-github-checkout)
instructions and their [install Python build dependencies](https://github.com/pyenv/pyenv/wiki#suggested-build-environment)
instructions. You **don't** need to install pyenv's shell integration.
You don't need to install any versions of Python: the `make` commands below
will install them automatically as needed.

Now to clone the repo and start the dev server on <http://127.0.0.1:8000> run:

```terminal
git clone https://github.com/seanh/seanh.github.io.git
cd seanh.github.io
make dev
```

For more development environment commands run:

```terminal
make help
```
