---
draft: true
sitemap: false
robots: noindex, nofollow
---

How to Backup Your Fastmail & Gmail Accounts Locally with isync
===============================================================

[isync](https://isync.sourceforge.io/) is a command line application that can synchronize a remote IMAP account (like a Fastmail or Gmail account) with local
maildirs. This post will show you how to use isync to make a local backup of your Fastmail and Gmail accounts. We're going to be using isync in **read-only mode**:
changes will be synced from your Fastmail and Gmail accounts to your local filesystem but not the other way round, so there's no chance of isync accidentally deleting
mail from your Fastmail or Gmail account if something goes wrong with the local copy.

isync is quick to install and configure and works great.

### Install isync

On Ubuntu it's just:

```shellsession
$ sudo apt install isync
```

### Configure isync

You need to create a `~/.mbsyncrc` file before isync will work (although the project is called "isync" the actual command line program is `mbsync`).
Here's an `~/.mbsyncrc` to backup a Fastmail account and a Gmail account to a local `~/Mail` folder:

```
# ~/.mbsyncrc

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
Pipelinedepth 1

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

The `Pipelinedepth 1` is necessary to prevent isync from hitting Gmail's bandwidth quotas and triggering this error message:

    IMAP error: unexpected BYE response: [OVERQUOTA] Account exceeded command or bandwidth limits.

### Create Fastmail and Gmail app passwords

You need to create a Fastmail app password for isync to use to access to your Fastmail account.
In Fastmail's web interface go to <https://www.fastmail.com/settings/security/devicekeys>, unlock the interface, and click <samp>New App Password</samp>.
You can create an app password with IMAP access only and with read-only access as an extra protection against isync accidentally deleting your mail.
See [Fastmail's docs](https://www.fastmail.com/help/clients/apppassword.html) for more on creating app passwords.

For Gmail you have to go to <https://myaccount.google.com/security> and click on <samp>App passwords</samp> to create one.
See [Google's docs on app passwords](https://support.google.com/accounts/answer/185833).

### Install `pass` and add the app passwords to it

We're going to use [pass](https://www.passwordstore.org/) to store the Fastmail and Gmail app passwords in encrypted files for isync to read:

1. Install `pass`:

   ```shellsession
   $ sudo apt install pass
   ```

2. Create a GPG key that'll be used to encrypt the passwords:

   ```shellsession
   $ gpg --full-generate-key
   ```

3. Initialize `pass` with the GPG key:

   ```shellsession
   $ pass init <GPG_KEY_ID>
   ```
   
   If you're not sure what the GPG key's ID is you can run `gpg --list-secret-keys` to list your keys.

4. You can now optionally run:

   ```shellsession
   $ pass git init
   ```
   
   If you have [Git](https://git-scm.com/) installed and want `pass` to automatically keep history in a git repo.

5. Add the Fastmail app password to `pass`:

   ```shellsession
   $ pass insert mbsync/fastmail
   ```
   
   Paste in the password when asked.

6. Add the Gmail app password to `pass`:

   ```shellsession
   $ pass insert mbsync/gmail
   ```

You should now be able to read the app passwords with `pass mbsync/fastmail` or `pass mbsync/gmail`. These are the commands that the `.mbsyncrc` file above uses
to get the passwords.

### Create the empty local maildirs

`mbsync` won't create these so you have to do it manually:

```shellsession
$ mkdir -p ~/Mail/Fastmail ~/Mail/Gmail
```

### Run `mbsync`

Now to download all of your email just run:

```shellsession
$ mbsync -a
```

You can re-run the command at any time to update the local copy. You can also download only Fastmail or only Gmail with `mbsync fastmail` or `mbsync gmail`.

#### Gmail errors from `mbsync`

    IMAP error: unexpected BYE response: System Error

You just seem to have to re-run it when this happens. Can take a lot of re-runs to get through the first initial download of all your mail.

Also this:

    Warning: lost track of 39544 pulled message(s)
    
Which doesn't seem to be a problem?

### Read the local copy with Mutt

Once you've made a local copy of your email you can read the `~/Mail` folder with a local mail client like Thunderbird or [Mutt](https://mutt.org/).

To install Mutt run:

```shellsession
$ sudo apt install mutt
```

You can now just run `mutt -Rf ~/Mail/Fastmail/Inbox/` to open your Fastmail inbox in read-only mode.
But it can be convenient to create a `~/.muttrc` file to avoid having to pass arguments on the command line.
Here's a minimal example:

```
# ~/.muttrc

set read_only

set spoolfile=+Fastmail/Inbox
set mbox=+Fastmail/Archive
set record=+Fastmail/Sent
set postponed=+Fastmail/Drafts
set trash=+Fastmail/Trash

set header_cache=~/.muttcache
set message_cachedir=~/.muttcache
```

The `set read_only` tells Mutt to work in read-only mode (for example Mutt won't let you delete messages).
Since isync isn't going to sync any changes up to your Fastmail and Gmail accounts it makes sense to tell Mutt not to make any changes to the local copy.

The `header_cache` and `message_cachedir` settings tell Mutt to use a `~/.muttcache` dir to speed up re-opening and searching large folders.
You should create this directory before launching Mutt: `mkdir ~/.muttcache`.

The rest of the settings just tell Mutt where to find your inbox, archive, drafts, sent, and trash folders.
For example Mutt will open `~/Mail/Fastmail/Inbox` by default when you launch it.

Now you can just launch `mutt` without command line arguments:

```shellsession
$ mutt
```
