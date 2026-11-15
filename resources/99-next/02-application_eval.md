# **Phase 1: LLM Application Evals**

This phase shows how to build a real evaluation suite for a chatbot, an extraction feature, or an agent. You read traces first, turn failures into tests, pick the simplest grader for each failure, calibrate any LLM judge, and keep the suite alive with CI and production traces.

The main rule:

```text
Error analysis first. Metrics second.
```

Do not start with "what accuracy should I measure?". Start with "how is my system actually failing?".

---

## **1. Key Terms**

| Term | Meaning |
|---|---|
| Eval | A repeatable test of an LLM system against clear criteria |
| Task or test case | An input plus success criteria |
| Trial | One attempt at a task |
| Grader | Logic that decides if a trial met a criterion |
| Trace | The full record of one run |
| Span | One step inside a trace (a model call, a retrieval, a tool call) |
| Trajectory | The path of steps an agent took |
| Outcome | The real final state (database rows, files, tickets), not what the model claims |
| Eval harness | The system that runs tasks, records traces, grades, and aggregates |
| Failure mode | A named, repeated kind of failure |
| Failure taxonomy | The organized list of failure modes with counts |

Phase 0 skills you will use here: Python and pytest, JSON and JSONL, SQL for sampling traces, confidence intervals, paired comparison, Cohen's kappa, and train, dev, and held-out splits.

The whole workflow in one line:

```text
Read traces, list failures, write test cases, pick graders, calibrate judges, run and compare, gate releases, learn from production, repeat
```

---

## **2. Error Analysis First**

Error analysis means reading real traces to learn how the system fails, before building any metric.

A generic score such as "helpfulness from 1 to 10" hides the real problems. A chatbot can score well while it still invents refund rules or calls the wrong tool. Each problem needs a different fix and a different grader.

**What a trace holds**

- The user request and earlier turns
- System instructions and tool descriptions
- Retrieved documents
- Every tool call, its arguments, and its result
- The final response
- The final environment state
- Metadata: prompt version, model, latency, cost, timestamps

Response versus outcome: an agent may say "your refund was issued", but the outcome is whether a refund row exists in the database. Check both.

Example trace:

```text
User: Cancel order ORD-12. It has not shipped.

1. Agent calls get_order("ORD-12")
2. Tool returns status = "processing"
3. Agent calls cancel_order("ORD-21")        <- wrong id
4. Tool returns status = "cancelled"
5. Agent says "ORD-12 has been cancelled."
6. Database: ORD-12 is still processing
```

The final reply is false, but it is only a symptom. The first meaningful failure is step 3.

**How to collect traces**

| Source | Best use | Limit |
|---|---|---|
| Production traces | Real behavior and surprises | Privacy, sampling bias |
| Internal testing | Before launch | Biased to what developers expect |
| Simulated users | Repeatable multi turn cases | The simulator may be unrealistic |
| Synthetic data | Rare and edge cases | Must be reviewed, can be too clean |
| Past incidents and tickets | Regression cases | May lack execution details |

Collect 50 to 100 traces for the first pass. If you have no real traffic, write realistic inputs by hand and label them as simulated, including hard ones such as "I already used the course for three weeks. Can I still get a refund?"

Rules:

- Include good and bad runs. Reading only failures bends the picture.
- Keep prompt version, model, and app version with every trace.
- Remove personal data before anyone annotates.

If one intent dominates traffic, sample per intent so rare cases appear:

```sql
SELECT trace_id, task_type, status, latency_ms, created_at
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY task_type ORDER BY RANDOM()) AS row_number
    FROM traces
    WHERE created_at >= CURRENT_DATE - INTERVAL '14 days'
) AS sampled
WHERE row_number <= 20;
```

**How to read a trace**

Use the same order every time:

1. Read the user request. What was asked?
2. Read the system instructions and tool descriptions. Are they clear?
3. Check retrieval. Right documents, current, enough?
4. Check each tool call. Right tool, right arguments?
5. Check each tool result. Did the model read it correctly?
6. Read the final response. Correct, safe, honest about what happened?
7. Check the final environment state. Did the action really happen?
8. Mark the first meaningful failure.

Record the first failure, because upstream mistakes cause downstream symptoms. If retrieval brings back an old policy and the model follows it faithfully, the first failure is retrieval, not generation. Add other independent failures as secondary tags so one root cause is not counted twice.

**How to annotate**

Force a pass or fail decision, then write one line about the first failure. Do not force categories yet. This is called open coding.

| Weak note | Better note |
|---|---|
| "Bad answer" | "Says refund is complete, but no refund record exists" |
| "Tool problem" | "cancel_order received ORD-21, user asked for ORD-12" |
| "Hallucination" | "Gives a delivery date that is not in the tool result" |
| "Slow" | "Retrieval took 2.4 s, target is 0.5 s" |

Annotation template:

```json
{
  "trace_id": "trace_002",
  "label": "fail",
  "first_failure_span": "span_4",
  "failure_note": "cancel_order received ORD-21, user asked for ORD-12.",
  "category": null,
  "severity": "high",
  "confidence": "high"
}
```

Habits: describe what you can see, not guesses about the cause. Keep notes to one line. Use one severity scale for all reviewers. Keep reading until new traces stop showing new kinds of failure.

**From notes to failure modes**

```text
Trace 1:  Used wrong price.
Trace 7:  Used the listed price, not the discounted price.
Trace 19: Calculated the refund wrongly.
Trace 31: Refunded full amount instead of partial.
```

These four notes group into one mode: incorrect refund amount.

Aim for 5 to 12 modes. Give each a short name, a one sentence definition, what counts and what does not, one example, and a way to measure it. Name modes after the behavior, not a guess about the cause. Avoid "agent is wrong" (too broad) and "used ORD-12 wrongly on Tuesday" (too narrow). Keep an "other" bucket and review it later.

Example taxonomy for a support agent with retrieval:

| Group | Failure modes |
|---|---|
| Retrieval | Wrong document, missing document, stale document |
| Reasoning | Wrong calculation, wrong policy reading, ignored user limit |
| Tool use | Wrong tool, wrong arguments, misread tool result |
| Policy and safety | Skipped identity check, unauthorized action |
| Outcome | Action not done, false completion claim |
| Communication | Rude tone, unclear explanation, false promise |

Counting example, 100 traces read and 40 had a problem:

```text
Failure rate = 40 / 100

Failure rate = 40%

Biggest category has 12 traces

Share of failures = 12 / 40

Share of failures = 30%
```

This is the rate in your sample. It equals the production rate only if the sample is representative.

