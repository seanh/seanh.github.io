Title: The Open Knowledge Data Packager
Subheading: An open source web app for creating and publishing tabular data packages.
Tags: CKAN
Alias: /post/datapackager/

The Data Packager is a fun little project that
<a href="https://github.com/joetsoi">Joe Tsoi</a>,
<a href="https://whiteink.com/">Nick Stenning</a>,
and I worked on for a couple of months, with some extra design input from
<a href="http://www.mintcanary.com/">Sam Smith</a>. This is a re-post of the original
<a href="http://ckan.org/2014/06/09/the-open-knowledge-data-packager/">release announcement on the CKAN blog</a>.

[Data Packager](http://ckan.org/2014/06/09/the-open-knowledge-data-packager/)
is a web app for quickly creating and publishing
[Tabular Data Packages](http://dataprotocols.org/tabular-data-package/) from
collections of CSV files on your computer. You can
[register for a free user account](http://datapackager.okfn.org/user/register)
and start creating data packages now, or take a look at a
[sample data package](http://datapackager.okfn.org/package/my-first-tabular-data-package).

With Data Packager's simple interface you can create a data package, upload 
CSV files to it, enter some metadata, and get a web page where users can
explore and download your data package. When you login, you'll be taken to
your dashboard, where you'll see a list of any packages you've created so far
and an _Add package_ button:

<figure>
    <img src="{static}/images/datapackager-dashboard.png" alt="Screenshot of my Data Packager dashboard" title="Screenshot of my Data Packager dashboard">
    <figcaption>My Data Packager dashboard</figcaption>
</figure>

Click the _Add package_ button to create a new data package and you'll be taken
to a form where you can enter the title and other metadata for your package:

<figure>
    <img src="{static}/images/datapackager-create-package.png" alt="Screenshot of creating a data package" title="Screenshot of creating a data package">
    <figcaption>Creating a new data package</figcaption>
</figure>

Click on _Next: Add CSV files_ and you'll be taken to a form where you
can upload one or more CSV files to your data package:

<figure>
    <img src="{static}/images/datapackager-upload-csv.png" alt="Screenshot of uploading CSV files" title="Screenshot of uploading CSV files">
    <figcaption>Uploading CSV files to a new data package</figcaption>
</figure>

Finally, click on _Finish_ to create your data package. You'll be taken to your
data package's page:

<figure>
    <img src="{static}/images/datapackager-browse-package.png" alt="Screenshot of browsing a data package" title="Screenshot of browsing a data package">
    <figcaption>Browsing your newly created data package</figcaption>
</figure>

You can publish the URL of this page, or share it with anyone who you want to
share your data package with.

## Why Tabular Data Packages?

Tabular Data Packages (defined by the
[DataProtocols.org Tabular Data Package spec](http://dataprotocols.org/tabular-data-package/))
are a simple and easy-to-use data publishing and sharing format for the web.
A Tabular Data Package is
a collection of CSV files with a `datapackage.json` file.
The `datapackage.json` file contains metadata about the package (title of the
package, description, keywords, license, etc.) and schemas for each of the
package's CSV files.

The format is a good compromise between CSV and Excel, providing the simplicity
and ease-of-use of CSV with some of the expressivity of full-blown
spreadsheets.

The schemas for the CSV files use the
[JSON Table Schema](http://dataprotocols.org/json-table-schema/) format,
a simple format for tabular data schemas. It
includes metadata for each of the CSV file's columns (column name, type,
description, etc.) and optional primary and foreign keys for the file.


After you've created your data package and uploaded some CSV files to it,
Data Packager has a few nice features for you...


## Download Data Packages

The *Download Data Package* button on your data package's page will download
a ZIP file including all of your package's CSV files and the `datapackage.json`
file containing the metadata you entered for your package and files, plus schemas
for each of your files:

<img style="border: none;" src="{static}/images/datapackager-download.png" alt="Screenshot of Download Data Package button">

## Schema Browser

Data Packager automatically generates a JSON Table Schema for each CSV file
that you upload. The generated schema includes:

* **Column names** for each of the file's columns (taken from the CSV file's
  header row, if it has one)

* The **type** of the data in each column (string, number, date...), inferred
  from the values in the columns

* Some **descriptive statistics** calculated for numerical columns
  (minimum and maximum values, mean, standard deviation...)

* **Temporal extents** (earliest and latest dates) for date and time columns

By clicking on one of the CSV files on your data package's page, you can browse
the file's schema using the schema browser. Each file's page shows a preview
of the CSV file contents, and by clicking on the columns in the preview you
can inspect the schema for each column:

<figure>
    <img src="{static}/images/datapackager-schema-browser.gif" alt="Screenshot of the schema browser" title="Screenshot of the schema browser">
    <figcaption>The schema browser<figcaption>
</figure>

## Schema Editor

By clicking the *Edit* button on one of your CSV file's pages, you can edit the
file's JSON Table Schema and add your own custom attributes.
Data Packager validates all the changes that you make and gives helpful error
messages if you try to save an invalid schema.

<figure>
    <img src="{static}/images/datapackager-schema-editor.gif" alt="Screenshot of the schema editor" title="Screenshot of the schema editor">
    <figcaption>The schema editor</figcaption>
</figure>

## Primary and Foreign Keys

If you add primary and foreign keys to a CSV file's schema, they'll also be
shown on the file's page.

<figure>
    <img src="{static}/images/datapackager-keys.png" alt="Screenshot of primary and foreign keys" title="Screenshot of primary and foreign keys">
    <figcaption>Primary and foreign keys</figcaption>
</figure>

## API

All of Data Packager's features can also be used via its
[JSON API](http://datapackager.okfn.org/api).


## Open Source

Data Packager is 100% open source. You can:

* Deploy your own Data Packager site - just
  [follow our instructions](https://github.com/okfn/datapackager) to install
  Data Packager on an Ubuntu server

* Contribute to the [Data Packager source code on GitHub](https://github.com/ckan/ckanext-datapackager) - send us a pull request!

* Report bugs using our [issue tracker](https://github.com/ckan/ckanext-datapackager/issues)


## Built with CKAN

Data Packager is built using [CKAN](http://ckan.org/), the highly-customisable
open source data portal platform. All Data Packager features are implemented
by a CKAN extension,
[ckanext-datapackager](https://github.com/ckan/ckanext-datapackager).
