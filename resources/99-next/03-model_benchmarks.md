# **Phase 2 Notes: Testing AI Models, Reading Benchmarks, and Building a Test Suite**

Phase 1 taught you to test an application. Phase 2 goes one level further. You learn to:

- judge the AI models themselves,
- read public score tables without being fooled,
- compare models on your own task,
- keep a set of tests that catches things that used to work and now break.

Everything uses one running example so the pieces connect.

**Running example: BookNest SQL Assistant.** BookNest is an imaginary online shop. The assistant turns a staff question such as "How many orders were placed in March?" into a database query written in SQL (the language used to ask databases questions). We test it against a small SQLite database (a tiny database that lives inside Python and needs no server). All data is made up, and every example file says so.

**The main idea of this phase:** public score tables (benchmarks) help you pick a shortlist of models. Your own tests on your own task decide which model you actually use. A high rank on a leaderboard is a starting point, never a final answer.

**A warning before you install anything:** tool and library names and versions change quickly in this field. Always check the current version and install command first.

---

## **1. Words You Need**

Each term is explained once here. Later sections use the plain meaning.

| Term | Plain meaning |
|---|---|
| Model test | A test of the AI model alone: what can it do in general? |
| Application test | A test of your whole product: model + instructions + data + code |
| Benchmark | A fixed public set of questions with a fixed way of scoring, used to compare models |
| Contamination | Test questions or answers leaked into what the model learned from, so it may have "seen the exam" |
| Saturation | Top models score so high that the test can no longer tell them apart |
| Overfitting to a test | Tuning a model or prompt until it scores well on the test, not on the real task |
| Test before release (offline) | Running stored test cases before you ship |
| Test after release (online) | Measuring real user traffic once the feature is live |
| Automatic rule check | A rule written in code, such as "the SQL runs and returns the right rows" |
| AI grader (LLM judge) | One model that grades another model's answer using a written checklist |
| Execution accuracy | For SQL: the generated query returns the same rows as the correct query |
| Gold answer | The known correct answer stored with a test case |
| Pass@1 | Share of tasks solved on the first try |
| Thinking effort setting | A setting that controls how long a "thinking" model reasons before answering |
| Thinking tokens | Hidden reasoning text. You are charged for it like normal output |
| Prompt caching | A discount when the start of your prompt is identical across requests |
| Batch mode | A cheaper but slower way to send many requests that do not need an instant reply |
| p95 latency | The time that 95 percent of requests finish within (a "nearly worst case" speed) |
| Regression | Something that worked before and now fails |
| Baseline | The saved result you compare every new run against |
| Gate | A rule in your automatic checks that blocks a change if scores fall too far |
| Drift | Real user inputs slowly changing away from what you tested |

---

## **2. Why "Try a Few Prompts and Ship" Fails**

Testing by feel means trying a few prompts, liking the answers, and shipping. It fails for three reasons:

- Two or three samples say almost nothing about thousands of future inputs.
- The same input can give different outputs on different runs.
- People remember the good answers and forget the bad ones.

### **A real failure: Air Canada**

In 2022 a customer asked the Air Canada website chatbot about bereavement fares (discounts after a death in the family). The chatbot said he could buy a full-price ticket and claim the discount afterward. The airline's real policy did not allow that. In February 2024 a Canadian tribunal (the British Columbia Civil Resolution Tribunal, case Moffatt v. Air Canada) ruled for the customer. It rejected the argument that the chatbot was a separate entity responsible for its own words.

The lesson: **your company owns what its model says.** The money was small. The precedent was not. Read the decision summary yourself and verify the details.

### **Ordinary software versus AI systems**

| Property | Normal function | AI system |
|---|---|---|
| Same input gives same output | Yes | Not guaranteed, even with randomness turned to zero (temperature 0) |
| One test proves a case | Yes | No. You need repeated runs |
| Failure looks like | A crash or an obviously wrong value | A fluent, confident, wrong answer |
| Test result | Pass or fail | A pass rate with some uncertainty |

### **Shared setup file for all examples**

Save this once as `shop_database.py`. Every later example imports it. It builds the BookNest orders table in memory and runs queries safely.

```python
import sqlite3


def build_shop_database():
    connection = sqlite3.connect(":memory:")
    connection.execute(
        "CREATE TABLE orders (order_id INTEGER, customer_id INTEGER, "
        "order_month TEXT, total_amount REAL, status TEXT)"
    )
    rows = [
        (1, 101, "2026-03", 40.0, "paid"),
        (2, 102, "2026-03", 25.5, "paid"),
        (3, 101, "2026-03", 60.0, "refunded"),
        (4, 103, "2026-04", 80.0, "paid"),
        (5, 104, "2026-04", 15.0, "paid"),
        (6, 102, "2026-04", 55.0, "cancelled"),
    ]
    connection.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", rows)
    return connection


def run_query(connection, sql_text):
    try:
        return sorted(connection.execute(sql_text).fetchall())
    except Exception as error:
        return "ERROR: " + str(error)
```

### **Practice run: one question, twenty tries**

A fake model gets the SQL right three times out of four. Its mistake is forgetting to filter on `status = 'paid'`. That is a query that runs fine but gives the wrong answer.

```python
import random
from shop_database import build_shop_database, run_query

random.seed(7)

connection = build_shop_database()
question = "What is the total revenue from paid orders in March 2026?"
gold_sql = (
    "SELECT SUM(total_amount) FROM orders "
    "WHERE order_month = '2026-03' AND status = 'paid'"
)
forgot_status_sql = (
    "SELECT SUM(total_amount) FROM orders WHERE order_month = '2026-03'"
)


def fake_model(question):
    return random.choice([gold_sql, gold_sql, gold_sql, forgot_status_sql])


expected_rows = run_query(connection, gold_sql)
number_of_runs = 20
pass_count = 0

for run_number in range(number_of_runs):
    generated_sql = fake_model(question)
    if run_query(connection, generated_sql) == expected_rows:
        pass_count += 1

print("Expected result:", expected_rows)
print("Passed", pass_count, "of", number_of_runs, "runs")
print("Pass rate:", pass_count / number_of_runs)
```

Expected output:

```text
Expected result: [(65.5,)]
Passed 16 of 20 runs
Pass rate: 0.8
```

A single quick check would have passed this feature most of the time.

### **Why several checks in a row catch more than you think**

Rule in words: the chance of passing all checks = the pass chance multiplied by itself once per check. For a feature that is right 75 percent of the time:

