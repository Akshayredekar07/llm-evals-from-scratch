### Recap: What We Have Covered So Far In This Class

Before jumping into today's topic, here is the full flow of the course so far, exactly as discussed in class:

- First, we studied **why model evals are important**.
- Then we formally studied **what model evals actually are**.
- We learned that there are two types of model evals:
  - **Standardized benchmarks**
  - **Custom evals**
- Today's session is entirely about **benchmarks**.
- Before studying benchmarks, it was explained that we first need to know **which core capabilities exist**, because benchmarks are built to test those capabilities.
- We studied that **there are eight core capabilities**.
- Now that this foundation is done, we are fully equipped and prepared to actually study what benchmarks are.
- The plan for this session is to spend the next 10-15 minutes on this topic, kept in a high-level overview mode so that most things become clear.

---

### What Is A Benchmark? (Simple Definition)

- If someone asks in the simplest words what an LLM benchmark is: it is one of the most famous terms in this space. Every day, left, right, and center, whenever a new model comes out, benchmark numbers are thrown at you — "this model scored this much on SWE-bench," "this model scored this much on ARC-AGI," and so on. Entire YouTube videos are made comparing how different models score on different benchmarks.
- **Simple definition:** A benchmark is basically **a standardized test used to measure a particular model capability**.
- In simple words, a benchmark is nothing but a standardized test that checks some specific capability of a model.

---

### The Four Components Of Every Benchmark

Any benchmark you pick up will have these four things inside it:

1. **Dataset / Task**
2. **Run configuration**
3. **Scoring method**
4. **Aggregation method**

To understand these four components properly, we take one example benchmark and study it in detail.

---

### Example Benchmark: GSM8K

- The benchmark we are using as an example is called **GSM8K**.
- This is an older benchmark — it came around 2020-2021 — and is not used as much anymore (it has become saturated, discussed later).
- **Full form:** GSM stands for **Grade School Mathematics**.
- **8K** means that the dataset for this particular benchmark has around **8,000 rows**.
- We will use this benchmark as a lens to understand what goes inside any benchmark.

---

### Component 1: Dataset And Task

- The dataset is **the question plus the answer key**.
- Whenever a benchmark has a dataset, it contains two things: questions and answers. It is like a **golden dataset**.
- In GSM8K's case, the dataset contains math questions along with their solutions.

**Sample question from GSM8K:**

"Natalia sold clips to 48 friends in April, and then she sold half as many clips in May. How many clips did she sell altogether?"

- April: 48 clips
- May: 24 clips (half of 48)
- Total: 48 + 24 = 72
- The answer given in the dataset is indeed 72.

- These are basically very simple mathematical questions — the kind of math taught in grades 6th, 7th, 8th (grade school math).
- The dataset has around 8,000 such question-answer pairs.
- This dataset is publicly searchable — you can Google "GSM8K" and find it on places like Hugging Face and Kaggle. It contains a "Files and versions" section where you can browse the actual data: question column, answer column, and around 8,500 question-answer pairs in total.
- Similarly, MMLU has its own dataset, and every other benchmark has its own dataset — every benchmark has a dataset containing both questions and answers, along with a defined **task**.
- **The task** for GSM8K: when the model is given a simple grade-school mathematics problem, it has to generate the answer. This is the task.

---

### Component 2: Run Configuration

- Every benchmark gives you some guidelines about what typical settings you should use while performing the evaluation.
- It is not acceptable to run one model under one setting and another model under a completely different setting. When comparing two models, all the settings during the run must be **exactly the same** for both.
- These settings are described in the **run configuration**, which has three parts:
  1. Prompt construction
  2. Decoding and sampling configuration
  3. Scoring strategy and environment (tool usage)

#### 2.1 Prompt Construction

- This defines how exactly the prompt sent to the model is built.
- **Zero-shot vs Few-shot:**
  - **Zero-shot** means you simply give the question to the model and ask it to solve it, without showing any example.
  - **Few-shot** means you first show the model a few solved examples of similar questions in the prompt, and then attach the actual question at the end, asking it to solve that one.
  - GSM8K is **classically reported as 8-shot** — meaning before sending the actual question, eight solved examples are shown to the model in the system prompt.
  - Naturally, zero-shot performance will usually be worse, and few-shot performance improves the model's results. GSM8K uses few-shot (8-shot).
