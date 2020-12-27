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
* <kbd><kbd>Ctrl</kbd> + <kbd>b</kbd> <kbd>=</kbd></kbd> shows you all the paste buffers and lets you choose one to paste from

tmux maintains a list of paste buffers. When you copy some text it creates a new paste buffer and copies the text into it. When you then copy some text again it
creates _another_ new paste buffer, so previously copied texts are still available in their historical paste buffers and can be viewed and pasted using
<kbd><kbd>Ctrl</kbd> + <kbd>b</kbd> <kbd>=</kbd></kbd>.

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

## Using tmux-yank to copy into the system clipboard

The [tmux-yank](https://github.com/tmux-plugins/tmux-yank) plugin adds some keybindings for copying into the system clipboard:

* Selecting text with the mouse (if tmux's mouse mode is enabled) copies it into the system primary selection. (You don't have to press anything to do the copy,
  just select some text.)
  
  This will probably also work if you _don't_ have tmux's mouse mode enabled, because the text selection will be handled by your terminal emulator instead of tmux
  and your terminal emulator probably copies selected text into the primary selection.

  In most apps middle-mouse-click pastes from the primary selection. In tmux if you have mouse mode enabled you have to hold down <kbd>Shift</kbd> while middle
  mouse clicking (to send the middle-mouse-click through to your terminal emulator, not to tmux).

* If you've set `@yank_action` to `'copy-pipe'` or `'copy-pipe-no-clear'` (see below) then you can also select a word by double-clicking or an entire line by
  triple clicking, but you have to already to be in copy mode for this to work. I can't find a way to make double- and triple-clicking select words and lines when not
  already in copy mode.

* In copy mode:

  * <kbd>y</kbd> copies the selected text to the clipboard.
  
    Selecting text with the mouse puts you into copy mode, so you can:
    
    1. Select some text with the mouse (this already copies the text into the primary selection)
    2. Click <kbd>y</kbd> to copy the text to the clipboard
    
    This again requires setting `@yank_action` to `'copy-pipe'` or `'copy-pipe-no-clear'`, see below.

    Or you can select some text with the keyboard in copy mode and click <kbd>y</kbd>.
  
    tmux-yank still copies the text into a tmux paste buffer as well, so the text can still be pasted with <kbd><kbd>Ctrl</kbd> + <kbd>b</kbd> <kbd>]</kbd></kbd> or
    <kbd><kbd>Ctrl</kbd> + <kbd>b</kbd> <kbd>=</kbd></kbd> and won't be lost if you copy some more text.
    
  By default tmux-yank will clear the selection and exit copy mode when you click <kbd>y</kbd> or as soon as you lift the mouse button if selecting text with the
  mouse. To stop it from clearing the selection add this to your `~/.tmux.conf`:

  ```
  # Don't clear the selection or exit copy mode after copying with y or selecting with the mouse.
  set -g @yank_action 'copy-pipe-no-clear'
  ```

  * <kbd>Y</kbd> pastes the current selection onto the command line
  
* In default mode:

  * <kbd><kbd>Ctrl</kbd> + <kbd>b</kbd> <kbd>y</kbd></kbd> copies what's on your shell's command line to the clipboard
  * <kbd><kbd>Ctrl</kbd> + <kbd>b</kbd> <kbd>Y</kbd></kbd> copies the current pane's working directory to the clipboard

## Pasting from the system clipboard

To paste from the system clipboard just use your terminal emulator's paste command. In both GNOME Terminal and st this is
<kbd><kbd>Shift</kbd> + <kbd>Ctrl</kbd> + <kbd>v</kbd></kbd>.
