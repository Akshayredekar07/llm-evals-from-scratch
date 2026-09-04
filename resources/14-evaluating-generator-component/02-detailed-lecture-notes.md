# **RAG Generator Evaluation**

## **Plan of Action for Today's Session**

So guys, let's discuss the plan of action for today's session first. If you remember, two classes ago we started RAG eval. We made a very detailed plan for how we will evaluate a RAG application, and in that detailed plan, currently we are only doing one thing: we are building a RAG eval suite for our RAG application. Basically a set of evaluations that we can run together and get the evaluation of our entire RAG application done. This is what we're building, and we're building it at three levels:

- Component level
- Pipeline level
- Application level

In the last session, we started building at the component level. I told you that in RAG there are only two components: the retriever and the generator. In the last session, we completed the evaluation for the retriever. We tracked two metrics, Recall and Precision, and both of those were completed.

So today's plan is this: we will learn to evaluate the generator, and then, in this same session, we will also learn to evaluate our complete RAG pipeline. These are the two tasks we need to complete in today's session. That's our plan for today. Okay? I hope the plan is clear.

## **Building the Generator**

Now let's move on to the start of the session. So first of all, if we need to evaluate the generator, we first need to build the generator in our application. So the first thing we're doing is building a generator, okay? You should remember this: we discussed that we are not building the entire RAG application in one go and then testing it. We are building the RAG application component by component, and along with building each component, we are also testing it. Exactly the way it happens in software. We're using exactly the same format. We built the retriever, evaluated the retriever. Today we build the generator, evaluate the generator. This is how the process is going to be.

So, the generator is a very simple component. You probably already know the whole logic of a generator. In a RAG pipeline, the retriever's job is that as soon as it gets a query, it sends that query to a vector database, embeds it, and fetches back five or ten relevant docs. After that, in the RAG pipeline, what do you do? You take these five or ten relevant docs along with the question and send them to the generator. And what is the generator's job? To generate an answer based on this question and the relevant docs.

So basically the generator is a function that receives two things as input: your question and these relevant documents, and it gives you one thing as output: the answer to your question. Okay? So basically we need to build this component today. A very simple component. It basically just uses an LLM. That's it.

So again, I won't write the code from scratch because it will take time. Instead I'll use the code I've already written and pushed to Git. This is the same repo I showed you in the last session. I've pushed new files into it today as well. So if you go into `src` here, you'll see a new file called `generator.py`. As soon as you click on it, here's your generator code. Very simple and neat code. Let's quickly go through it.

- First, we imported the libraries.
- Called `load_dotenv` because we need the OpenAI API keys.
- Here we called an LLM. Our LLM is GPT-4o mini. It's cheap, and we set the temperature to zero. Most of the time, during evaluation, we set the temperature to zero. Although this is the process of building the RAG, but whatever.
- Now here we built a prompt for our generator. Very simple prompt: "You are a helpful teaching assistant for a course on LLM evaluations. Answer the student's question only from the context provided below."

We gave a few rules:
- Use only information present in the context, do not add outside knowledge. Obviously RAG chatbots answer only from context, not from their training knowledge, so we explicitly wrote this.
- If the context does not contain enough information to answer, say "I don't have enough information in the course material to answer that." So we straight up said do not hallucinate no matter what. If you don't know, just say you don't know.
- And lastly, keep the answer clear and concise.

Along with this, we're providing the context that we're getting from the retriever, and the question that the user is providing. And here we built a simple LangChain chain. We get the prompt, we send it to the LLM, and whatever response comes, we put it in a string output parser to extract the string. Here we built a simple `generate` function which receives two things as input, query and context, and in return gives us our answer, which is what the generator will generate. And this is the code simply to test it. You can ignore this too.

So we'll just use this simple code. I'll copy this, go into my code, and in `src` I'll create a new file named `generator.py`, and paste the same code there, and save it. Okay? Simple.

### **Testing the Generator**

Let's run it once and see. So what's written in the code to run it? We basically created a dummy context ourselves. This is not coming from the retriever. We're generating it ourselves. And we made up a question according to our choice: "What is online eval?" And we passed the context to the `generate` function. With the help of these two things, the LLM will generate an answer for us. Let's quickly try this.

So if we go to the terminal and run it, now this code is running, and hopefully we'll get an answer. Okay, here it is, "online eval means evaluating your system on live production traffic after deployment," it worked without an error. Unlike offline eval... okay guys, right from here it gave us the answer. So it clearly shows that our code is working. We haven't proven anything more than that. So, in a nutshell, we've created our generator and it is working. Whether it's doing a good job or a bad job, we don't know that. We'll find that out by evaluating it. But we have built the generator. Now we will evaluate it.

## Failure Modes of the Generator

So now the question comes: if you have a generator, how do you evaluate it? See, whenever you want to evaluate any system, what's the thinking approach? The first-principles approach is that you think about where and how that system can fail. Basically you find the failure modes of that system. So if we need to evaluate the generator, we'll first discuss the failure modes of the generator, i.e., what are the ways in which the generator can fail.

There are two major ways in which the generator can fail.

### **Failure Mode 1: Unfaithful Response (Faithfulness)**

The first way is that your generator gives an unfaithful response. What does unfaithful mean? You gave the generator a question, and along with it you brought some context, and you said, "look, here's the question, read this context, and answer this question based on this context." But what mistake did the generator make? It read the context, but it also added a little bit of information from its own side. This is called an unfaithful response.

Here's an example. "Does the Campus X AI Engineering program include live classes?" This was the question the user asked. The context we fetched is: "The AI Engineering program includes recorded lessons, coding assignments, projects, and weekly doubt-solving sessions." But nowhere exactly is it written whether there are live sessions or live classes or not. The rest of the things are written in the context. Now here, look at what answer is coming: The answer is "Yes. The program includes two live classes every week along with weekly doubt-solving sessions."

Now you tell me, is this answer faithful with the context or not? You can clearly see this is not faithful. The LLM is hallucinating and it is creating a response from its own end. When it didn't get the answer in this context, it created the answer with its own freedom. This is what we call a hallucinated response or an unfaithful response. And this is very, very dangerous, because if this thing is in your RAG application, it can create massive problems.

