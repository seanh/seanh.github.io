Title: Mozilla Thunderbird Keyboard Shortcuts
Alias: /post/thunderbird-keyboard-shortcuts/

Thunderbird actually has fairly complete keyboard shortcuts. The schema is all
over the place, there's little consistency to the design of the keyboard
shortcuts, and frequently needed shortcuts are often out-of-the-way keys or
difficult to hit multi-key combos, but the shortcuts **do** cover a lot of the
app's functionality. You can't do everything with the keyboard, you'll have to
reach for the mouse sometimes, but a lot can be done from the keyboard in
Thunderbird.

The complete set of shortcuts isn't documented in any one place that I can
find, so this is my cheat sheet. It isn't intended to be comprehensive, just
contains the ones that I find useful. It's compiled from experimentation and
various sources including:

* [Thunderbird keyboard shortcuts page](https://support.mozilla.org/en-US/kb/keyboard-shortcuts)
  on Mozilla Support
* An old [Mozilla Keyboard Shortcuts](https://www-archive.mozilla.org/docs/end-user/moz_shortcuts.html)
  page
* The [keyconfig Thunderbird extension](https://addons.mozilla.org/en-GB/thunderbird/addon/dorando-keyconfig/)
  (install the extension then go to <samp><samp>Tools</samp> → <samp>Keyconfig</samp></samp> to get a list of shortcuts)
* Browsing through the in-app menu bar (it has keyboard shortcuts labeled
  on the right hand side of each menu item)

## Undo

<kbd><kbd>Ctrl</kbd>+<kbd>z</kbd></kbd> undoes the last action, and
<kbd><kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>z</kbd></kbd> redoes,
but be warned that undo **doesn't work for all actions**.

## The menu bar

<figure>
    <img src="{static}/images/thunderbird/menubar.png" alt="Thunderbird's menu bar" title="Thunderbird's menu bar">
    <figcaption>Thunderbird's menu bar</figcaption>
</figure>

Menu bars are out of fashion these days. The menu bar is hidden by default in both Firefox
and Thunderbird now. You can still open the menu bar in Firefox or Thunderbird
with a keyboard shortcut like <kbd>F10</kbd> or <kbd><kbd>Alt</kbd>+<kbd>f</kbd></kbd>,
or you can show it permanently (so you can use it with the mouse too) with
<kbd><kbd>Alt</kbd>+<kbd>v</kbd> <kbd>Enter</kbd> <kbd>Enter</kbd></kbd>
(<kbd><kbd><samp>View</samp></kbd> → <kbd><samp>Toolbars</samp></kbd> → <kbd><samp>Menu Bar</samp></kbd></kbd> in the menu bar).
Chrome doesn't have a menu bar (its header bar menu is similar, and can be
opened with <kbd>F10</kbd> and controlled with the arrow keys and
<kbd>Enter</kbd>, but contains less functionality). Modern Gnome apps also have
a Chrome-like header bar menu that can be opened with <kbd>F10</kbd> instead of
a menu bar.

But the humble menu bar has a lot of strengths: it's global and consistent, it
has space to contain a **lot** of functionality, it can be controlled with either
the keyboard or the mouse, you don't need to memorize keyboard shortcuts to
control it with the keyboard (since you can see on the labels what letters you
need to press to activate them) but you will get faster as you start to
memorize common actions. Unlike with direct keyboard shortcuts, the menu bar
provides a visual confirmation of which action was selected, so mistakes are
less likely and less confusing when they happen.  Menu bar labels even provide
a place to document the direct (non-menu-bar) keyboard shortcuts for actions.

Use the menu bar as the main way of controlling Thunderbird with the keyboard,
and memorize just a few direct keyboard shortcuts for very commonly used
actions. The advantage of direct keyboard shortcuts is that they can be done
with a single keystroke, whereas getting to a menu bar item requires at
least two, and often three or four keystrokes. Menu bars are more flexible
though: they can contain more actions, and can contain dynamic lists of options
such as lists of folders to copy or move to.

### Using the menu bar with the keyboard

None of what follows is unique to Thunderbird, it's just the standard way of
using a menu bar from the keyboard (and the standard way that apps use their
menu bars to document their keyboard shortcuts) across Linux, Windows and
macOS. For example, here's Leafpad:

<figure>
    <img src="{static}/images/thunderbird/leafpad.png" alt="Leafpad's menu bar" title="Leafpad's menu bar">
    <figcaption>Leafpad's menu bar</figcaption>
</figure>

Getting back to Thunderbird though,
<kbd><kbd>Alt</kbd>+<kbd>f</kbd>, <kbd>e</kbd>, <kbd>v</kbd>, <kbd>g</kbd>, <kbd>m</kbd>, <kbd>t</kbd> or <kbd>h</kbd></kbd>
opens the menu bar at the <samp>File</samp>, <samp>Edit</samp>, <samp>View</samp>
etc menu. <kbd>F10</kbd> also opens the <samp>File</samp> menu.

You can use the menus with the arrow keys and <kbd>Enter</kbd>, but you can
also jump directly to and activate a menu item in one keystroke by hitting the
underlined character in the menu item's label or, if there's no underlined
character, the label's first character. This means you can use
combos of 2+ keystrokes to hit a menu item. For example the key combo
<kbd><kbd>Alt</kbd>+<kbd>m</kbd> <kbd>c</kbd> <kbd>r</kbd> <kbd>r</kbd></kbd>
will copy a message by opening the <samp>Message</samp> menu (<kbd><kbd>Alt</kbd>+<kbd>m</kbd></kbd>)
then the <samp>Copy To</samp> submenu (<kbd>c</kbd>), then the <samp>Recent</samp>
submenu (<kbd>r</kbd>), and then finally selecting the <samp>Receipts</samp>
folder (<kbd>r</kbd> again):

<figure>
    <img src="{static}/images/thunderbird/receipts.gif" alt="Copying a message using menu bar keyboard controls" title="Copying a message using menu bar keyboard controls">
    <figcaption>Copying a message using menu bar keyboard controls</figcaption>
</figure>

#### Cycling

If multiple menu items have the same underlined or first character then hitting
that character will jump to the first matching menu item but not activate it
yet, and hitting it repeatedly will cycle through the matching items. When the
item you want is selected then hit <kbd>Enter</kbd> to activate it.
The underlined characters in the menu labels have been chosen to avoid this
situation, but it can still happen when selecting a folder from your email. For
example here hitting <kbd>b</kbd> repeatedly cycles through all the folders
beginning with <samp>b</samp>:

<figure>
    <img src="{static}/images/thunderbird/b.gif" alt="Menu bar cycling" title="Menu bar cycling">
    <figcaption>Menu bar cycling</figcaption>
</figure>

#### Keyboard shortcuts documented in the menu bar

Last menu bar tip: the right-aligned labels on many menu bar items show you
the keyboard shortcuts that you can use to execute those actions directly.
For example, here the <samp>Message</samp> menu is showing you that instead
of going to <kbd><kbd><samp>Message</samp></kbd> → <kbd><samp>New Message</samp></kbd></kbd>
(<kbd><kbd>Alt</kbd>+<kbd>m</kbd> <kbd>n</kbd></kbd>) you can just hit <kbd><kbd>Ctrl</kbd>+<kbd>n</kbd></kbd>.
Similarly, <kbd>a</kbd> will archive the currently selected message, and
<kbd>r</kbd> will mark the thread as read, without having to open any menus:

<figure>
    <img src="{static}/images/thunderbird/labels.png" alt="Keyboard shortcuts documented in the menu bar" title="Keyboard shortcuts documented in the menu bar">
    <figcaption>Keyboard shortcuts documented in the menu bar</figcaption>
</figure>

So the way to learn most keyboard shortcuts in Thunderbird is this:

1. Begin by using the menu bar with the arrow keys and <kbd>Enter</kbd> to
   control Thunderbird with the keyboard

2. For menu bar items that you use a lot, start to use and memorise menu bar
   key combos like <kbd><kbd>Alt</kbd>+<kbd>m</kbd> <kbd>n</kbd></kbd> to get
   to them. For many actions, such as things like moving or copying a message
   that require selecting a folder from the menu, these key combos are the
   best way to do those actions with the keyboard.

3. For menu bar items that you use a lot and that have a keyboard shortcut
   labeled on them, start to use and memorize the direct keyboard shortcut
   instead.

Most keyboard shortcuts in Thunderbird have menu bar items with the shortcut
documented on them, so they can be learned over time from using the menu bar.
But not all keyboard shortcuts have menu bar items. Some that don't (see below
for more on each of these):

* <kbd>Space</kbd> to scroll through unread content
* <kbd>→</kbd> and <kbd>←</kbd> to move within the current thread and expand and
  collapse threads.
* Selecting multiple messages with <kbd><kbd>Shift</kbd>+<kbd>↑</kbd></kbd> and <kbd><kbd>Shift</kbd>+<kbd>↓</kbd></kbd>.
* <kbd><kbd>Shift</kbd>+<kbd>Del</kbd></kbd> to delete a message immediately
  (rather than moving it to the trash)
* <kbd><kbd>Shift</kbd>+<kbd>c</kbd></kbd> to mark all as read (although this
  can be done with the menu bar by selecting all then marking as read)
* Moving between tabs
* Going to the global search bar or quick filter toolbar
* Moving the keyboard focus between the three mail panes with <kbd>F6</kbd> and <kbd><kbd>Shift<</kbd>+<kbd>F6</kbd></kbd>
* ...

### Context menus

<kbd><kbd>Shift</kbd>+<kbd>F10</kbd></kbd> opens the context menu (right mouse click menu) for the
currrently selected folder, message, or thread:

<figure>
    <img src="{static}/images/thunderbird/contextmenu.png" alt="One of the context menus" title="One of the context menus">
    <figcaption>One of the context menus</figcaption>
</figure>

Which context menu you get depends on which mail pane (see [The three mail
panes](#the-3-mail-panes)) has the keyboard focus and on whether a thread or a
single message is selected. The context menu for the message pane contains many
of the same items as, but isn't exactly the same as, the one for the thread
pane. Most, maybe all, of what you can do from these context menus can be done
using the menu bar instead, without having to worry about which pane has
keyboard focus / which context menu you're going to get.

## The main window

### Getting new messages

<kbd>F5</kbd> or <kbd>F9</kbd> gets new messages for the currently selected account,
<kbd><kbd>Shift</kbd>+<kbd>F5</kbd></kbd> or <kbd><kbd>Shift</kbd>+<kbd>F9</kbd></kbd> gets new messages for all accounts.

### The three mail panes

<kbd>F6</kbd> and <kbd><kbd>Shift</kbd>+<kbd>F6</kbd></kbd> move the keyboard focus between the
folder pane, thread pane, and message pane. For example:

* If you want to go to another folder you can hit <kbd>F6</kbd> until the focus
  is on the folder pane, then use the up and down arrows. (Alternatively, press
  <kbd><kbd>Alt</kbd>+<kbd>g</kbd> <kbd>o</kbd></kbd> to change folders using the <samp><samp>Go</samp> →
  <samp>Folder</samp></samp> menu.)

* Similarly, you can use <kbd>F6</kbd> to focus the thread pane and then use
  the arrows to move betweeen messages. (Alternatively, <kbd>f</kbd> and
  <kbd>b</kbd> always move to the next and previous message in the thread pane,
  regardless of which pane has keyboard focus. This will automatically move the
  keyboard focus to the thread pane.)

* Or focus the message pane and then use the arrows to scroll the message
  contents.

<kbd>F8</kbd> shows / hides the message pane. If you use the <samp>Vertical View</samp>
layout as I do this can be useful when you want to read a long subject or
sender in the thread pane.

### Moving between messages

<kbd>f</kbd> and <kbd>b</kbd> change the keyboard focus to the thread pane and
move between messages.

<kbd>[</kbd> and <kbd>]</kbd> move "back" and "forward". This means back to the
previously selected message, no matter whether that message was in the current
folder or another, and whether it was selected using the mouse or the keyboard.
The exact behaviour of these is pretty confusing though. It behaves differently
after moving between messages using <kbd>↑</kbd> and <kbd>↓</kbd> than after
using <kbd>f</kbd> and <kbd>b</kbd>, and doesn't work with selecting multiple
messages. These are probably best only used occasionally, when you want to
quickly jump back to a message far away in the current folder or in a different
folder.

### Moving through unread messages

<kbd>n</kbd>, <kbd>t</kbd> and <kbd>Space</kbd> are ways to advance through
unread messages skipping over read ones. <kbd>n</kbd> goes to the next unread
message and <kbd>t</kbd> goes to the next unread thread. <kbd>n</kbd> and
<kbd>t</kbd> will ask you if you want to move on to the next folder if there
are no more unread in the current folder. Similarly, <kbd>Space</kbd> is a way
to scroll through all unread content: repeatedly hitting <kbd>Space</kbd> it
will scroll down in the current message until it gets to the bottom of the
message, then it'll go to the next unread message and do the same, and like
<kbd>n</kbd> it will ask you if you want to move to the next folder with unread
messages after you've exhausted the current ones.

### Threads

<kbd>→</kbd> and <kbd>←</kbd> move within the current thread and expand and
collapse threads. <kbd>→</kbd> expands the currently selected thread if it
isn't expanded already, then moves to the next message in the thread, and won't
move beyond the end of the thread. <kbd>←</kbd> moves to the previous message
in the thread, or collapses the thread if already on the first message in the
thread (and also won't move outside of the current thread). <kbd>→</kbd> and
<kbd>←</kbd> only work when the keyboard focus is in the thread pane. If focus
is in the folder pane they do a similar thing but with the folders. If the
focus is in the message pane they scroll the message horizontally (or do
nothing if there's no horizontal scroll bar).

<kbd>&#92;</kbd> collapses _all_ threads and <kbd>*</kbd> expands all threads
(keyboard focus can be in any pane).

<kbd><kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>a</kbd></kbd> expands the currently selected thread (or the thread
that the currently selected message belongs to) if it isn't already expanded,
and selects all the messages in the thread. This works whether the keyboard
focus is in the folder, thread or message pane.

### Selecting multiple messages

<kbd><kbd>Ctrl</kbd>+<kbd>a</kbd></kbd> selects all messages in the thread pane _if_ the keyboard
focus is in the folder or thread pane. If the focus is in the message pane then
it selects all text in the current message instead.

When the keyboard focus is in the thread pane you can select multiple messages
without necessarily selecting all messages in the thread, with
<kbd><kbd>Shift</kbd>+<kbd>↑</kbd></kbd> and <kbd><kbd>Shift</kbd>+<kbd>↓</kbd></kbd>.

### Acting on messages

<kbd>a</kbd> archives the selected message(s) or thread(s).

<kbd><kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>m</kbd></kbd> moves the currently selected message to the same folder
as the last message that was moved was moved to. (The same folder as named in
the <samp><samp>Message</samp> → <samp>Move to "Some Folder" Again</samp></samp> menu bar item.)

<kbd>Del</kbd> deletes the selected message(s) or thread(s) to the trash.
<kbd><kbd>Shift</kbd>+<kbd>Del</kbd></kbd> deletes them immediately, without moving them to the trash
first. <kbd><kbd>Shift</kbd>+<kbd>Del</kbd></kbd> can't be undone with <kbd><kbd>Ctrl</kbd>+<kbd>z</kbd></kbd> either.

<kbd>s</kbd> stars / un-stars the selected message(s) or thread(s).

<kbd>m</kbd> marks the selected message(s) or thread(s) as read / unread.

<kbd>r</kbd> marks the currently selected thread, or the thread that the
currently selected message belongs to, as read (but can't be used to mark a
read thread as unread, like <kbd>m</kbd> can).

<kbd><kbd>Shift</kbd>+<kbd>c</kbd></kbd> marks all as read. Again unlike <kbd>m</kbd>, pressing
<kbd><kbd>Shift</kbd>+<kbd>c</kbd></kbd> again will _not_ mark all as unread. You can undo
<kbd><kbd>Shift</kbd>+<kbd>c</kbd></kbd> with <kbd><kbd>Ctrl</kbd>+<kbd>z</kbd></kbd> though.

<kbd><kbd>Ctrl</kbd>+<kbd>p</kbd></kbd> prints the selected message. Doesn't work if a thread is
selected. _Does_ work is multiple individual messages are selected, but does
something very weird.

<kbd><kbd>Ctrl</kbd>+<kbd>s</kbd></kbd> saves a message as an <code>eml</code> file.

<kbd>1</kbd>, <kbd>2</kbd>, <kbd>3</kbd>, <kbd>4</kbd> and <kbd>5</kbd>
add/remove different tags (important, work, personal, ...) from the message,
and <kbd>0</kbd> removes all tags from the message.

<kbd><kbd>Ctrl</kbd>+<kbd>+</kbd></kbd> zooms in on the contents of the current message,
<kbd><kbd>Ctrl</kbd>+<kbd>-</kbd></kbd> zooms out, and <kbd><kbd>Ctrl</kbd>+<kbd>0</kbd></kbd> resets the zoom level.

<kbd><kbd>Ctrl</kbd>+<kbd>u</kbd></kbd> views the raw source of the selected message.

### Writing emails

<kbd><kbd>Ctrl</kbd>+<kbd>m</kbd></kbd> or <kbd><kbd>Ctrl</kbd>+<kbd>n</kbd></kbd> opens a new message.

<kbd><kbd>Ctrl</kbd>+<kbd>r</kbd></kbd> opens a new message in reply to the currently selected
message(s). This works with multiple messages selected, and will open multiple
reply windows. Keyboard focus can be on any of the three panes.

<kbd><kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd></kbd> does a "reply all" to the selected message(s).

<kbd><kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>l</kbd></kbd> does a "reply to list" for the selected message(s).

<kbd><kbd>Ctrl</kbd>+<kbd>l</kbd></kbd> forwards the selected message(s).

<kbd><kbd>Ctrl</kbd>+<kbd>e</kbd></kbd> edits selected message(s) as if they were new messages.

None of the keyboard shortcuts for replying or forwarding work when a thread is
selected, but they all work when multiple messages are selected.
<kbd><kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>a</kbd></kbd> expands the currently selected thread and selects all
its messages, at which point the reply and forward shortcuts will work.

### Misc

<kbd>F2</kbd> renames current folder.

<kbd><kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>b</kbd></kbd> opens the <samp>Address Book</samp> window.

### Closing and quitting

<kbd><kbd>Ctrl</kbd>+<kbd>w</kbd></kbd> when the main window is selected closes the main window. This
will quit Thunderbird _if_ there aren't any other windows open. If there's a
message window open, for example, that window will remain open after the main
window closed. <kbd><kbd>Ctrl</kbd>+<kbd>F4</kbd></kbd> does the same thing but only works from the
main window, doesn't work for closing a message window (but _does_ work for
closing a tab). <kbd><kbd>Ctrl</kbd>+<kbd>q</kbd></kbd> quits Thunderbird entirely (only works from
the main window).

### Tabs

<kbd>Enter</kbd> opens the selected message(s) or thread(s) in tab(s). This
will open multiple tabs if a thread or multiple messages are selected.
<kbd><kbd>Ctrl</kbd>+<kbd>o</kbd></kbd> does the same but doesn't work when a thread is selected!

<kbd><kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>o</kbd></kbd> opens the selected message as conversation. This only
works when a single message is selected, not multiple messages or a thread. The
conversation view for a message is a list of all messages in the same thread as
the message, including messages that aren't in the same folder, such as
messages sent by yourself.

<kbd><kbd>Ctrl</kbd>+<kbd>j</kbd></kbd> opens the <samp>Saved Files</samp> tab. You can search and scroll
through all attachments that you've ever saved, and open the downloaded files.

<kbd><kbd>Alt</kbd>+<kbd>1</kbd></kbd>, <kbd><kbd>Alt</kbd>+<kbd>2</kbd></kbd>, <kbd><kbd>Alt</kbd>+<kbd>3</kbd></kbd>, <kbd><kbd>Alt</kbd>+<kbd>4</kbd></kbd>,
<kbd><kbd>Alt</kbd>+<kbd>5</kbd></kbd>, <kbd><kbd>Alt</kbd>+<kbd>6</kbd></kbd>, <kbd><kbd>Alt</kbd>+<kbd>7</kbd></kbd> and <kbd><kbd>Alt</kbd>+<kbd>8</kbd></kbd> go to
the 1…8th tabs. <kbd><kbd>Alt</kbd>+<kbd>9</kbd></kbd> goes to the last tab. <kbd><kbd>Ctrl</kbd>+<kbd>Page Up</kbd></kbd>
and <kbd><kbd>Ctrl</kbd>+<kbd>Page Down</kbd></kbd> go to the next and previous tabs.
<kbd><kbd>Ctrl</kbd>+<kbd>Tab</kbd></kbd> and <kbd><kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>Tab</kbd></kbd> also go to the next and
previous tabs.

<kbd><kbd>Ctrl</kbd>+<kbd>w</kbd></kbd> or <kbd><kbd>Ctrl</kbd>+<kbd>F4</kbd></kbd> closes a tab. <kbd><kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>t</kbd></kbd>
restores recently closed tabs, like in Firefox.

### Search

These all work no matter which pane has keyboard focus:

<kbd><kbd>Ctrl</kbd>+<kbd>k</kbd></kbd> focuses the global search bar. (The search results tab
that you get after doing a search with this seems to have no keyboard
controls at all. You can avoid it by using the
[Search as list extension](https://addons.mozilla.org/en-US/thunderbird/addon/search-as-list/).)

<kbd><kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>k</kbd></kbd> opens and focuses the quick filter toolbar for
filtering the messages in the thread pane. <kbd>Esc</kbd> closes it again.

<kbd><kbd>Ctrl</kbd>+<kbd>f</kbd></kbd> opens and focuses a "Find in page" toolbar for the currently
selected message (only works when a single individual message is selected).
Once a search term is entered here <kbd><kbd>Ctrl</kbd>+<kbd>g</kbd></kbd> goes to the next match
(and moves the keyboard focus into the message pane). <kbd><kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>g</kbd></kbd>
goes back to the previous match. Alternatively <kbd>F3</kbd> and
<kbd><kbd>Shift</kbd>+<kbd>F3</kbd></kbd> also cycle through matches.

<kbd><kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>f</kbd></kbd> opens the advanced search window.

## The message composer window

This window has its own different menu bar and keyboard shortcuts.

* <kbd><kbd>Ctrl</kbd>+<kbd>s</kbd></kbd> saves a message as a draft.

* <kbd><kbd>Ctrl</kbd>+<kbd>Enter</kbd></kbd> sends the message.

* <kbd><kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>Enter</kbd></kbd> sends the message "later". This is useful when composing messages while offline. The message will
  go into your local outbox folder. You can manually send the message later with <samp><samp>File</samp> → <samp>Send Unsent Messages</samp></samp>. I don't think
  unsent messages ever get sent automatically.

* <kbd><kbd>Ctrl</kbd>+<kbd>1</kbd></kbd> goes back to the main Thunderbird window (but leaves the compose window open).

* <kbd><kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>a</kbd></kbd> is supposed to open the attach file(s) browser,
  but doesn't seem to work for me.

* <kbd><kbd>Ctrl</kbd>+<kbd>w</kbd></kbd> closes the message window (you'll be asked whether you want
  to discard the in-progress message or save it as a draft).

* <kbd>F9</kbd> shows and hides the contacts sidebar.

* <kbd><kbd>Ctrl</kbd>+<kbd>r</kbd></kbd> re-wraps text.

* <kbd><kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>p</kbd></kbd> opens a spellchecking dialog for the whole email
  that you can control with the keyboard.


## Other windows

There are many other windows and tabs in Thunderbird. The address book window, the view source window, the advanced search 
window, the search results tab, the saved files tab… These all have their own menu bars and some of them have some of their own 
keyboard shortcuts. Some of the main window keyboard shortcuts will work in some of them. I don't use any of these windows
often, so it's not worth learning keyboard shortcuts for them.
