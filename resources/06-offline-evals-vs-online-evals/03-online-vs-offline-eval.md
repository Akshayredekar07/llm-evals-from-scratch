### **Topic: Offline Evals vs Online Evals (LLM Evals Course)**

---

### **Quick Recap - Covered Before This Topic**

- Why do we need evals
- What exactly are evals (model-based vs application-based)
- How does an LLM eval pipeline look
- Why do we need multiple eval pipelines for a single application
  - Reason 1: multiple failure points (component level, workflow level, application level)
  - Reason 2: different risk categories (application quality, safety, operations)
- Different eval methods (programmatic, LLM-as-a-judge, human evals)

---

### **1. Offline Evals**

**Definition**

- Any eval pipeline run on an LLM application **before deploying it**.
- Whatever was studied/built in previous sessions (UPSC grader example) = offline eval.
- Evaluation happens after software is built but before deployment.

**Why We Need Offline Evals - 3 Main Purposes**

**1. Pre-release testing (Gating)**

- Test properly before releasing to catch risk before it reaches users.
- Ties into **LLMOps / CI-CD**:
  - Code changes pushed to Git → CI triggered (GitHub Actions) → eval script runs → score generated.
  - **Gate logic:** eval score → 95%+ → deploy. Below threshold → don't deploy, notify team.
  - Acts as a **release gate**: pass → deploy; fail → rollback to previous version.

**2. Version Comparison**

- Used when choosing between options: model A vs model B, prompt A vs prompt B, reranker A vs B, vector DB A vs B, architecture A vs B.
- Method: build two versions of the software, run the **same eval + same golden dataset** on both (level playing field).
- Whichever version scores higher → chosen.

**3. Regression Testing**

- Regression testing = "test of change."
- Problem pattern: improving one thing (e.g., politeness via system prompt) can quietly break another thing (e.g., chatbot becomes vague/evasive with numbers like pricing).
- Golden dataset should contain diverse case types (refund questions, pricing questions, curriculum questions, etc.).
- Run eval across all categories after any change → compare against prior scores per category.
- If one category's success rate drops (e.g., 90% → 80%) while testing another improvement → regression detected → change should not be kept.
- **Core rule:** any change anywhere (prompt, model, vector DB) must not break something else.

**Handwritten Notes Reference**

- LLMOps
- CI/CD
- gate
- eval → 95% → deploy

---

### **2. Post-Deployment Risks (Why Offline Eval Is Not Enough)**

Once deployed, offline eval cannot catch everything. Three major categories of production risk:

**1. Unanticipated Inputs**

- Golden dataset only covers what was anticipated (e.g., 200-500 anticipated questions).
- Real users bring a much larger, messier superset of inputs, such as:
  - Questions mixing Hindi and English (Hinglish)
  - Ambiguous, half-formed questions
  - Angry rants with a real question buried inside
  - Adversarial prompt-injection attempts
  - Edge-case scenarios never considered during design

**2. Emergent / Systemic Failures**

- Problems that only exist at scale, under load, or over time - impossible to simulate offline.
- Examples:
  - A retrieval index silently lagging behind its source document
  - Cost per conversation quietly tripling after a prompt change
  - The latency tail (p99) frustrating a slice of users
  - A subtle bias that only becomes visible across thousands of conversations
  - Degradation that only appears under real concurrent load (e.g., latency spike when many users hit the chatbot at once after a course launch)

**3. Drift**

- Business data changes over time (pricing, curriculum, policies change gradually).
- Golden dataset / offline eval setup was built against data as it existed at one point in time.
- As real-world data distribution shifts away from that snapshot, the offline eval setup becomes **obsolete** - it may still report good scores while real user experience degrades (negative feedback rises online).
- Root cause: environment keeps changing but eval setup is not being updated in sync.

**Conclusion**

- Offline eval works on a golden dataset with known correct answers.
- In production, there is no golden dataset - user can ask anything, and the correct answer for it is unknown in advance.
- Hence offline eval alone cannot manage post-deployment risk → need for **online eval**.

---

### **3. Online Evals**

