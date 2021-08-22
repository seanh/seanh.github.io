---
draft: true
sitemap: false
robots: noindex, nofollow
---

How to backup Fastmail & Gmail accounts with isync
==================================================

[isync](https://isync.sourceforge.io/) is a command line application that can synchronize a remote IMAP account (like a Fastmail or Gmail account) with local
maildirs. This post will show you how to use isync to make a local backup of your Fastmail and Gmail accounts. We're going to be using isync in read-only mode:
changes will be synced from your Fastmail and Gmail accounts to your local copies but not the other way round, so there's no chance of isync accidentally deleting
mail from your Fastmail or Gmail account if something goes wrong with the local copy.

### Install isync

On Debian or Ubuntu it's just:

```shellsession
$ sudo apt install isync
```

### Configure isync

You need to create a `~/.mbsyncrc` file before isync will work (although the project is called "isync" the actual command line program is `mbsync`).
Here's an `~/.mbsyncrc` to download a Fastmail account and a Gmail account into a local `~/Mail` folder:

```
CopyArrivalDate yes  # Don't mess up message timestamps when moving messages between folders.
Sync Pull            # Download changes only. Don't sync local changes up to the server.
Create Slave         # Create new folders in the local copy only.
Remove Slave         # Remove deleted folders from the local copy only.
Expunge Slave        # Expunge deleted messages from the local copy only.

IMAPAccount fastmail
Host imap.fastmail.com
User YOUR_USERNAME@fastmail.com
PassCmd "pass mbsync/fastmail"
SSLType IMAPS

IMAPStore fastmail-remote
Account fastmail

MaildirStore fastmail-local
Path ~/Mail/Fastmail/
Inbox ~/Mail/Fastmail/Inbox
SubFolders Verbatim

Channel fastmail
Master :fastmail-remote:
Slave :fastmail-local:
Patterns *
SyncState *

IMAPAccount gmail
Host imap.gmail.com
User YOUR_USERNAME@gmail.com
PassCmd "pass mbsync/gmail"
SSLType IMAPS
Pipelinedepth 50

IMAPStore gmail-remote
Account gmail

MaildirStore gmail-local
Path ~/Mail/Gmail/
Inbox ~/Mail/Gmail/Inbox
SubFolders Verbatim

Channel gmail
Master :gmail-remote:
Slave :gmail-local:
Patterns *
SyncState *
```

The `Pipelinedepth 50` is necessary to prevent isync from hitting Gmail's bandwidth quotas and triggering this error message:

    IMAP error: unexpected BYE response: [OVERQUOTA] Account exceeded command or bandwidth limits.

### Create Fastmail and Gmail app passwords

### Install `pass` and add the passwords to it

### Create the empty local maildirs

```shellsession
$ mkdir -p ~/Mail/Fastmail ~/Mail/Gmail
```

### Run `mbsync`

Now to download all of your email just run:

```shellsession
$ mbsync -a
```

You can re-run the command at any time to update the local copy. You can also download only Fastmail or only Gmail with `mbsync fastmail` or `mbsync gmail`.
