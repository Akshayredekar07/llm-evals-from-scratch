# **RAG Generator Evaluation**

## **1. Where This Fits in the RAG Eval Suite**

A RAG eval suite is built at three levels:

1. **Component level** — evaluate the Retriever and the Generator separately
2. **Pipeline level** — evaluate the Retriever + Generator connected together (RAG Triad)
3. **Application level** — correctness, completeness, style, safety, ops (covered in a later session)

**Status so far:**

- Retriever (component level): Recall and Precision — done in a previous session
- Generator (component level): Faithfulness and Answer Relevancy — covered in this session
- Pipeline level: Faithfulness, Answer Relevancy, Contextual Relevancy (the **RAG Triad**) — covered in this session

## **2. The Generator Component**

**Definition:** The generator is a function that takes two inputs and produces one output.

- Input 1: the user's question
- Input 2: the retrieved context (chunks from the retriever)
- Output: the generated answer

**Implementation details:**

- Model used: GPT-4o mini (cheap, good enough for this task)
- Temperature: set to 0 (standard practice during evaluation)
- System prompt rules (first version):
  - Use only information present in the context
  - Do not add outside knowledge
  - If context is insufficient, say so explicitly instead of hallucinating
  - Keep the answer clear and concise
- Built as a simple LangChain chain: `prompt -> LLM -> StringOutputParser`
- Exposed as a `generate(query, context)` function

**Note:** Building the generator alone only proves the code runs without errors. It does not prove the generator is producing *good* answers. Quality must be measured through evaluation.

## **3. Generator Failure Modes**

There are two major ways a generator can fail.

### **3.1 Unfaithful Response**

The generator adds information that is not present in the given context (hallucination), even though the instruction was to answer strictly from the context.

**Example:**

- Question: "Does the AI Engineering program include live classes?"
- Context given: mentions only recorded lessons, coding assignments, projects, weekly doubt-solving sessions (no mention of live classes)
- Generated answer: "Yes, the program includes two live classes every week..."
- This is **unfaithful** — the LLM invented information not present in context

**Real-world danger example:** The Air Canada chatbot case, where the bot promised a refund policy that was not actually part of the airline's real policy. That was a generator failure (ignoring context, inventing an answer).

**Important distinction:** Faithful does **not** mean correct.

- If the retriever brings the *wrong* context, a faithful generator will still build its answer entirely from that wrong context.
- Faithfulness only checks: "Is the answer derived strictly from the given context, without adding outside information?"
- It does not check whether the context itself was correct.

**Metric name: Faithfulness**

### **3.2 Irrelevant Answer**

The generator's answer is built entirely from the context (so it is faithful), but the answer does not actually address the question asked.

**Example:**

- Question: "Does the program include live classes?"
- Context: mentions recorded lessons, coding assignments, projects, weekly doubt-solving sessions
- Generated answer: "The program includes coding assignments, projects, recorded lessons and weekly doubt-solving sessions."
- This answer is **faithful** (fully derived from context) but **not relevant** — it does not tell the user whether live classes exist or not
- An ideal relevant answer: "The provided context does not confirm that the program includes live classes. It only mentions recorded lessons, coding assignments, projects and weekly doubt-solving sessions."

**Metric name: Answer Relevance**

**Other generator-level metrics that exist but are evaluated later at the application level:** citation accuracy, completeness, correctness.

## 4. How Faithfulness Is Calculated

**Requires:** a golden dataset (question and golden context pairs).

**Golden dataset structure:**

| Column | Content |
|---|---|
| Question | A sample question |
| Golden Context | Manually curated, verified-correct chunks relevant to that question |

**Step-by-step process:**

1. Take a question and its golden context from the dataset
2. Send both to the generator (in isolation — **the retriever is not involved at this stage**)
3. Generator produces an answer
4. An LLM-as-a-judge breaks the generated answer into individual **claims**
5. For each claim, the judge checks: does this claim exist in the golden context? (yes/no)
6. Faithfulness score for that question = (number of claims found in golden context) / (total number of claims)
7. Repeat for every question in the dataset, then average across all questions = final Faithfulness score

**Worked example:**

- Answer broken into 3 claims
- Claim 1 exists in golden context: yes
- Claim 2 exists in golden context: yes
- Claim 3 exists in golden context: no
- Faithfulness for this question = $2/3 \approx 0.67$

