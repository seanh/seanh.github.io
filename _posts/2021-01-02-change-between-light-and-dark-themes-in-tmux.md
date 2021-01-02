---
draft: true
sitemap: false
robots: noindex, nofollow
tags: [tmux]
---

Change Between Light and Dark Themes in tmux
============================================

<p class="lead" markdown="1">
How to toggle between light-background and dark-background themes in tmux.
</p>

tmux's `window-style` setting changes the default background and foreground colours for panes, and you can use it to toggle your terminal between light-on-dark
and dark-on-light themes:

```terminal 
$ # Change from dark to light background.
$ tmux set -g window-style 'bg=#FFFFFF fg=#171421' && tmux set -g status-style 'bg=#FFFFFF fg=#171421'
$ # Change from light back to dark background.
$ tmux set -g window-style 'bg=#171421 fg=#D0CFCC' && tmux set -g status-style 'bg=#171421 fg=#D0CFCC'
```

Here's a shell script to toggle between light and dark, using a tmux user option to keep track of which theme is currently active:

```sh
#!/usr/bin/env sh
set -e

# This assumes that your terminal starts out in dark mode.
# If your terminal has a light background by default add
# `set -g @light_mode true` to your `~/.tmux.conf` file.
if [ "$(tmux show -gv @light_mode)" = true ]
then
  tmux set -g window-style 'bg=#171421 fg=#D0CFCC'
  tmux set -g @light_mode false
else
  tmux set -g window-style 'bg=#FFFFFF fg=#171421'
  tmux set -g @light_mode true
fi
```

Save this script as `~/.tmux/bin/toggle-theme` and mark it executable and you can toggle between dark and light mode by just running it:

```terminal
$ ~/.tmux/bin/toggle-theme
```

You can bind a keyboard shortcut to toggle the theme. For example to bind add this to your `~/.tmux.conf` file:

```
bind T run-shell "~/.tmux/bin/toggle-theme"
```

Reload the file:

```terminal
$ tmux source ~/.tmux.conf
```

Now <kbd><kbd><kbd>Ctrl</kbd> + <kbd>b</kbd></kbd> <kbd><kbd>Shift</kbd> + <kbd>t</kbd></kbd></kbd> should toggle between light and dark mode.

You might want to add more lines to the script to change other options like `status-style` (the colour of the status bar) and `pane-border-style`
(the colour of the pane borders) between light and dark mode. See [the full version of the script](https://github.com/seanh/tmux/blob/67ac5ee97a5ac79ca5115ab2f02f7ed4f41250dd/bin/toggle-theme)
in my tmux config for an example.

There's also a `window-active-style` setting that you can use to highlight the active pane by giving it a different background colour than the other panes.

This all requires your terminal emulator to have a colour palette that works on either a light or a dark background. I'm using the default colour palette from
GNOME Terminal (as of GNOME 3.38):

<table>
<tr><td>Palette entry 0</td> <td><code>#171421</code></td></tr>
<tr><td>Palette entry 1</td> <td><code>#C01C28</code></td></tr>
<tr><td>Palette entry 2</td> <td><code>#26A269</code></td></tr>
<tr><td>Palette entry 3</td> <td><code>#A2734C</code></td></tr>
<tr><td>Palette entry 4</td> <td><code>#12488B</code></td></tr>
<tr><td>Palette entry 5</td> <td><code>#A347BA</code></td></tr>
<tr><td>Palette entry 6</td> <td><code>#2AA1B3</code></td></tr>
<tr><td>Palette entry 7</td> <td><code>#D0CFCC</code></td></tr>
<tr><td>Palette entry 8</td> <td><code>#5E5C64</code></td></tr>
<tr><td>Palette entry 9</td> <td><code>#F66151</code></td></tr>
<tr><td>Palette entry 10</td> <td><code>#33DA7A</code></td></tr>
<tr><td>Palette entry 11</td> <td><code>#E9AD0C</code></td></tr>
<tr><td>Palette entry 12</td> <td><code>#2A7BDE</code></td></tr>
<tr><td>Palette entry 13</td> <td><code>#C061CB</code></td></tr>
<tr><td>Palette entry 14</td> <td><code>#33C7DE</code></td></tr>
<tr><td>Palette entry 15</td> <td><code>#FFFFFF</code></td></tr>
<tr><td>Cursor and highlight background colour</td> <td><code>#D0CFCC</code></td></tr>
<tr><td>Cursor and highlight background colour</td> <td><code>#171421</code></td></tr>
</table>

As you can see from the script my dark mode background and foreground colours are `#171421` (background) and `#D0CFCC` (foreground),
and light mode is `#FFFFFF` (background) and `#171421` (foreground).
