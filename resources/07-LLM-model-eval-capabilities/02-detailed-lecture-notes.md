# LLM Model Evals — Session Notes

## Quick Recap

Let's start the session. So guys, quick recap. What have we covered so far in this playlist? I know you all sometimes think, why do I keep doing a recap before every session? I mean, you obviously remember it. I do this recap, guys, because as a teacher, whenever I start a session with a recap, I get into the flow a bit. I fully understand what we've studied so far, what we need to teach today, how to connect it — all of that becomes clear to me. So just stay with me even if you already know what we've covered so far. I'll just give you a quick recap.

We started with **why do we need LLM evals**. Then we discussed **what exactly are LLM evals**. Here we discussed a very important point — that there are two types of LLM evals. One is **model evals** and the other is **application evals**. I told you this, remember? Model evals mean evals that we specifically use to evaluate LLMs. And application evals are the ones we use to evaluate LLM-based applications. And I told you that the main focus of this course is going to be application evals only. This is where you'll learn RAG evaluations, agent evaluations, and so on.

After that, we discussed an **eval pipeline** — basically how evals work. Then we discussed an interesting point — **why do we need multiple eval pipelines**. And in the last video, we covered an important topic — **online evals**: once you've done the evaluation of your application and deployed it, how do you keep evaluating it even after deployment. We discussed this in the last video.

So in a way, I can say that so far we have discussed an overview of this entire course. Now we'll go into specifics. Whatever we've studied so far, we'll cover it in more and more detail, gradually.

## Today's Goal: Model Evals

The main goal of today's video is that we will cover **model evals**. Model evals mean evals that you use directly to test the capabilities of the LLM. So we'll start working on model evals today. It won't be covered in a single lecture — I'm trying to cover it across two lectures.

First, as usual, we follow our flow at Campus X — the **Why, What, How** approach. Let's move ahead the same way.

## Why Do AI Engineers Need Model Evals?

First, let's discuss why we need model evals. Actually, we won't ask that question. We'll ask: **why do AI engineers need model evals?** Because I've told you that we're studying this course from the perspective of AI engineers. So rather than discussing why model evals are needed in general — we already know that. The simple need for model evals is that model evals exist so that we can **measure the capabilities of our LLMs**.

And why is measuring these capabilities important? Because if you don't measure, how will you improve? You must have heard that famous line — **"If you can't measure, you can't improve."** So model evals basically give us mechanisms with the help of which we can evaluate multiple types of capabilities of any LLM.

That is why model evals exist in general. But we'll talk about it from the AI engineer's perspective — if I'm an AI engineer whose day-to-day job is building LLM-based applications, then why are model evals necessary for me? I can understand that model evals are necessary for frontier labs, because based on that, frontier labs understand what improvements they need to make, where things went wrong, how to shape their training. But as an AI engineer, why are model evals important for me? We'll discuss this.

All the discussion we've had so far in this entire playlist, in this entire course, was about how to evaluate LLM-based applications mostly. We talked about how to evaluate the retriever if we're building a RAG application, how to evaluate the generator, how to evaluate the entire pipeline, how to evaluate the whole application. But remember — in this entire discussion, we never once discussed how we evaluate the LLM itself, the one that will act as the brain of that RAG application. How are we selecting it?

Think about it. Suppose today you're thinking of building a RAG application for your company. Obviously, the first question that comes up is — which LLM will you use? Will you use OpenAI's LLM or Claude's LLM? Simple question. Think about it. You have two options — OpenAI, Claude. Now, in a professional setting, you can't say "whichever, use anything, both are good." You can't talk like that. In a team meeting, you will have to come with concrete pointers on why you should opt for OpenAI's LLM or why you should opt for Claude's LLM. And to answer this exact question, you need model evals.

Based on model evals, you can concretely say — "look, these are the pointers, these are the capabilities that are necessary for our application, and look, this particular LLM is scoring higher in that capability. And that is why we should choose this particular LLM over the competitor."

### Reason 1: Comparing Models

So the first reason to study model evals as an AI engineer is that you can easily compare two or more different models and choose one for your application. So this is reason number one.

### Reason 2: Tracking Whether New Models Are Actually Improving

