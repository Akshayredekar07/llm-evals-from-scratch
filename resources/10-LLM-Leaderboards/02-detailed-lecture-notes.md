### **What Are Leaderboards?**

Before we start, can someone tell me what leaderboards are? Have you seen any LLM leaderboards? If you have, name one leaderboard that you have seen or use in your company or in your day to day work. Can anyone tell me what a leaderboard is? Benchmarks we already understood. Benchmarks are basically tests. What are leaderboards? Anyone? It's pretty simple, right?

So what are benchmarks? Benchmarks are an exam to test LLMs on some particular aspect. Now after giving the exam, a result comes out. Now you have to publish that result somewhere, right? You have to show it somewhere. That place is your leaderboard. Right? Just like leaderboards in your school that tell you who topped or whatever the ranking was.

So here is a simple definition: **an LLM leaderboard is a public ranking and comparison table that shows how different LLMs perform on a common set of evaluations.** So whatever result comes out of the benchmark, we take that and show it on the leaderboard, and the leaderboard becomes a single place where we can compare different models on a benchmark. So that we immediately get an overview of which is the best model on this benchmark. That's the basic idea of a leaderboard.

### **Why Do Leaderboards Exist**

**Reason 1: Comparing models across labs with a common reference**

One reason I already told you is that we compare models across labs with a common reference. All the models gave the same exam. Who came first, who came second, who came last - this becomes clear. From that we understand which one we need to use in our application.

**Reason 2: Leaderboards provide trust**

Generally leaderboards are third party. Meaning if OpenAI or Claude themselves say that we scored this much on this benchmark, you probably won't trust that as much. Because obviously OpenAI will want its model to get more praise. But if a third party comes and says we tested Claude on this exam, we also tested OpenAI, and these are the results - you will believe it more because it's a third party, their stakes aren't as high as OpenAI's and Claude's. Okay? So this is one purpose of leaderboards existing.

**Reason 3: They guide model selection when you don't have resources to run evals yourself**

Right? You want to build a chatbot that has math capabilities. Your students are like this, so obviously you'd want to test the evaluation yourself. But is it possible for you to test all the hundreds of models that exist in the world right now? Not possible, right? There are so many models. You need to select one model. So what's your job? You bring 100 models and run those evaluations on all 100 of them. It will take a lot of money. Right? A lot of money will be spent. A lot of time and effort will go into it. Someone else is doing this work for you, so your job becomes easy. You simply go to that leaderboard, pick the top 10 from it, and pick your own model from there. So this is the second benefit.

**Reason 4: Helps identify if a benchmark has saturated**

With its help we get to know whether a benchmark has saturated or not. If a lot of top models start clustering around the same score - there's a benchmark that tests a knowledge capability, and there the score of the top 10 LLMs is between 92 and 94. As soon as this clustering starts showing up on the LLM leaderboard, we understand that this benchmark is saturating. So that's also a purpose for which people use LLM leaderboards.

**Reason 5: Discovering new models**

And the fourth one is also very useful. I use this a lot. I've been doing this since 2022-23, that whenever I need to discover new models, I use LLM leaderboards for that. Because generally the top three-four remain the same - your Google, OpenAI, and Anthropic models. But if you scroll down a little, at position 10, 12, 15, 20, you start seeing new models. And these models aren't the best, but they can work for your purpose. Because they're generally cheaper. So LLM leaderboards also help you discover new models.

### **Who Uses LLM Leaderboards and For What Purpose**

If we talk about who uses LLM leaderboards and for what purpose, there are three-four stakeholders here.

**AI Engineers**

The first are AI engineers - people like you and me who need to build LLM based applications. And we use LLM leaderboards for shortlisting. I need to build an application that's in the math domain. So I'll go to the math leaderboard and select my candidate models from there. Generally you don't select a single model from the leaderboard. You select candidate models. Then you run your evals on top of them and from there you get your best model which you will use to build an application. So LLM leaderboards help you filter from 100 down to 5.

**Frontier Labs**

Second, frontier labs also use leaderboards a lot. Because one, it tells them where they are lying, where they exist. And second, it tells them whether they should release their next model or not. For example, say I am OpenAI. My current model is GPT 5.5, okay, and on the other side is Opus 4.8. On one particular benchmark I see that the next model I'm training isn't even able to beat Opus 4.8. So will I release that model? I won't. I'll say I'll release a new model and people will immediately say this is even worse than Opus 4.8, the previous model. So my marketing goes bad. So rather than releasing that iteration, I'll go to the next iteration and release only when I see, yes, I'm able to significantly push others behind on the leaderboard. And this actually is done. Internally they plan and strategize about when to bring which release to market. They constantly check where they're lying on the leaderboard right now.

