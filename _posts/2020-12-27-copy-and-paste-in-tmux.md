Copy & Paste in tmux
====================

<p class="lead" markdown="1">
How to copy and paste in [tmux](https://github.com/tmux/tmux), including with the system's primary selection and clipboard.
</p>

<div class="seealso" markdown="1">
See also: [my tmux config](https://github.com/seanh/tmux)
</div>

## tmux's copy mode

<div class="note" markdown="1">
Note: tmux's copy mode uses emacs-style keybindings by default unless your `EDITOR` or `VISUAL` envvar contains the string `"vi"`, then it uses vi-style bindings.
You can force it to use vi-style bindings by putting `set-window-option -g mode-keys vi` in your `~/.tmux.conf`. I'm using the vi-style bindings in this guide.
</div>

In tmux <kbd><kbd>Ctrl</kbd> + <kbd>b</kbd> <kbd>[</kbd></kbd> enters **copy mode**, where you can move the cursor around and select text. If you have tmux's mouse mode enabled
(`set -g mouse on`) then scrolling with the scrollwheel also enters copy mode. <kbd><kbd>Ctrl</kbd> + <kbd>b</kbd> <kbd>Page Up</kbd></kbd> enters copy mode and scrolls up by
one page.

In copy mode:

* <kbd>Space</kbd> begins selecting some text
* <kbd>Enter</kbd> copies that text, but it copies it into a tmux paste buffer not the system clipboard 

Back in default mode:

* <kbd><kbd>Ctrl</kbd> + <kbd>b</kbd> <kbd>]</kbd></kbd> pastes from tmux's most recently created paste buffer (i.e. pastes the most recently copied text)
* <kbd><kbd>Ctrl</kbd> + <kbd>b</kbd> <kbd>=</kbd></kbd> (or `tmux choose-buffer` on the command line) shows you all the paste buffers and lets you choose one to paste from

<div class="hint" markdown="1">

#### tmux's Paste Buffers

tmux maintains a list of paste buffers. When you copy some text it creates a new paste buffer and copies the text into it. When you then copy some text again it
creates _another_ new paste buffer, so previously copied texts are still available in their historical paste buffers and can be viewed and pasted using
<kbd><kbd>Ctrl</kbd> + <kbd>b</kbd> <kbd>=</kbd></kbd> (`tmux choose-buffer`).

There are also commands for working with paste buffers so you can script them, my <kbd>Middle Mouse Button</kbd> key binding below uses these:

* `tmux show-buffer` or `tmux showb` prints the contents of the most recent buffer
* `tmux list-buffers` or `tmux lsb` prints a list of the buffers and their contents
* `tmux set-buffer <DATA>` or `tmux setb <DATA>` creates a new buffer and loads `<DATA>` into it
* `tmux load-buffer <PATH>` or `tmux loadb <PATH>` creates a new buffer and loads the contents of a file into it
* `tmux paste-buffer` or `tmux pasteb` pastes the most recent buffer into the current pane (you can also pass `-t <target-pane>` to paste into another pane)
* `tmux save-buffer <PATH>` or `tmux saveb <PATH>` writes the most recent buffer to a file, pass `-a` to append to the file instead of overwriting it
* `tmux delete-buffer` deletes the most recently added buffer

As well as using them as normal shell commands these can also be used on the tmux command line, for example:
<kbd><kbd>Ctrl</kbd> + <kbd>b</kbd> <kbd>:</kbd> <kbd>showb</kbd> <kbd>Enter</kbd></kbd>

These all take an optional `-b <buffer-name>` argument to work with a named buffer instead of the most recent one.
For example to load some data into `my_buffer`, paste it, and then delete the buffer: 

```terminal
$ tmux set-buffer -b my_buffer <DATA>
$ tmux set-buffer -b my_buffer -a <MORE_DATA>  # Append more data to the same buffer
$ tmux paste-buffer -b my_buffer
$ tmux delete-buffer -b my_buffer
```
</div>

As well as copying text, <kbd>Enter</kbd> also exits copy mode and loses your place. If you don't want <kbd>Enter</kbd> to exit copy mode add this to your
`~/.tmux.conf`:

```
# Don't clear the selection or exit copy mode when hitting Enter to copy.
# Use q to clear the selection and exit copy mode.
# Esc to clear the selection without exiting copy mode.
bind-key -T copy-mode-vi Enter send-keys -X copy-selection-no-clear
```

To make <kbd>v</kbd> begin a selection and <kbd>y</kbd> copy the selected text like in vim, add these lines to your `~/.tmux.conf`:

```
# Make v start a selection and y copy a selection, like in vim.
bind-key -T copy-mode-vi v send-keys -X begin-selection
bind-key -T copy-mode-vi y send-keys -X copy-selection-no-clear
# By default v enables rectangle-toggle (block selection) but I just re-bound v
# to begin-selection, so bind r to rectangle-toggle instead.
bind-key -T copy-mode-vi r send-keys -X rectangle-toggle
```

<div class="hint" markdown="1">

#### Copy mode keyboard shortcutes

Some other useful copy-mode keyboard shortcuts (there are more, see [`man tmux`](http://manpages.ubuntu.com/manpages/focal/man1/tmux.1.html)):

* <kbd>Esc</kbd> clears the selection and stays in copy mode

* <kbd>q</kbd> clears the selection and exits copy mode

* <kbd>h</kbd>, <kbd>j</kbd>, <kbd>k</kbd> and <kbd>l</kbd> move left, down, up and right

* <kbd>w</kbd>, <kbd>W</kbd>, <kbd>b</kbd>, <kbd>B</kbd>, <kbd>e</kbd> and <kbd>E</kbd> move forward and backward a word at a time, like in vim

* <kbd>$</kbd> moves to the end of the line and <kbd>0</kbd> goes to the start of the line. <kbd>^</kbd> goes to the first non-blank character on the line

* <kbd>g</kbd> goes to the beginning of the scrollback history (the top) and <kbd>G</kbd> goes to the end (the bottom)

* <kbd>v</kbd> enables block selection, like <kbd><kbd>Ctrl</kbd> + <kbd>v</kbd></kbd> (visual block mode) in vim. This is re-bound to <kbd>r</kbd> in my tmux.conf
  snippet above

* <kbd>V</kbd> selects the entire current line, same as in vim (in vim <kbd>V</kbd> enters visual line mode). Once you've selected a line you can move the cursor
  up and down to select more lines

* <kbd>/</kbd> begins a forward (downward) search and <kbd>?</kbd> begins a backward (upwards) search. <kbd>n</kbd> and <kbd>N</kbd> go to the next and previous
  search match.

  Add these lines to your `~/.tmux.conf` to make <kbd>/</kbd> and <kbd>?</kbd> do _incremental_ search instead (highlights all search matches as you type, similar
  to setting `incsearch` in vim):
  
  ```
  bind-key -T copy-mode-vi / command-prompt -i -p "(search down)" "send -X search-forward-incremental \"%%%\""
  bind-key -T copy-mode-vi ? command-prompt -i -p "(search up)" "send -X search-backward-incremental \"%%%\""
  ```

* <kbd>f</kbd> jumps forward to the next occurrence of a character on the same line. For example <kbd><kbd>f</kbd> <kbd>s</kbd></kbd> jumps to the next `s`.
  <kbd>F</kbd> jumps backward. <kbd>;</kbd> repeats the jump (goes to the _next_ `s`), <kbd>,</kbd> goes to the _previous_ match. <kbd>t</kbd> and <kbd>T</kbd> are
  the same as <kbd>f</kbd> and <kbd>F</kbd> but they jump the cursor to the character _before_ the matching character, instead of on top of the match.

* When the cursor is on an opening bracket <kbd>%</kbd> moves to the closing bracket

* <kbd>D</kbd> copies from the cursor to end of line and exits copy mode

* To make <kbd>Y</kbd> copy the entire current line (like in vim) and exit copy mode, add this to your `~/.tmux.conf`:

  ```
  # Make Y copy the entire current line.
  bind-key -T copy-mode-vi Y send-keys -X copy-line
  ```
  
  This works with a vi-like prefix, so <kbd><kbd>3</kbd> <kbd>Y</kbd></kbd> will copy three lines (the current line and the two below it).
</div>

## tmux-yank

The [tmux-yank](https://github.com/tmux-plugins/tmux-yank) plugin adds some keybindings for copying into the primary selection and clipboard:

### Don't clear the selection on copy

By default tmux-yank clears the selection and exits copy mode as soon as you click <kbd>y</kbd> to copy some text or as soon as you release the
<kbd>Left Mouse Button</kbd> if selecting text with the mouse. To make it behave like a normal app (copying text or releasing the mouse button neither clears the
selection or exits copy mode) add this to your `~/.tmux.conf`:

```
set -g @yank_action 'copy-pipe-no-clear'
```

This is much nicer. For example you can start off a selection with the mouse and then fine-tune it with the keyboard. Or select some text with the mouse, which
already copies the text into the primary selection, and then click <kbd>y</kbd> to also copy it into the clipboard.

### Copying into the primary selection with tmux-yank

Selecting text with the mouse (if tmux's mouse mode is enabled) copies it into the system primary selection. You don't have to press anything to do the copy, just select some text. The text also gets copied into a new tmux paste buffer as well so it won't be lost if you later select some other text.
  
This will probably also work if you _don't_ have tmux's mouse mode enabled, though without the tmux paste buffer integration. The text selection will be handled by
your terminal emulator instead of tmux and your terminal emulator probably copies selected text into the primary selection. But if you do have tmux's mouse mode
enabled then you need tmux-yank in order for mouse selections to be copied.

In most apps <kbd>Middle Mouse Button</kbd> pastes from the primary selection. In tmux if you have mouse mode enabled you have to hold down <kbd>Shift</kbd> while 
middle mouse clicking (to send the middle-mouse-click through to your terminal emulator, not to tmux).
See [Pasting from the primary selection](#pasting-from-the-primary-selection) below for a fix.

In most terminal emulators double-clicking the <kbd>Left Mouse Button</kbd> on a word will select that word and copy it into the primary selection, and triple-
clicking will select a whole line. To get this working in tmux add this to your `~/.tmux.conf` (requires `xsel` to be installed):

```
# Make double-left-click select the word under the cursor (entering copy mode
# if not already in it) and copy the word into the primary selection.
bind-key -T copy-mode-vi DoubleClick1Pane \
    select-pane \; \
    send-keys -X select-word \; \
    send-keys -X copy-pipe-no-clear "xsel -i"
bind-key -n DoubleClick1Pane \
    select-pane \; \
    copy-mode -M \; \
    send-keys -X select-word \; \
    send-keys -X copy-pipe-no-clear "xsel -i"
# Make triple-left-click select the line under the cursor (entering copy mode
# if not already in it) and copy the line into the primary selection.
bind-key -T copy-mode-vi TripleClick1Pane \
    select-pane \; \
    send-keys -X select-line \; \
    send-keys -X copy-pipe-no-clear "xsel -i"
bind-key -n TripleClick1Pane \
    select-pane \; \
    copy-mode -M \; \
    send-keys -X select-line \; \
    send-keys -X copy-pipe-no-clear "xsel -i"
```

### Copying into the clipboard with tmux-yank

In copy mode:

* <kbd>y</kbd> copies the selected text to the clipboard.
  
  Selecting text with the mouse puts you into copy mode, so you can:
    
  1. Select some text with the mouse (this already copies the text into the primary selection)
  2. Click <kbd>y</kbd> to copy the text to the clipboard
    
  (This requires the `set -g @yank_action 'copy-pipe-no-clear'` setting from above.)

  Or you can just select some text with the keyboard in copy mode and click <kbd>y</kbd>.
  
  tmux-yank still copies the text into a tmux paste buffer as well, so the text can still be pasted with <kbd><kbd>Ctrl</kbd> + <kbd>b</kbd> <kbd>]</kbd></kbd> or
  <kbd><kbd>Ctrl</kbd> + <kbd>b</kbd> <kbd>=</kbd></kbd> and won't be lost if you copy some more text.
    
* <kbd>Y</kbd> pastes the current selection onto the command line
  
In default mode:

* <kbd><kbd>Ctrl</kbd> + <kbd>b</kbd> <kbd>y</kbd></kbd> copies what's on your shell's command line to the clipboard
* <kbd><kbd>Ctrl</kbd> + <kbd>b</kbd> <kbd>Y</kbd></kbd> copies the current pane's working directory to the clipboard

## Pasting from the primary selection

To paste from the primary selection: <kbd><kbd>Shift</kbd> + <kbd>Middle Mouse Button</kbd></kbd>.
To make <kbd>Middle Mouse Button</kbd> paste from the primary selection _without_ having to hold down <kbd>Shift</kbd>, add this to your `~/.tmux.conf`
(requires `xsel` to be installed: `sudo apt install xsel`):

```
# Make middle-mouse-click paste from the primary selection (without having to hold down Shift).
bind-key -n MouseDown2Pane run "tmux set-buffer -b primary_selection \"$(xsel -o)\"; tmux paste-buffer -b primary_selection; tmux delete-buffer -b primary_selection"
```

## Pasting from the system clipboard

To paste from the system clipboard just use your terminal emulator's paste command. In both GNOME Terminal and st this is
<kbd><kbd>Shift</kbd> + <kbd>Ctrl</kbd> + <kbd>v</kbd></kbd>.