- **Chain of thought vs direct answer:**
  - If chain of thought is allowed, the system prompt instructs the model to solve the problem step by step (as seen in the example: "Natalia sold 48/2 = 24 clips in May. Natalia sold 48 + 24 = 72 clips altogether.")
  - If chain of thought is not allowed and the model is told to directly give the answer, the chances of mistakes go up.
  - GSM8K allows chain of thought.
- So, when constructing the prompt, you must decide: few-shot or zero-shot, chain-of-thought or direct/normal — these are the available options.

#### 2.2 Decoding And Sampling Configuration

- **Temperature** is usually kept around **zero**. If temperature is increased beyond zero, the model starts giving more creative answers, and results start varying every time you run it. For this kind of benchmark, temperature is mostly kept near zero.
- **Max tokens** is also set beforehand.
  - If max tokens is set too low, since chain of thought is triggered, the model may run out of tokens mid-reasoning and fail to produce the final answer.
  - If max tokens is set too high, a very powerful model might reason very extensively.
  - So max tokens is fixed in advance and applied equally to every model being compared — not too little, not too much.

#### 2.3 Scoring Strategy And Environment (Tools)

- A scoring strategy is finalized in advance. This is quite an interesting part.
- **Pass@1:** The model is shown the question once. It gives one answer, which is either right or wrong. This is called pass@1.
- **Pass@k:** For example, pass@5 means the same question is asked to the same model five times. If the model gets it correct in at least one of the five attempts, it is considered correct. So pass@k is a **more lenient** strategy, while pass@1 is a **stricter** strategy.
  - You have to decide in advance whether to use pass@1 or pass@k during evaluation.
  - For GSM8K, it is most likely pass@1 (would need to check the paper to confirm exactly), but some benchmarks may use pass@k depending on how difficult their questions are.
- **Majority@k:** The same question is asked k times, giving k different answers. Whichever answer appears the most number of times (the mode, like in mean-median-mode) is taken as the final answer.
- So whenever you read a benchmark result and someone says "our model scored 82% on this benchmark," you should dig in and ask: was pass@1 used, pass@k used, or majority@k used? Different scoring strategies are used across different benchmarks, and you should know which one was used before trusting the number.
- **Tool usage** is also decided in advance — whether tools are allowed during evaluation or not.
  - For example, if web search is allowed, the model could simply search the internet for the answer to a question.
  - If a code interpreter is given, the model could solve all the mathematical questions through code.
  - So whether tools are allowed has to be decided beforehand.
  - GSM8K does **not** allow tools.
  - Some benchmarks do allow tools — for example, **SWE-bench** (the software engineering benchmark) requires the model to solve GitHub issues, which requires tools to fetch issues from GitHub. So SWE-bench is a benchmark where tools have to be allowed.

---

### Component 3: Scoring Method

There are two important parts to the scoring method:

1. **Extraction of the model's answer**
   - The LLM's raw response can come in any format. For example, for the answer 72, the model might respond with "The answer is 72," or just "72," or "72" written in some other form — because it's an LLM, it can give output in many different forms.
   - So first, work has to be done on **extraction**. This is usually done using structured outputs (enforcing structured LLM output) or using regex, to make sure the answer is correctly extracted in the right format.
   - In GSM8K's case, the correct answer is 72, so only that number needs to be extracted — nothing else.

2. **Comparison**
   - Once extraction is done, comparison happens.
   - For something like GSM8K (a math test with a clear numeric answer), this is an **exact match comparison** — checking if the extracted number equals 72. Anything else is wrong: scored as 1 or 0.
   - This is a **closed-ended answer** (like 72). But if a benchmark produces **open-ended answers** (like a full paragraph as the answer, which is not as straightforward as "72"), then you need to use an **LLM-as-a-judge** to evaluate it. (An example of such a benchmark will be discussed in a future session.)
   - So comparison is either done straightforwardly and programmatically, or through LLM-as-a-judge, or through human evaluation.

---

### Component 4: Aggregation

