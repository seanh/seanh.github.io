Title: A Broken Link Checker Plugin for CKAN
Subheading: Check your CKAN site for broken links and produce a report.
Tags: CKAN
Alias: /post/ckanext-deadoralive/

[ckanext-deadoralive](https://github.com/ckan/ckanext-deadoralive) is a new
broken link checking plugin for [CKAN](http://ckan.org/). It checks your CKAN
site's resources for broken links and adds broken link reports to the site.

Many open data catalog sites have large numbers of datasets which link to
resource files hosted on other sites. These datasets may be created by many
different staff members (members of different government departments, for
example).  The datasets may even be automatically imported (harvested) from
other sites.

With so many links maintaining dataset quality is difficult.
A service is needed to automatically find broken links and enable dataset
maintainers to see at a glance which links need to be fixed, and site admins to
see which maintainers are responsible for datasets with broken links.

The Dead or Alive extension runs a background link checker service that checks
and re-checks all of a site's datasets for broken links every 24 hours.

A resource is marked as broken if at least three consecutive link checks over a
period of at least three days (configurable) have found its URL broken.
A public report is added to the resource's page detailing the results:

<figure>
    <img src="{static}/images/broken_resource.png" alt="Screenshot of a broken resource report" title="Screenshot of a broken resource report">
    <figcaption>A broken resource report, from a resource's public page. The details should help the data file's maintainers fix the problem. We also add a positive confirmation to working resource's pages.</figcaption>
</figure>

There's also a public report of all broken links on the site. Broken links are
grouped by data publishing organization, with the organizations with the most
broken links first. Hopefully highlighting which publishing organizations have
the most broken links will encourage them to fix the problems:

<figure>
    <img src="{static}/images/broken_links_by_organization.png" alt="Screenshot of the broken links by organization report" title="Screenshot of the broken links by organization report">
    <figcaption>The site-wide broken links report.</figcaption>
</figure>

Finally, there's a private broken links report viewable by site admins only.
This report groups the broken links by the email address of the maintainer or
author responsible for the dataset. The aim is to make it as easy as possible
for site admins to email dataset maintainers about their broken links:

<figure>
    <img src="{static}/images/broken_links_by_email.png" alt="Screenshot of the broken links by email report" title="Screenshot of the broken links by email report">
    <figcaption>The private broken links report.</figcaption>
</figure>

The _Email maintainer_ buttons open a new email in your email client with the
address, subject and body already filled out for you (on the production site
the email would be in Swedish, of course):

    From: Sean Hammond <seanh@oppnadata.se>
    To: mäintainër_2@authors.com
    Subject: You have 3 datasets with broken links on Oppnadata.se

    These datasets have broken links:

    Org 0 dätaßët 2
    http://oppnadata.se/dataset/org_0_dataset_2

    Org 0 dätaßët 1
    http://oppnadata.se/dataset/org_0_dataset_1

    Org 1 dätaßët 3
    http://oppnadata.se/dataset/org_1_dataset_3

    -- 
    Sean Hammond
    Site Administrator, http://oppnadata.se

We aimed to make this plugin as simple and easy as possible to install and
maintain. See the [README](https://github.com/ckan/ckanext-deadoralive)
for instructions.

The link checker service isn't just for CKAN sites, it works with any site that
implements its [simple API](https://github.com/ckan/deadoralive#api).

Features we'd like to add in the future include:

* Check new and updated resource links as soon as they're added to the site
  (not just hourly).

* Buttons on the site for admins to request an immediate re-check of a
  resource's, dataset's, or the entire site's links.

* A manual override, allowing sysadmins to mark a link as working or as broken
  even if the link checker thinks otherwise.

To contribute get the source from [github.com/ckan/ckanext-deadoralive](https://github.com/ckan/ckanext-deadoralive)
and send a pull request.

For details about how Dead or Alive works and why it was designed the way it
was, see [Background Tasks as Simple Web Services](/posts/background-tasks-as-simple-web-services).