So you must have seen this. Many times what happens is some models come on a leaderboard under a hidden name. Have you seen this ever? You must have heard of Nano Banana. Why does Nano Banana have such a funny name? Because initially when it came, it came in stealth mode on some image leaderboard and they didn't reveal that it's Google's model. Just a new model came by the name Nano Banana and completely smashed all the benchmarks. So when they saw, yes, it's significantly beating everything, then they release it in front of people. So there, Google then said, well, Nano Banana has become so famous, marketing has happened, so let's just keep the name Nano Banana. So for frontier labs it's a very good thing, leaderboards.

**Researchers**

Researchers also use this a lot because research gets a lot of clarity on what's happening right now, which benchmarks have saturated, which benchmarks are seeing good progress. So based on that, they're able to find out new techniques, new ideas come up - basically people get new research directions with the help of these leaderboards.

**Policy Makers and Safety Institutes**

Policy makers and safety institutes also have a lot of stake here. They constantly monitor which models are operating at what level right now. Is there any new model that's leaving everyone else far behind? So there they have to come into the picture, they have to stop, and they basically try to come in between and make changes. This is what happened with Fable 5 - the US government stepped in immediately because they saw this model is dangerous.

**Open Source Community**

And lastly, your open source community - leaderboards work very well for them too. Because leaderboards help with discovery. What I said, that I myself use leaderboards for discovery - there are many more people like me who go find this kind of new model on this kind of leaderboard. So some new research lab that has 101 people, and they released a new small cute model that scored very well on a single benchmark and went into the top three-four. So that lab got publicity. That model became famous, right? This is how those Chinese labs came into the picture - just like this, that suddenly a new model came overnight and started competing with the top model on some benchmark, so it got discovered, got publicity, got marketing. So in that sense too, LLM leaderboards are great.

So I hope by now you've understood what leaderboards are, why they exist, and who uses them for what.

### **Types of LLM Leaderboards**

Now let's quickly discuss what are the different types of leaderboards that exist. Precisely there are four types of leaderboards that you'll come across.

**Type 1: Benchmark Specific Leaderboards**

The first and simplest leaderboard is benchmark specific leaderboards. Here your leaderboard creates ranking based on just a single benchmark. It says here: these rank models using the result of one particular benchmark. Either it's MMLU or HumanEval for coding or GSM8K for math or GPQA - some single benchmark on which all models are run and that ranking is shown to you in the form of a leaderboard. So the main idea is to tell which model performs best on this benchmark.

The only problem with this kind of leaderboard is that it gives you a very narrow view. You only get to know how a model performs on one particular benchmark. You don't get an idea about how good the model is overall. There's a very good example of this. I already showed you - like the HLE website, Humanity's Last Exam. So this is its leaderboard. You can see that Gemini 3 Pro is at 38% and it shows calibration error and other things. So this is a leaderboard that caters to a single benchmark. Most of the famous benchmarks have their own leaderboards. These research teams build and maintain this entire leaderboard on their own. This type of leaderboard isn't very useful, honestly.

**Type 2: Multi-Benchmark Leaderboards**

What's genuinely useful is this second category, where you read about multi-benchmark leaderboards. Makes sense from the name, right? These are leaderboards that bring together results of multiple benchmarks at once and create a leaderboard with a cumulative score. It says here: these leaderboards compare models across multiple benchmarks and evaluation dimensions instead of relying on just one test. So there could be a leaderboard that combines knowledge, reasoning, mathematics, coding, instruction following, data analysis - all these benchmarks together to build one leaderboard.

I'll show you a very good example of this - LiveBench. See here it says: a challenging contamination free LLM benchmark with 23 objective tasks across seven categories - reasoning, coding, agentic coding - the score in each category is given for every model, and then an overall score is also given to you. So this is like a more useful leaderboard because it gives you an overall view of how a model is doing across multiple capabilities in general. I hope you're understanding.

