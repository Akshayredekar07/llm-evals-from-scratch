### **LLM Evaluations - Lecture Notes**

So now that we understand why LLM evaluations are needed, why they are important, and how LLM evaluations are different from software testing, let's move on to the main topic of the day - what exactly do LLM evals mean. We haven't discussed this in detail yet, we've only touched it from the surface. So let's go a little deeper into it.

---

### **What Are LLM Evals - The Definition**

Here I have written down a definition. I will first read the definition and then we will discuss the point.

So we can define LLM evals like this - **LLM evals are systematic, repeatable tests used to judge an LLM and LLM powered systems against a clear criteria.**

Basically, LLM evaluations are tests that we apply on LLMs as well as on LLM based applications, and there are three main aspects to this:

1. These tests are **systematic**
2. These tests are **repeatable**
3. These tests have **very clear criteria**

These three are very important pointers, very important characteristics of LLM evals. Let's understand them one by one.

---

### **Characteristic 1 - Systematic**

Systematic means that here you are not doing vibe testing. Like, five questions came to your mind, you asked them, you got the answer, you felt "yeah everything looks fine" - it doesn't work like that.

Here what you do is you create proper datasets, and in those datasets you try to cover every kind of edge case, so that you can properly test your chatbot or your LLM based system.

For example, if I'm building a chatbot for Campus X, what I will do is I will randomly pick up 100 real users who are chatting with my system, and I'll build a database of that chat, a dataset. And on top of that dataset I will do the testing, so that I get to see the actual real world behavior of my chatbot.

---

### **Characteristic 2 - Repeatable**

Repeatable means that tomorrow, if you change the prompt in your system, change the model, change the retriever, change the chunking strategy - change all of these things - even then you should be able to evaluate your system exactly the way you were evaluating it before.

So this is again one important idea, that LLM evals should be repeatable. The dataset you have, you should be able to apply it on any version of the software in exactly the same way, and extract results out of it.

This is very important, and this is exactly how you compare whether version one is better or version two is better. Because you have a test dataset - how much performance did version one give on it, how much performance did version two give on it. From that we understand whether the system is improving or not. So, it is repeatable.

---

### **Characteristic 3 - Clear Criteria**

The third, and most important thing, is that LLM evaluations depend on what criteria you want to base the evaluation on. Right?

For example, if I am building a chatbot for Campus X, there will be a lot of criteria based on which I would want to do the evaluation. First, obviously, the answer that is coming out should be correct. Second, the answer should be filled with simple explanation. Third, whatever explanation is coming should come from our own course content only. Fourth, it should be safe - there shouldn't be things in it which are unsafe, or which contain abusive language, or which have a threatening tone. None of this should be there.

So this is the kind of criteria you would define to evaluate the chatbot. Without criteria, you're just doing vibe testing. With criteria, you're doing a proper evaluation.

So in a nutshell, right now I've explained this at a very theoretical level, but don't worry - a little later we will understand this entire workflow through a proper example.

But at this point, if I would like to summarize - LLM evals are basically tests with the help of which you test LLMs or LLM based applications for some given clear criteria, and usually these tests are repeatable and very very systematic. This is what we've read so far.

---

### **Clarification - Evals Is Not Just a Metric**

Now here there's one more thing I want to clarify, because a lot of people have this doubt. I had it too, when I first heard about this topic. I used to think eval means metric, because I came from a machine learning, deep learning background. So there, what did evaluation mean? Metric. We used to say - how do we evaluate machine learning models? What did we talk about? We talked about accuracy, we talked about precision, recall. Those were metrics.

So in my mind there was this perception that LLM evals would also simply be a set of metrics based on which we perform evaluation. But this is not correct.

Right here, in this very first lecture, I want to tell you one thing - evaluation, or LLM eval, does not just mean metric. It is basically the **complete testing setup**. The entire setup that we create to test LLMs, that entire testing setup is what we call LLM evals.

So what are we evaluating? Let's say if you have a RAG chatbot, and we want to evaluate the retriever inside it - then the retriever component becomes a part of our LLM evals. What criteria are we evaluating it on - how accurate is the retriever, based on that we are evaluating.

