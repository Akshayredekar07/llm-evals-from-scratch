# LLM Eval Methods

The next thing we are going to study is a very important topic. Let's start.

So far we have learned that we need to build multiple LLM evals. Now we are going to study a very important thing called **Methods of LLM Eval**, or LLM Eval Methods. Basically, whatever eval pipeline you build, it will work based on some method. That's what we are going to study now.

## Definition

**An LLM eval method is the mechanism you use to decide whether an LLM's output is good or not.** It is the actual procedure that takes an output and produces a judgment about it.

Why do we build an evaluation pipeline? We build it so that we can figure out whether some component, workflow, or application is working correctly or not. But who actually carries out the evaluation pipeline? Our **method**.

Primarily speaking, whenever you build any evaluation pipeline, it will have one of three methods:

1. **Programmatic or Deterministic method**
2. **Human method** — basically a human is carrying out the eval
3. **Model graded or LLM graded method**

To put it simply, without confusing things: your evaluation pipeline is built, but *who* executes it? That's the whole point we're discussing. Is it a program executing it? Is it a human executing it? Or is it an LLM executing it? These are the only three options. Nothing else.

If you remember, in the last class I showed you an LLM eval pipeline and gave a use case. If you recall, we were AI engineers at Zomato, and our task was: whenever an email comes in, we send it to an LLM, and that LLM categorizes it as related to billing issue, technical issue, or general issue. We had built this application. Does anyone remember which eval method we used out of these three in that case?

We had discussed this in the last session. We first understood that in this whole scenario we need to capture accuracy — how accurately we are able to classify. So who was calculating this accuracy? We had done this through Python code. So basically you can say it was **programmatic**.

So that's what I mean — whatever evaluation pipeline you build, one of these three things will carry it out, execute it. Either a program will carry it out, or a human will carry it out, or a model as an LLM will carry it out.

Today I will give you one example of each of these three types of pipelines. I know I already gave a programmatic example in the past, but today I'll give a more relevant example of it.

---

## Example 1: Programmatic (Deterministic) Evaluation — Evaluating a Retriever

We are discussing an eval pipeline whose eval method is **programmatic**, or also called **deterministic programmatic**.

**The setup:** We planned to build a RAG chatbot for Campus X, so that any user coming to the site can interact with our chatbot and get help, without us needing to manually reply through email.

I thought — I want to build this chatbot really well, so I'll create every kind of eval pipeline for it. First, I thought let's build an eval pipeline at the **component level**. So I picked up the **retriever** first and decided to design an eval pipeline for it.

What does a retriever do? As soon as a question comes to the retriever, the retriever pulls the most relevant documents from the vector database. That's its whole job. Now I need to check whether this retriever is actually working correctly. I need to build a pipeline for this, and we will build that pipeline exactly through this flow:

### Step 1: Define the Task and Target

- **Task:** Our retriever should work correctly.
- **Target:** A single component — the retriever.

### Step 2: Define a Success Criteria

Next, we have to define a success criteria — how will we know our retriever is working correctly?

Can anyone tell how we can quantify whether a retriever is working correctly? The answer is this metric: **Recall@K**.

**Definition of Recall@K:** Out of all the correct items that exist, how many did the system retrieve in its top K results?

**Example:**
Question: *"What are the prerequisites for the ML course and how long is it?"*

We had already chunked all of Campus X's documents and put them into a vector store. For this question, we already know beforehand that the correct answer is hidden in two documents: Document 1001 and Document 1003. So in a way, for this question, the two correct documents are 1001 and 1003.

Now, when I sent this question to my retriever and told it to fetch **k = 5** documents, it fetched: **1001, 102, 104, 105, 106**.

Now tell me — what is the recall in this particular scenario?

Using the definition: Out of all correct relevant items that exist — how many are there? Two. How many did the system retrieve in its top K results? Only one (1001).

So the answer is **1/2**. Basically my recall is **50%**. Ideally it should be 100%. It can't be more than 100%, and can't be less than 0%.

That's what Recall@K means. So if you want to judge whether any retriever is working correctly, one very good way is to calculate its Recall@K, which I just showed you how to compute. Besides this, there are other things too — precision is also a thing, rank is also something you calculate. But for now, to keep this discussion simple, our success criteria is: **Recall@K**.

### Step 3: Build a Dataset

