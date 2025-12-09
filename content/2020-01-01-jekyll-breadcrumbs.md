Title: Breadcrumbs in Jekyll
Tags: Jekyll
Subheading: GitHub Pages-compatible breadcrumbs for Jekyll.

Breadcrumbs help users locate themselves within the hierarchy of your site.
While your site's header might have some links that act as the site's primary
navigation, breadcrumbs show the user exactly where they currently are. They
show the path from the home page down to the current page and provide links for
moving back up the site hierarchy.

[Jekyll](https://jekyllrb.com/) doesn't have any built-in support for rendering
breadcrumbs for a page or post and implementing them can be tricky because
[GitHub Pages](https://pages.github.com/) doesn't let you install plugins
(it only supports a [small list of Jekyll plugins](https://help.github.com/en/github/working-with-github-pages/about-github-pages-and-jekyll#plugins)),
so you can't use the [jekyll-breadcrumbs](https://github.com/git-no/jekyll-breadcrumbs) plugin on GitHub Pages.

I decided not to use them on my own site in the end, but the GitHub Gist below provides
a couple of Jekyll template includes that implement GitHub-compatible page and
post breadcrumbs.

The breadcrumbs look something like this:

<p>
  <a>Home</a>
  &gt;
  <a>Posts</a>
  &gt;
  <a>Example Category</a>
  &gt;
  <a>2019</a>
  &gt;
  <a>Dec</a>
  &gt;
  <a>23</a>
  &gt;
  <strong>Breadcrumbs in Jekyll</strong>
</p>

The breadcrumbs are made up of:

1. A breadcrumb for the site's front page: **Home** in the example breadcrumbs above
2. A breadcrumb for the page or post's collection, if it has one: **> Posts** in the example breadcrumbs above
   (posts belong to the collection "posts" by default)
3. One breadcrumb for each of the page or post's categories, if it has any:
   **> Example Category** in the example breadcrumbs above
4. For posts: breadcrumbs for the post's year, month and day: **> 2019 > Dec > 23** in the example breadcrumbs above
5. Finally, a breadcrumb for the page or post's title: **> Breadcrumbs in Jekyll** in the example breadcrumbs above

There are options for omitting each of the home, collection, categories, date
and title components, so you can customize the breadcrumbs to look how you
want. See the Gist's [README](https://gist.github.com/seanh/500f8fd75cf0a6da298b6b1a9006f22a#file-readme-md)
for docs.

Creating pages for breadcrumbs to link to
-----------------------------------------

Breadcrumbs will automatically find and link to their corresponding pages if they exist:

* If the site has a front page then the **Home** breadcrumb will be a link to the front page

* If there's a page whose URL matches the page or post's collection, the collection breadcrumb will be a link to that page.

    For example to create a page for the default "posts" collection create a `posts.md` or `posts/index.md` file.
    You might use this page to render a list of all your posts.

    The collection page's URL must be equal to the name of the collection with spaces replaced by `-`'s and uppercase letters downcased.
    For example a `Foo Bar` collection would match a page with a `/foo-bar/` URL.

* For each category, if there's a page whose URL matches the category's name then the category's breadcrumb will be a link to that page.

    For example to create a page for "Example Category" create a `example-category.md` or `example-category/index.md` file
    (as with collection pages: replacing spaces with `-`'s and downcasing uppercase letters).

    You might use this page to list all posts in the category.

    <aside markdown="1">
    When creating category pages it's important to understand that
    [categories in Jekyll aren't hierarchical](https://www.seanh.cc/jekyll-theme-oatcake/programming/web-design/bar/2019/12/24/categories-and-tags/#categories-arent-hierarchical).
    </aside>

* For a post's year, month and day, if there's a page whose URL matches that
  year, month, or day, then the year, month or day breadcrumb will link to it.

    For example the breadcrumb for the year 2019 will match a `2019.md` or `2019/index.md` file.
    You could use this page to list all posts from 2019.

    December 2019 matches a `2019/12.md` or `2019/12/index.md` file,
    and 23rd December 2019 matches a `2019/12/23.md` or `2019/12/23/index.md` file.

Controlling breadcrumb text
---------------------------

Whenever a breadcrumb finds a corresponding page to link to, it also takes on that page's title as the breadcrumb text.

For example if the `example-category.md` page has the title "All Posts in
Example Category" then "All Posts in Example Category" will appear as the
breadcrumb text for the category, in the breadcrumbs of posts that belong to
the category.

Or if `posts.md` has the title "Archive" then the post's collection will appear
as "Archive" in the breadcrumbs of posts belonging to that collection.

The title of the front page of the site (the top-level `index.md` file)
controls the text of the Home breadcrumb.

You can override this for any page by adding a `breadcrumb_text` variable to the page's frontmatter:

```yaml
---
breadcrumb_text: Example Category
---

All Posts in Example Category
=============================

...
```

Making breadcrumbs match URLs
-----------------------------

You might want your breadcrumbs to match the `/`-separated parts of your permalink URLs.
You can achieve this either by changing your [`permalink` setting](https://jekyllrb.com/docs/permalinks/)
in `_config.yml` to match the default breadcrumbs or by configuring the
breadcrumbs to match your `permalink` setting.

For example this permalink setting:

```yaml
permalink: /:collection/:categories/:year/:month/:day/:title/
```

will make your permalink URLs match the default breadcrumbs.

Another example: if you use the built-in `permalink: pretty` format then adding
then passing `omit_collection=true`to the include will change your breadcrumbs to match
your pretty permalinks:

```liquid
{% include breadcrumbs.html omit_collection=true %}
```

Limitations
-----------

* Although you can turn the different breadcrumb components on and off, you
  can't change their order. Categories must always come before dates in
  breadcrumbs, for example. The order matches the order of the components
  in [Jekyll's built-in permalink formats](https://jekyllrb.com/docs/permalinks/#built-in-formats).

* Page subdirs don't appear in breadcrumbs.

    If you put a post in a subdir or subdirs (for example: `foo/bar/_posts/`
    instead of the top-level `_posts/` dir) then Jekyll will add `foo` and `bar`
    to the post's categories in that order and <samp>> foo > bar ></samp> will
    appear in the post's breadcrumbs (as long as you haven't set
    `omit_categories: true`)

    But this doesn't work for pages. A `foo/bar/gar.md` page doesn't get `foo`
    and `bar` categories and its breadcrumbs will be just <samp>Home > PAGE_TITLE</samp>.

    This could probably be fixed quite easily: `page.dir | split: "/"` should give you
    a list of the subdirs, which you can then use to create breadcrumbs for each.
    You'd only want to do this for pages though, not posts.

The Gist
--------

Here's [the gist](https://gist.github.com/seanh/500f8fd75cf0a6da298b6b1a9006f22a),
with the breadcrumbs templates and installation and usage docs:

<script src="https://gist.github.com/500f8fd75cf0a6da298b6b1a9006f22a.js"></script>