And not only this, these leaderboards also give you information on other aspects - like what's the cost per token, what's the latency, what's the output speed, what's the context window size - all this information is also given. Let me show you an example of this too - there's a company called Artificial Analysis. Their job is exactly this - building leaderboards and providing this kind of information. So they give you leaderboards built on every kind of thing. See here, they have a separate leaderboard for intelligence, a separate leaderboard for speed, separate leaderboards for cost per task - a very exhaustive list. Look, they've made a separate one for HLE. There's GPQA Diamond, made separately. So these are companies that basically give you every kind of leaderboard. So they're like a proper product - coding agents have their own separate leaderboard, speech, image, audio, hardware. So a lot of leaderboards exist. Then they've also made an overall one accumulating everything together.

So this is the most useful category, which personally I also use the most and people generally use the most. This type of leaderboard answers the question: which model provides the strongest overall combination of capability, cost, and performance. This is the leaderboard you'll use the most. Okay?

**Type 3: Human Preference Based Leaderboards**

Third, another interesting category is human preference based leaderboards. In this, you don't rank based on any benchmark. What do you do instead? You get comparisons done. So your user comes to your website. You tell them to ask a question. The same question is asked to two models, A and B. Both give an answer. Now the user is asked whether they liked A's answer better or B's. So basically the user itself is scoring, based on helpfulness, clarity, writing quality, creativity - whatever the ways of giving answers are - on that basis. And then once a lot of this kind of votes get collected, a ranking is built based on that and that ranking is shown in this leaderboard.

It says here: these rank models using human votes. They took response from two models. Told the user, select which one you liked, and after a lot of votes, this leaderboard shows us which model is on top. So a very famous example of this is LM Arena. See, in battle mode you can ask anything - "what are LLM leaderboards." So now there are two models behind the scenes. I don't know which models they are and they'll each give their own answer, you can see. And once they give the answer, I'll read both and I'll be asked which of these I liked better. See, it's asking - A is better, both are good, both are bad, B is better. Now I haven't read it. Let's say I said B is better. Now it'll reveal which one is which. See this was Claude Opus 4.8 Search and this was Fable. So this way, collecting votes from people around the world all day, they build this leaderboard. Then this is the leaderboard. So this is the current ranking. Fable 5, 5.6 Sol, 4.8 Thinking - and you can do this in different categories too. So you can do it in normal chat. Code has a separate one, image has a separate one, video has a separate one.

So this is also a type of leaderboard that exists now and is very famous. The limitation with this approach is that it's not necessary that if a user finds one answer better, that answer is actually better too. Many times we humans get impressed that it's formatted very nicely, or an answer is given that I personally like. So there's a bit of human bias here. But again, it's happening at scale. People from all around the world are doing it. So you can still trust it. And that's why you can see that the top models are the ones that are also leading these leaderboards.

**Type 4: Application Specific Leaderboards**

And the last type of leaderboards are application specific leaderboards. These are leaderboards built around one particular domain or task. Like there could be a dedicated leaderboard for coding. So all the benchmarks that exist in coding, they combined those and made a single score, and that is shown here. Or you're building a separate leaderboard for agentic tasks. Or you're building a separate leaderboard for generating SQL queries, or a separate leaderboard for medical questions.

So an example of this type, if I show you, is the Berkeley Function Calling Leaderboard. So this is a leaderboard that specifically tells you how good your model's tool calling capacity is. So based on that it ranks models. So this is operating in a single domain. Even though it's using multiple benchmarks, but within a single domain. So there are a lot of this type too. Coding has its own separate benchmarks too. So different types of these benchmarks exist too.

So these are the four types you'll see. The least useful is the single benchmark leaderboard. The most useful is the multiple benchmark, general capability measuring leaderboard that tells you a lot more things too - cost, latency, everything. Human based is also popular, mostly for marketing - like who's on top on LM Arena - but yes, this category also exists. And the last one is application specific categories of leaderboards too. You use those too if, say, you're building an application specific to a particular domain.

These are the four types of leaderboards that you'll find on the internet. Okay?

### **Why You Cannot Blindly Trust Leaderboards**

Alright, let's read a bit more, then we'll do Q&A together. Okay? The next thing - although leaderboards are a very powerful thing and give you a summarized overview of the entire LLM landscape all at once, but you cannot blindly trust leaderboards. This is a very important point. Because in the future you'll be working as AI engineers. And most of the time when you go to build an application, step one is model selection. And in model selection too, step one is going to leaderboards to see which model is on top. So we develop this bias that if it's on the leaderboard, then it must be right. But that's not the case. You cannot blindly trust leaderboards. What are the reasons - we're discussing that.