**Definition**

- Evaluating your system on **live production traffic**, after deployment, as real users interact with it.

**Biggest Characteristic / Biggest Challenge**

- Works **without an answer key** - no golden dataset available in production.

---

### **4. Offline vs Online Eval - Comparison Table**

| Feature | Offline Eval (before deployment) | Online Eval (after deployment) |
|---|---|---|
| **Data** | Fixed, pre-collected dataset | Live production traffic |
| **Answer key** | Known in advance | None - must estimate quality |
| **Timing** | Runs before shipping | Runs continuously, live |
| **Inputs seen** | Only what you anticipated | The real, messy distribution |
| **Catches** | Known regressions | Drift, surprises, emergent bugs |
| **Best for** | Gating, version comparison, CI | Real-world quality, drift detection |
| **Cost & speed** | Fast, cheap, repeatable | Ongoing, needs sampling to afford |

**Key Takeaway**

- Offline and online evals are **not rivals** - they are **two halves of one loop**:
  - Offline eval gates what ships.
  - Online eval watches what shipped.

**Core Distinction (Handwritten Note)**

- Offline eval → checks **correctness**
- Online eval → checks **normality** (is the system behaving normally, not necessarily "is it correct")

---

### **5. Correctness vs Normality - Worked Example (UPSC Grader)**

- Offline: correctness measured by comparing grader's marks vs human's marks (golden dataset available).
- Online (post-deployment): correctness cannot be measured directly - no human marks exist for a brand-new answer being evaluated right now (no golden dataset for that specific case).
- **Workaround: baseline distribution comparison**
  - Plot distribution of scores from last week (baseline).
  - Compare with distribution of scores this week.
  - If distributions match → system likely behaving normally (same as before).
  - If distribution shifts significantly → signals something abnormal → triggers investigation.
- This does not guarantee correctness, but tells you whether the system is behaving normally or not - this is the core purpose of online eval.

**Distribution Comparison Diagram (from handwritten notes)**

- Week 1 vs Week 2 comparison
- Score buckets referenced: 300, 400, 500 (example marks)
- **Graph 1 (Last week):** roughly bell-shaped distribution across score axis 0, 200, 500, 750, 1000
- **Graph 2 (This week):** distribution shifted/skewed toward higher scores (around 800), across axis 200, 500, 800
- Shift in shape/peak between the two graphs = signal that something changed → needs investigation

---

### **6. Estimating Quality Without an Answer Key**

Two broad approaches when no golden dataset exists:

**A. Metrics that don't need a correct answer at all**

- Example: **Faithfulness** (RAG systems) - checks if the answer was generated purely from retrieved context; doesn't need to know the "correct" answer, just needs context + generated answer.

**B. Metrics that do need ground truth → require a workaround (jugaad)**

- Example 1: Baseline distribution comparison (UPSC case, described above).
- Example 2: **User feedback as a proxy for correctness**
  - Thumbs up / thumbs down signal.
  - Spike in thumbs-down within a time window → strong signal that something is going wrong → proxy for correctness when no ground truth exists.

---

### **7. Signal Types - Computed vs Captured**

**Captured Signals** (read directly from trace, no computation needed)

- Thumbs up / thumbs down
- Escalation rate
- Abandonment / drop-off
- Rephrase rate
- Conversion
- Latency (p50 / p95 / p99)
- Cost per conversation
- Token usage
- Error rate

**Computed Signals** (produced by an evaluator, needs calculation)

- Faithfulness
- Answer relevance
- Correctness
- Hallucination
- Toxicity
- Bias & fairness
- PII leakage / prompt injection
- Conciseness
- Task completion, satisfaction

---

### **8. Logging - Step 1 of Online Eval Pipeline**

**Core Idea**

- Capture a structured, replayable record of every conversation turn.
- Without logging, there is nothing to evaluate later - conversations would simply be lost.

**What Gets Logged**