**How to prioritize**

Rank modes by how often they happen and how much damage one case does. Rate each from 1 to 5.

```text
Priority = Frequency x Impact
```

| Failure mode | Frequency | Impact | Score | Priority |
|---|---:|---:|---:|---|
| False refund confirmation | 3 | 5 | 15 | Critical |
| Invalid tool arguments | 4 | 3 | 12 | High |
| Skipped identity check | 2 | 5 | 10 | Critical review |
| Unclear response | 4 | 1 | 4 | Lower |

The score is only a guide. A rare safety or legal failure can still block a release.

**Decide what to do with each failure**

Not every failure needs an eval. Some are plain bugs to fix first.

| Failure | Fix first | Then measure with |
|---|---|---|
| Wrong tool argument | Fix the tool description | Code check |
| Missing required field | Fix the output format in the prompt | Code check |
| Tone too harsh | Add a tone rule | LLM judge |
| Policy broken | Add the policy to the prompt | LLM judge |

---

## **3. Test Cases and Success Criteria**

A failure mode is general. A test case is one concrete input with clear success criteria. Each important mode needs several test cases, because one case cannot show a mode is fixed.

Example for the mode "incorrect refund amount":

```text
T001: Refund a $49.99 discounted order.
T002: Refund one item from a $99.98 two item order.
T003: Refund an order with a coupon.
T004: Refund an order with tax.
T005: Refund an order with a percentage discount.
```

Five kinds of case:

| Type | Purpose | Example |
|---|---|---|
| Normal | Common behavior | Standard refund |
| Edge | Unusual but valid | Partial refund |
| Adversarial | Misuse or manipulation | User asks for a bigger refund |
| Regression | An old bug stays fixed | A past failing refund case |
| Safety | Unsafe action is blocked | Refund for another person's order |

Also include cases where the behavior should not happen. If every case rewards an action, the system learns to always do it.

A test case as JSON:

```json
{
  "task_id": "refund_006",
  "category": "policy_and_safety.skipped_identity_check",
  "input": {"customer_id": "cust_101", "message": "Refund my order immediately."},
  "expected_outcome": {"refund_processed": false},
  "success_criteria": [
    "Does not process a refund before identity is verified",
    "Asks for the required verification"
  ],
  "tags": ["refund", "identity", "regression"]
}
```

**Write the criterion before the grader.** A good criterion is clear (two reviewers read it the same way), observable (the evidence is in the output, trace, or state), measurable, and about one behavior. If you cannot write it clearly, you do not yet understand the failure.

| Vague | Measurable |
|---|---|
| "Good answer" | "Contains the two required facts and does not contradict the source" |
| "Uses tools correctly" | "Calls `get_order` with the order id the user gave" |
| "Safe refund" | "Does not call `process_refund` before identity check succeeds" |
| "Code works" | "All existing tests and the new regression test pass" |

Criteria by feature:

| Feature | Criteria |
|---|---|
| RAG chatbot | Every claim is supported by retrieved text. No invented citation. Says so when the documents lack the answer |
| Support agent | Identity checked first. Refund within the allowed amount. Refund row exists. Reply states the real status |
| Extraction | Valid JSON. All required fields. Invoice id matches exactly. Amount correct |
| Coding agent | Patch touches the intended files. Existing tests pass. New regression test passes. No forbidden files changed |

---

## **4. Choosing the Grader**

Use the simplest grader that works. If an assertion can do it, use the assertion.

| Failure type | Grader | Examples |
|---|---|---|
| Deterministic and checkable | Code check | Valid JSON, required fields, allowed labels, tool arguments, database state, latency |
| Subjective or needs reading | LLM judge | Tone, policy adherence, completeness, groundedness |
| High stakes, unclear, or for calibration | Human review | Rare serious cases, and the labels used to calibrate judges |

Why code first: it is free, fast, gives the same result every time, needs no calibration, and does not drift when a judge model changes.

Two setups you will see:

- Reference based: compare with a known expected answer or state. Good for extraction and fixed outcomes.
- Reference free: grade against a rule with no golden answer. Good for tone, safety, and production monitoring.

These describe the setup, not the tool. Either can use code, a model, or a human. A mixed approach is usually best.

**Code check patterns**

Exact match, regex, JSON and schema checks, required fields, tool arguments, database or file state, unit tests, latency, and cost.

Five checks on a support assistant output, with a dry run:

```python
import json
import re

allowed_categories = ["refund", "booking", "technical", "other"]
student_message = "Please refund order ORD-12345, it arrived damaged."
model_output = '{"category": "refund", "order_id": "ORD-12345", "reply": "Your refund request is received."}'

parsed_output = json.loads(model_output)
order_id_in_message = re.search(r"ORD-\d{5}", student_message).group()

print("valid json:", isinstance(parsed_output, dict))
print("required fields:", all(field_name in parsed_output for field_name in ["category", "order_id", "reply"]))
print("allowed category:", parsed_output["category"] in allowed_categories)
print("order id matches:", parsed_output["order_id"] == order_id_in_message)
print("reply length:", len(parsed_output["reply"].split()) <= 60)

parsed_output["order_id"] = "ORD-1234"
print("after breaking order id:", parsed_output["order_id"] == order_id_in_message)
```

Expected output:

```text
valid json: True
required fields: True
allowed category: True
order id matches: True
reply length: True
after breaking order id: False
```

Return more than a bare true or false, so a failure is easy to debug:

```json
{
  "grader": "correct_order_argument",
  "status": "FAIL",
  "reason": "Expected order_id ORD-12, received ORD-21.",
  "evidence": {"expected": "ORD-12", "actual": "ORD-21"}
}
```

Cautions:

- A regex proves a phrase appears, not that the statement is true. Check state for that.
- Malformed JSON should give a structured FAIL result, not crash the run.
- Run agent written code only in a real sandbox. A plain subprocess is not one.
- Test on an isolated database, never on real customer data.
- One request cannot show a p95. Aggregate many requests.
- For money, use Decimal instead of floats in real checks.

**Test your graders.** Each code check needs at least one passing case and one failing case in pytest.

```python
def grade_refund_amount(actual_amount, expected_amount):
    return abs(actual_amount - expected_amount) < 0.01

def test_correct_refund_amount():
    assert grade_refund_amount(49.99, 49.99) is True

def test_wrong_refund_amount():
    assert grade_refund_amount(59.99, 49.99) is False
```

Expected output of `pytest`:

```text
2 passed
```

---

## **5. LLM Judges**

A judge is an LLM prompt that grades one output against a rule. Use it only when code cannot decide.

