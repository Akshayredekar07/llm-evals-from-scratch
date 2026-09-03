# RAG Evaluation Strategy: Complete Framework

## Recap of the Playlist So Far

Before starting today's topic, here is a recap of the entire LLM Eval playlist, because we have already covered two big milestones and it is important to know where we stand in the full curriculum.

In this LLM Eval playlist, the first three or four lectures were spent on introduction and fundamentals, where we understood why LLM evaluation is needed and what LLM eval actually is. We covered:

- Reference based eval and reference free eval
- Online eval and offline eval
- The most important distinction: LLM eval is of two types, model eval and application eval

We said we would focus more on application eval, but we first covered model eval, which we did over the last two or three sessions. While studying model eval, we also discussed that model eval is again of two types:

1. **Standardized eval**, which we call benchmarks. This covered knowledge capability topics where we discussed various benchmarks.
2. **Custom model eval**, which you run for your own application by creating your own dataset. This was covered in the last lecture.

So in summary, this is everything covered in the playlist so far. Now the most important part of this playlist is coming, which is application eval, and we start that from today.

From today we will learn that if you have an LLM based application, how can you evaluate it using the knowledge gained so far.

## Types of LLM Based Applications

You need to understand that there can be different types of LLM based applications:

- A simple chatbot
- A RAG based chatbot
- An agent
- A multimodal app, meaning an application working in some modality other than text, for example an image generator (this is also an LLM based application, but there you are generating images)
- A fixed schema output type application, where your application uses an LLM to produce output in a specific schema. Example: the Zomato case study discussed two or three lectures ago, where you read an email and its content and classify it as a support email, refund email, or technical email. Here the output follows a fixed schema.

It is genuinely not possible to teach application eval for every single type of application. It cannot be done that application eval is taught for chatbots, then for RAG, then for agents, and so on separately.

So a decision had to be made, and it was decided to teach two topics going forward:

1. **RAG**, because it is extremely important. Most chatbots you will build in your professional journey will have RAG functionality, so RAG becomes very important from that perspective.
2. **Agents**, because agents are also very important.

The remaining topics, like evaluating a plain chatbot with no RAG or agent functionality, are not being taught, with the expectation that once you master the harder topics, the easier ones can be figured out on your own. The fixed schema output case is also relatively easy. The multimodal app is a bit different, not necessarily harder, but different from the rest. It can still be done, it is just that multimodal setups are less common in production. Very few companies and very few projects are multimodal in nature. Mostly you will see RAG and agent design patterns, which is why RAG and agent application eval are being covered next.

So today's session and the next two or three sessions will be on RAG eval. Essentially, a RAG chatbot will be built and evaluated properly. After these three or four sessions, you will be able to answer a very important interview question very easily:

**"How do you evaluate your RAG chatbot?"**

This is a very popular question for GenAI interviews. It is asked in about 8 out of 10 interviews, and most of the time students cannot give a satisfactory answer. Many do not even know about it because they never studied evaluation. Those who have studied evaluation also often cannot give a well organized and correct answer.

Guarantee: if you watch today's session and the next three or four sessions attentively, you will be able to answer this question very well and impress the interviewer.

## The Case Study: CampusX Doubt Solver

The next step is to learn RAG evaluation through a case study using everything learned so far. Naturally, a RAG project is needed first to evaluate.

The problem statement was deliberately kept simple. There were many good, more complex problem statement ideas involving different stages of application building, but the goal here is not to build a very complex RAG application. The goal is to learn how to properly evaluate even a simple RAG application. So a very simple problem statement was chosen.

**The project**: a doubt solver for CampusX.

The basic problem statement is that you are taking this LLM course, where roughly two lectures are given every week, and at the end of every lecture, both the recording and the transcript of the lecture are provided. So a transcript of every lecture is available.

What will be done with this:

- These transcripts are used as documents
- These documents are fed into an LLM
- This LLM can then be asked any question or doubt about the entire playlist

Essentially, a RAG chatbot is being built for this specific course, using all the transcripts available. This is only for the LLM course, not other courses, because only this course has transcripts for every lecture available.

There is no need to re-explain how RAG works. It is assumed you already know: there is a retriever, a generator, and a vector database, and an embedding model. So the mechanics are not covered again, only the problem statement.

The plan is to first build this chatbot or RAG project, and then evaluate it. Actually, evaluation happens throughout the building process, not after.

## The Overall Evaluation Framework