Which we saw in the past too, in the examples, when we discussed that Air Canada case study, where Air Canada's chatbot just said, "you go ahead and book the ticket, we'll reimburse you the money later." So this was a generator problem. The generator failed there. It ignored the context and created information on its own and gave it to the user in front. So this is a very, very dangerous situation. This is something you need to avoid.

So, this metric that tests this thing, we call it **Faithfulness**. In simple words, how faithful your generated answer is towards your context. This is what is measured with the help of faithfulness. I really hope I was able to explain this to you.

Here's an important point too: many times it will happen that the context you retrieve and bring is completely wrong. It happens, your RAG chatbot's retriever fetched the wrong context. So what will a correct generator do? It will create the answer from that wrong context itself, even if that answer is completely wrong. So here's an important thing you need to remember: being faithful doesn't necessarily mean that your answer is also correct. Being faithful only means that whatever context has come, right or wrong, I will create the answer entirely from that itself. Apart from that, I will not add even a bit of information from my own side. This is the promise of faithfulness. I really hope I was able to explain this to you.

So faithfulness, as a metric, we will evaluate on our generator. This is our first key metric.

### **Failure Mode 2: Answer Relevance**

Apart from this, there is one more failure mode. One more way in which the generator can fail. How? Imagine again, this is your question: "Does the Campus X AI Engineering program include live classes?" And this answer got generated: "The program includes coding assignments, projects, recorded lessons and weekly doubt-solving sessions." Okay? This is the question, this is the answer. Now first tell me, in yes or no, is this answer faithful to the context? Here's the context, by the way. Is this answer that got generated faithful?

I guess you're able to see that the answer is fully faithful to the context. Whatever it got in the context, it prepared the answer from that only, almost word by word the same. So clearly this answer is faithful.

Second question: is this answer relevant to the question? Think about this and tell me. Is this answer relevant to the question? Is it answering the question that the user asked? The answer is no.

So this is also a failure mode: that many times it will happen that the generator will generate the answer sticking to the context, but that answer itself won't be relevant to answering the question. That is also a failure mode, because in this case too the user didn't get their answer. Ideally, a relevant answer would be if the generator printed: "The provided context does not confirm that the program includes live classes. It only mentions recorded lessons, coding assignments, projects and weekly doubt-solving sessions." Now this thing, at least, is relevant. The answer is relevant to the question, and along with that, it is also faithful, because it's not creating any information on its own.

So this is the second failure mode, where the answer came from the context, but that answer itself is not relevant. So this is called the second metric, and its name is **Answer Relevance**.

Apart from this, there are also other metrics that you test on the generator, such as citation accuracy, completeness, correctness, all these things exist too. But we will test these at the application level, not right now. Okay?

So right now our goal is this: we will evaluate our generator on two things. First, we will evaluate it on faithfulness, which basically tests whether the answer we generated is derived from the context, or is our generator inventing something different. And second, we will test answer relevance, which basically means whether the answer that got generated is relevant to the question or not, whether it is correctly answering the question or not. We will test these two quantities. Okay?

So next our goal is to fully understand how these two metrics are calculated. So far we discussed what metrics we'll evaluate. Now we'll discuss how, i.e., exactly how faithfulness is calculated, how answer relevance is calculated. And then we'll implement it in DeepEval and run it to see whether our generator is really working correctly or not.

## **How Faithfulness Is Calculated**

First, to calculate faithfulness, we need a dataset. Now where will that dataset come from, we'll discuss that a bit later. For now, let me tell you what that dataset will look like.

So this dataset will have two columns. The first column will be "question," and the second column will be "golden context." These are the two columns. Now let me explain to you what will be in these two columns.

So basically there will be a question here. Simple question. Let's say the question is "What is the RAG Triad," which we discussed in some session. Now what will be in its corresponding golden context, let me tell you. So someone will go through our entire chunks in our vector database, and go pull out the chunks where the RAG Triad has been discussed. And they'll put all those chunks here.

Then similarly we'll take another question: "What are online evals?" And here too we'll again go and search for which chunks discuss online evals, and we'll bring all those chunks here and keep them. And we'll do this for 10, 15, 50 questions. Okay? So basically this is our dataset. In a way, this is a golden dataset. This contains our golden context. Okay?

Now the process is very simple. What you will do is you'll bring an LLM as a judge. You'll bring an LLM as a judge, and send it this first question. Okay? And this LLM, what will it do? First actually this LLM-as-a-judge will not come into the picture. First we will do this: we'll take this question and send it to the generator, and we'll also give the generator this golden context. Okay? So the generator always needs two things: one, it needs a question, second, it needs context.

Here's an important thing I'd like to clarify right now: since we are evaluating the generator in isolation, it means at this point this connection is not in the picture, i.e., that the retriever is connected to the generator. Which basically means the context we're sending to the generator is not coming from the retriever. We are testing the generator independently, in isolation. This is a very critical point. That is why what we're doing is: we are sending both the question and the golden context from within our golden dataset to our generator. Okay? What will the generator do in return? It will look at this question, look at this golden context, and generate an answer, right? Simple setup.

Now what will we do? We'll take this answer and send it to this LLM-as-a-judge. What will the LLM-as-a-judge do? It will break that answer into claims. Let's say it breaks into five claims. And now what will it do? It will take each claim and go check whether that claim exists anywhere in the golden context or not. Then it will take the second claim and again go check whether that claim exists anywhere in the golden context or not. And it will do this for all five claims.

Let's assume for a moment that the first claim existed in the golden context. The second one also did. The fourth one also did. But the third one didn't, the fifth one didn't. So how will faithfulness be calculated? You will simply say, out of five claims that were in the answer, only three were in the golden context. That is why for this question the faithfulness score would be 3/5, and you'll repeat this process for every question, and then you'll take the average score.

Exactly this same thing you'll see in this graphic. So here your question is "What does it mean for a benchmark to get saturated?" This question was asked, and this is the golden context we provided, not by the retriever, but by us, from within our dataset. This answer got generated. Now we broke this answer into claims with the help of an LLM-as-a-judge: claim one, claim two, claim three. Now what is that LLM-as-a-judge doing? Going and checking whether this claim exists in this golden context or not. It does, good. Second claim exists in the golden context? It does. Good. Third claim exists? It doesn't. Bad. So 2 out of 3, the faithfulness score for this particular question is 67. And you'll do this with every question in your golden dataset, and then you'll calculate the average. That's your faithfulness score.

