---
tags: [tmux]
---

Binding Keys in tmux
====================

<div class="tip" markdown="1">
To list all current key bindings, including any custom bindings you've added and bindings added by plugins:

* <kbd><kbd><kbd>Ctrl</kbd> + <kbd>b</kbd></kbd> <kbd>?</kbd></kbd>
* `tmux list-keys` or `tmux lsk` in a shell inside tmux
* `list-keys` or `lsk` at tmux's command prompt (<kbd><kbd><kbd>Ctrl</kbd> + <kbd>b</kbd></kbd> <kbd>:</kbd></kbd>)
</div>

The `bind-key` and `unbind-key` commands (aliases `bind` and `unbind`) change key bindings in tmux. Like all tmux commands a `bind` or `unbind` command can be
entered in three different ways:

1. By running `tmux bind ...` in a shell inside tmux
2. By hitting <kbd><kbd><kbd>Ctrl</kbd> + <kbd>b</kbd></kbd> <kbd>:</kbd></kbd> in tmux and then entering `bind ...` into tmux's command prompt
3. By adding a `bind ...` line to your `~/.tmux.conf` file to bind the key at startup

For example:

    bind C-t new-window

Now <kbd><kbd><kbd>Ctrl</kbd> + <kbd>b</kbd></kbd> <kbd><kbd>Ctrl</kbd> + <kbd>t</kbd></kbd></kbd> will open a new window.

To remove the key binding:

    unbind C-t

The `C-` stands for <kbd>Control</kbd>. There's also `S-` for shift and `M-` for <kbd>Alt</kbd>, e.g. `bind M-t new-window`, `bind -n C-S-PgDn swap-window -t +1`. There are also several special key names for use in
`bind` commands, including: `Up`, `Down`, `Left`, `Right`, `BSpace`, `Delete`, `End`, `Enter`, `Escape`, `F1` ... `F12`, `Home`, `Insert`, `PageDown` or `PgDn`,
`PageUp` or `PgUp`, `Space` and `Tab`.

Every keybinding lives in a **key table**. There are three built-in key tables:

1. `prefix`: Keys in this table must be pressed after the prefix <kbd><kbd>Ctrl</kbd> + <kbd>b</kbd></kbd> to trigger the binding. This is the table that the
   `bind` command uses by default. Example: `bind C-t new-window`

2. `root`: Keys in this table can just be pressed, without any prefix. Use `-n` (a shortcut for `-T root`) to bind keys in this table.
   Example: `bind -n C-t new-window`

3. `copy-mode` or `copy-mode-vi` for when in copy mode, depending on whether you're using emacs- or vi-style key bindings mode
   (add `set-window-option -g mode-keys vi` to your `~/.tmux.conf` file to force vi-style). Use `-T copy-mode-vi` to bind keys in this table.
   Example: `bind -T copy-mode-vi C-t new-window`

## Repeatable prefix key bindings

For key bindings in the `prefix` table the `-r` option can be used to make them repeatable.
For example with `tmux bind -r t new-window` <kbd><kbd><kbd>Ctrl</kbd> + <kbd>b</kbd></kbd> <kbd>t</kbd></kbd> is needed to open a first new window, then you can
keep hitting <kbd>t</kbd> to open more without having to hit <kbd><kbd>Ctrl</kbd> + <kbd>b</kbd></kbd> each time. The `repeat-time` setting decides how much time
you have to repeat the key before the prefix times out (default: 500 milliseconds).

## Binding a key to run multiple commands at once

You can use `\;` to separate multiple commands in a single key binding:

    bind t new-window \; display-message "new window opened"

If using the `tmux bind` shell command you may need to quote the commands instead:

    tmux bind t 'new-window; display-message "new window opened"'

A multiline format is also possible by ending each line with <code> &bsol;</code> or (if the line is part of the command) <code> &bsol;; &bsol;</code>. Example:

```
bind -n DoubleClick1Pane \
    select-pane \; \
    copy-mode -M \; \
    send-keys -X select-word \; \
    send-keys -X copy-pipe-no-clear "xsel -i"
```

## Binding a sequence of keys: custom key tables

You can bind keys in custom named key tables and use the `switch-client` command to move between key tables. This enables sequences of keys to be bound.
For example to make `abc` in quick succession open a new window:

    bind -T root       a switch-client -T my_table_1
    bind -T my_table_1 b switch-client -T my_table_2
    bind -T my_table_2 c new-window

## Binding `"` and `'`

To bind `"` or `'` you need to put them in quotes:

    bind '"' split-window
    bind "'" new-window

## Binding mouse events

If tmux's mouse support is enabled (`set -g mouse on`) then `bind` can also bind mouse events. For example to make clicking the <kbd>Left Mouse Button</kbd> on a
pane open a new window:

    bind -n MouseDown1Pane new-window

The mouse events are `MouseDown1`, `MouseUp1`, `MouseDrag1`, `MouseDragEnd1`, `DoubleClick1`, `TripleClick1`, `MouseDown2`, `MouseUp2`, `MouseDrag2`,
`MouseDragEnd2`, `DoubleClick2`, `TripleClick2`, `MouseDown3`, `MouseUp3`, `MouseDrag3`, `MouseDragEnd3`, `DoubleClick3`, `TripleClick3`, `WheelUp`, `WheelDown`.
Each event always needs to be suffixed with one of the target locations `Pane`, `Border`, `Status` (the window list in the status line), `StatusLeft`,
`StatusRight` or `StatusDefault` (any other part of the status line that isn't the window list or left or right parts).

Mouse button 2 (`MouseDown2`, `MouseUp2`, ...) is the middle mouse button and 3 (`MouseDown3`, `MouseUp3`, ...) is the right button.

The special token `{mouse}` in a mouse event `bind` command resolves to the target-window or target-pane that was clicked on, for when you need the target window
or pange in the bound command.
For example `bind -n MouseDown1Pane select-pane -t {mouse}` makes clicking on a pane select that pane.
`bind -n MouseDown1Status select-window -t {mouse}` makes clicking on a window in the status line select that window.