- **Identity / threading:** conversation_id, turn_id, user_id / session_id, timestamp
- **Input:** raw student message, plus preprocessing (normalized text, detected language/intent)
- **Retrieved context** (for RAG systems)
- **Output:** response text, model_name / prompt_version (needed for A/B testing and figuring out "which version regressed"), tool calls, finish reason
- **Operational telemetry** (operational-metric family, captured directly):
  - latency_ms (ideally split into retrieval vs generation)
  - prompt_tokens, completion_tokens
  - derived cost
  - error / status codes
- **Downstream user signals** (behavioral-metric family, captured directly):
  - thumbs up / down
  - escalation to support
  - drop-off
  - rephrase
  - conversion

**Tool Used**

- LangSmith (or similar observability tool) - store conversations, view metadata, run monitoring/alerting.

**Engineering Properties of Logging**

- **Non-blocking**
  - Logging must never add latency to the response.
  - Fire to a queue, write in the background.
- **Durable + queryable**
  - Use a data warehouse / observability tool that supports analytical queries.
  - Not scattered text logs - must be retrievable in future.
- **Late-signal attachment**
  - Signals land at different times: thumbs-down within seconds, escalation within an hour, conversion the next day.
  - Records keyed on conversation_id and updated as new signals arrive.
- **PII handling**
  - Scrub / tokenize / mask emails, phone numbers, payment details, Aadhaar number, date of birth, etc.
  - Apply retention limits and access control.
  - Purpose: prevent teammates/employees from extracting sensitive info later from the logging tool.

---

### **9. Pipeline Flow - Captured Quantities**

- Flow: **Log → Dashboard → Alerting**
- No computation/evaluator step needed since the value is already available.

**Dashboarding**

- Quantities displayed over time windows: last 1 hour, 24 hours, 1 week, 6 months, etc.
- Always viewed **aggregated** - a single conversation's latency in isolation doesn't matter; aggregated trend across many conversations matters.
- Example: sudden traffic spike (course launch) → latency graph spikes → team scales resources (e.g., more EC2 instances, load balancer adjustments) → latency normalizes.

**Alerting**

- Engineers can't watch dashboards 24/7.
- Set threshold-based alerts (Slack, email, PagerDuty, custom API).
- Example: alert triggers when a metric crosses threshold in last 5 minutes → team notified → corrective action taken.

**LangSmith Reference (Captured Quantities)**

- Monitoring tab shows built-in graphs: trace latency, error rate, LLM call count, LLM latency, cost.
- Time window selectors: last 1 hr, 3 hrs, 6 hrs, etc.
- Alerts section: select project, name alert, select metric, define condition and threshold, connect to Slack / PagerDuty / custom API.

---

### **10. Pipeline Flow - Computed Quantities**

**Example Used: Hallucination Detection**

**Full Pipeline**

```
Logging → Sampling → Evaluator → Dashboard → Alerts
```

**Step 1: Logging**

- Same as above - log all conversations (e.g., 500/day).

**Step 2: Evaluator Setup**

- Hallucination has no ground truth available → **reference-free evaluation**.
- Recap: reference-based = golden dataset with correct answers exists (e.g., UPSC case); reference-free = no golden dataset.
- **Method: LLM-as-a-judge**
  - A more powerful LLM is given: retrieved context, question, and the original LLM's output.
  - A detailed **rubric** guides the judge LLM on how to detect hallucination.
  - Structure:
    - Inputs → [retrieved context, question, output] → judge LLM → hallucination verdict/score

**Step 3: Sampling (Cost Control)**

- Running the evaluator on all 500 conversations/day is very costly (paying for the conversation + paying to evaluate it).
- **Solution: Sampling** - e.g., out of a large volume like 50,000 conversations, sample down to around 1,000 for evaluation.
- **Random sampling vs Stratified sampling:**
  - Random sampling = simplest, but not the most effective.
  - **Stratified sampling** (better approach):
    - Divide conversations into categories first (e.g., thumbs-down conversations, money/refund-related, abruptly ended, repeated rephrasing, escalated).
    - Pull more samples from "problematic" categories, fewer from normal/thumbs-up categories.
    - Increases chance of correctly catching hallucination in the sample.
  - Diagram reference: question pool (~50,000) → stratified split (~105 each category type example) → sampled set (~1,000)

