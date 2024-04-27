Title: How to Use Pelican with GitHub Actions
Status: draft

You will need
-------------

1. Git
2. GitHub CLI
3. Git authentication configured
4. pipx

Install Pelican locally
-----------------------

I recommend installing Pelican using [pipx](https://pypa.github.io/pipx/):

1. Install pipx:

   On Ubuntu or Debian run:

   ```console
   sudo apt install pipx
   ```

   On macOS [install Homebrew](https://brew.sh/) then run:

   ```console
   brew install pipx
   ```

2. Use pipx to install Pelican:

   ```console
   pipx install 'pelican[markdown]'
   ```

Create your Pelican site locally
--------------------------------

```console
mkdir ~/my-pelican-site
cd ~/my-pelican-site
pelican-quickstart
```

Run your Pelican site locally
-----------------------------

```console
pelican --autoreload --listen
```

Open <http://localhost:8000/> in a browser to view your site locally.

Create a GitHub Actions workflow to deploy your site to GitHub Pages
--------------------------------------------------------------------

Create a `.github/workflows` directory:

```console
mkdir -p .github/workflows
```

Now create a `.github/workflows/pelican.yml` file with these contents, this
will be the GitHub Actions workflow for building your site with Pelican and
deploying it to GitHub Pages:

```yaml
# .github/workflows/pelican.yml
name: Build & Deploy
on:
  push:
    branches: ["main"]
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: "pages"
  cancel-in-progress: false
jobs:
  Build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3.5.3
      - name: Set up Python
        uses: actions/setup-python@v4.7.0
        with:
          python-version: "3.11"
      - name: Configure GitHub Pages
        id: pages
        uses: actions/configure-pages@v3.0.6
        with:
          enablement: true
      - name: Install Pelican
        run: pip install "pelican[markdown]"
      - name: Build site
        run: pelican --settings publishconf.py --extra-settings SITEURL='"${{ steps.pages.outputs.base_url }}"'
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2.0.0
        with:
          path: "output/"
  Deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2.0.4
```

Create a `.gitignore` file
--------------------------

Create a `.gitignore` file with these contents:

    # .gitignore
    __pycache__/
    output/

Create a git repo and commit everything
---------------------------------------

```console
git init
git add .
git commit -m 'Initial commit'
```

Create a GitHub repo and push to it
-----------------------------------

Use GitHub CLI to create a new GitHub repo and push everything to it:

```console
gh repo create --source . --public --push
```



1. Install pyenv
2. Install Python
3. Create `requirements.in`
4. Create a venv
5. Install pip-tools
6. Compile `requirements.txt`
7. Install `requirements.txt`
8. Create Pelican starter files
9. Build site locally
10. Actions workflow
