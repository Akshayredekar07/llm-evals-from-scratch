# **RAG Application Quality Evaluation with G-Eval**

## **1. Context: Where This Fits in the Overall Eval Plan**

The offline evaluation suite for a RAG pipeline is built at three levels:

1. **Component level**: already completed
2. **Pipeline level** (retriever + generator together): already completed
3. **Application level**: current focus

The application level itself has three separate eval suites:

1. **Quality suite**: covered in this session
2. **Safety suite**: next session
3. **Operations suite**: next session, along with regression testing

### **Quality Suite: Three Metrics Covered Today**

| Metric | What it checks |
|---|---|
| Correctness | Is the generated answer factually right or wrong |
| Completeness | Does the answer cover every sub-part of a multi-part question |
| Style | Does the answer match the intended teaching/brand voice (Campus X style) |

All three are computed using a technique called **G-Eval**.

## **2. Recap: The Five Metrics Covered Earlier**

| # | Metric |
|---|---|
| 1 | Recall |
| 2 | Precision |
| 3 | Faithfulness |
| 4 | Answer Relevance |
| 5 | Context Relevance |

### **Common Pattern: These Are All Count-Based Metrics**

All five follow the same recipe:

1. Break the generated answer into individual **claims** using an LLM.
2. For each claim, ask a yes/no question against a reference (context, golden answer, etc.).
3. **Count** how many claims are favorable vs unfavorable.
4. Compute a **ratio** from that count as the final score.

**Worked example: Faithfulness**

- Generated answer is split into claims (Claim 1, 2, 3, 4).
- Each claim is checked: does it exist in the retrieved context?
- Say 3 out of 4 claims are grounded in context, 1 is invented.
- Faithfulness score = 3/4.

This is a counting exercise, not a judgment exercise.

## **3. Why Some Metrics Cannot Be Count-Based**

Count-based scoring breaks down when there is no natural "claim vs reference" check to perform.

### **Case A: Style**

- Style (e.g., "does this follow a why-what-how teaching pattern") exists at the **whole-answer level**, not the sentence/claim level.
- Breaking an answer into claims and checking each one against a style rule does not make sense, since the pattern spans the whole response.

### **Case B: Correctness (a subtler failure of counting)**

- If a generated answer uses an **analogy** to explain a point, that analogy will not literally match any claim in the golden answer.
- Checked in isolation, the analogy looks like a "false claim" and gets penalized, even though it strengthens the answer.
- Correctness therefore needs to be judged holistically, not claim-by-claim.

### **Metrics That Require Judgment Instead of Counting**

- Correctness
- Completeness
- Style
- Helpfulness
- Safety-related metrics

**Conclusion:** For these, instead of counting, you need **judgment**, either from a human or from an LLM acting as a judge.

## **4. LLM-as-a-Judge: The Naive Approach**

### **Setup**

1. Build a **golden dataset**: pairs of (question, correct/ideal answer), typically written by a human subject-matter expert. Correct here means universally/factually correct, not necessarily "what was taught in this specific course."
2. Feed each question to the RAG pipeline to get an **actual/generated answer**.
3. Send `{question, expected answer, actual answer}` to a judge LLM with a prompt like:
   - "Compare the actual answer against the expected answer and decide how factually correct it is. Give a score from 0 to 10, where 10 = fully correct, 0 = completely wrong."
4. Repeat for all questions in the golden dataset (e.g., 15 questions) and **average** the scores.

### **Key Difference from Count-Based Metrics**

- Count-based metrics: LLM only does a small sub-task (claim extraction/checking); the **ratio formula** decides the score.
- LLM-as-judge: there is no ratio; the LLM's **judgment directly produces the number**.

## **5. The Core Flaw: High Variance**

Running the same evaluation twice, with identical inputs, should ideally give (nearly) the same score. The naive approach does not, for two reasons.

### **Reason 1: Loose, High-Level Criteria**

- A single vague instruction like "decide how factually correct it is" leaves too much room for interpretation.
- Each independent LLM call may apply a slightly different internal standard.
- Result: inconsistent scoring across runs on the *same* input.

