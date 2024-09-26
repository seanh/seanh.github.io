Title: Comment and Uncomment Lines with <code>commentary.vim</code>
Tags: vim

<p class="lead">Using the commentary.vim plugin to learn about Vim's operators, motions and test objects.</p>

[commentary.vim](https://github.com/tpope/vim-commentary) provides several ways to comment or uncomment lines.
First install the plugin
(see [my post about installing Vim plugins]({filename}2024-09-10-vim-packages.md)):

```console
$ git clone https://tpope.io/vim/commentary.git ~/.vim/pack/plugins/start/vim-commentary
$ vim -u NONE -c "helptags commentary/doc" -c q
```

...and now:

1. Press <kbd>gcc</kbd> in normal mode to comment or uncomment the current line.

    <figure>
        <video controls="" muted="" playsinline="" src="{static}/videos/gcc.mp4"></video>
        <figcaption><kbd>gcc</kbd> toggles commenting of the current line.</figcaption>
    </figure>

    You can precede <kbd>gcc</kbd> with a count,
    for example <kbd>3gcc</kbd> comments or uncomments three lines
    (the current line and the two below it).

2. Select some lines then press <kbd>gc</kbd> in visual mode to comment or uncomment the selected line(s):

    <figure>
        <video controls="" muted="" playsinline="" src="{static}/videos/Vgc.mp4"></video>
        <figcaption><kbd>gc</kbd> toggles commenting of the selected text.</figcaption>
    </figure>

3. <kbd>gc{motion}</kbd> in normal mode comments or uncomments all lines that the given `{motion}` moves over.

    This works with any of Vim's built-in motions or text objects and ones provided by plugins.
    See [`:help motion.txt`](https://vimhelp.org/motion.txt.html) for all the built-in motions and text objects you can use.
    Here's some examples:

    * <kbd>j</kbd> moves to the line below and <kbd>k</kbd> moves to the line above,
      so:

        * <kbd>gcj</kbd> comments or uncomments the current line and the line below it.
        * <kbd>gck</kbd> comments or uncomments the current line and the one above it.

    * Motions can take counts: <kbd>3j</kbd> moves down three lines and <kbd>3k</kbd> moves up three lines, so:

        * <kbd>gc3j</kbd> comments or uncomments the current line and three lines below it.
        * <kbd>gc3k</kbd> comments or uncomments the current line and the three above it.
        * You can also put the count at the start of the command: <kbd>3gcj</kbd> and <kbd>3gck</kbd> do the same thing.

    * <kbd>gg</kbd> moves to the top of the file and <kbd>G</kbd> moves to the bottom of the file, so:

        * <kbd>gcgg</kbd> comments or uncomments the current line and every line above it to the top of the file.
        * <kbd>gcG</kbd> comments or uncomments the current line and every line below it.

    * <kbd>ap</kbd> is a text object for the current paragraph, so:

        * <kbd>gcap</kbd> comments or uncomments the current paragraph.
        * Text objects work with counts too:
          either <kbd>3gcap</kbd> or <kbd>gc3ap</kbd> comments or uncomments three paragraphs
          (the current paragraph and the two below it).

    * [vim-indent-object]({filename}2020-08-08-vim-indent-object.md) is a plugin that
      adds <kbd>ii</kbd> as a text object for the current indented block
      and <kbd>ai</kbd> for the current indented block _and the first line above the indentation_, so:

        * <kbd>gcii</kbd> comments or uncomments the current indented block.
        * <kbd>gcai</kbd> comments or uncomments the current indented block and the first line above it.

    * [vim-textobj-entire](https://github.com/kana/vim-textobj-entire)
      adds <kbd>ae</kbd> as a text object for the entire file
      so <kbd>gcae</kbd> comments or uncomments the entire file.

    * Commentary.vim itself also adds <kbd>gc</kbd> as a text object for the current comment
      so <kbd>gcgc</kbd> uncomments all lines of the current comment.

        Like any text object <kbd>gc</kbd> can be used as the object of any command that expects one.
        For example <kbd>dgc</kbd> deletes the current comment,
        <kbd>ygc</kbd> copies (yanks) the current comment,
        <kbd>&gt;gc</kbd> or <kbd>&lt;gc</kbd> indents or dedents the current comment,
        etc.

4. Type `:[range]Commentary` in command line mode to comment or uncomment a range of lines.

    For example `:'<,'>Commentary` will comment or uncomment the currently selected lines (the same as pressing <kbd>gc</kbd> in visual mode),
    or `:3,5Commentary` will comment or uncomment lines 3-5
    (see [`:help cmdline-ranges`](https://vimhelp.org/cmdline.txt.html#cmdline-ranges)).

5. Finally, `Commentary` can be used with Vim's `:global` command (see [`:help :global`](https://vimhelp.org/repeat.txt.html#%3Aglobal)) to comment or uncomment all lines that match a pattern,
   for example `:g/TODO/Commentary` comments or uncomments all lines containing `TODO`.

Vim's dot command with <kbd>gc</kbd>
------------------------------------

Because commentary.vim commands either comment a line (if it's not already commented)
or uncomment a line (if it's already commented) you can use <kbd>.</kbd> ([the dot command](https://vimhelp.org/repeat.txt.html#.)) to toggle
a previous comment or uncomment action.
For example after using <kbd>gcap</kbd> to comment out a paragraph <kbd>.</kbd> will
now uncomment the same paragraph.
If you move the cursor to a different paragraph then <kbd>.</kbd> will comment or uncomment that paragraph.

Vim operators, motions and text objects
---------------------------------------

To understand a command like <kbd>gcgc</kbd> (uncomment a comment) you first have to understand Vim's
concepts of **operators**, **motions** and **text objects**.

Many of Vim's normal mode keyboard commands have this form:

<pre class="lead" style="text-align:center;">{operator} {motion}</pre>

For example <kbd>dw</kbd> deletes from the cursor to the start of the next word.
<kbd>d</kbd> is the delete operator and <kbd>w</kbd> is a motion that jumps to the start of the next word:

<figure>
    <video controls="" muted="" playsinline="" src="{static}/videos/dw.mp4"></video>
    <figcaption><kbd>dw</kbd> deletes from the cursor to the start of the next word.</figcaption>
</figure>

**Motions** are keyboard commands that move the cursor around. For example:
<kbd>h</kbd> and <kbd>l</kbd> to move one character to the left and right,
<kbd>0</kbd> or <kbd>Home</kbd> to jump to the start of the line,
<kbd>^</kbd> to jump to the first non-blank character on the line,
<kbd>$</kbd> or <kbd>End</kbd> to jump to the end of the line,
<kbd>g_</kbd> to jump to the last non-blank character on the line,
<kbd>{number}G</kbd> to jump to line `{number}` (for example <kbd>42G</kbd> to jump to line 42),
<kbd>j</kbd> and <kbd>k</kbd> to move down to the next line or up to the previous line,
<kbd>w</kbd> to jump to the start of the next word,
<kbd>e</kbd> to jump to the end of the next word,
<kbd>b</kbd> to jump to the start of the _previous_ word,
<kbd>ge</kbd> to jump to the _end_ of the previous word.
<kbd>)</kbd> and <kbd>(</kbd> jump to the next and previous sentence,
whereas <kbd>}</kbd> and <kbd>{</kbd> jump to the next and previous paragraph.
There are many more motions, see [`:help motion.txt`](https://vimhelp.org/motion.txt.html) for them all.

**Operators** are commands that operate on text. For example:
<kbd>d</kbd> to delete,
<kbd>y</kbd> to "yank" (copy),
<kbd>gu</kbd> to change to lowercase,
<kbd>gU</kbd> to change to uppercase,
<kbd>~</kbd> to toggle case,
<kbd>&gt;</kbd> to indent and <kbd>&lt;</kbd> to dedent.

To operate on some text you type an operator followed by a motion:

<pre class="lead" style="text-align:center;">{operator} {motion}</pre>

For example <kbd>gU$</kbd> will uppercase everything from the cursor position to the end of the line.
<kbd>gU</kbd> is the uppercase operator and <kbd>$</kbd> is a motion to the end of the line:

<figure>
    <video controls="" muted="" playsinline="" src="{static}/videos/gU$.mp4"></video>
    <figcaption><kbd>gU$</kbd> uppercases everything from the cursor to the end of the line.</figcaption>
</figure>

When you type an operator Vim goes into "operator pending mode":
it displays the operator that was typed in the bottom-right and waits for you
to tell it what text to operate on by typing a motion:

<figure>
    <img src="{static}/images/operator-pending.png" alt="Vim in operator-pending mode">
    <figcaption>
      Vim in operator-pending mode.
      The <code>d</code> in the bottom-right indicates that a <kbd>d</kbd> (delete) command has been entered.
      Vim is waiting for you to tell it what text you want it to delete by entering a motion.
    </figcaption>
</figure>


<aside class="note" markdown="1">**Aside:** there's a shortcut for operating on the current line: you just hit the operator key twice.
For example <kbd>yy</kbd> will yank the entire current line,
or <kbd>cc</kbd> will delete the current line and enter insert mode so you can type a replacement (<kbd>c</kbd> is the "change" operator).

For multi-character operator commands you just repeat the last key, for example <kbd>gUU</kbd> will uppercase the whole line.
This is why <kbd>gcc</kbd> toggles commenting of the current line.
</aside>

**Text objects** are commands that you can use in visual mode to select ranges of text.
For example <kbd>aw</kbd> stands for "around word", typing <kbd>aw</kbd> in visual mode expands the selection in both directions at once to contain the word under the cursor including any trailing whitespace:

<figure>
    <video controls="" muted="" playsinline="" src="{static}/videos/aw.mp4"></video>
    <figcaption><kbd>aw</kbd> expands the selection in both directions to select the word under the cursor.</figcaption>
</figure>

<kbd>iw</kbd> ("inner word") selects the word _without_ trailing whitespace,
<kbd>as</kbd> and <kbd>is</kbd> select sentences,
<kbd>ap</kbd> and <kbd>ip</kbd> select paragraphs.

There are several text objects for selecting text within pairs of surrounding characters.
<kbd>i[</kbd>, <kbd>a[</kbd>,
<kbd>i(</kbd>, <kbd>a(</kbd>,
<kbd>i&lt;</kbd>, <kbd>a&lt;</kbd>,
<kbd>i{</kbd>, <kbd>a{</kbd>,
<kbd>i'</kbd>, <kbd>a'</kbd>,
<kbd>i"</kbd>, <kbd>a"</kbd>,
<kbd>i\`</kbd> and <kbd>a\`</kbd>
select text within or around pairs of `[...]`'s, `(...)`'s, `<...>`'s, `{...}`'s, `'...'`'s, `"..."`'s or <code>\`...\`</code>'s:

<figure markdown="1">
<video controls="" muted="" playsinline="" src="{static}/videos/brackets.mp4"></video>
<figcaption markdown="1"><kbd>i"</kbd> selects everything inside the `"..."`'s. <kbd>i(</kbd> selects everything inside the `(...)`'s.</figcaption>
</figure>

The <kbd>i</kbd> versions select only the text inside the brackets whereas the <kbd>a</kbd> versions select the brackets themselves as well):

<figure markdown="1">
<video controls="" muted="" playsinline="" src="{static}/videos/around-brackets.mp4"></video>
<figcaption markdown="1"><kbd>a"</kbd> and <kbd>a(</kbd> select _around_ the `"..."`'s and `(...)`'s.</figcaption>
</figure>

You can type either the opening or the closing bracket,
for example <kbd>i]</kbd> is the same as <kbd>i[</kbd>,
<kbd>a)</kbd> is the same as <kbd>a(</kbd>, etc.

There's also <kbd>it</kbd> and <kbd>at</kbd> which select text within or around pairs of HTML opening and closing tags like `<div>...</div>`:

<figure markdown="1">
<video controls="" muted="" playsinline="" src="{static}/videos/vat.mp4"></video>
<figcaption markdown="1"><kbd>it</kbd> and <kbd>at</kbd> select within and around HTML tags.</figcaption>
</figure>

Text objects can be used in place of the motions in operator commands:

<pre class="lead" style="text-align:center;">{operator} {text object}</pre>

For example <kbd>di[</kbd> will delete everything inside the pair of `[...]`'s that the cursor is currently within:

<figure markdown="1">
<video controls="" muted="" playsinline="" src="{static}/videos/di.mp4"></video>
<figcaption markdown="1"><kbd>di[</kbd> deletes everything inside the `[...]`'s.</figcaption>
</figure>

Or <kbd>&gt;ap</kbd> will indent the current paragraph:

<figure>
    <video controls="" muted="" playsinline="" src="{static}/videos/&gt;ap.mp4"></video>
    <figcaption><kbd>&gt;ap</kbd> indents the current paragraph.</figcaption>
</figure>

And that's what <kbd>gcgc</kbd> is: it's an `{operator} {text object}` command:
commentary.vim provides both a <kbd>gc</kbd> operator for commenting or uncommenting
_and_ a <kbd>gc</kbd> text object for the current comment.
In the command <kbd>gcgc</kbd> the first <kbd>gc</kbd> is the "toggle comment" operator
and the second <kbd>gc</kbd> is the "current comment" text object.
So <kbd>gcgc</kbd> uncomments the entire current comment:

<figure>
    <video controls="" muted="" playsinline="" src="{static}/videos/gcgc.mp4"></video>
    <figcaption><kbd>gcgc</kbd> uncomments a comment.</figcaption>
</figure>
