---
tags: [tmux]
---

Setting Options in tmux
=======================

<p class="lead" markdown="1">
How to use tmux's `set` and `show` commands to set and query tmux config settings ("options").
</p>

The `set-option` command (alias `set`) sets options, and `show-option` (alias `show`) shows what value an option is currently set to.
See [`man tmux`](http://manpages.ubuntu.com/manpages/focal/man1/tmux.1.html#options) for a list of all the available options.
There are three ways to enter a `set` or `show` command:

1. By running `tmux set ...` or `tmux show ...` in a shell inside tmux.
   For example:
   
   ```terminal
   $ tmux set status off  # Hide the status bar.
   $ tmux show status
   status off
   ```

2. By hitting <kbd><kbd><kbd>Ctrl</kbd> + <kbd>b</kbd></kbd> <kbd>:</kbd></kbd> then entering `set ...` or `show ...` into tmux's command prompt

3. By adding a `set ...` line to your `~/.tmux.conf` file to set an option at startup

There are four types of option:

1. **Session options** are set and shown using plain `set` and `show` commands, and apply to the current session. For example:

   ```
   set status off  # Turn off the status bar, for this session only.
   show status
   ```

   Each session option also has a global value that each session inherits by default. Use `-g` to change the global value. When setting a session option in your
   `~/.tmux.conf` file you _always_ want `-g` because there is no current session. Example:
   
   ```
   set -g status 2  # Show the two-line version of the status bar, for all sessions by default.
   ```

2. **Server options** are set and shown using the `-s` option to `set` and `show` and apply to the tmux server. The `-s` can be omitted and tmux will infer it from
   the option name.

3. **Window options** are set and shown using the `-w` option to `set` and `show` and apply to the current window. The `-w` can be omitted and tmux will infer it
   from the option name. For example:

   ```
   tmux set -w window-status-separator '|'  # Change this window's status separator to "|"
   ```
   
   or with the `-w` inferred:
   
   ```
   tmux set window-status-separator '|'  # Change this window's status separator to "|"
   ```
   
   Each window option also has a global value that each window inherits by default. Use `-g` to change the global value. When setting a window option in your
   `~/.tmux.conf` you _always_ want `-g` because there is no current window. Example:

   ```
   tmux set -g window-status-separator '|'  # Change the status separator to "|" for all windows by default.
   ```

4. **Pane options** are set and shown using the `-p` option to `set` and `show` and apply to the current pane. The `-p` is necessary, otherwise tmux will assume
   the option is a window option. Pane options inherit from window options, so any pane option can be set as a window option instead and will apply to all panes in
   the window (or to all panes, if set as a global window option).

`show <OPTION>` will normally output nothing if the option is unset and is being inherited from a parent set.
`show -A <OPTION>` will print the inherited value, flagging it with a `*` if it's inherited.

## Appending to an option

`-a` can be used to repeatedly append to an option's value, useful for building up styles and strings. For example this:

    set status-left foo
    set -a status-left bar
                   
is equivalent to:

    set status-left foobar

## Unsetting an option

Use `-u` to unset an option and revert to the default:

    set -u status
    set -gu status  # Unset the global `status` option.

## Setting an option only if it isn't already set

`-o` sets an option but only if it's not already set, and fails if the option is already set:

    set -o status off  # Turn off the status bar, but only if `status` isn't already set for this session.

## Supressing errors

`-q` supresses errors, such as the error that `-o` gives when an option is already set, or the error that happens when an option name is unknown:

    set -qo status off
    set -q foo bar

## User options

Options whose names begin with `@` are user options. These can have any name and value, so while `set foo bar` will fail (because there is no option `foo`),
`set @foo bar` will always succeed. Some plugins use user options. You do need the `-w` or `-s` when trying to set a user option as a server or window option,
tmux can't infer them because it doesn't know what the option is.
