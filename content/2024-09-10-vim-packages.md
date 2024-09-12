Title: How to Use Vim's Built-in Package Manager
Tags: vim

Many people use third-party Vim plugin managers like vim-plug, Vundle, Pathogen, etc.
I recommend just using the built-in package manager that was introduced in
[Vim 8.0](https://vimhelp.org/version8.txt.html) (released in 2016).
Here's a quick how-to...

See also: [`:help packages`](https://vimhelp.org/repeat.txt.html#packages)

Installing plugins and colorschemes
-----------------------------------

Here's how you'd install the [vim-commentary](https://github.com/tpope/vim-commentary)
plugin as a package:

```terminal
$ git clone https://github.com/tpope/vim-commentary.git ~/.vim/pack/plugins/start/vim-commentary
```

Now when you launch Vim the `commentary.vim` plugin will be loaded,
for example press <kbd>gcc</kbd> to comment or un-comment the current line.

If there's a way to install a plugin in an already-running instance of Vim
without quitting Vim and opening it again, I don't know how.

The plugin doesn't need to come from a git repo:
you can put any directory containing a Vim plugin in `~/.vim/pack/plugins/start/`
and it'll work.

Now let's add the [PaperColor](https://github.com/NLKNguyen/papercolor-theme) colorscheme,
the docs recommend putting colorschemes in `~/.vim/pack/*/opt` rather than
`~/.vim/pack/*/start`:

```terminal
$ git clone https://github.com/NLKNguyen/papercolor-theme.git ~/.vim/pack/colorschemes/opt/papercolor-theme
```

Restart Vim and the PaperColor colorscheme should be available,
run `:colorscheme PaperColor` to use it.

Installing plugins as "optional"
--------------------------------

It's also possible to install plugins as "optional" by putting them in an `opt`
directory instead of the `start` directory. Optional plugins aren't loaded
automatically when you start Vim, but you can manually load them in a given Vim
instance using the `:packadd` command. For example let's install
[copilot.vim](https://github.com/github/copilot.vim) as an optional plugin:

```terminal
$ git clone https://github.com/github/copilot.vim.git ~/.vim/pack/plugins/opt/copilot.vim
```

The plugin won't be loaded when you first launch Vim,
but you can load it when you need it by running `:packadd copilot.vim`
(`copilot.vim` here is the name of the <code>~/.vim/pack/plugins/opt/<b>copilot.vim</b></code>
directory that contains the plugin).

Generating the docs for plugins
-------------------------------

Many plugins come with documentation for viewing with Vim's `:help` command,
for example vim-commentary has a [`doc/commentary.txt`](https://github.com/tpope/vim-commentary/blob/master/doc/commentary.txt)
file.

At first after installing a plugin the plugin's documentation won't be available
in Vim. You have to generate it by running a `:helptags` command like this:

```
:helptags ~/.vim/pack/plugins/start/vim-commentary/doc
```

Now `:help commentary` should open vim-commentary's docs in Vim's built-in help system.
See [my post about Vim's built-in help]({filename}2020-08-02-how-to-use-vim's-built-in-help.md)
for how to use the help system.

You can also just run `:helptags ALL` to build the documentation for all
installed plugins.

Updating plugins
----------------

To update a plugin just replace the contents of its directory with the latest version.
If the plugin came from a git repo just `cd` into the plugin directory and run `git pull`:

```terminal
$ cd ~/.vim/pack/plugins/start/vim-commentary/
$ git pull
```

Packages can contain multiple plugins and colorschemes
------------------------------------------------------

Technically a Vim "package" is actually a collection of one or more plugins and
colorschemes that may depend on each other but I don't think anyone uses it
like that: I think everyone just installs each individual plugin or colorscheme
as a separate package as in the examples above.

The `~/.vim/pack/*` subdirs are arbitrary
------------------------------------------------

The directory names `plugins` and `colorschemes` that I used above are arbitrary:
you can organise your plugins and colorschemes into whatever `~/.vim/pack/*` subdirs you like.

You could put all your colorschemes and plugins together in a single `~/.vim/pack/foo/` directory.
Or you could organise them by author, for example `~/.vim/pack/tpope/` for all of Tim Pope's plugins.
It makes no difference.
I've decided to put all my plugins in a `plugins` directory
and all my colorschemes in a `colorschemes` directory 🤷

You do have to put each plugin and colorscheme in some `~/.vim/pack/*/start`
or `~/.vim/pack/*/opt` subdir,
putting them directly in `~/.vim/pack/start` or `~/.vim/pack/opt` doesn't work.

