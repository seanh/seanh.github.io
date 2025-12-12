AUTHOR = "Sean Hammond"
DEFAULT_DATE_FORMAT = "%b %Y"
DEFAULT_PAGINATION = 10
DELETE_OUTPUT_DIRECTORY = True
GITHUB_URL = "https://github.com/seanh/"
OUTPUT_SOURCES = True
OUTPUT_SOURCES_EXTENSION = ".txt"
PATH = "content"
SITENAME = "seanh.cc"
SITEURL = "http://localhost:8000"
STATIC_PATHS = ["images", "videos", "dissertation.pdf", "ThesisChapter5.pdf", "open-data-licensing-and-ckan.pdf"]
THEME = "../sidecar"
TYPOGRIFY = True
TYPOGRIFY_DASHES = "oldschool"
SIDECAR_PYGMENTS_BORDERLESS = True

PLUGINS = ["pelican_alias"]

DIRECT_TEMPLATES = ["index", "authors", "categories", "tags", "archives", "drafts", "hidden"]
THEME_TEMPLATES_OVERRIDES = ["templates"]

AVATAR_URL = "{SITEURL}/images/avatar/avatar_cropped_360.jpeg"
SITESUBTITLE = "I blog, you blog, weblog."
SITEBIO = '''
    Hi 👋, I'm Sean:
    a software developer and future Portuguese Water Dog owner living in
    <s>Ottawa</s>, <s>Berlin</s>, <s>Edinburgh</s>, Leith.
    <a rel="author" href="{SITEURL}/about/">I'm currently looking for work.</a>
'''

SIDECAR_NAVBAR = [
    "HOME",
    "SPACE",
    "ARCHIVES",
    '<a rel="author" href="{SITEURL}/about/">About</a>',
    '<a href="{SITEURL}/projects/">Projects</a>',
    "GITHUB",
]

SIDECAR_ARTICLE_TAGLINE_ITEMS = ["TIME"]
SIDECAR_PAGE_TAGLINE_ITEMS = ["TIME"]
SIDECAR_PAGE_FOOTER_ITEMS = []

# Get both the date and the slug (not just the date) from page and post filenames.
FILENAME_METADATA = r'^(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)$'
SLUGIFY_SOURCE = 'basename'

# Configure Python-Markdown.
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {
            'css_class': 'highlight',
            'linenums': False,
            'guess_lang': False,
        },
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}

# Support markdown in the `summary`, `subheading`, and `subtitle` page/article metadata fields.
FORMATTED_FIELDS = ['summary', 'subheading', 'subtitle']

# Make the URLs of article permalink pages nicer.
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SOURCE_URL = "{article.url}index{OUTPUT_SOURCES_EXTENSION}"

# Make draft articles have the same URLs as they will have once published.
DRAFT_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
DRAFT_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'

# Make the URLs of static pages nicer.
PAGE_SAVE_AS = '{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SOURCE_URL = "{page.url}index{OUTPUT_SOURCES_EXTENSION}"

# Make draft pages have the same URLs as they will have once published.
DRAFT_PAGE_SAVE_AS = '{slug}/index.html'
DRAFT_PAGE_URL = '{slug}/'

# Make the URLs of tag pages nicer.
TAGS_SAVE_AS = "tags/index.html"
TAG_SAVE_AS = "tag/{slug}/index.html"
TAG_URL = "tag/{slug}/"

# Make the URL of the drafts page nicer.
DRAFTS_SAVE_AS = "drafts/index.html"

# Make the URL of the hidden articles page nicer.
HIDDEN_SAVE_AS = "hidden/index.html"

# Make the URL of the archives page nicer.
ARCHIVES_SAVE_AS = "archives/index.html"
ARCHIVES_URL = "/archives/"

# Make the URLs of category pages nicer.
CATEGORIES_SAVE_AS = "categories/index.html"
CATEGORY_SAVE_AS = "categories/{slug}/index.html"
CATEGORY_URL = "categories/{slug}/"

# Make pagination URLs nicer.
PAGINATION_PATTERNS = (
    (1, "{base_name}", "{save_as}"),
    (2, "{base_name}/page/{number}/", "{base_name}/page/{number}/index.html"),
)

# Disable the author pages.
AUTHORS_SAVE_AS = "" # "authors/index.html"
AUTHOR_SAVE_AS = "" # "authors/{slug}/index.html"

# Make author links go to the front page instead of to Pelican's author pages.
AUTHOR_URL = "" # "authors/{slug}/"

# Disable the period archives pages.
YEAR_ARCHIVE_SAVE_AS = ""  # "{date:%Y}/index.html"
YEAR_ARCHIVE_URL = ""  # "{date:%Y}/"
MONTH_ARCHIVE_SAVE_AS = ""  # "{date:%Y}/{date:%m}/index.html"
MONTH_ARCHIVE_URL = ""  # "{date:%Y}/{date:%m}/"
DAY_ARCHIVE_SAVE_AS = ""  # "{date:%Y}/{date:%m}/{date:%d}/index.html"
DAY_ARCHIVE_URL = ""  # "{date:%Y}/{date:%m}/{date:%d}/"

# Have only one feed.
FEED_ATOM = "feed.xml"
FEED_RSS = None
FEED_ALL_ATOM = None
FEED_ALL_RSS = None
CATEGORY_FEED_ATOM = None
CATEGORY_FEED_RSS = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
TAG_FEED_ATOM = None
TAG_FEED_RSS = None
TRANSLATION_FEED_ATOM = None
TRANSLATION_FEED_RSS = None
# The timezone used to generate RSS and Atom feeds.
TIMEZONE = "Europe/London"
# The domain prepended to feed URLs.
# Feed URLs should always be absolute, so it's recommended to set this.
FEED_DOMAIN = SITEURL
# Include all articles in the feeds.
FEED_MAX_ITEMS = None
