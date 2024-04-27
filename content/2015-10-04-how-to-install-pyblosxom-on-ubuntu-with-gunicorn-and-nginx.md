Title: Pyblosxom on Ubuntu with Gunicorn &amp; Nginx
Subheading: How to set up a Pyblosxom blog on Ubuntu using the Gunicorn WSGI server and Nginx web server.
Tags: pyblosxom
redirect_from: /post/how-to-install-pyblosxom-on-ubuntu-with-gunicorn-and-nginx/

This is a guide to installing the blog engine
[Pyblosxom](http://pyblosxom.github.io/) on [Ubuntu](http://www.ubuntu.com/),
and deploying it with [Gunicorn](http://gunicorn.org/) and
[Nginx](http://nginx.org/).

This is a really quick and easy way to deploy Pyblosxom, and it has the added
bonus that the steps to install Pyblosxom and run it with Gunicorn on your
local Ubuntu machine for development are a subset of those to deploy Pyblosxom
with Gunicorn and Nginx on an Ubuntu server for a production website.

These instructions were tested on Ubuntu 14.04 but may work on other versions
of Ubuntu as well.

## Installing Pyblosxom and Gunicorn locally for development

You might want to run Pyblosxom on your local desktop or laptop running Ubuntu,
for example to work on draft entries before publishing them to your server,
to hack on Pyblosxom plugins or themes, or just to try out Pyblosxom or try a
plugin or theme.

Since the version of Pyblosxom currently in Ubuntu's package repositories is
the latest version, we'll just install it using `apt-get`. We'll install
Gunicorn at the same time as well:

```console
$ sudo apt-get install pyblosxom gunicorn
```

Now to create a new Pyblosxom blog in a `blog` directory in your home
directory, do:

```console
$ pyblosxom-cmd create ~/blog
```

This generates several files in the `blog` directory including a `config.py`
file containing the blog's configuration settings, a `flavours` directory
containing themes for the blog, and an `entries` directory for the blog's
entries (including an example entry).

To run your Pyblosxom blog locally with Gunicorn:

```console
$ gunicorn --log-file - \
  --pythonpath ~/blog Pyblosxom.pyblosxom:PyblosxomWSGIApp
```

Open <http://127.0.0.1:8000/> in a web browser to see the blog, it's that easy!

The `--log-file -` makes Gunicorn print any errors from Pyblosxom to the
terminal.


## Installing Pyblosxom, Gunicorn and Nginx on a web server

These steps will create a Pyblosxom blog on an Ubuntu web server with Gunicorn
running behind Nginx, and running automatically as a service.

The easiest way to install Pyblosxom and Gunicorn on the server is with
`apt-get`, just as we did on the local development machine. This time we'll
also install Nginx at the same time:

```console
$ sudo apt-get install pyblosxom gunicorn nginx
```

Create a new Pyblosxom blog just as we did on the development machine.
A good place to keep website files on a server is in `/var/www`:

```console
$ pyblosxom-cmd create /var/www/blog
```

Create a Gunicorn config file `/etc/gunicorn.d/blog` with the following
contents, to tell Ubuntu how to run your blog with Gunicorn automatically:

    CONFIG = {
        'working_dir': '/var/www/blog',
        'args': (
            'Pyblosxom.pyblosxom:PyblosxomWSGIApp',
        ),
    }

**Note**: These `/etc/gunicorn.d/` config files and running Gunicorn using
the `service` command are features of the Gunicorn Debian package, they won't
work on non-Debian based Linux distributions.

Restart the Gunicorn service:

```console
$ sudo service gunicorn restart
```

At this point Gunicorn should be running your blog on port `8000`. You can test
it by running `curl localhost:8000`, which should print out the HTML code of
your blog's front page.

**Note**: If you install a plugin, or make a change to your `config.py` file,
you'll need to restart Gunicorn with `sudo service gunicorn restart` for the
change to take effect.

To serve the blog to the Internet we need to hook Gunicorn up to Nginx.
Create the Nginx config file `/etc/nginx/sites-available/blog` with the
following contents:

```nginx
server {
  listen 80;
  server_name blog.example.com;
  access_log  /var/log/nginx/blog.log;

  location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }
}
```

Replace `blog.example.com` with your blog's domain name.

To enable the Nginx site create a `sites-enabled` symlink for it:

```console
$ sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled
```

You also need to remove the `sites-enabled` symlink for the default Nginx site:

```console
$ sudo rm /etc/nginx/sites-enabled/default
```

Restart the Nginx service, and test the new Nginx configuration file:

```console
$ sudo service nginx restart
$ sudo nginx -t
```

Your Pyblosxom blog should now be running on port 80 at your server's domain
name or IP address.


### Log files

If Pyblosxom crashes you can look in the Nginx and Gunicorn log files for
error messages. There are located at `/var/log/nginx/blog.log` and
`/var/log/gunicorn/blog.log`.


### Permissions

All files in `/var/www` need to be readable by the `www-data` user, and
directories need to be readable and executable by this user. Otherwise
Pyblosxom can crash or fail to see blog entries. An `HTTP 500` error from
Pyblosxom containing `IOError: [Errno 13] Permission denied` is a sure sign
that you have a file in `/var/www/blog` that `www-data` can't read.

One way to make sure that `www-data` can read all your blog's files is to make
the files and directories world-readable so that any user on the system can
read them, but only you can write them. In the output of `ls -l` the
permissions of a file should be `-rw-r--r--`, and the permissions of a
directory shoud be `drwxr-xr-x`.

To make sure that all files and directories that you create on the server have
these permissions, set your `umask` to `0022`. Put the line:

```console
$ umask 0022
```

in your `~/.profile`, `~/.bashrc`, or other shell configuration file.

Note that if you create files on your local machine and then move them to the
server, or if you create files on the server using an editor running locally
that is capable of editing remote files, you may need to make sure that your
umask on your local machine is `0022` as well.


### Static files

To make static files such as image, CSS and JavaScript files available to your
blog you can setup a second site on the same web server but at a different
domain or subdomin to host them.

Create the Nginx config file `/etc/nginx/sites-available/static` with these
contents:

```nginx
server {
  listen 80;
  server_name static.example.com;
  root /var/www/static;
  expires 1d;  # How long should static files be cached for.
}
```

Replace `static.example.com` with the domain name for your static files site.

Create the directory on the server where the static files will go:

```console
$ mkdir /var/www/static
```

Enable the site by creating a `sites-enabled` symlink for it and restarting
Nginx:

```console
$ sudo ln -s /etc/nginx/sites-available/static /etc/nginx/sites-enabled
$ sudo service nginx restart
```

Now if you put, say, an image file at `/var/www/static/image.jpeg` then it'll
be available to web browsers at <http://static.example.com/image.jpeg>. To use
this image in one of your blog posts, you might put an `img` tag like this
in the entry file:

```html
<img src="http://static.example.com/image.jpeg" />
```

**Note**: As with your blog's files, all files in `/var/www/static` need to be
readable by the `www-data` user.

**Tip**: If your theme needs access to static files you can add a setting in
your `config.py` file like this:

```python
py["static_url"] = "http://static.example.com/"
```

Then you can link to static files in your flavour templates with code like:

```html
<link href="$(static_url)/mystyles.css" rel="stylesheet" type="text/css">
```

This saves having to code the full URL to your static files site into your
flavour templates.