So is this entire discussion clear? How faithfulness is being calculated, did you understand? We made a golden dataset. In it we kept questions, kept golden context. We sent both those things to the generator. The generator generated an answer. The generated answer was broken down into claims. And then, for each claim, we checked whether that claim is in the golden context or not, is or is not, is or is not. And finally, total number of claims divided by however many we found in the context, dividing that gives us our answer. This is how you calculate faithfulness.

### **A Question from Harry: Evaluating LLM Applications in General**

A question came from Harry. "Sir, is there any way we can evaluate LLM applications in general, other than RAG and Agentic AI-based systems? Example, an application which acts as an interview synth?"

Yes, yes, obviously, if you go into DeepEval, I'll quickly show you, just one second. Let's say you go into DeepEval, here you'll find metrics of every kind. Don't need agentic RAG, you can go to multi-turn. Suppose it's a chatbot, then for that chatbot these are the metrics you can use. And if there's something that's completely different, it's neither a chatbot nor a RAG application nor an agent, then you can also create custom metrics. We'll study that in the next class. So it's not that you can only evaluate RAG and agents. You can evaluate any kind of LLM-based application. It's completely possible.

And a few more questions are coming. "Do we pass a subset of the golden dataset and the full golden, or is this a completely new golden dataset that we've made specifically for calculating faithfulness?" So we calculate faithfulness score over this entire dataset. If there are 15 questions, we'll calculate it over all 15. If there are 50, we'll calculate over 50.

"Are we not checking precision recall for the generator?" No, no, no, this is not precision and recall. This is completely different. Actually, if you notice, recall is exactly the opposite process of this. What do you generate over there? You generate context and compare it to an ideal answer. Here it's exactly the opposite. Here you have ideal context and generated answer. Two completely opposite things. Calculating recall, calculating faithfulness, is like two opposite things. But yeah, if it triggered in your mind, that's a good thing. It basically means you are recalling. Meaning reconnecting to those things.

## **How Answer Relevance Is Calculated**

So now that we know how faithfulness score is calculated, let's focus on Answer Relevance. Answer relevance is a bit easier. Honestly, for answer relevance, you don't even need a golden dataset. You can work without a golden dataset. So in that manner we can say that answer relevance is a **reference-free eval**, because we don't need any references.

How does it work? Let me tell you. Very simple logic. What are you doing? You're sending a question and context to the generator. The generator is generating an answer. Now you bring an LLM-as-a-judge into the picture and tell it, "look, here's the question and here's the answer. What you do is, tell me whether this answer is relevant according to this question or not." How will you tell? Very simple. You break this answer again into claims. Claim one, claim two, claim three. And then compare each claim with this question and ask whether this claim is helping answer this question, or is it irrelevant? If it's helping, then we'll consider it relevant.

Is the second claim helping answer this question? Yes. Is the third claim helping answer this question? No. So two out of three claims are relevant. One claim is irrelevant. So the answer relevance score would come out to be 2/3 for this particular question. And you can do this for however many questions you want.

So here, you need a golden dataset only in the sense that you need some answers to be generated. But you are not using any aspect of the golden dataset as a reference. You're not referring back to say "look, this is correct." Please keep this point in mind. We need a golden dataset for generating multiple answers, but we don't need it for reference. That's the main difference. So we'll use the dataset here, but not as a reference. Okay?

Here's an example of this. Let's say again your query is "What does it mean for a benchmark to get saturated?" And this is your generated answer: "A benchmark gets saturated when model scores cluster high and close together, so it can no longer tell models apart. Separately, benchmark contamination happens when test data leaks into training data."

Now in this there are three claims. First claim is, "saturation is when all models start clustering, their scores start coming similarly." Statement two is "the benchmark cannot differentiate between two good models." And then there's a third claim, "benchmark contamination is test data leaking." So the first one is obviously relevant to answering this question. The second one is also relevant. But the third one is a bit off-topic. And that's why we'll call this irrelevant. And that's why the score would be 2/3, 0.67. And we'll do this for every question.

This is how you calculate answer relevancy. This is even simpler than the previous one. In this you didn't do any comparisons. You left it to one LLM's judgment to say, "you tell me, is this claim answering the question or not?" That's it. There isn't much more here.

So we discussed how both these metrics are calculated. Now next what will we do? We'll implement both of these using DeepEval.

### **Q&A: What If a Claim Point Is Missed by the Generator**

"Sir, what if some claim point is missed by the generator, then how to calculate relevancy?" Ok, so what if some claim point is missed by the generator. Then its relevancy will come out bad. That's the whole point, right? We want to judge whether the generator is good or bad. If it's missing good claims, it means it's bad. We need to evaluate that.

"The LLM which we will use for breaking into claims and the LLMs which we use to analyze the answer, are these the same?" No problem, both are the same. In DeepEval's implementation, the LLM that breaks down into claims and then analyzes each claim against the question, they are the same LLM. It's the same, so what difference does it make? No difference at all. Every LLM API call is independent anyway, right? We're not providing any context, first time we're using the same LLM to say "break down this answer," it did. It's an API call. In the next one, what are we doing? We're taking this question and taking this statement and telling the LLM to tell us whether this question and this statement are related or not. It's a separate API call. There's no context between the two at all. So it doesn't make any sense to use two different LLMs. Use one LLM that's good.

"Since it's LLM reasoning there will be chance of false positive and false negative, correct?" Yeah yeah, obviously, look, all these LLM-as-a-judge methods that we're discussing here, there's a very big chance here that your judge might also make a mistake. Obviously this happens. And, take this as given, if you remember, in the beginning, in our theoretical classes, every time we've studied that LLM-as-a-judge will be used, we've discussed there that you cannot completely rely on LLM-as-a-judge.

But the good thing is that if you run the same judge twice, both times the mistakes are the same, right? It's like if a pitch is bad for playing cricket, then it's bad for both teams. So that match's evaluation will also happen on the same basis. So similarly, if you run a faulty judge twice, at least it's faulty consistently. This bias is removed, right? Now it may be that ideally your application's faithfulness score should have come out 40, but because of your LLM-as-a-judge it's coming 30 in a particular run. So the next time you run it, it will also stay around 30. So you can compare two evaluations.

