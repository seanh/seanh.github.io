Title: How to Comment and Uncomment Lines in Vim
Tags: vim

You need the [commentary.vim](https://github.com/tpope/vim-commentary) plugin.
Then:

<kbd>gcap</kbd>
: Toggle commenting of the paragraph under the cursor ("comment a paragraph").
  Takes a count, e.g. <kbd>3gcap</kbd> toggles commenting of three paragraphs.
  
<kbd>gcc</kbd>
: Toggle commenting of the current line.
  This also takes a count, e.g. <kbd>3gcc</kbd> toggles commenting of three lines.

<kbd>gcG</kbd>
: toggle commenting of the current line and every line below it, to the bottom
  of the file

Like with other operators you can also highlight some lines in visual mode and
do <kbd>gc</kbd> to toggle commenting of the highlighted lines.

Finally, you can use <kbd>gc</kbd> as a motion for another operator rather than
as an operator itself:

<kbd>dgc</kbd>, <kbd>cgc</kbd>, <kbd>ygc</kbd>, <kbd><gc</kbd>, <kbd>>gc</kbd>,  
: delete, change, yank, dedent, or indent the current comment

This means you can use <kbd>gc</kbd> as the motion for the <kbd>gc</kbd> operator:
<kbd>gcgc</kbd> uncomments the entire comment that's currently under the cursor.

The <kbd>gc</kbd> part of these commands is commentary.vim's comment
"operator". The part after <kbd>gc</kbd> in each command is the motion. The
same motions also work with standard Vim operators like <kbd>d</kbd> (delete),
<kbd>c</kbd> (change), <kbd>y</kbd> (yank, i.e. copy text into a register or
into the clipboard), <kbd><</kbd> (dedent), <kbd>></kbd> (indent),
<kbd>=</kbd> (autoindent), etc.

When you type an operator Vim goes into "operator pending mode": it displays
the operator you entered (<samp>d</samp>, <samp>c</samp>, <samp>y</samp>, etc)
in the bottom-right and waits for you to enter the motion.

Some standard operator commands (see <kbd>:h operator</kbd> for the full list
of operators):

<kbd>dl</kbd>, <kbd>cl</kbd>, <kbd>yl</kbd>
: delete, change or yank the **letter** under the cursor ("delete a letter")
  (you can also use <kbd>x</kbd> to delete the letter under the cursor)

<kbd>dd</kbd>, <kbd>cc</kbd>, <kbd>yy</kbd>, <kbd><<</kbd>, <kbd>>></kbd>, <kbd>==</kbd>
: delete, change, yank, dedent, indent, or format the **line** under the cursor

<kbd>daw</kbd>, <kbd>caw</kbd>, <kbd>yaw</kbd>
: delete, change or yank the **word** under the cursor ("delete a word")

<kbd>dap</kbd>, <kbd>cap</kbd>, <kbd>yap</kbd> <kbd><ap</kbd>, <kbd>>ap</kbd>, <kbd>=ap</kbd>
: delete, change, yank, dedent, indent or format the **paragraph** under the
  cursor ("delete a paragraph")

These can all take counts the same as <kbd>gc</kbd> can, e.g. <kbd>2x</kbd> to
delete two letters, <kbd>3>ap</kbd> to indent three paragraphs.

The comment/uncomment operator <kbd>gc</kbd> is two keystrokes. Some of the
builtin operators are also two keystrokes, for example: <kbd>g~</kbd> (toggle
case), <kbd>gu</kbd> (lowercase) and <kbd>gU</kbd> (uppercase). To invoke an
operator like <kbd>gc</kbd> on the current line you don't have to type
<kbd>gcgc</kbd>, you can just type <kbd>gcc</kbd>:

<kbd>gcc</kbd>, <kbd>g~~</kbd>, <kbd>guu</kbd>, <kbd>gUU</kbd>
: toggle commenting, toggle case, lowercase, or uppercase the current line

Plugins can also add new motions as well as new operators
For example [vim-textobj-entire](https://github.com/kana/vim-textobj-entire)
adds the <kbd>ae</kbd> motion for the entire file:

<kbd>gcae</kbd>, <kbd>yae</kbd>, <kbd>dae</kbd>, etc
: toggle commenting of, yank, or delete the entire file
