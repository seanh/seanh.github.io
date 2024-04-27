Title: When and When Not to Use Mocks
Tags: Python Unit Tests at Hypothesis
Alias: /post/when-to-use-mocks/

[The first post about mocks](/2017/03/17/mock/)
covered the basics of how to use Python's mock library.
[The Problem with Mocks](/2017/03/17/the-problem-with-mocks/)
explained the dangers of using mocks and advanced features of the mock library
that can be used to minimize those dangers.
Returning to the topic of mocks, this post discusses the complex question of
when and when not to use them in your tests.

My references for this are J.B. Rainsberger's
[Integrated Tests Are a Scam series](http://blog.thecodewhisperer.com/series#integrated-tests-are-a-scam)
and Gary Bernhardt's videos about
[Boundaries](https://www.destroyallsoftware.com/talks/boundaries) and
_functional core, imperative shell_.

## It's really about when to write isolated tests

Mocks aren't an end in and of themselves. You don't use mocks in your tests
just for the sake of using mocks. Mocks are a means to an end, that end being
isolated unit testing. The real question to ask, then, is
**when to write isolated tests and when to write integrated tests?**

I'll give my opinion on that question below, but first I want to explain what isolated and
integrated tests are, and what their pros and cons are.

* An **isolated test** is one that tests just one "unit" (usually a class or
  function) in isolation. No other code outside of that class or function is
  run when the test runs - either because the code under test doesn't call any
  other code (it doesn't have any dependencies) or because the tests mock out
  all its dependencies.

* An **integrated test** is one in which the code under test calls the real
  code that it depends on, whether that dependency is another module of your
  own codebase or is a third-party library. One or more dependencies aren't
  mocked, and the code is tested _in integration with_ those dependencies.


## You can have isolated tests without mocks

It's possible to [design your code in such a way that you can write
isolated tests without needing to use mocks](https://www.destroyallsoftware.com/talks/boundaries)
by applying a "functional core, imperative shell" approach and using value
objects as the boundaries between your units. When you can achieve fully
isolated tests without mocks, that's the best of both worlds - you get
all the advantages of isolated tests (see below) and avoid the
[problem with mocks](/2017/03/17/the-problem-with-mocks/).

This, however, is an advanced technique that isn't always easy to apply, that
might not be applicable when you're working with existing code, and that
may lead to complaints from other developers that it's esoteric and too
different from the style of the rest of the codebase. So for the rest of the
time, when you want to write isolated tests and the unit of code you want
to test does have non-trivial dependencies, there are mocks.

## Isolated tests vs integrated tests

Isolated tests (with or without mocks) have a lot of advantages over
integrated tests:

* Isolated tests run **extremely fast**, integrated tests are much slower
  (especially when running a large test suite of them all at once).

    Real dependency objects can be slow to create or to use. Perhaps they touch
    the database or filesystem, or do a lot of computation. If these real objects
    are used many times throughout a large test suite this can result in slow
    tests.

    It's worth noting here, though, that
    [factories](/2017/01/29/factories/)
    can mitigate this problem by making real ORM objects fast to create and use
    if you use the `.build()` method (which creates the object without adding it
    to the database session). You can't always get away with this though - some
    ORM object attributes aren't initialized until that object is added to the
    db, if your test needs one of those attributes you might not be able to use
    `.build()`.
    
    Mocks are always very fast to create and use.

* Isolated tests are **small and easy to understand**.

    Because you're testing just one method in isolation, isolated tests
    tend to be much smaller and simpler to understand than integrated tests
    (requiring less setup, for example).

    This isn't true if your isolated test has to create a lot of complex mock
    objects though (see below).

* Isolated tests are **resilient**, integrated tests are fragile and brittle.

    If you use real `Bar` objects in the tests of any modules that depend on
    `Bar`, then a bug in the `Bar` code can break the tests for all the modules
    that depend on `Bar` as well. One bug causes many tests to fail because
    **the tests are duplicating each other**, running the same `Bar` methods
    with the same arguments again and again.

    A cascade of dozens or hundreds of test failures, many of them irrelevant to
    the actual bug, can make debugging difficult by making it difficult to find
    the code that's at fault.

    Isolated tests **pinpoint bugs**. Ideally, a bug in the `Bar` code would only
    cause `Bar`'s own unit tests to fail, and a failing test should point quickly
    to the line of code that's wrong. A good test should have only one reason to
    fail, and if you know what test failed then you should know what the problem
    is.

* Isolated tests enhance **Test Driven Development (TDD)** by providing design feedback on your code.

    A unit test for a method is a piece of user code that calls that method. If
    the method and its arguments, return values and side effects are complex or
    awkward to use then its unit tests will be complex and awkward to write.
    If you find yourself writing difficult unit tests this is likely a sign that
    your code is hard to use, changing the code in a way that makes the tests
    nicer to write will also improve the design of the code.

    If the test has to create many complex or deeply nested mocks
    in order to test the unit in isolation then the mocks are telling
    you that your code is coupled to many dependencies in complex and deeply
    nested ways. Again, changing the code in a way that makes it easier to test
    in isolation will also improve the design of the code itself.

* Isolated tests can **cover more with fewer tests**.

    You can cover more lines of code, and more of the different possibilities and
    paths through your code, by using isolated tests than by using
    integrated tests. The number of isolated tests needed to have high
    coverage of a codebase is large, but increases linearly as the size of the
    codebase increases. The number of integrated tests required to cover all the
    same paths and possibilities increases combinatorially (read: worse than expontential).
    This point is well covered in
    [Integrated Tests Are A Scam](http://blog.thecodewhisperer.com/permalink/integrated-tests-are-a-scam).

* Mocks are **easy to setup**.

    Sometimes creating a real object can be difficult, if it requires a lot of
    arguments or depends on a lot of other objects to be setup first.
    Setting up real objects can not only make tests hard to write, it can also
    tightly couple your tests to the details of how to create and setup the
    dependency objects and their own dependencies. The code under test doesn't
    care about these details - perhaps it doesn't create the objects itself.
    But its tests are now coupled to these details. This can make your tests
    **fragile** - if the dependency code changes then your tests can break, and
    refactoring the dependency code can be difficult if it breaks a lot of tests
    of other modules.

    Again it's worth noting that
    [factories](/2017/01/29/factories/)
    can mitigate this problem by making real dependency objects simple to create.

    Tests don't just need to create dependency objects though, often they also need to
    set them up so that they return the required values, or have the required
    side effects (for example: raising an exception) depending on what this
    particular test is trying to test for. Writing the necessary setup code to
    get a real dependency object to do what you want can be time-consuming and
    can **tightly couple** your unit tests for `Foo` to implementation details
    of `Foo`'s dependency `Bar`.

    Mocks are very easy to create and their `return_value` and
    `side_effect` attributes make them easy to setup with required behaviors as
    well. Mocks don't couple your tests to the implementation details of the
    dependencies they're mocking, mocks represent only the interface and contract
    of the objects being mocked.

* Mocks make it easy to write **collaboration tests**.

    As we saw in [the first post about mocks](/posts/mock), mocks come
    with a collection of attributes and methods that make it easy to assert that
    a mock method was or was not called, that it was called with the right
    arguments, etc. This can be very helpful when writing collaboration tests -
    tests that a module uses the code that it depends on in the correct ways.

* Mocks have **no real world side effects**.

    A real object might try to send an email, access the Internet, read from or
    write to the filesystem, etc. You don't want objects to be doing these things
    whenever anyone runs the unit tests for a module that depends on those objects.
    Mocks are guaranteed not to have any "real world" side effects.

* Using mocks enables you to **write the high level code first**.

    You can take a top-down approach to designing your code, first writing the
    high level code and testing it using mocks of the lower level modules that
    haven't been written yet.

## Fallacies of integrated tests

There's a couple fallacies about integrated testing out there that I think many
programmers believe (consciously or not). I certainly used to believe in both
of these:

First, that the way to write solid code that doesn't have any bugs is to have a
lot of tests to make sure there aren't any bugs.  The way to write solid code
with few bugs is not by high test coverage but by **good design**.  Isolated
tests are the way to get that good design (and, incidentally, will also result
in high test coverage). Test driven development is about good design, as much
as it's about testing.

Second, that if you just write integrated tests, tests of `Foo` using the real
`Bar` instead of a mock `Bar`, then you **know that it really works**
(whereas with a mock `Bar` you don't really _know_, because the mock could be
wrong).

It may be true that if you write an integrated test for "if x1 then y1" than you do
know that that one particular thing really does work. But that's just one tiny
thing, it doesn't guarantee that the system as a whole really works, what about
"if x2 then y2"? Because of the combinatorial explosion in the number of
integrated tests needed to cover all possibilities, you can't write them
all. If a test is missing,
**the tests could all be passing even though the code is wrong**.

And do you even really know that "if x1 then y1"?
What if your test code is wrong and doesn't actually test what it intends to
test? **The tests could all be passing even though the code is wrong**.

It can even be the case that, with an integrated test for `Foo` that uses the
real `Bar` not a mock `Bar`, your "if x1 then y1" integrated test for `Foo` was
correct once, but then `Foo`'s dependency `Bar` was changed in such a way that
the test no longer tests what it was intended to, but still passes.  Again,
**the tests could all be passing even though the code is wrong**.

It's true that mocks being out of sync with the real objects that they mock is
one way for the tests to still pass even if the code is wrong. But this is just
one of many ways in which **if the tests are wrong or incomplete, then the
tests could all be passing even though the code is wrong**, and most of the
ways that this can happen apply to integrated tests as well as isolated tests.

The lesson is, again, that it's really **good design** that produces code with
fewer bugs. Good design of the kind that makes it quick and easy to write
fast, readable tests so that the tests will contain fewer mistakes and
omissions.

## When to write isolated tests and when to write integrated tests?

So isolated tests have many advantages over integrated tests.
Let's return to the question that we started out with: when to write isolated
tests (and when to use mocks to do so, if necessary) and when to write
integrated tests?

On this I agree with J.B. Rainsberger in
[Integrated Tests Are A Scam](http://blog.thecodewhisperer.com/permalink/integrated-tests-are-a-scam).

### When to write integrated tests

For the most part, I think a good rule of thumb is that **at the boundaries**
where your code touches external code that you don't control - third-party
libraries (especially complex ones such as database libraries), web frameworks,
the standard library - you should probably test that edge code in integration
with that external code, rather than trying to mock the external code.

One reason for this is that external code often has complex interfaces, mocking
them would be complex and brittle, and since it's not your code you can't
redesign the external code to simplify its interface (at least, not at the
**very** edge where your code final touches the external code).

Another reason is that you want to test your understanding of the external
code, to test that your code really does use the external code correctly, that
that complex SQL query really does return what you want it to. External modules
like database libraries are often complicated to use correctly.

One exception is when your code uses a third-party library that has real-world
side-effects: sending emails or something like that. In those cases you do need
a fake or mock of that library to test against.

When testing in integration with external code, you should design your code
to **encapsulate** those external dependencies. Minimize the amount of your
code that needs to be tested in integration with complex external dependencies
and maximize the amount of your code that can be tested in isolation.

### When to write isolated tests

In the core of your codebase, where you're just dealing with your own modules
depending on other modules of your own, you almost always want to test in
isolation. But you should design your code so that you only need a few simple
mocks, or if possible even no mocks at all, in order to test it in isolation.

One exception is when the module under test depends on a [value object](https://en.wikipedia.org/wiki/Value_object)
that's so simple that it doesn't need mocking, simple enough that the advantages
of mocking and the disadvantages of integrating don't come into play. In that
case, of course, you don't need to mock it. Knowing the pros and cons of
mocking vs integrating (see above) will enable you to decide when to do this.

Personally, I'd place a pretty strict definition on whether something qualifies
as a value object for this purpose: it should be an object that's under our
control (not one that comes from an external codebase), it should be a simple
(not complex or deeply nested) data object, with possibly a few very simple
"computed property"-type methods (very simple nothing in, value out code that
does nothing complex, operates only on the object's internal data, takes no
arguments, and has no side effects).

## Listen to what your bad mocks are telling you

The problem with mocks getting out of sync with the real code that they mock
and causing false-positive test passes isn't a big problem if you only have a
few simple mocks. It's at its worst when you have a lot of complex and deeply
nested mocks.

I already mentioned this above but it's worth repeating another way - having a
lot of complex mocks in your tests is a problem that you shouldn't put up
with. But it's a symptom rather than a cause. The cause of numerous complex
mocks could be one of two things:

1. Choosing to write isolated tests when you should be writing integrated
   tests. If the complex interface that you're mocking is a third-party library,
   then maybe you should be testing in integration with that library instead.
   _Or_:

2. Bad code design. If the complex interface that you're mocking is part of your
   own codebase, then maybe your code is badly designed and you should change
   it so that it can be tested in isolation with only a few simple mocks,
   if any.

Conclusion
----------

That's my opinion about when to use isolated tests and mocks!
Admittedly, mostly formed by listening to what others have said.
If you've made it this far I'd really encourage you to watch
[Integrated Tests Are A Scam](http://blog.thecodewhisperer.com/permalink/integrated-tests-are-a-scam)
and
[Boundaries](https://www.destroyallsoftware.com/talks/boundaries).