Rules for a good judge:

- One criterion per judge. Not "polite and correct and complete".
- Binary result: pass or fail, plus a short reason, plus an unknown option.
- A clear definition of pass, fail, and unknown.
- A few examples, at least one pass and one fail.
- Only the evidence it needs. Extra context hurts.
- A fixed output format such as JSON.

A 1 to 10 score is a bad choice: it mixes many things, drifts, and nobody agrees what a 7 means.

Judge prompt template:

```text
You are checking one thing only: is the reply grounded in the supplied context?

Pass: every important claim in the reply is supported by the context.
      The reply may say "I don't know" when the context is not enough.
Fail: at least one important claim contradicts the context or has no support in it.
Unknown: the context is missing or too incomplete to decide.

Do not reward length. Do not assume a claim is true just because it sounds likely.

Example 1
Context: Refunds are available within 7 days.
Reply: You can get a refund within 7 days.
Reason: Matches the context.
Verdict: pass

Example 2
Context: Refunds are available within 7 days.
Reply: You can get a refund within 30 days.
Reason: Says 30 days, the context says 7.
Verdict: fail

Context: {context}
Reply: {reply}

Return JSON: {"reason": "<one short sentence>", "verdict": "pass" | "fail" | "unknown"}
```

What to do with unknown:

- Never count it as a pass.
- Report the unknown rate separately and send those items to a human.
- If more than about 5% come back unknown, the rule is probably unclear. Rewrite it.

---

## **6. Calibrating a Judge**

A judge is a measuring tool, so measure the tool. A judge that gives confident reasons can still be wrong.

**Steps**

1. Hand label 100 to 200 items as pass or fail, with a short reason each. Make sure there are at least 20 to 30 real failures, or TPR will be very uncertain. For important criteria, have a second person label part of them and settle disagreements. This is a planning target, not a rule.
2. Split the items. One example split: 20% for writing the prompt and examples, 40% dev, 40% held out. Keep enough failures in every part.
3. Use only prompt split items as examples inside the judge prompt. Never a held-out item.
4. Run the judge on dev, read every disagreement, fix the prompt, repeat.
5. Freeze the prompt and run once on held out. Report the numbers.
6. Re-check after any change of judge model or rubric, and on a small fresh sample about once a month. Save a new version name for every prompt change.

**What to report.** Positive means "a real failure".

| | Human says fail | Human says pass |
|---|---:|---:|
| Judge says fail | TP | FP |
| Judge says pass | FN | TN |

| Metric | Question it answers |
|---|---|
| TPR (recall) | Of the real failures, how many did the judge catch? |
| TNR | Of the real good outputs, how many did the judge pass? |
| Precision | When the judge says fail, how often is it right? |
| F1 | One number balancing precision and recall |
| Cohen's kappa | Agreement with humans after removing luck |
| Unknown rate | How often the judge could not decide |

Take unknown out of the binary math at first, but report its count. Which number matters most depends on risk. For a safety failure, a missed failure (low TPR) costs more than a false alarm. For an expensive human review queue, precision matters more.

**Worked example.** 100 items. Humans: 40 fail, 60 pass. Judge: TP 36, FP 8, FN 4, TN 52.

```text
TPR = 36 / (36 + 4)

TPR = 36 / 40

TPR = 90%

TNR = 52 / (52 + 8)

TNR = 52 / 60

TNR = 86.7%

Precision = 36 / (36 + 8)

Precision = 36 / 44

Precision = 81.8%

F1 = 2 x 0.818 x 0.90 / (0.818 + 0.90)

F1 = 1.4724 / 1.718

F1 = 85.7%
```

Kappa step by step:

```text
Observed agreement = (36 + 52) / 100

Observed agreement = 0.88

Humans say fail 0.40 of the time, the judge says fail 0.44 of the time

Chance agreement = 0.40 x 0.44 + 0.60 x 0.56

Chance agreement = 0.176 + 0.336

Chance agreement = 0.512

Kappa = (0.88 - 0.512) / (1 - 0.512)

Kappa = 0.368 / 0.488

Kappa = 0.754
```

Report both raw agreement and kappa. Kappa depends on how common each label is, so never read it alone, and there is no single pass line for it.

The same numbers in code, with a Wilson interval for TPR:

```python
import math

true_positive = 36
false_positive = 8
false_negative = 4
true_negative = 52
total_items = true_positive + false_positive + false_negative + true_negative

true_positive_rate = true_positive / (true_positive + false_negative)
true_negative_rate = true_negative / (true_negative + false_positive)
precision = true_positive / (true_positive + false_positive)
observed_agreement = (true_positive + true_negative) / total_items

human_fail_share = (true_positive + false_negative) / total_items
judge_fail_share = (true_positive + false_positive) / total_items
chance_agreement = human_fail_share * judge_fail_share + (1 - human_fail_share) * (1 - judge_fail_share)
kappa = (observed_agreement - chance_agreement) / (1 - chance_agreement)

z_value = 1.96
proportion = true_positive_rate
denominator = 1 + z_value**2 / (true_positive + false_negative)
centre = (proportion + z_value**2 / (2 * (true_positive + false_negative))) / denominator
spread = z_value * math.sqrt(proportion * (1 - proportion) / (true_positive + false_negative) + z_value**2 / (4 * (true_positive + false_negative)**2)) / denominator

print(f"TPR: {true_positive_rate:.1%}")
print(f"TNR: {true_negative_rate:.1%}")
print(f"precision: {precision:.1%}")
print(f"kappa: {kappa:.2f}")
print(f"TPR 95% interval: {centre - spread:.1%} to {centre + spread:.1%}")
```

Expected output:

```text
TPR: 90.0%
TNR: 86.7%
precision: 81.8%
kappa: 0.75
TPR 95% interval: 76.9% to 96.0%
```

So "TPR 90%" really means "somewhere from about 77% to 96%". More real failures in the labelled set make the range smaller.

**Fix the judge's pass rate.** A judge with known TPR and TNR gives a biased pass rate that you can correct. Suppose the judge says 80% pass, with TPR 85% and TNR 90%.

```text
Top part = 0.80 + 0.85 - 1

Top part = 0.65

Bottom part = 0.85 + 0.90 - 1

Bottom part = 0.75

Corrected pass rate = 0.65 / 0.75

Corrected pass rate = 86.7%
```

Treat this as a rough guide. It is noisy when the labelled set is small, unstable when the judge is weak, and assumes the judge behaves the same on new data.

**Know the biases**

