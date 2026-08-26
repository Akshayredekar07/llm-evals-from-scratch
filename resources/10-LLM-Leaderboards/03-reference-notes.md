### **LLM Leaderboards**

**Definition:** An LLM leaderboard is a public ranking or comparison table that shows how different LLMs perform on a common set of evaluations.

- Benchmarks = the exam (test LLMs on a particular aspect)
- Leaderboard = the result sheet (publishes and compares exam results across models)
- Core idea: one place to compare multiple models on the same evaluation, so you instantly know which model leads

---

### **Why Leaderboards Exist**

- **Common reference for comparison across labs** — every model gives the "same exam," so you can objectively see who ranks where
- **Provides trust** — leaderboards are usually run by a neutral third party, not the model's own company, so the score is more believable (a company scoring its own model has an incentive to inflate results; a third party does not)
- **Guides model selection when you lack resources to run evals yourself** — testing hundreds of models yourself costs huge time and money; someone else has already done that work, so you shortlist from the leaderboard instead
- **Detects benchmark saturation** — when the top models cluster very close together (e.g., top 10 all scoring 92-94%), it signals the benchmark has saturated and a harder benchmark is needed
- **Helps discover new models** — top 3-4 spots are usually dominated by the big labs (Google, OpenAI, Anthropic), but scrolling further down (rank 10-20) surfaces newer, cheaper models that may fit your use case even if they aren't the absolute best

---

### **Who Uses Leaderboards, and For What**

| Stakeholder | Purpose |
|---|---|
| **AI Engineers** | Shortlisting — narrow hundreds of candidate models down to 3-5 worth testing themselves |
| **Frontier Labs** | Competitive positioning and release gating — leaderboard standing is both a marketing asset and an internal go/no-go signal before releasing a new model |
| **Researchers** | Check whether a new technique genuinely helps, measured against a shared baseline; find new research directions |
| **Policymakers and Safety Institutes** | Track capability trends for forecasting and regulation; step in if a model appears significantly more capable/dangerous than others |
| **Open-Weight / Open-Source Community** | Discovery — a small lab with no marketing budget can appear next to a frontier model on the same table and get noticed overnight |

**Real-world example (Frontier Labs):** If OpenAI's next model can't beat Anthropic's current model on a key benchmark, OpenAI will likely delay release rather than launch a model that looks like a downgrade — bad for marketing. Labs strategize release timing based on leaderboard standing.

**Real-world example (Stealth releases):** Google's "Nano Banana" model was initially released under a hidden name on an image leaderboard. Once it dominated the benchmarks and gained attention, Google revealed it was their model and kept the name because it had already become popular.

---

### **Types of LLM Leaderboards**

```
                    LLM Leaderboard Types
                            |
    ------------------------------------------------------
    |               |                |                   |
Benchmark-      Multi-Benchmark   Human-Preference   Application-
Specific        Leaderboards      Based Leaderboards Specific
Leaderboards                                         Leaderboards
    |               |                |                   |
Single test    Combines multiple  Ranks via blind    Ranks for one
(MMLU, GSM8K,  benchmarks +       human votes        real task/domain
HumanEval,     cost/latency/      (e.g. LM Arena)    (coding, SQL,
GPQA)          context info                          agentic, medical)
    |               |                |                   |
Narrow view    Most useful —      Popular for         Good for
of performance overall capability marketing, has      domain-specific
               + cost/perf view   human bias          selection
```

**1. Benchmark-Specific Leaderboards**
- Rank models using the result of one particular benchmark only
- Examples: MMLU, HumanEval, GSM8K, GPQA
- Answers: *Which model performs best on this one benchmark?*
- Limitation: gives a very narrow view — good score on one test tells you little about overall model quality
- Example seen: Humanity's Last Exam (HLE) leaderboard — shows a single benchmark's scores per model

