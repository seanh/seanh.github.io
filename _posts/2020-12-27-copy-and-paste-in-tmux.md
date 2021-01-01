---
tags: [tmux]
---

Copy and Paste in tmux
======================

<div class="lead" markdown="1">
How to make copy and paste in tmux work the same as in other apps, using the system clipboard and primary selection.
</div>

<div class="note" markdown="1">
### TLDR

Install [Tmux Plugin Manager](https://github.com/tmux-plugins/tpm)
and [tmux-yank](https://github.com/tmux-plugins/tmux-yank), then paste
the config below into your `~/.tmux.conf` file and reload it (`tmux source ~/.tmux.conf`)
to get copy and paste to work like it would in a normal app:

* tmux mouse mode enabled
* Selecting text with the mouse copies it into the primary selection
* <kbd><kbd>Ctrl</kbd> + <kbd>c</kbd></kbd> or <kbd>y</kbd> copies a selection into the system clipboard
* It no longer clears your selection as soon as you copy it or raise the mouse button
* Double-clicking on a word selects it
* Triple-clicking on a line selects the whole line
* <kbd>Middle Mouse Button</kbd> pastes from the primary selection
* Your terminal emulator's keyboard shortcut pastes from the system clipboard
  (probably <kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>v</kbd></kbd>)

```
# ~/.tmux.conf
set -g mouse on

# These bindings are for X Windows only. If you're using a different
# window system you have to replace the `xsel` commands with something
# else. See https://github.com/tmux/tmux/wiki/Clipboard#available-tools
bind -T copy-mode    DoubleClick1Pane select-pane \; send -X select-word \; send -X copy-pipe-no-clear "xsel -i"
bind -T copy-mode-vi DoubleClick1Pane select-pane \; send -X select-word \; send -X copy-pipe-no-clear "xsel -i"
bind -n DoubleClick1Pane select-pane \; copy-mode -M \; send -X select-word \; send -X copy-pipe-no-clear "xsel -i"
bind -T copy-mode    TripleClick1Pane select-pane \; send -X select-line \; send -X copy-pipe-no-clear "xsel -i"
bind -T copy-mode-vi TripleClick1Pane select-pane \; send -X select-line \; send -X copy-pipe-no-clear "xsel -i"
bind -n TripleClick1Pane select-pane \; copy-mode -M \; send -X select-line \; send -X copy-pipe-no-clear "xsel -i"
bind -n MouseDown2Pane run "tmux set-buffer -b primary_selection \"$(xsel -o)\"; tmux paste-buffer -b primary_selection; tmux delete-buffer -b primary_selection"

set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-yank'
set -g @yank_action 'copy-pipe-no-clear'
bind -T copy-mode    C-c send -X copy-pipe-no-clear "xsel -i --clipboard"
bind -T copy-mode-vi C-c send -X copy-pipe-no-clear "xsel -i --clipboard"

# Initialize TMUX plugin manager (keep this line at the very bottom of tmux.conf)
run '~/.tmux/plugins/tpm/tpm'
```
</div>

By default if you're running tmux in GNOME Terminal or st you can copy and
paste with the primary selection and system clipboard like you would in any
normal app:

* Click and drag with the <kbd>Left Mouse Button</kbd> to select some text and copy it into the primary selection
* Double-click the <kbd>Left Mouse Button</kbd> on a word to select the word and copy it into the primary selection
* Triple-click the <kbd>Left Mouse Button</kbd> on a line to select the whole line and copy it into the primary selection
* Click the <kbd>Middle Mouse Button</kbd> to paste from the primary selection
* <kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>c</kbd></kbd> to copy the selection into the clipboard
* <kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>v</kbd></kbd> to paste from the clipboard

None of this has anything to do with tmux. It's because tmux doesn't handle
mouse events by default, so all the clicking, dragging, copying and pasting is
being handled by the terminal emulator that tmux is running in.
<kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>c</kbd></kbd> and
<kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>v</kbd></kbd> are the keyboard
shortcuts that both GNOME Terminal and st use for copying to and pasting from
the system clipboard.

There are a few problems with this:

1. The terminal emulator isn't aware of tmux's status bar, panes, etc.
   So when you have a window split into two panes, trying to copy text from one
   of the panes will also copy the pane border and the contents of the other
   pane. There are other problems too, like being unable to copy a block of
   text that takes up more than one screenful in the scrollback history.

   <img src="/assets/images/tmux-copy-fail.png" style="box-shadow: none;">

2. Copying text using keyboard commands and tmux's copy mode doesn't copy the
   text into the system clipboard. Selecting text with tmux's keyboard commands
   and then using your terminal emulator's copy command
   (<kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>c</kbd></kbd>) doesn't work either.

3. You're missing out on the features of tmux's mouse mode such as being able
   to scroll with the mousewheel, click on panes and windows to select them,
   and click and drag on pane borders to resize panes.

We can fix this by enabling tmux's mouse mode:

```
$ tmux set -g mouse on
```

Now selecting text by clicking-and-dragging with the mouse is aware of tmux panes, scrollback, and everything else:

<img src="/assets/images/tmux-copy-fix.png" style="box-shadow: none;">

And we've gained the rest of tmux's mouse mode features, too:

* You can use the mouse wheel to scroll through the history
* You can click on a pane to select that pane
* You can click on a window in the status bar to select that window
* You can click and drag on pane borders to resize panes

Unfortunately now that mouse mode's enabled the system clipboard and primary
selection no longer work at all:

* Selecting text by clicking and dragging doesn't copy it into the primary
  selection, and your selection disappears as soon as you release the mouse
  button
* Double-clicking and triple-clicking to select words and lines no longer works
  (it does select the word or line _if_ you manually enter tmux's copy mode first,
  but still doesn't copy it into the system clipboard)
* Terminal emulator keyboard shortcuts like
  <kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>c</kbd></kbd> don't copy the
  selection into the system clipboard. The terminal emulator is no longer aware
  of the selection, because tmux is now handling it.

You **can** still paste from the system clipboard with
<kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>v</kbd></kbd> though, that never
breaks.

Fortunately we can fix all of this with a little bit of tmux config work...

## tmux-yank

The first thing to do is install [Tmux Plugin Manager](https://github.com/tmux-plugins/tpm)
and then use it to install the [tmux-yank](https://github.com/tmux-plugins/tmux-yank) plugin.

<div class="note" markdown="1">
You don't _really_ need tmux-yank to get copy and paste working.
You can just add custom key and mouse bindings to your `~/.tmux.conf` so that
it pipes to and from an external program to work with the system clipboard and
primary selection. The tmux wiki has [a page about it](https://github.com/tmux/tmux/wiki/Clipboard).
The problem is that the needed external program varies depending on whether you're using X
Windows (`xsel` or `xclip`), Wayland (`wl-copy`), macOS or WSL (`clip.exe`),
etc. The value of tmux-yank is that it automatically uses the right copy
program for the current system.
</div>

You will need:

* [Git](https://git-scm.com/)

To install Tmux Plugin Manager and tmux-yank:

1. Clone Tmux Plugin Manager:

   ```terminal
   $ git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
   ```

2. Add this to your `~/.tmux.conf` file:

   ```
   set -g mouse on

   set -g @plugin 'tmux-plugins/tpm'
   set -g @plugin 'tmux-plugins/tmux-yank'
   bind -T copy-mode    C-c send -X copy-pipe-no-clear "xsel -i --clipboard"
   bind -T copy-mode-vi C-c send -X copy-pipe-no-clear "xsel -i --clipboard"

   # Initialize TMUX plugin manager (keep this line at the very bottom of tmux.conf)
   run '~/.tmux/plugins/tpm/tpm'
   ```

3. Reload your `~/.tmux.conf` file:

   ```terminal
   $ tmux source ~/.tmux.conf
   ```

4. Use Tmux Plugin Manager to install tmux-yank:

   ```terminal
   $ ~/.tmux/plugins/tpm/bin/install_plugins
   ```

You should now have a couple of things working:

* Selecting text with the mouse will copy it into the primary selection so that
  you can paste it into another app with the <kbd>Middle Mouse Button</kbd>.
  (<kbd>Middle Mouse Button</kbd> to paste won't be working in tmux itself yet,
  we'll get to that below.)

* If you use tmux's copy mode keyboard commands to select some text and then
  click <kbd><kbd>Ctrl</kbd> + <kbd>c</kbd></kbd> or <kbd>y</kbd> it'll copy it
  into the system clipboard.

  <div class="note" markdown="1">
  <kbd>y</kbd> is the key that tmux-yank uses for copying to the clipboard,
  the same as vim's "yank" key (which ironically doesn't use the system
  clipboard by default in vim).

  The `bind`'s in the `~/.tmux.conf` snippet above make <kbd><kbd>Ctrl</kbd> + <kbd>c</kbd></kbd>
  do the same thing as <kbd>y</kbd>, but they only work in X Windows. If you're
  using a different window system you'll have to replace the `xsel` commands
  with something else.
  </div>

## Don't clear the selection on raise

When you click and drag with the <kbd>Left Mouse Button</kbd> to select some
text in tmux's mouse mode, as soon as you release the button it infuriatingly
clears your selection:
{% capture html %}
<video controls>
  <source src="/assets/videos/tmux-clear-selection.mp4" type="video/mp4">
</video>
{% endcapture %}
{% include wide.html content=html %}

It does the same when you select text with the keyboard and hit <kbd>y</kbd> to copy it.
To fix it add this line to your `~/.tmux.conf`:

    set -g @yank_action 'copy-pipe-no-clear'

Then reload your `~/.tmux.conf` file:

```terminal
$ tmux source ~/.tmux.conf
```

Now when you release the mouse button your selection will be copied into the
primary selection but not cleared, like in any other app. After selecting some
text you can:

* Use the arrow keys and other tmux copy mode cursor movement commands to refine a
  selection that you started with the mouse
* Press <kbd><kbd>Ctrl</kbd> + <kbd>c</kbd></kbd> or <kbd>y</kbd> to copy a
  mouse-created selection into the system clipboard

Hit <kbd>q</kbd> to clear the selection and exit copy mode.
To just clear the selection and remain in copy mode hit
<kbd><kbd>Ctrl</kbd> + <kbd>g</kbd></kbd>, or <kbd>Esc</kbd> if you have tmux's
vi-style copy mode bindings enabled.

## Double-click and triple-click

Double-clicking to select a word and triple-clicking to select a line still
don't work unless you're already in tmux's copy mode. And even in copy mode
they don't copy into the primary selection.

Add these lines to your `~/.tmux.conf` to fix it:

```
bind -T copy-mode    DoubleClick1Pane select-pane \; send -X select-word \; send -X copy-pipe-no-clear "xsel -i"
bind -T copy-mode-vi DoubleClick1Pane select-pane \; send -X select-word \; send -X copy-pipe-no-clear "xsel -i"
bind -n DoubleClick1Pane select-pane \; copy-mode -M \; send -X select-word \; send -X copy-pipe-no-clear "xsel -i"
bind -T copy-mode    TripleClick1Pane select-pane \; send -X select-line \; send -X copy-pipe-no-clear "xsel -i"
bind -T copy-mode-vi TripleClick1Pane select-pane \; send -X select-line \; send -X copy-pipe-no-clear "xsel -i"
bind -n TripleClick1Pane select-pane \; copy-mode -M \; send -X select-line \; send -X copy-pipe-no-clear "xsel -i"
```

<div class="warning" markdown="1">
This is for X Windows only. If you're using a different window system you have
to replace the `xsel` commands with something else.
</div>

Then reload your `~/.tmux.conf` file:

```terminal
$ tmux source ~/.tmux.conf
```

Now double-clicking or triple-clicking with the <kbd>Left Mouse Button</kbd>
should enter copy mode if you aren't already in it, select the word or line,
and copy it into the primary selection.

As with clicking-and-dragging you can use the arrow keys and other tmux copy
cursor movement commands to refine the selection and press
<kbd><kbd>Ctrl</kbd> + <kbd>c</kbd></kbd> or <kbd>y</kbd> to copy
it into the system clipboard.

## Middle-click to paste

<kbd>Middle Mouse Button</kbd> still doesn't paste from the primary selection.
To fix it add this to your `~/.tmux.conf`:

```
bind -n MouseDown2Pane run "tmux set-buffer -b primary_selection \"$(xsel -o)\"; tmux paste-buffer -b primary_selection; tmux delete-buffer -b primary_selection"
```

<div class="warning" markdown="1">
This is for X Windows only. If you're using a different window system you have
to replace the `xsel` command with something else.
</div>

Reload your `~/.tmux.conf` file:

```terminal
$ tmux source ~/.tmux.conf
```

Middle-click to paste should now work.

## Pasting from the system clipboard

It would be possible to add a tmux key binding to paste from the system
clipboard using an external program like `xsel` (depending on your window
system) but it's unnecessary: your terminal emulator's paste command will still
work. In GNOME Terminal or st it's just
<kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>v</kbd></kbd>

## Other terminal emulator mouse commands

GNOME Terminal shows a context menu if you click the
<kbd>Right Mouse Button</kbd> on the terminal. If you click on a URL this menu
can open the URL in a browser. I don't think there's any way to get these sorts
of terminal emulator mouse commands to work when you have mouse mode enabled in
tmux: tmux either takes over all mouse events or none of them. You just always
have to do <kbd><kbd>Shift</kbd> + <kbd>Right Mouse Button</kbd></kbd> instead
(holding down <kbd>Shift</kbd> temporarily disables tmux's mouse mode).

## tmux's copy mode

tmux has a "copy mode" for finding, selecting and copying text using the
keyboard. You don't really need copy mode if you've followed the instructions
above to fix mouse-based copy and paste but it's very powerful so it might be
worth learning.

<div class="note" markdown="1">
Note: tmux's copy mode uses emacs-style keybindings by default unless your
`EDITOR` or `VISUAL` envvar contains the string `"vi"`, then it uses vi-style
bindings.  You can force it to use vi-style bindings by adding this line to
your `~/.tmux.conf`:

    set -g mode-keys vi

I'm using the vi-style bindings in this guide.
</div>

In tmux <kbd><kbd>Ctrl</kbd> + <kbd>b</kbd> <kbd>[</kbd></kbd> enters **copy
mode**, where you can move the cursor around and select text. If you have
tmux's mouse mode enabled (`set -g mouse on`) then scrolling with the
scrollwheel also enters copy mode. <kbd><kbd>Ctrl</kbd> + <kbd>b</kbd>
<kbd>Page Up</kbd></kbd> enters copy mode and scrolls up by one page.

In copy mode:

* <kbd>Space</kbd> begins selecting some text
* <kbd>Enter</kbd> copies the selected text and exits copy mode, but it copies
  the text into a tmux paste buffer not the system clipboard
  (tmux-yank adds the <kbd>y</kbd> command to copy into the system clipboard)

Back in default mode:

* <kbd><kbd>Ctrl</kbd> + <kbd>b</kbd> <kbd>]</kbd></kbd> pastes from tmux's
  most recently created paste buffer (i.e. pastes the most recently copied
  text)
* <kbd><kbd>Ctrl</kbd> + <kbd>b</kbd> <kbd>=</kbd></kbd> (or `tmux
  choose-buffer` on the command line) shows you all the paste buffers and lets
  you choose one to paste from

<div class="hint" markdown="1">

#### Copy mode keyboard shortcuts

Some other useful copy-mode keyboard shortcuts (there are more, see [`man tmux`](http://manpages.ubuntu.com/manpages/focal/man1/tmux.1.html)):

* <kbd>Esc</kbd> clears the selection and stays in copy mode

* <kbd>q</kbd> clears the selection and exits copy mode

* <kbd>h</kbd>, <kbd>j</kbd>, <kbd>k</kbd> and <kbd>l</kbd> move left, down, up and right

* <kbd>w</kbd>, <kbd>W</kbd>, <kbd>b</kbd>, <kbd>B</kbd>, <kbd>e</kbd> and <kbd>E</kbd> move forward and backward a word at a time, like in vim

* <kbd>$</kbd> moves to the end of the line and <kbd>0</kbd> goes to the start of the line. <kbd>^</kbd> goes to the first non-blank character on the line

* <kbd>g</kbd> goes to the beginning of the scrollback history (the top) and <kbd>G</kbd> goes to the end (the bottom)

* <kbd>v</kbd> enables block selection, like <kbd><kbd>Ctrl</kbd> + <kbd>v</kbd></kbd> (visual block mode) in vim.

* <kbd>V</kbd> selects the entire current line, same as in vim (in vim <kbd>V</kbd> enters visual line mode). Once you've selected a line you can move the cursor
  up and down to select more lines

* <kbd>/</kbd> begins a forward (downward) search and <kbd>?</kbd> begins a backward (upwards) search. <kbd>n</kbd> and <kbd>N</kbd> go to the next and previous
  search match.

  Add these lines to your `~/.tmux.conf` to make <kbd>/</kbd> and <kbd>?</kbd> do _incremental_ search instead (highlights all search matches as you type, similar
  to setting `incsearch` in vim):

  ```
  bind -T copy-mode-vi / command-prompt -i -p "(search down)" "send -X search-forward-incremental \"%%%\""
  bind -T copy-mode-vi ? command-prompt -i -p "(search up)" "send -X search-backward-incremental \"%%%\""
  ```

* <kbd>f</kbd> jumps forward to the next occurrence of a character on the same line. For example <kbd><kbd>f</kbd> <kbd>s</kbd></kbd> jumps to the next `s`.
  <kbd>F</kbd> jumps backward. <kbd>;</kbd> repeats the jump (goes to the _next_ `s`), <kbd>,</kbd> goes to the _previous_ match. <kbd>t</kbd> and <kbd>T</kbd> are
  the same as <kbd>f</kbd> and <kbd>F</kbd> but they jump the cursor to the character _before_ the matching character, instead of on top of the match.

* When the cursor is on an opening bracket <kbd>%</kbd> moves to the closing bracket

* <kbd>D</kbd> copies from the cursor to end of line and exits copy mode

* To make <kbd>Y</kbd> copy the entire current line (like in vim) and exit copy mode, add this to your `~/.tmux.conf`:

  ```
  # Make Y copy the entire current line.
  bind -T copy-mode-vi Y send-keys -X copy-line
  ```

  This works with a vi-like prefix, so <kbd><kbd>3</kbd> <kbd>Y</kbd></kbd> will copy three lines (the current line and the two below it).
</div>

## tmux's paste buffers

Whenever you select some text with the mouse or copy some text with the
keyboard (with either <kbd>Enter</kbd> or tmux-yank's <kbd>y</kbd>) tmux
creates a new **paste buffer** and saves the text in it. When you then select
or copy some other text tmux creates _another_ new paste buffer. Previously
selected texts are still available in their historical paste buffers and can be
viewed and pasted using
<kbd><kbd><kbd>Ctrl</kbd> + <kbd>b</kbd></kbd> <kbd>=</kbd></kbd> (`tmux choose-buffer`).

There are commands for working with paste buffers so you can script them:

* `tmux show-buffer` or `tmux showb` prints the contents of the most recent buffer
* `tmux list-buffers` or `tmux lsb` prints a list of the buffers and their contents
* `tmux set-buffer <DATA>` or `tmux setb <DATA>` creates a new buffer and loads `<DATA>` into it
* `tmux load-buffer <PATH>` or `tmux loadb <PATH>` creates a new buffer and loads the contents of a file into it
* `tmux paste-buffer` or `tmux pasteb` pastes the most recent buffer into the current pane (you can also pass `-t <target-pane>` to paste into another pane)
* `tmux save-buffer <PATH>` or `tmux saveb <PATH>` writes the most recent buffer to a file, pass `-a` to append to the file instead of overwriting it
* `tmux delete-buffer` ot `tmux deleteb` deletes the most recently added buffer

These all take an optional `-b <buffer-name>` argument to work with a named
buffer instead of the most recent one.
For example to load some data into `my_buffer`, paste it, and then delete the
buffer:

```terminal
$ tmux setb -b my_buffer <DATA>
$ tmux setb -b my_buffer -a <MORE_DATA>  # Append more data to the same buffer
$ tmux pasteb -b my_buffer
$ tmux deleteb -b my_buffer
```

My <kbd>Middle Mouse Button</kbd> key binding above uses these commands to copy
the text from the window system's primary selection into a named buffer, paste
from that buffer, then delete the buffer so it doesn't pollute your buffer
list.

As well as using them as normal shell commands these can also be used on the
tmux command line, for example:
<kbd><kbd><kbd>Ctrl</kbd> + <kbd>b</kbd></kbd> <kbd>:</kbd> <kbd>showb</kbd> <kbd>Enter</kbd></kbd>