But yeah, this is true that LLM-as-a-judge can make mistakes. And there's only one solution for this, which is that you use a good judge. A powerful judge. Because it's not like you need to spend a lot of money on this, right? It's not like you're serving crores of users. No, you need to do testing on some samples. So use the best possible LLM you have for this. So there will be a bit of expense, but you'll have this security that in LLM-as-a-judge we're using a very powerful model.

"Final score would be average value as the number of claims may change?" Yeah, Aman, for what we just discussed, this was for one question. Like this we have 15 questions in our dataset. So each question will have a faithfulness score. Each question will have an answer relevance score. We take the average of all of them. So that's our final faithfulness score for the generator. Final answer relevancy score for the generator.

"Are the number of claims something we decide as a hyperparameter?" No, Rahul, I don't think so. So there's no such restriction that you decide how many claims to break down into. That is not a hyperparameter in my opinion.

"Sir, if for the same query, the generator gives statement two and misses statement one, which is the main answer to our query, and statement three is also there which is not relevant, then what would be the score in that case?" 50%. You made two claims, one was right, one was wrong, so 50%. Here we are not talking about correctness. Understand this: faithfulness tells you how faithful your answer is to the context, that is not correctness. Answer relevance tells you how relevant your answer is in answering the question. Again, relevant doesn't mean it's correct. Correctness is a different metric. We'll discuss that in the next class.

## **Building the Golden Dataset**

Now next step is, this dataset I talked about, where on one side there'll be a question and on the other side actually the golden context, how do you build this?

So what did I do? I simply exported my entire vector database, in which all the chunks were stored, I exported that whole thing. Okay? So if I show you here on GitHub, there's a code called "export chroma chunks." This is the entire code for how you can export the entire set of chunks in your vector database together. So I had about 862 chunks. I exported the entire thing into a JSON file.

And then what did I do? I took this entire JSON file and put it on Claude. And I told Claude to "create this dataset for me." But one important thing I said was, "create it step by step." Meaning generate one question and golden context pair at a time. So then it analyzed the entire 862 chunks and it generated the first question for me. I looked at the first question. I read the context that came out for it because I've taken all these classes, so I know when and where I've taught what. And when it felt right to me, then I added it into the JSON file. And doing this again and again, I made a dataset of 15 questions. And this is how you can do it.

- One method is manually
- Second method is with the help of an LLM, but you do the reviewing
- Third method is again DeepEval's synthesizer, which I showed you in the last class, but I haven't been able to use it properly yet, so in some future class I'll show you properly how to do it

But yeah, this is how I created this dataset. So this dataset, I guess, is here, if you go into "golds," here it is, "faithfulness_dataset," this is the dataset which has the question and then its ideal context. Okay? And like this there are 15 questions. See, there are 15 questions. Okay?

So again, I've verified it. You can also do this if you want. What will you do? You'll simply copy this file and go to your codebase, wherever all your golden datasets are. There you'll create a new file named `faithfulness_dataset.json` and paste it here, save. Okay? So this becomes our golden dataset.

## **Implementing the Generator Evaluation Using DeepEval**

Now we have our golden dataset. Now what do we need to do? We simply need to write a DeepEval code that will evaluate these two metrics for us on our generator. Okay? So again the code is very simple. Let me show you. The code you'll find here in the "evals" section. Here I've made a file called `eval_generator.py`. A very simple file, just like you saw for the retriever. Exactly the same file. Let's see what's in it here.

- First we're loading the golden dataset we just made, the faithfulness one.
- This is our judge model. We're using GPT-4o mini. You can use a slightly more powerful model if you want.
- We're setting a threshold. Below this we'll consider it fail. Above this we'll consider it pass.
- Here we're loading that dataset into a file object.
- Then we're running a loop in which each time we take a question and build an `LLMTestCase` object.

Now here look at the interesting thing, where are we bringing the query in the input from? From our golden dataset. Where is the actual output coming from? From the answer. And where is this answer coming from? Pay attention, from the `generate` function. And where is this `generate` function? This `generate` function is inside your generator. So basically we're giving the question and context to the generator. Here look, the question and the context, and this context is also coming to us from the golden dataset. We're sending both these things to the generator. The generator is giving us the answer.

So in the input, question went in from the golden dataset. In actual output, the generator's answer went in. And in retrieval context, our golden dataset's context went in, the ideal one. And then here we're defining two metrics. One is faithfulness and one is the answer relevancy metric. Both of these are built-in metrics of DeepEval. Here we're sending the threshold, sending the model, sending `include_reason` equal to true. From this we'll know if any test case failed, why it failed. And finally we're calling the `evaluate` function by sending all our test cases and metrics.

Exactly the same code that we saw in the retriever. Look, exactly the same code. Same code. There too we had two metrics and there was your evaluate function. Now I haven't added all these hyperparameters in evaluate. You can if you want. But yeah, this is the code.

So what I'll do is I'll copy this and here I'll go into "evals," and I'll create a new file named `eval_generator.py`, and here I'll paste this file. I'll save it and that's it. Now we're ready to run our first eval on the generator. Okay?

### **Running the Generator Evaluation**

So how do we run it? Again, `python3`, and we'll run this as a module. `evals.eval_generator`. Okay? And we'll hit enter, and our DeepEval will start its work on these two metrics. Let's wait and see what happens. Let me expand this a bit more.

Again one thing here I want to mention: at this point our generator is not connected to the retriever. We are evaluating the generator in isolation. So the golden context, the context, is coming from our dataset. Not coming from the retriever. Okay?

Two test cases, somehow, I don't know, in a live class two, one test case takes a bit longer. When I test normally, not with a live class running, everything is much faster. This happened in the last class too. I don't know what the problem is. Maybe the system takes a bit more load when a live class is running. It's not a money problem. I recharged my OpenAI wallet, where you use the API, with $10 today itself. So I have enough credits. So this time is due to something else.

### **Results and Improving the Prompt**

So, guys, here's the output. Here are our aggregate metrics. Faithfulness is quite good, around 91%. But the answer relevancy is not that great, coming in at 73. Okay? So we need to improve this. So let's have a discussion about how we can improve this.

First, let's have a simple discussion about why the faithfulness score is coming out to be 91, which is quite good. Why did it directly come to 91? Why not lower? Can anyone think and tell why, without tweaking any code, without doing any effort, the very first time we run it, it came to 91 directly? Anyone want to answer?