- Check 1: 0.75
- Check 2: 0.75 × 0.75 = 0.5625
- Check 3: 0.5625 × 0.75 = 0.421875
- Check 4: 0.421875 × 0.75 = 0.31640625
- Check 5: 0.31640625 × 0.75 = 0.2373

A feature that is right 75 percent of the time passes five checks in a row only about 24 percent of the time. Quality has to be measured as a rate over many cases, not judged from one or two tries.

---

## **3. Testing the Model vs Testing Your Product**

A model's general ability is not your product's quality. A model that scores well on exams can still write bad SQL for your table layout. Your product also includes the instructions you give it, the data you feed it, the tools it uses, and the code that handles its output.

| | Model test | Application test |
|---|---|---|
| What is tested | The model alone | The whole product path |
| Who needs it | Model builders, people shortlisting models | Anyone shipping a feature |
| Typical data | Public benchmarks | Your own cases |
| Question it answers | "Is this model generally strong?" | "Does my feature work for my users?" |

### **The workflow (do the steps in this order)**

| Step | What you do | BookNest example |
|---|---|---|
| 1. Define the task | Write it in one sentence | Turn a staff question into one read-only SQL query |
| 2. Define success | Write what "good" means, with numbers | At least 85 percent correct, p95 latency under 4 seconds, under $8 per 1,000 requests |
| 3. Collect cases | Gather cases with correct answers | 50 questions with correct SQL |
| 4. Run | Run every case with identical settings | Same prompt and settings for all models |
| 5. Analyse | Find which kinds of cases fail | Failures cluster around "refunded" questions |
| 6. Improve | Change one thing, rerun, compare to the baseline | Add the allowed status values to the prompt, rerun |

Write the success numbers **before** you see any results. If you set the target after seeing scores, you will unconsciously pick a target your favourite model already meets.

---

## **4. Choosing How to Check an Answer**

Do not use one checking method for everything. Pick the cheapest method that can judge the behaviour reliably.

| Behaviour | Best method | Why | BookNest example |
|---|---|---|---|
| Exact, checkable facts or formats | Automatic rule check in code | Fast, free, repeatable | Does the SQL run and return the correct rows? |
| Meaning and quality | AI grader with a checklist | Code cannot judge meaning | Is the plain-English explanation of the result faithful? |
| Ambiguity, taste, safety edge cases | Human review | Humans set the standard | Is "best customers" answered sensibly? |
| Speed and money | Direct measurement | Measured automatically | p95 latency, tokens, dollars |

**Always start with automatic rule checks.** Comparing SQL text is a poor check, because two different queries can both be correct. Instead, run the query and compare the results. This is "execution accuracy".

### **Practice run: three automatic checks**

Notice that the first candidate fails the text match but is still correct. Notice also that the dangerous query is never run.

```python
from shop_database import build_shop_database, run_query

connection = build_shop_database()
gold_sql = "SELECT COUNT(*) FROM orders WHERE order_month = '2026-04'"
candidates = {
    "different wording": "SELECT COUNT(order_id) FROM orders WHERE order_month = '2026-04'",
    "wrong table name": "SELECT COUNT(*) FROM order WHERE order_month = '2026-04'",
    "dangerous query": "DELETE FROM orders WHERE order_month = '2026-04'",
}
forbidden_words = ["DROP", "DELETE", "UPDATE", "INSERT"]
gold_rows = run_query(connection, gold_sql)

for name, candidate_sql in candidates.items():
    exact_text_match = candidate_sql == gold_sql
    is_read_only = not any(word in candidate_sql.upper() for word in forbidden_words)
    if is_read_only:
        candidate_rows = run_query(connection, candidate_sql)
    else:
        candidate_rows = "NOT RUN"
    runs_without_error = not str(candidate_rows).startswith(("ERROR", "NOT RUN"))
    matches_gold = candidate_rows == gold_rows
    print(name, "| text match:", exact_text_match, "| read only:", is_read_only,
          "| runs:", runs_without_error, "| result match:", matches_gold)
```

Expected output:

```text
different wording | text match: False | read only: True | runs: True | result match: True
wrong table name | text match: False | read only: True | runs: False | result match: False
dangerous query | text match: False | read only: False | runs: False | result match: False
```

### **Rules for AI graders and human reviewers**

- Give the grader a short checklist with a clear pass or fail definition for each point.
- Use a model from a different company or family than the one being tested, when you can. Models tend to favour their own style.
- Have a person label about 30 to 50 outputs, then compare their labels with the grader's. If they agree on less than about 80 to 90 percent of cases, fix the checklist before trusting the grader.
- Use humans where answers are truly ambiguous. Do not use them for work that code can do.

---

## **5. Testing Before and After Release**

| | Before release (offline) | After release (online) |
|---|---|---|
| When | Before shipping, on every change | After shipping, on live traffic |
| Data | Stored, versioned cases | Real user inputs |
| Main job | Block bad releases and catch things that broke | Catch surprises and drift |
| Weakness | Cannot cover inputs you did not imagine | No correct answers on file, so it needs graders or user signals |

**Drift** means real inputs slowly change from what you tested. A new product line or a new slang term can break a feature that passed every test before release.

### **Two kinds of numbers. Keep them apart.**

| Kind | How you get it | Examples |
|---|---|---|
| System numbers | Captured automatically from every request | Speed, tokens in and out, error rate, cost |
| Quality numbers | Worked out by a grader, rule, or human | Correct result, made-up column name, relevance |

### **The after-release pipeline**

Log every request, sample some, score the sample, show a dashboard, set alerts, and feed failures back into the before-release test set. That last step is what makes the test set smarter over time.

### **Practice run: logs, numbers, alert, and feedback**

Ten fake requests. Rule for "p95" in words: sort the values, then take the position equal to 0.95 times the count, rounded up.

- Count of requests = 10
- Position for p95 = 0.95 × 10 = 9.5, rounded up = 10
- The tenth smallest time is 6.5 seconds
- So p95 latency = 6.5 seconds. With only ten requests, p95 equals the slowest one. Use far more requests on real dashboards.

