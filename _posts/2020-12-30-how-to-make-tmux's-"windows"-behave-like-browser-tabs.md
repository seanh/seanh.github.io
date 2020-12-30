---
tags: [tmux]
---

How to Make tmux's "Windows" Behave like Browser Tabs
=====================================================

<p class="lead" markdown="1">
Make tmux tabs ("windows") look more like browser tabs, and control them using the same keyboard shortcuts that you're used to from browsers and other apps.
Plus some browser-like search shortcuts at the bottom.
</p>

Key bindings
------------

Add the snippet below to your `~/.tmux.conf` file to get browser-like keyboard shortcuts for working with tabs (tmux calls them "windows"):

<kbd><kbd>Ctrl</kbd> + <kbd>t</kbd></kbd> Open a new tab.

<kbd><kbd>Ctrl</kbd> + <kbd>Page Down</kbd></kbd>, <kbd><kbd>Ctrl</kbd> + <kbd>Page Up</kbd></kbd> Go to the next, previous tab.  
In browsers <kbd><kbd>Ctrl</kbd> + <kbd>Tab</kbd></kbd> and <kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>Tab</kbd></kbd> also work, but binding `C-Tab` and
`C-S-Tab` in tmux doesn't seem to work.

<kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>&larr;</kbd></kbd>, <kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>&rarr;</kbd></kbd> Move the current tab left,
right (swapping it with the left or right adjacent tab).  
In browsers this is <kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>Page Up</kbd></kbd> and
<kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>Page Down</kbd></kbd> but binding `C-S-PgUp` and `C-S-PgDn` in tmux doesn't seem to work.

<kbd><kbd>Alt</kbd> + <kbd>1</kbd> &hellip; <kbd>8</kbd></kbd> Jump to tab 1 ... 8.

<kbd><kbd>Alt</kbd> + <kbd>9</kbd></kbd> Jump to tab 9 (I couldn't figure out how to implement "jump to rightmost tab").

<kbd><kbd>Alt</kbd> + <kbd>0</kbd></kbd> Jump to tab 10.

<kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>w</kbd></kbd> Close the current tab.  
In browsers this is just <kbd><kbd>Ctrl</kbd> + <kbd>w</kbd></kbd> but
<kbd><kbd>Ctrl</kbd> + <kbd>w</kbd></kbd> is often used by terminal apps (for example vim uses it for switching between windows). I followed GNOME Terminal's lead
in using <kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>w</kbd></kbd> to close tabs instead.

<kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>q</kbd></kbd> Ask for confirmation before closing all tabs and killing the current tmux session.
Browsers use <kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>w</kbd></kbd> to close the current window and all its tabs, but I've already used that for closing a
single tab. So I've followed GNOME Terminal again and used <kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>q</kbd></kbd> to close the whole window.
Firefox does also use <kbd><kbd>Ctrl</kbd> + <kbd>q</kbd></kbd> for quit (closing _all_ windows and tabs).

<kbd>F11</kbd> Toggle the current pane between zoomed (occupying the whole window and hiding all other panes) and unzoomed (normal).

```
set -g base-index 1       # Start numbering windows at 1, not 0.
set -g pane-base-index 1  # Start numbering panes at 1, not 0.
bind -n C-t new-window
bind -n C-PgDn next-window
bind -n C-PgUp previous-window
bind -n C-S-Left swap-window -t -1\; select-window -t -1
bind -n C-S-Right swap-window -t +1\; select-window -t +1
bind -n M-1 select-window -t 1
bind -n M-2 select-window -t 2
bind -n M-3 select-window -t 3
bind -n M-4 select-window -t 4
bind -n M-5 select-window -t 5
bind -n M-6 select-window -t 6
bind -n M-7 select-window -t 7
bind -n M-8 select-window -t 8
bind -n M-9 select-window -t 9
bind -n M-0 select-window -t 10
bind -n C-W kill-window
bind -n C-Q confirm -p "Kill this tmux session?" kill-session
bind -n F11 resize-pane -Z
```

Appearance
----------

Add the snippet below if you also want your tmux tabs to _look_ a bit more like browser tabs. It makes the current tab stand out a lot more by having a different
background color, and also highlights the last tab (which you can jump to directly with the `last-window` command) with a grey background:

```
set -g status-style "bg=default fg=#ffffff"
set -g window-status-current-style "bg=default fg=default,reverse"
set -g window-status-last-style "bg=#444444 fg=#ffffff"
set -g window-status-separator ''  # No spaces between windows in the status bar.
set -g window-status-format "#{?window_start_flag,, }#I:#W#{?window_flags,#F, } "
set -g window-status-current-format "#{?window_start_flag,, }#I:#W#{?window_flags,#F, } "
```

<figure>
  <img src="/assets/images/tmux-tabs.png" style="box-shadow:none;">
  <figcaption>tmux's tabs ("windows") styled to look a bit more like browser tabs.</figcaption>
</figure>

You can also move the tabs to the top of the window with `set -g
status-position top`, but I find I prefer them at the bottom.

In the screenshot I've also removed the default stuff that tmux puts in the
bottom-left and bottom-right of the window:

```
set -g status-left ''
set -g status-right ''
```

Search
------

Here's a snippet to add browser-like keyboard bindings for searching:

<kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>f</kbd></kbd> Begin a search of the terminal history.

<kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>g</kbd></kbd> Go to the next search match. Just <kbd>n</kbd> also works (tmux's default).

<kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>h</kbd></kbd> Go to the previous search match.  Just <kbd>N</kbd> also works (tmux's default).

<kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>j</kbd></kbd> Clear the search. Just <kbd>q</kbd> also works (tmux's default).

These are just <kbd><kbd>Ctrl</kbd> + <kbd>f</kbd></kbd>, <kbd><kbd>Ctrl</kbd> + <kbd>g</kbd></kbd>, etc in Chrome and Firefox but those are likely to conflict
with terminal apps so I've followed GNOME Terminal in using <kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd></kbd> and in using
<kbd>h</kbd> to go to the previous match.

These assume you're using vi-style copy mode bindings (see the `mode-keys` setting in [`man tmux`](http://manpages.ubuntu.com/manpages/focal/man1/tmux.1.html)).
If you're using the default emacs-style copy mode bindings replace `copy-mode-vi` with just `copy-mode`.

```
bind -n C-F copy-mode \; command-prompt -i -p "(search up)" "send -X search-backward-incremental \"%%%\""
bind -T copy-mode-vi C-F copy-mode \; command-prompt -i -p "(search up)" "send -X search-backward-incremental \"%%%\""
bind -T copy-mode-vi C-G send-keys -X search-again
bind -T copy-mode-vi C-H send-keys -X search-reverse
bind -T copy-mode-vi C-J send-keys -X cancel
```

These use _incremental_ search, so it'll highlight all matches and jump to the first match as you type (instead of waiting for you to hit <kbd>Enter</kbd>).
To also make the normal <kbd>/</kbd> and <kbd>?</kbd> search commands in copy mode search incrementally, add:

```
bind -T copy-mode-vi / command-prompt -i -p   "(search down)" "send -X search-forward-incremental \"%%%\""
bind -T copy-mode-vi ? command-prompt -i -p   "(search up)" "send -X search-backward-incremental \"%%%\""
```

Again, this is for vi-style copy mode bindings. If you're using the default emacs-style copy mode bindings then <kbd><kbd>Ctrl</kbd> + <kbd>r</kbd></kbd>
and <kbd><kbd>Ctrl</kbd> + <kbd>s</kbd></kbd> already do incremental search.
