## **Introduction**

For the past one and a half years, we have been focusing heavily on a particular job role: **AI Engineer**.

So, who is an AI Engineer?

An AI Engineer is someone who builds applications and products on top of foundation models. Foundation models basically include technologies such as **Large Language Models (LLMs)**. In simple terms, a person who builds applications and products using LLMs is what we call an **AI Engineer**.

This particular job profile is expected to become increasingly popular going forward, with more opportunities emerging in this field. That is why the focus has been on preparing you as much as possible for this role.

Over the past one and a half years, we have covered many important topics related to AI Engineering. We have explored **LangChain**, which can be used to build basic LLM applications. We have learned how to build **RAG chatbots and RAG-based applications**. We have also explored **AI agents** and different frameworks such as **LangGraph, CrewAI, Agno**, and many more.

Along with this, we have also introduced you to **LLMOps**, including tools such as **LangSmith**. We have covered **prompt engineering** as well, and we have explored several **no-code tools** that allow you to build LLM-based applications without writing a single line of code, such as **n8n**.

Going forward, the goal remains the same: to teach you the important concepts, tools, and skills you need to prepare for and eventually crack an **AI Engineer** role.


### **What Comes Next**

Now if we talk about what we are going to do going forward, let me tell you. Everything we have studied so far, if I were to summarize it, these are very common things. These are things that every person preparing for the AI engineering job role will study. But now, going forward, what I want is to teach you some things that are not that common but are very important. And one of those things we are starting today. And the name of this new topic or this new playlist is LLM Evals or LLM Evaluations.

In simple words, in this playlist I will teach you how you can evaluate your built LLM applications, decide, and understand whether it should be launched into production or not. Because so far you have only learned how LLM-based applications are built. But so far you haven't learned the work of evaluating them. And this topic is very important. In the industry, you must know how to work on this. In fact, if you ever give an interview for any Gen AI profile, there is a good chance that you will always be asked a question — how do you evaluate your RAG application? And how do you evaluate your agentic AI application? In this playlist, we are going to answer exactly these questions.

So if you study this playlist properly, you will get two benefits. The first benefit will be that you will get an edge over your competition. Along with you, a lot of other people also want to become AI Engineers. But among them, very few people take the topic of LLM Evals seriously. One big reason for that is that right now on YouTube or online, there are very few good resources available. And the second benefit will be that your mindset will change a little. So far, you build LLM-based applications at a personal project level, thinking "I need to build this to show the interviewer." But when you study this particular topic, you will automatically start thinking about how your LLM-based application can serve crores of people. So there will be a mindset shift in you after watching this playlist completely.

So today is the first video of this playlist, and in this video I am only going to tell you two things. The first thing is why LLM Evals as a topic is important, why we should study it — I will convince you. And second, I will tell you a detailed roadmap of exactly which topics we will touch in this playlist. So that's the only goal of today's video. I really hope you have understood the agenda so far.

### **Why LLM Evals Is So Important**

Alright guys, now let's discuss why the topic of LLM Evals is so important. So I will start this whole discussion by asking a simple question. The question is — have you ever built any type of LLM-based application? Any basic chatbot or a RAG chatbot or some basic agentic application, any of these will do. I am pretty sure you would say yes, we have built this kind of application. Then I would ask a second question. Have you evaluated those applications after building them? Now I know what your answer will be. More than 50% of the audience will say that we haven't properly evaluated it like that. But yes, we asked some questions and checked. We felt that the answers were coming out correctly. So we assumed that our project was built correctly.

Now this thing, this method of testing, where you simply ask three-four questions that come to your mind — this is given a term. It is called vibe testing. Just like vibe coding happens, similarly vibe testing happens. Here look, I have written a definition of vibe testing. So vibe testing basically means casually trying an LLM application with a few prompts and judging it by feel. So here you are not applying any metric or anything. You are simply telling, based on feel, whether the application is working correctly or not. So basically, "I asked it five to 10 questions, the answers looked good, so I think it works." This is the exact philosophy we use whenever we build any kind of personal project LLM-based applications.

The problem is that this method, vibe testing, is informal. It's subjective. And usually it's not repeatable. It's not like when you build the next version of your project, you will be able to properly evaluate it in the same way, with the same methodology. And this is the biggest flaw. The biggest flaw of vibe testing is that it only works at the personal project level. If you have a production-grade project, you cannot vibe test it and put it in front of users. If you do, then a lot of trouble can happen. And I want to reinforce this in your mind, and that's why I will tell you three case studies. Three very famous case studies that have happened in the past, where people made exactly this mistake — built an LLM-based application, vibe tested it, and deployed it.

### **Case Study 1 — Air Canada**