- Aggregation is quite simple.
- Suppose the full dataset has 8,000 (or 1,000 for this explanation) questions, and for each question you get a 1 or 0 (correct or incorrect).
- In the aggregation stage, you simply aggregate this — for example, "out of 1,000 questions, 920 were answered correctly by the LLM," which basically means the LLM scored 92% on this benchmark. That's how aggregation is done.
- Aggregation is mostly straightforward, as shown above.
- But sometimes aggregation is **not** straightforward. For example, **MMLU** checks general knowledge across 57 subjects. Here, you might need to publish a separate result for each subject — Biology 87%, Physics 91%, Economics 72%, and so on.
- Now, to combine all these into one overall aggregate score for MMLU, you cannot simply add up all the percentages and divide by 57 — because the dataset might have fewer Biology questions and more Economics questions, for instance. So a **weighted mean** might be required instead.
- Aggregation strategies can differ depending on the benchmark.

---

### Summary Of What A Benchmark Is

- A benchmark is basically a standardized test.
- Inside that test, multiple things exist:
  1. **Task** — what to measure
  2. **Dataset** — with both questions and answers
  3. **Run configuration** — the exact conditions under which the test is executed
  4. **Scoring mechanism**
  5. **Aggregation mechanism**
- Where is all of this written down? In the **research paper**.
- Most benchmarks used today were originally published as research papers. For example, searching for the "GSM8K paper" brings up the original paper where researchers first introduced this benchmark to the world. This paper discusses everything — which dataset was used, what run configuration was used, what scoring mechanism was used, what aggregation mechanism was used.
- The same dataset is then made available on the internet.
- Similarly, MMLU also has its own research paper with the same information, following the same overall structure: task, dataset, run configuration, scoring mechanism, aggregation mechanism. SWE-bench most likely also follows the same structure.
- So each benchmark was originally a research paper brought forward by researchers. This is literally the researchers' job — studying how a particular capability of a particular LLM can be tested. Researchers from their respective fields bring their own benchmarks, and those benchmarks become popular. Their datasets become popular, and then every new LLM that comes to market gets measured on them.
- Note: benchmark names were intentionally not thrown at you in bulk during this explanation — that will come later. The goal here was to first give an overall idea of what benchmarks are.

---

### How Model Evaluation Using A Benchmark Actually Works (Step By Step)

Scenario: imagine we are a frontier lab (like OpenAI, Anthropic, etc.) that trains its own LLMs. We have trained a new LLM and want to test it against a new, popular benchmark that has just been published.

- Simply put, model evaluation using a benchmark is basically a **loop**.
- Every question in the benchmark's dataset becomes one row in this loop.

**Example setup:**
- Our new LLM: "CampusX v1"
- The benchmark: GSM8K (tests mathematical capability)

**Step-by-step loop:**