The most important discussion now is understanding how this chatbot will be evaluated once it is built. A proper eval suite will be built.

Reminder: whenever you build an LLM based application, there is not just one evaluation. There are multiple evaluations. The RAG chatbot will be evaluated from every angle at multiple levels, and only after passing all these evaluations will it be deployed. Even after deployment, it will continue to be evaluated using online evals.

**The RAG chatbot will be evaluated at three levels:**

1. Component level
2. Pipeline level
3. Application (or system) level

This is a general rule: any LLM based application can be evaluated at these three levels.

### Level 1: Component Level Evaluation

At the component level, components are evaluated while the RAG chatbot is being built, one piece at a time.

**RAG architecture reminder**: There is a retriever and a generator, and a vector database where all documents are stored as vectors. When a query comes in, it is sent to the vector database. The vector database sends back the four (or so) most relevant documents. This entire job is done by the retriever. So the retriever provides the query and relevant context. This query and context are passed to the generator, and the generator produces an answer using these two. This is how a basic RAG chatbot works.

**Building step by step:**

**Step 1: Build the retriever**

This means writing the retriever code:

- Load documents
- Chunk them
- Feed them into an embedding model to convert into vectors
- Use a retriever to fetch relevant documents for a new query

This entire process is called the retriever.

**Step 2: Evaluate the retriever in isolation**

Only the retriever is evaluated, not the full application. The focus is only on whether the retriever built is working properly, meaning whether given a question, the retriever can fetch the correct documents from the vector database.

Two metrics are used here:

- **Recall**: out of all the correct documents that exist, how many were actually fetched
- **Precision**: out of all the documents that were fetched, how many were actually useful

Once this evaluation is done and there is satisfaction that the retriever works properly, move to step 3.

**Step 3: Build the generator**

The generator is essentially an LLM where you provide a question and relevant context, and in return the generator gives an answer. This is built in isolation.

**Step 4: Evaluate the generator in isolation**

Two or three metrics are used here:

- **Faithfulness**: whether the generated answer actually comes from the provided context, or whether the model hallucinated some incorrect information on its own
- **Relevance**: whether the generated answer is relevant to the question
- **Citation accuracy**: whether the citation given is correct. You have probably seen ChatGPT sometimes reference which line or link in a document it took information from. This is called citation.

For this doubt solver, apart from answering the question, it will also tell which session the instructor discussed this topic in, and provide the transcript link for that session. So citation accuracy of the generator will also be checked.

**Important note**: the generator is evaluated in isolation, meaning at this stage it is not connected to the retriever. Manual questions and manual contexts are provided to the generator directly, like a kind of golden dataset. The generator is not getting information from the retriever. That pipeline has not been built yet. This is component level evaluation.

Once the generator has been evaluated in isolation and there is satisfaction that it works well on its own, component level work is complete. The retriever works well in isolation, the generator works well in isolation, and the first stage is done.

### Level 2: Pipeline Level Evaluation

**Step 5: Build the RAG pipeline**

Building the RAG pipeline simply means connecting the retriever and the generator together. This is very simple code.

**Step 6: Evaluate the pipeline using the RAG Triad**

Once the retriever and generator are connected into a pipeline, it needs to be checked whether the whole pipeline works correctly. This evaluation is a very popular term called the **RAG Triad**.

Here, three metrics are checked right after building the RAG pipeline. Why is it called a triad? Because three things exist here:

1. The user's question
2. The context fetched from the vector database by the retriever
3. The answer generated by the generator

There is a metric for each pair of these three things:

- **Question and context**: this metric is called **Context Relevance**, which tells you whether the context fetched by the retriever for a given question is relevant to the question
- **Answer and context**: this metric is called **Faithfulness**, which tells you whether the generated answer actually comes from the context, or whether the model hallucinated
- **Answer and question**: this metric is called **Answer Relevance**, which tells you whether the answer generated is relevant to the question asked

These three metrics are tested for the RAG pipeline in isolation. If all three metrics work correctly, it means the RAG pipeline is working correctly, and this level is complete.

**Note on the overall approach**: this is not a case of building the entire RAG chatbot first and then evaluating it at the end. That is not how it works. Building the chatbot and evaluating it happen together, just like in software engineering, where you do not build the whole application and then test it. You test at the feature level, you test at the function level. Here it is the same: components are tested, then when components are joined the pipeline is tested, and now that the pipeline is built, the application level will be tested.

### Level 3: Application Level Evaluation

**Step 7: Application level testing**