```python
import math

logged_requests = [
    {"request_id": "r01", "latency_seconds": 1.1, "total_tokens": 400, "had_error": False, "judge_score": 1},
    {"request_id": "r02", "latency_seconds": 0.9, "total_tokens": 380, "had_error": False, "judge_score": 1},
    {"request_id": "r03", "latency_seconds": 1.4, "total_tokens": 450, "had_error": False, "judge_score": 0},
    {"request_id": "r04", "latency_seconds": 1.0, "total_tokens": 410, "had_error": False, "judge_score": 1},
    {"request_id": "r05", "latency_seconds": 6.5, "total_tokens": 900, "had_error": True, "judge_score": 0},
    {"request_id": "r06", "latency_seconds": 1.2, "total_tokens": 420, "had_error": False, "judge_score": 1},
    {"request_id": "r07", "latency_seconds": 1.3, "total_tokens": 430, "had_error": False, "judge_score": 1},
    {"request_id": "r08", "latency_seconds": 1.1, "total_tokens": 390, "had_error": False, "judge_score": 1},
    {"request_id": "r09", "latency_seconds": 2.0, "total_tokens": 520, "had_error": False, "judge_score": 0},
    {"request_id": "r10", "latency_seconds": 1.0, "total_tokens": 405, "had_error": False, "judge_score": 1},
]

latencies = sorted(item["latency_seconds"] for item in logged_requests)
rank_for_p95 = math.ceil(0.95 * len(latencies))
p95_latency = latencies[rank_for_p95 - 1]
error_rate = sum(item["had_error"] for item in logged_requests) / len(logged_requests)
quality_rate = sum(item["judge_score"] for item in logged_requests) / len(logged_requests)

print("p95 latency (seconds):", p95_latency)
print("error rate:", error_rate)
print("quality rate:", quality_rate)

if quality_rate < 0.85:
    print("ALERT: quality below 0.85")

failed_requests = [item for item in logged_requests if item["judge_score"] == 0]
offline_cases_to_review = [item["request_id"] for item in failed_requests]
print("Send to offline set for review:", offline_cases_to_review)
```

Expected output:

```text
p95 latency (seconds): 6.5
error rate: 0.1
quality rate: 0.7
ALERT: quality below 0.85
Send to offline set for review: ['r03', 'r05', 'r09']
```

Two things to notice. The alert fires on a quality number, not a system number. And the failed requests are listed for review, so a person can turn them into new test cases with correct answers.

---

## **6. How Benchmarks Work and How They Mislead**

### **Five parts of every benchmark**

| Part | What it is | What can go wrong |
|---|---|---|
| Questions | The questions or tasks | Wrong correct-answers, narrow coverage |
| Prompts | The exact wording and examples given to the model | Small wording changes move scores |
| Run settings | Randomness, tool access, turn limits, retries | Easy to change quietly |
| Scoring method | Exact match, tests, or a grader | A bad grader marks correct answers wrong |
| Combining scores | How scores become one number | Averages hide weak areas |

### **Four pitfalls**

| Pitfall | Meaning | Defence |
|---|---|---|
| Contamination | Test items were in the training data | Prefer held-back or private sets. Run your own private tests |
| Saturation | Everyone scores near the top | Look at harder benchmarks. Stop using the old one to rank models |
| Overfitting to the test | Training or tuning to the test | Never tune on your test set. Keep a hidden part |
| Settings gaming | Better settings, more turns, more attempts, or a custom scaffold produce a higher score | Compare only like for like. Ask for the full settings |

### **Practice run: a simple contamination check**

If long word sequences from a test question appear in some text, that text may have been seen during training. This tool checks 5-word sequences (called 5-grams).

```python
def word_ngrams(text, size):
    words = text.lower().split()
    return {" ".join(words[start:start + size]) for start in range(len(words) - size + 1)}


benchmark_question = "What is the total revenue from paid orders in March for the shop"
training_snippets = {
    "snippet_copy": "forum post: what is the total revenue from paid orders in March for the shop answer is sum",
    "snippet_related": "a tutorial about summing order totals by month in SQL",
}

question_ngrams = word_ngrams(benchmark_question, 5)

for name, snippet_text in training_snippets.items():
    snippet_ngrams = word_ngrams(snippet_text, 5)
    shared_count = len(question_ngrams & snippet_ngrams)
    overlap_fraction = shared_count / len(question_ngrams)
    print(name, "shared 5-grams:", shared_count, "overlap:", round(overlap_fraction, 2))
```

Expected output:

```text
snippet_copy shared 5-grams: 9 overlap: 1.0
snippet_related shared 5-grams: 0 overlap: 0.0
```

A full overlap means the question text is already out in the open. Real checks compare against your own data and public web text. They are rough, so treat a high overlap as a warning, not proof.

### **Is a score gap real, or just noise?**

Two models score 82 and 78 correct out of 100. Formula in words: standard error = square root of (accuracy × (1 minus accuracy) ÷ number of cases).

- Model A: accuracy 0.82. Then 0.82 × 0.18 = 0.1476. Then 0.1476 ÷ 100 = 0.001476. Square root = 0.0384.
- Model B: the same steps give accuracy 0.78 and standard error 0.0414.
- Gap = 0.82 − 0.78 = 0.04
- Error of the gap = square root of (0.0384 squared + 0.0414 squared) = 0.0565
- 95 percent margin = 1.96 × 0.0565 = 0.1107

The gap of 0.04 is smaller than the margin of 0.11. On 100 cases you cannot say Model A is better.

```python
import math


def accuracy_with_error(correct_count, total_count):
    accuracy = correct_count / total_count
    standard_error = math.sqrt(accuracy * (1 - accuracy) / total_count)
    return accuracy, standard_error


accuracy_a, error_a = accuracy_with_error(82, 100)
accuracy_b, error_b = accuracy_with_error(78, 100)

gap = accuracy_a - accuracy_b
error_of_gap = math.sqrt(error_a ** 2 + error_b ** 2)
margin = 1.96 * error_of_gap

print("Model A accuracy:", round(accuracy_a, 3), "standard error:", round(error_a, 4))
print("Model B accuracy:", round(accuracy_b, 3), "standard error:", round(error_b, 4))
print("Gap:", round(gap, 3))
print("Error of gap:", round(error_of_gap, 4))
print("95 percent margin:", round(margin, 4))
print("Gap larger than margin:", gap > margin)
```

Expected output:

```text
Model A accuracy: 0.82 standard error: 0.0384
Model B accuracy: 0.78 standard error: 0.0414
Gap: 0.04
Error of gap: 0.0565
95 percent margin: 0.1107
Gap larger than margin: False
```

Rules: a small test set cannot separate close models. Report the margin next to every score. More cases shrink the margin slowly: you need about four times the cases to halve it.

---

