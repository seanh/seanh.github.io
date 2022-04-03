Running Locally
---------------

**See also:**
GitHub's instructions for [running a GitHub Pages site locally](https://help.github.com/en/articles/setting-up-your-github-pages-site-locally-with-jekyll)
using the GitHub Pages gem.

To install and run this site locally:

1. Install Ruby (2.1 or newer), Bundler and git:

   ```terminal
   sudo apt install ruby bundler git
   ```
   
2. Clone this repo and cd into it:

   ```terminal
   git clone https://github.com/seanh/seanh.github.io.git
   cd seanh.github.io
   ```

3. Install Jekyll and other dependencies:

   ```terminal
   bundle install --path vendor/bundle
   ```

4. Finally, serve the site at <http://localhost:4000>:

   ```terminal
   bundle exec jekyll serve
   ```

You should run `bundle update` now and then to keep up to date with the GitHub
Pages gem.
