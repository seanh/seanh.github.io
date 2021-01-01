---
tags: [tmux]
---

Browser-like Search Shortcuts for tmux
======================================

tmux's default key sequence to enter copy mode and begin a search of the terminal history/scrollback is pretty awkward:
<kbd><kbd><kbd>Ctrl</kbd> + <kbd>b</kbd></kbd> <kbd>[</kbd> <kbd><kbd>Ctrl</kbd> + <kbd>r</kbd></kbd></kbd>
if you're using the default emacs-style copy mode bindings, or
<kbd><kbd><kbd>Ctrl</kbd> + <kbd>b</kbd></kbd> <kbd>[</kbd> <kbd>?</kbd></kbd> if you're using the vim-style bindings.

Browsers use much easier shortcuts for searching the page. In Chrome and Firefox:

* <kbd><kbd>Ctrl</kbd> + <kbd>f</kbd></kbd> begins a search
* <kbd><kbd>Ctrl</kbd> + <kbd>g</kbd></kbd> goes to the next match
* <kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>g</kbd></kbd> goes to the previous match

You wouldn't want to bind <kbd><kbd>Ctrl</kbd> + <kbd>f</kbd></kbd> in a terminal emulator because it's likely to
conflict with keyboard shortcuts used by apps running in the terminal. So GNOME Terminal uses a similar set of
<kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd></kbd>-based shortcuts instead:

* <kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>f</kbd></kbd> begins a search
* <kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>g</kbd></kbd> goes to the next match
* <kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>h</kbd></kbd> goes to the previous match

Apps like tmux that run _inside_ a terminal can't use <kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd></kbd>: <kbd>Ctrl</kbd>-modified keys are case-insensitive in terminal
apps.

These tmux key bindings are designed to be as close as possible to Chrome, Firefox and GNOME Terminal's,
while avoiding <kbd><kbd>Ctrl</kbd> + <kbd>f</kbd></kbd> or <kbd><kbd>Ctrl</kbd> + <kbd>Shift</kbd></kbd>:

* <kbd><kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>f</kbd></kbd> begins a search

* <kbd><kbd>Ctrl</kbd> + <kbd>g</kbd></kbd> goes to the next match.
  tmux's default key binding <kbd>n</kbd> also works.

* <kbd><kbd>Ctrl</kbd> + <kbd>h</kbd></kbd> or <kbd><kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>g</kbd></kbd> goes to the previous match.
  tmux's default key binding <kbd>N</kbd> also works.

* tmux's default <kbd>Esc</kbd> key binding will clear the search (as it also does in browsers and GNOME Terminal). If you're using tmux's vi-style copy mode key
  bindings <kbd>Esc</kbd> will leave you in copy mode, <kbd>q</kbd> will clear the search and exit copy mode.

To add the bindings paste this snippet into your `~/.tmux.conf` file:

```
bind -n C-M-f copy-mode \; command-prompt -i -p "(search up)" "send -X search-backward-incremental \"%%%\""
bind -T copy-mode-vi C-M-f copy-mode \; command-prompt -i -p "(search up)" "send -X search-backward-incremental \"%%%\""
bind -T copy-mode-vi C-g send -X search-again
bind -T copy-mode-vi C-M-g send -X search-reverse
bind -T copy-mode-vi C-h send -X search-reverse
```

<div class="warning" markdown="1">
The snippet is for tmux's vi-style copy mode bindings. If you're using emacs-style replace `copy-mode-vi` with just `copy-mode`.
</div>

These key bindings do _incremental_ search: it highlights all matches and jumps to the first match as you type the search query, instead of waiting for you to
hit <kbd>Enter</kbd>. If you're using emacs-style bindings then the default <kbd><kbd>Ctrl</kbd> + <kbd>r</kbd></kbd> and <kbd><kbd>Ctrl</kbd> + <kbd>s</kbd></kbd>
bindings for starting a search from copy mode already do an incremental search. If you're using vi-style bindings then the default copy mode bindings
<kbd>?</kbd> and <kbd>/</kbd> do a non-incremental search (an excremental search). To make <kbd>?</kbd> and <kbd>/</kbd> do incremental search add these lines to
your `~/.tmux.conf`:

```
bind -T copy-mode-vi / command-prompt -i -p "(search down)" "send -X search-forward-incremental \"%%%\""
bind -T copy-mode-vi ? command-prompt -i -p "(search up)" "send -X search-backward-incremental \"%%%\""
```
