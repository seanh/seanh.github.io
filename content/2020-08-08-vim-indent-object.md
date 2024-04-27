Title: Operate on an Indented Block of Lines with vim-indent-object
Tags: vim

[vim-indent-object](https://github.com/michaeljsmith/vim-indent-object) is a great Vim plugin that adds an `i` text object for an indented block of text,
very useful in Python!

* <kbd>vii</kbd> selects all lines at the same indentation level as the current line.

    For example just the body of a method and _not_ the method signature or any empty lines below the method.
    Or just the body of a `try` clause and _not_ the `try` line itself.
  
* <kbd>vai</kbd> selects all lines at the same indentation level as the current line,
  _and_ the first unindented line above the indented block (e.g. the method
  signature, if the indented block is a method, or the `try` if the indented
  block is a try clause, etc).
  
    This also selects any blank lines below the indented block, if it's followed
    directly by empty lines.

* <kbd>vaI</kbd> selects an indentation level and both the unindented line above _and_ the unindented line below it.

    For a method this will select the method's signature (unindented line above) _and_ the signature of the next method
    below (unindented line below) (as well as any empty lines between the two methods).
  
    For a `try` clause it'll select both the `try` above and the first `except` below (but not the body of the `except` clause).

* In visual mode you can keep repeating one of the above mappings to keep extending the selection to more and more text at higher and higher indentation levels.
For example:

    <kbd>vii</kbd> (goes into visual mode and selects the body of a try clause),
    <kbd>ii</kbd> (widens the selection to the entire method),
    <kbd>ii</kbd> (widens the selection again, to the entire class body),
    <kbd>ii</kbd> (widens the selection to also include the `class` signature).
    After this, further <kbd>ii</kbd>'s start selecting lines and blocks above the class.

You can combine the `ai`, `ii` and `aI` text objects with other operators besides `v` for visual mode,
e.g. <abbr title="Change an indented block (cuts the block and puts you in insert mode with the cursor where the block started)"><kbd>cii</kbd></abbr>, <abbr title="Delete (cut) an indented block"><kbd>dii</kbd></abbr>, <abbr title="Yank (copy) an indented block"><kbd>yii</kbd></abbr> etc.
For example <kbd>>ii</kbd> or <kbd><ii</kbd> will indent or dedent an indented block.
If you have [vim-commentary](https://github.com/tpope/vim-commentary) installed then
<kbd>gcii</kbd> will comment out an indented block.