Next, we had to build a dataset. This is what we did — this is the dataset you see on screen. In this dataset, we picked out about 50–100 questions that users might ask in the future, once this chatbot goes live on the website. We tried to cover all cases — edge cases, difficult questions, easy questions, random questions — all kinds of questions were sampled to build a dataset.

Then we sat down a human expert. We told them: pick up this question, look at it, then go into our vector database and search which document(s) actually contain the correct answer to this question. So in a way, we are building our **golden dataset** here. We did this for 50 to 100 questions. This dataset was ready.

### Step 4: Define an Evaluation Method

Then we defined the evaluation method. It's very simple — here we will programmatically determine what our recall is.

How? We took all 50 questions and sent them to our retriever — just the retriever, not the entire RAG chatbot, only the retriever. The retriever's K is 5, by the way.

- For Q1, the retriever fetched 5 documents.
- For Q2, it fetched 5 documents.
- Same for Q3, Q4, Q5 — we retrieved documents for every question.

Now I have both the original correct answer and what the retriever brought back. So now I calculate recall per question (per row).

- For the first question: all the information was in one document (1001), and the retriever found 1001. So recall = 1 (100%).
- For the second question: the correct documents were 1001 and 1003. The retriever brought back 1001 but not 1003. So recall = 1/2.

We do this for every question, and at the end we **average** this entire quantity. Averaging gives us our overall **Recall@K** across the whole dataset.

This quantity tells us how successful our retriever is at fetching relevant documents.

### Result and Improvement

We wrote a program to do this whole thing, ran it, evaluated it, and got a **67% recall**. Now what do we do? We deeply study the cases/questions where our recall is very poor. After analyzing those questions, we try to improve our model — in this case, the retriever.

What can you improve in a retriever? Many things:

- Improve your **embedding model** — maybe it's not capturing semantic meaning properly.
- Do **query expansion** — instead of directly sending the user's question, first expand it through an LLM, then send the expanded question to the retriever.
- Increase the value of **k** — currently k = 5, try k = 10.
- Try **re-ranking** — maybe the correct document was in your top 10 but not top 5. After adding a re-ranker, something that was at position 8 might come to position 3, automatically giving better results.