The reason behind this is very simple. In faithfulness, there isn't really that much effort needed. Think about it, what are we doing? We have an LLM, which is our generator, we give it a question and we give it a context, and we give this LLM the instruction, "please answer this question with the help of this context," and here we get our answer. So obviously the probability is very high that this answer was made from this same context. Because today's LLMs have quite high instruction-following capability, right. So if I give it a context, give it a question, and tell it to answer from this exact context, there's a good chance that the faithfulness metric will come out good.

Answer relevancy is low, whatever it came, because now we are asking whether the answer that got generated is relevant to the question or to answering the question or not, right? So I hope you understand that scoring on faithfulness is kind of easier compared to answer relevance.

### **Improving the Generator**

Now comes the question, how do we improve the generator? How do we increase its answer relevancy? See, there are two-three ways to improve the generator, like we saw ways to improve the retriever. Does anyone remember, in the last class we discussed. How to improve the retriever? Can anyone tell? What were the ways we discussed in the last class to improve the quality of retrieval?

What was the first thing we tried? Obviously first you can change your chunk size and all. Apart from that you can change the embedding model. Apart from that, what else? You can add a reranker, right? So these were three-four ways with the help of which you can fix a retriever.

In the generator, you actually don't have that many options. The two biggest options are these:

1. You switch to a better model, one that gives you better instruction following.
2. Second, your system prompt, the generator's, matters a lot here.

This prompt we've written, if you go to generator, `src/generator`, this prompt, I'll just zoom in a bit. This prompt matters a lot. If you tweak the prompt properly, you'll be able to bring better results. So that's exactly what I did too. Right now I can't show you all the tweaks exactly because I did multiple runs, and in every run I tried to improve the system prompt. Let me show you the final version.

So what did I do? After running it two-three-four times, I analyzed all these results, which test cases are failing and what reason it's giving, and I put all this into an LLM, and slowly I refined the prompt. So after refining three-four times, I got this prompt. This was the prompt, okay? This wasn't made in one go. It was made over three-four iterations.

Let me copy this once, and go back into the code. And this existing simple prompt we have, let's replace it. So here you'll see, first of all the rules got a bit more, and all these rules got added slowly. Looking at each individual failed test case, I did refinement and added some points.

- "Use only information present in the context, do not add outside knowledge." This was there before too.
- "Do not strengthen or overstate claims. If the context says two different things are different, do not upgrade that to separate methods and strong wording."
- "The context is an informal lecture transcript, synthesize and rephrase what is there."
- "Do not require the question's exact wording to appear."

So basically what I'm saying is that I did multiple runs, the test cases that were failing, why were they failing? I took that reason. I put this entire context into an LLM, into Claude, and slowly, over three-four iterations, I improved the system prompt. And this was the final one that gave me the best results.

So what I'll do is I'll save this code, and once again I'll show you running the evaluation with this new system prompt. Let's see if this brings an improvement.

By the way, one thing I didn't discuss with you, when you use the `evaluate` function of DeepEval, if you have 15 test cases, they are used in parallel. They are run in parallel. It's happening in parallel, not sequentially. That is why evaluation is very fast. This is one thing you should know.

So, guys, here's the output. You can see, this is our output. So by tweaking this system prompt, our faithfulness score increased further, 96. And our answer relevancy also increased quite a bit, 0.92, which is a very good score.

So that's what I'm saying, if your generator isn't giving good results on these two metrics, you don't have many options really. You can tweak your system prompt to a good extent, and you can switch to a better model. If you use a good model, both these quantities will automatically improve.

So yeah, this is the prompt that gave me this score, and there's still one test case failing. We can analyze that too and improve it a bit more. But again, if you tweak your entire system prompt too much according to just the golden dataset, it can be kind of an overfitting, that on your test data it's giving good results. But when new data comes to you, new retrieved context comes from the retriever, when you connect it, your faithfulness score might just drop. So we'll test that later, when we build the pipeline, what happens. At that point, the retrieved context won't be coming from the golden dataset, it'll be coming through the retriever. So there we'll find out whether this system prompt we wrote was only giving good results on our test data, or is it giving good results on our overall pipeline too.

I'll tell you in advance, it will give a good score on that too, because this is kind of a general kind of system prompt we've made. But yeah, in a nutshell, this is the improvement. You can improve the model, you can improve the system prompt. We improved the system prompt.

So yeah, I'll come back, and with that, we can go to the plan of action slide and say that we've done both these components. We've learned to evaluate both of these. We've evaluated both the retriever and generator at the component level. So this part is complete. We learned four metrics: recall, precision for the retriever, faithfulness, answer relevancy for the generator, and we're done.

### **More Q&A**

Now we'll move on to the next level, which is pipeline level. These are all reproducible results, by the way. If you run on your machine too, there'll be a bit of plus-minus. It's not like if I'm getting 96 here, you'll see 76. On your machine too, it will give you similar kinds of results. Obviously it changes a bit because LLMs are probabilistic, but the difference won't be very large.

Is the entire discussion, the entire narrative clear in your head? What did we start doing? We came to evaluate the RAG application. Then we discussed that we need to build a RAG eval suite. We're building that eval suite at three levels. Of that, we completed the first level. In that process we studied four new metrics. We implemented them on DeepEval.

"Sir, can we do the entire evaluation using open source models including generation of golds? I saw rate limiting issues when trying to generate golds." Yes, there are rate limiting issues for certain models. You can tweak that in settings, or you can use slightly smaller models. If you use GPT-5 here, actually sorry, where, I was also getting that issue, it limits how many parallel LLM calls you can make at once. On GPT-4o mini this restriction wasn't there. So I'm doing it with GPT-4o mini. But you can do it with GPT-4.1 or 5.6. You'll need to check some settings in your OpenAI dashboard.

But if you want to do it completely open source, Himanshu, is there an option that you run open source models on DeepEval? Have you ever done it? If you're in the chat, tell me once. So Himanshu is saying, "set a sync config, there is a way but a lot of glue code." Okay. Yeah, that's it. Meaning there's some way for sure. So this is the advantage. Look, with open source libraries, this is the advantage that you can tweak quite a lot at your own level. But let's go, I'll show you some demo in the next class.

