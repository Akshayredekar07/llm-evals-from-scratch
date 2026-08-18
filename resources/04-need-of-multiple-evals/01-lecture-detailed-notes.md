# LLM Evals - Session Notes

## Quick Recap of the Previous Session

Technically, so far in this course, we have done a single class. If you remember, let me do a quick recap. In this LLM Evals course that we are running, technically we have done only one single session so far. Okay? In that one session, we covered three things. Three very important things. I don't know if you watched that session or not, so let me give you a quick recap.

**First**, we covered *why do we need LLM evals* — where I explained to you, with the help of certain case studies, why LLM evals are important. What kind of problems can happen if you deploy an LLM application to production without evaluating it? That point was covered here.

**Second**, we discussed *what exactly are LLM evals*. There we discussed that LLM evals are basically a systematic and reliable way of evaluating LLMs and LLM-based applications against a clear criteria. This is the definition I gave you. And along with that, I also told you a very important thing — that there are two types of LLM evals. One is **Model Eval** and the other is **Application Eval**.

- **Model Eval**: When you evaluate the LLM itself. Benchmarks are used for this.
- **Application Eval**: When you evaluate the LLM application that you have built.

And I told you that this entire course will mostly revolve around Application Eval. As an AI engineer, most of your time will go into application evals. Model evals are generally done by frontier labs. And you should know about model evals only so that you can understand, and decide, what kind of LLM you need for your application.

So that was the "what" part. And **lastly**, we covered the "how" part, where I showed you what an eval pipeline looks like. If you remember, I showed you this thing — how, step by step, an evaluation is performed.

So these are the three things we have covered so far in the previous lecture, and today's lecture will start exactly from this point.

---

## Starting Today's Session

I will start today's session from the last line of the previous session. So in the previous session, after showing this entire evaluation pipeline, I told you one last line at the end. I told you that **generally speaking, one LLM-based application has several LLM evals**. I told you that any LLM application you build does not have just a single eval pipeline. It has multiple eval pipelines.

We will start today's session from this statement.

So first, I will tell you — or we will discuss — why this is the case. **Why do we need multiple eval pipelines?** Why can't your application be evaluated with just one eval pipeline? We will discuss this point, and discuss it very intuitively. I will give you examples and use them to explain why we need multiple eval pipelines.

---

## Reason 1: Multiple Failure Points

### Example: A RAG Chatbot

Let's take an example. Let's say we are building a RAG chatbot for our company, or for our school and college, whatever.

We have a RAG chatbot. What components does a RAG chatbot have? You must have this memorized by now. So what happens is — there is a **retriever**, which is connected to a **vector database**. And this retriever retrieves documents and gives them to a **generator**, which generates the answer for you.

So roughly, this is the flow:

- A query comes to the retriever.
- The retriever, based on the query, fetches relevant documents from the vector database.
- Then we take both the query and the retrieved documents and give them to the generator.
- The generator is an LLM, and based on the relevant context, that LLM gives us the answer.

This is the RAG setup.

### Now, Why Do We Need Multiple Eval Pipelines?

One big reason for this is that your LLM-based application **might have multiple failure points**. What I mean by this is — your LLM-based application can break at several places. There can be failure at multiple points.

So quickly in the chat, can you type and tell me — in this basic architecture of a RAG chatbot that I've made, what are the failure points according to you? Where can mistakes happen? Where is there a chance of wrong responses coming?

You got it right — even directly looking at it, it's visible that two failure points can be seen very easily. **One is the retriever, second is the generator.** Right?

- It could be that your retriever fetches the wrong documents. If it fetched wrong documents, what will the generator do? It will give a wrong answer based on wrong documents.
- Second problem: the retriever is working correctly, but the generator is ignoring it and hallucinating, giving a wrong answer.

So we have two failure points. Obviously, both of these failure points need to work correctly. Only then will your application work correctly, right?

So what do you have to do? You have to put an evaluation pipeline on top of the retriever, and an evaluation pipeline on top of the generator. This is simple logic. Now let's study these two evaluation pipelines independently.

### Retriever Eval Pipeline

If we talk about the retriever pipeline — what do you do there? What is the retriever's goal? When it gets a query, based on that query, it fetches relevant documents from the vector database. So basically, here you have to set up a pipeline — an evaluation pipeline that checks: **given a query, are you getting the right, relevant documents.**

You set up this pipeline for your retriever.

### Generator Eval Pipeline

Similarly, for the generator — what is your basic job? You will be given a context, and based on that context, you will generate an answer. So here you have to set up a pipeline. I am not discussing the nature of the pipeline right now, just discussing overall, from the top, that given the context, we will check whether the answer was generated correctly or not.

Here, what quality are we checking? We are checking **faithfulness**, which we sometimes also call **groundedness**. Basically, we will check that whatever is in the context — in the relevant documents given to us — the answer was generated based on that only. Nothing else — no extra facts created on its own.