1. **Load the item** — load the first question from the dataset.
2. **Build the prompt** — inject few-shot examples if required (e.g., inject 8 solved examples for GSM8K's 8-shot setup), apply the chat template, add instructions. Now you have the exact string you want to send to the model.
3. **Call the model with the pinned decoding config** — set temperature, set max tokens, and any stopping criteria to avoid problems. In code, this means calling something like `model.generate` (or `.invoke()` if using LangChain), sending the built prompt, and passing the fixed temperature and max token values.
4. **Capture the raw output** — pull whatever the model returned.
5. **Extract the answer** — for example, if the model said "The answer is 72," extract just "72" and store it as the prediction.
6. **Score** — check whether the answer is True or False (correct or incorrect), and store that score.
7. **Repeat** this process for every question in the dataset (e.g., 8,000 times), appending each result to a list.
8. Once the loop finishes, you have a large list of results — a 1 or 0 for every question.
9. **Aggregate** — take the mean of all these scores to get the final benchmark score for the model.

This is how evaluation is done using a benchmark, at least for the simpler ones. More complex benchmark examples will be discussed later.

---

### Why Evaluation Is Not As Simple As It Looks: Introducing "Eval Harness"

- Looking at this loop, it can seem like a very simple task — "I can build this loop myself easily."
- But the problem is that when you actually sit down and write the real code (not just pseudocode), you realize it is not that straightforward. For example:
  - You need extra code to correctly extract the answer (e.g., pulling "72" out of "The answer is 72").
  - You need to write the exact scoring mechanism as specified by the benchmark paper.
  - Since you are sending thousands of questions to the LLM, you need some **batching strategy**, which needs its own code.
  - If an API call fails midway, you need retry logic, which needs its own code.
  - If there are rate limits, you need to handle those too.
- So while the core task is "just run a loop," running a **reliable** loop at the scale of 8,000-10,000 LLM calls requires a lot more engineering around it.
- Because of this, people generally do not write all of this plumbing code themselves. Instead, they use existing **libraries**.
- The piece of code that handles all this additional plumbing — batching, retries, rate limits, extraction, scoring according to spec, etc. — is given a specific name: it is called an **eval harness**.
- **Eval harness:** a piece of code that you write (or use) in order to execute model evaluation.
- This work is usually not done from scratch — there are libraries built specifically to handle this.

**Popular libraries/frameworks for running evals:**
- **lm-evaluation-harness** — a very popular library (built by EleutherAI, a well-known company). It lets you test your LLM against any benchmark with minimal code, and it already has built-in support for a large number of benchmarks.
- **Inspect** — another well-known library.
- **DeepEval** — another library (discussed further below).

**Analogy:** Think of the benchmark as the exam paper, and the eval harness as the entire exam administration/organization that handles everything else on your behalf, so you don't have to do much yourself.

---

### Live Code Walkthrough: Running GSM8K Using lm-evaluation-harness

- Step 1: Install the library `lm-eval`.
- Since the model being tested is an OpenAI model, an OpenAI API key is required (used and then deleted for the demo).
- This library — `lm-evaluation-harness` — supports many providers, not just OpenAI; models from Hugging Face can also be pulled and tested. It supports a large number of benchmarks already.
- Command used for the demo (not really "code," just a command):
  - **Model arguments:** specifies which model to test/evaluate — here, targeting **GPT-5.6** (as an example of the model being tested at the time of the class).
  - **num_concurrent = 5** — how many concurrent questions can be handled at once.
  - **Max retries** were also set.
  - **Tasks:** set to GSM8K benchmark.
  - **cot (chain of thought):** enabled — chain of thought is allowed.
  - **num_fewshot = 8** — since this is 8-shot prompting.
  - **Apply chat template**
  - **Limit = 20** — this tells the harness to evaluate only 20 questions instead of all 8,000, just to test that the setup works correctly. In a real/proper evaluation, this line would not be included, and the full 8,000 questions would be evaluated.
  - Reasoning for limiting to 20: evaluating all 8,000 questions on GSM8K was estimated to cost around ₹2,300 for one full evaluation run, whereas 20 questions costs only around ₹3-4 or even less.
  - **Output path:** where the results get printed/saved.
  - **Log samples:** enabled, so that all results generated are logged.
- Running this single command starts the entire evaluation process — no loop had to be written manually, no extra code was needed. Everything was handled by this one command because of the abstraction provided by the eval harness. Without this harness, all of that plumbing code would have to be written manually.
- Behind the scenes, since 20 questions were being evaluated, 20 API calls were automatically made to the LLM.
- **Result:** around 90% score — meaning the model got 18 out of 20 questions correct.
- Full logging is available: a results folder is created, and inside it, a JSON object is generated per question — showing the doc ID (which question it was), what answer came back, and the full evaluation detail for every single question.
- If the "limit 20" line were removed, this would essentially become the real GPT-5.6 evaluation on GSM8K, and the resulting numbers could actually be published — this is essentially what OpenAI itself would do.

---

### DeepEval As An Alternative

- DeepEval also provides this option for running benchmarks — it has a documentation section listing "Available Benchmarks," and GSM8K is present there too.
- However, DeepEval requires writing a lot more code just to run something like an OpenAI model through it, compared to `lm-evaluation-harness`, where a single command handled everything with almost no code.
- That is why `lm-evaluation-harness` was used for the demo instead of DeepEval.
- **DeepEval is more suited to application-level evaluation.** It's useful if you want to try out your own small, fine-tuned LLMs against a benchmark, but it doesn't offer as many benchmark options — most of its available benchmarks are already saturated ones anyway.
- **lm-evaluation-harness is considered the more "premium"/industry-standard option** — even big companies use this library to run their benchmarks.

---

### Who Actually Performs Benchmarking? (Three Stakeholders)

Since most benchmarks are open and publicly available on the internet, a valid question arises: who actually bothers to run these evaluations? There are primarily three categories of people/organizations who do model evaluation/benchmarking:

#### 1. Frontier Labs Themselves

- Companies like OpenAI, Anthropic, Google DeepMind, etc. will obviously do evaluation and benchmarking for their own models, because it helps them during the model's development process. The benchmark results tell them whether the next model they are training is actually improving over the previous version.
- What they do: during the pre-training stage, at different checkpoints, they pull out intermediate versions of the model and run these benchmarks. This gives them a fair idea, during pre-training itself, of whether training is heading in the right direction — and they can even change the training trajectory mid-way if needed. This is extremely helpful for them.
- **Release gating:** benchmarks help decide whether a new version of a model is actually better than the previous one, and whether it should be released at all.
- **Marketing:** if a new model scores very well on a particular benchmark for a particular capability, this becomes great marketing material for them — a very effective marketing channel. You've probably heard things like "this new model has completely crushed the coding benchmarks," and then every YouTuber starts covering it. This drives a lot of marketing value.

**Important caution for AI engineers:** If you're an AI engineer selecting which model to use in your application, **do not blindly rely on benchmark numbers given by frontier labs.** If a lab shows you a benchmark number, you should ask: who ran this evaluation? If they say "we ran it ourselves, under our own controlled settings," you should not trust it too much.

- This is similar to how a car's advertised mileage is 25, but when you actually drive it, you get 5-10. The same thing applies here — lab-published numbers are basically a **ceiling**, i.e., the upper limit, because they run benchmarks under the most favorable conditions possible for their own model, and on top of that, they often do **cherry-picking**: showing off benchmarks where their model scores well, and quietly hiding/downplaying ones where it doesn't. This makes the model look very impressive on paper, but real-world usage often turns out less impressive.
- This has happened to many people — even referencing personal experience with "Fable": the actual real-world experience did not match the amount of hype around it. It was expected to be extremely powerful (people even joked it was "banned by the government" because it was supposedly that strong), but the personal experience did not live up to expectations — some people even claimed that behind the scenes it sometimes routes queries to Opus. So you have to be cautious here.

#### 2. Third-Party Evaluators

- There are independent leaderboards and companies (such as **LM Arena**) whose entire job is to benchmark different LLMs against each other and publish a ranking/leaderboard.
- These organizations have been doing this for a long time, so people have started trusting them — because whenever they test two different models (say, a Claude model and an OpenAI model), they test them under the exact same conditions, making their ranking more reliable.
- These are **independent organizations** whose product is literally evaluation — that's how they earn money.
- Their numbers are considered the most reliable and trustworthy way to read model performance comparisons.
- For example, LM Arena's leaderboard is reliable because it's run by a third party, and they even document exactly how the leaderboard is built and maintained.
- These third-party evaluators also provide extra useful information that labs often don't share — such as **cost and latency** of using these models. Many leading labs will just show you a benchmark number, without telling you how long it takes or how much it costs to use the model. Third-party evaluators fill this gap.

#### 3. AI Engineering Teams (You)

- The third category is AI engineering teams who are building LLM-based applications.
- Instead of relying purely on frontier labs or third-party evaluators, they often say: "We already have the tools — publicly available benchmarks, and libraries like lm-evaluation-harness — let's just run our own evaluation to see how the model performs on a particular benchmark under our own conditions, including latency and cost."
- So teams/companies also run their own evaluations at their own level.

**Summary:** there are three stakeholders who perform (or can perform) these evaluations — frontier labs, third-party evaluators, and companies/AI engineers themselves.

**Note on leaderboards:** These leaderboards are like an "IMDb ranking" for models — that's a good way to think about them. Leaderboards will be covered in more detail in the next session (they are essentially an aggregation of multiple benchmarks). Leaderboards are not being covered in this particular class.

---

### Problems With Benchmarks: Why You Should Not Blindly Trust Them

Everything discussed so far establishes that benchmarks are superb and help understand a particular capability of an LLM. But benchmarks are not flawless or perfect, and you should not always believe the information they give at face value. In many scenarios, benchmarks can be misleading, so you cannot blindly trust them — you have to be very, very careful whenever reading benchmark results. There are three to four types of problems with benchmarks:

#### 1. Benchmark Contamination

- Most benchmarks — MMLU, GSM8K, and many others to be discussed later — are mostly **public benchmarks**. Being public means their research paper, full methodology, and dataset are all publicly available on the internet.
- Especially benchmarks that came out a long time ago (2021, 2022, 2023) have had their datasets available on the internet for a long time.
- Imagine: OpenAI recently trained GPT-5.6 a few months ago. For training, they scraped the most recent internet data available at that time for pre-training.
- There's a good chance that when scraping the entire internet a few months ago, the public benchmark's dataset — its questions and correct answers — also became part of that model's pre-training data.
- If the model has already seen all 8,000 questions and their answers, then in the future, when you ask it to answer one of those questions, there's no guarantee whether it's actually reasoning through the answer or simply recalling it from memory (memorization).
- This is why, for many large models trained on very large datasets, these benchmarks can become **contaminated** — because the model already "knows" the answers, since they became part of its training data.
- This is a big problem, especially with public benchmarks.
- **Common solutions:**
  - Use **private benchmarks** (many exist; will be discussed in the next class).
  - Use **dynamic benchmarks** — unlike static benchmarks, where the same dataset published in research 5 years ago remains unchanged, dynamic benchmarks have datasets that get updated on a daily basis or within some particular window. These kinds of datasets/benchmarks can be used instead.
- Benchmark contamination is a serious, real issue.

#### 2. Benchmark Saturation

- Benchmark saturation is a process where a benchmark is introduced (say, in 2021) — at that point it's new, and no model has any prior exposure to it. Models initially perform poorly on it (25%, 36% scores, all models hovering around that range).
- Over time, the benchmark itself stays static — nothing changes in it — but models keep improving every six months or so, and their performance on those questions improves over time.
- So you'll notice that newer models gradually perform better and better on the same benchmark. What was 36% for one generation becomes 50%, then 70%.
- Eventually, models start hovering around 90-95%, and all models cluster together in the same range — meaning there isn't much difference in their scores anymore. For example: newest model at 95%, GPT-5.6 at 94%, Google Gemini at 92% — heavy clustering in one place.
- This is called **benchmark saturation**.
- This means the benchmark is no longer useful — it can no longer differentiate between models. If everyone scores about the same, it's like an exam that has become too easy — you can no longer tell who's genuinely better and who isn't.
- In that case, the benchmark is considered saturated, gets retired/removed, and a new benchmark is introduced. The industry then starts working with that new benchmark instead.
- GSM8K (the example used throughout this class) is itself a **saturated benchmark** — it's not really used anymore, since nearly everyone scores 94-97% on it. MMLU is also considered saturated. SWE-bench has also saturated.
- So benchmarks generally follow a lifecycle: introduced → initially very hard for all models → models gradually improve on it → benchmark saturates → gets retired → gets replaced by a new benchmark. That is how the benchmarking process works over time.

#### 3. Configuration Gaming

- Configuration gaming refers to a situation where frontier AI labs, while running their own benchmarking, tamper with the run configuration — giving their own model the most favorable possible conditions, while giving rival/competitor models default/less favorable conditions.
- For example: while benchmarking on GSM8K, a lab might give their own model access to a Python interpreter tool. The model then writes code to solve all the mathematical questions programmatically, which obviously improves its score.
- Configuration can be tampered with in many ways, and this can cause huge variation — swings of 5-10% in scores.
- You should be cautious about this, especially when a frontier lab claims their model "crushed" a benchmark — that claim should never be taken at face value, because you have no idea how they actually tested the model internally. It's their own eval harness — what changes did they make? Did they set unlimited max tokens? What level of reasoning setting did they use? What temperature value did they use? You have no idea. What is the latency? What is the cost? None of that is disclosed — they just give you a single number like "92% on this benchmark," and that alone is not trustworthy.

#### 4. Aggregation Gaming

- This happens in the last step of benchmarking — aggregation — where individual question scores are combined into one overall number. Many people/organizations play smart here.
- For example: MMLU has 57 subjects. A model might score very well in Physics but very poorly in Economics.
- Instead of giving you the individual, subject-wise scores, the model provider might just give you the overall average score, without telling you that the model performs poorly specifically in Economics.
- If you were building an economics-focused chatbot, you might look at the overall MMLU score, see that it looks good across 57 subjects, and deploy the model — only to later discover that it performs very poorly specifically on economics-related questions, because its economics-specific score was actually quite bad, but that fact was hidden inside the aggregate number.
- So because benchmarks can hide information like this within aggregation, you might not realize it until it's too late.

---

### Closing Note

These are the four major reasons why benchmark numbers should be taken with a pinch of salt — you should not blindly accept whatever number is thrown at you. You need to implement your own evaluation methodology, and based on that, decide for yourself which model works for your use case and which doesn't. This will be discussed further in upcoming sessions, including how to handle this more practically. This is roughly everything that was meant to be covered in today's class — some remaining topics will be covered in the next session.