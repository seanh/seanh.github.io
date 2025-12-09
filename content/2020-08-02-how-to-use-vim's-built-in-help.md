Title: How to Use Vim's Built-in Help
Tags: vim

Vim has a comprehensive built-in manual. Unfortunately you need some help to know how to use the help.
This post is a quick reference and tutorial for Vim's <kbd>:help</kbd> files.

<aside markdown="1">
#### See also

* <kbd>:help</kbd> opens Vim's "main help file" ([`help.txt`](https://vimhelp.org/)).
  There's a short tutorial on how to use the help files at the top.
  
* <kbd>:help helphelp</kbd> opens [`helphelp.txt`](https://vimhelp.org/helphelp.txt.html),
  which is the full documentation for the `:help` commands and how to use the help files.

* The Getting Started pages of the docs also have a [Finding Help](https://vimhelp.org/usr_02.txt.html#02.8) section
  (<kbd>:help 02.8</kbd> from within Vim)
  
* You can browse and search all of the help pages online at <https://vimhelp.org/>
  (you _don't_ want to use the copy at <http://vimdoc.sourceforge.net/>, it's hopelessly out of date)

* The [quickref](https://vimhelp.org/quickref.txt.html) (<kbd>:help quickref</kbd>)
  and [index](https://vimhelp.org/index.txt.html) (<kbd>:help index</kbd>) are two
  handy help pages.

    vimhelp.org also has the [VIM FAQ](https://vimhelp.org/vim_faq.txt.html)
    (which I don't think is available from inside Vim).
</aside>

## Opening the help window

<kbd>:help</kbd> (or just <kbd>:h</kbd>) opens the "main help file" (the front page of the help manual, `help.txt`)
in a new window.
<kbd>F1</kbd> does the same thing. The <kbd>Help</kbd> key on your keyboard might also work if it has one.
Use <kbd>:vert help</kbd> to open it in a vertical split instead of a horizontal one,
or <kbd>:tab help</kbd> to open it in a new tab.
I don't think it's possible to open a help file in or in-place-of the current non-help window.
If there's already a help window open <kbd>:help</kbd> will use that window instead of opening a new window
(even if the cursor is currently in a different window).

<kbd>:help {subject}</kbd> (or just <kbd>:h {subject}</kbd>) opens the help tag `{subject}`.
`{subject}` can be lots of different types of thing:

* Topics, e.g.
  [<kbd>:help deleting</kbd>](https://vimhelp.org/change.txt.html#deleting)
  or [<kbd>:help options</kbd>](https://vimhelp.org/options.txt.html)

* Normal-mode commands:
  [<kbd>:help x</kbd>](https://vimhelp.org/change.txt.html#x)
  or [<kbd>:help cc</kbd>](https://vimhelp.org/change.txt.html#cc).
  
    Use `ctrl-` for commands that're prefixed with <kbd>Ctrl</kbd>, e.g.
    [<kbd>:help ctrl-a</kbd>](https://vimhelp.org/change.txt.html#CTRL-A).
  
    Use `_` for multi-key commands, e.g.
    [<kbd>:help ctrl-w_w</kbd>](https://vimhelp.org/windows.txt.html#CTRL-W_W).
  
    `^` also works insead of `ctrl`, e.g.
    <kbd>:help ^p</kbd> is the same as <kbd>:help ctrl-p</kbd>.

    Names of special keys need to be wrapped in angle brackets, e.g.
    [<kbd>:help ctrl-w_&lt;Up&gt;</kbd>](https://vimhelp.org/windows.txt.html#CTRL-W_%3CUp%3E).
    See [<kbd>:help keycodes</kbd>](https://vimhelp.org/intro.txt.html#keycodes) for the names of all the special keys.
  
* Insert-mode commands have an `i_` prefix, e.g.
  [<kbd>:help i_ctrl-r</kbd>](https://vimhelp.org/insert.txt.html#i_CTRL-R)

* Visual-mode commands have a `v_` prefix,
  e.g. [<kbd>:help v_o</kbd>](https://vimhelp.org/visual.txt.html#v_o)

* Ex commands start with `:`, e.g.
  [<kbd>:help :substitute</kbd>](https://vimhelp.org/change.txt.html#:substitute)

* Keyboard commands that you can use when in Vim's command-line mode start with
  `c_`, for example
  [<kbd>:help c_ctrl-r</kbd>](https://vimhelp.org/cmdline.txt.html#c_CTRL-R).
  
    Special characters for use in Ex commands also use `c_`, for example:
    [<kbd>:help c_%</kbd>](https://vimhelp.org/cmdline.txt.html#c_%).

* Vim command-line arguments start with `-`, e.g.
  [<kbd>:help -t</kbd>](https://vimhelp.org/starting.txt.html#-t)

* The names of settings have to be wrapped in single quotes, e.g.
  [<kbd>:help 'number'</kbd>](https://vimhelp.org/options.txt.html#'number')

* Error messages have their own help tags, e.g. [<kbd>:help E37</kbd>](https://vimhelp.org/message.txt.html#E37)

* And more! See [<kbd>:help help-summary</kbd>](https://vimhelp.org/usr_02.txt.html#help-summary) for the complete list of help tag types

## Closing the help window

[<kbd>:q</kbd>](https://vimhelp.org/editing.txt.html#:q) or [<kbd>ZZ</kbd>](https://vimhelp.org/editing.txt.html#ZZ)
will close a help window like any other window if the cursor is in the help window.

[<kbd>:helpclose</kbd>](https://vimhelp.org/helphelp.txt.html#:helpclose) or [<kbd>:helpc</kbd>](https://vimhelp.org/helphelp.txt.html#:helpc)
will close the help window even if the cursor isn't in it.

## Navigating in the help window

Vim's help files are peppered with highlighted "tags" that're links to other locations in the help files.
The tags work as links for jumping back and forth:

* [<kbd><kbd>Ctrl</kbd>-<kbd>]</kbd></kbd>](https://vimhelp.org/tagsrch.txt.html#CTRL-])
  goes to the help tag under the cursor.

    [<kbd><kbd>Ctrl</kbd>-<kbd>]</kbd></kbd>](https://vimhelp.org/tagsrch.txt.html#CTRL-])
    is Vim's general "jump to definition" command, it can be used to jump to the
    definitions of things in code too.

    If you have mouse mode enabled (<kbd>:set <a href="https://vimhelp.org/options.txt.html#'mouse'">mouse</a>=a</kbd>)
    then double-clicking on a tag also follows it.

* [<kbd><kbd>Ctrl</kbd>-<kbd>t</kbd></kbd>](https://vimhelp.org/tagsrch.txt.html#CTRL-T)
or [<kbd><kbd>Ctrl</kbd>-<kbd>o</kbd></kbd>](https://vimhelp.org/motion.txt.html#CTRL-O)
go back to the previous location (repeat to keep going back to prior locations).

    These are Vim's general commands for going back to older positions in the
    [tag stack](https://vimhelp.org/tagsrch.txt.html#tag-stack) (<kbd><kbd>Ctrl</kbd>-<kbd>t</kbd></kbd>)
    or [jump list](https://vimhelp.org/motion.txt.html#jump-motions) (<kbd><kbd>Ctrl</kbd>-<kbd>o</kbd></kbd>).

    <kbd>:tag</kbd> and [<kbd><kbd>Ctrl</kbd>-<kbd>i</kbd></kbd>](https://vimhelp.org/motion.txt.html#CTRL-I) go forward again.

## Searching for help topics
<kbd>:help {subject}</kbd> (or just <kbd>:h {subject}</kbd>) opens the help tag `{subject}`.
`{subject}` can include wildcards like `*`, `?` or `[a-z]`.

If there are multiple help tags matching the given subject then when you press <kbd>Enter</kbd>
Vim opens the "best" match.
See [<kbd>:help {subject}</kbd>](https://vimhelp.org/helphelp.txt.html#{subject}) (literally)
for details of the algorithm Vim uses to decide which match is best.

You can use [<kbd><kbd>Ctrl</kbd> + <kbd>d</kbd></kbd>](https://vimhelp.org/cmdline.txt.html#c_CTRL-D)
or [<kbd>Tab</kbd>](https://vimhelp.org/cmdline.txt.html#c_<Tab>) to search for tag names.
For example type <kbd>:help buffer</kbd> and then instead of <kbd>Enter</kbd> press
<kbd><kbd>Ctrl</kbd> + <kbd>d</kbd></kbd> or <kbd>Tab</kbd> to see a list of all help tags
matching "buffer". This doesn't just list all tags that start with "buffer",
it lists all tags that match "buffer" according to the matching algorithm Vim uses. It includes
all tags that have "buffer" anywhere in the tag name.

## Searching the full text of help files with `:helpgrep`

[<kbd>:helpgrep {pattern}</kbd>](https://vimhelp.org/helphelp.txt.html#:helpgrep)
or [<kbd>:helpg {pattern}</kbd>](https://vimhelp.org/helphelp.txt.html#:helpg)
does a full-text search of all help files for `pattern` and opens the first
match.  It populates the quickfix list with all the matches so you can use
quickfix commands like [<kbd>:cn</kbd>](https://vimhelp.org/quickfix.txt.html#:cn)
to go to the next match, [<kbd>:cp</kbd>](https://vimhelp.org/quickfix.txt.html#:cp)
to go to the previous match, [<kbd>:copen</kbd>](https://vimhelp.org/quickfix.txt.html#:copen)
to open the quickfix window with the list of all matches.
See [<kbd>:help quickfix</kbd>](https://vimhelp.org/quickfix.txt.html) for how to use the quickfix window.

Patterns are case-sensitive, regardless of the `ignorecase` setting, unless you append `\c` to the end of the pattern.

[<kbd>:lhelpgrep</kbd>](https://vimhelp.org/helphelp.txt.html#:lhelpgrep)
(or just [<kbd>:lh</kbd>](https://vimhelp.org/helphelp.txt.html#:lh))
does the same but uses the help window's
[location list](https://vimhelp.org/quickfix.txt.html#location-list),
so it doesn't mess up your quickfix list.

You can also use Google to search the full text of vimhelp.org:
[google.com/search?q=quickfix site:vimhelp.org](https://www.google.com/search?q=quickfix+site%3Avimhelp.org).
Or Duck Duck Go: [duckduckgo.com/?q=quickfix site:vimhelp.org](https://duckduckgo.com/?q=quickfix+site%3Avimhelp.org).