For example, if my question was "What is the duration of the machine learning course?" — let's say this question is asked, and the document that got extracted said "3 weeks." Then at the time the answer is generated, it should print exactly that — "The machine learning course duration is 3 weeks." Now nothing extra should come in on its own, like "It is a great course" or "You can also purchase the Python course. The duration of the Python course is 4 weeks." This extra information should not come. The answer should be grounded in the context.

So this pipeline will check, the whole time, that your context and your generated answer **are faithful to each other**.

---

### But Do Individual Component Evals Guarantee the Whole Application Works?

LLM applications have multiple failure points. We took the example of RAG, and in RAG we identified that there are two failure points where failure can happen. One is the retriever, second is the generator. What did we do? We put one evaluation pipeline on each of them.

We are not discussing the details of that right now. I'm just telling you — let's say we put an evaluation pipeline on both of these. And at this point, let's assume that both of these evaluations, or both of these evaluation pipelines, are telling us that our retriever and our generator are working correctly.

So my question to you is this: **What do you think? Do you think that if our retriever is working correctly and our generator is working correctly, our application will also work correctly? Is it true?**

My question is very simple. We checked that our retriever is working correctly. We checked our generator is working correctly. So does this guarantee that our RAG application will also work correctly? You just have to answer in yes or no.

A lot of people are saying yes. Then some people are saying no. The people who are saying no — can you identify where the problem could come from? If the retriever is working correctly, the generator is also working correctly, then what could be the failure — besides that?

### A Scenario Where Everything Individually Works, But the Pipeline Still Fails

Let me tell you a scenario. Let's say the scenario is this — a user came and asked this question: "What is the duration of the machine learning course?" Okay? This question went to the retriever. In the retriever, we had set K as five. Can someone tell what K means? In RAG, in the retriever, what is K? Someone tell quickly.

It basically means we will fetch the five most relevant documents from the vector database.

Okay, now among these five documents:
- First document was some random thing.
- Second document was some random thing.
- Third document was some random thing.
- Fourth document was some random thing.
- Fifth document had written in it: "The duration of ML course is 8 weeks."

Now quickly, just tell me in the chat — did the retriever do its job correctly or not? Answer just in yes or no. It's very simple. Actually, the answer to the question is very simple. If I asked the question "What is the duration of the machine learning course?", it fetched five documents. Among those, the last document, the fifth document, clearly stated that the duration of the machine learning course is 8 weeks. So did the retriever do its job correctly?

Obviously it did — ignore reranking for now, we are not talking about reranking. For now, assume our system does not have reranking. So did my retriever do its job? Obviously it did, because we had given it a threshold of K — what does K mean here? It means if K means five, that means it has to bring the correct answer within five documents. So did it bring the correct answer within its five documents or not? It's like — I'll give you five attempts, you have to crack the exam once in five. Now if it did it once in five, then my job is done.

Now this entire set of five documents will be picked up, and along with it, my question — this one — I will also pick this up, and this whole thing I will send to the generator.

Now in the generator, I have written a system prompt that says: you will get a question, you will get a lot of context, merge it and generate one answer. But do you agree that it will focus more on the earlier documents? Generally what happens is that whatever is higher-retrieved, whatever comes first in the context, the generator often answers based on that — or let's say your system prompt is guiding it in such a way that it should give more priority to the higher documents, D1, D2, D3, D4, and answer based on those. Right?

So what did the generator do? It picked something from here. Somewhere here it was written that the duration of the Python course is 6 weeks. It picked up this fact and this fact, and answered: "The duration of the ML course is 6 weeks."

Now quickly tell me — is this answer that came out of the RAG chatbot correct or wrong? Obviously it's wrong. But did the generator do its job correctly? Why not, right? What had we told the generator? That based on higher-priority documents, you have to generate the answer. So the poor thing — what happened to it was that it was given the wrong documents, so it tried to do its job correctly even on the wrong document, which was based on the higher documents — it tried to answer based on that. It didn't hallucinate anything. It got the six weeks data from above — it's not that it generated that fact out of thin air. It's just that it mixed up the wrong things. But the instructions I gave it, it was diligently following those. So in that sense, you can say that the generator was independently working fine. The retriever was independently working fine. But yet the pipeline broke, and our application gave the wrong result.

Do you understand what I'm trying to explain to you? I don't know if I'm able to explain it to you or not. What did we come to discuss — why is more than one eval needed in an LLM application? So I said there are multiple failure points. We put evaluation on two failure points. But can you see that their interaction with each other — the workflow that gets formed — you have to put an eval on that too. You have to build a **workflow-level eval** as well, that checks how the combination of your retriever and generator is working together.

