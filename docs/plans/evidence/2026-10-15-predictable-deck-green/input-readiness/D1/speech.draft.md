## Slide 1: Shared login: a proposal to examine

Hi everyone.

I want to walk through a shared login proposal and the trade-offs it brings.

The idea we will examine is one personal account across services. We expect that could reduce some repeated access work, but we do not have measurements yet.

Let me start with the access pattern we are using as a working assumption.

## Slide 2: Access today: a working assumption

Imagine a colleague moving between three services. This is an illustration, not a report about a particular person.

For the discussion, I am assuming each service has its own account and access steps. That can mean choosing credentials again or dealing with recovery separately.

We need to confirm that pattern against our actual environment. With that assumption visible, we can look at what the proposal changes.

## Slide 3: The proposed model

Now, here is the model I propose we discuss. The account belongs to one person and can be recognised across services.

Where a service supports it, the sign-in session could be reused. That is a design condition to check, not something we have already proved.

Signing in tells a service who the person is. Permissions still decide what that person can do in that service. Keeping those responsibilities clear gives us a basis for discussing the benefit.

## Slide 4: Where time could be saved

So, where might the time saving come from?

First, a person could have fewer account credentials to keep track of. Second, where session reuse works, they may avoid some repeated sign-in steps as they move between services.

Those are the mechanisms we expect to help. We cannot say how much time they save yet, and the benefit will depend on how people actually move between services.

Now let us look at the questions that come with sharing the sign-in path.

## Slide 5: Trade-offs to investigate

A shared sign-in path gives us a common dependency to design carefully. What should happen if that path is unavailable?

We also need a clear account lifecycle. Who helps with recovery, and how should access be removed when it is no longer appropriate?

Then there is ownership: who manages the personal account, and who grants access inside each provider? These are investigation questions. I am not presenting settled implementation decisions.

That leaves us with a useful set of questions for the engineering discussion.

## Slide 6: Questions for investigation

So, we have a proposal, a possible benefit mechanism and a set of trade-offs.

I would like us to check which assumptions need evidence and which design questions deserve a small investigation. If we later choose a trial, we should agree how to evaluate it before claiming a saving.

What have we missed, and where would you start?
