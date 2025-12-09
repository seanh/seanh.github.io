Title: The Network as the Database
Subheading: Store work-in-progress user data in the network, instead of in your database.
Tags: CKAN
Alias: /post/the-network-as-the-database/

[Data Packager](/posts/datapackager/)'s schema editor uses a simple technique
that was really helpful with implementing the editing interface.  The editor's
task is to let the user edit metadata associated with the columns of a tabular
data file. The interface shows a preview of the data file and each of its
columns. At any time one column is selected, and the metadata editor form on
the left-hand-side shows the metadata for that column. Clicking on any of the
other columns changes to editing the metadata for that column:

<figure>
    <img src="{static}/images/datapackager-schema-editor.gif" alt="Screenshot of the schema editor" title="Screenshot of the schema editor">
    <figcaption>The schema editor</figcaption>
</figure>

It was a requirement that this interface be usable without JavaScript, so each
time you click on one of those columns it's actually submitting the form and
reloading the whole page.

The challenge here is that if the user edits the metadata of one column, then
goes to another column, then goes back to the first column, the changes they
made to the first column should still be there. But the changes haven't been
saved yet, the user hasn't clicked the *Save* button and they could still
bail out and not save their edits. When they do click *Save* it
should save the metadata for all the columns, not just the one that's currently
showing.

At first glance this looks like a pain to implement. We need to keep a draft
version of the metadata in the database and keep updating it whenever the user
changes columns. When they finally hit *Save* we need to overwrite the real
version of the data with the draft. Lots of complicated logic in the view
controller, and we could end up with abandoned drafts lying around in the db.

This is where *the network as the database* comes in:
instead of storing the draft data in the database server-side,
you store it in the HTML form itself. When you're looking at the schema editor
form above, showing the form fields for the selected column, the form actually
contains hidden form fields for all the unselected columns as well.
Each time you change columns you submit the form, the server captures your
submitted form data and reflects it back to you in hidden form fields when it
re-renders the form with the new column selected.

Server-side, you just need three simple functions:

1. Take a convenient, internal representation of all the data file's columns
   and their metadata (from the database) and render it as an HTML form.

2. When the user clicks on a column take the HTML form submitted by the user
   and parse it, turning the submitted form data back into its convenient
   internal representation.

3. Take that internal representation and actually save it to the database.

You just keep repeating 1 and 2, and finally do 3 when they hit *Save*.
Nothing is written to the database until 3 happens.

There are a few more details, but not much. In step 1 you need a little logic
to decide which column to render as the selected column each time, and you need
to render the metadata for all the other columns as hidden form fields.  In 2
you have to validate the submitted form data and send any warnings or
validation errors to 1 to be shown to the user.

Validation errors present a user interaction problem. Any errors are shown next
to the form fields themselves. When they hit *Save* the server may
find problems with the metadata fields on any of the columns, but the interface
only shows the fields for the selected column. How to present the errors to the user?

<figure>
    <img style="border: none;" src="{static}/images/datapackager-validation-error.png" alt="Screenshot showing a validation error" title="Screenshot showing a validation error">
    <figcaption>A validation error</figcaption>
</figure>

The solution we went with was to validate the data whenever the user changes
columns as well as when they hit *Save*, and don't let them change to a new
column as long as the current column has any validation errors. The page will
re-render still showing the same column, with the error messages in the form.

What it actually does if there are any validation errors is to render the form
showing *the first column that has any errors*. If somehow there are errors in
multiple columns this will work just fine, although the user will have to
submit the form multiple times to correct each column.
But by validating on each column
change, that should never happen anyway. The logic for deciding which column to
render as selected is:

1. Choose the first column that has any validation errors, or
2. Choose the column that the user just clicked on, or
3. Choose the first column (this happens the first time the form is rendered)

I think the *network as the database* technique would be a nice one to use for
any multi-form editing interface, whether it involves jumping between different
"pages" like the schema editor, or going through multiple sequential steps
(maybe with the option to jump back to previous steps), etc. It does have the
disadvantage that if the user's browser crashes or if they accidentally close
the tab, they may lose their work in progress if their browser doesn't save it
for them. Nothing is saved server-side until the final step. But it's a simple
technique that makes it easy to write pleasing interfaces without many logic
bugs or edge cases.

Googling _the network as the database_ brings up an interesting
[blog post from Armin Ronacher](http://lucumr.pocoo.org/2013/11/17/my-favorite-database/)
about using similar techniques to store sensitive things like access tokens.
