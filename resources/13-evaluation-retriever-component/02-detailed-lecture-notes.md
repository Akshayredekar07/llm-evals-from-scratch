# Building and Evaluating the Retriever (RAG Component Level Eval)

## Connection to the Previous Session

Today's session is totally connected to the previous session. In the last session, it was discussed that we are going to start RAG evaluations, or RAG eval as it can be called. A complete roadmap was set for how a RAG application will be evaluated. First, a problem statement was shared: what kind of RAG application will be built. Then a roadmap was shared for how to evaluate it step by step.

So today's class starts right from there. Going forward, over the next three classes including this one, the goal is to build a RAG eval suite. Basically, the RAG application will be evaluated at three levels:

1. Component level
2. Pipeline or workflow level
3. Application level

Once all these evaluation pipelines are built, this is collectively called the eval suite, which will be used in regression testing.

**Today's goal**: complete the first part, which is the component level part of the eval suite. Today we will learn how to evaluate the components of our RAG application.

As you probably know, the two most important components in any RAG application are the **retriever** and the **generator**.

- The retriever's job is to fetch relevant context from the vector database for a given query
- The generator's job is to produce an answer relevant to the question, given a query and relevant context

Today we will learn how to evaluate both of these components. We have built them in the past, but never learned how to evaluate them. Today we learn that.

**Plan for today**: first work with the retriever, then move on to the generator. That said, today's session focuses only on the retriever (the generator will come in the next class based on how things progress).

## Setting Up the Project

Before starting, the project needs to be set up properly, because this project will run across the next two or three classes. It is a good idea to set it up well.

**Steps taken:**

1. Created a new folder called **rag_eval_project** and opened it in VS Code
2. Followed standardized project setup instructions, carried out one by one

### Directory Structure

Instead of randomly creating files, a fixed structure is followed:

- **data/** — stores all the lecture transcript data. Every lecture provided comes with a generated transcript, and these transcripts serve as the knowledge base for the RAG application
- **src/** (source folder) — stores every file created in order to build the application: retriever, generator, RAG pipeline, and later possibly a Streamlit application
- **evals/** — stores all the evaluation pipelines: pipeline to evaluate the retriever, pipeline to evaluate the generator, pipeline to evaluate the full RAG pipeline, etc.
- **goldens/** — stores the golden datasets

These folders are considered sufficient for now; more can be created later if needed.

### Adding Transcripts

The transcripts for roughly the first eight or nine lecture sessions were copied from an existing version of this project (built separately beforehand) and pasted into the `data` folder.

- Transcripts look like movie subtitles: a timestamp is given, and under that timestamp is the information about what the teacher said or what students said
- These are long files, obviously, because lectures run about two hours each
- This is our knowledge base, on the basis of which the RAG chatbot will work

### Creating the Virtual Environment

Since this is a new project, it will have its own dependencies. Instead of installing them globally, they are installed inside the project using **UV**.

Steps:
- Initialize UV
- Use Python version 3.11
- Install all required libraries together

**Libraries needed:**
- LangChain (a lot of the work will go through LangChain)
- OpenAI library
- DeepEval (this is what will be used for testing)
- Pytest (a dependency of DeepEval)
- python-dotenv (needed to work with environment files)

Running the install command installs all these libraries. As a result, a `pyproject.toml` file and a `.gitignore` file appear. Essentially, UV quickly set up the entire project.

### Creating the .env File

The last setup step is creating a `.env` file to store the OpenAI API key. A `.env` file was created and the OpenAI API key was pasted into it.

With that, all setup steps are complete. These were very basic steps that have definitely been done before in past sessions.

## Step 1: Building the Retriever

From here, today's actual session begins. First, the retriever needs to be built.

**Reminder from the last session**: you never evaluate by building the entire application first and then testing it. You operate exactly like software development: build a new module, write a new function, test it, then move forward. Test the new thing, then move forward again, and this is how the application gets built step by step.

Similarly here, while building an LLM based application:

1. Build the first component (the retriever)
2. Evaluate the retriever
3. Once satisfied, move forward and build the generator
4. Evaluate the generator
5. Build the pipeline
6. Evaluate the pipeline
7. Once the application is built, do application level evaluation

This is how you develop an LLM based application. So since this is the start, the first component, the retriever, needs to be built first.

### How the Retriever Works

A retriever is basically a component that receives a query as input. What it does:

1. Converts the query into a vector using an embedding model
2. Takes that vector and searches a vector database
3. The vector database already has chunks stored in vector form
4. Fetches the 5 or 10 nearest vectors, which we call the context

**This setup includes:**
- Fetching documents (currently in the form of transcripts)
- Chunking them
- Embedding them
- Once embedded, building a retriever object that will be used whenever the retriever needs to run or be evaluated

### Walking Through the Retriever Code

The same folder structure (data, evs/evals, golds/goldens, src) applies here. Inside `src`, a file called `retriever.py` was created (code copied from a pre-built version of this project, since exactly the same code was needed here too).

**Explanation of the code:**

- All dependencies are imported. `load_dotenv` is used because the OpenAI API key is being imported from the environment file.
- Setup: the data directory is called `data`. A vector database directory is created, called `chroma_store`. This directory won't be visible until the code is run for the first time — running the code creates the `chroma_store` directory, which becomes the vector store, holding all chunks in vector form.

**Main function: `build_retriever`**

Inside this function:

1. Calls a `load_store` function
2. `load_store` first brings in an embedding model — **text-embedding-3-small** (OpenAI's embedding model)
3. It checks whether the vector database currently exists
   - If it doesn't exist, it creates a new one
   - If it already exists, it does not recreate it
4. If not created yet, it loads all the transcripts into document form using a function called `load_transcripts`

**The `load_transcripts` function:**

This function looks complex but does something simple:

- Goes into the `data` directory
- Loads all the `.txt` files (all our transcript files have this extension)
- Reads them line by line
- For each line, checks whether it contains a timestamp
  - If it has a timestamp, ignore it
  - If it doesn't have a timestamp, pick it up and add it to the text

**Why timestamps are removed**: the strategy is to not use the whole document as-is, only the actual text. If timestamps were kept in, the retriever's quality would come out very poor, because the text would be interrupted by timestamps repeatedly, which would badly hurt semantic meaning capture. That is why a filter is created that removes all timestamp lines and extracts only the normal text, storing it inside LangChain Document objects.

**Also stored**: metadata about which session a particular line was spoken in. This is done so that later, citations can be given, i.e., telling the user that the answer to their question was taught in a specific session. That is why the session number is also extracted, alongside the documents.

**After documents are collected:**

1. Chunking is performed
   - Chunk size: starting small, set at **750**
   - Chunk overlap: **100**
2. Chroma database is used, and chunk embeddings are sent through the `from_documents` function
3. This gets loaded into `build_retriever`, and calling `as_retriever` on it creates the retriever object

Once you have the retriever, you can invoke it with any question. When invoked:

1. The current question is converted into vectors
2. The nearest five vectors are fetched from the vector database
3. Results are stored, and looped over to display

**Quick one-minute recap of the whole retriever code:**

- Load all transcripts
- Remove timestamp lines, convert into Document objects
- Also store which session each line was spoken in
- Chunk the documents: chunk size 750, chunk overlap 100
- Build a vector database from this
- Build a retriever from that vector database, with K = 5
- Perform a query using that retriever object and display the results

Very straightforward code if you have done RAG before.

### Running the Retriever

The code in `retriever.py` was run with the question: **"What is regression testing?"** (this was discussed in detail in the previous session).

- The vector database took some time to build the first time (since it didn't exist yet)
- After that, the query ran and results were shown
- A **Chroma Store** vector database got created
- Output: five chunks were retrieved for the query

At this point, we can say the retriever has been built. It's working — how well it's working hasn't been evaluated yet, but it is working. One component of the RAG application has been built: the retriever.

### Question: How Do We Handle Changes to the Documents?

If a new session is conducted, its transcript will need to be added:

1. Bring the new transcript and paste it into the `data` folder
2. Delete the existing `chroma_store` folder
3. Run `retriever.py` again — this re-performs embedding and brings documents back into vector form

This step has to be repeated every time there are changes to the documents.

**A question was raised**: ideally, data ingestion and retrieval should be decoupled.

**Answer**: That's correct. It's just that the current focus is not on application development, it's more on the evaluation side of things. That's why one shouldn't expect very production-grade code here — this is intentionally simplified. If very production-grade code were written here, a lot of time would go into explaining what's happening. That's why the instruction given (when generating this code with Claude) was to keep it at a very basic level that anyone could understand at a glance. It's a conscious choice.

## Step 2: How Do We Know If the Retriever Is Working Correctly?

Now that we have our retriever, the question is: is the retriever we built actually working correctly or not? Basically, we need to evaluate our retriever somehow.

Before writing evaluation code, a discussion is needed to understand exactly what kind of evaluation code to write.

### How Does a Retriever Fail?

A retriever is basically a function: you give it a query, and it outputs the 5 (or 10, whatever K is set to) relevant contexts related to that query.

**There are ideally two scenarios where a retriever can fail:**

**Failure Mode 1: Missing the correct context entirely**

Suppose there's a question A B C, and the vector database has chunks numbered 1 to 100. Correctly answering A B C requires chunks 1, 15, and 13, because the correct answer is hidden within these three chunks. But the retriever isn't good — for question A B C, it brings back chunks 27, 28, 29. Basically it didn't fetch even a single relevant chunk. This kind of retriever is obviously not a good retriever.

**Failure Mode 2: Bringing correct context, but noisy**

Suppose the correct context was chunks 1, 15, and 13, and the retriever brought back 1, 15, 27, 28, 29. Ideally it should have brought those three; it got two of them right, but the other three it brought were not correct ones. These extra ones can be considered noise. Now if you send all five of these to the generator, you're giving it two correct contexts along with three unnecessary contexts. So it's getting information, but also getting noise. There's a good chance the final answer that comes out won't be great.

### The Two Metrics

Corresponding to these two failure modes, we have two metrics (discussed in the past as well):

- **Recall** — measures how many correct contexts the retriever was able to fetch
- **Precision** — measures how many of the fetched contexts are actually useful

These are the two metrics we will use today to evaluate the retriever.

**Formal definitions:**

- **Recall**: out of all the correct contexts that are available in the vector database, how many of them was the retriever able to bring back. If 5 were correct and the retriever brought back 3, recall = 3/5.
- **Precision**: out of all the contexts the retriever brought back, how many were actually correct. If 5 were brought back and only 2 are useful, precision = 2/5.

Ideally, both recall and precision should be high — the closer both are to 1, the better the retriever you've built.

### The Trade-off Between Recall and Precision

There is a tension, or trade-off, between recall and precision.

**Example**: Suppose recall is currently 3/5 (65%), meaning out of five correct contexts, only three are being fetched. A quick hack to increase recall: **increase K**. Currently K = 5, only bringing back 3 out of 5. Set K to 10 — there's a good chance the remaining two will now also get fetched. Increasing K always increases recall.

**But the problem**: as soon as K increases to 10, precision takes a hit. Because now out of 10 results, 5 are correct, but 5 are also noise. So as recall moves toward 100, precision starts moving toward zero. This is why there is a trade-off between the two, and pushing both up together is a tricky task requiring some thought. K especially trades off precision and recall against each other.

### Question: Are Recall and Precision Reference-Based Evaluations?

**Statement to evaluate**: Both recall and precision are reference based evaluations. True or false?

**Answer: True.**

Reminder of the earlier distinction: reference based eval means that at the time of performing evaluation, you need a golden dataset or golden answer. Reference free eval doesn't need any such golden answer.

To tell whether recall is high or low, you need to know what the correct context looks like for every query. Since you have to state what the correct context is for every query, this requires a **golden dataset** and **golden context**. Since you have to specify what the correct answer is, this becomes a reference based eval.

This point is important because over the next three classes, you'll perform many evaluations, and there needs to be clarity in your mind about which evaluation is reference based and which is reference free. Both of today's metrics are reference based evals, because evaluating them requires a golden dataset and golden context.

## Building the Golden Dataset — First Approach (and Why It's Wrong)

### The First (Flawed) Approach

**Structure**: two columns — Question, and Document/Chunk ID.

Example rows:
- Question: "What is regression testing?" → correct chunks: 72, 89, 100
- Question: "What is RAG Triad?" → correct chunks: 120, 111
- Question: "What are online evals?" → correct chunks: 151, 121, 130

This way, a dataset of about 50 questions is built, with document IDs marked against each question indicating where the relevant context lives.

**Calculating recall with this dataset:**

- Send the first question to the retriever
- Retriever returns 5 chunks (since K=5): e.g., 72, 81, 89, 99, 100
- Recall = how many of the expected chunks (72, 89, 100) appear in the retrieved set. All three appeared → recall = 3/3 = 1 (perfect for this question)
- Repeat for the second question ("What is RAG Triad?"): retriever gives 1, 2, 3, 120, 5. Expected: 120 and 111. Only 120 appeared → recall = 1/2
- Repeat this for all 50 questions, then average all the recall values → that average is the overall recall

**Calculating precision similarly:**

- First question: 5 chunks retrieved, 3 correct, 2 noisy → precision = 3/5
- Second question: 5 chunks retrieved, only 1 correct → precision = 1/5
- Average across all rows gives overall precision

Together, these two numbers tell you how well your retriever is performing.

### Why This Approach Is Wrong for This Application

**Important claim**: this method, where the golden dataset stores IDs of correct documents/chunks and recall and precision are calculated on that basis, **cannot be used** for this application — and in fact cannot be used for many types of RAG applications.

**Question posed to the audience**: why is this approach wrong here, even though it seems very logical? This method is taught in many books and YouTube channels, and it does work in some places, but it will fail in many places.

**The real reason**: 

Think about the person who would be given the job of creating this golden dataset. Would they be happy in their life doing this job, or would they want to quit? The task given to them: go through every single chunk manually and figure out which chunks are related to a given question.

At this point, the number of chunks in this project was checked by printing the chunk count — roughly **800+ chunks** after chunking. So the person doing this task would need to:

1. Read a question
2. Go through all 800 chunks and decide which ones (say, three of them) contain content that answers this question
3. Repeat this process for the next question
4. Repeat this 50 times (since there are 50 questions in the dataset)

Nobody would want to do this job — it's extremely tedious.

**But suppose someone did do it.** They stayed up all night and finished it. The next day, running the retriever against this golden dataset gives a recall of 65, which obviously isn't great. To improve it, K could be increased from 5 to 8.

**The real problem surfaces here**: as soon as you change chunking parameters (say, chunk size and overlap, from 750/100 to 1000/150), the chunks themselves change. Since the chunks change, the entire vector database has to be recreated. And now you have new chunks — where you had 800 chunks before, increasing chunk size might reduce that to 700 chunks. As soon as the chunks are new, **the golden dataset becomes void** — the chunk IDs recorded earlier are no longer meaningful, since they were valid only for the previous chunk size. The golden dataset has to be built again from scratch.

So every time chunking parameters are changed, the golden dataset has to be rebuilt. This is a terrible engineering pattern — the dataset creation task was already extremely hectic, and now it needs to be redone every time parameters are tweaked. **This will not work.**

**When does this approach actually work?**

There are certain applications where this method can work — for example, when the documents are very cleanly separated from each other (Document 1 is very different from Document 2, Document 2 is very different from Document 3). In such cases, chunking parameters aren't tweaked much once set, so this type of golden dataset (with fixed IDs) can be used.

**But in our case, this is not true.** Documents are related, and information can be spread from one document into another. There could be a question whose answer was given in Session 1 and also touched on again in Session 5. That is why chunking parameters will need to be tweaked, and every time they change, the golden dataset would become void, requiring a brand-new golden dataset each time — way too much effort. That is why this approach cannot be used.

## The Correct Approach: A New Kind of Golden Dataset

So how do we actually calculate precision and recall? Time to discuss the real method.

### New Golden Dataset Structure

Two columns again:
1. **Question**
2. **Ideal Answer** (not context or document IDs this time)

**Example:**
- Question: "What is regression testing?"
- Ideal Answer: the actual definition of regression testing as taught in class, written here. This was created by going to the relevant document IDs, and combining information from those chunks into an answer.

**Very important note**: "ideal answer" does not mean an answer fetched from Google. It means the answer that was actually taught in class, based on what is in the vector database (the transcripts).

- Question: "What is RAG Triad?" → similarly, someone goes to the relevant chunks, combines the material, and creates the ideal answer
- This process is repeated for 50, 100, or 500 questions

This is the golden dataset: rows of (question, ideal answer), where the ideal answer is based on what was taught in the transcripts, not something pulled from Google.

### Calculating Recall With This New Dataset — Using LLM as a Judge

Steps:

1. Take the first question ("What is regression testing?") and send it to the retriever
2. Retriever searches the vector database and returns 5 contexts: 72, 81, 89, 99, 100
3. Bring in an **LLM as a judge**
4. Tell this LLM: "Here is our ideal answer. First, break it down into claims."

**Example**: suppose the ideal answer has three sentences:
   - Sentence 1: "Regression testing is basically a way to test whether your new version is better than your previous version"
   - Sentence 2: "It runs an eval suite against your software"
   - Sentence 3: "It can be used for CI as well"

The LLM breaks this into **three claims**, one per sentence.

5. Now ask the same LLM: go through each of the five retrieved contexts, one by one, and tell how many of these three claims exist in each context

**Result:**
   - Claim 1 was found in chunk 72
   - Chunk 81 had no claims
   - Claim 2 was found in chunk 89
   - Chunk 99 had no claims
   - Claim 3 was found in chunk 100

This means all three claims from the ideal answer were found somewhere across these five contexts. This means 100% of the required context to answer this question was retrieved. So the calculation becomes **3/3 = 1**.

**Repeat for the next question**: "What is RAG Triad?"

Sent to the retriever, which produced chunks: 1, 2, 3, 120, 5.

Suppose the ideal answer has two claims:
   - Claim 1: "RAG Triad is basically a combination of three metrics"
   - Claim 2: "It includes answer relevance, faithfulness, and context relevance"

LLM checks all five retrieved chunks for these claims:
   - None found in 1
   - None found in 2
   - None found in 3
   - Claim 2 found in 120
   - None found in chunk 5

So one out of two claims was found somewhere in these five. **Recall for this question = 1/2**.

Repeat this process for all questions in the golden dataset.

**Why this approach is much better**: think about it — if recall comes to 65 and chunk size is increased to improve it, does the golden dataset need to change? Since the ideal answer was already written based on the actual teaching content, will chunk changes affect the ideal answer? **No, the ideal answer stays the same.** The information may shift from one chunk to another chunk, but that doesn't matter — the ideal answer is still the ideal answer. The effort done once doesn't need to be redone just because chunk boundaries move. This saves us from repeatedly rebuilding the golden dataset.

**This is why this technique is used instead of the previous one.**

This exact technique is used inside DeepEval, and in DeepEval's terminology, this is called **Contextual Recall**. (What was taught earlier as "Recall @ K" is not what's being used here — this contextual recall is a different flavor, using the LLM-as-a-judge approach.)

**A question posed**: what are the chances that the LLM-as-judge combines multiple claims into one, and our retrieved context comes split across different chunks?

There are chances, but two design choices reduce the risk:

1. The person creating the golden dataset writes the ideal answer in such a way that atomic claims combine cleanly, so an LLM breaking it down into claims does it easily
2. Using a good quality LLM judge with a well written system instruction that it follows carefully

### Calculating Precision With the New Dataset

Similar technique. Take the first question, send it to the retriever, get back the same 5 chunks: 72, 81, 89, 99, 100.

This time, you don't need to convert the ideal answer into claims. Instead, you simply give the LLM-as-judge a prompt:

> "Here is the question. Here is the ideal answer. Here is one retrieved chunk. Is this chunk relevant? Does it contain information that helps produce the expected answer? Answer yes or no, and give a reason."

This system prompt is applied to each chunk one at a time:

- Take question, ideal answer, and current chunk (say chunk 72)
- Ask the LLM: does this chunk help produce this answer? Yes or no?

Following this process for all five chunks tells you which ones are correct and which are noisy. Then precision = correct chunks / total chunks retrieved, e.g., **3/5**. Repeat this for all questions and average across all of them to get overall precision.

### An Important Nuance: Precision Considers Rank Too

Precision as calculated so far (correct out of total retrieved) doesn't distinguish between two cases with the same ratio but different orderings.

**Example — two cases, both with 3 noisy chunks and 2 correct chunks out of 5:**

- **Case A**: positions 1, 2 correct; positions 3, 4, 5 noise
- **Case B**: positions 1, 2, 3 noise; positions 4, 5 correct

By the basic precision formula (correct/total), **both cases give the same precision (2/5)**. But which is the better retriever? Obviously **Case A**, because it brought the correct contexts to the top of the ranking, rather than burying them at the bottom. Case A is a better retriever than Case B, but plain precision cannot distinguish between them since the ratio is identical.

**This is why DeepEval's precision metric is called Contextual Precision** — it is rank aware.

**How it's calculated** (walking through both cases):

**Case A** (correct, correct, noise, noise, noise):
- After seeing 1 chunk: 1/1 correct so far → 1
- After seeing 2 chunks: 2/2 correct so far → 1
- After seeing 3 chunks: 2/3 correct so far → 0.667
- After seeing 4 chunks: 2/4 → 0.5
- After seeing 5 chunks: 2/5 → 0.4
- Average of these five values gives the overall contextual precision for Case A

**Case B** (noise, noise, noise, correct, correct):
- After 1 chunk: 0/1 → 0
- After 2 chunks: 0/2 → 0
- After 3 chunks: 0/3 → 0
- After 4 chunks: 1/4 → 0.25
- After 5 chunks: 2/5 → 0.4
- Average of these five values gives the overall contextual precision for Case B

**Case A's average will clearly be higher than Case B's average**, correctly reflecting that Case A is the better retriever, even though basic precision treated them the same.

So contextual precision still captures the basic idea (how many of the retrieved are correct), but also incorporates whether the correct ones are ranked higher. This is the calculation method used in DeepEval.

### Summary of the New Method

The last 15-20 minutes covered a new technique: using a golden dataset with (question, ideal answer) pairs, and calculating recall and precision using an LLM-as-judge approach. This is the method that will be followed to calculate contextual precision and contextual recall for the retriever.

This was all the theory needed to understand how the evaluation will be carried out. Important point: both calculations use **LLM as a judge** — this is not a programmatic evaluation anymore. The initial plan was programmatic evaluation, but a problem came up (explained above) which led to changing the approach.

## How to Build the Golden Dataset

Before proceeding, the biggest question: how will this golden dataset actually be created? There are **three or four methods**:

### Method 1: Hand-Authored (Best but Not Scalable)

You create the dataset entirely by hand. This requires having full knowledge of all the data.

Since the instructor has personally taught all these classes, he knows exactly what was taught in which session, making this feasible for him:

- Think of a question to put in the golden dataset, e.g., "What is RAG Triad?"
- He knows RAG Triad was taught in session 8 (the last session)
- Go to the chunks belonging to session 8 (maybe 15-30 chunks)
- Find which chunks discuss RAG Triad
- Bring those chunks and construct an answer from them (possibly with LLM help)
- Repeat this process 15, 20, 25, or 50 times

**Why this is the best method**: human judgment is involved, so the chance of mistakes is low.

**The only problem**: it is not scalable. After making 50 questions this way, the person would get tired, or if someone else is hired to do it, they need to be paid.

### Method 2: LLM-Assisted Drafting (Used for This Session)

This is the method actually used for this project:

- Upload the dataset (transcripts) to Claude and explain what kind of dataset is needed
- Once the dataset is generated, review it very carefully

Here, the creation work is not done by the human — but the human's job is to review it carefully.

**Process actually followed:**

1. Took all the transcripts, put them into Claude
2. Gave clear instructions: "I need to build a RAG chatbot. I need to evaluate its retriever. To evaluate the retriever, I need to measure contextual precision and contextual recall. For that I need a golden dataset with column 1 being X and column 2 being Y. Can you create it for me?"
3. Did not generate too many questions at once — generated them one at a time: first question, then second, then third, then fourth, and so on, building a set of **15 questions**

**Benefit**: cost, time, and effort are reduced. **Risk**: chances of mistakes can increase — the LLM might write something in the answer that wasn't actually taught in class, or might pull in something it read on the internet rather than from the actual course transcripts. That is where human review becomes important, to manually remove such incorrect points.

**Result reviewed**: the 15 questions produced this way (stored in a `retriever_goldens.json` file) read like genuine student questions, for example:
- "What is an online eval and how is it different from offline eval?"
- "What is the difference between faithfulness and groundedness?"
- "How do I know if my eval is reference based or reference free?"
- "Why can't we test LLM apps the same way we test normal software?"

These sound like genuine student language, and the answers were pulled from the actual transcripts. This was manually verified for these 15 questions.

### Method 3: DeepEval's Synthesizer Module

DeepEval has a **Synthesizer** module that can also be used to generate golden datasets.

**Honest experience shared**: this was tried for this project, and the experience was not great. A file called `generate_gold.py` demonstrates this:

- Loads all transcripts and performs chunking
- Picks some random chunks and sends them to DeepEval's Synthesizer
- The Synthesizer is a class inside DeepEval that has an LLM set up internally with instructions to create a golden dataset in a particular format

**Running this code**: it generated a file called `retriever_deepeval_golden.json`. Reviewing this output manually revealed problems:

- Example question: "What specific grade school math problems does the GSM8K dataset contain for model training?" — this seems okay-ish, since GSM8K was discussed in a benchmarks class
- Example question: "Access methodologies to validate LLM's robustness against adversarial exploits and misinformation generation" — this doesn't sound like something a real student would ask on this doubt solver; the language doesn't match. The synthesizer over-optimized the question generation.
- Example question: "Is the platform's success criteria to evaluate UPSC answers exactly as human experts do with consistent accuracy?" — this pulled from a UPSC example given long ago in a session, but it's not exactly useful since the course is more about LLM evals in general, not specifics of that particular UPSC application.
- Another example about schema details and descriptive prompts helping LLMs parse technical columns — again pulled from wherever it found relevant text, without judgment about what's actually useful for the doubt-solver context

The Synthesizer has no idea where to focus, what kind of questions people will actually ask in a doubt-solving context — it just extracts questions from whatever transcript content it's given. The quality wasn't good enough to use for evaluating the retriever in this project.

**Conclusion**: this technique is not being used for the current application, although it is a technique people do use, and DeepEval does offer this option. Even with this method, heavy human review is required afterward, since ultimately it's still LLM generated.

### Method 4: Mining Logs From Production

Once the app is deployed, users will come and ask questions. Sometimes the app gives a wrong answer, sometimes a right one. For interactions that get positive signals (thumbs up, etc.), you can turn those into golden dataset entries, since it shows the retriever and the full chatbot worked correctly there.

This is another way of building a golden dataset, but obviously it can't be the very first method used, since you need some entries to start with.

### Summary of the Four Methods

1. Do it manually yourself
2. Do it with LLM help (reviewed carefully)
3. Do it with DeepEval's help (Synthesizer)
4. Pull from production logs and keep adding to the dataset over time

**Method actually used**: Method 2 (LLM-assisted drafting). A file called `retriever_goldens.json` was created inside the `goldens` folder, containing the 15 manually-reviewed question/ideal-answer pairs.

## Current Position in the Plan

At this point, we know:
- We built the retriever
- We had a detailed discussion about how to evaluate it (first the wrong way, then why it's wrong, then the right way)
- We learned how to build our golden dataset

Now we are ready to actually carry out the evaluations. We know what needs to be done, and we have a golden dataset. Next: use DeepEval to calculate contextual precision and contextual recall.

## Introduction to DeepEval's Structure

Before diving into the code, a short intro to DeepEval's basic pattern. Whenever you perform an evaluation using DeepEval, you primarily work with **three things**:

### 1. LLM Test Case

An **LLM test case** basically represents **one row of your golden dataset**. Whenever you see this term in DeepEval code, it simply means we're currently talking about one row of the golden dataset.

**Example**: a small demo where an application's **Answer Relevancy** metric (another RAG Triad metric) is being tested. Since there are two rows in the golden dataset here, there are two LLM test cases:

- **LLM Test Case 1**: input = "What is the capital of France?", actual output = "The capital of France is Paris."
- **LLM Test Case 2**: another question and its actual output

Each LLM test case has fields such as **input** (the question) and **actual output** (the answer produced).

### 2. Metric

The metric decides which dimension you want to evaluate the application on. In the example, the metric used is **Answer Relevancy**. Similarly there's **Contextual Precision**, **Contextual Recall**, and so on.

Each metric has some parameters you can set:

- **Which LLM to use as judge** for calculating that metric (e.g., using GPT-4.1)
- **A threshold** — if the score falls below this threshold, that particular test case is considered failed; if above, it's considered passed
  - Example: if precision for a case came out to 1/2 (0.5) and the threshold was set higher, that test case would fail
- **Include reason = True** — this tells you the reason why a test case passed or failed

### 3. The `evaluate` Function

This function simply runs the specified metric(s) against the specified test case(s), and gives you a score. That's it.

**General structure of any DeepEval code:**

1. LLM Test Case(s) — representing rows of your golden dataset (one or many)
2. Metric(s) — one or more metrics you want to evaluate against
3. `evaluate` function — evaluates the test case(s) based on the metric(s) provided

## Writing the Retriever Evaluation Code

Using this exact structure, code was written to evaluate the retriever on two metrics: **Contextual Recall** and **Contextual Precision**. This code lives inside `evals`.

**Walking through the code:**

- Imports, including importing the retriever from `src`
- Sets the path to the golden dataset
- Sets which model will act as the judge (LLM as a judge)
- Sets a threshold

**Main logic:**

1. Load the golden dataset (a JSON file, the same one just created)
2. Loop over the JSON file — with 15 questions in the file (labeled G01 through G015), the loop runs **15 times**
3. In each loop iteration:
   - Call the retriever with the current question
   - Retriever returns 5 contexts
   - Extract the text of these five contexts into a variable
   - Build an **LLM Test Case** object for this row:
     - **input**: the question
     - **expected output**: the ideal answer fetched from the golden dataset
     - **retrieval context**: whatever the retriever sent back
     - **actual output**: since the generator isn't in the picture yet, a placeholder text like "Generator not evaluated in this run" is used here (can be ignored)

**Summary**: loop over the golden dataset, convert each row into an LLM Test Case object, sending three things per test case: the question, the ideal answer, and the retrieved context for that question.

**Metrics used:**
- Contextual Recall Metric
- Contextual Precision Metric

Settings inside each: threshold, judge model, include_reason = True.

**Calling `evaluate`**: passing in all 15 test cases and the two metrics.

**Configuration logging**: the code also logs configuration parameters used in this run — embedding model, chunk size, chunk overlap, top K value, judge model, golden dataset path. But the main code is really just two key lines:

1. Build 15 LLM test cases (since there are 15 rows in the dataset)
2. Work with the two metrics together
3. Call `evaluate` and pass both

This is the structure of the code — this is the essence of a DeepEval script.

### Running Into an Import Error

The code was copied into `evals/eval_retriever.py` and run using:

```
python eval_retriever.py
```

**Error encountered**: `ModuleNotFoundError: No module named 'src'`.

**Cause**: the retriever import line was failing because `retriever.py` is a separate file living inside `src`. Since the eval script is run from inside the `evals` folder, from that perspective, the `src` folder doesn't exist relative to it.

**Fix**: convert both `src` and `evals` into proper Python modules by creating an `__init__.py` file inside each. Then instead of running the file directly, run it as a module:

```
python3 -m evals.eval_retriever
```

This resolved the error, and the evaluation started running — DeepEval began processing all the test cases.

## Running the First Evaluation (Baseline)

**Results of the first baseline run:**

- **Contextual Recall**: 80
- **Contextual Precision**: 80
- **5 out of 15 test cases failed**

Ideally, you should go and fully study the "reason" given for each test case — reading these reasons is how you understand exactly what mistakes are happening in which test cases.

**Baseline recorded:**
- Recall: 80
- Precision: 80
- 10 out of 15 test cases passed, 5 failed

This is the current scenario — congratulations, the first eval run has been completed. Now it's time to improve the retriever.

## Improving the Retriever

### Improvement 1: Increasing Chunk Size and Overlap

**Suggestion discussed**: the two chunking parameters — chunk size and overlap — can be changed. Currently: 750 and 100 (deliberately set low to leave room for improvement).

**Change made**: chunk size increased to **1000**, overlap increased to **150**.

Steps:
1. Changed these values in `retriever.py`
2. Changed the same values in `eval_retriever.py`
3. Since chunking parameters changed, the existing vector database (`chroma_store`) had to be deleted, otherwise a new one wouldn't get created
4. Ran the eval code again

**Result**: total chunk count printed as **697** (recall: this print statement was set up earlier specifically to show total chunk count).

**New scores after this change:**
- **Contextual Recall: 97**
- **Contextual Precision: 83**
- Now only **3 out of 15** test cases are failing (previously 5)

This became the new baseline.

### Improvement 2: Adding a Reranker

**Question posed**: recall is already quite good (93% pass rate roughly), but how can precision be improved further?

**Suggestion from a participant**: implement a **reranker**. Adding a reranker into the picture almost always increases precision, and the reason follows directly from the earlier discussion: contextual precision is rank-aware — it's not just about how much noise came in, but also whether correct items are ranked higher.

**What a reranker does**: takes the retriever's context and reranks it — bringing the most meaningful chunks to the top and pushing non-meaningful ones down. Since meaningful ones move up and noisy ones move down, precision should increase by definition.

This class doesn't aim to teach reranker mechanics in depth (already covered by Himanshu in the advanced RAG track) — it is directly implemented here just to show the effect.

**Implementation**: 
- A pre-built reranker file exists inside `src` (alongside `retriever.py`), copied over
- In the eval code, the line that was previously `build_retriever` is now changed to `reranking_retriever`

**Result after adding the reranker:**
- Precision moved from 83 to **85**
- Recall dropped slightly
- Now only **2 out of 15** test cases fail (previously 3)

This is an improvement based on the threshold set. The underlying model powering this specific reranker is a sentence-transformer model downloaded from Hugging Face.

### Improvement 3: Upgrading the Embedding Model

**Suggestion**: try improving the embedding model itself.

Change made: switched from `text-embedding-3-small` to `text-embedding-3-large` (both when building the retriever and, since a new embedding model was used, when loading — the vector database had to be deleted and recreated too, since it changes the embedding model, obviously increasing cost).

**Result after switching to the large embedding model (with reranker still applied):**
- Recall jumped to **99%**
- Precision came back to **85** (no additional gain here)
- 3 test cases failed this time (slightly worse than the 2 that failed just before, though recall improved a lot)

### Trying K = 3

**Suggestion**: try lowering K (currently 5) to 3, since precision is proving harder to push further.

Changed K to 3 in `retriever.py` (no need to rebuild the vector database for this change, since only the retrieval count changes).

**Result**: precision actually dropped slightly to **84**. A small amount of variation like this is expected because the golden dataset only has 15 rows — such a small sample naturally introduces some run-to-run variance, even with the same settings.

**Conclusion on this attempt**: lowering K didn't really help.

### Final State and Wrap-up

Rough summary of where things landed:

- Achieved a recall of **95+**, which is very good
- Achieved a precision of around **85**, which is also fairly good

**Remaining ideas for further improvement** (not tried further in this session):
- Try an even better quality reranking model
- Try even larger chunking settings (e.g., 1500 chunk size with 200 overlap, instead of the current 1000/150)

**Summary of today's session**: for the first time, a RAG project's retriever was built, and beyond building it, we now have a very important piece of information: how good its retrieval quality actually is. We can now say the retrieval quality of this retriever is genuinely good — recall above 95, precision around 85.

With this, one can move forward with more confidence and build the generator, which is planned for the next class. That was the main idea of today's class: build a retriever, evaluate it, and improve it.

According to the original plan, the component-level work needed both retriever and generator evaluation. The retriever part is now done. The generator remains for the next session.