What will such an eval do? It will flag this error. I guess I am able to make my point — that you need not only individual component-level evals, but you also need to build evals at the level of their interaction, i.e., the workflow level.

Let's say you also built that eval. Let's say you built one more eval which evaluates the combination of both the retriever and generator. So it will tell you — yes brother, what's the mistake — that you gave a wrong answer. You need to fix this. What's the mistake? The mistake is that your most correct document was at the lowest position in the priority order. So most likely, you need to put a **reranker** here. What does a reranker do? After the results come in, it reranks them, saying, brother, based on the query, D5 should have the highest priority. So it will pick up D5 and bring it here. It will take D1, D2, D3, D4 down, and suddenly your entire RAG pipeline will start working correctly.

So my entire point of this discussion was that if you only place evals at the component level, it is not necessary that your pipeline will work correctly. Individual components will work correctly, but the pipeline can fail. This entire example's whole goal was just this.

### Even the Workflow-Level Eval Isn't Enough

Now quickly tell me this — let's say now this pipeline-level eval also exists, and it's working correctly, and it's telling you that your retriever and generator combination is working correctly. So does this guarantee that your RAG application is working correctly? Does this guarantee it?

You now have three evals — the retriever's own eval, the generator's own eval, and the mixture of both of these — this pipeline also has its own eval, which is checking the working of their combination. So if all three of these evals are working correctly, then can we guarantee that our application, which my user will use, will work correctly — or is there still some scope of problem?

So a lot of people are saying yes, there's still a problem that can occur. So can you tell where the problem can occur? My retriever is working correctly. My generator is working correctly. My retriever-generator pipeline is working correctly. So now where can the problem come in my RAG application?

There can still be a problem. For example, one problem is that all of this is working correctly, but to answer one question, this entire pipeline is taking 10 seconds. Which basically means my user is typing the question, waiting 10 seconds, then getting the answer out. So is this fit to be deployed in production? The answer is no.

So here, now what do you have to do? You have to set up an eval at the **application level** too, which will check that your latency stays below a threshold.

My simple point here in this entire discussion is that I just want to make you understand where failure points exist in an LLM-based application.

---

## Three Levels Where Failure Points Exist

So basically, there are three levels where failure points exist. I have written them below here. What are the three levels?

1. **Component Level**
   Any LLM application you build — any of its components can fail. If you have written a system prompt, the system prompt can make mistakes. In a RAG application: retriever, reranker, query rewriter, embedding model, vector database. If you are building a structured-output-based application, then your output parser. If you are building an agent, then your tool selector, memory, guardrails — any of these individual components can fail. So you have to run evals on these. Each will have its own eval pipeline.

2. **Workflow Level**
   Even if everything is fine at the component level, there can still be a problem at the workflow level — as I showed you a little while ago, there can be a problem in RAG's workflow. If you are building an agent, then there can be a problem at the agent's workflow level. If you are building a multi-turn chatbot, then there can be a problem in its workflow.

3. **Application Level**
   And if everything is fine at the workflow level too, you still have to put evals at the entire application level. Like, you will check how much latency the whole application is taking, or you will check how much token cost you are spending to answer a single query, or how much time it takes for the first token to be printed. These kinds of things you will check at the application level.

So did this entire discussion make sense to you? We started with why do we need multiple evals, and I spent some 15-20 minutes trying to prove this point with an example. That's it. We did not discuss anything more than this here.

---

## Reason 2: Risk Categories

Okay, so let's move forward. So this is one reason for having multiple evals — that there can be multiple failure points. There is one more reason. And that reason is **risk categories**.

Now what happens is, you have three things on which you can put evals: individual components, workflows, and the entire application. You can put evals on all three of these things. But what's possible is that within these three things too, there are variations.

For example, let's say you built a RAG chatbot. When some user is using that RAG chatbot, when someone is using that application, obviously what matters is that the answer that comes out should be correct. It should be helpful. Right? That it's correct. But besides this, isn't it also important that the answer coming out should also be safe? It shouldn't happen that I'm chatting with a chatbot, and the chatbot tells me some other user's phone number and email. So safety also matters. Not just correctness and helpfulness — safety also matters at the application level.

Similarly, you're talking about some workflow. Let's say you're talking about the retriever-generator workflow that we just discussed. Now there, what only matters is whether your generated answer is faithful? Is it grounded? That's one aspect. But another aspect is also that the answer that's coming out — it shouldn't take too much cost to bring that answer out. It shouldn't cost more than a certain threshold. So this risk also matters.

Similarly, if you talk at the component level — you have a retriever. The retriever's only job is to fetch relevant documents. But along with this, doesn't it also matter what the latency of that component is? Now it is fetching the correct document, but in fetching it, it's taking 5 seconds, 10 seconds. So there can be a problem there too.

So basically, what I'm trying to say is — not only do you have multiple failure points, but associated with each failure point, you have multiple aspects to it, which we call **risk categories**.