**2. Multi-Benchmark Leaderboards**
- Combine results from multiple benchmarks and evaluation dimensions into one view instead of relying on a single test
- Cover capabilities such as: knowledge, reasoning, mathematics, coding, instruction-following, data analysis
- Often also include practical deployment factors: cost per token/query, latency, output speed, context-window size, availability, price-to-performance ratio
- Results may be shown as separate scores per category or combined into one overall ranking
- Answers: *Which model provides the strongest overall combination of capability, cost, and performance?*
- This is the **most useful category** and the one used most in practice
- Examples: LiveBench (23 tasks across 7 categories with an overall score), Artificial Analysis (separate leaderboards for intelligence, speed, cost, and more)

**3. Human-Preference-Based Leaderboards**
- Do not rank using a fixed benchmark — rank using human votes instead
- Mechanism: a user asks a question, two anonymous models (A and B) respond, the user picks the better response; after enough votes, a ranking emerges
- Answers: *Which model's responses do users prefer?*
- Useful for measuring: helpfulness, clarity, writing quality, creativity, tone, conversational ability
- Limitation: preferred answer is not always the most factually correct one — humans are swayed by longer, more confident, better-formatted, or more agreeable/entertaining answers; also affected by human bias and possibly coordinated voting
- Example: LM Arena (battle mode — ask a question, compare two hidden model outputs, vote, then reveal identities)

**4. Application-Specific Leaderboards**
- Built around one particular domain or real-world task, even if they use multiple underlying benchmarks
- Examples: fixing software bugs, calling APIs/tools, generating SQL queries, answering medical questions, completing agentic tasks, working with long documents
- Answers: *Which model or AI system performs best for this specific application?*
- Example: Berkeley Function Calling Leaderboard — ranks models specifically on tool/function-calling ability

---

### **Why You Cannot Blindly Trust Leaderboards**

**1. Benchmark performance may not transfer to real applications**
- Benchmark questions are clean, well-defined, self-contained (like Kaggle datasets)
- Real applications involve: ambiguous requests, missing information, company-specific data, multi-turn conversations, tool failures, unusual edge cases
- A model that tops academic benchmarks can still fail inside a real customer-support bot, coding assistant, or RAG system
- Leaderboards are good for shortlisting, not a substitute for evaluating on your own use case

**2. Benchmark contamination can inflate scores**
- Many benchmark questions are publicly available (papers, repos, tutorials, websites) and may leak into a model's training data
- A model may answer correctly because it has memorized the question, not because it can genuinely solve it
- A high score may reflect: genuine capability, memorization, or familiarity with similar questions — you cannot tell which just from the number

**3. Models can be over-optimized for the leaderboard (leaderboard overfitting)**
- Once a leaderboard becomes influential, developers optimize specifically for it: submit a model, study weak areas, tweak the model/prompt/agent, repeat
- The model gets very good at winning that specific leaderboard without improving equally on unseen real-world tasks
- Example: to win human-preference leaderboards like LM Arena, labs may fine-tune models to give longer, more agreeable, better-formatted responses — optimizing for what humans vote for, not for real capability
- This is explained by **Goodhart's Law**: *"When a measure becomes a target, it ceases to be a good measure."*
- Analogy: if a car company only optimizes for mileage because that's what Indian buyers care about, the car's mileage improves but overall quality (handling, acceleration, safety) suffers

**4. Overall rankings depend on subjective design choices**
- Multi-benchmark leaderboards must decide: which benchmarks to include, which to exclude, how scores are normalized, how much weight each benchmark gets, whether cost/latency affects ranking
- These choices are often not disclosed, and changing them changes the final ranking
- Example: a coding-heavy composite leaderboard favors one model; a reasoning-heavy one favors another — same models, different "best" answer

**5. Small score differences may not be meaningful**
- Leaderboards show exact ranks even when the gap between models is tiny (e.g., Model A: 84.3 vs Model B: 84.1)
- Such a small difference can be caused by prompt variations, a small test set, evaluation noise, or grading errors
- A model ranked 3rd may not be meaningfully better than one ranked 5th
- Rankings become especially unreliable when confidence intervals are not shown — analogy: rank 1 vs rank 25 in an exam like IIT JEE may just come down to one or two questions

**6. Human-preference leaderboards have human biases**
- Human voting is valuable for helpfulness, tone, and writing quality, but people tend to prefer answers that are longer, more confident, better formatted, more agreeable, or more entertaining — not necessarily more accurate or better reasoned
- The voting population may not represent your actual users
- Can also be affected by coordinated voting or attempts to identify and favor specific models