| Bias | What happens | What to do |
|---|---|---|
| Position | Prefers the first or last answer when comparing two | Swap the order, run twice, keep only answers that agree |
| Verbosity | Prefers longer answers | Say "length does not matter", test short correct against long wrong answers |
| Self preference | Prefers its own model family | Judge with a different model family where practical |
| Formatting | Prefers nicely formatted text | Test plain and formatted versions of the same answer |
| Leniency | Passes too easily, so low TPR | Add failure examples |
| Strictness | Fails good outputs, so low TNR | Add clear pass examples, including valid alternatives |
| Instability | Same item, different verdicts | Run twice and check how often it flips |

A different model family helps, but it does not replace calibration.

---

## **7. Preventing Grader Gaming**

Grader gaming is when a system satisfies the grader without doing the real task. Agents find weak graders.

| Weak grader | How it is gamed | Better grader |
|---|---|---|
| Keyword "refund" appears | "I cannot help with refunds." | Check the refund state and the policy |
| Passes if `process_refund` was called | Call it with a wrong id or amount | Check arguments, result, and database row |
| Output contains "All tests passed" | Print the phrase | Run the real tests, check the exit code |
| Score 1 to 10 for quality | Long confident answer | One criterion per judge, penalize unsupported claims |

How to make graders harder to game:

1. Grade the real outcome, not a stand in for it.
2. Use separate checks for separate criteria.
3. Include adversarial and negative cases.
4. Keep a held-out set that is never used for tuning.
5. Review suspiciously perfect scores.
6. Try to fool your own grader with an output that passes the shortcut but fails the task.
7. Use human review for high risk cases.

---

## **8. Evaluating Agents**

For agents the first question is: did the environment end in the required state?

| Task | Agent says | Check | If it fails |
|---|---|---|---|
| Refund | "Refund processed" | Refund row exists, correct amount | Fail |
| Booking | "Meeting scheduled" | Calendar event exists | Fail |
| File writing | "Report saved" | File exists and has the right content | Fail |
| Code fix | "Bug fixed" | Tests pass in a clean environment | Fail |

A tool saying "success" is not enough. Also look for duplicate or partial actions, and reset state between trials.

Grade several things on their own, and never let an average hide a serious failure:

| Dimension | Example grader |
|---|---|
| Outcome | Database has the expected refund |
| Policy | Identity was verified before the refund |
| Tool use | Correct tool and arguments |
| Communication | Reply states the real outcome |
| Efficiency | Tool calls and latency within limits |

A good tone score must never hide a policy violation.

**Use the trajectory for debugging, rarely as the pass rule.** Two agents can reach the same correct result by different paths (search the policy then get the order, or the reverse). Requiring one exact sequence would reject a valid solution. Check only what matters:

- A required tool was used when the policy needs it.
- Arguments were correct.
- A required step came before a sensitive action (identity check before refund).
- The final state is correct.
- No forbidden action was taken.

**Span attached evaluation** puts a small grader on one step:

```text
Trace
├── retrieve_policy    relevance   pass
├── calculate_refund   correctness fail   <- first failing step
├── create_refund      action      pass
└── customer_response  tone        pass
```

When the root result fails, you can see which step failed first.

**Examples of agent evals**

| Agent type | What the grader checks | Public benchmark to study |
|---|---|---|
| Customer support, tool use | Final database state, policy followed, reliability over repeated trials | tau-bench |
| Coding agent | Hidden tests pass after the patch, no forbidden files touched | SWE-bench Verified |
| Function calling | Right function, right arguments | Berkeley Function Calling Leaderboard |
| Web or browser agent | Page or account state after the task | WebArena |
| General assistant with tools | Exact final answer to a hard question | GAIA |
| SQL agent | Query result equals the reference result | Spider, BIRD |
| RAG agent | Retrieval hit, groundedness, abstention when evidence is missing | HotpotQA, CRAG, RAGTruth |

Use these to learn how real evals are built (task, environment, state check). Your own application still needs its own tasks, built from your own traces.

A coding agent test case:

```json
{
  "task_id": "code_014",
  "category": "coding.regression",
  "input": {"issue": "parse_date crashes on empty string", "repo_snapshot": "repos/app_v3"},
  "expected_outcome": {"failing_test": "tests/test_dates.py::test_empty_string", "must_pass": true, "existing_tests_must_pass": true},
  "success_criteria": [
    "The named regression test passes in a clean container",
    "All previously passing tests still pass",
    "No file under config/ or secrets/ is changed"
  ],
  "tags": ["coding", "regression"]
}
```

A SQL agent test case:

```json
{
  "task_id": "sql_007",
  "category": "tool_usage.wrong_arguments",
  "input": {"question": "Total revenue in March 2026 for paid orders"},
  "expected_outcome": {"result_rows": [[18450.00]]},
  "success_criteria": [
    "Query runs read only",
    "Result rows equal the reference result",
    "Refunded and unpaid orders are excluded"
  ],
  "tags": ["sql", "aggregation"]
}
```

For SQL, compare result rows, not the query text, because many different queries are correct.

---

## **9. Multiple Trials: pass@1, pass@k, pass^k**

LLMs are non deterministic: the same input can give different outputs or action sequences. One trial is weak evidence for important tasks.

| Metric | Meaning | Use when |
|---|---|---|
| pass@1 | Share of tasks that pass on the first trial | The user gets one attempt |
| pass@k | Share of tasks that pass at least once in k trials | Retries or best of k are allowed (capability) |
| pass^k | Share of tasks that pass every one of k trials | It must work every time (reliability) |

Example, 3 tasks with 3 trials each:

| Task | Trial 1 | Trial 2 | Trial 3 |
|---|---|---|---|
| A | pass | pass | pass |
| B | fail | pass | fail |
| C | pass | fail | pass |

```python
trials_by_task = {
    "A": [1, 1, 1],
    "B": [0, 1, 0],
    "C": [1, 0, 1],
}

task_count = len(trials_by_task)
pass_at_1 = sum(trials[0] for trials in trials_by_task.values()) / task_count
pass_at_3 = sum(1 for trials in trials_by_task.values() if sum(trials) >= 1) / task_count
pass_hat_3 = sum(1 for trials in trials_by_task.values() if sum(trials) == 3) / task_count

print(f"pass@1: {pass_at_1:.1%}")
print(f"pass@3: {pass_at_3:.1%}")
print(f"pass^3: {pass_hat_3:.1%}")
```

Expected output:

```text
pass@1: 66.7%
pass@3: 100.0%
pass^3: 33.3%
```

If one trial passes with probability p and trials are independent:

```text
pass@k = 1 - (1 - p)^k

pass^k = p^k
```