Here you test whether the application, that is the doubt solver, is working correctly overall. More metrics come in at this level:

- **Correctness**: whether the answer that came out is correct
- **Completeness**: whether the answer fully addresses the question asked. For example, if a question has two parts and the answer only addresses one part while ignoring the other, then even though one part is correct, it lacks completeness.
- **Style**: whether the explanation style of the CampusX doubt solver matches the style of CampusX instructors. This is also evaluated and falls under application level evaluation.

These are quality related metrics.

**Step 8: Safety evaluation**

At the application level, safety is also tested:

- Whether the response is toxic
- Whether the response is leaking any personally identifiable information (PII)
- Whether the CampusX doubt solver can be jailbroken

These safety related evaluations are done in step 8.

**Step 9: Operations (Ops) evaluation**

Finally comes operational evaluation, where three main things are checked:

- Latency
- Cost per query
- Number of tokens being consumed

This is called **Ops Evaluation**, done in step 9.

### Summary of the Eval Suite

Everything covered so far, component, pipeline, and application level, is how the entire application is evaluated. Collectively, this is called the **eval suite**. It is like a complete testing suite. Whenever the application needs to be tested, instead of running just one test, all these tests are run together. This helps understand whether the application is working correctly from every angle. This entire collection of tests is the evaluation strategy.

**Question asked**: Are we going to generate a golden dataset?

**Answer**: Yes, many of these evaluations require you to generate a golden dataset. Some evaluations do not need a golden dataset at all.

## The Tooling: DeepEval

In the classes done so far, custom code was written for building evaluations. Especially in the last lecture on custom model evaluation, code was written manually. But this will not be done that way going forward, because writing all this code manually would turn this into a very large project.

Instead, a library called **DeepEval** will be used. In DeepEval, many of the metrics discussed are already available, for example:

- Answer relevancy
- Faithfulness
- Contextual precision and recall
- Contextual relevancy

For safety, things like toxicity and PII leakage are also already available.

So instead of writing custom code to evaluate the RAG application, this excellent library will be used, which is a current state of the art library. Most large companies use this library for LLM based evaluation. The best part about this library is that its entire syntax is based on **Pytest**, the primary Python software testing library. So if you have ever used Pytest for software testing, this library will feel very familiar.

**Why DeepEval instead of Ragas**: Both can be used, Ragas can do all this as well. DeepEval is being chosen specifically for two reasons:

1. Ragas has already been taught in the Advanced RAG course
2. DeepEval is a much broader library. Its scope extends much further, for example to agents, multi-turn chatbots, non-LLM applications, and image based applications. DeepEval can be used for all of these. So its adoption is much higher, and there is a good chance that in a year or two it will become the benchmark library for LLM evaluation, essentially a standard.

So it is a good strategy to give more importance to DeepEval. To be clear, Ragas is also good, there is no problem with it. As already mentioned, two reasons apply: it has already been covered, and DeepEval is a more advanced library compared to Ragas.

## Regression Testing

Once the eval suite is built, a very important task follows called **regression testing**.

**What is regression testing?**

Regression testing is essentially the process of running your eval suite on your application. So far, the eval suite was being built, meaning separate evaluation code was written for different components, pipelines, and the application. Once all of this is built, running it together on the entire application is called regression testing.

**General idea of regression testing**: If version one of your software has run, and now you have built version two of the same software, how do you know that version two is not objectively worse than version one? Has the application gotten worse? How do you check this? The answer is regression testing.

There is nothing special about regression testing itself. You simply run the entire eval suite you built at once, and from running it, you get a result, a full report showing which metric has decreased and which metric has increased. Running the full regression test gives a clear picture of whether the new version of the software is objectively better than the previous version. Based on that, a decision is made on whether to deploy the new version.

### Project Structure for Regression Testing

To explain this in simple terms, a project folder will be built step by step:

- A folder named **src** will contain the source code of the RAG chatbot: the retriever file, the generator file, and the RAG pipeline file. FastAPI might be used for building the API, and Streamlit might be used for building the UI. All this code lives in src.
- A folder named **evals** will contain all the evaluation files:
  - `eval_retriever.py`, which evaluates the retriever
  - `eval_generator.py`, which evaluates the generator
  - Similarly, a separate file for the RAG pipeline
  - A separate file for testing the application
  - A separate file for safety
  - A separate file for operations

All these files inside the evals folder, where all the tests are written, together form the **eval suite**.