**7. Scores may be stale, incomplete, or self-reported**
- A leaderboard may contain: results from older model versions, missing newly released models, discontinued models still listed, or self-reported results that were never independently verified
- Example: HLE leaderboard may still be missing the latest released models simply because maintainers haven't updated it yet
- Some leaderboards let companies submit their own model's results directly — reduces trustworthiness

---

### **How to Read LLM Leaderboards as an AI Engineer**

**Core principle: Leaderboards are a filtering tool, not a decision tool.**

```
Step 1: Write down your requirements
        (task type, latency budget, cost ceiling,
         context needs, deployment constraints)
                    |
                    v
Step 2: Pick the leaderboard that matches your task
        (not the most famous one)
                    |
                    v
Step 3: Read the leaderboard correctly
        (what's scored, who evaluated it, inference
         compute used, dataset age, saturation,
         confidence intervals, composite weights)
                    |
                    v
Step 4: Cut down to 3-5 candidate models
        (apply hard filters: license, price, latency,
         regional availability)
                    |
                    v
Step 5: Run your own evaluation
        (this is where the real decision happens)
```

**Step 1: Write your requirements down before opening any leaderboard**
- Task type
- Latency budget
- Cost ceiling
- Context needs
- Deployment constraints (on-prem? open weights? data retention rules?)
- Doing this first stops you from unconsciously rationalizing toward whatever model sits at rank #1 — this is the single most important habit to take away

**Step 2: Pick the leaderboard that matches your task, not the famous one**
- Agents → SWE-bench Pro / Terminal-Bench / OSWorld
- Tool use → BFCL (Berkeley Function Calling Leaderboard)
- Chat → the matching LM Arena sub-arena
- RAG → MTEB (embedding model ranking leaderboard, since RAG needs a good embedding model)
- Budget-constrained → a leaderboard that reports price and throughput (e.g., Artificial Analysis, Vellum)

**Step 3: Read the leaderboard correctly**
- What exactly is scored — an answer key, a test suite, human votes, or an LLM judge?
- Who ran the evaluation — an independent evaluator or the vendor itself (self-reported)?
- At what inference compute — reasoning-effort settings change both the score and your bill
- How old is the eval set — static and public data means assume contamination risk
- Is it saturated — if the top ten scores sit within a couple of points of each other, the benchmark is effectively over
- Are confidence intervals shown — if not, treat adjacent ranks as tied
- If it's a composite score — what are the category weights? Unpublished weights mean an unpublished opinion baked into the ranking

**Step 4: Cut down to 3-5 candidates**
- Apply hard filters first: license, price ceiling, latency requirement, regional availability

**Step 5: Run your own evaluation — this is where the actual decision happens**
- Use 50 to a few hundred examples from your real traffic — this beats any public benchmark for your specific use case
- Score candidates on: quality, cost, latency, and failure behaviour

---

### **Key Takeaway**

Leaderboards are a **filtering tool, not a decision tool.** Use them to shortlist 3-5 candidate models based on your requirements — never pick your final model directly off a leaderboard rank. The final decision always comes from running your own custom evaluation on your own data.

---

### **Quick Revision Cheat Sheet**

| Question | Answer |
|---|---|
| What is a leaderboard? | Public ranking/comparison table of LLM performance on shared evaluations |
| 4 types of leaderboards | Benchmark-specific, Multi-benchmark, Human-preference, Application-specific |
| Most useful type | Multi-benchmark (gives capability + cost + latency view) |
| Least useful type | Benchmark-specific (too narrow) |
| Key law about metric gaming | Goodhart's Law — "when a measure becomes a target, it ceases to be a good measure" |
| Biggest risk to benchmark reliability | Benchmark contamination (data leaking into training) |
| RAG-related leaderboard | MTEB (embedding models) |
| Tool-calling leaderboard | BFCL (Berkeley Function Calling Leaderboard) |
| Human-vote leaderboard example | LM Arena |
| Final rule | Leaderboards filter candidates; your own eval decides the winner |