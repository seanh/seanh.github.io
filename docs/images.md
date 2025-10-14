How to add images
=================

1. Add the image file to the [`content/images/`](https://github.com/seanh/seanh.github.io/tree/main/content/images) folder.
   I mostly don't bother to sort image files within this folder.

2. Add the image to a page or blog post by using `{static}/images/foo.png` as the URL.

   You can either use an HTML `<img>` tag:

   ```html
   <img src="{static}/images/foo.png" alt="Alt text for the image" title=Title text for the image">
   ```

   Or you can use Markdown:

   ```markdown
   ![Alt text for the image]({static}/images/foo.png "Title text for the image")
   ```