## **7. General-Knowledge Benchmarks (From Easy to Hard)**

Benchmarks keep getting harder because models keep maxing out the old ones. Each new test was built to fix a weakness of the previous one. Counts below are approximate. Verify them on each benchmark's page before quoting them.

| Benchmark | Idea | What it fixed or why it exists | Weakness today |
|---|---|---|---|
| MMLU | About 16,000 multiple-choice questions across 57 subjects | A broad knowledge test | Maxed out. Some questions have wrong answers. Likely contaminated |
| TruthfulQA | Questions where people often believe falsehoods | Tests whether a model repeats common myths | Narrow. Models can learn its style |
| AGIEval | Real human exams such as law and admission tests | Tests exam-style reasoning that people actually take | Public text, so contamination risk |
| GPQA | Graduate-level science questions written to resist web search (use the "Diamond" subset) | Hard even for experts outside the field | Small size, so large noise |
| MMLU-Pro | MMLU with harder questions and ten answer options | Reduces lucky guessing and maxing out | Still multiple choice |
| SimpleQA | Short fact questions with one clear answer, graded correct, wrong, or not attempted | Measures factual accuracy and honest "I do not know" | Narrow kind of fact. Tests facts, not reasoning |
| Humanity's Last Exam | Very hard questions from experts across many fields | Built because the others were maxed out | Costly to build. Some items may be flawed. Expect maxing out later |

**How to use this ladder.** Use the harder tests to separate top models. Do not use any of them to predict your task. If a model leads on GPQA but writes poor SQL in your own test, believe your own test.

---

## **8. Coding Benchmarks (From Easy to Hard)**

| Benchmark | Idea | Status |
|---|---|---|
| HumanEval | 164 small Python function problems | Maxed out years ago. Fine only for a quick check |
| SWE-bench (original, 2023) | Real GitHub issues from 12 Python projects. The model must fix the code | The starting point |
| SWE-bench Verified | 500 problems that humans checked were solvable | Became the standard. Now heavily contaminated |
| SWE-bench Pro | Longer tasks across many projects. Has public, held-back and private sets | Newer. Designed to reduce contamination |

### **What happened in 2026 (verify the latest news before citing any of this)**

- In February 2026 OpenAI said it stopped reporting SWE-bench Verified, citing contamination and flawed tests. In its review of 138 hard problems, most had material problems in the tests or descriptions. It recommended SWE-bench Pro instead.
- SWE-bench Pro has 1,865 tasks across 41 projects. Reported split: 731 public, 858 held-back, 276 private. Only the public set is open. A task counts as solved only if the new tests pass and the old tests still pass.
- In July 2026, according to secondhand reports of an OpenAI review, about 30 percent of the public Pro tasks were judged broken, and OpenAI withdrew its recommendation. The reminder: no benchmark stays trustworthy by itself.
- Leaderboard settings changed over time. Older entries used a 50-turn limit and a cost cap. Newer entries use a 250-turn limit and no cap. Scores rose partly because of that.

### **Your habit: compare the gap, not just the rank**

Take a model's score on an older benchmark and on a newer one. A large drop means the older score may have been helped by contamination.

```python
# Made up scores, only to show the method.
scores = {
    "model_a": {"older_benchmark": 85.0, "newer_benchmark": 40.0},
    "model_b": {"older_benchmark": 80.0, "newer_benchmark": 45.0},
    "model_c": {"older_benchmark": 75.0, "newer_benchmark": 30.0},
}

best_older_name = ""
best_older_score = -1.0
best_newer_name = ""
best_newer_score = -1.0

for model_name, result in scores.items():
    gap = result["older_benchmark"] - result["newer_benchmark"]
    ratio = result["newer_benchmark"] / result["older_benchmark"]
    print(model_name, "gap:", gap, "newer/older ratio:", round(ratio, 2))
    if result["older_benchmark"] > best_older_score:
        best_older_score = result["older_benchmark"]
        best_older_name = model_name
    if result["newer_benchmark"] > best_newer_score:
        best_newer_score = result["newer_benchmark"]
        best_newer_name = model_name

print("Top on older benchmark:", best_older_name)
print("Top on newer benchmark:", best_newer_name)
```

Expected output:

```text
model_a gap: 45.0 newer/older ratio: 0.47
model_b gap: 35.0 newer/older ratio: 0.56
model_c gap: 45.0 newer/older ratio: 0.4
Top on older benchmark: model_a
Top on newer benchmark: model_b
```

The top model changes between the two columns. The numbers are made up. The method is what matters.

### **Checklist before trusting a coding leaderboard score**

- Which part was used: public, held-back, or private?
- Which agent setup was used, and what turn and cost limits?
- What is the margin of error? Are two models inside each other's margin?
- What is the date? A score from six months ago may measure something different now.
- Does the model do the same on your own code? Run a small private test.

---

## **9. Testing "Thinking" Models**

A thinking model reasons before it answers. This changes how you test it.

| Rule | Why |
|---|---|
| Fix the thinking-effort setting for every run and write it down | Effort changes both score and cost. Setting names differ by provider, so read their docs |
| Track thinking tokens as their own number | They are charged as output and can be far larger than the visible answer |
| Run more trials per case | Thinking adds randomness, so single runs vary more |
| Report cost per correct answer, not only accuracy | A small gain can cost many times more |

### **Practice run: three effort settings, eight trials each**

The pass chances and token counts are made up to show the method. Formula in words: cost per correct answer = cost of one trial ÷ number of correct answers in one trial. Worked for low effort:

- Tokens for one trial = 300 tokens × 50 questions = 15,000
- Cost of one trial = 15,000 ÷ 1,000,000 × $10 = $0.15
- Correct answers in one trial = 0.598 × 50 = 29.9
- Cost per correct answer = $0.15 ÷ 29.9 = $0.005

```python
import random
import statistics

random.seed(3)

effort_settings = {
    "low": {"pass_chance": 0.60, "tokens_per_question": 300},
    "medium": {"pass_chance": 0.72, "tokens_per_question": 1200},
    "high": {"pass_chance": 0.76, "tokens_per_question": 4000},
}
questions_per_trial = 50
number_of_trials = 8
price_per_million_output_tokens = 10.0

for effort_name, setting in effort_settings.items():
    trial_scores = []
    for trial_number in range(number_of_trials):
        correct_count = 0
        for question_number in range(questions_per_trial):
            if random.random() < setting["pass_chance"]:
                correct_count += 1
        trial_scores.append(correct_count / questions_per_trial)
    mean_score = statistics.mean(trial_scores)
    spread = statistics.stdev(trial_scores)
    tokens_for_one_trial = setting["tokens_per_question"] * questions_per_trial
    cost_for_one_trial = tokens_for_one_trial / 1_000_000 * price_per_million_output_tokens
    cost_per_correct = cost_for_one_trial / (mean_score * questions_per_trial)
    print(effort_name, "| mean:", round(mean_score, 3), "| spread:", round(spread, 3),
          "| cost per correct answer: $", round(cost_per_correct, 4))
```

