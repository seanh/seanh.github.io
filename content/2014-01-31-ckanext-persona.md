Title: A Mozilla Persona Plugin for CKAN
Subheading: Login to CKAN sites without creating an account, using Mozilla Persona.
Tags: CKAN
redirect_from: /post/ckanext-persona/

<figure>
  <img src="{static}/images/persona.png" alt="Logging into CKAN using Persona" title="Logging into CKAN using Persona">
  <figcaption>Logging into CKAN using Persona</figcaption>
</figure>

[ckanext-persona](https://github.com/ckan/ckanext-persona) is a [CKAN](http://ckan.org/) plugin that
lets users login to CKAN sites using [Mozilla
Persona](http://www.mozilla.org/en-US/persona/).

The Persona plugin adds a *login using your email address* option to CKAN's
login and register pages. As you can see in the screenshot above, CKAN's
traditional username and password login is still available as well.

When a user clicks on the *Email* button it opens a Persona sign in page in a
popup window. After signing into Persona the popup window disappears and the
user is taken back to CKAN and logged in.

Here's a video of the login process:

<iframe src="//player.vimeo.com/video/85054941?title=0&amp;byline=0&amp;portrait=0" width="600" height="474" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>

This was quite a fun plugin to develop, it was one of the first plugins to use
[CKAN's IAuthenticator plugin interface](http://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IAuthenticator)
and it revealed some interesting limitations that could be addressed in CKAN.

The way it works is:

<figure>
    <img src="{static}/images/persona_signin_1.png" alt="Logging into CKAN using Persona" title="Logging into CKAN using Persona">
    <figcaption>Logging into CKAN using Persona</figcaption>
</figure>

1. The user browses to the login page of the CKAN website and clicks on the
   *Email* button. The button opens the Persona sign-in page in a popup window.

2. The user signs in to Persona using their email address, verifying that they
   are the owner of the email address. The popup window closes, returning the
   user to the CKAN site that they came from.

3. Persona sends an *Identity Assertion Certificate* to CKAN, asserting that
   the user owns the email address. Some JavaScript belonging to the Persona
   plugin receives this assertion from Persona and posts it to CKAN's login
   URL.

4. CKAN's Python code on the server receives a request to its `/login` URL with
   the Identity Assertion Certificate in the post parameters. CKAN must now
   handle this request and log the user in.

When a request is made to CKAN's `/login` URL CKAN iterates over the active
`IAuthenticator` plugins and calls the `login()` method of each, to see if any
of them can handle this login request.  If no plugin logs in the user, CKAN
will fall back to its default username and password login handler.

After finding the Identity Assertion Certificate in the post params and
verifying it, the Persona plugin's `login()` method handles the login request
as follows:

<figure>
    <img src="{static}/images/persona_signin_2.png" alt="Logging into CKAN using Persona" title="Logging into CKAN using Persona">
    <figcaption>Logging into CKAN using Persona</figcaption>
</figure>

1. It searches CKAN's database for an existing user
   account with the verified email address. There are three possible responses
   from the database:

    1. There is one existing CKAN user with the email address
       (this is what's shown in the video above.)

    2. There is no existing user with the email address, so the plugin creates a
       new account with this email address and logs the user into it
       (this is done silently - the user isn't bothered with the fact that a new
       account is created for them on the CKAN site).

    3. The CKAN site has multiple users with the same email address.
       In this case the plugin shows the user
       a list of the user accounts and asks them to choose which one they want
       to login to.
       (Note: this page isn't implemented yet!)

2. Whichever route we took, we end up with one CKAN account that matches the
   Persona email address that was used. The plugin logs the user into the
   account by saving the email address and username of the account in CKAN's
   Beaker session. (The session is a file on the server that keeps track of
   the logged-in user.)

3. Finally, the plugin redirects the user's browser to the dashboard page of
   the account they've just logged in to.

On every page load, CKAN calls the `identify()` method of every active
`IAuthenticator` plugin to see if any of them can find out which user is logged
in. If no plugin identifies the logged-in user, CKAN searches for a cookie
created by its default username and password login.

The Persona plugin's `identify()` method will use user name it saved in the
Beaker session to identify the user. This is how the user stays logged-in as
they move from page to page on the site.

Finally, when the user hits the logout button CKAN calls the Persona plugin's
`logout()` method, which deletes the cookie that the plugin created so that its
`identify()` method will no longer find a logged-in user when the next page is
loaded.


## Todo

A few of things still need to be implemented:

* When creating new user accounts, the Persona plugin has to generate a user
  name. Currently it just uses a UUID, and the user can change their name in
  CKAN once they're logged in.

    A nicer solution would be to generate a username based on the email address.
    `bob@gmail.com` would get the username `bob`, of if `bob` is already taken
    then something like `bob54` (random number appended).

    Before being logged in the user should be taken to a *Choose your username*
    form where they can enter the username they want, and the form is pre-filled
    with the generated username as a suggestion.

    When the user enters a username into this form and submits it, it needs to be
    checked to make sure that it's a valid and untaken username, and then the
    user account can be created and the user logged in.

* When creating new user accounts, the Persona plugin also has to generate a
  password, because CKAN currently requires a password for the new account.
  This password is never shown to the user so they can't use it to login using
  the traditional username and password route. They can only login using
  Persona. The generated password is nothing but a potential security issue.

    This needs to be fixed in CKAN by allowing user accounts without passwords,
    that cannot be logged into the traditional way. See the issue here:
    <https://github.com/ckan/ckan/issues/1459>.

* Logging in when there are multiple user accounts with the same email address
  isn't implemented yet (CKAN just crashes). This feature will actually
  probably be quite handy when done, e.g. for developers who have multiple
  accounts on the same site for testing (a normal account, a sysadmin account,
  etc).

Other things that still need to be done include JavaScript-less
login with Persona, [CSRF protection](https://developer.mozilla.org/en-US/Persona/Security_Considerations),
tests, a nicer user experience when the Persona verification fails, and
enabling CKAN accounts to have multiple email addresses and
[verifying those addresses with Persona](https://developer.mozilla.org/en-US/Persona/The_implementor_s_guide/Adding_extra_email_addresses_with_Persona).

[Mozilla recommend using Selenium](https://developer.mozilla.org/en-US/Persona/The_implementor_s_guide/Testing?redirectlocale=en-US&redirectslug=Persona%2FThe_implementor_s_guide%2FTesting)
to test logging in with Persona. We've been planning to use Selenium for new
frontend tests in CKAN, so once we get going with that maybe we can write the
ckanext-persona tests in the same way.

To test ckanext-persona, see the [ckanext-persona website](https://developer.mozilla.org/en-US/Persona/The_implementor_s_guide/Adding_extra_email_addresses_with_Persona)
for installation instructions.