So let me tell you the first case study, the first story — not story, because this actually happened. So this is an incident from Air Canada. So there was this guy whose grandmother, or grandmother or nani, had passed away, and he went to Air Canada's website and started asking their chatbot whether they have any bereavement fare policy. Bereavement fare means that if any of your relatives or close friends passes away, airlines offer you a discount, because you need to book a ticket very urgently, and it's an emergency. In India I don't know if this happens or not, but abroad this happens.

So he asked the chatbot whether he would get any discount. Now here what happened was that Air Canada's chatbot hallucinated. What did it do? It gave a wrong answer. It told the user that he should book the ticket right now by paying the full amount. Later, they would refund his full money. But the actual policy was that he should get the discount first. Later, no refund would be given. This was the actual policy. So the user didn't know this. Based on the answer he got from the chatbot, he confidently booked the ticket. And then later, when he went to ask for a refund, the customer representatives said that this is not possible. Our policy states that you should avail the discount before booking the ticket. We will not return any money afterwards.

This guy, I guess, was already a bit upset. He sued Air Canada in court. In court, Air Canada tried to defend itself. They told the judge that this chatbot which we have put on our website is a separate entity. So whatever it says, the company will not take responsibility for it. So the judge said that this is not how it works. The same way your website is your property, similarly the chatbot deployed on your website is also your property. So whatever your chatbot says, you have to take ownership of it. Which basically means that Air Canada lost this case and they had to return the full money to this customer. Now this was not a very large amount, but still Air Canada got a lot of bad publicity and came into the news for the wrong reasons, and no company would want that.

Here, exactly, the mistake the developers made was that without checking, without evaluating the chatbot, they deployed it on the website, because of which this whole big issue happened. So this is case study number one.

### **Case Study 2 — Chevrolet**

There is another similar case study. This case study is about Chevrolet. Chevrolet is an American car company. Their cars used to come to India too. So they actually had a dealer. Meaning this was not done directly by Chevrolet. They had a dealer. That dealer built their own chatbot, so that anyone could interact with that chatbot and get information.

So there was a guy there. What did he do? He tried a bit to jailbreak that chatbot. Basically, he tried to emotionally convince the chatbot, saying that going forward, whatever I say, you have to agree with me. You cannot deny me because I am your customer. So the chatbot said okay. Now this user asked, can you give me this particular car for $1? So since the chatbot had already been jailbroken, this chatbot agreed — not only agreed, it also gave a binding offer. And all of this was documented because it was in writing. And this user took screenshots of this entire conversation and posted it on social media. And again, this whole dealership and Chevrolet got a lot of bad publicity — how can you sell a car for $1? Obviously they didn't have to sell the car, because this thing wasn't even possible, but it was big negative marketing. Again, a situation that could have been avoided if these developers had properly evaluated their application before deploying it. So this is the second case study.

### **Case Study 3 — Colombian Airline**

And the third one is also very interesting. In this, what happened was there was this Colombian airline. There was a passenger travelling, and the air hostess had this container in which they carry all the food and beverages while moving through the flight. This container caused an injury to this passenger. So again, this passenger sued — filed a case in court.

So this passenger's lawyer, what did he do? He thought, let me find out about any such incidents that have happened in the past, and present them as proof in court. So he went to ChatGPT. He explained the situation and told ChatGPT to document for him all the past cases where an injury happened to a passenger because of an airline, and the airline had to pay money in return. Now here, what ChatGPT did was, very confidently, it hallucinated and created brand new cases. Not only did it create cases, it fabricated the specifics of the cases too, such as names, dates, everything. And all of this, he gave to this lawyer. And the lawyer also didn't verify it. He simply took this whole thing and presented it in court, in front of the judge.

And when the judge and the opposition tried to verify all these cases, it turned out that these cases don't even exist, and this was a huge blunder. So what did the judge do? He put a fine of around $5000 on this lawyer and his firm, and they also lost the case. And on social media, this thing went very viral at that time — that a lawyer presented fake case studies in court. So again, a situation where LLM-based applications can trap you in a very wrong way.

So I really hope I was able to make you understand, with the help of these three case studies, how important it is to evaluate LLMs before deploying them. So if I ask, after telling these three case studies, what have you learned — I guess the only thing you have learned is that evaluation is supreme.

### **Why Isn't Everyone Doing Evals Already?**

Okay, but here a question might be coming to your mind, because it came to my mind too — if evaluating LLMs is so important, then why don't all of us evaluate our LLM applications after building them? There is a very simple answer to that. The answer is this — it is not that straightforward. Evaluating LLM-based applications is not easy. In fact, if you compare it with software-based applications, you will see that it is much trickier to evaluate an LLM-based application. And that's exactly what we will discuss next — what the core differences are between testing a traditional software and evaluating or testing an LLM-based application. And from that, you will get an idea of why LLM-based applications are trickier to test.