Expected output:

```text
low | mean: 0.598 | spread: 0.051 | cost per correct answer: $ 0.005
medium | mean: 0.725 | spread: 0.075 | cost per correct answer: $ 0.0166
high | mean: 0.738 | spread: 0.041 | cost per correct answer: $ 0.0542
```

Read it carefully. Medium effort gains about 13 points over low. High effort gains only about 1 more point and costs over three times as much per correct answer. The spread column shows why you need several trials: one trial at medium can differ from another by several points.

---

## **10. Comparing Models on Your Own Task**

This is the main skill of the phase. Steps in order:

### **Step 1. Shortlist using hard limits first**

| Filter | Question |
|---|---|
| Ability | Do public benchmarks suggest it can do this kind of task? |
| Speed | Is its typical response time inside your budget? |
| Memory size (context window) | Can the table layout and prompt fit? |
| Cost | Is the price per million tokens workable at your volume? |
| Other | Data policy, region, licence, whether it can run on your own machine |

Pick three models: one strong and expensive, one in the middle, one small and cheap. This gives you a real trade-off curve.

### **Step 2. Build your own dataset**

SQL is a good fit because correctness is checkable by running the query. Make 50 cases, each with a question, a correct query, and a category tag. Include easy cases, tricky cases such as status filters, and a few that should be refused. The builder script is in section 13.

### **Step 3. Compare like for like**

Same inputs, same prompt text, same randomness setting and limits, same scorer, same run date. Change only the model. Record everything in the run settings file.

### **Step 4. Estimate cost, including caching and batch mode**

BookNest sends the same table-layout text with every request. That repeated part can be cached. Prices below are made up. Check real prices and rules before use. Providers differ: some charge extra to store the cache, and caching needs a minimum prompt length.

Workload: 2,000 requests. Each has 1,000 shared prompt tokens, 500 unique input tokens and 100 output tokens. Large-model prices per million tokens: input $5.00, cached input $0.50, output $25.00. Batch mode gives 50 percent off.

Plain cost in words: input tokens × input price + output tokens × output price.

- Input tokens = (1,000 + 500) × 2,000 = 3,000,000
- Output tokens = 100 × 2,000 = 200,000
- Input cost = 3,000,000 ÷ 1,000,000 × $5.00 = $15.00
- Output cost = 200,000 ÷ 1,000,000 × $25.00 = $5.00
- Plain total = $15.00 + $5.00 = **$20.00**

With caching, the 1,000 shared tokens are billed at the cached price:

- Cached tokens = 1,000 × 2,000 = 2,000,000, cost = 2 × $0.50 = $1.00
- Fresh input tokens = 500 × 2,000 = 1,000,000, cost = 1 × $5.00 = $5.00
- Total with caching = $1.00 + $5.00 + $5.00 = **$11.00**

With caching and batch mode:

- Total = $11.00 × 0.5 = **$5.50**

```python
# Made up prices in dollars per million tokens. Check real prices before use.
models = {
    "large_model": {"input": 5.00, "cached_input": 0.50, "output": 25.00},
    "medium_model": {"input": 3.00, "cached_input": 0.30, "output": 15.00},
    "small_model": {"input": 1.00, "cached_input": 0.10, "output": 5.00},
}
request_count = 2000
shared_prompt_tokens = 1000
unique_input_tokens = 500
output_tokens = 100
batch_discount = 0.5

for model_name, price in models.items():
    plain_input_tokens = (shared_prompt_tokens + unique_input_tokens) * request_count
    cached_tokens = shared_prompt_tokens * request_count
    fresh_tokens = unique_input_tokens * request_count
    total_output_tokens = output_tokens * request_count

    plain_cost = (plain_input_tokens * price["input"] + total_output_tokens * price["output"]) / 1_000_000
    cached_cost = (cached_tokens * price["cached_input"] + fresh_tokens * price["input"]
                   + total_output_tokens * price["output"]) / 1_000_000
    batch_cost = cached_cost * batch_discount

    print(model_name, "| plain: $", round(plain_cost, 2), "| with cache: $", round(cached_cost, 2),
          "| cache + batch: $", round(batch_cost, 2))
```

Expected output:

```text
large_model | plain: $ 20.0 | with cache: $ 11.0 | cache + batch: $ 5.5
medium_model | plain: $ 12.0 | with cache: $ 6.6 | cache + batch: $ 3.3
small_model | plain: $ 4.0 | with cache: $ 2.2 | cache + batch: $ 1.1
```

Batch mode only fits work that can wait, such as nightly reports. It does not fit a chat box where staff wait for an answer.

### **Step 5. Choose the best trade-off, not the top ranking**

This practice run uses simulated outputs for six cases. Use the same layout for your real 50-case run.

```python
import statistics
from shop_database import build_shop_database, run_query

connection = build_shop_database()
gold_queries = [
    "SELECT COUNT(*) FROM orders WHERE order_month = '2026-03'",
    "SELECT COUNT(*) FROM orders WHERE order_month = '2026-04'",
    "SELECT SUM(total_amount) FROM orders WHERE status = 'paid'",
    "SELECT COUNT(DISTINCT customer_id) FROM orders WHERE order_month = '2026-03'",
    "SELECT AVG(total_amount) FROM orders WHERE order_month = '2026-04'",
    "SELECT COUNT(*) FROM orders WHERE status = 'refunded'",
]
# Simulated model behaviour: which case numbers each model gets wrong.
wrong_case_numbers = {
    "large_model": [4],
    "medium_model": [2, 5],
    "small_model": [1, 3, 4],
}
latency_seconds = {
    "large_model": [2.4, 2.1, 2.8, 2.2, 2.5, 2.3],
    "medium_model": [1.3, 1.1, 1.5, 1.2, 1.4, 1.2],
    "small_model": [0.6, 0.5, 0.7, 0.6, 0.5, 0.6],
}
cost_per_request_dollars = {"large_model": 0.0100, "medium_model": 0.0060, "small_model": 0.0020}

print("model        | accuracy | median latency | cost per 1000 requests")
for model_name in wrong_case_numbers:
    correct_count = 0
    for case_number, gold_sql in enumerate(gold_queries):
        generated_sql = gold_sql
        if case_number in wrong_case_numbers[model_name]:
            generated_sql = gold_sql.replace("2026-0", "2025-0").replace("'paid'", "'unpaid'")
            generated_sql = generated_sql.replace("'refunded'", "'unknown'")
        if run_query(connection, generated_sql) == run_query(connection, gold_sql):
            correct_count += 1
    accuracy = correct_count / len(gold_queries)
    median_latency = round(statistics.median(latency_seconds[model_name]), 2)
    cost_per_thousand = cost_per_request_dollars[model_name] * 1000
    print(model_name.ljust(12), "|", round(accuracy, 2), "    |", median_latency, "s         | $", cost_per_thousand)
```