The dataset we prepared for evaluation - that is also part of LLM evals. When are we running this test - are we running it offline, or are we running it after it's deployed in production - that is also a part of this setup.

After that, which tools are we using. Let's say we're using Ragas because it's a RAG application - so this tool is also a part of your LLM evals.

So in a nutshell, if I simplify this entire discussion - just understand that whenever someone asks you "what is LLM evals", you should say that LLM evals does not just mean metric. LLM evals means the entire testing setup. What are we testing, on what basis are we testing, when are we testing, which tool are we using to test - all of this combined together is what we call LLM evals.

Is this point clear? This might feel a little confusing to you, but is this point clear - that LLM evals is not only metric, it is basically the entire testing setup?

And the goal of LLM eval is not to give you a score. Its goal is to answer practical questions for you. What kind of questions? Here look, it's written down:

- Can the model be used for a particular task or application?
- Is this system good enough to ship? Can we put this into production?
- Did prompt version two improve over prompt v1?
- Is the RAG answer grounded in retrieved context?
- Is the agent completing the task correctly?
- Is the chatbot safe for real users?
- Is the latency under control?

This is the kind of questions you get an answer to when you evaluate LLMs. LLM evals answers these kinds of questions.

So in a nutshell, we've covered a lot of theory right now, but don't worry - even if this hasn't fully clicked at this point, a little later we will revisit this entire thing through a practical example, and everything will make sense, don't worry.

---

### **Two Types of LLM Evals**

Now, before we discuss how LLM evals exactly work, there's a very important distinction I want to tell you about. This distinction being clear in your mind is very important - it will help you a lot going forward.

What is this distinction? Today, you can divide LLM evals into two parts. One we call **Model Evals**, and the second we call **Application Evals**.

Model evals are the evals with the help of which we evaluate LLMs. And application evals are the evals with the help of which we evaluate LLM based applications.

If you go back to the previous slide, read the definition there once again - what did it say? "LLM evals are systematic, repeatable tests used to judge an LLM and LLM powered systems" - both are written there. And that is why, based on this definition, we can say that there are two types of LLM evals. One we call model evals, the second we call application evals.

Model evals' job is very simple - to evaluate a given LLM. And application evals' job is to evaluate the entire LLM based application.

And this distinction, if it becomes clear in your mind right from the start, that's great. In fact, let me also give you a disclaimer here - the disclaimer is that these terms written here, "model eval" and "application eval", are not official terms. I have created these. Why did I create them? Because I want to simplify this topic in your mind. So don't quote me tomorrow saying "model eval" is a term, "application eval" is a term. In the industry today, both are still just called LLM evals combined together. And then, depending on the use case, people automatically and implicitly understand whether it's talking about model eval or application eval.

So this is a disclaimer I'm giving you in advance.

---

### **Model Evals - Explained in Detail**

Now let's try to understand both types of evals in a little more detail - what exactly does each of them do.

First, let's talk about model evals. Here's a definition written - **model evals evaluate the model itself.** Simple. Their job is to evaluate the LLMs themselves.

The main idea is to test and evaluate the capabilities of a model. This kind of eval has one single goal - when a new LLM is released, we test what capabilities this new LLM has, and we benchmark it, we document it.

You might have noticed this too - whenever any new LLM is released, it is said something like "on this particular benchmark or this particular leaderboard, this LLM came on top." It has this much accuracy, it's at this percentage. Have you seen this? Have you ever noticed this? Whenever these new releases happen, you see that these users always quote these benchmarks and leaderboards, saying "on this particular leaderboard or benchmark, this LLM topped."

So what's actually happening there - some evals are kept ready, already built. As soon as a new LLM comes into the market, we test that LLM on those evals to find out the capability level. And then we document the same thing and publish it on the internet, which tells us how capable an LLM is.

---

### **The Eight Capabilities Tested in Model Evals**

Now the question comes - what kind of capabilities can we test? So today's LLMs are majorly tested on eight capabilities.