**Key point:** This is the opposite direction of Recall.

- Recall: compares retrieved *context* against an ideal answer
- Faithfulness: compares generated *answer* against the ideal/golden context

## 5. How Answer Relevance Is Calculated

**Type:** Reference-free evaluation — no golden context is used as a ground truth reference. A golden dataset is only used as a convenient source of questions to generate answers for.

**Step-by-step process:**

1. Send question + context to the generator, get an answer
2. LLM-as-a-judge breaks the answer into claims
3. For each claim, ask: does this claim help answer the question? (yes/no)
4. Answer Relevance score = (number of relevant claims) / (total number of claims)
5. Average across all questions in the dataset

**Worked example:**

- Answer broken into 3 claims about benchmark saturation and contamination
- Claim 1 (saturation definition): relevant
- Claim 2 (can't differentiate good models): relevant
- Claim 3 (benchmark contamination, off-topic for this question): not relevant
- Answer Relevance = $2/3 \approx 0.67$

## **6. Common Q&A Clarifications on Faithfulness / Answer Relevance**

- **Same LLM for claim-breakdown and claim-checking?** Yes, using the same LLM for both steps is fine. Each LLM call is independent; there's no shared context between the two steps that would make using different models necessary.
- **Can LLM-as-a-judge make mistakes (false positives/negatives)?** Yes, this is a known limitation. Mitigation: use the same (best available, most powerful) judge model consistently across runs, so any bias is at least applied uniformly, and evaluation runs remain comparable across iterations.
- **Number of claims is not a hyperparameter** — it is not something you fix in advance; it naturally depends on how the answer is written.
- **If a generator misses a good claim or includes an irrelevant one, the metric score should reflect that** — this is the entire point of the evaluation.
- **This is entirely different from Precision/Recall** (which apply to the retriever). Faithfulness and Answer Relevance are generator-focused and work in the opposite comparison direction.
- **Faithfulness ≠ Correctness** and **Answer Relevance ≠ Correctness**. Correctness is a separate metric, covered in a later (application-level) session.

## **7. Building the Golden Dataset**

**Method used in this session:**

1. Export the entire vector database's chunks into a single JSON file (862 chunks in this case)
2. Feed the JSON file to an LLM (Claude) and ask it to generate question + golden-context pairs **one at a time** (step by step, not all at once)
3. Manually review and verify each generated pair before adding it to the dataset
4. Repeat until a dataset of the desired size is built (15 questions in this case)

**Other possible methods:**

- Fully manual creation
- LLM-assisted with human review (used here)
- DeepEval's synthesizer tool (mentioned as a future topic, not yet reliably used by the instructor)

**Final dataset:** `faithfulness_dataset.json` with 15 question/golden-context pairs, stored in the project's `golds` folder.

## 8. Implementing Generator Evaluation in DeepEval

**File:** `evals/eval_generator.py`

**Test case field mapping:**

| DeepEval field | Source |
|---|---|
| Input | Question from golden dataset |
| Actual output | Answer from `generate()` function (the generator) |
| Retrieval context | Golden context from golden dataset (not from the real retriever) |

**Metrics used:** DeepEval's built-in `FaithfulnessMetric` and `AnswerRelevancyMetric`, both configured with:

- Judge model (GPT-4o mini)
- A threshold value (pass/fail cutoff)
- `include_reason=True` (to get explanations for failures)

**Execution:** Run as a module: `python3 -m evals.eval_generator`. DeepEval runs all test cases **in parallel**, which is why evaluation is fast even with many test cases.

### Results — First Run (Baseline Prompt)

| Metric | Score |
|---|---|
| Faithfulness | ~91% |
| Answer Relevancy | ~73% |

**Why Faithfulness is naturally high even without tuning:** Modern LLMs have strong instruction-following ability. When explicitly told "answer only from this context," there is already a high probability the answer will be derived from it. Faithfulness is comparatively easy to score well on.

**Why Answer Relevancy was lower:** It requires the answer to actually address the question, which is a harder bar than just staying grounded in the context.

## 9. Improving the Generator

Only two real levers exist to improve a generator (unlike the retriever, which has chunk size, embedding model, reranker, etc.):

1. **Switch to a more powerful / better instruction-following model**
2. **Improve the system prompt** — this has a large impact

**Prompt refinement process used:**

- Ran the evaluation multiple times
- Analyzed each failed test case and its stated reason
- Fed the failure patterns into an LLM to help refine the prompt
- Repeated over 3 to 4 iterations

**Rules added to the refined prompt (on top of the original ones):**

- Do not strengthen or overstate claims
- If the context distinguishes between two different things, do not merge/upgrade them into one
- Treat the context as an informal lecture transcript — synthesize and rephrase rather than copy
- Do not require the question's exact wording to appear in the context

### **Results — After Prompt Refinement**

| Metric | Score |
|---|---|
| Faithfulness | ~96% |
| Answer Relevancy | ~92% |

**Caution — overfitting risk:** Tuning the prompt too specifically to the golden dataset could make it look great on this test data but not generalize once real (retriever-sourced) context is used. This gets checked later at the pipeline level.

## 10. Experiment Tracking with Confident AI

- `deepeval view` command logs an entire evaluation run to Confident AI (DeepEval's parent company platform)
- Requires login and an API key (created per project)
- Each run stores: pass/fail counts, per-test-case detail and reasoning, and can also store configuration values (system prompt used, chunk size, etc.)
- This is essentially experiment tracking, conceptually similar to MLflow
- Classified as more of an **LLM Ops** concern than a core "hardcore evals" topic

## **11. Building the RAG Pipeline**

Once the retriever and generator are each individually working, they get connected into a single pipeline.

**Structure (`RAGPipeline` class in `src/rag_pipeline.py`):**

1. Take a user question
2. Pass it to the retriever (reranking retriever) → get back context chunks
3. Convert retrieved chunks into a single string
4. Pass the question + context string to the generator → get the answer
5. Return the answer

This is essentially glue code connecting the two already-built components.

**Verification:** Running a sample question ("What is drift and why does it matter after deployment?") through the pipeline produced a coherent answer sourced from real retrieved chunks, confirming the pipeline runs end-to-end without errors.

## 12. Evaluating the Pipeline: The RAG Triad

Standard way to evaluate a full RAG pipeline. Based on the relationship between three elements: **Question**, **Context**, **Answer**.

| Relationship | Metric |
|---|---|
| Answer vs Context | Faithfulness |
| Answer vs Question | Answer Relevancy |
| Context vs Question | Contextual Relevancy |

Together these three metrics are called the **RAG Triad**.

### **Key Difference from Component-Level Evaluation**

At the component level, the generator was tested **in isolation**, using the golden context supplied directly from the dataset.

At the pipeline level, the context now comes from the **real retriever**, not from the golden dataset.

- Same metric names (Faithfulness, Answer Relevancy)
- Same calculation method
- Different context source, so scores can differ from the component-level run

## **13. How Contextual Relevancy Is Calculated**

**Definition:** How relevant the context that the retriever pulled is, with respect to answering the question.

**Type:** Reference-free (needs a golden dataset only as a source of questions, not as a reference for correctness).

**Step-by-step process:**

1. Send a question to the retriever only (no golden context needed)
2. Retriever returns K contexts (for example, K = 5)
3. LLM-as-a-judge breaks each of the K contexts into individual claims (say 15 claims total across all 5 contexts)
4. For each claim, ask: is this claim related/relevant to the question? (yes/no)
5. Contextual Relevancy score = (number of relevant claims) / (total number of claims)
6. Repeat across all questions in the dataset and average

**Worked example:** Out of 15 total claims extracted from the 5 retrieved contexts, 10 are found relevant to the question → Contextual Relevancy = $10/15$.

## 14. Implementing the Full RAG Triad in DeepEval

**File:** `evals/eval_rag_pipeline.py`

**Test case field mapping (note the change from the generator-only eval):**

| DeepEval field | Source |
|---|---|
| Input | Question from golden dataset |
| Actual output | Answer from the **RAG pipeline** (not the isolated generator) |
| Retrieval context | Context from the **RAG pipeline's retriever** (not the golden dataset) |

All three metrics (Faithfulness, Answer Relevancy, Contextual Relevancy) are defined and passed into DeepEval's `evaluate()` function together.

### **Results — Full Pipeline Evaluation**

| Metric | Score |
|---|---|
| Faithfulness | ~92–93% |
| Answer Relevancy | ~86% |
| Contextual Relevancy | ~42–43% |

**Positive takeaway:** Answer Relevancy stayed high even after switching from golden context to real retriever context, confirming the tuned system prompt generalizes well and was not overfit to the test dataset.

**Problem area:** Contextual Relevancy is low.

## 15. The Retriever Paradox: Good Recall/Precision but Low Contextual Relevancy

**The puzzle:** The same retriever, evaluated independently, showed:

| Metric | Score |
|---|---|
| Recall | ~99% |
| Precision | ~89% |

But Contextual Relevancy (measured inside the pipeline) was only ~42%. How can a retriever be simultaneously "good" and "bad"?

**Definitions recap:**

- **Recall:** out of all the correct contexts that exist, how many did the retriever manage to fetch
- **Precision:** out of all the contexts fetched, how many are useful/helpful overall (evaluated at the whole-chunk level)
- **Contextual Relevancy:** out of the individual claims/sentences inside the fetched contexts, how many are actually relevant to the question

**The explanation — noise within a chunk:**

- Precision treats a whole chunk as "useful" even if only a small part of it is relevant. If even one sentence in a 5-sentence chunk is useful, that chunk still counts positively toward precision.
- Contextual Relevancy breaks each chunk down into individual claims and checks each one separately.
- If a chunk has 5 claims and only 1 or 2 are actually relevant to the question, Precision still marks the whole chunk as "useful," but Contextual Relevancy will correctly score it low (for example $2/5$).

**Worked illustration:**

- 5 retrieved chunks (K = 5), 4 of them contain at least some relevant information → Precision looks high
- But within each of those 4 chunks, only a fraction of the sentences are actually useful (the rest is unrelated "noise")
- When broken into claims, the ratio of useful claims to total claims is much lower → Contextual Relevancy comes out low

**Conclusion:** Precision measures relevance at the *chunk* level; Contextual Relevancy measures relevance at the *claim/sentence* level inside each chunk. A retriever can score well on chunk-level metrics while still returning noisy, bloated chunks.

**Fix / lever to pull:** Reduce **chunk size** (and possibly overlap). Smaller, more focused chunks are more likely to be fully relevant, which should raise Contextual Relevancy.

**Trade-off warning:** Reducing chunk size to raise Contextual Relevancy could potentially reduce other scores (Recall, Precision, Faithfulness, Answer Relevancy) — this needs to be tested experimentally, not assumed.

**Practical takeaway:** If Faithfulness, Answer Relevancy, Recall, and Precision are all strong, a comparatively lower Contextual Relevancy score is not necessarily a blocker — final answer quality can still be good. It is an area for potential improvement, not automatically a failure.

## **16. Summary Table — All Metrics Covered So Far**

| Metric | Level | Compares | Reference-free? |
|---|---|---|---|
| Recall | Component (Retriever) | Retrieved context vs ideal answer | No (needs golden context) |
| Precision | Component (Retriever) | Retrieved context vs usefulness | No (needs golden context) |
| Faithfulness | Component (Generator) / Pipeline | Answer vs context | No (needs golden/real context) |
| Answer Relevancy | Component (Generator) / Pipeline | Answer vs question | Yes |
| Contextual Relevancy | Pipeline | Context vs question | Yes |

These five metrics together make up DeepEval's standard RAG metric set (visible under the RAG category in DeepEval's documentation).

## **17. Additional Notes from Q&A**

- LLM applications that are **not** RAG or agentic (for example, an "interview synthesizer" type app) can still be evaluated. DeepEval supports metrics for multi-turn/chatbot use cases, and fully custom metrics can also be built (using a concept called **G-Eval**, covered in a later session).
- Fully open-source model evaluation is possible but comes with practical friction: rate limiting on parallel LLM calls (varies by model/provider), and more "glue code" is needed to wire up open-source models with DeepEval.
- The four core RAG metrics (Recall, Precision, Faithfulness, Answer Relevancy) are considered standard for essentially any RAG application. Contextual Relevancy completes the five-metric standard set. Beyond these, correctness, completeness, and style are custom/application-level metrics.

## **18. What Comes Next**

Remaining parts of the eval suite, planned for future sessions:

- **Application-level evaluation:**
  - Correctness of answers
  - Completeness of answers
  - Style/tone matching (for example, matching a specific brand or course voice)
- **Safety evals**
- **Ops evals**
- **Regression testing**
- **Online evaluation** (evaluating on live production traffic after deployment)