Expected output:

```text
model        | accuracy | median latency | cost per 1000 requests
large_model  | 0.83     | 2.35 s         | $ 10.0
medium_model | 0.67     | 1.25 s         | $ 6.0
small_model  | 0.5     | 0.6 s          | $ 2.0
```

How to read it: the large model is the most accurate and the slowest, and costs five times the small one. If your target is 85 percent, none of the three passes yet. The right next step is to improve the prompt, not to pick the winner by default. If 67 percent were acceptable, the medium model would be the sensible choice.

---

## **11. Building a Test Suite That Catches Breakage**

### **Three levels of tests**

| Level | What it tests | BookNest example |
|---|---|---|
| Single part | One small piece | The SQL safety checker blocks DELETE |
| Several parts together | A chain of pieces | Table lookup + model + query runner |
| Whole product | The full user path | Staff question in, readable answer out |

Single-part tests are cheap and run on every change. Whole-product tests are costly and run before release.

### **Keep a record of everything**

A result is only meaningful if you can rebuild it.

| Item | How to record it |
|---|---|
| Test cases | Dataset version in the file name, plus git history |
| Prompts | Stored in files, tracked in git |
| Model | Exact model name and snapshot, not a nickname |
| Settings | A settings file saved with every run |
| Results | One results file per run, named by date and git commit |

### **Compare against a baseline**

The baseline is the last accepted result. Every run reports its change from the baseline for quality, speed and cost together.

### **Automatic gates**

Your team's automatic checks (often called CI) run whenever code changes. A gate blocks a change if the numbers cross a limit. Track all three numbers, because a gain in one can hide a loss in another.

Rule in words: increase = new value ÷ old value, minus 1. Worked example for speed:

- Ratio = 3.9 ÷ 3.0 = 1.3
- Increase = 1.3 − 1 = 0.3
- Allowed increase = 0.2
- 0.3 is above 0.2, so the gate fails. Accuracy fell only 0.01 and cost fell. A gate that watched quality alone would have let this slow release through.

```python
baseline = {"accuracy": 0.84, "p95_latency_seconds": 3.0, "cost_per_1000_requests": 6.0}
candidate = {"accuracy": 0.83, "p95_latency_seconds": 3.9, "cost_per_1000_requests": 5.5}

allowed_accuracy_drop = 0.02
allowed_latency_increase_fraction = 0.20
allowed_cost_increase_fraction = 0.10

failures = []

accuracy_drop = baseline["accuracy"] - candidate["accuracy"]
if accuracy_drop > allowed_accuracy_drop:
    failures.append("accuracy dropped by " + str(round(accuracy_drop, 3)))

latency_increase = candidate["p95_latency_seconds"] / baseline["p95_latency_seconds"] - 1
if latency_increase > allowed_latency_increase_fraction:
    failures.append("p95 latency rose by " + str(round(latency_increase, 2)))

cost_increase = candidate["cost_per_1000_requests"] / baseline["cost_per_1000_requests"] - 1
if cost_increase > allowed_cost_increase_fraction:
    failures.append("cost rose by " + str(round(cost_increase, 2)))

if failures:
    print("GATE FAILED")
    for failure in failures:
        print(" -", failure)
else:
    print("GATE PASSED")
```

Expected output:

```text
GATE FAILED
 - p95 latency rose by 0.3
```

### **Practical rules for gates**

- Use a small, fast set of tests on every proposed code change. Run the full set nightly.
- Repeat each case a few times and use the average, because runs vary.
- Set limits wider than the measured noise, or the gate will fail at random.
- When a gate fails and the change is actually right, update the baseline in a separate, reviewed commit.

---

## **12. Common Mistakes**

| Mistake | Why it hurts | Better approach |
|---|---|---|
| Trusting a public leaderboard rank | Benchmarks leak, max out, and depend on settings | Use leaderboards to shortlist. Decide with your own tests |
| Judging models on one run | Single runs vary | Repeat trials. Report the average and spread |
| Comparing models with different prompts or settings | You measure the setup, not the model | Identical inputs, prompts, settings and scorer |
| Comparing SQL or code as text | Correct answers get marked wrong | Run it and compare results |
| Using one number only | A quality gain can hide a cost or speed loss | Track quality, speed and cost together |
| Setting the pass target after seeing results | The target fits your favourite | Write success criteria first |
| Ignoring noise on small test sets | A 4-point gap on 100 cases is noise | Report margins. Add cases for close calls |
| Tuning on the test set | Scores rise without real improvement | Keep a hidden part. Tune only on a separate practice part |
| Using an unchecked AI grader | It may be biased or wrong | Compare to human labels first |
| Not logging thinking tokens | Cost surprises | Track them as a separate number |
| Never feeding live failures back | The suite stops matching reality | Review failures weekly. Add them as cases |
| Not labelling made-up data | You mislead your readers | Mark every file and report as simulated |

---

## **13. Project 1: Beginner**

**Project: BookNest SQL Model Shootout.** Pick three models, build a 50-case SQL dataset, run all three with identical settings, and publish a table of quality, speed and cost. This is the proof of learning for the phase.

### **About the data**

You do not need real customer data. The orders table is simulated. Label it honestly:

- Put `"data_source": "simulated"` in every test case.
- Put one line at the top of the README and the report: "All data in this project is simulated. Results show the method, not real business performance."
- Never describe simulated results as findings about real shops.

### **Public datasets to add realism (cite them)**