**Reason 1: Benchmark performance may not transfer to real applications**

This is a very important point. Generally if a model is hitting 80, 90 on a leaderboard, it does not mean that in your real application too it will give you equally good results. There's a famous saying - if you can solve problems on Kaggle, it doesn't mean you'll become a good data scientist in real life. Why was this said? Because on Kaggle the data given to you is very clean data. The problem statement is very clear. So generally you get easy work. In the real world, everything is messy. So the same thing applies here. In benchmarks, the data is generally clean. Models will perform well on that, they will. In the real world there are a lot of things - ambiguous requests, missing information, company specific data, tool failures, unusual edge cases - whether the model handles all of these or not, don't know. So this is the first reason.

**Reason 2: Benchmark contamination**

Second, as we discussed, benchmarks get contaminated very easily, and if benchmarks get contaminated, then their leaderboard score also gets contaminated and inflated. Shows higher than it should. So don't blindly trust that. It could be that the score showing on the leaderboard is genuine. But it could also be that the model has memorized it, or it already knew this kind of questions. So you cannot blindly trust it.

**Reason 3: Models can be over-optimized for the leaderboard**

After that, this is a very genuine problem, and this is something people have started discussing in the last one-two years - that models can be over-optimized for the leaderboard. Sometimes what happens is a particular leaderboard becomes very popular. Like LM Arena - it became very popular that who's topping on LM Arena. So now what happens is companies also see that the most talk happens about who's topping on LM Arena. So we need to top it. Now who will top on LM Arena? Whoever wins over humans. To win over humans, what do you need to do? Do a bit of formatting this way. Give a bit softer answers this way. Give a bit of flattering answers - then there's a higher chance that our model gets selected, gets voted. So now what will they do? They'll feed this kind of data to their model during training or fine-tuning stages. So that rather than performing well on actual capability, it performs well only in LM Arena type situations. So what will happen is your model will start scoring well on the leaderboard, but its real world capabilities won't improve.

So there's a law here, a very famous law - Goodhart's Law. It says: when a measure becomes a target, it ceases to be a good measure. So if you start targeting a metric, that you'll improve this metric - imagine a car, and you know that in India people buy cars purely based on mileage. So now your entire engineering team is focused only on this - how do we improve mileage, how do we improve mileage. So the entire engineering will be around mileage. But the overall car will become bad. Because you're not focusing at all on things like driving dynamics, 0 to 100 time. You're focused only on mileage. So the same thing is written here - if you make one metric your target, then that metric stops being a good metric. So this is happening these days, that companies are building models so that they can top the leaderboards, but the actual performance then isn't good.

**Reason 4: Lack of transparency in composite leaderboards**

After that, this is also an important point, especially for leaderboards that combine multiple benchmarks and show you results. Now the problem there is - which benchmarks is that leaderboard including? Which benchmarks is it excluding? That's up to the leaderboard. After that, how are the scores normalized? If, say, we're calculating one overall score from different capabilities, then how much weightage are we giving to each capability - this also isn't told to us. So these kinds of things stay hidden and sometimes they can trouble you. So whenever you're looking at a leaderboard, the more transparency it has, the better it is. The more you can find out about that leaderboard, the better it is.

**Reason 5: Small differences on the leaderboard don't matter much**

After that, small differences on the leaderboard don't matter that much. Like two models - one has a score of 84.3, one has 84.1, and this model came third position and this one went to fifth position. But the difference was only two, right? From this it doesn't really make sense. We start feeling like, well, let's grab the third one, we won't choose the fifth one for our application. But there's a good chance that both of these are very similar. And the fifth one might actually be better for your application. So sometimes we start focusing too much on which rank a model is at that we're choosing. It's at this rank on this leaderboard. So there's a rank bias that happens. That's not a good thing. If the difference is small, the models are at the same level - that's the point. Like in IIT JEE, there won't be much difference between rank one and rank 25. One or two questions could go wrong for anyone, right? So the same logic applies here.

**Reason 6: Human preference leaderboards have human biases**

Sixth, human preference leaderboards have human biases. We've already discussed this. Now on LM Arena, the top model there - it does not necessarily mean it's objectively the top model. Humans find longer answers, more confident answers, better formatted answers, more entertaining answers more likeable. But it could be that the actually better model doesn't have this. So then it'll fail in the human based leaderboard ranking. So that is also a problem.

**Reason 7: Leaderboard scores can be stale, incomplete, and self-reported**