This is how you do a component-level programmatic eval. This was an example of how a programmatic eval is run, and in this process you also learned something new (or maybe you'd studied it before): how to evaluate a retriever using Recall@K.

**Question to think about:** Did we need any human here to evaluate the retriever? Did you feel a human should have been brought in, or did the program do the job on its own? I guess you can see that if a program can do it, why bring a human into the picture — humans are costly, you'd have to pay salaries.

**On relevance — there can be multiple aspects:**
1. Out of all the correct documents, how many were you able to fetch from the vector database. (This is the aspect we covered.)
2. How many of the documents you fetched were not useful.
3. Whether the documents that came back were properly ranked or not.

So we are covering one aspect: how many of the actual relevant documents we fetched. Who told us this? The person who created the golden dataset — they told us, "look, only one document (1001) is related to this question in our vector database," or "only two documents (1001, 1003) are related to this question." If you bring back both, you brought the most relevant information. Bring back half, you brought half the relevant documents. Bring back neither, you brought zero relevant documents. This is how we're defining relevance here.

Whether any eval is programmatic, human-based, or model-generated depends on **who executes it when we run it**. Creating the golden dataset is a separate activity. Executing the LLM eval, running it, extracting scores — that's the activity this whole discussion is based on. Obviously the golden dataset is created by a human.

---

## Example 2: Human Evaluation — Chatbot Helpfulness

This is the second example. In this case, you'll notice that the entire execution of the evaluation pipeline is carried out by a **human**.

**The setup:** Again, we have a chatbot on the Campus X website, and this time it's a **general-purpose chatbot** that you can ask any kind of question. "When is the next course launching?" "What is the fee for some course?" "Will I get a certificate?" "What is the course validity?" — this kind of thing. It's a general chatbot that obviously answers based on our documents.

Now we need to evaluate whether this chatbot is working correctly. We are not evaluating safety and operations here — we are evaluating the **application quality** part. We are evaluating the **helpfulness** of the answer — when a user asks a question, was the response they got helpful or not? This is what we're evaluating.

### Step 1: Task and Target

- **Target:** The entire application — not one component, not one workflow, the entire application.
- **Task:** Evaluate its helpfulness.

**Helpfulness** means: the answer that came out was accurate, its tone was correct, and the answer was complete in itself. This is what defines helpfulness.

### Step 2: Success Criteria

Here, defining a success criteria is very tricky, because you're evaluating an entire application on whether it is helpful or not. How would you define a metric for this? The answer is **there is no single correct metric** — this will vary business to business.

So what did we do? We defined a kind of **rubric** for Campus X — a helpfulness criteria on a scale of **1 to 5**:

- **5** — the answer is correct, accurate, complete, and in exactly the right tone.
- **3** — partially helpful.
- **1** — not helpful at all; the chatbot started talking about something else entirely.

This became our kind of success criteria.

### Step 3: Build a Dataset

We built a dataset — again, took around 50–100 questions, and again thought about coverage: normal questions, difficult questions, edge cases, random questions that a user might ask. We tried to put a representation of all of it into this dataset.

One thing to note about this dataset: it has **only one column** — the question being asked to the chatbot. Examples: "How long is the ML course?" "Is the ML course right for me if I already know Python?" "What's the fee for the DL course?" "Do I get a refund if I drop out midway?" "Can I pay the fee in installments?" We pulled out about 50 samples of whatever kinds of questions might be asked and put them in this dataset.

### Step 4: Define an Evaluation Method

Now — can you tell me, can this "helpfulness" figuring-out be measured programmatically? Can you write a program/code that automatically tells you this chatbot is helpful — 70% helpful, 90% helpful? Or do you feel this is too nuanced and requires **human judgment**?

I guess you understand — here we'll need a human. So here, your evaluation method becomes **human**. Basically you need a human.

**How it works:**
- You run the model — trigger your eval pipeline. You take each question one by one and send it to your chatbot.
- The chatbot generates an answer.
- You sit down a human and give them instructions: "Look at this question, look at this answer, and give a grade."
- Next question, sent to the chatbot, got an answer, told the human: look at this question, look at this answer, assign a number based on the rubric we've defined.
- You do this for the entire dataset.

### Why Multiple Human Graders

Generally you use more than one human — for instance, Grader A and Grader B. Why might it help to seat more than one human?

One human doing the work makes sense — you trust their judgment. What's the benefit of having two or more humans?

A straightforward benefit: if the two graders' grading doesn't match on a lot of questions, what can you conclude? There is **some ambiguity in your rubric**. There might be a problem in the criteria you defined. So sometimes multiple graders are seated **just to refine the rubric**. If they start agreeing a lot, it means the instruction is pretty clear. If they disagree, it means the instruction above is ambiguous, and that's why both are confused and giving these kinds of numbers.

For now, though, you can assume there is only one human doing all the evaluations for you. Finally, you average this and get your **helpfulness score** — and it came about because of your human.

This was a very simple scenario where a human comes into the picture and carries out your evaluation pipeline end to end.

### Humans Don't Just Evaluate One Way — Five Types of Human Evaluation

I want to clarify one more thing: in LLM evals, humans don't only do evaluation in one way — they do it in multiple ways. What I just showed you (looking at the chatbot's answer and giving it a score) is the simplest type of human evaluation. Besides this, there are a few more types:

**1. Direct Grading and Rating** — what we just covered above; the chatbot's answer is looked at and given a score.

**2. Red Teaming** — a situation where a group of individuals (humans) deliberately attack an LLM-based system and try to figure out where the system breaks. Whenever big LLMs launch, before that, there are red teaming teams whose job is to try to break the system. Wherever it breaks, that data is sent back to the development team and fixed. Red teaming is also a kind of evaluation done by humans, but a different kind from what we just studied.

**3. A/B Testing** — suppose you have two versions of a chatbot. You put both into production and A/B test them, and you've told your humans-as-users to rate their experience so far. Whichever version gets a better rating, you select that version and deploy it across the whole region. So here, your users are evaluating your application in production. This is also a type of evaluation humans perform, but different from what we studied.

**4. Golden Dataset Creation** — when humans come into the picture to create the golden dataset and rubrics. Someone asked earlier that even in the programmatic case, we needed humans to create the golden dataset. So that is also a kind of evaluation. If I go and say "for this particular question, the answer is hidden in this particular document" — I'm performing a kind of evaluation.

**5. Human in the Loop** — sometimes there are cases so complex that you don't trust purely programmatic or LLM-based evaluations. In some complicated cases, you pass the judgment to a human. So basically, human is also in the picture whenever the LLM can't handle it, or programmatic checks can't handle it, or there's a threshold — a grey area forms — and there you pass on the responsibility to a human, and the human gives you the answer based on their own judgment.