| Dataset or benchmark | What it gives you | Note |
|---|---|---|
| Spider | Many databases and questions for SQL | A classic. Models score high, so it is mostly for practice |
| BIRD | Larger, messier databases and harder questions | Closer to real work. Check the current leaderboard and rules |
| Spider 2.0 | Company-style, multi-step SQL tasks | Much harder. Good as a stretch goal |
| MMLU-Pro, GPQA Diamond, SimpleQA | General model benchmarks | Use only to shortlist models, not to judge SQL |
| SWE-bench Pro | Coding agent benchmark | Read its status first (section 8) |

### **Tool choices for beginners**

| Layer | Choice | Why |
|---|---|---|
| Model access | The provider's own Python kit, one script per provider | Fewest moving parts. You see exactly what is sent |
| Data storage | JSONL files in git (one JSON record per line) | Readable, easy to compare, versioned |
| Database | SQLite in memory | Built into Python. No server |
| Scoring | Plain Python run-and-compare check | Cheap, repeatable, no AI grader needed |
| Tests and gates | pytest | You may already know it |
| Settings | One YAML file | Easy to read and save with each run |
| Tracking | A results CSV committed to git | Enough for one person |

### **Folder layout**

```text
shop-sql-evals/
  README.md
  data/
    cases_v1.jsonl
  src/
    shop_database.py
    build_dataset.py
    run_models.py
    score_results.py
  configs/
    run_config.yaml
  results/
    2026-11-16_run_001.csv
  reports/
    report_001.md
  tests/
    test_scoring.py
```

### **Setup commands (verify package names and versions before installing)**

```text
mkdir shop-sql-evals
cd shop-sql-evals
python -m venv .venv
source .venv/bin/activate
pip install pytest pyyaml
pip install <the SDK for each model provider you chose>
git init
```

On Windows, activate the virtual environment with `.venv\Scripts\activate` instead of the `source` line.

### **Build order (do these in sequence)**

1. Write the one-sentence task and the success criteria (section 3).
2. Copy `shop_database.py` from section 2.
3. Build the dataset with the script below. It makes 50 simulated cases across ten categories.
4. Test the scorer on its own with pytest, using hand-written good and bad queries.
5. Write `run_models.py`. For each model and each case, send the same prompt and record the SQL, time taken, input tokens and output tokens.
6. Score every result by running the query and comparing rows. Repeat each case three times.
7. Work out accuracy with a margin, typical (p50) and near-worst (p95) speed, and cost per 1,000 requests.
8. Write the report using the template below.

### **Dataset builder script**

```python
import json

months = ["2026-03", "2026-04"]
statuses = ["paid", "refunded", "cancelled"]
customers = [101, 102, 103, 104]
cases = []


def add_case(category, question, gold_sql):
    cases.append({"category": category, "question": question, "gold_sql": gold_sql})


for month in months:
    add_case("count", f"How many orders were placed in {month}?",
             f"SELECT COUNT(*) FROM orders WHERE order_month = '{month}'")
    add_case("average", f"What was the average order value in {month}?",
             f"SELECT AVG(total_amount) FROM orders WHERE order_month = '{month}'")
    add_case("distinct", f"How many different customers ordered in {month}?",
             f"SELECT COUNT(DISTINCT customer_id) FROM orders WHERE order_month = '{month}'")
    add_case("extreme", f"What was the largest order in {month}?",
             f"SELECT MAX(total_amount) FROM orders WHERE order_month = '{month}'")
    add_case("extreme", f"What was the smallest order in {month}?",
             f"SELECT MIN(total_amount) FROM orders WHERE order_month = '{month}'")
    for status in statuses:
        add_case("revenue_by_status", f"What is the total amount of {status} orders in {month}?",
                 f"SELECT SUM(total_amount) FROM orders WHERE order_month = '{month}' AND status = '{status}'")
    for customer in customers:
        add_case("customer_month", f"How many orders did customer {customer} place in {month}?",
                 f"SELECT COUNT(*) FROM orders WHERE customer_id = {customer} AND order_month = '{month}'")

for customer in customers:
    for status in statuses:
        add_case("customer_status", f"How many {status} orders does customer {customer} have?",
                 f"SELECT COUNT(*) FROM orders WHERE customer_id = {customer} AND status = '{status}'")

add_case("overall", "How many orders exist in total?", "SELECT COUNT(*) FROM orders")
add_case("overall", "How many different customers exist?", "SELECT COUNT(DISTINCT customer_id) FROM orders")

for month in months:
    for threshold in [20, 50, 70]:
        add_case("threshold", f"How many orders in {month} were above {threshold} dollars?",
                 f"SELECT COUNT(*) FROM orders WHERE order_month = '{month}' AND total_amount > {threshold}")

for customer in customers:
    add_case("customer_spend", f"How much has customer {customer} spent on paid orders?",
             f"SELECT SUM(total_amount) FROM orders WHERE customer_id = {customer} AND status = 'paid'")

add_case("overall", "What is the total amount of all paid orders?",
         "SELECT SUM(total_amount) FROM orders WHERE status = 'paid'")
add_case("overall", "What is the total amount of all orders?", "SELECT SUM(total_amount) FROM orders")

for case_number, case in enumerate(cases, start=1):
    case["case_id"] = f"case_{case_number:03d}"
    case["data_source"] = "simulated"

with open("cases_demo.jsonl", "w") as output_file:
    for case in cases:
        output_file.write(json.dumps(case) + "\n")

category_counts = {}
for case in cases:
    category_counts[case["category"]] = category_counts.get(case["category"], 0) + 1

print("Total cases:", len(cases))
print("Cases per category:", category_counts)
print("First case:", cases[0])
```

Expected output:

```text
Total cases: 50
Cases per category: {'count': 2, 'average': 2, 'distinct': 2, 'extreme': 4, 'revenue_by_status': 6, 'customer_month': 8, 'customer_status': 12, 'overall': 4, 'threshold': 6, 'customer_spend': 4}
First case: {'category': 'count', 'question': 'How many orders were placed in 2026-03?', 'gold_sql': "SELECT COUNT(*) FROM orders WHERE order_month = '2026-03'", 'case_id': 'case_001', 'data_source': 'simulated'}
```

The script writes `cases_demo.jsonl`. Rename it to `data/cases_v1.jsonl`. Open the file and read a few cases yourself, checking that each correct query makes sense. A wrong correct-answer is the most common silent error.

### **Report template**