"We do recall and contextual precision for retriever and answer relevancy and faithfulness for generator. Is it true always for all RAG apps, or can change as per use cases?" No, no, for RAG this is true. In fact, that's why if you go to DeepEval's documentation and select RAG there, you'll only see five metrics there. Out of those five, we've done four already. So you'll see answer relevancy and faithfulness. We've done both of these. You'll see contextual precision, contextual recall, which we've done. One is left, contextual relevancy, which we will do shortly. So these five are your core metrics. Apart from this there are other metrics too, like how you define correctness, or how you define styling, how you define completeness. All these things exist too, we'll see them in the next class. Those are custom metrics you build according to your own needs. There a concept called G-Eval is used. Here, look, it says G-Eval. We'll use this. This is next session's topic. So mostly the standard metrics are these that we're discussing right now. Whatever RAG application you build, these four will always be there.

"When we changed multiple prompts, should we save all prompts and their scores, is there an option to?" Yeah, this option is there right? What can you do? Confident AI, if you look here, there's an option that comes up. I haven't shown you this yet, because it actually doesn't matter for us. But if you look here, there's an option here, "run deepeval view to analyze and save testing results to Confident AI." If I want, I can run this command right now, and this entire run I just did, I can store it in Confident AI, which is DeepEval's own parent company. So whatever prompt changes I made, every run, I can save it. So in a way you can do experiment tracking. Let me show you how it's done.

### **Experiment Tracking with Confident AI**

`deepeval view`, we ran this command. Now it brought me here. This is Confident AI. This is the parent company of DeepEval, this is their library. And here what did it tell me? It logged me into my account, and now it's asking me for my API key. So where's the API key? We do it here within the project. "Test 3, create, copy." This is my last try. If this works this time, okay, otherwise we'll look at it more carefully again. Again the same project opened. And this time we made an API key for this same project. It worked. So yeah, look at this, whatever evaluation we just ran, that whole thing has been logged into Confident AI's dashboard. So you can see, tests passed 14 out of 15, whatever failed is here. Clicking on this, you can basically see everything. You can evaluate every individual row. Here, along with this, you can also store your configs. Which system prompt did you use? What was your chunk size? All these parameters you can store with this run. So in a way you're doing experiment tracking. Which you did in MLflow. Same thing is happening here. So I guess you got the answer to your question. This took a bit more time than needed. But you can do it.

This is a bit of the LLM Ops part, rather than the pure hardcore evals we're studying. This isn't part of that. This is connected to what Himanshu is teaching. But I guess Himanshu is using MLflow for this. But Confident AI has this option too.

## **Building the RAG Pipeline**

Now what do we need to do, our retriever is built already, our generator is also built already. And the good thing is both of these are also working correctly. Now what do we do? We connect these two. And as soon as we connect them, our RAG pipeline will be complete. Okay? And then what will we do? As soon as this RAG pipeline is built, then we'll evaluate this entire RAG pipeline as a whole. Basically we'll evaluate it at the pipeline level. Okay?

So now step by step, what's our work? Step one is first to build this pipeline. First we'll build this pipeline. Then in step two, what will we do? We will evaluate it. Okay, this is our step-by-step process now.

So building the pipeline is very simple. You need to connect these two components. These two files, you need to connect them and convert them into a single component. It's very simple. You've already done it too. So if you go here, in `src` you'll find `rag_pipeline.py` again, where a very simple code is written. What's written?

- First we're bringing the retriever from here. We're using the reranking retriever.
- We're bringing the generator from here.
- And here we're building a class named `RAGPipeline`, and inside the RAG pipeline we're simply doing this: step by step, first with the help of the retriever, we fetch the context, and we convert that context into a string, and then we send that context and that question to the generator, from which we get an answer, and we return that answer, and here we've basically tested that same code.

I guess this makes sense to you. Simple. Brought the generator. Brought the retriever. Took a question. Sent it to the retriever. Retriever gave context. Took the context. Took the question. Sent it to the generator. Generator gave the answer. Displayed the answer. This is the code. Basically glue code. It's code that connects both of them.

So we'll copy this, go back into our codebase, and inside `src` we'll create a new file called `rag_pipeline.py`, and paste this code there, save, and run it once to see.

### **Testing the Pipeline**

Okay, so let's say this question was asked: "What is drift and why does it matter after deployment?" This question, actually, will now go to our real retriever. It will fetch context from there, and then send the question and context to a real generator, and the generator will generate an answer for us. So this is like the real thing. This is our application that we just created.

So let's run this once and see. So what we need to do is we'll simply write `python3`, and we'll run this again as a module because we've taken imports. And we'll run `src.rag_pipeline`. And we'll get our answer to this question. Here it is. This is the answer. This was the question, as it is. This is our answer, and these are the chunks that got retrieved. These five chunks got retrieved. So you can actually read: question was "What is drift and why does it matter after deployment?" The answer is, "drift refers to the gradual change in a system's performance and the relevance of its evaluation setup over time, particularly after deployment. It matters because as a business operates," whatever it is, not showing correctly but you can read it. And this was produced from this context. Okay? It basically means our RAG pipeline is working fine. Not throwing any error.

So if I go back to our plan, we can say that we have successfully built our retriever, RAG pipeline. The pipeline is working fine. Now what do we need to do? We need to evaluate it. We need to evaluate this pipeline at the pipeline level. Okay?

## **Evaluating the Pipeline: The RAG Triad**

So is this clear? How we built the pipeline, is this clear? Right at the start I want to clarify, we are not evaluating at the application level. We are evaluating at the pipeline level. Which basically means we need to evaluate a RAG pipeline. And if you go on the internet and search once for "how do you evaluate a RAG pipeline," you'll only see one keyword, which we call the **RAG Triad**. This is what the evaluation of a RAG pipeline is. What is it? Let me tell you again quickly, I've told you before in the past.

There are three things. First you have a question that the user asked. You sent that to the retriever, and the retriever generated context. And then, with the help of that question and context, an answer got generated. Now on the combination of these three things, three metrics exist. Now you tell me, which metric exists on the relationship between question and context?

Let's leave that one for the last. Tell me this, which metric tells the relationship between answer and context? We discussed this today. Answer and question context. Is our answer, which came out, derived from the context? Yes or no? Which metric tells this? No, no, think carefully. Is the answer built from the context or not? This is told by faithfulness, right? We studied this today itself. Faithfulness.