Reason number two is that if model evals are in the picture, you can track whether the new models coming out are actually improving or not. Think about it — your RAG application is deployed. You've put Claude's Opus 4.8 in it. Everything in the application is working fine. Now Claude's Fable has come out. Now your manager is telling you — "hey, do a bit of research and tell me whether we should deploy Fable or stay on Opus."

Now how will you understand this? How would you know as a fact that Fable is better? Again, the answer is model evals. You will get those numbers through model evals only, based on which you can justify whether a new model is better than the previous model or not.

### Reason 3: Checking Safety

Point number three — model evals are the way based on which you can tell whether the model you have deployed or are about to deploy is safe. Right? Model evals tell you how much your LLM is hallucinating. How safe it is to use. Whether it can be jailbroken or not. So all these things, again, model evals tell you.

### Reason 4: Deciding Between Self-Hosting and Using Existing APIs

And the last point — based on model evals, you can make a very important decision — whether you should host your own LLM, deploy it yourself, or use the existing APIs. Right? How will you decide whether you should go with a proprietary LLM like Claude, or you should go with an open source LLM like DeepSeek? Both have their own advantages. Maybe Claude costs more, DeepSeek might be a bit cheaper. But it could also be that Claude is more powerful, better in multiple capabilities, and DeepSeek might not be able to match it.

So how would you decide — should I go for a proprietary LLM, use the API directly, or should I pull an open source model from Hugging Face, put it on my own company's servers, write my own API, and build the entire application myself? Again, this comparison is facilitated using model evals.

**In a nutshell, without model evals, you are basically blind.** If you want to see how a model performs and if you need to compare two models, the only option you have is model evals. In that sense, as an AI engineer, this topic is very important — and that's why we'll cover this topic well.

## What Exactly Are Model Evals?

Now let's discuss a bit more formally — what exactly are model evals? So far, we've only discussed that a model eval is basically a way to evaluate your LLMs. Let's discuss this a bit more formally in this section.

**Definition:** A model eval is a systematic process of measuring an underlying model's capabilities, behavior, reliability, and operational characteristics under controlled conditions.

That definition is just a slightly expanded version. But in a nutshell, it's still the same point — a model eval is a process with the help of which you can test any LLM, its capabilities, its behavior.

### The Four Steps in Every Model Eval

Now, if we talk a bit more technically about what exactly happens inside a model eval — whenever you talk about any type of model eval, there are four things that happen. Every model eval follows four steps:

1. **Decide which capability to test.** LLMs are general purpose models. They can do a lot of types of work. They have a lot of capabilities inside them. So there is no single model eval that can test every capability. It's not like humans, where there's something like IQ. A single number can tell you quite a lot about a human. Unfortunately, this is not the case with LLMs. Every capability of an LLM has a separate model eval. So the first thing you have in a model eval is that you decide which capability of the model or LLM you need to test. Do you want to test its reasoning capability, or its coding capability, or do you want to see how safe it is to use, or do you want to test its instruction-following capability?

2. **Bring a test.** After that, what do you do? You bring a test to test that capability. You bring a test or a mechanism with which you will test that capability. I'll talk more about this in a bit. But the second step is that you bring a test.

3. **Run the model under a fixed protocol.** Third, you run that model on that test. Basically, the model gives that exam. And at exam time, you fix some things — like which prompt will be used, what kind of conditions there will be. All of this you fix, so that you can repeat this going forward. If you're testing multiple models, all models should get the same kind of conditions. So third is — you run the model under a fixed protocol.

4. **Score and interpret.** And the fourth thing is — once the test is done, you score and interpret it.

So, in four steps: first you decide which capability to test, then you bring a test or exam for testing that capability, then you run that test in a controlled environment, and whatever score comes out, you publish it or interpret it.

## Two Types of Tests in Model Evals

Let's talk a bit about an important second step, where we said we bring a test. Now here there are two types of tests in model evals.

### 1. Benchmarks

The first type of test is called a **benchmark**. You may have heard this name too. There are very famous benchmarks. What are benchmarks? Benchmarks are basically standardized, shared tests — like MMLU or SWE-bench — because everyone runs the same test, it's great for comparing models on common ground. So one type of test is a benchmark. A benchmark is like a standardized test. It's basically the same for all models. And its score can also be openly compared between two models. It's like a standardized thing. Everyone recognizes it, and everyone uses it.

