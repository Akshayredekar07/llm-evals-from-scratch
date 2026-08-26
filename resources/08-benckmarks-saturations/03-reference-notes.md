### LLM Evals — Benchmarks: Revision Notes

**Course flow so far:** Why evals matter → What evals are (Standardized Benchmarks vs Custom Evals) → 8 Core Capabilities → **Benchmarks (this topic)**

---

### 1. What Is A Benchmark

- **Definition:** A benchmark is a **standardized test used to measure a particular model capability**.
- Every model release is followed by benchmark scores (SWE-bench, ARC-AGI, MMLU, etc.) — this is the most talked-about term in LLM evaluation.
- Every benchmark is built from **four parts**:
  1. Dataset / Task
  2. Run Configuration
  3. Scoring Method
  4. Aggregation Method

---

### 2. Running Example — GSM8K

- **GSM** = Grade School Mathematics
- **8K** = ~8,000 rows in the dataset
- Old benchmark (2020-21 era), now considered **saturated** (see Section 6)
- Used throughout as the reference example to explain all four parts of a benchmark

---

### 3. Part 1 — Dataset / Task

- **Dataset = Questions + Answer key** ("golden dataset")
- **Task** = what the model is asked to do with each item (e.g., solve a grade-school math word problem)

**Sample GSM8K item:**
> "Natalia sold clips to 48 friends in April, and then she sold half as many clips in May. How many clips did she sell altogether?"
> **Answer:** 72 (48 in April + 24 in May)

- Every benchmark has its own dataset (MMLU, SWE-bench, etc.) — always question + answer pairs.
- GSM8K dataset is publicly available (Hugging Face, Kaggle) — ~8,500 Q&A rows.

---

### 4. Part 2 — Run Configuration

> Definition: the complete list of settings under which the model is run during evaluation. Both models being compared **must** use identical settings — otherwise the comparison is invalid.

Three layers:

#### 4a. Prompt Construction
- **Zero-shot vs Few-shot**
  - Zero-shot: question given with no worked examples
  - Few-shot: N solved examples shown before the actual question
  - GSM8K → classically **8-shot**
  - Few-shot reliably lifts scores — teaches the model the expected answer format
- **Chain-of-thought (CoT) vs Direct**
  - Direct: model blurts an answer immediately → more mistakes
  - CoT: model told to "think step by step" → walks through reasoning (48 → half is 24 → 48+24=72) → accuracy improves significantly
  - GSM8K → CoT allowed

#### 4b. Decoding / Sampling Configuration
- **Temperature**
  - `temperature = 0` (greedy) → deterministic, same output every run, most reproducible → used by most benchmarks
  - `temperature > 0` → sampling, creative/varying outputs, less reproducible
- **Max tokens**
  - Too low → CoT gets cut off mid-reasoning → model never emits final answer → scored 0 even though it was solving correctly (a **config failure**, not a capability failure, but looks identical in the score)
  - Too high → very capable models may over-reason
  - Same cap applied to every model under test

#### 4c. Scoring Strategy & Environment
- **Attempt strategy**
  - **pass@1** — one attempt, correct or incorrect (strict)
  - **pass@k** — k attempts; counted correct if *any* one succeeds (lenient)
  - **maj@k / majority@k** — k attempts; the most frequent (mode) answer is taken as final (self-consistency)
  - These give **very different numbers** on the same model (e.g., 92% maj@8 vs 85% pass@1) — if a report doesn't specify which was used, the number is not interpretable
- **Tool access**
  - Tools = web search, code interpreter, etc.
  - Toggling tools on/off can massively change scores on the same benchmark (e.g., Python interpreter solving math questions programmatically)
  - GSM8K → tools **not allowed**
  - SWE-bench → tools **required** (needs GitHub issue fetching)

---

### 5. Part 3 — Scoring Method

Two steps: **Extraction**, then **Comparison**.

#### 5a. Extraction
- The model rarely outputs just "72" — it might say "The answer is 72," "72 clips," "$72," "seventy-two," etc.
- Extraction pulls the actual answer out of this free text.
- Methods: **regex** (e.g., "take the last number," parse after `####`) or **enforced structured output**.
- This step is fragile and often under-discussed: a brittle extractor can score a genuinely correct model as wrong.