1. **Reasoning** - Can our LLM reason? Can it think step by step and solve a problem or not?
2. **Knowledge** - Does our LLM have basic world knowledge or not? General knowledge or not? This is where we talk about the cutoff date - all the world's knowledge before this cutoff date should be with the LLM.
3. **Basic Math** - Can our LLM solve math problems or not?
4. **Coding** - Can our LLM code or not?
5. **Instruction Following** - Can our model follow instructions or not? If I give it 10 instructions to follow, will it follow all of them one after another or not?
6. **Long Context Handling** - Can our LLM pull out correct answers even from a very large context or not?
7. **Multimodal Understanding** - Does our LLM have multimodal capabilities or not? Can it understand images, text, sound, or give output in those forms or not?
8. **Tool Use** - Can our LLM properly utilize tools or not?

These are, as of today, the eight main capability categories on which every new LLM is evaluated, and then documented and talked about.

---

### **Benchmarks Used for Model Evals**

And this entire evaluation is done on the basis of benchmarks. Here I've written some example benchmarks. We won't discuss all benchmarks right now, but for example:

- If you want to check general knowledge and reasoning of a model, there is a famous benchmark called **MMLU**, which asks questions across a lot of subjects - science, history, law, medicine - it will ask your LLM questions from these subjects and record and evaluate it.
- For math, there's a benchmark called **GSM8K**, which asks grade school math questions and evaluates the answer based on those.
- For coding, **SWE-bench** - you might have heard of it, it's a very famous benchmark. There's also **HumanEval**.
- For instruction following, there's **IFEval**.
- To check long context, there's a famous benchmark called **Needle in a Haystack**.
- To check multimodal capabilities, there's a benchmark called **MMMU**.

So in a nutshell, if I summarize the discussion so far - we divided LLM evals into two parts, model eval and application eval. Model eval is used to test the capabilities of LLMs. And which capabilities - for now we've read about these eight capabilities. And how are these capabilities tested - with the help of benchmarks.

---

### **Why Model Evals Matter Less for an AI Engineer**

Now this is our next lecture's topic, where in an entire lecture I will teach you about the most popular benchmarks - how they are applied on LLMs, how results are extracted from them - this entire workflow I will teach you. So you will basically get a pretty good idea about model evals in the next lecture.

But here I want to clarify one thing - if you are going to become an AI engineer, then you won't work that much on model evals, because think about it - a new LLM comes out, evaluating it, benchmarking it, documenting its evaluations - this is not your job. This is the job of big frontier labs. When they bring out a new model, they will test it on these benchmarks and they will tell how their new LLM is.

You just need to know what model evaluation is, what benchmarks are, and how to read benchmarks. The benefit of this will be that tomorrow, when you pick a new project, since you have the idea of how to read benchmarks and you have the knowledge of which model tops on which benchmark, based on that you will be able to make better decisions about which LLM you should use in your LLM based application. So you'll feel a bit more literate if you know this topic.

But it doesn't mean that you will ever have to practically run these evaluations. There's a good chance you never run model evaluations, but you should know about them. You should know how to read them. You should know about top benchmarks - because as a project developer, one very important job of yours is that when you're starting a project, you also decide whether you need OpenAI's LLM, or Anthropic's, or maybe even some open source LLM would work for you - and this decision making comes from model eval only.

So is this clear so far - LLM evals, two types, model evals and application evals. We just discussed model evals.

---

### **Application Evals - Explained in Detail**

Now let's talk about the second category, that is application evals. Before discussing this category, I want to tell you one thing - this is the category you need to study well. This should be your topic of interest, and this is the category which you will do practically.

Because your job as an AI engineer is to build LLM based applications. So evaluating them is also your job. So application eval is the main topic of this playlist. In this entire course, we will focus more here. There will just be one dedicated lecture on model eval, and that too because I want you to understand how model evaluation works - you should have understanding, you should have literacy about it, that's it.

---

### **Why Application Evals Exist**

Application evals exist because, in LLM applications, the LLM is just one component. If you think about it, we feel - especially beginners feel - that LLM application means LLMs are the main thing, if the brain itself is that, then everything is about LLMs. But that's not the case.