### 2. Custom Evaluation Sets

And second — sometimes, rather than a benchmark, you also build your own evaluation sets to test an LLM. Data you assemble from your actual task, which measures what you specifically care about rather than what's generically useful.

Now this is a very important point. Understand it. I just said an important point — that model evals are of two types. One is benchmarks, which are basically standardized tests that test specific capabilities — like math capability, or reasoning capability, or instruction-following capability. And second, sometimes you also run custom evaluations on your own model, because you need to find out how your given LLM's capability or performance will be on your specific application.

Now obviously, a question can come to your mind — if I'm getting standard answers on questions from a benchmark about how good it is in math, reasoning, coding, then why do I need to run my own custom eval separately? Let me answer this question.

## A Practical Scenario: Model A vs Model B

Let's take a small scenario. If you remember, in the first session, we discussed that we built a system for Zomato that reads the content of an incoming email and tells whether it should be routed to billing, or there were other categories too. Suppose billing, technical, refund — three categories. Ignore that. So basically, you have to build this application.

Now, to build this application, you have two model choices.

**Model A** is a proper big LLM — big, top of the leaderboard, but expensive. Here, using 1 million tokens roughly costs you $15.

**Model B** — you have a second, smaller model, and obviously cheaper. Here you pay just 50 cents for using 1 million tokens. And if you look at public benchmarks, this one comes mid of the table, whereas Model A is top of the table.

So imagine Model A is something like Claude's Opus type model, and Model B is something like a MiniMax or a Qwen small billion-parameter model.

Now common sense says — why are you overthinking this? Just directly deploy Model A. Model A will give good results anyway. But understand one thing — if you directly put Model A at Zomato's scale, the cost can rise a lot. So here, clearly, if you just go by benchmarks, Model A will be better than Model B on every benchmark. Right? Better at math, better at coding, better at language generation, better at everything. So here the obvious answer would be to use Model A.

But here, what would you do? You would simply do a small thing. You would build your own dataset, where you pick 200 to 500 past emails and label them too — whether the email is technical, billing, or refund. Basically, you're building a **golden dataset**, and you give this golden dataset to both Model A and Model B, and see the results.

So after the results came in:

- **Classification accuracy**: Model A = 94%, Model B is obviously a bit lower, but not by much. Surprisingly, since this task isn't that difficult, the second model also scores 91%.
- **Urgency accuracy** (reading the content of the mail and telling how urgently the user needs a reply): Model A gives 88% correct, and Model B gives 87%. Again, not much difference.
- **Cost**: For processing 1000 emails, Model A costs less than $6... actually less than $0.21 for Model B. [Note: exact numbers as spoken above.]
- **Latency**: Since Model A is a big model, it takes 4.1 seconds, whereas Model B takes just 0.9 seconds to serve a request.

Now, tell me — based on this table, logically, which model would you choose? Would you go for Model A, which is a bigger, more powerful model, or Model B? It's very, very simple, very, very straightforward that you will say — even though Model A is much more powerful and much better compared to Model B, for our task, Model B is a much better value proposition, because we're not losing much accuracy, but we're saving a lot of money and latency. So we will go with Model B.

Now think about it yourself — if we only depended on benchmarks, would we have ever reached this conclusion? Quickly tell me — if we only had the option of benchmarks, if we only did model evaluation through benchmarks, would we ever reach the conclusion that Model B is better? No. In every benchmark, Model A would beat Model B. But since we ran a custom eval on our own data, we found out that for our work, Model B is actually better.

So I guess it's clear to you now what a model eval is — a process of testing a model's capabilities, but you can test it in two ways. Either you run standardized benchmarks, which tell you the generic capabilities of the model, or you run specific custom evals according to your application, your data — so that you find out which model is more suitable for your kind of work.

Is this entire discussion clear — what model evals are and what their types are?

## What's Next: Two-Part Plan

Now what will we do? Today's entire discussion, today's entire session, we will spend on benchmarks. Because — what are benchmarks? How do benchmarks work? What is the evaluation process of benchmarks? What are the famous benchmarks? All this is also important to know. How to read benchmarks — all this is also important to know. And that's why we'll spend the entire session today on benchmarks.