### **Reason 2: Directly Trusting the Output Token**

- LLMs generate tokens **autoregressively**, with each candidate token assigned a probability.
- When asked to output "a number from 0 to 10," several nearby numbers may have close probabilities (e.g., 7 at 40 percent, 8 at 51 percent, 6 at 9 percent).
- Because output is probabilistic, one run may output 8, another run 7, even though the underlying distribution barely changed.
- Averaging over many questions amplifies this instability (score could swing from 60 to 75 across identical re-runs).

**Net effect:** Naive LLM-as-judge is not reliable for production-grade evaluation.

## **6. G-Eval: What It Is**

- Introduced in a 2023 research paper.
- Reported to give best results when the judge model is a GPT-4-class model.
- G-Eval is still "LLM as a judge" underneath; it does not introduce a fundamentally new judging concept. It fixes the **two variance problems above** with two specific innovations.

### **Innovation 1: Convert Criteria into Evaluation Steps via Chain of Thought (CoT)**

**Step 1: Provide two inputs**
- The **metric name** (e.g., correctness).
- A **high-level criteria** (e.g., "Compare the actual answer against the expected answer and decide how factually correct it is").

**Step 2: Let the judge LLM expand the criteria into a rule book**
- Using CoT, the high-level criteria is broken down into 4 to 5 precise **evaluation steps**.
- This acts like a "constitution" for the judge to follow, e.g.:
  1. Compare only the factual claims in the actual output against the expected output.
  2. A claim is wrong only if it contradicts the expected output or is factually false.
  3. A factually accurate answer scores high even if shorter and covering fewer points; do not deduct for brevity.
  4. Do not penalize omitted information; only wrong statements count.
  5. Additional correct information must never lower the score.

**Step 3: Build the final judge prompt**
- Combine: role instruction + evaluation steps + (optional) scoring rubric + the actual input, expected output, and actual output.
- Because every future call uses the **same fixed, detailed rule book** instead of a vague one-liner, interpretation variance across runs drops sharply.

### **Innovation 2: Probability-Weighted Scoring (instead of trusting the raw output token)**

**Background:** an LLM's final layer assigns a probability to every possible output token; the highest-probability token is what typically gets printed.

**G-Eval's fix, step by step:**

1. Instead of accepting the single printed number, extract the **top-k candidate tokens** and their probabilities for the score position (commonly top 5).
2. **Discard non-numeric tokens** (e.g., "the", ":") since only digits are relevant to the score.
3. **Normalize** the remaining numeric token probabilities so they sum to 1.
4. Compute a **weighted average** of the numeric values using their normalized probabilities.
5. Divide the result by 10 to map it into a 0 to 1 range.
6. Compare against a **threshold** (commonly 0.7) to decide pass/fail.

**Worked numeric example**

| Token | Raw probability | Normalized probability |
|---|---|---|
| 8 | 0.70 | 0.73 |
| 7 | 0.20 | 0.21 |
| 9 | 0.05 | 0.05 (approx) |

Weighted average:

$$
\text{score} = (8 \times 0.73) + (7 \times 0.21) + (9 \times 0.05) \approx 7.84
$$

- If the raw top token alone were used, the answer would simply be "8."
- Using the weighted average captures *how confident* the model was across 7, 8, and 9, producing 7.84.
- Because this is an average across a probability distribution, small internal fluctuations between runs barely move the final number (e.g., 7.84 stays close to 7.4 to 7.9 on repeat runs, instead of swinging from 6 to 8).

### **Summary of the Two Innovations**

| Problem in naive LLM-as-judge | G-Eval's fix |
|---|---|
| Vague criteria interpreted differently each run | CoT expands criteria into fixed, detailed evaluation steps |
| Raw output token is unstable / probabilistic | Use a probability-weighted average of top-k numeric tokens |

## **7. Implementation Pattern (DeepEval Library)**