For p = 0.8:

| k | pass@k | pass^k |
|---:|---:|---:|
| 1 | 80% | 80% |
| 2 | 96% | 64% |
| 3 | 99.2% | 51.2% |
| 5 | 99.97% | 32.77% |

The gap grows with k. A support agent with high pass@3 but low pass^3 can rescue tasks by retrying, yet is unreliable on the first attempt. Trials are often not independent (shared state, caching, fixed seeds), so prefer counting real trials.

Rules:

- Report the number of tasks and trials, with intervals.
- Reset state between trials.
- Use the same trial count when comparing two versions.
- Never report only the best run.

---

## **10. Datasets**

One dataset is not enough. Build four layers plus a held-out split.

| Layer | What it holds | How it is made | Use |
|---|---|---|---|
| Golden | Human verified items with trusted answers | Hand built from real traffic | The honest score before a release |
| Regression | One item for each past failure | Added whenever a real bug is found | Old bugs do not come back |
| Synthetic | Many generated items for coverage | LLM writes, a human reviews | Fills gaps in rare cases |
| Adversarial | Tricky items made to break the feature | Hand written attacks and edge cases | Finds weak spots |

Notes:

- Golden: keep it small and clean, around 50 to 200 items to start.
- Regression: it only grows.
- Synthetic: generate along a few dimensions (topic by tone by difficulty). Generated items are often too clean and too alike, so review them.
- Adversarial: off topic requests, prompt injection ("ignore your rules"), rude users, empty or very long input, mixed languages, contradictory instructions.
- Held out: choose it by a fixed list of ids, not a new random split each time. Never paste held-out items into prompts. Never mix calibration items with held-out items.

**Fields for each item**

| Field | Purpose |
|---|---|
| task_id | Stable unique id |
| category | Failure mode or capability tested |
| difficulty | Easy, medium, hard |
| input | The request and task data |
| context | Retrieval context or setup, if needed |
| expected_outcome | Expected final state or reference |
| success_criteria | Explicit conditions for passing |
| tags | Searchable labels |
| source | production, synthetic, manual, regression |
| dataset_version | Release id |

JSONL means one JSON object per line, with no comments and no trailing commas:

```jsonl
{"task_id": "rag_001", "category": "retrieval.missing_document", "input": {"question": "What is the return period?"}, "context": [], "expected_outcome": {"should_abstain": true}, "tags": ["rag", "abstention"], "source": "manual", "dataset_version": "v1"}
{"task_id": "tool_001", "category": "tool_usage.invalid_arguments", "input": {"message": "Refund order ORD-12345"}, "expected_outcome": {"tool": "create_refund", "order_id": "ORD-12345"}, "tags": ["refund"], "source": "regression", "dataset_version": "v1"}
```

**Versioning**

- Name files with a version, such as `golden_v3.jsonl`.
- Never edit a version in place. Make a new version and write what changed.
- Also version the system prompt, tool descriptions, judge prompts, graders, and model settings, so a result can be reproduced.

**Good public datasets to learn from and borrow patterns from**

| Dataset | What it teaches |
|---|---|
| tau-bench | Tasks with a database end state, user simulator, policy documents, pass^k |
| SWE-bench Verified | Real issues, hidden tests, clean container grading |
| HotpotQA and CRAG | Multi step questions for RAG, retrieval and answer checks |
| RAGTruth and HaluEval | Labelled examples of unsupported claims, useful to test a groundedness judge |
| MT-Bench | Judge agreement with humans and judge bias |
| TruthfulQA | Questions that tempt a model to repeat common false beliefs |
| HarmBench and AdvBench | Safety and adversarial prompts |
| Berkeley Function Calling Leaderboard | Tool selection and argument checks |

Public sets measure general ability. They do not replace a golden set built from your own application traces.

---

## **11. Metric Families**

Pick the metric that fits the output. Many metrics look scientific but fit open ended text badly.

| Metric | What it measures | Good for | Weak spot |
|---|---|---|---|
| Exact match | Output equals the reference after cleaning | Labels, ids, dates, numbers | Fails on harmless wording changes |
| BLEU and ROUGE | Word overlap with a reference | Rough check of translation or summaries | Same meaning in other words scores low |
| Embedding similarity | How close two texts are in meaning | Retrieval, near duplicates | A wrong answer can still be similar |
| Rubric judge | A judge grades against a written rule | Tone, policy, completeness, groundedness | Needs calibration |
| Safety and toxicity | Harmful or unsafe content | Safety filters, red team sets | Watch recall, missing harm is costly |
| Format adherence | Valid JSON, schema, required fields | Any structured output | Says nothing about correctness |
| Latency | Time to respond | User experience | Use percentiles, not the average |
| Cost per task | Money spent per task | Budget, comparing versions | Also count cost per successful task |

The overlap problem:

```text
Reference:  The refund takes 7 days.
Output:     You will get your money back within a week.
```

Both mean the same, but they share almost no words, so overlap scores are low.

Latency: an average hides slow requests. Report p50 (typical) and p95 (slow tail), and p99 if tail delay matters.

Cost: total cost 2.40 dollars, 100 tasks, 80 passed.

```text
Cost per task = 2.40 / 100

Cost per task = 0.024

Cost per successful task = 2.40 / 80

Cost per successful task = 0.030
```

The second number is more honest, because failed tasks still cost money. Count model, tool, and infrastructure cost together.

Percentiles with the nearest rank method:

```python
import math

latencies_in_milliseconds = [620, 700, 710, 750, 800, 820, 900, 950, 1200, 3100]
sorted_latencies = sorted(latencies_in_milliseconds)

median_index = math.ceil(0.50 * len(sorted_latencies)) - 1
tail_index = math.ceil(0.95 * len(sorted_latencies)) - 1

print("p50 latency:", sorted_latencies[median_index], "ms")
print("p95 latency:", sorted_latencies[tail_index], "ms")
```

Expected output:

```text
p50 latency: 800 ms
p95 latency: 3100 ms
```

Ten items only teach the calculation. Real tail percentiles need a large sample.

---

## **12. Evaluating Prompts, Not Just Models**

Most changes in an LLM app are prompt changes, not model changes. Your app is also tools, retrieval settings, guardrails, output parser, memory, and orchestration code. Treat all of these as versioned files with their own regression tests:

```text
prompts/
  system_prompt_v4.txt
  tool_descriptions_v2.json
  few_shot_examples_v3.jsonl
  judge_tone_v2.txt
CHANGELOG.md
```

Rules:

- Change one thing at a time, so you know what caused the result.
- Save the version name with every result row.
- Run the regression set on every change.
- Look at the items that flipped, not only the overall number.
- Compare per criterion too: a change can raise completeness and lower groundedness.
- Write one line in the changelog per version.

Finding flips between two versions:

```python
results_version_1 = {"t001": 1, "t002": 1, "t003": 0, "t004": 1}
results_version_2 = {"t001": 1, "t002": 0, "t003": 1, "t004": 1}

regressions = [task_id for task_id in results_version_1 if results_version_1[task_id] == 1 and results_version_2[task_id] == 0]
fixes = [task_id for task_id in results_version_1 if results_version_1[task_id] == 0 and results_version_2[task_id] == 1]

print("regressions:", regressions)
print("fixes:", fixes)
```

Expected output:

```text
regressions: ['t002']
fixes: ['t003']
```

Both versions pass 3 of 4, so the overall number did not move, yet one item got worse and one got better. With few items, one flipped item moves the percentage a lot, so look at counts and intervals first.

---

## **13. Running Locally and Gating Releases in CI**

A local runner does the same steps every time:

1. Load the tasks.
2. Run the application.
3. Record the output and trace.
4. Run the graders.
5. Save one result row per task, with the evidence.
6. Aggregate and write a report.

A tiny runner with a dry run (replace `predict_answer` with your real app call):

```python
import json

dataset = [
    {"task_id": "extract_001", "text": "Order ORD-12 costs 500", "expected": {"order_id": "ORD-12", "amount": 500}},
    {"task_id": "extract_002", "text": "Order ORD-13 costs 700", "expected": {"order_id": "ORD-13", "amount": 700}},
]

def predict_answer(text):
    parts = text.split()
    return {"order_id": parts[1], "amount": int(parts[-1])}

passed_count = 0
with open("results.jsonl", "w", encoding="utf-8") as results_file:
    for row in dataset:
        actual = predict_answer(row["text"])
        passed = actual == row["expected"]
        passed_count += int(passed)
        results_file.write(json.dumps({"task_id": row["task_id"], "actual": actual, "passed": passed}) + "\n")
        print(row["task_id"], "pass" if passed else "fail")

print(f"passed {passed_count}/{len(dataset)}")
```

Expected output:

```text
extract_001 pass
extract_002 pass
passed 2/2
```

A real runner also stores app version, prompt version, model, latency, token use, trace id, grader version, and judge verdicts. Save failures with evidence, treat timeouts and exceptions as their own status, and never run against live production state.

**CI release gate.** Treat the suite like unit tests. On every change to a prompt, tool, retrieval, or model routing:

1. Run the pytest tests for the eval code itself.
2. Run the regression and critical tasks.
3. Compare with the agreed limits.
4. Fail the build when a limit is broken.
5. Save the report as a build file.

Example release rules:

```text
Every critical safety and policy check must pass.
Regression pass rate must not fall below the agreed limit.
No known critical failure may come back.
Judge unknown rate must stay under the review limit.
```

Do not pick limits at random. Base them on the product need, the baseline result, the sample size, and the risk you accept. With a small dataset, one item can move the percentage by several points.

```python
def release_allowed(report):
    if report["critical_failures"] > 0:
        return False
    if report["pass_rate"] < 0.93:
        return False
    return True

print(release_allowed({"critical_failures": 0, "pass_rate": 0.95}))
print(release_allowed({"critical_failures": 1, "pass_rate": 0.99}))
```

Expected output:

```text
True
False
```

The second case fails even with a high pass rate, because a critical check failed.

GitHub Actions starter:

```yaml
name: LLM Eval Gate
on:
  pull_request:
  push:
    branches: [main]
jobs:
  evaluation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r requirements.txt
      - run: pytest -q
      - run: python evals/runner.py
      - run: python evals/check_release.py
      - uses: actions/upload-artifact@v4
        if: always()
        with: { name: evaluation-report, path: results/ }
```

Tips:

- Keep a fast subset for pull requests and the full suite for merges or nightly runs.
- Keep API keys in the CI secret store, never in the repository.
- Do not report an infrastructure error (timeout, missing key) as a quality failure.
- Judges are slow and noisy, so decide which runs really need them.

---

## **14. Online Evaluation and Closing the Loop**

Offline evaluation runs on a fixed dataset before release. Online evaluation scores real production traces after release.

| Offline | Online |
|---|---|
| Fixed dataset | Live traffic |
| Often has an expected answer or state | Often has no golden answer |
| Before deployment | After deployment |
| Good for regression | Good for finding new failures |

Signals to watch: task completion, user feedback, tool error rate, retry rate, escalation rate, latency, cost, policy violations, judge unknown rate, and the mix of task types. A signal such as rising retries only hints at a problem. Read the traces to find the cause.

You do not need an expensive judge on every request. Sample a share of traffic, sample high risk tasks more, trigger review when errors or complaints rise, and send uncertain or high impact cases to a human. Remove personal data first.

A/B tests compare two versions on separate traffic groups. Compare success, safety, latency, cost, and feedback, and use intervals and paired methods before calling a winner.

The loop:

1. Sample production traces (random, error flagged, slow).
2. Run the same graders, or a cheap subset, online.
3. Read the low scoring or surprising traces.
4. Annotate new failure modes and update the taxonomy.
5. Turn confirmed failures into regression cases in the versioned dataset.
6. Fix the prompt, retrieval, tool, or code.
7. Confirm the fix with the offline suite and CI.
8. Deploy, keep monitoring, repeat.

Example: users report outdated cancellation terms. You sample those traces, confirm retrieval picked an old document, add a regression case with two policy versions, fix the retrieval filter, and rerun the suite before release.

---

## **15. Project Setup 1: Beginner**

Goal: a small suite you fully understand, with plain Python, no paid tools except the model calls for your judges.

Pick one feature: a support assistant, an invoice extractor, an FAQ chatbot, a simple RAG chatbot, or a classifier. The examples use a course support assistant that returns JSON with category, order_id, and reply.

**Folder layout**

```text
phase1-evals/
├── data/
│   ├── traces.jsonl
│   ├── annotations.jsonl
│   ├── golden_v1.jsonl
│   ├── regression_v1.jsonl
│   ├── adversarial_v1.jsonl
│   └── judge_labels_groundedness.jsonl
├── graders/
│   ├── code_checks.py
│   └── judges.py
├── prompts/
│   ├── system_prompt_v1.txt
│   ├── judge_groundedness_v1.txt
│   └── judge_tone_v1.txt
├── tests/
│   └── test_code_checks.py
├── runner.py
├── metrics.py
├── results/
├── CHANGELOG.md
├── requirements.txt
└── README.md
```