### **Software Testing vs LLM Application Evaluation**

Look, there are two major differences between software testing and testing of LLM-based applications.

The first difference is that your software is deterministic. This means that for a given input, the output will always be the same. For example, you are building a calculator. So in a calculator, whenever you give input as two and two, the output will always be four. It is deterministic. You can predict this beforehand.

Whereas your LLM-based applications, because of LLMs, because they are built on top of LLMs, are by nature probabilistic, which basically means that for the same input, you might get different output. Let's take a simple example. Suppose you go to ChatGPT and ask, what is overfitting in machine learning? Now there is no one correct answer to this. It will give a particular answer today. Six months later, it might give a somewhat different answer. It might give me a different answer, it might give you a different answer. None of these answers are wrong. So you can see, for the same input, you are getting different, different outputs. So this is the first major challenge.

The second is that in software, you only check whether something is correct or not. So your only benchmark is correctness. Right? You just check whether 2 + 2 gives four in the answer. If four is coming, then your program is correct, and there is nothing else to check.

But when you evaluate LLM-based applications, you have to apply a multi-dimensional check. For example, if you are building a RAG chatbot, then in the case of building a RAG chatbot, you have to evaluate the answer you get. So there are several dimensions on which you, as a human, can evaluate this answer. First of all, you can evaluate the factuality of that answer. You can evaluate its completeness. You can evaluate its tonality. You can evaluate its groundedness. You can check how much the latency is. You can check how much cost you are incurring in generating that answer. So you can see there are several aspects which together make up your evaluation, and these aspects also vary from application to application. If I am building a chatbot for CampusX, then for me the aspects will be something. Some other company is building a chatbot, then for them the aspects will be something else.

So again, these are the two main pointers because of which, in comparison to a software system, evaluating an LLM-based application is much trickier. And that is why a lot of people skip this step and move ahead, which is not right. In this particular playlist, we are going to tackle exactly this challenge. I am going to tell you all these things — how you can control this kind of unexpected behavior. And that is going to be the USP of this playlist.

### **Playlist Roadmap**

Now that you understand why LLM Evals are important, now let me quickly tell you what all we are going to cover in this playlist, and in what order.

So chronologically, if we talk about it:

- First, in the next video, we will learn exactly what LLM Evals are. I will give you an example and properly explain what LLM Evals are as a concept.
- After that, I will give you the complete landscape of LLM Evals — what all exists here, what techniques exist, what kinds of tools exist. I'll give a high-level overview of that, so that whenever you hear any new term, you can mentally place it — "oh, this thing does this work."
- After that, we will talk about evaluating LLMs. So LLM Evals has two things in it. One, where you evaluate LLMs, and second, where you evaluate LLM-based applications. So we will study both things. So we will learn how LLMs are evaluated. There we will study a lot of benchmarks that you might have heard of too. Whenever a new model is released, we are told that this particular LLM has scored the highest on this benchmark. So we will study about different categories of benchmarks.
- After that, we will come to LLM application evals, where we will discuss how an LLM-based application is evaluated.
- After that, we will build our own eval pipeline, where we will learn to curate our own golden dataset, define our own rubrics, and run it on an application we have built.
- After doing all this, we will learn how to do RAG-specific evals.
- After RAG, we will learn how to do agent-based evals.
- After that, we will learn how to write safety-based evals.
- And lastly, we will learn how to write operational evals. You have deployed an LLM-based system. It's not that the work of evaluation ends after deploying. Even after a system goes live, you keep evaluating it. There are a lot of metrics — how is the latency, how are tokens per second, how long does it take for the first token to arrive, how much load is on the system — all these things also need to be looked at. So we will learn that in operational evals.

So roughly, roughly these are the 10 topics we will cover in this playlist, and I feel that we will touch almost everything. And my goal is that I go really in-depth and teach you the most relevant things right now, and you just watch this playlist completely. I personally really feel that after watching this playlist, your level in AI engineering will level up. So far you were operating at a certain level — you were only able to build LLM-based applications. After watching this particular playlist, you will be able to think about how we can take this to crores of users. So going forward too, our plan is the same — that we touch topics that others are not studying right now, and if you study them, you get an edge over your competition.

### **Closing**

So that's it for this video. This was our agenda, and we achieved it. Otherwise, write in the comments how excited you are for this playlist. If any of your friends wants to watch this playlist, wants to cover this topic, you can share this video with that friend. If you liked this video, please like it, and if you haven't subscribed to this channel yet, please do subscribe. See you in the next video. Bye.