**In a nutshell, humans perform five types of evaluations in the LLM world:**
1. Direct grading and rating
2. Red teaming
3. A/B testing
4. Golden dataset creation
5. Human in the loop

So we've now learned two evaluation methods — programmatic and human.

### Advantage and Disadvantage of Human-Based Evaluation

**Advantage:** When you use a human to evaluate an LLM-based application, the biggest advantage is that their **judgment is reliable**. If you're hiring a decent, careful person and putting them on the job, you'll trust their judgment. A human brain can easily figure this stuff out compared to a machine. So it's much more reliable compared to some program or LLM — reliability is very high, trust in the system stays high.

**Disadvantage:** **Cost.** You have to pay people to hire them. That's the biggest downside. And that's why if your application is working at scale — lakhs (hundreds of thousands) or crores (tens of millions) of users using it — you most likely cannot use humans for evaluation there. It would be too costly.

---

## The Third Category: LLM as a Judge

So what if there's a scenario where we can't use the programmatic method, because what we want to evaluate is very ambiguous — such as we want to evaluate how helpful a chatbot is. There we can't apply programmatic checks. But at the same time, we can't seat humans there either, because humans are costly.

So what's the alternative? What lies between programmatic and human — something that has the strengths of programs *and* the strengths of humans?

The answer is **LLMs** — our third category. When you use LLMs for evaluation. This is the third category, and it's the most useful category — if you use it correctly. That's why you'll notice that most LLM evaluation pipelines that are built are mostly based on LLMs. The eval method there is **model graded**, or you could say **LLM graded**. And the technique used here — a very popular technique that you'll study a lot in this course — is called **LLM as a Judge**. You use an LLM like a judge to evaluate something.

Now I'll show you a very interesting example / use case of this.

---

## Example 3: LLM as a Judge — UPSC Mains Answer Evaluation Platform

Let me set up the scenario first. Suppose I am a website and YouTube channel that provides UPSC preparation. UPSC is India's toughest exam, they say — by clearing this exam you become an IAS officer.

**UPSC exam pattern** (for those who don't know): there are three stages — **Prelims, Mains, and Interview**. Whoever passes Prelims has to give the Mains exam, and then comes the Interview, and after that comes your selection. Prelims is MCQ-based. Mains is subjective — you have to write subjective answers.

**Setup:** Our website is called Campus X UPSC, and we prepare students for both Prelims and Mains.

Over time we realized we could conduct an **automated test**. For Prelims, conducting an automated test is very easy, because it's an MCQ-based exam — anyone can do that easily. For Mains, conducting an automated test is difficult, because the answers are subjective — meaning you need subject matter experts to evaluate the answers.

Our problem: lakhs of children come to our YouTube channel, and lakhs of children could give this exam. So it's a huge earning opportunity for me — I could make a lot of money. The only problem is, if say 10,000 children sit for our mock test, we would need to evaluate the subjective papers of these 10,000 children. Think about how many subject matter experts we'd need, and we'd have to pay these experts per paper evaluated. So my profitability drops.

But suddenly a company came to me and said: "We've built a platform. You can send any number of children to it. We have an LLM-based system that, based on your defined rubrics, can evaluate even lakhs of children's answers, and you only have to pay a fraction of the cost."

Does it make business sense for me to use this platform? Very simple, logical — yes. So this platform is what we need to build. Suppose we've already built this platform — now we need to **evaluate** it. That's our task.

We are this platform that conducts UPSC mock Mains exams and evaluates them. We need to evaluate whether this system is working correctly or not. At scale, humans can't come into the picture. It has to be done through LLMs.

### Step 1: Task and Target

**Target:** We've built this application; we need to evaluate whether it is checking papers correctly — evaluating like a human expert would or not.

### Step 2: Success Criteria

What could the success criteria be here? In the chatbot case it was helpfulness, in the retriever case it was Recall@K. Here, for this particular platform, what is the success criteria? What does success look like? When would we consider this system successful?

Take some time and think — this question has multiple possible perspectives, and there could be multiple answers here.

**The success criteria we'll use:** If our platform can evaluate the UPSC answers exactly the way human experts do, then I would say my platform is successful. If our platform grades papers just like a human expert does, then I'll accept that my platform is successful — I can deploy it, launch it, earn money from it.

This is what we'll take as our success criteria in this particular scenario. There could be other success criteria too, but this is also a good one.

So the success criteria is: does our platform evaluate papers like a human, or not?

The exact metric — I'm not telling you yet, just the success criteria for now. I'll tell you the metric a bit later.

### Step 3: Build a Dataset

Now, based on our success criteria, we have to build a dataset. This is where things get interesting.

First, we'll define a **rubric**. Suppose for now our UPSC paper has three questions (it could be any number, but let's assume three for now):