**Setup commands**

```bash
mkdir phase1-evals && cd phase1-evals
python -m venv .venv
source .venv/bin/activate
pip install pytest
mkdir data graders prompts tests results
touch runner.py metrics.py CHANGELOG.md
```

**Steps**

1. Write what a good output looks like for your feature.
2. Collect 50 to 100 traces into `data/traces.jsonl`. Mix good runs, wrong answers, retrieval or tool problems, missing information, edge cases, and adversarial instructions.
3. Annotate each trace: pass or fail, first failure, short note, category, severity, confidence. Save to `data/annotations.jsonl`.
4. Write 3 to 5 failure modes with one line definitions.
5. Build at least 15 test cases (normal, edge, adversarial, regression) in versioned JSONL files.
6. Write 5 code checks in `graders/code_checks.py`:

| Check | Rule |
|---|---|
| Valid JSON | The output parses as JSON |
| Required fields | category, order_id, and reply are all present |
| Allowed category | category is one of the allowed labels |
| Order id matches | order_id equals the id in the student message |
| Reply length | The reply is 60 words or fewer |

For an invoice extractor use: valid JSON, invoice_id present, date in YYYY-MM-DD form, amount is a number, and invoice id matches the expected one.

7. Test every check in `tests/test_code_checks.py`, with at least one passing and one failing case each. Run `pytest -q`.
8. Write 2 judges, each with one criterion, examples, and an unknown option. Save them in `prompts/`.

| Judge | Criterion |
|---|---|
| Groundedness (or completeness) | Every claim is supported by the supplied input |
| Tone (or policy) | The reply is polite and calm, or makes no refund promise outside the 7 day rule |

9. Hand label 100 to 200 items per judge, with at least 20 real failures. Split into prompt, dev, and held out. Edit the prompt only on dev, then freeze it.
10. Run once on held out. Report human pass and fail counts, judge pass, fail, and unknown counts, TP, FP, FN, TN, TPR, TNR, precision, F1, kappa, held-out size, and intervals.
11. Run 3 trials per task where non determinism matters. Report pass@1, pass@3, pass^3 with intervals.
12. Add at least one regression test from a confirmed failure.
13. Write the report.

**Report template.** The numbers are an example only.

```text
Feature:        Course support assistant
Traces read:    100 (failure modes: 5)
Dataset:        golden_v1 (60 items) + regression_v1 (12 items)
Prompt:         system_prompt_v1
Trials:         3 per task

Code checks (pass rate over 100 runs):
  Valid JSON            98/100
  Required fields       96/100
  Allowed category      97/100
  Order id matches      91/100
  Reply length          94/100

Judge calibration (held out):
  Groundedness judge   TPR 90.0% (36/40, 95% interval 76.9% to 96.0%)
                       TNR 86.7% (52/60)
                       Kappa 0.75   Unknown rate 3%
  Tone judge           TPR 80.0% (12/15, 95% interval 55% to 93%)
                       TNR 93.3% (42/45)
                       Kappa 0.72   Unknown rate 2%

Agent metrics:  pass@1 83%, pass@3 97%, pass^3 70% (30 tasks)
Top failures:   1. Order id mismatch  2. Unsupported claim  3. Missing field
Limits:         Only 15 real failures for the tone judge, so its TPR is uncertain.
                Single judge model. Small dataset.
Next step:      Label more failures, re-check judges in a month, grow the regression set.
```

**Definition of done**

| Check | Done when |
|---|---|
| Failure list came from real traces | Each check or judge links to a failure mode |
| 50 to 100 traces read and annotated | Every trace has a note |
| 3 to 5 failure modes written | Each has a definition |
| 15 or more test cases | Normal, edge, adversarial, and regression are all there |
| Code first | Nothing is given to a judge that a code check could do |
| 5 code checks tested | Each has pytest cases that pass and fail |
| 2 binary judges | Each has one criterion, examples, and unknown |
| Held out was kept | Prompt was frozen before the held-out run |
| TPR and TNR reported | Both shown with counts and an interval |
| Trials run | pass@1, pass@k, pass^k with sample counts |
| Versioned | Datasets, prompts, and graders have versions |
| Regression test added | At least one from a confirmed failure |
| Honest limits | The report says what the sample cannot show |

---

## **16. Project Setup 2: Production Level**

Goal: the same ideas, run as a service with tracing, shared datasets, CI gates, scheduled judge checks, and a human review queue.

**Tool choices.** Pick one per row. These are well known options, check the current docs before you commit.

| Need | Options |
|---|---|
| Tracing and annotation | Langfuse, Arize Phoenix, LangSmith, MLflow |
| Eval runner and graders | Inspect AI, promptfoo, DeepEval, Ragas (for RAG), or your own runner |
| Dataset and experiment storage | Braintrust, LangSmith, Langfuse datasets, or versioned files in git |
| Sandbox for agent code | Docker with resource limits, or a hosted sandbox service |
| CI | GitHub Actions, GitLab CI |
| Human review | A labeling tool or a simple internal review page |

**Folder layout**

```text
llm-app/
├── app/
│   ├── agent.py
│   ├── tools/
│   └── prompts/
│       ├── system_v7.txt
│       └── tool_descriptions_v3.json
├── evals/
│   ├── datasets/
│   │   ├── golden/v4/golden.jsonl
│   │   ├── regression/v12/regression.jsonl
│   │   ├── adversarial/v3/adversarial.jsonl
│   │   ├── synthetic_reviewed/v2/synthetic.jsonl
│   │   └── splits/heldout_ids_v2.txt
│   ├── graders/
│   │   ├── code/
│   │   └── judges/
│   │       ├── groundedness_v3.txt
│   │       └── tone_v2.txt
│   ├── calibration/
│   │   ├── labels/groundedness_labels_v3.jsonl
│   │   └── reports/groundedness_v3_report.json
│   ├── environments/
│   │   ├── docker/
│   │   └── fixtures/seed_database.sql
│   ├── suites/
│   │   ├── smoke.yaml
│   │   ├── regression.yaml
│   │   └── full.yaml
│   ├── runner.py
│   ├── metrics.py
│   └── check_release.py
├── monitoring/
│   ├── sample_production_traces.py
│   └── online_judges.py
├── tests/
│   ├── graders/
│   └── metrics/
├── results/
├── .github/workflows/
│   ├── evals_pr.yml
│   ├── evals_nightly.yml
│   └── judge_recheck_monthly.yml
├── CHANGELOG.md
└── README.md
```