- Outside all folders, there will be a file called **run_evals.py**, which contains code that, when triggered, runs all these tests on the application one by one and generates a report.

Analyzing that report tells you whether the new version of the software is objectively better than the previous version. The retriever file tells you whether the new retriever is better than the old retriever. The new generator file tells you whether the new generator is better than the old generator, and so on.

This is how regression testing is done: the application is built step by step, and during the building process, the eval suite is created with multiple evaluation files, and then there is a single script, run_evals.py, to run all those files. So whenever the application is complete or something is changed in it, this run_evals.py file is run, and it generates a complete report on where the new version stands compared to the previous one, helping decide whether the new version should be deployed.

## Advanced Regression Testing (LLMOps Territory)

This next part leans more into the LLMOps and engineering domain rather than pure evaluation, but it is related, so it is worth covering.

Regression testing can be done in much more advanced ways than the simple version described above.

### Level 1: Basic Regression Testing

Running the file once, comparing all metrics with the previous version, and finding out whether the new version is better or not.

### Level 2: Experiment Tracking

If you have studied MLOps, you may have heard of **MLflow**, used to run multiple experiments on your application. The same idea applies here.

Essentially: you build your application for the first time with certain settings, for example:

- How many characters are used for chunking
- How much overlap
- What temperature is used
- Embedding model related settings

All these settings are kept in one place, and the eval suite is run for the first time. This eval suite gives numbers for all the metrics. For example, retriever recall might come out to 82, and precision might come out to 68, and so on for every metric.

These configuration numbers and metric numbers are then logged into a tool like MLflow. This is called experiment 1, with these configuration values, resulting in these metric values. This becomes your **baseline**, the first reading of the software.

After that, you try to improve. For example, you increase the chunk size and decrease the overlap size, then run the application again through the same file. New readings come in for the new settings, and these are logged too. Now you can easily compare it with the previous one. Visually, you literally get a dashboard where you can compare every metric across the last several runs and see how they are fluctuating.

So experiment tracking and dashboarding become part of regression testing. This is a slightly more advanced version, and it becomes even better if you add an experiment tracker and a dashboarding tool.

### Level 3: CI/CD Integration

You can make it even better by adding **CI (Continuous Integration)**.

What this means: you take a CI tool, for example GitHub Actions, and set up a condition so that as soon as you make a code change and push it (say, changing the chunk size value), the CI automatically triggers the eval suite to run again on the full suite.

Once it runs, a new set of readings comes in. This new set is quickly compared with the current baseline. You set a threshold, for example, the new result should not be more than 3 points lower than the baseline.

- If the new reading is lower than the threshold, the new deployment is stopped. The new change is not deployed because it is worse than the current baseline, meaning the software has regressed.
- If the new reading shows improvement over the baseline, deployment is allowed to proceed.

So with CI, you can create a **gating mechanism**. This lets you change your software without worry, push improvements, and deploy them, and it will only get deployed when the changes have a positive impact on the current baseline. Otherwise it gets rejected.

This is how an engineering team handles the whole process. You built an eval suite, and that eval suite is being used as a gating mechanism in regression testing.

Note: It is uncertain whether CI/CD itself will be demonstrated here, since it will likely be covered by Himanshu in the LLMOps classes. This part could have been skipped, but it was mentioned because it is related.

### Summary of the Three Regression Testing Levels

1. **Simple regression testing**: run the software once to get baseline numbers, then manually compare numbers from each subsequent run to see if the software is improving.
2. **Experiment tracking**: add a tool like MLflow to automate this somewhat. Every time the evaluation pipeline is triggered, metric values are logged according to configuration settings, and this can be viewed visually on a dashboard.
3. **CI/CD automation**: bring a CI tool into the process so that whenever the evaluation pipeline runs, it automatically checks whether the new version's metrics are better than the baseline. If better, deployment happens and the baseline is updated to the new metrics. This continues iteratively.

**Note on tools**: MLflow is not the only option for experiment tracking. DeepEval's own company has another tool called **Confident AI** that does this as well. There is also **Weights and Biases**. Many companies and players exist in this space.

**Core principle**: do not get attached to a specific tool. Understand the concept, because once the concept is understood, any tool can be learned within a week. There is no obligation that a company you get hired at will specifically use MLflow. There is no standard tool for LLMs yet the way MLflow has become the de facto standard for machine learning. So the focus should be on the concept, not the tool.

## Deployment and Online Evaluation

Once regression testing is done and it is confirmed that the new version's readings are better than the baseline, the software gets deployed.