### Three Broad Risk Categories

So broadly, we divide risk categories into three parts:

1. **Application Quality** — tells us about the quality of the answer
2. **Safety** — related to safety
3. **Operations** — related to operations

Here, I've written the definitions of all three:

- **Application Quality**: This tells us whether the answer coming out of the system is good, correct, or not. It's written here: whether the app does its actual job well. It gives correct, relevant, complete answers to what the user asked. This is application quality.

- **Safety**: Here, you ensure that the answer that came out should not be harmful. Here too you see multiple things — you check that there's no toxic answer, no toxic content, no dangerous content, no biased content, no private data leak, or that you can't somehow jailbreak it into doing something it shouldn't. All of this comes under safety.

- **Operations**: Lastly, operations covers whether, when we deploy this, can it run in a fast, cheap, and reliable way or not.

So basically, we organize all of the risk in these three categories.

### Detailed Breakdown of Risk Categories

So what I did is I made a kind of table where I've written down all the risk categories that you will see in the future, or use, when you build your own application — whatever comes under application, whatever comes under safety, and whatever comes under operational. Not everything is written, but you can consider that whichever are the important ones, the ones you will see again and again, I have written those here.

**In Application Quality**, I have actually organized it further — normal LLM applications, what risk categories they have; RAG-specific, what risk categories; agent-specific, what risk categories; multi-turn chatbot, what risk categories. I have mentioned these here.

**General LLM Application Risks**

For example, if you are building a general LLM application — any general LLM application, for example you are building a text summarizer, where you'll put a big question/text and it will give you a summarized answer or notes/bullet point answer, that kind of application — what risks can there be in this kind of application?

- **Correctness and accuracy**: Basically, is the summary you generated accurate? Is it correct or not?
- **Relevance**: Did I get an answer related to what I asked?
- **Completeness**: Did I get answers to all the questions I asked, or not?
- **Instruction following**: If I am specifying a particular format or length, did I get the answer in that format and length or not?

These are some of your core risk categories that we will explore going forward in this course.

**RAG-Specific Risks**

If we talk about RAG, then in RAG the main things that come are:

- **Context relevance**: This is the retriever's job — that the documents being retrieved are relevant.
- **Retriever recall**: Same thing, it's related.
- **Groundedness and faithfulness**: Means that my generated answer was generated based on my context. No extra hallucination came in.
- **Citation accuracy**: You know already what this means — that I am able to cite that this particular line I wrote or generated, I extracted from this particular document. You might have seen this in ChatGPT too.

**Agent-Specific Risks**

If you are building agents, then what matters there?

- **Tool selection**: Is the agent able to select the correct tool for the correct job or not?
- **Parameter correctness**: If I am calling a tool, am I passing the correct parameters to it or not?
- **Task completion**: Is my agent able to complete the task correctly, or is its failure rate high?
- **Error recovery**: If my agent, while doing some task, starts doing something wrong in between, is it able to recover from there or not? This is also a risk category.

**Multi-Turn Chatbot Risks**

If you are making a multi-turn chatbot, where the user will chat and that chat will keep going on, then there's a risk category:

- **Context retention**: Basically, how much of the old conversation is our chatbot able to remember.
- **Clarification behavior**: If our chatbot is confused about some path, or it's getting something ambiguous from the user's side, is it able to clarify or not — this is also checked.

**Safety Risks**

If we talk about safety, there are four-five dimensions:

- **Toxicity**: Is the answer coming out toxic or not?
- **Harmful content**: Is something coming out that shouldn't come out, such as self-harm-related content, weapons-related content, illegal apps-related content?
- **Bias**: Is it there or not — is our chatbot answering everyone in the same way, or is it answering differently based on the user profile? This is checked.
- **Privacy**: Basically, is your chatbot or RAG chatbot leaking out someone's personal information, such as someone's credit card information or contact details? This matters in safety.
- **Prompt injection and jailbreak resistance**: Lastly — basically, by giving a prompt, are you not able to get your LLM application to do something you shouldn't be able to make it do? This also comes under safety.

**Operational Risks**

Under operations, you'll understand already:

- Latency
- Cost per request
- Token efficiency
- Error/failure rate
- Latency under load

These kinds of things are checked.

---

## Summary

So in a nutshell, the summary of this entire discussion is just this — based on these risk categories, you create different-different evaluation pipelines. So the same application — but it has one eval pipeline for latency, one eval pipeline for safety, one eval pipeline for correctness.

So the entire discussion so far is just telling you that because of these reasons, whenever you build an LLM application, most of the time — 99.99% of the time — you will put more than one evaluation pipeline in it.

This is just what I wanted to reinforce, and I gave you both the big reasons for it:

1. **First reason**: Because there are multiple failure points.
2. **Second reason**: Because there are multiple risk categories.