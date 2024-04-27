Title: PDF Fingerprinting
Subheading: How to uniquely identify a PDF file, independent of the path or URL the file is currently at, and even after the file has been edited, using PDF.js's &ldquo;fingerprint&rdquo; algorithm in JavaScript or Python.
tags: Hypothesis

[The Hypothesis web annotation client](https://hypothes.is/) uses PDF
fingerprints to identify PDFs independent of their URLs. Hypothesis
knows when it's looking at the same PDF, even if that PDF appears at two
different URLs, or appears as a local file on your computer and then later
online, and even if the file has been edited and then re-uploaded.
This enables a "magic" Hypothesis feature where, for example, you can annotate
a local PDF file on your computer and then later publish that file online and
[Hypothesis will still find your annotations of the file when you view it online](https://web.hypothes.is/blog/synchronizing-annotations-between-local-and-remote-pdfs/).

Hypothesis knows that it's looking at the same PDF because it looks at the
PDF's fingerprint. Computing the fingerprint of a PDF turns out to be a simple
algorithm, implemented by PDF.js, based on top of standard identifiers that
PDFs contain.

This post explains what PDF file identifiers and fingerprints are, and
re-implements the PDF.js fingerprint algorithm in Python.

## PDF file identifiers

PDFs can contain **file identifiers** that are intended to be used to allow one
PDF to contain a filename-independent link to another PDF, although
applications may also use them to identify files for other purposes.

A file identifier looks something like this, inside the PDF file:

```
/ID [<6426256F1EF8F6A9CC257A60F3D3BA57> <27efe497bd0ec74687a46771aa54f25b>]
```

Some variation on the format is possible.

Section 14.4 of
[the PDF spec](www.adobe.com/content/dam/Adobe/en/devnet/acrobat/pdfs/PDF32000_2008.pdf)
(this is ISO 32000-1, the PDF 1.7 spec, there's now a newer
[ISO 32000-2 PDF 2.0 spec](https://www.iso.org/standard/63534.html) but you
have to pay to download it) describes PDF file identifiers as an
"**optional ID entry in the PDF file's trailer dictionary**."

(The **trailer** of a PDF is a dictionary at the end of the file that PDF
readers use to find certain parts of the file, see section 7.5.5 in ISO 32000-1.)

The ID entry is an **array of two byte strings**.
The first byte string in the array is a "**permanent identifier**" that's
"based on the contents of the file at the time it was originally created" and
"shall not change when the file is incrementally updated".
This is the identifier that we're interested in.

The second byte string is a secondary identifier that should also be based on
the contents of the file, and should initially have the same value as the first
identifier, but that should be re-computed based on the new file contents each
time the file is updated. It enables you to identify a different version of the
same file. Hypothesis doesn't use this second identifier.

Section 14.4 of ISO 32000-1 goes on to say that file identifiers "should be
computed by means of a message digest algorithm such as MD5" using the current
time, the file's pathname, the size of the file in bytes, and the contents of
the file.  There's of course no guarantee that every program that creates PDFs
computes the IDs in this way.

**PDF identifiers aren't guaranteed to be unique**. The spec emphasises that
the algorithm a program uses to generate IDs should ensure that they're
"likely to be unique" but nothing guarantees this.

**Not all valid PDFs contain a file identifier**. The spec says
"The ID entry is optional but should be used."

In practice most but not all PDFs do contain an ID. Of 3594 real-world PDFs that
I tested below, 5% had no file identifier.

## PDF.js's PDF "fingerprints"

[PDF.js](https://mozilla.github.io/pdf.js/), the JavaScript PDF viewer that
Hypothesis uses, provides access to a fingerprint for any PDF based on PDF file
identifiers and MD5 message digests.
This fingerprint is what Hypothesis actually uses to identify PDFs independent
of their URLs and make annotations magically follow their PDFs from one
location to another.

The fingerprint for a PDF is computed by
[PDF.js's `fingerprint()` function](https://github.com/mozilla/pdf.js/blob/3ed2290c5b9c72b80f9a7335f41351cd949d9712/src/core/document.js#L594-L616).
What this `fingerprint()` function does is:

1. Extract the file identifier from the PDF's trailer, if it has one
2. If the ID can't be extracted (because the PDF doesn't contain a trailer,
   the trailer doesn't contain a valid ID array, etc) then use an MD5 digest
   of the first 1024 bytes of the file instead
3. Either way, convert the bytes of the ID or digest to a hex string and that's
   your fingerprint

This turns out to be a pretty nice fingerprint algorithm:

* It's simple and easy to implement and to understand.

* It knows when it's looking at a modified version of the same file, because
  it uses the file identifier from the PDF whenever one is available.
  
    You can fingerprint any file, PDF or not, by just computing something like an
    MD5 digest of the file's contents. But a digest will change if the file's
    contents change, failing to identify a file as a modified version of an
    earlier file.

    PDF file identifiers work better than simple digests because, assuming the
    tool that's used to create and edit the PDF follows the PDF spec, the
    identifier doesn't change when the file is modified.

* It's robust, able to produce a fingerprint for _any_ PDF, because it falls
  back on an MD5 digest if the PDF doesn't contain an identifier.

    The fingerprint of a PDF without an identifier _may_ change when the PDF is
    edited, failing to identify a modified version of the same file, but it's
    better than nothing for the 5% of files that don't have an identifier.

* It's performant because it avoids reading the entire PDF.

    PDFs can be large and reading and parsing an entire large PDF could use a lot
    of time and memory.

    PDF file identifiers are located in the PDFs trailer, which is at the very
    end of the file. By reading from the end of the file backwards a PDF parser
    can extract the fingerprint without reading the entire file.

    When the file turns out not to have an identifier the algorithm computes a
    digest of the first 1024 bytes, not the entire file. This is a good tradeoff -
    it avoids reading in the entire file but is still likely to be unique.

* It's printable and readable because it turns the file identifier or digest
  into a nice, all-ASCII-characters hex string.

This fingerprint is described by PDF.js's API docs as
["A unique ID to identify a PDF. Not guaranteed to be unique."](https://github.com/mozilla/pdf.js/blob/3ed2290c5b9c72b80f9a7335f41351cd949d9712/src/display/api.js#L507-L508)
It's possible for two different PDFs to contain the same identifier,
or for two PDFs without identifiers to contain the same first 1024 bytes.
But in practice the fingerprint is likely to be unique almost always.


## PDF fingerprinting in Python

At Hypothesis we thought we had a need to compute these PDF.js fingerprints
server-side. We got this to work but didn't actually end up using it. It might be
useful to record what we did anyway.

It's possible to [run PDF.js server-side using Node](https://github.com/mozilla/pdf.js/tree/master/examples/node)
and get the fingerprints from it. But we didn't want to do that. We have a
Python web app, and it'd be easier if we could do the fingerprinting in Python.

**The challenge was to implement a Python PDF fingerprinter that would produce
the same fingerprints as PDF.js does for almost any PDF file**.
Failing to parse a small portion of PDFs and erroring out on those files would
be acceptable, even if PDF.js _could_ parse them.
What I really wanted to avoid was _successfully producing a fingerprint that
didn't match PDF.js's fingerprint_ for the same file. This could lead to silent
failures and incorrect behaviour only noticed too late, in a system that
depended on the Python fingerprinter's results matching PDF.js's.

This turns out to be doable but tricky.

### Python PDF parsers

While the fingerprint algorithm itself is pretty straightforward, it sits on
top of a PDF parser that's needed to extract the file identifier byte string
or to decide that the file doesn't contain an identifier.
Any differences between the Python PDF parser and PDF.js's parser could result in
different fingerprints being produced.

Not wanting to write my own PDF parser I went looking for Python libraries.
I ran into problems with both [PyPDF2](https://github.com/mstamy2/PyPDF2)
and [pdfrw](https://github.com/pmaupin/pdfrw).
They'd return a different file ID than PDF.js for a lot of PDFs,
either by doing unwanted interpretation of the file ID's bytes, or parsing the
PDF incorrectly, etc.

I had better luck using [PDFMiner](https://github.com/euske/pdfminer),
with which I was able to extract the same ID as PDF.js for almost all PDFs that
I tested. The PDFs that failed were ones that PDFMiner failed to parse
entirely and crashed. Unlike with PyPDF2 and pdfrw, whenever PDFMiner _did_
extract an ID it would always be the same as PDF.js's.

### PDF fingerprinting in Python using PDFMiner

Here's a Python script, `fingerprint.py`, that prints out the fingerprint of a
given PDF, using PDFMiner:

```python2
#!/usr/bin/env python2
"""
Print out the fingerprint of the given PDF file.

Exit with non-zero status code if fingerprinting the file fails.

Installation:

1. Create a new Python virtual environment

2. Install PDFMiner from git (because the version on PyPI is out of date and
   missing AES v2 decryption support):

   pip install git+https://github.com/euske/pdfminer.git

Usage:

    ./fingerprint.py /path/to/file.pdf

"""
import hashlib
import sys

import pdfminer.pdfparser
import pdfminer.pdfdocument


def hexify(byte_string):
    ba = bytearray(byte_string)

    def byte_to_hex(b):
        hex_string = hex(b)

        if hex_string.startswith('0x'):
            hex_string = hex_string[2:]

        if len(hex_string) == 1:
            hex_string = '0' + hex_string

        return hex_string

    return ''.join([byte_to_hex(b) for b in ba])


def hash_of_first_kilobyte(path):
    f = open(path, 'rb')
    h = hashlib.md5()
    h.update(f.read(1024))
    return h.hexdigest()


def file_id_from(path):
    """
    Return the PDF file identifier from the given file as a hex string.

    Returns None if the document doesn't contain a file identifier.

    """
    parser = pdfminer.pdfparser.PDFParser(open(path, 'rb'))
    document = pdfminer.pdfdocument.PDFDocument(parser)

    for xref in document.xrefs:
        if xref.trailer:
            trailer = xref.trailer

            try:
                id_array = trailer["ID"]
            except KeyError:
                continue

            # Resolve indirect object references.
            try:
                id_array = id_array.resolve()
            except AttributeError:
                pass

            try:
                file_id = id_array[0]
            except TypeError:
                continue

            return hexify(file_id)


def fingerprint(path):
    return file_id_from(path) or hash_of_first_kilobyte(path)


if __name__ == '__main__':
    print fingerprint(sys.argv[1])
```

A few notes about this code:

1. You'll notice the install instructions at the top of the file say to install
   PDFMiner from GitHub instead of from PyPI. The version on PyPI is very out
   of date, and lacks support for AES v2 encryption which a lot of PDF files
   use.

1. The `hexify()` function is turning the file ID byte string
   into a hexadecimal string using Python's built in `hex()` function, but then
   it has to do a little work of its own (removing `0x` from the start of
   some hex characters, appending `0` to the beginning of some) to make the
   output match PDF.js's hex strings.

1. When the file doesn't contain an ID we don't need to pass the MD5 digest
   through `hexify()` (as PDF.js does) because Python's `hexdigest()` function
   returns a hexadecimal digest directly.

1. The `file_id_from(path)` function is finding the file ID using PDFMiner by
   looping over all "xref"s in the PDF, looking for the first xref that
   contains a trailer that contains a non-empty ID array.

     One tricky thing here is the `id_array = id_array.resolve()` call.
     This resolves PDF "indirect references" (see ISO 3200-1 section 7.3.10).
     Any object in a PDF file, including the file ID array in the trailer,
     can be an "indirect object" which is just an identifier that the PDF reader
     has to use to look up the actual document elsewhere in the file.
     In some PDF files the file ID array is an indirect object, and PDFMiner's
     `resolve()` does the lookup for us.

### Testing the fingerprinter

I used a couple of scripts to test the above code, comparing its fingerprints
to those of PDF.js, using 3594 public PDFs that have been annotated by
Hypothesis users. Of the 3594 PDFs tested:

* The Python fingerprinter produced the same fingerprint as PDF.js for
  **3590** files (99.9%)
* The Python fingerprinter crashed on **4** files for which PDF.js _did_
  successfully produce a fingerprint
* **0** mismatching fingerprints were produced

The comparison of the fingerprinting algorithms was done using a couple of
command line scripts that you can find over in [my fork of PDF.js](https://github.com/mozilla/pdf.js/compare/master...seanh:fingerprint).

First, here's a Node.js script, `fingerprint.js`, that prints out the PDF.js
fingerprint of a given PDF:

```javascript
#!/usr/bin/env node
/**
 *
 * Print out the fingerprint of the given PDF file.
 *
 * Exit with non-zero status code if fingerprinting the file fails.
 *
 * Installation:
 *
 *   git clone git@github.com:seanh/pdf.js.git
 *   cd pdf.js
 *   git checkout fingerprint
 *   npm install
 *   npm install estraverse
 *   gulp dist-install
 *
 * Usage:
 *
 *   ./fingerprint.js /path/to/file.pdf
 *
 */
let pdfjs = require('pdfjs-dist');
let pdf = process.argv[2];

pdfjs.getDocument(pdf).then((doc) => {
  console.log(doc.fingerprint);
}).catch((error) => {
  process.exit(1);
});
```

Now here's a Python script, `compare-fingerprints`, that takes one or more PDF
files as command-line arguments, runs both `fingerprint.py` and
`fingerprint.js` on each file, and prints out which fingerprints match and
which don't. For example to compare results for an entire directory of PDFs,
run: `./compare-fingerprints my_files/*.pdf`.

```python2
#!/usr/bin/env python2
"""
Compare fingerprints from fingerprint.js and fingerprint.py.

Installation:

1. git clone git@github.com:seanh/pdf.js.git
2. cd pdf.js
3. git checkout fingerprint
4. npm install
5. npm install estraverse
6. gulp dist-install
7. Create a new Python virtual environment
8. Install PDFMiner from git (because the version on PyPI is out of date and
   missing AES v2 decryption support):

     pip install git+https://github.com/euske/pdfminer.git

Usage:

    ./compare-fingerprints files_to_compare/*.pdf

"""
import subprocess
import sys


for pdf in sys.argv[1:]:

    # Get the fingerprint from PDF.js.
    try:
        js_fingerprint = subprocess.check_output(['./fingerprint.js', pdf])
    except subprocess.CalledProcessError:
        # Skip files that PDF.js can't parse.
        continue

    # Get the fingerprint from Python.
    try:
        py_fingerprint = subprocess.check_output(['./fingerprint.py', pdf])
    except subprocess.CalledProcessError:
        print "Fail: " + pdf
        continue

    matches = js_fingerprint == py_fingerprint

    # Strip newlines before printing.
    js_fingerprint = js_fingerprint.strip()
    py_fingerprint = py_fingerprint.strip()

    if matches:
        print "Match: " + js_fingerprint
    else:
        print "Mismatch. File: " + pdf + " PDF.js: " + js_fingerprint + " Python: " + py_fingerprint
```

## Conclusion

It turns out _not_ to be the case that "all PDFs contains a unique fingerprint".
PDF fingerprints are actually just a function implemented in PDF.js, one
particular PDF reader.
They're based on standard identifiers that PDF files _do_ contain, but these
identifiers aren't _guaranteed_ to be unique and not _every_ valid PDF contains
one. When a PDF doesn't contain an identifier the fingerprint function falls
back on a digest of the first part of the file, which is also not _guaranteed_
to be unique.

Changes to PDF.js's fingerprint code over time may also be a concern to
Hypothesis, given that we store the fingerprints from this function in our
database and rely on them being stable.

In practice, though, these pseudo-unique fingerprints can be robustly computed
for almost any PDF file and aren't likely to have collisions.
Separate implementations of the fingerprint algorithm in different languages
turn out to be possible, with very high agreement in the results.