Next, is the answer we got related, relevant to the question? Where does this get told? Answer relevancy. Just discussed. And third, the context that got generated, is that related or relevant to the question? Here comes your third metric, which we call **Contextual Relevancy**. Combining all three metrics, we call this the RAG Triad. If we're doing well on all three of these metrics, it means our RAG pipeline is working fine. This is the basic logic. Okay?

Now here's a quick question for you. Okay? If you've followed everything so far, you'll be able to tell. We also calculated faithfulness at the individual component level when we were evaluating the generator, and calculated answer relevancy when we were evaluating the generator. So can you tell me how this pipeline-level faithfulness and answer relevancy is different from what we just discussed at the component level? Aren't both these things exactly the same? Faithfulness we just calculated a while ago. Answer relevancy we just calculated a while ago. So why are we calculating again? What's different?

Prem said it exactly right. This time the context is different. Last time when we were discussing at the component level, where was the generator getting context from? From our golden dataset. But now since the pipeline is built, where is that context coming from? That context is coming from your retriever. And that's why things will be different. Here when you calculate faithfulness and calculate answer relevancy, these will give you different scores, right? I hope you understand this. This is the main change between pipeline level and component level. Okay?

But again, the way to calculate is exactly the same. How will faithfulness be calculated? Exactly the same, everything. The only difference will be that this time, instead of the ideal context, you'll use the retriever's context. That's the only difference. And answer relevancy is the same anyway. Whatever answer got generated, and whatever the question is, we're sending it to the LLM-as-a-judge.

### **How Contextual Relevancy Is Calculated**

The one metric we haven't discussed yet is Contextual Relevancy. Let's discuss this once, how it's calculated. Then we'll have all three metrics of the RAG Triad. Okay?

So what is contextual relevancy? In simple words, we see how relevant the context that my retriever pulled and gave me is, to answering the question. How is it calculated? Let me tell you.

So basically, let's say you have a retriever. What did you do? You gave the retriever a question, and that's it. You'll only give it a question. The retriever doesn't need anything else. And what did the retriever produce in return? Context. Let's say K = 5, so it fetched five contexts.

Now what will we do? We'll again do the same work. We'll bring an LLM-as-a-judge, and we'll give it the first out of the five contexts and tell it to break down this first context into claims. So claim one, claim two, claim three, like that. Then we'll break the second context into claims too. Break the third one down too. Let's say in total we have 15 claims combined in our retrieved context.

Now what will we do? We'll individually pick up each claim and pick up the question, and ask this LLM-as-a-judge whether this claim is related or relevant to this question. Yes or no. So for these 15, you'll get a yes/no answer. First one, yes, related to the question. Second one, related to the question. Third one is not. Fourth one is. So we find out that out of these 15 claims that the retriever fetched, 10 claims are actually relevant to answering the question. So your contextual relevancy for that particular question will be 10/15, and you'll do this for multiple questions. So in our golden dataset there are 15 questions. We'll pick up all 15 questions and send them to the retriever.

So this is also a reference-free evaluation. Because again, we need the golden dataset only because we need some questions. And we don't need anything else. No need for any reference. So that's how you calculate contextual relevancy.

Is this thing clear? Is this thing clear? How contextual relevancy is calculated. Very simple. Pick up a question, send it to the retriever. Retriever will generate context. Break the context into claims. Pick up each claim, pick up the question, send it to the LLM, and ask whether this claim is related to this question or not. Do this for all the claims, and then you can calculate a ratio for how much contextual relevancy is there for that particular question. Do this for 10-15 questions, average it out, that will be your entire RAG pipeline's contextual relevancy. It's all LLM-as-a-judge, because these are like reference-free evals. So here you can't really do any other kind of evaluation either. You'll have to put in an LLM, or you can bring a human into judgment, into the picture, which would be costly. So yeah, LLM is the solution.

### **Implementing All Three RAG Triad Metrics in DeepEval**

So now that we're clear on how these three metrics are calculated, now what do we do? We'll implement all three using DeepEval. So now what are we doing? We'll build one more eval file. Again the file is on our Git. So if you go to evals, here you'll find a file called `eval_rag_pipeline`. Again very simple code, pay attention, this whole code is for importing things.

- Here we imported our RAG pipeline, which we just created.
- We need a dataset. That dataset is `faithfulness_dataset.json`. Same model we're using.
- Threshold is there too.
- Again what are we doing? We're loading our golden dataset, and for every row we're creating an `LLMTestCase` object.

Just pay attention here, what is the input? The question from our golden dataset. What is the actual output? What our generator produced. And retrieved context, this time look at what it is? Coming from our RAG pipeline. Okay? Last time what was it? If you go into the generator one, here what was the retrieved context? What was in your golden dataset. But in the RAG pipeline one, look, where is the context coming from? From inside your RAG pipeline, meaning the retriever is sending it. So it's simple. Question is coming from the golden dataset. Output is coming from the RAG pipeline, and context is also coming from the RAG pipeline. Okay?

And here we defined all three metrics because all three are built-in metrics. So we can define them. And then we called the evaluate function. Same format we're repeating. Nothing special.

We'll just copy this code and go into our project, and inside the evals folder we'll create a new file named `eval_rag_pipeline.py`, and paste it here. Save it. Saved the RAG pipeline too. And yeah, we're ready. We're ready to run our eval. Okay? Nothing to do. Again we'll run the same command. This time it'll be `eval_rag_pipeline`, and we'll hit enter, and let's see what scores we get.

### **Results and the RAG Triad Summary**

So yeah, guys, here's the output. This is the summary of our RAG Triad. Faithfulness, let me note it somewhere. Faithfulness is coming out to be 92, 93 actually. So this is a very good sign. Answer relevancy is also good. 87? No, 86, 86. But one thing that's not coming out good, and that is Contextual Relevancy. It's coming out to be just 43, 42.

One thing that's clearly proven, first of all, is that the system prompt we wrote for the generator, because of which the answer relevancy score went up, we've written that correctly, because even when we changed the context, now the context is coming from the retriever, still the answer relevancy score hasn't gone very low. So okay, this is fine.

## **The Curious Case: Good Recall and Precision but Low Contextual Relevancy**

