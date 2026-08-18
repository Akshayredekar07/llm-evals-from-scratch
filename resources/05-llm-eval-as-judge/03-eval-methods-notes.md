### **LLM Eval Methods - Revision Notes**

### **Definition**
- An LLM eval method is the mechanism used to decide whether an LLM's output is good or not.
- It is the actual procedure that takes an output and produces a judgment about it.
- Every eval pipeline you build runs through one of three methods - who actually executes the judgment.

### **Three Types of Eval Methods**
1. Programmatic / deterministic - a program produces the verdict.
2. Human - a person produces the verdict.
3. Model graded (LLM-as-judge) - a model/LLM produces the verdict.

### **Zomato Recap Example**
- Email classifier task (billing / technical / general).
- Accuracy was calculated using Python code.
- Eval method used there: programmatic.

---

### **1. Programmatic (Deterministic) Evaluation**

### **How it works**
- Code checks the output against a rule or a known correct answer.
- Techniques: exact match, regex, JSON schema validation, executing code/SQL and comparing results.
- Fast, cheap, reproducible.
- Only works where correctness is mechanically checkable.

### **Example - Evaluating a RAG Retriever (Campus X chatbot)**
- Component being evaluated: the retriever only, not the full RAG pipeline.
- Retriever's job: pull the most relevant documents from the vector database for a given question.

**Step 1 - Define task and target**
- Task: check if the retriever works correctly.
- Target: a single component, the retriever.

**Step 2 - Define success criteria**
- Metric: Recall@K.
- Definition: out of all correct/relevant items that exist, how many did the system retrieve in its top K results.
- Formula: Recall@K = (number of relevant items retrieved in top K) / (total number of relevant items).
- Worked example:
  - Question: "What are the prerequisites for the ML course and how long is it?"
  - Correct/gold docs: 1001, 1003.
  - Retriever fetched top k=5: 1001, 102, 104, 105, 106.
  - Found: only 1001.
  - Recall = 1/2 = 0.5 (50%).
- Ideal recall = 100% (1.0), minimum = 0%.
- Other related metrics that exist but weren't the focus here: precision, rank.

**Step 3 - Build a dataset**
- Sampled 50-100 likely user questions, covering edge cases, easy, difficult, random questions.
- A human expert manually searched the vector database and identified the correct gold document IDs per question.
- This labeled set = the golden dataset.

**Step 4 - Define evaluation method**
- Programmatic: send all questions to the retriever only (k=5), collect retrieved docs.
- Calculate recall per question, then average across the dataset to get overall Recall@K.

**Result and improvement**
- Example overall result: 67% recall.
- Study low-recall questions, then improve the retriever:
  - Improve the embedding model (may not capture semantic meaning well).
  - Query expansion - expand the user's question via an LLM before sending to retriever.
  - Increase k (e.g. 5 -> 10).
  - Add a re-ranker to push correct docs higher in ranking.

**Why no human needed here**
- Program can objectively check retrieval against the labeled gold docs.
- No need to pay for human evaluation when a program can do the job.

**Note on "relevance" - multiple aspects possible**
1. Out of correct documents, how many were fetched (the aspect covered here).
2. How many fetched documents were NOT useful.
3. Whether retrieved documents were properly ranked.
- Creating the golden dataset is a separate human activity from running the eval itself; the eval here is still programmatic because the execution/scoring is done by code.

---

### **2. Human Evaluation**

### **Example - Chatbot Helpfulness (Campus X general chatbot)**
- General-purpose chatbot answering any course-related question.
- Evaluating "application quality" - specifically helpfulness of answers.

**Step 1 - Task and target**
- Target: entire application (not a single component).
- Task: evaluate helpfulness.
- Helpfulness = accurate + correct tone + complete answer.

**Step 2 - Success criteria**
- No single correct metric exists (varies business to business).
- Defined a rubric, helpfulness scale 1 to 5:
  - 5 = fully answers the question, accurate and complete, appropriate tone.
  - 3 = partially helpful, missing something or slightly off.
  - 1 = unhelpful, wrong, or irrelevant.

**Step 3 - Build a dataset**
- 50-100 sample questions covering normal, difficult, edge case, random questions.
- Dataset has only ONE column: the question (no reference/correct answer given).
- Example questions:
  - "How long is the ML course?"
  - "Is the ML course right for me if I already know Python?"
  - "What's the fee for the DL course?"
  - "Do I get a refund if I drop out midway?"
  - "Can I pay the fee in installments?"

**Step 4 - Define evaluation method**
- Helpfulness is too nuanced to measure programmatically -> method = human.
- Process:
  - Run each question through the chatbot to get an answer.
  - Human reads question + answer, assigns a score based on the rubric.
  - Repeat for the whole dataset, then average scores = helpfulness score.

**Why use multiple human graders (Grader A, Grader B)**
- If two graders disagree a lot on the same questions, it signals ambiguity in the rubric.
- High agreement between graders = clear rubric/instructions.
- Sometimes multiple graders are used specifically to refine and clarify the rubric.