#### 5b. Comparison
- **Closed-ended answers** (e.g., GSM8K's "72"): exact match comparison → trivial, automatic (1 or 0), nothing to argue about.
- **Open-ended answers** (e.g., "write a good summary"): no single correct answer key → requires **LLM-as-a-judge** or **human evaluation**.
  - The grader itself now becomes a source of error/bias.
  - Most benchmark controversy originates here.
- Comparison is done one of three ways: programmatically, via LLM-as-a-judge, or via human evaluation.

---

### 6. Part 4 — Aggregation

- Collapses thousands of per-item 1/0 scores into one summary number.
  - Example: 920 correct out of 1,000 → **92% on GSM8K**
- Not always a simple average:
  - **MMLU** spans 57 subjects of unequal size (Biology 87%, Physics 91%, Economics 72%, etc.)
  - Naive averaging can be misleading if question counts per subject are unequal → may require a **weighted mean**
- Aggregation strategy is benchmark-specific and must be checked, not assumed.

---

### 7. The Evaluation Loop (How Evaluation Actually Runs)

Evaluation = a **loop over the dataset**, one pass per item:

1. **Load the item** — question + gold answer
2. **Build the prompt** — inject few-shot examples, apply chat template, add instructions
3. **Call the model** — with the pinned decoding config (temperature, max_tokens, etc.)
4. **Capture the raw output** — log it verbatim (critical for debugging: tells you whether the *model* failed or the *parser* failed)
5. **Extract the answer** — regex/parser pulls the answer from the prose
6. **Grade** — compare extracted answer vs gold answer → 1 or 0
7. **Store** — per-item result along with prompt + output that produced it

After the loop completes → **aggregate** all per-item scores into the final headline number.

**Pseudocode:**
```python
results = []
for item in dataset:
    prompt = build_prompt(item, few_shot=8, template=chat_template)
    output = model.generate(prompt, temperature=0, max_tokens=512, stop=["\n\n"])
    pred = extract_answer(output)              # regex: last number
    score = (pred == item.gold)                # 1 or 0
    results.append({prompt, output, pred, item.gold, score})
accuracy = mean(r.score for r in results)
```

---

### 8. Why This Is Harder Than It Looks — The "Eval Harness"

Looks simple on paper: take a question → send to model → check answer → repeat. In practice, real production code needs to additionally handle:

- Extracting the final answer correctly across varied output formats (e.g., "The answer is C" vs "C." vs "Option C")
- Scoring using the benchmark's **exact** specified method
- Sending thousands of questions efficiently in **batches**
- **Retrying** failed API requests
- Handling **rate limits**

- **Eval harness** = a ready-made piece of code/system that already handles all of this plumbing for you.
- An eval harness already knows:
  1. Where to get the benchmark's (GSM8K, MMLU, etc.) questions
  2. How to format each question
  3. How to send it to the model
  4. How to extract the model's answer
  5. How to judge correctness
  6. How to calculate the final benchmark score

**Analogy:**
> Benchmark = the exam paper.
> Eval harness = the entire exam administration system — instructions, answer-sheet format, checking rules, and score calculation.

**Common eval harness tools:** `lm-evaluation-harness` (EleutherAI, industry standard, used by big companies), **Inspect**, **HELM**, **DeepEval**

#### Live Demo Recap (lm-evaluation-harness)
- Installed `lm-eval`, used OpenAI API key
- Command specified: model (GPT-5.6), `num_concurrent`, max retries, `task=gsm8k`, `cot=True`, `num_fewshot=8`, `apply_chat_template`, `limit=20` (for cheap testing — full run ≈ ₹2,300; 20-question run ≈ ₹3-4), output path, `log_samples=True`
- One command → full evaluation ran automatically, no manual loop code needed
- Result: **~90%** (18/20 correct) — full per-question JSON logs generated
- Removing `limit=20` would produce a real, publishable GPT-5.6 GSM8K score

#### DeepEval vs lm-evaluation-harness
- DeepEval also lists benchmarks (GSM8K included) but requires **more manual code** to run a model through it
- DeepEval is better suited for **application-level evaluation** (testing your own fine-tuned models)
- Most benchmarks available in DeepEval are already saturated ones
- **lm-evaluation-harness = the more "premium"/industry-standard choice**, used at scale by big companies

---

### 9. Who Actually Runs Benchmarks — Three Stakeholders

#### 9a. Frontier Labs (OpenAI, Anthropic, Google DeepMind, etc.)
- Run evals during **pre-training** at different checkpoints → tells them whether training is heading in the right direction, allows mid-course correction
- Used for **release gating** — decide if a new model version is actually better and ready to ship
- Used for **marketing** — strong benchmark scores become a major promotional channel

> ⚠️ **Caution for AI engineers:** Do **not** blindly trust benchmark numbers published by frontier labs.
> - Ask: who ran this evaluation? If "we ran it ourselves, under our own controlled settings" → trust cautiously.
> - Lab numbers are a **ceiling** (best-case, favorable conditions), not a realistic real-world estimate — similar to how advertised car mileage (25) rarely matches real driving mileage (5-10).
> - Labs often **cherry-pick**: highlight benchmarks where they score well, downplay/hide ones where they don't.
> - Personal experience example discussed: "Fable" did not live up to its hype despite claims of being extremely powerful.

#### 9b. Third-Party Evaluators
- Independent organizations/leaderboards (e.g., **LM Arena**) whose core product is evaluation
- Test all models under **identical conditions** → more reliable comparisons
- Provide extra data labs often withhold: **cost** and **latency**
- Considered the **most trustworthy** source for reading model comparisons
- Analogy: like an **IMDb ranking, but for models**

#### 9c. AI Engineering Teams / Companies (You)
- Use public benchmarks + libraries like `lm-evaluation-harness` to run **their own** evaluations
- Captures real conditions relevant to their own use case: latency, cost, actual task performance

---

### 10. Why Benchmarks Can Be Misleading (4 Key Problems)

Benchmarks are useful but **not flawless** — never accept numbers at face value.

#### 10a. Benchmark Contamination
- Most benchmarks are **public** — paper, methodology, and dataset all freely available online
- Especially old benchmarks (2021-2023) have been on the internet a long time
- Large models trained on recent internet scrapes may have **seen the benchmark's questions and answers during pre-training**
- Result: no guarantee the model is reasoning vs. simply **recalling/memorizing**
- **Mitigations:**
  - Use **private benchmarks**
  - Use **dynamic benchmarks** (datasets refreshed daily/periodically, unlike static ones)

#### 10b. Benchmark Saturation
- Lifecycle of a benchmark:
  1. Introduced → hard for all models (e.g., 25-36% scores in 2021)
  2. Models improve every ~6 months → scores rise (50% → 70% → 90%+)
  3. Eventually all top models **cluster near the top** (e.g., 92-95%), with little meaningful separation
  4. Benchmark becomes **saturated** → can no longer differentiate model quality → gets retired and replaced
- GSM8K, MMLU, and SWE-bench are all cited as examples of **saturated** benchmarks

#### 10c. Configuration Gaming
- Frontier labs may tamper with run configuration to favor their own model (e.g., giving their model a Python interpreter on GSM8K while rivals get default settings)
- Can cause **5-10%+ score swings**
- Reinforces: never trust a bare claim like "our model crushed this benchmark" without knowing exact settings used (max tokens, reasoning level, temperature, latency, cost — usually undisclosed)

#### 10d. Aggregation Gaming
- Aggregated averages can **hide weak subject/category performance**
- Example: MMLU — strong in Physics, weak in Economics — but only the **overall average** is disclosed
- Risk: deploying a model for a specific use case (e.g., an economics chatbot) based on a good aggregate score, only to discover poor performance in that specific subject after deployment

---

### 11. Key Takeaway

- Benchmark numbers should always be taken **with a pinch of salt**.
- Do not blindly accept a published number — dig into: run configuration, scoring strategy, tool access, and aggregation method used.
- Build **your own evaluation methodology** for deciding which model actually fits your use case.
- **Leaderboards** (aggregations across multiple benchmarks) and further practical handling of these issues to be covered in the next session.

---

### Quick Reference Table — The Four Benchmark Components

| Component | What It Covers | Key Sub-Decisions |
|---|---|---|
| **Dataset / Task** | Questions + answer key, what the model must do | Public vs private, size, domain |
| **Run Configuration** | Exact conditions under which the model is evaluated | Zero/few-shot, CoT on/off, temperature, max tokens, pass@1/pass@k/maj@k, tools on/off |
| **Scoring Method** | Turning raw output into a 1/0 score | Extraction (regex/structured output), Comparison (exact match / LLM-judge / human) |
| **Aggregation** | Combining per-item scores into one number | Simple mean vs weighted mean, subject-wise breakdown |