The only problem in this entire evaluation piece is this. Now this is a bit of a curious case. It's curious because first of all, if contextual relevancy is low, can you tell me who is mainly responsible for this? Think and tell me. In the RAG pipeline, if contextual relevancy is coming low, who takes the core responsibility for that? Who will be the culprit?

The retriever, right. It's the retriever's responsibility, right. The context is being brought by it only. But the curious case is that when we evaluate the retriever independently. Let me show you once again, I'm running it again. We did this in the last class. Let me run the eval for the retriever, `eval_retriever`, which we built in the last class. Right now watch, this eval will run on two things: recall and precision. Let me take the recall and precision scores again at this same point. Does anyone remember how much came in the last class? Recall and precision, if you remember, because it should be around the same. Recall I remember was 90 plus.

Yo, nice. Look at this. So if I go back, recall is coming at 99%, and precision is coming at 89%. Now what's the mess here? On one hand, when I'm evaluating the retriever independently, its own metrics are very good. But when we put it in a pipeline and calculate contextual relevancy, it's just 42%. So can someone explain how a retriever, while being good, can also be bad at the same time? Can someone explain this?

If a retriever's recall is good, it means that out of all the correct contexts it should have brought, it's bringing 99% of them correctly. Second, out of however many contexts it's bringing, 89% or 90% of the contexts are valid, correct. But contextual relevancy is low.

Now can someone explain where this duality of the retriever is coming from? Some metrics are good. Then one metric is bad? Contextual relevancy being bad while recall and precision being good. Can someone explain why this is happening? I'll wait. I actually want you to answer, because now you're seeing everything. If someone answers, I'll be very happy.

It's not actually overfitting. I'll tell you the exact reason. I'll tell you the exact reason. It's very interesting. It's very simple. Again we need to go back to definitions. Okay? Let's go to definitions.

- Recall being good means: if 100 correct contexts were needed for a question to be answered, then we're able to bring 99 out of them. That's recall.
- Precision basically means: if we're fetching 100 contexts, then out of them 89 are helpful for answering the question.
- On the other hand, contextual relevancy tells you how relevant the context you pulled, that you brought, is to answering the question.

So the strange thing is that recall is coming good. Precision is also coming good. Precision actually, if you look, don't you think precision and contextual relevancy are very similar metrics? What does precision tell you? Precision tells you, out of everything you brought, how many are useful. Context. Right? And what does contextual relevancy tell you, that however much your context is, how much of it is related to the answer or relevant.

But here precision is 89, contextual relevance is 42. Now can someone tell? I've opened up the answer completely already. Yeah, that's it.

Rahul said it exactly right. **Too much noise per chunk.**

So let's say we have K = 5 set. So we got five contexts: C1, C2, C3, C4, C5. Okay? Now out of these five, four contexts have relevant chunks. Meaning, basically, information to answer the question is available in this one too, available in this one too, available in this one too, available in this one too. It's not available in this one. So in this case what will happen? Your precision will obviously be high.

But there's one more situation, and that situation is that inside each context too, there can be noise. Think about it. Now let's say in this context there are five lines, and out of five, only two lines are useful. The remaining three lines are about something else entirely. So when you break this down into claims, this will become five claims. And out of five claims, only two are useful. So contextual relevance became how much? 2/5.

Similarly here too, out of five claims, let's say only one is useful. Now since even one is useful, we're calling this chunk useful right, so at the precision level, it becomes useful. But there's noise inside the chunk.

Here exactly this is being revealed, that our chunks that are coming, even though overall inside them there are one or two sentences which will help us answer, but in the rest of the stuff there's a lot of noise. This is what contextual relevancy means. Is this point clear, why recall is good, why precision is good, but why contextual relevancy is bad? Is this point clear, guys? Is the curious case of the retriever settled now?

The problem is not that out of the correct ones, how many are we able to bring. That's what recall is looking at. The problem is also not that out of however many we brought, how many are noise. That's what precision looks at. But we weren't checking so far, how much noise is there inside a single context. That's what contextual relevancy tells us.

Now think and tell me, which parameter, if tweaked, can improve contextual relevancy? Exactly, chunking. Try reducing your chunk size and see. If chunks are smaller themselves, there's a chance of less noise, right? So that's your homework now. I've brought you to this level anyway, that if your faithfulness score, answer relevancy, recall, and precision are all coming good, then even if contextual relevancy isn't that great, it doesn't matter much. Because ultimately your answers are coming out good. Now what difference does it make that there's noise in one of your contexts? Obviously, if you reduce the noise a bit, the other values will also increase a bit. But yeah, since the other four things are working well, contextual relevancy being a bit low too, it can be accepted.

But yeah, you can always go and try it out. For that, I don't need to burn another 70-80 rupees right now. You try reducing chunk size, reducing overlapping a bit, try out different parameters, and you might see that contextual relevancy has maybe gone up a bit. But it's also possible that a trade-off happens, contextual relevancy goes up but the other four might come down. It might be possible.

## **Wrapping Up and What's Next**

But yeah, now again we've discussed and we've completed this part of our eval suite. This is also done. Now what's left is doing evaluation at the application level, where we'll check different kinds of things, like whether our answer is correct or not. We haven't checked that yet. We'll check whether our answer is complete or not. We haven't checked that yet. We'll check whether the answer's style matches Campus X's or my style or not. We haven't checked this yet. And apart from this, remaining are the safety-related evals and ops-related evals. We need to do these in the next class. And then regression testing, online eval.

So we're like on track. Okay? We did two important things. It's interesting, what we promised at the start of this course, that you'll be able to understand and perceive things better than others. Everyone builds a RAG application. I think you've leveled up a bit. You'll look at things through a different lens when you build a RAG application. I hope that understanding is developing for you. That is very important. And more importantly, I think you'll perform better in interviews because of this scarce knowledge.

It's not boring, right? This isn't boring, right? I mean, one metric clearly is how many people are attending. From that too you can understand, so there are very few people. So it might be boring, but I'm trying from my side that it's very logical, very narrative-driven. And the progression is very logical. I'm trying this from my side. The rest, you all tell me. Even on YouTube, few people are watching. I've noticed, hardly 3-5000 people are watching. So it's okay. Maybe slowly, as the season grows, people will watch. It's a bit niche right now. Not that many people are serious about evaluations right now, but they will be within one year.