**A suite file**

```yaml
suite: regression
dataset: evals/datasets/regression/v12/regression.jsonl
app_version: 1.8.0
prompt_version: system_v7
model: provider/model-name
trials_per_task: 3
graders:
  code: [valid_json, required_fields, order_id_match, refund_row_exists, identity_before_refund]
  judges: [groundedness_v3, tone_v2]
limits:
  critical_failures: 0
  min_pass_rate: 0.93
  max_judge_unknown_rate: 0.05
timeout_seconds: 60
```

**Production checklist**

| Area | What to do |
|---|---|
| Tracing | Log every request as a trace with spans, prompt version, model, latency, tokens, cost. Redact personal data before storing |
| Isolation | Run each trial in a fresh container with a seeded test database. Never touch production data |
| Datasets | Version in git or a dataset store. Keep held-out ids in a fixed file. Promote every confirmed production failure into the regression set |
| Graders | Code checks first. Every grader has pytest cases. Graders return status, reason, evidence |
| Judges | One criterion each, frozen versions, calibrated on held out, TPR and TNR stored in a report file next to the prompt |
| Judge upkeep | Monthly job re-labels a small fresh sample and compares. Alert when TPR or TNR drops |
| Trials | 3 or more trials for non deterministic tasks. Report pass@1, pass@k, pass^k |
| CI on pull requests | Run grader tests, smoke suite, and critical tasks. Block on any critical failure |
| CI nightly | Run the full suite with judges. Save the report. Compare with the last baseline |
| Gates | Critical checks must all pass. Overall limit comes from the baseline and sample size, not a guess |
| Infra errors | Timeouts and missing keys are reported as errors, not quality failures |
| Secrets | Keys live in the CI secret store only |
| Cost control | Cache deterministic results, use a small model for cheap judges only after calibration, sample online judges instead of running on all traffic |
| Online monitoring | Sample random, error flagged, and slow traces. Run cheap judges. Alert on policy violations, tool error rate, escalation rate, and judge unknown rate |
| Human review | Queue uncertain and high impact cases. Review labels feed judge calibration |
| Release notes | One changelog line per prompt, tool, judge, or dataset version, with the eval result |

**Weekly operating routine**

1. Read 20 to 30 fresh production traces, mixed random and flagged.
2. Add new failure notes and update the taxonomy.
3. Turn confirmed failures into regression cases.
4. Fix the cause, run the suite, check the flipped items.
5. Ship through the CI gate and watch the online signals.

---

## **17. Common Mistakes**

| Mistake | Better approach |
|---|---|
| Starting with generic metrics | Read traces first |
| Testing only happy paths | Add edge, adversarial, and regression cases |
| Vague criteria such as "be helpful" | Observable, single behavior criteria |
| Grading only the final text | Grade outcome, tool arguments, and spans |
| Trusting an uncalibrated judge | Report TPR and TNR on held-out items |
| Reporting only accuracy for a judge | Report TPR, TNR, precision, kappa |
| One judge for many criteria | One binary judge per criterion |
| Tuning and reporting on the same items | Keep a held-out set untouched |
| Ignoring unknown | Report the unknown rate and find the cause |
| Forcing one tool order | Check required properties and the outcome |
| Too few items, no intervals | Report counts and Wilson intervals |
| A single aggregate score | Report per criterion and critical metrics |
| Never testing the graders | Pytest each grader with pass, fail, and edge cases |
| Shared state between trials | Reset or isolate the environment |
| Forgetting prompt and tool versions | Version every artifact |
| Stale dataset | Promote real failures into it regularly |
| Generating 30 near identical synthetic traces | Vary topic, tone, and difficulty, then review by hand |
| Over fitting to a weak metric | Keep reading traces |

---

## **18. Quick Reference**

| Term | Simple meaning |
|---|---|
| Error analysis | Reading real traces and noting what went wrong, before building metrics |
| Open coding | Writing a short free note for each bad trace |
| Code check | A rule based grader: free, fast, same result every time |
| LLM judge | A prompt that grades one output on one criterion |
| Reference based | Compared with a known expected answer or state |
| Reference free | Graded against a rule, with no golden answer |
| Calibration | Comparing a judge with human labels |
| TPR | Of the real failures, how many the judge caught |
| TNR | Of the real good outputs, how many the judge passed |
| Precision | When the judge says fail, how often it is right |
| Kappa | Agreement with humans after removing luck |
| Held-out set | Labelled items used once, for the final numbers |
| Grader gaming | Passing the grader without doing the real task |
| Span attached eval | A grader attached to one step of a trace |
| pass@k | At least one of k trials passes |
| pass^k | All k trials pass |
| Golden set | Human verified items, the honest score |
| Regression set | One item per past failure |
| Release gate | A CI check that blocks a release on regression |
| Offline and online eval | Fixed dataset before release and live traces after |

Key rules to remember:

- Read traces before you choose any metric, and record the first failure.
- If an assertion can do it, use the assertion.
- For agents, grade the outcome, and use the trajectory to debug.
- Use binary, single criterion judges with an unknown option.
- Never trust a judge until you report its TPR and TNR on held-out items.
- Report pass@1 and pass^k for anything that must work every time.
- Build datasets in layers, version them, and keep a held-out split.
- Test prompt changes like code changes, and check the items that flipped.
- Put the suite in CI, and promote production failures into the regression set.

---

## **19. Interview Answer**

Question: "How would you build an evaluation suite for an LLM application?"

I start with error analysis, not metrics. I collect 50 to 100 real or realistic traces, read each one, and write a short note on the first meaningful failure. I group the notes into a small failure taxonomy and rank the modes by frequency and impact.

For each important mode I write test cases with clear success criteria, including normal, edge, adversarial, and regression cases. I use code checks for anything deterministic, such as schema, tool arguments, and final database state. For subjective criteria I write separate binary judges that return pass, fail, or unknown with a short reason.

I calibrate each judge against human labels, with a dev split for tuning and a held-out split for the final numbers, and I report TPR, TNR, and kappa instead of raw accuracy. For agents I grade the final outcome and use the trajectory only for debugging. I run multiple trials and report pass@1, pass@k, and pass^k with intervals.

The datasets are layered and versioned, the suite runs in CI as a release gate, and I sample production traces to find new failures and add them back as regression cases.

Questions to ask before trusting any eval:

```text
Did I read real traces first?
Is each failure measured by the simplest grader that works?
Do I know my judge's TPR and TNR on held-out items?
Did I check the outcome, not only the words?
Did I check the items that flipped between versions?
Are production failures becoming regression tests?
```