As you get a bit more experienced in AI engineering, as you build slightly bigger applications, you would realize that yes, the brain is important, but apart from that there are a lot of other things you need to put in, so that your LLM based application works correctly.

Here I've made a list of all these things:

- Your user interface is one thing
- The prompt you write, the system prompt, that's one thing
- If you add tools, APIs to it, that's one thing
- The code you've written to orchestrate the entire system - let's say in LangGraph - where control goes from here to here, where branching happens, then control goes in parallel - this is also a thing
- The guardrails you put at the application level, that's also a very important thing
- If you're using output parsers, that's one thing
- Memory and context - what can I even say, super important
- If you're building a RAG system, there's a separate system for retrieval, you use a separate embedding model, there are vector databases
- After deploying, there's the entire monitoring setup
- There's the entire feedback loop

So you might understand that when you build a proper LLM based application, the LLM is just one component there. Apart from that, you have to put in a lot of other things there. And that is why application evals is such an important topic. Just model evaluation is not enough. Model evaluation just tells us how capable the model is. But this entire system that you've built around it, that also needs to work correctly.

---

### **The Smartphone Analogy**

A very good analogy is smartphones. In smartphones, what happens - there's a chip, whichever chip manufacturer's it is, Snapdragon, MediaTek - and you'll see that these chip manufacturers, what they do is they release benchmarks saying "our new chip has come, this has this much score" - from this we get to know how strong our processor is.

Now tell me yourself - does a good processor being there guarantee that your smartphone will also be good, or do other things also matter? Can you tell me? Is it enough that your processor is strong and then your smartphone is assumed to be strong too, or does building a smartphone also need other things?

Obviously, building a smartphone needs a lot more things, right? Your camera system is one, your operating system is one, your sound system is one, your graphics card is one - there are a lot more things. And all of them need to work well together for your smartphone to be good. Just a good processor doesn't do anything. Battery is also one important thing. So all these things work together, then your smartphone runs well.

So since there are so many more things - if you've put in a battery, you'll test the battery too. If you've put in a graphics card, you'll test that too. You'll test the screen too. The same thing applies here too - the evaluation of LLMs is being given to us by frontier labs. But the entire system we've built on top of it, the entire responsibility of evaluating that is ours as an AI engineer. We do that evaluation.

---

### **Definition of Application Evals**

So here's what the theory says: **application evals assess the behavior and performance of an LLM powered application, whether at the level of the entire system or a specific component within it.**

What do application evals do? They evaluate at the component level as well as at the entire system level. So if you've built a RAG chatbot, you will evaluate the entire RAG chatbot too - how is its final response, how is the latency, how is the cost per token - and you will also evaluate it at the component level, like whether my retriever is working correctly or not, whether my embedding model is working correctly or not, whether my reranker is working correctly or not.

Do you get my idea? So here it's written - in application eval, we don't ask "can the model do this" - that's the job of model evaluation. Instead, in application eval, we ask - will our product work correctly or not?

For example, if you're building a chatbot for Campus X, application evals will give us answers to these questions:

- Was the student's question answered correctly?
- Was the course material properly used?
- Was the answer faithful?
- Was the answer easy for a beginner to understand?
- Did hallucination happen or not?
- Was the answer received quickly or not?
- Is our chatbot safe or not?

I hope you understood what application eval is and what model eval is, and why we are going to talk about application eval throughout this entire course.

---

### **Summary So Far**

Is this entire discussion clear, everyone? I wanted to clarify this upfront, and I really hope I was able to do that.

Going forward too, whenever you watch a video in the future on YouTube and it's titled "LLM Evaluation", you can assume that it's teaching you application evaluation, not model evaluation - most likely, 99% of the time. That's what you'll need to study.

So okay, if we summarize the entire flow so far - in this lecture, what did we do? First we discussed **why** - why are we studying this topic. Then we discussed **what** - what LLM evals actually are, and what their types are. We covered two types - model evals and application evals. So why and what should be clear to you by now.

---

### **What's Next - The How**

Now we move towards **how** - how are LLM evaluations actually done. And here again there's a disclaimer - the "how" that I'm going to teach you will actually be taught from the perspective of application eval, not from the perspective of model eval.