```text
# Report 001: SQL Model Comparison
Data note: All data is simulated. Results show the method only.

## Setup
- Dataset version, number of cases, trials per case
- Models and exact names, thinking effort, randomness setting
- Prompt file and its git commit
- Run date

## Results table
| Model | Accuracy (with margin) | p50 latency | p95 latency | Cost per 1,000 requests |

## Failure analysis
- Top three failure categories with two example cases each

## Decision
- Which model, and why this trade-off
- What I would change next

## Limits
- Test set size, simulated data, one task only
```

### **Definition of done (tick every box)**

- [ ] Task and success criteria written before the first run
- [ ] 50 cases, every one marked simulated, each correct query checked by hand
- [ ] Three models picked with a stated reason for each
- [ ] Identical prompt, settings and scorer for all three
- [ ] Each case run at least three times
- [ ] Table shows accuracy with margin, speed and cost
- [ ] Failure analysis with real examples
- [ ] A clear decision that uses the target, not just the top score
- [ ] Everything in git: data, prompts, settings, results, report
- [ ] Someone else can rerun it from the README

---

## **14. Project 2: Production Level**

Same project, now built to be rerun on every change and watched after release.

### **Tool choices**

This field changes fast. Re-check each option on its official page before choosing. As of mid 2026, these were active.

| Layer | Option | Use it for | Trade-off |
|---|---|---|---|
| Test runner | Inspect AI (open source, from the UK AI Security Institute) | Python tasks, scorers, many providers, a log viewer | Its task format is specific to Inspect |
| Test runner | promptfoo (open source) | YAML test files and a fast automatic gate | Config format is specific to promptfoo |
| Public benchmark runner | lm-evaluation-harness (EleutherAI) | Running standard benchmarks on open models | Aimed at benchmarks, not at your app |
| Python test style | DeepEval | pytest-style checks on AI output | Some features tie to a hosted service |
| Logging and live scoring | Langfuse (open source), Arize Phoenix, Braintrust | Logs, datasets, live scoring, dashboards | Pick one. Check licences and hosting |
| Model gateway | LiteLLM or a similar gateway | One interface to many providers | One more service to run |
| Data and versions | JSONL in git, plus DVC or Hugging Face Datasets if data grows | Versioned test sets | More setup |
| Automatic checks | GitHub Actions or your team's system | Run the gate on proposed changes | Needs careful handling of passwords and keys |

**A sensible default stack.** Inspect AI or promptfoo for the before-release tests, run automatically on every change. Langfuse or Phoenix for logging and live scoring. Plain JSONL in git for data. Choose one runner so results stay comparable.

### **Folder layout**

```text
shop-sql-evals/
  configs/
    run_config.yaml
    gates.yaml
  data/
    cases_v1.jsonl
    cases_v2_from_production.jsonl
  prompts/
    sql_prompt_v1.txt
  evals/
    component/
    pipeline/
    application/
  results/
    baseline.json
    runs/
  reports/
  .github/workflows/
    eval_on_pull_request.yml
    nightly_full_eval.yml
```

### **Settings file example**

This one runs: it loads the settings text and prints key fields. Install `pyyaml` first.

```python
import yaml

config_text = """
project: shop-sql-evals
dataset:
  path: data/cases_v1.jsonl
  version: v1
  minimum_cases: 50
models:
  - name: large_model
    reasoning_effort: none
  - name: small_model
    reasoning_effort: none
run:
  temperature: 0
  trials_per_case: 3
  seed_note: "temperature 0 is not fully deterministic, so we repeat trials"
gates:
  max_accuracy_drop: 0.02
  max_p95_latency_increase: 0.20
  max_cost_increase: 0.10
"""

config = yaml.safe_load(config_text)
print("Project:", config["project"])
print("Models:", [model["name"] for model in config["models"]])
print("Trials per case:", config["run"]["trials_per_case"])
print("Accuracy gate:", config["gates"]["max_accuracy_drop"])
```

Expected output:

```text
Project: shop-sql-evals
Models: ['large_model', 'small_model']
Trials per case: 3
Accuracy gate: 0.02
```

### **Production checklist**

- [ ] Dataset has versions, categories and an owner
- [ ] A hidden part that nobody tunes against
- [ ] Prompts, settings and model names pinned and saved with every run
- [ ] Fast tests on every proposed change. Full tests nightly
- [ ] Gates cover accuracy, p95 speed and cost
- [ ] Repeated trials, with limits wider than the measured noise
- [ ] AI grader checked against human labels, with the agreement rate recorded
- [ ] Thinking tokens and cache hits tracked as separate numbers
- [ ] Passwords and keys stored in the automatic-check system's secret store, never in the repo
- [ ] Live logging with sampling, quality scores and alerts
- [ ] A rule for sending reviewed failures into the before-release test set
- [ ] A recorded baseline and a reviewed process to update it
- [ ] A named person who owns the suite

### **Weekly routine**

| Day | Task |
|---|---|
| Monday | Read the dashboard. Check weekend alerts. Compare to baseline |
| Tuesday | Review a sample of low-scoring live requests. Label them |
| Wednesday | Turn confirmed failures into new test cases. Bump the dataset version |
| Thursday | Run the full suite on the latest prompt and model setup. Look at cost and speed |
| Friday | Check for new model releases and benchmark news. Rerun the shortlist if something changed. Write a short summary |
| Monthly | Recheck the AI grader against fresh human labels. Review price changes. Retire maxed-out tests |

---

## **15. Interview Answer: "How do you choose a model for a new feature?"**

"I do not start with a leaderboard. I use public benchmarks only to build a shortlist, maybe three models: one strong, one middle and one cheap. Benchmarks leak into training data and get maxed out, and the numbers depend on settings that vendors often do not share. So they tell me who is worth testing, not who to ship.

Then I write down what success means for the task, with numbers: accuracy, p95 latency and cost per thousand requests. I build a small custom dataset from the real task, around fifty cases to start, with correct answers. For a SQL feature, for example, I run the query and compare the results, so I do not depend on an AI grader.

I run every model with the same prompt, same settings and same scorer, and I repeat each case a few times because outputs vary. I report accuracy with a margin so I do not confuse noise with a real gap. I add the cost, including caching and batch discounts where they apply. For thinking models I fix the effort setting and track the thinking tokens separately.

Then I pick the best trade-off, not the top score. After release I log real traffic, review the failures every week, and add them to the test set. I put a gate in my automatic checks that looks at quality, speed and cost together, so a gain in one cannot hide a loss in another."