So basically, today's session's name will be **"LLM Benchmarking."** And then the next session, we'll learn how you run custom model evals — how you can run your own evals on a given LLM. So we're dividing the whole thing into two parts. This is today's session. This will be the next session.

## Core Capabilities of LLMs

Before discussing benchmarks properly, first we need to discuss capabilities — what capabilities an LLM has, or can have.

So we discussed a little while ago that LLMs are like general purpose. This is the biggest strength of LLMs — that they are general purpose. You can get them to do different types of work. You can do text generation, sentiment analysis, summarization, parts of speech tagging — it can do a lot of things.

So it has a lot of capabilities inside it. And who tests these capabilities? Benchmarks. But before studying benchmarks, you should know what core capabilities an LLM has. Mostly speaking, what core capabilities exist.

So in total, there are **eight core capabilities** that everyone has agreed upon collectively. And most of the benchmarks you'll see in the future will fall under these eight categories.

So in the next 10 minutes, we're going to discuss all the core capabilities once. We've discussed this in the past too, but now we'll discuss it in a bit more detail.

**Disclaimer**: The entire discussion for the next 10 minutes will be a bit text-heavy — meaning there's a lot of text on screen, and I'll be reading quite a bit of it, because the explanation here is very well written.

### 1. Knowledge and Reasoning

Let's start. The first core capability is **Knowledge and Reasoning**. We've clubbed these two together because many times they work together.

I guess you already know what both mean. In this domain, two things come up:

- First, how much factual knowledge does our LLM have, which it learned during training.
- Second, is it able to connect that entire factual knowledge or not? Is it able to connect the dots or not?

These two things are measured under this capability.

What exactly is measured:

- First, your LLM's **factual recall** is measured across different subjects — like biology, physics, chemistry, history. In fact, there's a benchmark called **MMLU**, which evaluates the model across 57 subjects. So across all your fields of knowledge, you test whether your LLM can answer the basic, important questions or not. This is the first thing tested in the knowledge capability.

- Second is **multi-step logical reasoning**. Here you test whether your model is connecting multiple facts in the right sequence to reach a conclusion or not.

I'll give you a simple example. Suppose I asked it — summarize the entire human evolution. Analyze the whole thing from the Big Bang up to now, and tell me why today's society is the way it is. Now here you see multiple aspects, multiple things being tested about our model. First, we're checking its factual knowledge — does it really know what events happened from the Big Bang up to now, and in what order — and then it also has to connect all these things and tell what impact that entire thing had on today's society. So this is a proper task where both its knowledge and its reasoning are being tested. So this is what we check in the model. This is the first capability — Knowledge and Reasoning.

**Why frontier labs focus so much on this capability**: If your model scores well in knowledge and reasoning, it simply means how intelligent your model is. And that is why frontier labs care about this a lot. So whatever benchmarks you'll study, every model wants to score well on them, because this is what determines how intelligent a model is judged to be.

**Real-world relevance**: If you're ever building a research chatbot whose job is to analyze research papers and conduct new research — there, both knowledge and reasoning are checked. If you're analyzing complex customer questions — here I'm not really sure how much it's used, but okay, this is what's written. If you're analyzing technically accurate documents — you've uploaded a machine learning paper, now you're asking questions from it — reasoning gets tested quite a bit there. If you're building a chatbot that's helping professionals in their field — helping a lawyer in law, helping a teacher teach some subject — there again this capability is tested a lot.

So this is the first very important capability. As I said, this determines how intelligent a model is.

### 2. Coding and Software Engineering

The second capability is **Coding and Software Engineering**. In my opinion, if you ask me, this is the most important one from an economics point of view. This is where any model provider, any frontier lab, can earn a lot of money. I guess you understand — Cursor's valuation reached 60 billion, all because of this capability. Because LLMs can code. They can do software engineering tasks. And as of today, software development is a big, big field. If a model is doing well there, you are basically creating a lot of value for a lot of enterprises. So in that sense, this capability becomes very important.

What is measured here:

- Whether your model can write code that actually works — this is the basic question.
- Can you do real software engineering tasks or not?
- Can you edit large codebases or not? Which is measured by software engineering tasks.

What specifically comes under this:

- Can your model generate function-level code or not? You gave an English sentence saying, "build me a function like this in Python." So can it build that function or not?
- Can it generate test cases or not?
- Based on errors coming in test cases, can it improve the code or not?

All this comes under this. Second capability tested here — can you go into an existing codebase and fix bugs or not? This is also very important. Then, can you do multi-file, long-horizon engineering tasks or not? You were given a whole codebase and told to refactor the entire codebase based on some aspect. So can you do this or not? This is a capability.

Can you run multiple commands in the command line or not? For example, you were told to install some packages, configure some servers, and set up some environment. So is all this work being done by your LLM or not? This is a capability. Lastly, can you do API and function calling or not? All these sub-capabilities are tested here.

**Real-world relevance**: Whenever you're making any AI coding agent — which are now many in the world — you need this exact capability of your LLM. So in that sense, this capability is very important.

### 3. Mathematics

Third capability is **Mathematics**. Again, here you simply measure whether your model is doing accurate symbolic and numerical reasoning or not. Basically think of math as a form of reasoning. Math is a form of reasoning — that step by step, doing something, you're reaching a solution. So it's a form of reasoning. But this has more applications in the real world.

What's tested here:

- First, you test whether your model can solve grade-school level mathematics or not — seventh, eighth grade level mathematics problems.
- Can your model do competition-level problem solving or not — like problems asked in Olympiads, etc., where a bit of creative thinking is needed — can it solve that level of problems or not?
- Can it solve undergraduate level problems or not?
- And lastly, can it do research-level mathematical reasoning or not — some problems which are currently open-ended, whose solutions don't exist yet. Can it get there or not?

All these capabilities come under mathematics. And again, this is very important because there are a lot of fields touching this — like if you're building applications for scientific computing, financial modeling, engineering simulations, data analysis — for all these fields, your mathematics capability will come in handy. So again, this is a very important capability, and a lot of benchmarks have been built for it, because testing it is super important.

### 4. Long Context

Fourth one is **Long Context**. I guess you know what context means. Context simply means, while giving a particular answer, how much information your model is able to see, and it's limited. Today's models have up to 1 million token context windows. But even in that, is it able to use all of it or not? That's a big question.

**Definition**: This domain measures whether a model can effectively use information from very long inputs, sometimes containing hundreds of thousands of tokens.

What's measured here:

- Can you extract a small fact from a very long context or not?
- Can you fetch the details of some particular person or entity from a very large document or not?
- Can you summarize a very large context or not?
- Lastly, if you're working like a coding agent, can you maintain the whole context of a very large codebase or not?

These kinds of things are judged here.

**Why frontier labs care**: Because models claim their context window is 128k tokens, 200k tokens, 1 million tokens. But what actually happens is, as your chat grows bigger, you'll notice that the capability to retain context diminishes, decreases, and the quality of the chat degrades over time. So by testing this particular capability, it becomes clear which model actually performs well on large context. So this metric becomes very important, and it's applicable everywhere. Whatever kind of LLM-based application you build, long context will become an important capability to measure. From this only, you'll know how long a context is being handled by your model.

### 5. Vision and Multimodal

Fifth one is **Vision and Multimodal**. I'll summarize a bit and read through this. You'll get this document, you all can read it — it's written in a lot of detail. Here, simply, you go beyond text and go into the domain of vision.

The idea is — can your model understand vision or not? Can it understand images or not? Can it understand videos or not? And again, it is very important because we live in a multimodal world, and only text doesn't work anymore. As of today, we're immediately turning on video and asking — "hey, tell me, here's a fridge in front of me with all this stuff, tell me what can be made from this?" Or in a library, we're asking for a particular book. So we are living in a multimodal world. So there should be benchmarks to test multimodal capabilities too. That's why this is also a very important capability to measure.

### 6. Agentic and Tool Use

Sixth one is **Agentic and Tool Use**. Again, a capability that's becoming more and more important gradually. The entire field of agentic AI has emerged from this — that you don't just need LLMs that can print text. You need LLMs that can actually do things too. And to do that, what do you have to do? You have to attach tools.

So basically, here you have to test how effectively a model is using tools:

- Can it do web browsing on its own?
- Can it do structured tool calling?
- Can it interact with APIs?
- Can it use desktops and computers?

These kinds of things are evaluated here. You get these kinds of benchmarks here.

