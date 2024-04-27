Title: Python Unit Tests at Hypothesis
Tags: Hypothesis, Python Unit Tests at Hypothesis
Alias: /post/python-unit-testing/

This is the index page for a series of posts about our approach to Python unit
tests at [Hypothesis](https://hypothes.is/):

<ol>
    <li><a href="/2017/01/16/running-the-h-tests/">Running the Hypothesis Python Tests</a></li>
    <li><a href="/2017/01/28/debugging-tests/">Debugging Failing Tests with pytest</a></li>
    <li><a href="/2017/01/28/writing-tests/">Writing Simple Python Unit Tests</a></li>
    <li><a href="/2017/01/29/arrange-act-assert/">Arrange, Act, Assert</a></li>
    <li><a href="/2017/01/29/factories/">Python Test Factories with factory_boy</a></li>
    <li><a href="/2017/01/29/testing-that-exceptions-are-raised/">Testing that an Exception is Raised with pytest.raises</a></li>
    <li><a href="/2017/01/31/parametrize/">Parametrizing Python Tests</a></li>
    <li><a href="/2017/02/02/fixtures/">Basic pytest Fixtures</a></li>
    <li><a href="/2017/02/12/advanced-fixtures/">Advanced pytest Fixtures</a></li>
    <li><a href="/2017/03/17/mock/">Python’s unittest.mock</a></li>
    <li><a href="/2017/03/17/patch/">Hypothesis’s patch Fixture</a></li>
    <li><a href="/2017/03/17/sentinel/">sentinel: Unique Objects for Tests</a></li>
    <li><a href="/2017/03/17/the-problem-with-mocks/">The Problem with Mocks</a></li>
    <li><a href="/2017/03/17/usefixtures-class-decorator/">usefixtures as a Class Decorator</a></li>
    <li><a href="/2017/04/25/when-to-use-mocks/">When and When Not to Use Mocks</a></li>
    <li><a href="/2017/05/12/matchers/">Matcher Objects in Python Tests</a></li>
</ol>

While this tutorial is based on Hypothesis's approach and the examples are
taken from Hypothesis's tests, most of it should be applicable to Python unit
testing generally.

These posts are aimed at intermediate Python developers, not complete beginners.
Basic knowledge of [Python](https://www.python.org/) programming and
[virtualenv](https://virtualenv.pypa.io/) are assumed, for example.

In a large, real-world project like Hypothesis the tests contain a lot of
things that might be unfamiliar - factories, `parametrize`, mocks, `sentinel`,
`patch`, `usefixtures` and [test method arguments that seem to come from nowhere](./python-unit-tests-at-hypothesis/_posts/2017-02-02-fixtures.md).
One of the aims of this tutorial is to introduce you to all these, so that you
can read the Hypothesis test code and understand what's going on.

Knowing how and when to use all of these tools will help you to write better
tests. We'll also cover a few more advanced aspects of writing **good tests**,
as opposed to bad ones, particularly when we talk about how to organize your
tests; the arrange, act, assert pattern and test naming; fixtures; and how and
when to use mocks.

Finally, we'll touch even less on the important but difficult topic of how to
design **good code** that works well and is easy to test.
