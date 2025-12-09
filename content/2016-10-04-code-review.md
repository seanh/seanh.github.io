Title: Code Review
Subheading: How to make code reviews a more pleasant and empowering experience for everyone involved.
Tags: Hypothesis
Alias: /post/code-review/
       /posts/code-review/

<aside markdown="1">
See also:

* This post was [cross-posted to the Hypothesis blog](https://hypothes.is/blog/code-review-in-remote-teams/)
* Discussion of this post [on MetaFilter](https://www.metafilter.com/163682/Code-reviews-are-for-improving-code-quality-and-morale)
</aside>

This is a write-up of some research that I did for a session with our dev team
at [Hypothesis](https://hypothes.is/) about how to make our code reviews a more
pleasant and empowering experience for everyone. Links to sources are sprinkled
throughout the text, and you can also find links to all of the sources I used
(and more) in
[my code review links on Pinboard](https://pinboard.in/u:seanh/t:code-reviews/).
Also thanks to our engineering manager [Lena](https://twitter.com/lenazun) for
suggestions.

We're a fully remote team at Hypothesis, so all communication goes over the
Internet and a lot of it happens asynchronously. We use Trello cards to specify
features, we write code alone, we send GitHub pull requests, and we use
GitHub's pull request review feature to send written code reviews. This can be
very different from face-to-face code reviews in an office, or even from remote
code reviews over video chat.

If taken lightly, this kind of written, asynchronous code review can be a
recipe for disaster where negative communication and collaboration patterns are
concerned. But if the team takes an active interest in doing it well, then I
think it can work very effectively.



What are code reviews for?
--------------------------

Before discussing how and how not to do code reviews it'll be useful to think
about what code reviews are for in your organization so that the do's and
don'ts that follow can be assessed against these aims. I think it's also good
to remember that code reviews aren't just about finding bugs and code design
issues.

The point that I want to make here is that code reviews are for improving code
quality **and morale**.

Code review is one of the main ways that developers interact with each other
during a normal working day, so it needs to be an uplifting experience that
developers look forward to and
[that all participants actively want to take part in](https://speakerdeck.com/stuartherbert/how-to-do-positive-code-reviews?slide=8).
If code review is often an unpleasant experience morale will suffer.

Here are some aims to consider when doing a code review:

* **Create your team's internal culture**.
  Code reviews are one of the main places in which your team culture is
  enacted, and [unpleasant code reviews are a side-effect of a lack of
  deliberate team culture](https://speakerdeck.com/stuartherbert/how-to-do-positive-code-reviews?slide=32).
  Use code reviews to deliberately foster a positive, patient and friendly
  culture.

* **Improve your working relationships** by having a chance to talk to your
  fellow developers.

* **Relieve tension** by giving people positive feedback.

* **Learn**. A reviewer can learn new things from the code they're reviewing,
  and an author can learn from the feedback they receive.

* **Break down code silos** by having everyone on the team review changes to
  different parts of the code, gaining familiarity with the whole codebase.

* **Mentoring and education**. Code review is a chance for more experienced
  developers to mentor and teach others. But be aware that code review, after
  time has already been spent and code written, isn't always the best time for
  mentoring and education. Developers should already have collaborated on the
  technical design before and during the code writing itself.

* **Code quality.** Finally, yes, code quality (including bugs,
  maintainability, documentation, organization, architecture, usability, ...)
  is one of the aims of code review.


Don'ts
------ 

This long list of bad behaviours may feel a bit negative, but honestly, this is
meant to be a positive post, and when you get through this section there's a
long list of _do's_ to follow!
There are many ways to make a code review unpleasant by doing the wrong things,
so I think knowing what not to do is a good place to start.
Combative, unkind and unpredictable code reviews can make developers unhappy
and can make the job emotionally difficult to do. 

> "Understanding what to avoid in code review can mean the difference between
> your review being a valuable part of your team's delivery and your review
> simply being cruel and unusual punishment." [Erik Dietrich: What To Avoid When Doing Code Reviews][]


### Don't just do the direct and minimal code review

(a.k.a. _find out how much you suck_)

Don't just be straight and minimal, simply pointing out the things that are
wrong with the code, saying what you want to be changed, and nothing more.

Developers spend a lot of time on and take pride in their code, and code review
is the chance for them to showcase that. With this kind of direct and minimal
code review the best result that the author can hope for is no comments:
"LGTM, merged."
The code review might as well be titled [find out how badly people think you suck][Erik Dietrich Programmers Stack Exchange answer to "How important is positive feedback in code reviews?"].

[Blunt and unfiltered communication carries a long-term cost][Daniel Bader: 7 ways to avoid aggravation in code reviews]. It can poison
the team's communication culture and hit developer productivity. The developer
on the receiving end of lots of code reviews like this
["often feels like it's a bashing session designed to beat out their will"][Robert Bogue: Effective Code Reviews Without the Pain],
and code reviews can become ["mental jousting matches where people take shots
at a target ... the developer that wrote the code"][Robert Bogue: Effective Code Reviews Without the Pain].


### Don't think that "criticize the code, not the coder" is enough

"Criticize the code, not the coder" is probably the most well known advice
about how to do code reviews. It's good advice (if you're criticizing your
teammates as people, rather than talking about the code, you've got a problem).
But it's not enough. Code is creative work that developers put their heart and
soul into and harshly or bluntly criticizing someone's code is tantamount to
criticizing them. You have to do better, and find a more positive way to
deconstruct and make suggestions about code.


### Watch your tone

**Don't use personal tone when criticizing**. Phrases like "Why have you ... ?"
etc feel like attacks. Instead of saying "The way you've written this function
makes it hard to read, add more code comments" (which is quite personal and
implies that the person has done something wrong), say "Do you think that
adding more code comments would make this function easier to read?"
(which gives the author back their agency, and focuses on what they can do to
improve the code).

**Don't use demanding or challenging language**. Avoid phrases whose meaning
comes across as "you are wrong." Don't tell people that they're wrong, or that
what they've said is invalid, because it can make them feel under attack.
If they feel under attack, people can become defensive, can't engage creatively
any longer, and stop learning.
Avoid phrases like:

* "That is simply false"
* "This is completely wrong"
* "Why didn't you just ... ?"

**Don't use hyperbole when making criticisms**. You don't want the coder to
feel offended because they feel that your criticisms of their code are
unjustified or exaggerated. [Avoid unnecessary words like "always", "never",
"endlessly", and "nothing" in criticisms][Daniel Bader: 7 ways to avoid aggravation in code reviews].

**Don't use insulting language**. [Avoid "accidental insults" by not using
words like "dumb" or "stupid" in code reviews][Daniel Bader: 7 ways to avoid
aggravation in code reviews], even though you don't intend them as insults.
This kind of language carries contexts and associations and can set the frame
of mind of the person receiving it.

**Don't use impatient or passive-aggressive language**.
Always keep it patient and friendly, avoid unpleasant phrases that show
irritability and make people feel like they're not doing good enough:

* "Once again, this should be..."
* "As I've already said..."

**Don't pile on**.
It can make someone feel attacked if they're given a critical comment by one
colleague, and then one or more further colleagues +1 the comment or jump in
with critical comments of their own. Multiple critics can also be confusing
and create a "too many chefs" problem.


### Don't be a back-seat coder

This means holding off, and not requesting many of the code changes that you
may be tempted to request. Feedback that asks for too many changes and feels
like a rewrite can be demoralizing, so consider your suggestions carefully and
pick the best ones.

Yes, one of the aims of code review is to find and correct bugs and design
issues with the code. 
But don’t use code review to try to get the author to rewrite the code to the
way you would have written it yourself.
Remember that many things in software are a matter of opinion,
multiple solutions that each have their pros and cons. For each "correction"
that you want to suggest ask yourself whether it might be just a difference of
opinion? In cases where the author has considered different solutions and
chosen one solution for a reason, consider empowering the coder and respecting
their right to make that decision.

> "Although the developer might have coded something differently from how you
> would have, it isn't necessarily wrong. The goal is quality, maintainable
> code. If it meets those goals and follows the coding standards, that's all
> you can ask for." [Robert Bogue: Effective Code Reviews Without the Pain][]

> "You're never going to beat someone into writing the exact code that you would
> have, and it's counterproductive to try. (Honestly, you should have just
> written the code yourself in the first place if that's your attitude.)"
> [Erik Dietrich: What To Avoid When Doing Code Reviews][]


### Don't break the rule of no surprises

[Do not violate the rule of no surprises](https://speakerdeck.com/stuartherbert/how-to-do-positive-code-reviews?slide=41). Have a shared, documented agreement up
front about pull request expectations and standards, and make reviews
evidence-based not opinion-based.


### Don't say things just to hear the sound of your own voice

Before giving feedback think about what you're aiming to achieve by doing so
and think about whether each comment is necessary. Remember that you're trying
to constructively help, not trying to make a point. When writing a code review
I go back and review my comments before posting them, asking myself whether
each comment is really helpful or necessary, and end up deleting many of my
comments before posting the review. Reviewing your comments post hoc can make
this easier. While you're deep in the code, working to understand it and to
develop your thoughts on it, you can write down as many comments as you please.
After, you can decide what you actually want to send to the coder.


> "Well-actually-ing just for the sake of being right isn't always helpful (or
> appreciated), and sometimes keeping that kind of feedback to yourself can be
> beneficial for the sake of your long-term relationship with a person." [Katherine Daniels: On Giving and Receiving Feedback][]


### Don't think that you have to find a problem in every code review

If the code is good and can be merged without any changes, that's fine!


Do's
----

**It doesn't have to be this way!** Below are some of my favourite suggestions,
collected from around the Internet, about how to turn code reviews around and
make them into a positive, collaborative experience.


### Praise good code

Remember to spend plenty of time praising what is good about the code, before
pointing out problems and making suggestions.

> "Human nature is such that we want and need to be acknowledged for our
> successes, not just shown our faults. Because development is necessarily a
> creative work that developers pour their soul into, it often can be close to
> their hearts. This makes the need for praise even more critical." [Robert Bogue: Effective Code Reviews Without the Pain][]

You want people to look forward to code review as a positive and constructive
experience and not fear it as pure criticism. Positive feedback also relieves
interpersonal tensions and helps people to respond better to any critical
feedback.

The hard part is to find a way to give positive comments without making them
seem like fluff or fake praise, or obvious [shit sandwich](http://blog.idonethis.com/sandwich-feedback-performance-management/) constructions.

Avoid the **backhanded compliment**, phrases like "Great job, but..." (followed
by all the changes that you want to be made) can seem insincere.

Some ways to give more natural, sincere and concrete praise:

* Appreciate lots of the specific parts or aspects of the code that are good,
  and try to say _why_ you like them.

* [Leave a "running monologue" of your  thoughts as you read and understand the
  code][Jimmy Hoffa Programmers Stack Exchange anser to "How important is positive feedback in code reviews?"]. "Ok, I see what that does.. Good it connects to this and calls that,
  alright.. and that piece depends on both of those alright."

    Seeing another programmer show comprehension of you work is itself a form of
    validation of the work, and when you run into parts of the code that you
    don't understand you can ask for an explanation.


### Put a positive summary at the top

[Set the mood by indicating, in a positive summary statement at the top of your
review, that you're happy and thankful for the code][Robert Bogue: Effective Code Reviews Without the Pain]. [GitHub's new code review features](https://github.com/blog/2256-a-whole-new-github-universe-announcing-new-tools-forums-and-features)
make this a lot easier by letting you write multiple line comments and then
post them all at once (rather than each comment being posted as soon as you
save it), and by letting you add a summary (which appears the top of your
review) before posting the comments:

<img src="{static}/images/github-code-review.gif">


### Avoid inherent accusations

**Ask, don't tell**. Ask questions rather than making statements:

> "A statement is accusatory. "You didn't follow the standard here" is an
> attack—whether intentional or not. The question, "What was the reasoning
> behind the approach you used?" is seeking more information." [Robert Bogue: Effective Code Reviews Without the Pain][]

Asking questions instead will improve the mood, change the tone of the
following conversation by opening the door for dialogue and learning, and
encourage the developer to explain their reasoning or ask themselves whether
there's a better way.

Ideally, if there is a bug in the code then it will be found by the author
themselves in response to prompting by question asking, or if there is an
improvement to be made to the code, it will be suggested by the author.

> "If you see things that could be errors, you don't need to tell people they're
> wrong, usually a "what do you think would happen if I passed null into this
> method" would suffice because the person will probably say, "oh, I didn't
> think of that — I’ll fix it when we’re done here." Allowing them to solve the
> problem and propose the improvement is empowering and <em>so, so</em> much
> better than giving them orders to fix their deficient code." [Erik Dietrich: How to Use a Code Review to Execute Someone’s Soul][]

Bad:

* "You didn't follow the standard here"
* "This is wrong, use B instead."
* "This code is confusing."
* "You didn't initialize these variables"

Good:

* "What was the reasoning behind the approached you used?"
* "What was your thinking in using A instead of B?"
* "I didn't understand this bit. Can you clarify that for me?"
* "I didn't see where these variables were initialized"


**Avoid the accusatory why**. Like statements,
["why" questions can also be accusatory as well][Robert Bogue: Effective Code Reviews Without the Pain],
and avoiding them can improve the mood.

Bad:

* "Why didn't you follow the standards here?"
* "Why didn't you just ...?"

Good:

* "What was the reasoning behind the deviation from the standards here?"
* "What did you have in mind when you ...?"


### Be humble

**Ask questions, don’t make demands**.
Rather than just telling the code author to make a change that you want,
ask them a question about their code or make a suggestion and ask them whether
they think it would be an improvement. This puts the ball in their court and
respects the author's agency, giving them a chance to explain their decisions
or to decide whether they think a suggestion is an improvement.

> "Instead of saying "Let’s call that variable userName because it's unclear",
> phrase your suggestion as a question, like so:
> 
> "What do you think about naming this userName? The current name felt unclear to me
> because it's also used in another context in someotherfile.js." [Daniel Bader: 7 ways to avoid aggravation in code reviews][]


**When making a suggestion, also give the reason why** you think this change
might be an improvement.

**Use personal examples**.
[Let the code author know that they're not the only person ever to make this mistake][Kate Matsudaira: Giving Feedback – learning to criticize in a way that actually works].
This can be a great way to make criticism more comfortable:
"I learned this the hard way...", or "I used to do the same thing..."


**Agree that not every question needs to be responded to**.
[Make an upfront agreement that not every question needs to be responded to][Robert Bogue: Effective Code Reviews Without the Pain].
This lets you include thought-provoking questions in your review that don't
necessarily need to be resolved or even responded to in order to get the code
merged, but that can nonetheless get developers thinking and improve the
quality of the entire codebase in the long run.


### Don't break The Rule of No Surprises

**Use checklists**:

> "It's very likely that each person on your team makes the same 10 mistakes
> over and over. Omissions in particular are the hardest defects to find
> because it's difficult to review something that isn't there. Checklists are
> the most effective way to eliminate frequently made errors and to combat the
> challenges of omission finding." [SmartBear: Best Practices for Code Review][]

Even though it can't cover everything, a good checklist of what a pull request
should have before it can be merged / what a reviewer should be looking for
when reviewing a pull request is a useful tool for both the coder and the
reviewer. A checklist can mean better and more consistent code quality and can
help to avoid breaking the rule of no surprises. Documenting what's
expected is particularly useful for new team members sending their first pull
requests and doing their first code reviews.

Here's an example to get you started:

<label><input type="checkbox">
Your branch should contain one logically separate piece of work and not any
unrelated changes.
</label>

<label><input type="checkbox">
You should have good commit messages, see `<link to commit messages guide>`.
</label>

<label><input type="checkbox">
Your branch should contain new or changed tests for any new or changed code,
and all the tests should pass on your branch, see
`<link to test writing guide>`.
</label>

<label><input type="checkbox">
Your branch should contain new or updated documentation for any new or updated
code, see `<link to writing documentation guide>`.
</label>

<label><input type="checkbox">
Your branch should be up to date with the master branch and mergeable without
conflicts, so rebase your branch on top of master before submitting your pull
request.
</label>

<label><input type="checkbox">
Any new code should follow our code architecture and Python, JavaScript, HTML
and CSS style guides. See `<link to architecture and style guides>`.
</label>

<label><input type="checkbox">
If the new code contains changes to the database schema, it should include a
database migration. See `<link to DB migrations guide>`.
</label>

<label><input type="checkbox">
If the code contains any changes that break backwards-incompatibility for
plugins, API clients or themes, is the breakage necessary or do the benefits of
the change justify the breakage?  Have the breaking changes been added to the
changelog?
</label>

<label><input type="checkbox">
Does the new code add any dependencies (e.g. new third-party Python modules
imported)? If so, is the new dependency justified and has it been added
following the right process? See `<link to upgrading dependencies guide>`.
</label>

<label><input type="checkbox">
Has the code been tested using production data?
See `<link to getting production data in development guide>`.
</label>

<label><input type="checkbox">
If there are UI changes, have they been tested on different screen sizes and in
different browsers? See `<link to responsive design guide>`.
</label>

<label><input type="checkbox">
If there are UI changes, do they meet our accessibility standards?
See `<link to accessibility guide>`.
</label>

<label><input type="checkbox">
If there are new user-visible strings, are they internationalized?
See `<link to internationalization guide>`.
</label>

Have **comprehensive documented coding standards**:

Coding standards are a ["shared agreement that the developers have with one
another"][Robert Bogue: Effective Code Reviews Without the Pain], a shared set of guidelines with buy-in from everyone, about what
makes quality, maintainable code in this organization.
[Coding standards are the foundation of code review][Robert Bogue: Effective Code Reviews Without the Pain] (the coding standards
are the standards that you're reviewing the code against).
Rather than bringing up requirements that aren't in your coding standards, send
a pull request to get them added to the standards instead.

Without the shared project of coding standards as a reference, developers can
find themselves [not knowing where the next problem will come from][Robert Bogue: Effective Code Reviews Without the Pain] in
code review. This doesn't empower developers to contribute effectively.

The coding standards should be comprehensive.
[PEP 8](https://www.python.org/dev/peps/pep-0008/) is a code formatting style,
it's not a complete enough standard for code review.


### Review the right things and let tools do the rest

[Code formatting issues should almost never come up during a code review][Daniel Bader: Should you call out code style issues in a code review?].
Code reviews should provoke productive thoughts and discussions, and spending
too much time on code style and formatting won't help with that. Use tools such
as linters and code formatters instead.


## Conclusion

This post has been about how to give positive feedback as well as making
criticisms, and about how to make suggestions successfully when doing code
reviews. My suggestion for what to do with this for our dev team at Hypothesis,
and any other team interested in doing more effective code reviews, is to make
a concise, bullet point version of this guide and adopt it as the team's
"how to do a code review". Put it in a git repo that team members can open
issues on and send pull requests to, so that the how-to becomes a shared
collaboration.

Beyond what happens at code review time, I think it's also worth thinking about
how the code that's being reviewed gets created in the first place.
I think you want the coder and the reviewer to be largely synchronized on what
the technical design for a feature is going to be _before_ any code makes it
into review. Know who the coder and reviewer for a feature are going to be
beforehand, and encourage them to work as a team of two to deliver the feature,
discussing code designs and intermediate versions of the code before it makes
it to the final review. The aim is to get better code designs (two heads are
better than one), but also to avoid having a debate at review time between two
completely different solutions (one of which would require a rewrite of the
already written code).

If there has already been plenty of collaboration between the coder and the
reviewer before code review time then there'll likely be fewer issues that
need to be raised in review, so you're already off to a good start.

[Daniel Bader: Should you call out code style issues in a code review?]: https://dbader.org/blog/code-review-style-and-formatting-feedback "Daniel Bader: Should you call out code style issues in a code review?"

[Robert Bogue: Effective Code Reviews Without the Pain]: http://www.developer.com/tech/article.php/3579756/Effective-Code-Reviews-Without-the-Pain.htm "Robert Bogue: Effective Code Reviews Without the Pain"

[Erik Dietrich Programmers Stack Exchange answer to "How important is positive feedback in code reviews?"]: http://programmers.stackexchange.com/a/168508 'Erik Dietrich Programmers Stack Exchange answer to "How important is positive feedback in code reviews?"'

[Daniel Bader: 7 ways to avoid aggravation in code reviews]: https://dbader.org/blog/avoiding-aggravation-in-code-reviews 'Daniel Bader: 7 ways to avoid aggravation in code reviews'

[Kate Matsudaira: Giving Feedback – learning to criticize in a way that actually works]: http://katemats.com/giving-feedback-learning-to-criticize-in-a-way-that-actually-works/ 'Kate Matsudaira: Giving Feedback – learning to criticize in a way that actually works'

[Katherine Daniels: On Giving and Receiving Feedback]: https://beero.ps/2016/09/26/on-giving-and-receiving-feedback/ 'Katherine Daniels: On Giving and Receiving Feedback'

[Erik Dietrich: How to Use a Code Review to Execute Someone’s Soul]: http://www.daedtech.com/how-to-use-a-code-review-to-execute-someones-soul/ 'Erik Dietrich: How to Use a Code Review to Execute Someone’s Soul'

[Jimmy Hoffa Programmers Stack Exchange anser to "How important is positive feedback in code reviews?"]: http://programmers.stackexchange.com/questions/168494/how-important-is-positive-feedback-in-code-reviews/168503#168503 'Jimmy Hoffa Programmers Stack Exchange anser to "How important is positive feedback in code reviews?"'

[Erik Dietrich: What To Avoid When Doing Code Reviews]: http://www.daedtech.com/avoid-code-reviews/ 'Erik Dietrich: What To Avoid When Doing Code Reviews'

[SmartBear: Best Practices for Code Review]: https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/ 'SmartBear: Best Practices for Code Review'