And lastly, leaderboard scores are stale, incomplete, and self-reported. Now take the same example we just discussed - what did we discuss just now? Humanity's Last Exam. Now here, Gemini 3 Pro is there, this has 38.3. Now the most recent models aren't here. Where do you see Fable or 5.6 Sol here? It's not there. Because these people haven't updated it yet. These people just haven't updated it. So many times what happens is that benchmark leaderboards aren't updated. You'll get results of old model versions, or the new one's won't be there, or many times you'll get results of discontinued models. That's not a good thing. Many times in some leaderboards, the results that are there - the company puts its own model's result itself. That's also not a good thing. The company itself is putting its own results. So why trust it?

So these are six-seven reasons why you don't blindly trust leaderboards. But you use them a bit carefully. It's a useful thing but you can't be blind about it. Okay?

### **How to Read LLM Leaderboards - A Guideline**

So now comes the last thing we have to discuss - if you are an AI engineer and you're building an LLM based application, and your first job is to select a model for it, then how should you read LLM leaderboards? So here's a guideline that I'll quickly tell you.

**Step 1: Clarify your requirements first**

Before going to any leaderboard, first clear these four-five things in your mind. What type of application are you building? How much latency do you need in that application? How much cost can you bear? What are your context needs? Are there any deployment constraints or not? Can I use generally publicly available models, or do I need an on-premise model? Write down all these things clearly. If this becomes clear, then you won't be biased towards the rank one model. You'll automatically start thinking objectively that, well, if I need to set up on-premise only, then obviously I can't use Claude, Fable. Then I'll have to go a bit towards the open source side. So this opens up your thinking a bit. If this is step one.

**Step 2: Go to the leaderboard relevant to your work**

In step two, now you won't blindly go to any leaderboard. You'll go to the leaderboard that's related to your work. Building an agent - then you'll go to an agent related leaderboard. Building a chatbot - then maybe you'll go to LM Arena type leaderboards. Because there you get a direct objective measurement of chatting. Building RAG - then you'll go to MTEB. This is actually a leaderboard for ranking embedding models. In RAG you need to fit an embedding model. If there are budget constraints in your application, then you'll probably go to Artificial Analysis type or this Vellum type leaderboard. Because there you get exact information about which models are how fast and how much money they cost. So this is step two - you go to the right leaderboard.

**Step 3: Read the leaderboard correctly**

After that, read the leaderboard correctly. Meaning understand everything. What thing is being scored? In what way is it being scored? Who evaluated it? What was the inference budget? Is reasoning happening or not? How old is the evaluation dataset? How old is it? Is it being updated? Is a private test set being maintained or not? Have the benchmarks saturated or not? We discussed confidence interval - if it's a small dataset then what's the confidence interval, is that even told or not? If it's not told, then two very close models are effectively the same. If it's a composite leaderboard combining multiple benchmarks into one score, then what weightage has been given to different capabilities? You'll analyze all of this. There are just a lot of pointers written here. But you get the idea. Don't blindly trust a single number. You need to read the fine print below it. Like the key definitions here - you'll go and read all these things. You'll read the frequently asked questions - then you'll be in a better position to judge that leaderboard. Okay?

**Step 4: Shortlist top 3-5 models based on your criteria**

And then based on your criteria, you'll shortlist the top three to five models. Okay?

**Step 5: Run your own custom evaluation**

And once you have your five models, then comes your fifth and most important step - that you'll run your own evaluation on top of them, on those five models. And when those five models run on your own evaluation set and give results, then you'll get your top candidate.

### **Key Takeaway**

So here's one line you need to remember. This is the most important line you need to take from this session: **leaderboards are not a selection tool. Leaderboards are a filtering tool, not a decision tool.** Meaning you don't go to a leaderboard and decide that I'll use this model to build this application. No, that's a wrong strategy. You shortlist four-five top models with the help of leaderboards, and then by running your own custom evals on all of them, you pick one model for your application. I hope you're understanding, and that's exactly what we're going to do in the next session.

### **What's Next**

What I said, that going forward the classes will be practical. So the next session is all about how do you run your custom evaluation on a given LLM. We'll learn that in the next class. So whatever flow I've told you, you'll practically do this in the next class. We've done benchmarks - meaning it's not complete. But at least conceptually, we've seen what it is, and we've done leaderboards too. Now we'll do custom evals. Once custom evals are done, after that we'll move towards application evals, where we'll learn both RAG evals and agent evals.