1. *"Ethical governance is impossible without administrative accountability. Discuss."* — 15 marks
2. *"Examine the role of the Governor in Centre-State relations."* — 10 marks
3. *"Federalism in India is more cooperative than competitive. Critically analyze."* — 15 marks

I brought in an expert who is very good at evaluating papers, and told them: just tell me which dimensions I should check to answer this question — what should be written in the answer for me to consider it a good answer? The expert defined about four or five things. For example, for the first question:

- If the answer discusses ethical governance and accountability — the answer is good.
- If it explains the link between the two.
- If it gives mechanisms.
- If it cites examples.
- If it has a balanced conclusion.

Basically, I'm defining a rubric for each of my questions. So we defined five checkpoints per question — if these five dimensions are met in the answer, I'll consider it a good answer. This is our rubric.

**This rubric is NOT the dataset.** This is just a rubric that can evaluate a question's answer.

**What the dataset looks like:** It will have:
- **Answer ID**
- Which question this is an answer to
- What is written in the answer (the exact answer written by the student — not a summary)
- Who evaluated this answer — by a human evaluator (by the way, we are creating our **golden dataset** here, created by a human evaluator)

We only had about 50–100 rows here — we didn't need to evaluate too many papers. We just took one subject matter expert, and they evaluated these 50–100 answers (not entire papers — 50 to 100 answers), so it wasn't too big a job.

The expert would look at which question this is the answer to, read the answer, and based on the rubric, check off which points were covered. For example, for Question 1's answer: all five points covered → gave 13 out of 15. For the next child's answer to the same Question 1: point 1 partially covered, point 2 not there, point 3 not there, point 4 not there, point 5 there → gave 4 marks.

This is basically how we're creating a golden dataset — we defined a rubric, then conducted the exams, took some children's answers, and had a human expert perform evaluation on that rubric basis. This is how a human would evaluate a UPSC Mains paper. So this became our golden dataset.

### Step 4: Define an Evaluation Method

Now, can we evaluate these papers programmatically? Is there a way we can evaluate the answer that the user wrote, put it into some Python code, and compare it to the human evaluation and figure it out? Not really. And we don't want to use humans either, because obviously it's costly.

So there's only one way: **we will use an LLM**.

So the evaluation method is set — it's an **LLM**.

### Running the Evaluation

Now we run this model, run this evaluation. Basically, we bring an LLM into the picture and give it some instructions:

> "You are a grader. You are grading a UPSC Mains answer against an evaluation rubric."

Then we tell it the question (extracted from the question paper), how many marks the question is worth, and the exact rubric for that question. We're pulling this data from our golden dataset — the question, the marks, and the exact rubric.

Then we give it the aspirant's answer — the answer the user wrote.

Then we instruct it further:

> "For each dimension, decide whether the answer genuinely addresses it, then allocate marks. Do not reward verbosity, keyword stuffing, and confident assertions that lack substantiation. Reward structure, relevant examples, and balanced argumentation."

We defined a prompt like this, and asked it to tell us which dimensions it addressed and the total marks it's giving, along with a one-sentence justification for why it gave those marks.

Now every answer the user wrote goes to this LLM, and our LLM gives us back: for a particular answer to a particular question, how many marks did the LLM give. We do this for all answers.

And at the same time, we're comparing this against: for that same question, how many marks did the human give the same user? Now I have side-by-side information — for the same answer, how many marks did the human give (evaluating), and how many marks did the LLM give (evaluating) — both based on the same rubric. Both the human and the LLM looked at the same rubric, and both are marking.

**What is our goal at this point?** Looking at these two columns — what should our goal be? What is the success criteria? The success criteria is hidden right in these two columns. If these two columns are very similar to each other, what does that mean? It means the way the human is evaluating papers, our LLM is also able to evaluate them the same way. It means our system is working correctly — at least on these 50 questions/answers.

### The Metric: MAE (Mean Absolute Error)