But evaluation does not stop after deployment. This was taught before, and this is exactly what happens here. Even after the software is deployed, it continues to be evaluated. This evaluation is called **online evaluation**.

Once the software is live, three or four things are measured:

### 1. Capturing Signals

Every time a student comes to the chatbot and asks a question, the following is captured:

- Latency: how long it takes to answer
- Cost
- Thumbs up or thumbs down feedback

Tools for this: **LangSmith** is one option, there is also **LangFuse**, and **Confident AI** also does this. In the LLM world, this is called **tracing** or **observability**.

Essentially, tracing code is added into the application code, and as a result, as the software runs live, data about every interaction is captured: latency, cost, tokens, thumbs up, thumbs down, all of it, visible on a dashboard such as the LangSmith dashboard.

### 2. Calculating Values Online

Beyond raw captured values, some things are also calculated. Once the software is deployed, the same things that were tested offline, such as faithfulness, answer relevance, and correctness, are also tested online.

### 3. Drift Detection

**Drift** essentially means checking whether the software's performance is degrading over time. There might be a graph of the last 24 hours tracking some metric, for example faithfulness. If the faithfulness graph suddenly drops over the last 8 hours, that is a kind of drift being detected, and then alerts are triggered and steps are taken to improve it.

### 4. Self Improving Loop

Sometimes a chat with a student might reveal that the application behaved incorrectly. If the application misbehaves, those specific examples are picked up and added as part of the offline evaluation, added to the offline dataset or golden dataset. This way, the offline or golden datasets keep getting richer, so that when new versions are built and evaluated offline in the future, evaluation becomes even better. So a loop is added here too.

## Roadmap for the Next Four Sessions

This is how the entire evaluation strategy will play out. The plan is to build a RAG application and test it according to the full framework outlined above.

1. **Next session**: full component level evaluation. This means building a retriever, then testing it, then building a generator, then testing it, using DeepEval for the first time.
2. **Session after that**: build the RAG pipeline and run the RAG Triad metrics (the three metrics).
3. **Third session** (possibly a bit sooner, this is not fully certain): run the full evaluation at the application level.
4. **Fourth and final session**: cover regression testing and online evaluation.

So over the next four sessions, the entire framework built for testing a RAG application will be completed practically. This is the roadmap for the next four sessions.

Today's topic was not started in full detail because the entire discussion takes about 2 hours, and the intention is to complete these 2 hours in one continuous sitting rather than splitting it, for example one hour today and one hour on Saturday, since that breaks the flow. That is why today's class was specifically reserved for this discussion.

## How to Answer "How Do You Evaluate Your RAG Chatbot?"

Based on today's session, this question can now be handled quite well.

If someone asks: **"How do you evaluate your RAG chatbot?"**, here is the framework style answer:

1. "First, I will create an evaluation suite."
   - If asked what an evaluation suite is: "I will test my application at three levels."
     - **Component level**: test the retriever and the generator (name the metrics: recall, precision for retriever; faithfulness, relevance, citation accuracy for generator)
     - **Pipeline level**: mention the RAG Triad (context relevance, faithfulness, answer relevance)
     - **Application level**: mention correctness, completeness, and then safety and operational metrics
2. "Once that is done, I will use these to perform regression testing." Mention that regression testing can have three levels: basic level, experiment tracking level, and CI/CD level. Mention working at whichever level fits the company's needs.
3. "Once regression testing is done and I have a new baseline, I will deploy it, and I will not stop there. I will run online evaluation." Explain what is run online (tracing, calculated metrics, drift detection).
4. "The errors caught there will be collected and added as part of my offline evaluation."

When you answer like this in an interview, the interviewer clearly understands that this person knows the subject, because there is nothing more to RAG evaluation beyond this. This is the complete answer to this question.

**Common mistake candidates make**: Having personally taken interviews, many candidates asked this question do not know the answer at all because they never studied evaluation. Those who have studied evaluation mostly answer with just three or four metric names, like recall, precision, answer relevance, and think that is the complete answer. But there is an actual framework here. When you answer with a full framework like this, the interviewer respects you and recognizes that you know the topic deeply and have actually implemented it.

This is the goal for the next four sessions: to practically implement everything covered here, so it gets embedded more deeply. The intention is for these four lectures to become a resource such that anyone in the world who wants to understand RAG evaluation can watch these four lectures and fully understand it.

The session closes with a promise that the next four lectures are going to be excellent.