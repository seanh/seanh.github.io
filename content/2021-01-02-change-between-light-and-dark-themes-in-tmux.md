Title: Change Between Light and Dark Themes in tmux
Tags: tmux
Summary: How to toggle between light-background and dark-background themes in tmux.

<img src="{static}/videos/tmux-toggle-theme.gif">

tmux's `window-style` setting changes the default foreground and background colours for windows, and you can use it to toggle your terminal between light-on-dark
and dark-on-light themes:

```console
$ # Change the current window (all panes) to light background.
$ tmux set window-style 'fg=#171421,bg=#ffffff'
$ # Change back to dark background.
$ tmux set window-style 'fg=#d0cfcc,bg=#171421'
```

Here's a shell script to toggle between light and dark:

```sh
#!/usr/bin/env sh
#
# Toggle the current window (all panes) between light and dark themes.
set -e

default_window_style='fg=#d0cfcc,bg=#171421'
alternate_window_style='fg=#171421,bg=#ffffff'
current_window_style=$(tmux show -Av window-style)

case $current_window_style in
    $default_window_style|'default')
        # Change to the alternate window style.
        tmux set window-style $alternate_window_style
        ;;
    *)
        # Change back to the default window style.
        tmux set window-style $default_window_style
        ;;
esac
```

Save this script as `~/.tmux/bin/toggle-theme` and mark it executable
(`chmod u+x ~/.tmux/bin/toggle-theme`) and you can toggle between dark and
light mode with a single command:

```console
$ ~/.tmux/bin/toggle-theme
```

You can bind a keyboard shortcut to toggle the theme. For example add this to
your `~/.tmux.conf` file:

```
bind T run-shell ~/.tmux/bin/toggle-theme
```

Reload the file:

```console
$ tmux source ~/.tmux.conf
```

Now <kbd><kbd><kbd>Ctrl</kbd> + <kbd>b</kbd></kbd> <kbd><kbd>Shift</kbd> + <kbd>t</kbd></kbd></kbd> toggles between light and dark mode.

You might want to add more lines to the script to change other options like `pane-border-style` and `pane-active-border-style`
(the colours of the pane borders) between light and dark mode. See [the full version of the script](https://github.com/seanh/tmux/blob/master/bin/toggle-theme)
in my tmux config for an example.

The script changes the default foreground and background colours of the **current window** (all panes).
You'll want your status line colours to be ones that work well against either a dark
or a light background, since the same session might contain both light and dark windows
at the same time. I'm using these (in my `~/.tmux.conf`):

```
set -g status-style 'fg=#d0cfcc,bg=#171421'
set -g window-status-current-style 'bg=default,reverse'
```

You can also use `-g` to change the colours of all windows across all sessions or `-p`
to change the colours of the current pane only:

```console
$ # Change the colours of all windows across all sessions.
$ tmux set -g window-style 'fg=#171421,bg=#ffffff'
$ # Change the colours of the current pane only.
$ tmux set -p window-style 'fg=#171421,bg=#ffffff'
```

There's also a `window-active-style` setting that you can use to highlight the active pane by giving it a different background colour than the other panes.

This all requires your terminal emulator to have a colour palette that works on either a light or a dark background. I'm using the default colour palette from
GNOME Terminal (as of GNOME 3.38):

<table>
<tr><td>Palette entry 0</td> <td><code style="background:#171421; color:white;">#171421</code></td></tr>
<tr><td>Palette entry 1</td> <td><code style="background:#C01C28; color:white;">#C01C28</code></td></tr>
<tr><td>Palette entry 2</td> <td><code style="background:#26A269; color:white;">#26A269</code></td></tr>
<tr><td>Palette entry 3</td> <td><code style="background:#A2734C; color:white;">#A2734C</code></td></tr>
<tr><td>Palette entry 4</td> <td><code style="background:#12488B; color:white;">#12488B</code></td></tr>
<tr><td>Palette entry 5</td> <td><code style="background:#A347BA; color:white;">#A347BA</code></td></tr>
<tr><td>Palette entry 6</td> <td><code style="background:#2AA1B3">#2AA1B3</code></td></tr>
<tr><td>Palette entry 7</td> <td><code style="background:#D0CFCC">#D0CFCC</code></td></tr>
<tr><td>Palette entry 8</td> <td><code style="background:#5E5C64; color:white;">#5E5C64</code></td></tr>
<tr><td>Palette entry 9</td> <td><code style="background:#F66151">#F66151</code></td></tr>
<tr><td>Palette entry 10</td> <td><code style="background:#33DA7A">#33DA7A</code></td></tr>
<tr><td>Palette entry 11</td> <td><code style="background:#E9AD0C">#E9AD0C</code></td></tr>
<tr><td>Palette entry 12</td> <td><code style="background:#2A7BDE; color:white;">#2A7BDE</code></td></tr>
<tr><td>Palette entry 13</td> <td><code style="background:#C061CB; color:white;">#C061CB</code></td></tr>
<tr><td>Palette entry 14</td> <td><code style="background:#33C7DE">#33C7DE</code></td></tr>
<tr><td>Palette entry 15</td> <td><code style="background:#FFFFFF">#FFFFFF</code></td></tr>
<tr><td>Cursor and highlight background</td> <td><code style="background:#D0CFCC">#D0CFCC</code></td></tr>
<tr><td>Cursor and highlight foreground</td> <td><code style="background:#171421; color:white;">#171421</code></td></tr>
</table>

<p></p>

As you can see from the script my dark mode background and foreground colours are
<code style="background:#171421; color:#D0CFCC">#D0CFCC on #171421</code>
and light mode is
<code style="background:#FFFFFF; color:#171421">#171421 on #FFFFFF</code>.
