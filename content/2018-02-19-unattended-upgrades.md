Title: Unattended Upgrades on Ubuntu
Subheading: How to configure an Ubuntu server to automatically keep itself up to date and send you email notifications.
Tags: Ubuntu
Alias: /post/unattended-upgrades/

See also:

* The [`unattended-upgrade` package](https://packages.ubuntu.com/xenial/unattended-upgrades)
* [List of all files](https://packages.ubuntu.com/xenial/all/unattended-upgrades/filelist) that are installed when you install
  `unattended-upgrade`
* [`man unattended-upgrade`](http://manpages.ubuntu.com/manpages/zesty/man8/unattended-upgrade.8.html)
* `less /usr/share/doc/unattended-upgrades/README.md.gz`, after you've done `sudo apt install unattended-upgrade`
* The [ArchWiki page on msmtp](https://wiki.archlinux.org/index.php/Msmtp)

Let's do this on a fresh Ubuntu 16.04 (Xenial) virtual machine, using Vagrant, to demonstrate.

## Create the new VM and ssh into it

```console
$ mkdir myUnattendedUpgradesDemoVM
$ cd myUnattendedUpgradesDemoVM
$ vagrant init ubuntu/xenial64
$ vagrant up
$ vagrant ssh
```

## Install and enable unattended upgrade

`unattended-upgrade` isn't enabled by default (even after you `apt install` it), so you have to run `dpkg-reconfigure` to enable it:

```console
$ sudo apt install unattended-upgrades
$ sudo dpkg-reconfigure unattended-upgrades
```

Answer yes to **Automatically download and install stable updates?**

<img src="https://gist.githubusercontent.com/seanh/49e543c05736ddbb7873240fa2a89767/raw/c51f9205326ef17cbadbf9434a211ac7b0d08074/scrot1.png">

Accept the default origins pattern, which configures `unattended-upgrade` to install only stable and security upgrades.

<img src="https://gist.githubusercontent.com/seanh/49e543c05736ddbb7873240fa2a89767/raw/c51f9205326ef17cbadbf9434a211ac7b0d08074/scrot2.png">

## Test it

First do a dry-run:

```console
$ sudo unattended-upgrade -v -d --dry-run
```

If everything looks good, do a real run:

```console
$ sudo unattended-upgrade -v -d
```

Email notifications
-------------------

To get `unattended-upgrade` to send you email notifications you need to install a program that provides the `mailx` command
(the command that `unattended-upgrade` calls when it wants to send an email) _and_ a Mail Transfer Agent (MTA) program (a program
that actually sends the emails, that the `mailx` command talks to), and make sure that the root user can send mails using the
`mailx` command.

I want an MTA that's able to use the SMTP server of my email provider (Gmail, FastMail etc) so that it can send
emails to my real email account (rather than doing something like appending to files in `/var/spool/mail/`).

[msmtp](http://msmtp.sourceforge.net/) is an MTA with SMTP support that's easy to set up.

1. Install mstmp:

        #!console
        $ sudo apt install msmtp msmtp-mta bsd-mailx
   
    `bsd-mailx` is a package that provides an msmtp-compatible `mailx` command, and `msmtp-mta` hooks `mstmp` up to the `mailx`
    command.
   
2. Create an msmtp config file for the root user:

        #!console
        $ sudo nano /root/.msmtprc
   
    Here's an example of what the contents of this file should look like for FastMail:
   
        account        fastmail
        host           smtp.fastmail.com
        port           465
        from           <YOU>@<YOUR_DOMAIN>
        user           <YOU>@fastmail.com
        password       <A_FASTMAIL_APP_PASSWORD_FOR_SMTP>
        auth           on
        tls            on
        tls_starttls   off
        tls_certcheck  off
        logfile        /root/.msmtp.log
        account default : fastmail

3. Test that the root user can successfully send email using the `mailx` command:

        #!console
        $ echo "This is the email body" > /tmp/body.txt && sudo mailx -s "This is the subject" YOU@YOUR_DOMAIN < /tmp/body.txt; rm /tmp/body.txt

4. Tell `unattended-upgrade` what email address to send emails to. Edit `/etc/apt/apt.conf.d/50unattended-upgrades` and set
   the `Unattended-Upgrade::Mail` setting:

        Unattended-Upgrade::Mail "<YOU>@<YOUR_DOMAIN>"

Logging
-------

Email notifications are better, but it's worth knowing that `unattended-upgrade` logs everything in the
`/var/log/unattended-upgrades/` directory. `/var/log/unattended-upgrades/unattended-upgrades.log` contains recent log entries. 
Older log entries are in the log dir in gzip files. And there's also a
`/var/log/unattended-upgrades/unattended-upgrades-shutdown.log` file.


Reboots
-------

TODO: What's the default behaviour when a reboot is required? Send an email?

You can set `Unattended-Upgrade::Automatic-Reboot` in `/etc/apt/apt.conf.d/50unattended-upgrades` to reboot automatically.

There's also a `reboot-notifier` package but it seems to conflict with a bunch of Ubuntu and Gnome desktop packages.

New releases
------------

TODO: How do you get it to email you or do the upgrade when a new release upgrade is available?

Hypothesis's servers have a `/etc/cron.weekly/update-notifier-common` script containing
`[ -x /usr/lib/ubuntu-releaseupgrader/release-upgrade-motd ] || exit 0` that does this, comes from the
[`update-notifier-common` package](https://packages.ubuntu.com/artful/update-notifier-common) which is a dependency of
`update-notifier`, but this seems to be installed by default. Is it enabled to send email notifications by default?
