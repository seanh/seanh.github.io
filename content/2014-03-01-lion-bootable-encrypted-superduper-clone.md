Title: SuperDuper &amp; FileVault on OS X Lion
Alias: /post/lion-bootable-encrypted-superduper-clone/

Lion is the latest version of OS X that my old MacBook will run, I don't know
if the following applies to later versions as well.

There's a few things that can go wrong when trying to make an encrypted Lion
clone with [SuperDuper](http://www.shirt-pocket.com/SuperDuper/):

* If you just format your external drive as Mac OS Extended (Journaled),
  then the clone will work fine but it won't be encrypted, even if you have
  FileVault encryption on your internal drive (FileVault's full-disk encryption
  in Lion is transparent to apps like SuperDuper).

* The first time I tried to make an encrypted clone, I made a two partition
  layout on the external drive and encrypted and cloned to one of the
  partitions. My MacBook failed to boot from the encrypted partition
  (it gave me the circle with a diagonal line through it).
  Maybe I did something wrong, or maybe SuperDuper clones to encrypted
  partitions are not bootable with multi-partition drive layouts.
  (Clones to unencrypted partitions on multi-partition drives work fine.)

* The next time I used SuperDuper's smart update to do the first copy,
  again the MacBook failed to boot from the clone.

This is the process that eventually worked for me, using
SuperDuper 2.7.2 (v92) on OS X 10.7.5:

1. Use Disk Utility to create a single, Mac OS Extended (Journaled, Encrypted)
   partition filling your entire external drive.
2. Use SuperDuper to clone your internal drive to your external, using the
   erase then copy method to do the first copy.
3. Now test it: shut down your mac, remove your internal drive, connect your
   external drive and turn on your mac. It should boot from your external
   drive, asking you for the drive password to decrypt it during boot.

This confirms that even if your internal drive completely dies, you can boot
your mac from your clone. It's not relying on any kind of boot or recovery
partition or encryption keys stored somewhere on the internal drive.
(To boot from your clone without removing your internal drive first:
shut down the mac, then hold down the option key and turn it on, keep the
option key held down until it offers you a choice of drives to boot from.)

I haven't tried it, but it should be possible to boot the clone and use
SuperDuper to restore your OS X system to a new, blank internal drive or even
to another mac.

You can now shut down your mac, put your internal drive back in, boot from it,
and then connect your external drive and update your clone using SuperDuper's
smart update, and the clone will continue to be bootable.