### **Five Types of Human Evaluation**
1. Direct grading and rating - reading an answer and scoring it against a rubric (what was covered above).
2. Red teaming - humans deliberately attack the system to find where it breaks (jailbreaks, adversarial inputs); findings sent back to the dev team.
3. A/B testing - two versions run in production, real users rate their experience, better-rated version gets deployed widely.
4. Golden dataset creation - humans define correct answers/gold labels/rubrics used in other eval methods.
5. Human in the loop (HITL) - humans step in for complex/ambiguous/high-stakes cases that programmatic or LLM checks can't confidently handle.

### **Advantages and Disadvantages of Human Evaluation**
- Advantage: judgment is reliable, human brain easily handles nuance/ambiguity, high trust in the system.
- Disadvantage: cost - paying people is expensive, doesn't scale to lakhs/crores of users.

---

### **3. LLM as a Judge (Model-Graded Evaluation)**

### **When to use it**
- Used when programmatic checks can't work (task is too ambiguous/subjective).
- Used when human evaluation is too costly to scale.
- Sits between programmatic and human - has strengths of both.
- Method type: model graded / LLM graded.
- Technique name: LLM as a Judge.
- Most commonly used method in real-world LLM eval pipelines.

### **Example - UPSC Mains Answer Evaluation Platform**
- Context: UPSC exam has 3 stages - Prelims (MCQ, easy to auto-grade), Mains (subjective, hard to auto-grade), Interview.
- Platform "Campus X UPSC" prepares students for Prelims and Mains.
- Problem: evaluating subjective Mains answers for thousands of students needs many paid subject matter experts (SMEs) - not scalable/profitable.
- Solution: an LLM-based platform that grades subjective answers based on defined rubrics, at a fraction of the cost.

**Step 1 - Task and target**
- Target: the built platform.
- Task: check whether it evaluates papers correctly, like a human expert would.

**Step 2 - Success criteria**
- Success = platform evaluates UPSC answers exactly the way human experts do.
- (Exact metric decided in a later step.)

**Step 3 - Build a dataset**
- Example paper with 3 questions used (15, 10, 15 marks).
- A rubric was defined per question by an expert - checkpoints/dimensions to look for.
  - Example for Q1 ("Ethical governance is impossible without administrative accountability. Discuss."):
    1. Defines ethical governance and accountability
    2. Explains the link between them
    3. Gives mechanisms (RTI, social audit, CVC)
    4. Cites examples/case
    5. Balanced conclusion
- Rubric is NOT the dataset - it's the standard used to grade answers.
- Dataset structure: answer ID, question ID, the actual student answer text, human evaluator's marks per dimension and total.
- Golden dataset size: ~50-100 answers, graded by one human subject matter expert.

**Step 4 - Define evaluation method**
- Not programmatic (too subjective/complex to code directly).
- Too costly to use humans at scale.
- Method = LLM.

**Running the evaluation**
- Prompt given to LLM: act as a grader evaluating a UPSC Mains answer against a rubric.
- Inputs given: the question, max marks, the rubric, and the student's answer.
- Instructions: check each rubric dimension, allocate marks accordingly, don't reward verbosity/keyword stuffing/unsubstantiated claims, reward structure/examples/balanced argument, and give a one-line justification.
- Every answer is graded by the LLM and compared side by side against the human's marks for the same answer (same rubric used by both).

### **Metric: MAE (Mean Absolute Error)**
- Goal: check if LLM's marks are close to the human's marks.
- Calculation: take absolute difference between LLM marks and human marks per answer, average across all answers.
- Example result: MAE = 2.3 (LLM deviates from human by about ±2.3 marks on average).
- Goal: bring MAE toward 0 - meaning the LLM grades exactly like the human.
- Ways to reduce MAE:
  - Use a better LLM.
  - Change the system prompt.
  - Change/refine the rubric.
- Same iterate-and-improve loop as before applies here too.

---

### **Reference-Based vs Reference-Free Evaluation**

### **Reference-Based Evaluation**
- A correct/reference answer is written down in advance for each test case.
- Output is graded by comparing it against that known reference.
- Examples from this lecture:
  - Retriever eval - gold document IDs known beforehand (e.g. doc 1001, 1003 marked correct in advance).
  - UPSC LLM-as-judge eval - human's marks act as the "correct answer" the LLM should match.

### **Reference-Free Evaluation**
- No predefined correct answer exists in the dataset.
- Output quality is judged directly against a criteria/rubric (a scale/standard, not a per-item correct answer).
- Example from this lecture:
  - Chatbot helpfulness eval - dataset only had questions, no correct answers; human judged using the 1-5 rubric and their own judgment.

### **How to classify quickly**
- Ask: is a correct answer given in the golden dataset or not?
- Given -> reference-based.
- Not given -> reference-free.

---

### **What's Next**
- Upcoming topic: Offline vs Online evaluation.
- Everything covered in this lecture (programmatic, human, LLM-as-judge examples) falls under offline evaluation.
- Online evaluation = evaluation that continues after the system goes live in production.

---

### **Quick Summary Table**

| Method | Who judges | Best for | Cost/Speed | Reference type used here |
|---|---|---|---|---|
| Programmatic | Code | Mechanically checkable correctness (e.g. retriever Recall@K) | Fast, cheap, reproducible | Reference-based |
| Human | Person | Nuanced/subjective/high-stakes judgment (e.g. chatbot helpfulness) | Slow, expensive, most reliable | Reference-free |
| LLM as judge | Model | Subjective tasks at scale (e.g. UPSC answer grading) | Middle ground, scalable | Reference-based |