Title: Background Tasks as Simple Web Services
Subheading: The design of the broken link checker API for CKAN.
Tags: CKAN
Alias: /post/background-tasks-as-simple-web-services/

[deadoralive](https://github.com/ckan/deadoralive) is a broken link
checker service that works with any site that implements its simple API.
[ckanext-deadoralive](https://github.com/ckan/ckanext-deadoralive) is a [CKAN](http://ckan.org/)
plugin that implements the API for CKAN sites. Together they demonstrate an
approach to implementing background tasks as simple web services.

When designing Dead or Alive we wanted a way to implement a background task
that would:

1. Be easy to install and maintain
2. Be easy to implement
3. Provide the background task as a service that can also be used by non-CKAN
   sites

([Thanks to Ross for the idea](https://github.com/ckan/ideas-and-roadmap/issues/65))

Examples of background tasks that you might want for CKAN include:

* Checking a site for broken links ([ckanext-qa](https://github.com/ckan/ckanext-qa))
* Automatically rating the datasets on a site according to
  [Tim Berners-Lee's five stars of openness](http://5stardata.info/) (ckanext-qa again)
* Downloading archive copies of all the resource files a site links to
  ([ckanext-archiver](https://github.com/ckan/ckanext-archiver))
* "Harvesting" datasets from one CKAN site into another
  ([ckanext-harvest](https://github.com/ckan/ckanext-harvest))
* Parsing a site's tabular data files and pushing the data into CKAN's
  DataStore ([DataPusher](https://github.com/ckan/datapusher/))
* [Analytics](http://docs.ckan.org/en/latest/maintaining/tracking.html)
* Sending [email notifications](http://docs.ckan.org/en/latest/maintaining/email-notifications.html)

Previous approaches to background tasks in CKAN include:

* Extensions that use [Celery](http://www.celeryproject.org/).
  This requires running a Celery daemon in development and setting up
  [Supervisor](http://supervisord.org/) to run Celery in production, and then
  monitoring it over time.

* A [paster command](http://docs.ckan.org/en/latest/maintaining/paster.html)
  meant to be run as a cron job. The background job has to run on the same
  server as CKAN and has to be setup separately for each CKAN site.

* [CKAN Service Provider](https://github.com/ckan/ckan-service-provider) apps.
  These are quite heavy to implement and maintain, each app having its own user
  accounts and authorization, database, job status tracking, etc.


## Simple Install

Our approach minimizes both setup work for the user and implementation work for
the developer. It uses two parts:

1. A CKAN plugin
2. A simple, stateless Python script, designed to be run on the command-line or
   by cron, that provides link checking as a service

(The plan is to [turn the link checker into an actual web service](https://github.com/ckan/deadoralive/issues/1),
but for now a cron job is much simpler and gets us 90% of the way there.)

To install the CKAN plugin, you do:

```console
$ pip install ckanext-deadoralive
```

To install the link checker:

```console
$ pip install deadoralive
```

Then add a couple of settings to your CKAN config file and you're done, there's
no extra setup steps or non-Python dependencies. (See
the [README](https://github.com/ckan/ckanext-deadoralive#installation-and-usage) for full instructions.)

The link checker can be installed on the same machine that CKAN is on or on a
different machine. Since it does all its communication with CKAN over the API,
it doesn't matter. (You can even have the link checker running automatically on
the server, but also install it on your laptop and sometimes run it manually
from there.)


## Not just for CKAN

The link checker service is not CKAN specific.
Any site that implements the simple API that the service requires can use it
and receive link check results.
`ckanext-deadoralive` provides a reference implementation.

The plugin and service communicate with each other over HTTP, using this
protocol:

    Link checker service                                            Client site

    deadoralive                                                     ckanext-deadoralive
                    - Give me up to 50 resources to check ------->
                    <-------------------- [<id_1>, <id_2>, ... ] -  (Gets resource IDs from db)

                    - What's the URL for resource <id_1>? ------->
                    <---- The URL for resource <id_1> is <url_1> -  (Gets URL from db)
    (Checks <url_1>) - Resource <id_1>'s URL is broken ----------->  (Saves result)

                    - What's the URL for resource <id_2>? ------->
                    <---- The URL for resource <id_2> is <url_2> -  (Gets URL from db)
    (Checks <url_2>) - Resource <id_2>'s URL is working --------->  (Saves result)

                ...

`deadoralive` continues the loop of asking for the URL for the next resource
ID, checking the URL, then posting the result until it has checked all 50 URLs.

The next time `deadoralive` is run (either manually or by cron) it starts
all over again by asking for another 50 resources to check.

Once all of the site's resources have been checked, `deadoralive` will start
getting empty lists back when it asks for more resources to check. After 24
hours (configurable) `ckanext-deadoralive` will start handing out the
already-checked resources again to be re-checked.

`ckanext-deadoralive` then implements some logic on top of the link checker
results it has saved in the db: if a link has been checked and found to be
broken at least three times consecutively over a period of at least three days,
the link is marked as broken. Various broken link reports are added to CKAN
based on this.

`ckanext-deadoralive` is smart about which links it hands out to be checked next:

* Older unchecked resources are checked before newer ones.
* Checked resources are re-checked after 24 hours.
* Resources that haven't been checked in a long time are re-checked before ones
  that have been checked more recently.
* New resources are checked before re-checking old ones.

The link checker service is as dumb as possible: it just keeps asking for more
links and checking them.


## We'll Call You

When you think of a web service you probably think of something that provides
an API, and you write code that calls that API. Dead or Alive works the other
way round - you implement an API that it specifies, and it calls you. This
keeps everything much simpler. If we had the client site calling the service
rather than the other way round, then:

* The CKAN plugin would need to call the service hourly to have links be
  re-checked every hour. So we'd need some sort of task queue or scheduler on
  the CKAN end, adding setup.

* The CKAN plugin would need to know which link checker service it gave each
  link check task to (in our implementation CKAN doesn't need to know anything
  about the link checkers).

* The service would need to implement authentication (e.g. with user accounts
  and API keys) duplicating something that CKAN (or any client site using the
  service) already implements.

    When the service makes requests to CKAN it sends along a CKAN API key (you
    configure it with the API key of an authorized CKAN user), so it's just using
    CKAN's existing authorization code.


## Separate State and Asynchronousness

A key aspect of the design is keeping state and asynchronousness separate:

**All of the state is in the CKAN plugin**.
CKAN already provides a database that plugins can use without any extra setup
from the user, so we use the existing CKAN database for all storage. This keeps
the link checker service simple - no state, no storage, no database to setup.

**All of the asynchronousness and periodicity is in the service**.
Running tasks asynchronously or at periodic time intervals is what CKAN (or a
CKAN plugin) can't do without extra setup, so we avoid any asynchronous or
periodic work on the CKAN end.

**We keep the link checker service as simple as possible**.
It does the periodic and asynchronous tasks and nothing else. It leans on the
CKAN plugin for everything else.


## Failure Resistance not Task Statuses

**The protocol is resistant to service failures**.
CKAN just hands out a resource ID to be checked and expects to be called back
with the result. If it doesn't get a call back after a while, it will just
hand the resource ID out to another link checker request when one comes along.

We don't need task statuses.  There's no API for the client site to query the
status of a task (queued, running, succeeded, failed...), for example. To
implement that API we'd need a periodic task on the CKAN end to call the API
and get updates about the statuses of tasks. And on the service end we'd have
to store the statuses of tasks to be able to report them. That would break the
rule of keeping all the asynchronous and periodic stuff in the service, and all
the state in CKAN. It would complicate both ends.


## Distributed Task Processing

**The protocol supports distributed tasks**: a single client site can be
checked by multiple link checkers, and a single link checker can check multiple
sites.  Each link checker just needs to know about the site(s) it should check.
The sites don't need to know about the link checkers, and the link checkers
don't need to know about each other.

This video shows CKAN running in the top-left, and three link checker processes
running in the other three corners. Each process requests 50 links to check
from CKAN, and together they check 150 (giant gif warning):

<img src="{static}/images/deadoralive.gif" alt="Distributed link checking" title="Distributed link checking">

In this case all three link checker processes and CKAN are running on the same
machine. But it would work exactly the same if they were all on different
machines.

`ckanext-deadoralive` hands out different resource IDs to different
link checkers without needing to know how many link checkers there are or
needing to be able to distinguish one link checker from another.
Once it's handed out a resource ID to a link checker request and is expecting
a result back, it won't hand out that same resource ID to another request
until enough time passes that it decides a result probably isn't coming.
(And if it does end up getting two results back for the same link, this
doesn't do any harm.)

The link checker itself has no state, so there's no reason not to run more than
one of it.


Conclusion
----------

This approach should be applicable to all kinds of background services for
CKAN:

1. Implement an asynchronous and/or periodic task as a simple, standalone
   web service. Not CKAN-specific.
2. Implement a CKAN plugin to integrate CKAN sites with the service.
3. Put all the state in the CKAN plugin, and do all the asynchronous and
   periodic work in the service.