**Step 4: Evaluator computes the metric**

- Judge LLM outputs a hallucination rate / score for sampled conversations.

**Step 5: Dashboard**

- Aggregated hallucination rate sent to dashboard over time.

**Step 6: Alerts**

- If hallucination rate crosses threshold → alert triggered → team investigates.

**LangSmith Reference (Evaluators)**

- Evaluator templates available under categories:
  - **Security:** PII leakage, prompt injection detection, code injection detection
  - **Safety:** toxicity, bias & fairness
  - **Quality:** hallucination, correctness, conciseness, conversation quality checker
  - **Trajectory:** for agents (not chatbots)
  - Separate evaluators for image-based and voice-based chatbots
- Setting up an evaluator: name it → select application → select judge model (OpenAI/Claude/etc.) + settings (temperature) → write rubric/prompt → define output format → choose run mode:
  - Run on **Tracing** (logs) → becomes an **Online Evaluator**
  - Run on a **Dataset** → becomes an **Offline Evaluator**
- LangSmith = single platform supporting both online and offline evaluation, datasets, experiments, logging, monitoring, and alerting.

---

### **11. The Self-Improving Loop (Closing Offline ↔ Online)**

- When a failure is found in a production conversation (via tracing), it can be added directly to the offline dataset (LangSmith: "Add to Dataset" option).
- Conversations can also be sent to an **annotation queue** - team notes what went right/wrong.
- **Loop:**
  1. Offline evaluation done → deploy
  2. Failures occur in production (caught via online eval)
  3. Failing conversations picked up and added to offline dataset
  4. Offline evaluation re-run on updated dataset → redeploy
  5. New failures surface in production → cycle repeats
- This is how offline and online evals stay in sync continuously - the **self-improving loop**.

---

### **12. Q&A Recap**

**Q: Dashboard shows faithfulness = 0.87, toxicity/latency = 3 - is the bot good?**

- Compare against a **baseline** (usually derived from offline eval).
- 0.87 vs baseline 0.85 → better, good.
- If it later drops to 0.75 against the same 0.85 baseline → concerning → triggers alert or investigation/improvement.

**Q: If offline metric improves from 92 to 99, is that automatically good for online/production?**

- Not necessarily - depends on:
  - Which specific quantity moved from 92 to 99.
  - Whether other quantities dropped as a side effect.
- Improvement in one metric must not cause regression in another metric - that is the exact failure pattern common in LLM-based systems.

---

### **13. Big-Picture Mindset Note**

- Goal of this course: shift mindset from "just build a chatbot with an API" to "make sure this chatbot works correctly for thousands/lakhs/crores of real users."
- This eval-focused thinking differentiates a candidate in interviews and real-world work, since it's not commonly taught/learned widely yet.

---

### **14. What's Next in the Course**

- How to build a golden dataset
- How to run offline evals (hands-on)
- How to run online evals (hands-on)
- Tools/libraries to be used going forward:
  - LangSmith
  - DeepEval
  - Ragas
- Next major topic: **Benchmarks** (model-level evals), before returning to deeper application-level eval work.

---

### **One-Line Summary Table (For Quick Revision)**

| Concept | One-Line Meaning |
|---|---|
| Offline Eval | Test before deployment, using a golden dataset with known answers |
| Online Eval | Test after deployment, on live traffic, without a golden dataset |
| Gating | Auto-deploy/block based on eval score threshold via CI/CD |
| Regression Testing | Ensure improving one thing doesn't break another |
| Drift | Offline eval setup becomes outdated as real-world data changes |
| Reference-based Eval | Golden dataset with correct answers exists |
| Reference-free Eval | No golden dataset; must estimate quality via workarounds |
| Captured Signal | Directly stored, no computation (e.g., latency, thumbs up/down) |
| Computed Signal | Requires an evaluator to calculate (e.g., hallucination, faithfulness) |
| Stratified Sampling | Sample more from problematic conversation categories, less from normal ones |
| Self-Improving Loop | Production failures get added back into the offline dataset |