DeepEval provides a built-in `GEval` metric class (unlike recall/precision/faithfulness, correctness has no separate built-in metric; G-Eval is used to create it as a custom metric).

**Parameters typically passed to `GEval`:**

- `name`: label for the metric (e.g., "Correctness")
- `criteria` or `evaluation_steps`: either a high-level criteria (G-Eval auto-generates steps via CoT) **or** manually written evaluation steps
- `evaluation_params`: which fields to use, e.g., input, actual output, expected output
- `model`: the judge model (e.g., GPT-4o mini or another GPT-4-class model)
- `threshold`: cutoff for pass/fail after scoring
- `strict_mode`: 
  - `True` disables the probability-weighted calculation and just uses the raw output token.
  - `False` (recommended) enables the full weighted-average calculation.

**Workflow:**

1. Build an `LLMTestCase` with input, actual output, and expected output.
2. Instantiate `GEval` with the above parameters.
3. Call `evaluate()` passing the test case(s) and the metric(s).

### **Criteria vs. Manually Written Evaluation Steps**

| Approach | When to use |
|---|---|
| Give a high-level **criteria**, let G-Eval auto-generate evaluation steps via CoT | Early in the process, when you are still exploring how your model performs and don't yet know the failure patterns |
| Provide your **own evaluation steps directly** | Once you understand common failure patterns; skips the CoT step entirely, is more deterministic since the exact same steps are sent on every call |

## **8. Case Study 1: Correctness Metric**

### **Setup**

- Golden dataset: 15 rows of `{question, ideal/correct answer}`, human-authored, saved as `correctness_golds.json`.
- Eval script (`eval_application.py`) loops over all 15 questions, sends each to the RAG pipeline, builds a test case of `{question, actual output, expected output}`, and evaluates with the `GEval` correctness metric.
- Judge model: GPT-4o mini. Initial threshold: 0.7.

### **First Run Result**

- **Score: 66 percent** (8 passed, 7 failed).

### **Root Cause Analysis**

- The golden/ideal answers were written very thoroughly (every angle covered) by a human expert.
- The RAG pipeline's generated answers were shorter/partial but still factually correct.
- The judge was penalizing generated answers simply for **not fully matching the coverage** of the ideal answer, not for being factually wrong.

### **Fix: Rewrite Evaluation Steps + Add a Scoring Rubric**

Updated evaluation steps included:

- Compare only the factual claims in the actual output against the expected output.
- A claim is wrong only if it contradicts the expected output and is factually false.
- **A factually accurate answer must score at least 9**, even if shorter, less detailed, or covering fewer points than the expected output.
- Do not deduct for brevity, missing elaboration, fewer examples, or omitted points.