**Why frontier labs care**: Going forward, you're already seeing a lot of agentic applications. So to build these kinds of agentic applications, you need a reliable model that can do agentic tasks — and whether it can or not, that's told to you by exactly these benchmarks, this exact capability.

### 7. Safety and Alignment

Seventh one is **Safety and Alignment**. Again, very straightforward. Here, you simply measure whether your model can be trusted to behave responsibly.

So here you check several kinds of things:

- Whether it's not generating harmful content.
- Whether it's easy to do adversarial attacks against it or not.
- Whether it is truthful or sycophantic. You may have noticed that if you present an idea to ChatGPT, it immediately starts praising you — "yes, yes, this is the best idea in the world." It shouldn't be like that. Ideally, a model should be truthful. In my personal experience, I've always noticed that Claude is much more truthful than ChatGPT. ChatGPT flatters me a lot of times. Claude is more like — "no, what you said has this flaw." So this is an important thing.

Then, recently, it's being seen that such models and such benchmarks are coming up that check whether your LLM has cybersecurity-related skills or not:

- Can your model do cryptography or not?
- Can it do reverse engineering or not?
- Can it do digital forensics or not?

The Claude Fable that recently came out — this was a model that was very strong in cybersecurity, and it found out many vulnerabilities in existing software. So how would you test whether this model has cybersecurity-related skills or not? Separate benchmarks have come up for this too.

So safety is a very important thing for frontier AI labs, because governments pressurize them that your model should be safe. Along with that, it's also a very big reputational concern for them. If even a minor incident happens, their business can shut down. So in this sense, testing and measuring this capability is very important for frontier AI labs.

### 8. Instruction Following

And the last thing — a bit underrated, but very important — **Instruction Following**. This is also a very important capability. Here, you measure whether the model did exactly what the user told it to do, in the exact way it was told to do it, or not.

If I told the model to answer in a bullet list, did it do that or not? I said, answer in less than 200 words. I said, give a friendly answer. Is the model following all these things or not? This is also very important to test, because this directly translates into user feedback. If the model doesn't follow our instructions, the user will become unhappy, will leave the product, will go to another company. So in that sense, testing this capability also becomes very important.

So here again, I've written that whatever the user is saying, is it being followed or not? And if the instructions given by the user are ever ambiguous, does the model ask clarifying questions in return or not? These kinds of things are also tested here.

So this was a very detailed document. I'll give it to you tomorrow. You can read it yourself — reading it line by line would be a bit boring. So I compressed it into 10 minutes and explained it to you. But in a nutshell, these are the eight capabilities that every frontier lab focuses on, and whatever benchmarks you'll study in the future, they target one or the other of these capabilities.

### Summary of the Eight Core Capabilities

1. Knowledge and Reasoning
2. Coding and Software Engineering
3. Mathematics
4. Long Context
5. Vision and Multimodal
6. Agentic and Tool Use
7. Safety and Alignment
8. Instruction Following

This is what you have to study about core capabilities.

## A Note on the Teaching Approach

Because I'm a teacher, I understand a little bit — I feel like some of you might be thinking that this is the fourth session in this course, and so far we've mostly been studying theory only. You've gotten a bit bored. And is it even important?

Trust me, from my experience, I'll tell you that whenever I've taught complex topics in my life, whenever I've covered the theory well in overview mode, then the practical part that comes afterward — people have enjoyed studying that a lot more. Because they've gotten to look at things from multiple perspectives. Whereas if I start teaching you on day one how golden datasets are made, or which metrics exist, your mind will only learn as much as I teach you.

But now you'll observe yourself, within the next two sessions, when we do things practically — whatever you study, you'll understand all of it anyway, and on top of that, you'll also be able to ask a bit more questions, explore a bit more. This is the difference. And that is why I have opted for this method, where initially I'm covering a lot of theory, and I'm trying to make sure it's not too boring. But yes, I am covering a lot of theory compared to some other classes, companies, and YouTube channels, where from day one you're taught practical things.

And this is a conscious choice from my side. Now you can criticize me for this if you want. But I think this works. I've seen this in the past with multiple courses — whether it was MLOps or even deep learning. There, I spent a good amount of time on theory, which eventually translated into a good practical experience. So you have to trust me on this.