Can you give me one metric? This was the success criteria — but give me a metric. For these two columns to be similar, can you define a metric?

The answer: **MAE — Mean Absolute Error**.

What we do: subtract them. 13 − 12, + 4 − 8, + 8 − 8, and so on for all 50 answers, then divide by 50.

Say we got **2.3**. What does 2.3 mean here? It means on average, my LLM deviates from the human by plus or minus 2.3 while evaluating answers.

**What's the overall goal?** Bring this number down toward zero. Because if this number becomes zero, it means your LLM is evaluating answers exactly the way a human would. That is your success criteria.

So your entire goal is to bring this number down. You can do several things for this:

- Bring in a better LLM.
- Change the system prompt.
- Change the rubric.

You'll keep making changes like this in a loop. But now you have an evaluation mechanism through which you can define how to build a system that will evaluate UPSC answers exactly the way a human does.

We just saw how LLM as a Judge works, with a relatable kind of example. Was it interesting? A lot of effort went into building this example, trust me — the earlier examples that came to mind were very boring. Finally, after a lot of exploring, I arrived at this conclusion that this might be interesting.

Up until now, you all were happy just building LLM-based applications. Do you feel a bit of a mindset shift? Now you're thinking like a **production engineer**, who first figures out whether the application will actually work correctly, and only then deploys it. Can you sense this change compared to before? It's not only about building an LLM-based application — that's the easy part. The difficult part is making sure it works every time, everywhere. That's the challenging part.

---

## Reference-Based vs Reference-Free Evaluation

One last thing to cover today's class, and that's a term that sometimes gets asked, so we're discussing it. You already know about it in a way — two terms get asked, or discussed, or you might come across them online: **Reference-Based Evaluation** and **Reference-Free Evaluation**. You've already seen examples of both. Let's define both.

### Reference-Based Evaluation

**Reference-based evaluation** is an evaluation where you have a reference/known correct answer, and the key thing is: a correct answer must be written down in advance for each test case. You grade by comparing the output against the reference.

Quickly tell me — out of the last three examples we saw (programmatic: evaluating the retriever, human: evaluating chatbot helpfulness, LLM as judge: the UPSC example) — which of these evaluations were reference-based? Meaning, we knew the correct answer beforehand. The answer is known to us in the golden dataset. Quickly think and tell me: in the UPSC example we just discussed, did we know the answer beforehand in the golden dataset?

Yes — we did. See here: where we say how many marks the human is giving — that IS the correct answer. What is "correctness" here? We want to evaluate like a human. So who is correct? The human's evaluation. The human's evaluation was told to us for every answer — how many marks the human gave for this answer. So you (the LLM) should also try to give the same marks. That's what we're telling the system, right? So this is an example of **reference-based evaluation**.

Similarly, if I go all the way up to the retriever example: for this question I told beforehand that the answer is in document 1001. For this other question I told beforehand that the answer is in documents 1001 and 1003. So again, I'm defining the correct thing in advance. So this is also an example of **reference-based**.

Whereas if you look at the human example (chatbot helpfulness): our dataset there was simply the list of questions. That's what we gave to the human — we picked up these questions, gave them to the chatbot, the chatbot answered, and we told the human to evaluate whether the answer is correct or not by looking at it. But there was **no correct answer in the data**. What is the human doing? Reading the rubric and, based on their own judgment, deciding how much to give on a scale of 1 to 5. There's no correct answer defined here. We are relying on human judgment and this rubric.

### Reference-Free Evaluation

This type of evaluation is called **reference-free evaluation**. You have no predefined correct answer. You judge the output's quality directly, on its own terms, against a criteria/rubric. A rubric here is a **scale/standard**, not a per-item correct answer. That's exactly the point I told you.

Going forward, would you be able to classify — if I show you an eval pipeline — whether it's reference-free or reference-based? Simply, you have to ask: is a correct answer given in your golden dataset or not? If it's not given, it's reference-free. If it's given, it's reference-based. Simple — that's the difference.

That's why I specifically taught it this way — that's why in the previous three examples, I deliberately took an example for the human case where there was no reference at all.

---

## Note: Offline vs Online Evaluation (Next Topic)

One very important topic is left: **offline vs online evaluation**. Everything we've studied so far is, in a way, **offline evaluation**. When the system goes into production, evaluation continues even after that — that is called **online evaluation**. We'll study that next. That was one topic left.