Added scoring rubric (explicit control over score bands, so the LLM doesn't decide bands on its own):

- 0 to 4: contains a clear factual error
- 5 to 8: mostly correct with one or two small inaccuracies
- 9 to 10: all claims are factually correct

### **Result After Fix**

- **Score: 84 percent** (14 passed, 1 failed).

### **Determinism Check**

- Re-running the exact same pipeline gave **83 percent** (14 passed, 1 failed), with the **same single test case** failing both times.
- This small, consistent variation (versus wild swings) demonstrates that G-Eval's tighter criteria and weighted scoring make evaluation far more deterministic than naive LLM-as-judge.

## **9. Case Study 2: Completeness Metric**

### **Definition**

- Given an ideal answer composed of multiple distinct points (e.g., points A, B, C), completeness measures whether the generated answer covers **all** of them, not just some.
- Example: ideal answer has 3 points; generated answer covers only 2 → judged as partially complete (e.g., 7.5/10).

### **Implementation**

- Reuses the exact same golden dataset (question + ideal answer).
- Add a **second `GEval` metric** named "Completeness" alongside the existing correctness metric, each with its own evaluation steps and rubric.
- No new code structure is needed beyond adding the second metric and updating the `evaluate()` call to include both.

### **First Run Result**

- **Score: 68 percent**, only **5 passed, 10 failed**, a concerning result.

### **Root Cause Analysis**

- The RAG pipeline's **generator prompt** explicitly instructed it to give concise/short answers strictly from context.
- This constrained scope caused the generator to leave out sub-points of multi-part questions, hurting completeness.

### **Fix: Refine the Generator Prompt (Not the Eval Metric)**

Added instructions to the generator's system prompt:

- Thoroughly identify every distinct part of the question and cover each one.
- Include all relevant points the context provides for answering it.
- If the question has multiple parts or the concept has multiple components, address all of them rather than stopping at the first.

Important: the generator is still restricted to answering from context only. It is not being told to invent information, only to be more thorough in coverage.

### **Result After Fix**

- **Score: 75 percent** (14 passed, 1 failed).

## **10. Case Study 3: Style Metric**

### **Definition**

- Checks whether the generated answer matches a target teaching/brand voice (referred to as "Campus X style").
- Unlike correctness/completeness, **no ideal answer is required** here; only a well-written **rubric** describing the desired style.

### **Rubric Highlights**

- Reward an intuitive, explanatory tone; plain language; ideas explained before formulas/jargon; technical terms briefly unpacked when used.
- Reward a direct, conversational register addressing the student like a live lecture, rather than a dry, formal, textbook tone.
- Reward (but don't strictly require) concrete examples/analogies and "why it matters" framing.

Scoring bands:

- 9 to 10: clearly in the target teaching voice; intuitive and conversational; explains before formalizing.
- 5 to 8: reasonably clear but somewhat flat, formal, or textbook-like.
- 0 to 4: dry, stiff, jargon-heavy, or robotic; doesn't read like a teaching explanation.

### **First Run Result**

- **Score: 54 percent**, expected, since the generator's prompt had never been told anything about the desired style.

### **Fix 1: Update the Generator Prompt for Style**

Added instructions such as:

- Write in flowing, conversational prose the way a teacher explains something out loud, not as a bulleted/numbered list.
- Only use a list when the question genuinely calls for enumeration.
- Explain the intuition first in plain language, and briefly unpack any technical terms used.

### **Fix 2: Correct an Over-Correction in the Rubric**

- After the first prompt fix, failures were being attributed to "missing analogy or example" too rigidly, as if **every** answer must include one.
- Added a balancing clause to the rubric:
  - "An analogy and concrete example is a bonus when the concept is abstract, but a clear, direct, well-explained answer is fully acceptable."

### **Final Run Result**

- **Score: 74 percent** (9 passed, 6 failed).
- Threshold can be tuned further (e.g., lowering from 0.7 to 0.6) depending on how strict the pass bar should be.
- Pushing style too high is not advisable in isolation, since over-optimizing style can start hurting other metrics like faithfulness.

## **11. Key Takeaways**

- **Prompt engineering genuinely moves evaluation scores.** Every fix in this session (correctness, completeness, style) came from tweaking either the eval rubric/evaluation steps or the generator's system prompt, not from changing the underlying model.
- **Correctness vs. Faithfulness are different dimensions:**
  - Faithfulness = is the answer grounded in the retrieved context (regardless of whether that context itself is factually correct).
  - Correctness = is the answer factually correct in the real world/Google-verifiable sense (regardless of whether it came from context).
  - Four possible combinations exist: faithful and correct (ideal), faithful but incorrect (context itself was wrong), correct but not faithful (model used outside/training knowledge), and neither faithful nor correct (hallucinated and wrong).
- **G-Eval generalizes to many custom metrics** beyond correctness, completeness, and style: coherence, tonality, helpfulness, and safety-related metrics can all be built the same way (define metric plus criteria/evaluation steps plus rubric).
- **Two core innovations to remember for G-Eval specifically:**
  1. Convert a high-level criteria into fixed evaluation steps via Chain of Thought, reducing interpretation drift across runs.
  2. Use a probability-weighted average of top-k numeric tokens instead of trusting the single printed score, reducing run-to-run score jumps.

## **12. Next Session Preview**

- Safety eval suite (application level)
- Operations eval suite (application level)
- Regression testing