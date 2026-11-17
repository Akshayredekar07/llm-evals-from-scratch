# **Phase 2 Notes: Model Evals, Benchmarks and Eval Suites**

Phase 1 taught you to test one application. Phase 2 teaches you to compare models, read benchmarks without being fooled, and build an eval suite that guards every release. All examples use one running project: **ShopSQL**, a Text-to-SQL helper. A user asks a question in plain English ("How many orders were placed last month?") and the system writes a SQL query for a small shop database.

**Core rule of the phase:** public benchmarks shortlist models, your own task evals choose one, and a regression suite keeps that choice safe. Always judge quality, latency and cost together.

Before you install anything, verify current tool versions and model names. They change every few months. Versions seen while writing: Inspect AI 0.3.290, lm-evaluation-harness 0.4.13, DeepEval 4.3.4, Ragas 0.4.4. Treat these as examples only.

---

## **1. Key Terms**

| Term | Plain meaning | ShopSQL example |
|---|---|---|
| Eval | A repeatable test that gives a score for model behaviour | Run 50 questions, count correct queries |
| Model eval | Tests a raw model's general ability | MMLU-Pro score of a model |
| Application eval | Tests your product on your task | Does ShopSQL return the right rows? |
| Benchmark | A public, fixed test set with a scoring rule | Spider 2.0, SWE-bench Pro |
| Dataset (test set) | The questions and expected answers | 50 shop questions with gold SQL |
| Gold answer | The known correct answer | The reference SQL query |
| Execution match | Two SQL queries are equal if they return the same rows | Predicted and gold queries both return 3 |
| Programmatic check | A rule written in code | Does the SQL run without error? |
| LLM judge | A model that grades another model's output | Judge says the SQL meaning matches the question |
| Offline eval | Run before release on a fixed set | Nightly run of the 50 cases |
| Online eval | Run on live traffic | Sample 5% of real questions and score them |
| Contamination | Benchmark questions leaked into training data | A model has seen the test answers |
| Saturation | Top models score near the maximum, so the test stops separating them | MMLU scores in the 90s |
| Reasoning tokens | Hidden thinking tokens a reasoning model produces, billed as output | 900 thinking tokens for an 80 token answer |
| p50, p95 latency | Median time, and the time 95% of requests beat | p95 of 4.5 s means 1 in 20 is slower |
| Prompt caching | Cheaper price for a repeated prompt prefix | The schema text sent every time |
| Batch API | Asynchronous processing at a discount | Run the 50 cases overnight at half price |
| Regression | A change that makes something worse | New prompt drops accuracy by 4 points |
| Baseline | The saved result you compare new runs against | Last week's accepted run |
| Eval gate | A CI check that blocks a change when scores fall | Fail the build if quality drops over 2 points |

---

## **2. Workstream 1: Why Vibe Testing Fails**

**Vibe testing** means trying a few prompts, liking the answers, and shipping. It fails for three reasons.

- A few examples hide rare failures. A system that is right 95% of the time looks perfect in ten tries.
- Models are probabilistic. The same input can give different outputs on different runs.
- Nobody can repeat or compare your impressions. You cannot tell if a change made things better.

**Real failure: Air Canada.** In November 2022 a customer, Jake Moffatt, asked the Air Canada website chatbot about bereavement fares after his grandmother died. The chatbot said he could book at full price and claim a bereavement discount afterwards. The airline's real policy did not allow that. In February 2024 the British Columbia Civil Resolution Tribunal (Moffatt v. Air Canada, 2024 BCCRT 149) ruled for the customer. The airline had argued the chatbot was a separate entity responsible for its own words. The tribunal rejected that: a chatbot is part of the website, and the company is responsible for all the information on it. The airline was ordered to pay about 812 Canadian dollars in damages and fees. The press called it an AI chatbot. The tribunal did not establish what technology it used, and that does not change the lesson: the company owns what its chatbot says.

The lesson for evals: one wrong policy answer cost real money, and a small test set of policy questions would likely have caught it.

**Deterministic tests versus probabilistic systems**

| | Normal software test | LLM system test |
|---|---|---|
| Same input | Same output every time | Output can vary |
| Pass rule | Exact match | Often a score or a rate |
| One run proves | Usually enough | Almost nothing |
| Result looks like | Pass or fail | A percentage with uncertainty |
| Regression means | A test turns red | A rate drops over many runs |

The example below shows the difference. Normal code gives the same answer every run. A pretend model that is right 80% of the time gives a wrong answer on one of eight runs.

```python
import random

random.seed(3)


def add_numbers(first_number, second_number):
    return first_number + second_number


def pretend_model_answer(question):
    correct_sql = "SELECT COUNT(*) FROM orders"
    wrong_sql = "SELECT COUNT(*) FROM customers"
    if random.random() < 0.8:
        return correct_sql
    return wrong_sql


print("Normal code, same input, 8 runs:")
for run_number in range(1, 9):
    print(" run", run_number, "->", add_numbers(2, 3))

print("Pretend model, same question, 8 runs:")
for run_number in range(1, 9):
    print(" run", run_number, "->", pretend_model_answer("How many orders are there?"))
```

Expected output:

```text
Normal code, same input, 8 runs:
 run 1 -> 5
 run 2 -> 5
 run 3 -> 5
 run 4 -> 5
 run 5 -> 5
 run 6 -> 5
 run 7 -> 5
 run 8 -> 5
Pretend model, same question, 8 runs:
 run 1 -> SELECT COUNT(*) FROM orders
 run 2 -> SELECT COUNT(*) FROM orders
 run 3 -> SELECT COUNT(*) FROM orders
 run 4 -> SELECT COUNT(*) FROM orders
 run 5 -> SELECT COUNT(*) FROM orders
 run 6 -> SELECT COUNT(*) FROM orders
 run 7 -> SELECT COUNT(*) FROM orders
 run 8 -> SELECT COUNT(*) FROM customers
```

**Rules to remember**
- Test many cases, not a few.
- Score a rate, not a single answer.
- Repeat runs when the system is random, and report the spread.

---

## **3. Workstream 2: Model Evals Versus Application Evals**

A model's score on a public test tells you what the raw model can do. It does not tell you whether your product works. A model that is excellent at graduate-level science questions may still write bad SQL for your shop schema, ignore your output format, or be too slow.

| | Model eval | Application eval |
|---|---|---|
| Question | How capable is this model in general? | Does my product do the job? |
| Data | Public benchmark | Your own cases |
| Includes | Model only | Prompt, schema, tools, retrieval, output parsing |
| Used for | Shortlisting | Choosing and releasing |
| Owner | Model lab or a leaderboard | You |

**The six step workflow** (use it for every eval)

1. **Task definition.** Write one sentence. ShopSQL: "Turn a question about the shop database into one read-only SQL query."
2. **Success criteria.** State what counts as correct. ShopSQL: the query runs, is read-only, and returns the same rows as the gold query.
3. **Dataset.** Collect cases with expected answers. Start with 50.
4. **Execution.** Run every case through the system with fixed settings and save raw outputs.
5. **Analysis.** Score, then group failures by type. Read the actual failures. Numbers alone do not tell you why.
6. **Iteration.** Change one thing (prompt, model, schema text), rerun, compare to the baseline.

Why one change at a time: if you change the prompt and the model together, you cannot tell which one moved the score.

---

## **4. Workstream 3: Match the Method to the Behaviour**

Pick the cheapest method that can judge the behaviour reliably.

| Behaviour | Method | ShopSQL example |
|---|---|---|
| Deterministic (right or wrong by rule) | Programmatic check | SQL runs; no DROP or DELETE; same rows as gold |
| Semantic (meaning, tone, completeness) | LLM judge | Is the plain-English explanation of the query faithful? |
| Ambiguous or high stakes | Human review | Question says "recent". Which time window is right? |
| Speed and spend | Operational metrics | p95 latency, tokens, cost per request |

**Programmatic checks first.** They are free, fast and exact. For Text-to-SQL, execution match is the main check: run both queries on a test database and compare the rows. This is better than comparing SQL text, because `COUNT(*)` and `COUNT(id)` look different but give the same rows.

```python
import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()
cursor.execute("CREATE TABLE orders (id INTEGER, customer_id INTEGER, total REAL)")
cursor.executemany(
    "INSERT INTO orders VALUES (?, ?, ?)",
    [(1, 10, 25.0), (2, 11, 40.0), (3, 10, 15.0)],
)

test_cases = [
    {"name": "count orders", "gold": "SELECT COUNT(*) FROM orders",
     "predicted": "SELECT COUNT(id) FROM orders"},
    {"name": "sum of totals", "gold": "SELECT SUM(total) FROM orders",
     "predicted": "SELECT AVG(total) FROM orders"},
    {"name": "broken sql", "gold": "SELECT COUNT(*) FROM orders",
     "predicted": "SELECT COUNT( FROM orders"},
]

passed_count = 0
for test_case in test_cases:
    gold_rows = cursor.execute(test_case["gold"]).fetchall()
    try:
        predicted_rows = cursor.execute(test_case["predicted"]).fetchall()
    except sqlite3.Error as error_message:
        print("FAIL (does not run):", test_case["name"], "|", error_message)
        continue
    if predicted_rows == gold_rows:
        passed_count += 1
        print("PASS:", test_case["name"])
    else:
        print("FAIL (wrong result):", test_case["name"], "|", predicted_rows, "vs", gold_rows)

print("Passed", passed_count, "of", len(test_cases))
```

Expected output:

```text
PASS: count orders
FAIL (wrong result): sum of totals | [(26.666666666666668,)] vs [(80.0,)]
FAIL (does not run): broken sql | near "FROM": syntax error
Passed 1 of 3
```

**Judges for meaning.** An LLM judge gives scale but has its own bias. Give it a short rubric, ask for a reason before the score, and use a different model family than the one being judged when you can.

**Humans for calibration.** Have a person grade 30 to 50 cases, then check how often the judge agrees with the person. If agreement is low, fix the rubric before trusting the judge.

**Operational metrics.** Measure these on every run, because a quality gain that doubles latency may not be a win. The example below computes median latency, slow-request latency, error rate and average output tokens.

```python
import math

latencies_in_seconds = [0.8, 1.1, 0.9, 1.0, 1.2, 0.7, 1.0, 4.5, 0.9, 1.1]
error_flags = [0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
output_tokens = [60, 75, 58, 80, 0, 66, 70, 0, 64, 72]


def nearest_rank_percentile(values, percent):
    sorted_values = sorted(values)
    rank = math.ceil(percent / 100 * len(sorted_values))
    return sorted_values[rank - 1]


median_latency = nearest_rank_percentile(latencies_in_seconds, 50)
slow_latency = nearest_rank_percentile(latencies_in_seconds, 95)
error_rate = sum(error_flags) / len(error_flags)
average_output_tokens = sum(output_tokens) / len(output_tokens)

print("p50 latency (seconds):", median_latency)
print("p95 latency (seconds):", slow_latency)
print("error rate:", error_rate)
print("average output tokens:", average_output_tokens)
```

Expected output:

```text
p50 latency (seconds): 1.0
p95 latency (seconds): 4.5
error rate: 0.2
average output tokens: 54.5
```

How the numbers come from the data (nearest-rank method):

Formula in words: sort the values, find the position = ceiling of (percent divided by 100 times the count), and take the value at that position.

Median (p50) position = ceiling of (50 / 100 x 10)

= ceiling of 5

= position 5, which is 1.0 seconds

p95 position = ceiling of (95 / 100 x 10)

= ceiling of 9.5

= position 10, which is 4.5 seconds

Why look at p95: the median says 1.0 s, so the service seems fast. The p95 says 4.5 s, so one user in twenty waits much longer.

Note that two failed requests have zero output tokens, which pulls the average down to 54.5. Compute token averages on successful requests only, and report errors separately.

---

## **5. Workstream 4: Offline Versus Online**

| | Offline | Online |
|---|---|---|
| When | Before release, in CI | After release, on live traffic |
| Data | Fixed, labelled cases | Real user inputs, usually unlabelled |
| Catches | Regressions, known failure types | Unexpected inputs, drift, new user habits |
| Cost | Predictable | Grows with traffic, so sample |
| Role | Gate | Smoke alarm |

Drift means the live world slowly moves away from your test set. ShopSQL example: the shop adds a new `returns` table and users start asking about returns, but your 50 cases never mention it.

**Two kinds of metric. Keep them separate.**

| Kind | How it is obtained | Examples |
|---|---|---|
| System metrics | Captured automatically on every request | Latency, input and output tokens, error codes, cost |
| Quality metrics | Computed by a check or a judge, so they cost extra | Hallucination, relevance, SQL correctness |

**The online pipeline**

1. **Log.** Store every request, response, model name, prompt version and system metrics.
2. **Sample.** Score a slice (for example 5%, plus every error and every thumbs-down).
3. **Dashboard.** Plot quality and system metrics over time.
4. **Alert.** Notify someone when a metric crosses a threshold.
5. **Feed back.** Add the failures to the offline set. This is how the suite keeps pace with reality.

Why step 5 matters: every production failure that does not become a test case can happen again.

---

## **6. Workstream 5: Benchmark Anatomy and Pitfalls**

A benchmark has five parts. A score is only meaningful if all five are stated.

| Part | Question | Example |
|---|---|---|
| Dataset | What are the questions? | 2,500 expert questions |
| Prompts | How is each question presented? | Zero-shot or few-shot, with what wording |
| Run configuration | Which settings? | Temperature, reasoning effort, turn limit, tools allowed |
| Scoring method | How is an answer marked? | Exact match, test pass, or a judge |
| Aggregation | How are scores combined? | Plain average, or per-subject then averaged |

**Pitfalls**

| Pitfall | Meaning | What to do |
|---|---|---|
| Contamination | Test questions were in the training data, so the model memorised them | Prefer private, new or rotating test sets; run your own data |
| Saturation | Top models are near 100%, so the test no longer separates them | Move to a harder benchmark |
| Overfitting to the benchmark | A lab or team tunes to the test, not to the real skill | Check results on a different test of the same skill |
| Configuration gaming | Scores rise because of looser settings, not a better model | Compare only runs with the same settings |

Configuration gaming is not a theory. On SWE-bench Pro, a coding benchmark, leaderboard figures were reported to have risen sharply partly because the allowed number of agent turns went from 50 to 250. A score without its run settings is not a measurement.

**A simple contamination check.** Take each benchmark question, cut it into overlapping six-word windows, and see how many appear in a text sample you suspect was in the training data. This is a rough signal, not proof.

```python
def word_windows(text, window_size):
    words = text.lower().split()
    windows = set()
    for start_index in range(len(words) - window_size + 1):
        windows.add(" ".join(words[start_index:start_index + window_size]))
    return windows


training_text_sample = (
    "forum post: which customer placed the most orders in the first "
    "quarter of the year is a common sql interview question"
)
benchmark_questions = [
    "Which customer placed the most orders in the first quarter of the year",
    "List every product that was returned twice by the same buyer",
]

window_size = 6
training_windows = word_windows(training_text_sample, window_size)

for question in benchmark_questions:
    question_windows = word_windows(question, window_size)
    shared_windows = question_windows & training_windows
    overlap_share = len(shared_windows) / len(question_windows)
    print(round(overlap_share, 2), "|", question)
```

Expected output:

```text
1.0 | Which customer placed the most orders in the first quarter of the year
0.0 | List every product that was returned twice by the same buyer
```

The first question shares every six-word window with the forum post, so it is likely contaminated. The second shares none.

**Public benchmarks shortlist models. Your domain evals decide.** Use a leaderboard to cut fifty models to three, then run your own cases.

---

## **7. Workstream 6: The Knowledge Benchmark Progression**

Each new benchmark exists because models learned the last one.

| Benchmark | What it is | Why it appeared or what to know |
|---|---|---|
| MMLU | About 16,000 multiple-choice questions across 57 subjects | Early general knowledge test. Frontier models now score in the 90s, so it is saturated |
| TruthfulQA | 817 questions built to trigger common false beliefs | Tests whether a model repeats popular myths. Useful, but small and now widely trained on |
| AGIEval | Questions from human exams such as the SAT, LSAT and Chinese gaokao | Tests the model on tests built for people |
| GPQA (Diamond) | 198 graduate-level science questions that experts wrote to be hard to search | Meant to be "Google-proof". Top models have approached saturation |
| MMLU-Pro | About 12,000 harder questions with 10 answer options instead of 4 | Harder and less guessable than MMLU. Top scores are now high |
| SimpleQA | Short fact questions with one clear answer, built to be hard for models | Measures factual accuracy and also whether the model admits it does not know |
| Humanity's Last Exam (HLE) | About 2,500 expert-written questions from close to 1,000 contributors | Built in 2025 by the Center for AI Safety and Scale AI as a long-lasting hard test |

**Why benchmarks keep getting harder.** Frontier models improve quickly, so a test that separates models this year saturates the next. Public tests also leak into training data. Authors respond with harder questions, more answer options, expert writers, and private or rotating sets.

HLE shows how fast this moves. It launched with scores in the single digits and low tens, and by mid-2026 sources report several models above 50%, mostly when the model may use tools. Check the live leaderboard for current numbers, and note whether the score is with or without tools.

**How to use this list.** Do not memorise scores. Learn what each test measures, how saturated it is, and whether it matches your task. A knowledge benchmark says little about Text-to-SQL. Use it only to cut the shortlist.

---

## **8. Workstream 7: The Coding Benchmark Progression**

**SWE-bench Verified** gives an agent a real bug report from an open source Python repository and asks it to fix the code. A test suite decides if the fix works. The Verified set has 500 tasks that humans checked as solvable. Top scores passed 70%, so it saturated quickly. There are also contamination concerns: the repositories are public and old, so models may have seen the fixes.

**SWE-bench Pro** (Scale AI, September 2025) was built to reduce those concerns.

| | SWE-bench Verified | SWE-bench Pro |
|---|---|---|
| Source | Public Python repositories | 1,865 tasks from 41 repositories |
| Contamination defence | None built in | Public set uses copyleft (GPL style) repositories. A held-out set is never published. A private set comes from company code under agreements |
| Task size | Often small fixes | Larger changes, often several files |
| Early frontier scores | Above 70% | About 23% at launch for the best models |
| Scoring | Failing test must pass | A fix must pass the target tests and must not break existing tests |

**Compare the gap before you trust a rank.** Take a model's Verified score and its Pro score. A large gap hints that its Verified score may rely on memory or a tuned setup. A small gap suggests the skill is more general.

Gap = Verified score minus Pro score.

Example with made-up numbers: Model A scores 78 on Verified and 45 on Pro.

Step 1: 78 - 45 = 33 points.

Model B scores 72 on Verified and 55 on Pro.

Step 2: 72 - 55 = 17 points.

Model A ranks higher on Verified but has the bigger gap. Model B looks more reliable on harder, newer tasks.

**Two warnings, both reported after launch. Verify them yourself:**
- Reports say scores on Pro rose sharply after the leaderboard allowed more agent turns (250 instead of 50), so always read the harness settings next to the score.
- Reports say OpenAI stopped reporting Verified scores in 2026 and later audited the public Pro set and found a large share of tasks flawed. Whatever the final facts are, the lesson holds: even good benchmarks have errors, so treat close ranks as ties and check the date, subset, harness and confidence interval.

For ShopSQL, the matching Text-to-SQL ladder is Spider 1.0, then BIRD, then Spider 2.0. Spider 2.0 has 632 enterprise-style tasks. Its paper reported a best agent result near 21% while the same kind of models scored above 90% on Spider 1.0. The pattern is the same: an easy benchmark saturates, a harder one appears.

---

## **9. Workstream 8: Reasoning Models**

A reasoning model thinks before it answers. The thinking uses extra tokens, which are billed as output, and it makes both cost and quality vary more.

**Three rules**

1. **Evaluate at fixed reasoning-effort settings.** Providers expose a setting (often low, medium, high, or a token budget for thinking). The name differs by provider, so read the current docs. Score each setting separately. "Model X" is not one system, it is several.
2. **Track reasoning tokens separately.** Keep three numbers: input tokens, reasoning tokens, answer tokens. Without this you cannot see where the money goes.
3. **Run more trials.** Variance is higher, so run each case several times (3 to 5) and report the mean and the spread.

The example below shows five trials of one model at one setting.

```python
trial_scores = [0.62, 0.70, 0.58, 0.66, 0.64]
reasoning_tokens_per_request = 900
answer_tokens_per_request = 80
output_price_per_million_tokens = 4.00

average_score = sum(trial_scores) / len(trial_scores)
lowest_score = min(trial_scores)
highest_score = max(trial_scores)
score_spread = highest_score - lowest_score

reasoning_cost = reasoning_tokens_per_request / 1_000_000 * output_price_per_million_tokens
answer_cost = answer_tokens_per_request / 1_000_000 * output_price_per_million_tokens

print("average score:", round(average_score, 3))
print("lowest to highest:", lowest_score, "to", highest_score)
print("spread:", round(score_spread, 2))
print("reasoning cost per request:", round(reasoning_cost, 5))
print("answer cost per request:", round(answer_cost, 5))
print("reasoning share of output cost:", round(reasoning_cost / (reasoning_cost + answer_cost), 2))
```

Expected output:

```text
average score: 0.64
lowest to highest: 0.58 to 0.7
spread: 0.12
reasoning cost per request: 0.0036
answer cost per request: 0.00032
reasoning share of output cost: 0.92
```

Calculations behind the output (example price: 4.00 dollars per million output tokens, made up):

Average score = sum of trial scores divided by number of trials.

Sum = 0.62 + 0.70 + 0.58 + 0.66 + 0.64 = 3.20

Average = 3.20 / 5 = 0.64

Spread = highest score minus lowest score.

Spread = 0.70 - 0.58 = 0.12

Reasoning cost per request = reasoning tokens divided by 1,000,000, times price.

Reasoning cost = 900 / 1,000,000 x 4.00 = 0.0036 dollars

Answer cost = 80 / 1,000,000 x 4.00 = 0.00032 dollars

Reasoning share = 0.0036 / (0.0036 + 0.00032) = 0.92

So 92% of the output bill is thinking you never see. One run could have scored 0.58 or 0.70. If you compared this model with another using a single run, you could pick the wrong winner.

---

## **10. Workstream 9: Custom Model Evaluation**

This is the heart of the phase and the proof of learning. Build a model comparison for your own task, in five steps.

### **10.1 Shortlist by four filters**

| Filter | Question | ShopSQL need |
|---|---|---|
| Capability | Does it do the task class? Use public benchmarks here | Good at code and SQL |
| Latency | Is it fast enough? | Under 3 seconds median |
| Context window | Does the schema plus question fit? | Schema is about 1,500 tokens, so any modern model fits |
| Cost | Does it fit the budget at your volume? | Under a set cost per 1,000 questions |

Pick three on purpose: a small fast model, a mid model, and a large or reasoning model. For example, from one provider family you might pick a small, a mid and a large tier, and add one open-weight model you can run yourself. Check current model names and prices on each provider's page before you start. Names change.

### **10.2 Build a custom dataset (Text-to-SQL)**

You need no real customer data. Build a small simulated shop database in SQLite, with tables like `customers`, `orders`, `order_items` and `products`. Then write 50 questions with gold SQL.

**Label simulated data honestly.** Put `"source": "simulated"` in every case, say so in the report ("all data in this report is simulated"), and never present simulated numbers as real business results.

Suggested mix of 50 cases:

| Category | Count | Example |
|---|---|---|
| Simple count or sum | 10 | How many orders are there? |
| Filters and dates | 10 | Orders over 100 dollars in March |
| Joins across tables | 10 | Customer names with more than 2 orders |
| Group by and ranking | 8 | Top 3 products by revenue |
| Tricky or ambiguous | 6 | "Recent" orders (needs a stated rule) |
| Unsafe or out of scope | 6 | "Delete all orders" (must refuse) |

Check your file before you use it. The script below catches a duplicate id and a missing gold query.

```python
import json

case_lines = [
    '{"case_id": "sql_001", "question": "How many orders are there?", "gold_sql": "SELECT COUNT(*) FROM orders", "category": "count", "source": "simulated"}',
    '{"case_id": "sql_002", "question": "What is the total of all orders?", "gold_sql": "SELECT SUM(total) FROM orders", "category": "sum", "source": "simulated"}',
    '{"case_id": "sql_002", "question": "Average order value?", "gold_sql": "SELECT AVG(total) FROM orders", "category": "average", "source": "simulated"}',
    '{"case_id": "sql_004", "question": "Which customer spent most?", "category": "group_by", "source": "simulated"}',
]
required_fields = ["case_id", "question", "gold_sql", "category", "source"]

seen_ids = set()
category_counts = {}
problem_count = 0

for line_number, line_text in enumerate(case_lines, start=1):
    case = json.loads(line_text)
    missing_fields = [field for field in required_fields if field not in case]
    if missing_fields:
        print("line", line_number, "missing:", missing_fields)
        problem_count += 1
    if case["case_id"] in seen_ids:
        print("line", line_number, "duplicate id:", case["case_id"])
        problem_count += 1
    seen_ids.add(case["case_id"])
    category = case["category"]
    category_counts[category] = category_counts.get(category, 0) + 1

print("categories:", category_counts)
print("problems found:", problem_count)
```

Expected output:

```text
line 3 duplicate id: sql_002
line 4 missing: ['gold_sql']
categories: {'count': 1, 'sum': 1, 'average': 1, 'group_by': 1}
problems found: 2
```

Public sources if you want more cases: Spider (1.0) dev set, which has many databases, and BIRD, which has 12,751 question and SQL pairs over 95 databases with messier data. Check their licences and mark them `"source": "spider"` or `"source": "bird"`. Do not mix them into your simulated set without the label.

### **10.3 Compare like for like**

Every model gets the same inputs, same prompt, same parameters (temperature 0 where allowed, same maximum output tokens, same reasoning-effort setting) and the same scoring code. If a model needs a different prompt format, change only the wrapper and say so. The example runs two fake models through one loop to show the shape.

```python
import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()
cursor.execute("CREATE TABLE orders (id INTEGER, customer_id INTEGER, total REAL)")
cursor.executemany("INSERT INTO orders VALUES (?, ?, ?)", [(1, 10, 25.0), (2, 11, 40.0), (3, 10, 15.0)])

test_cases = [
    {"question": "count orders", "gold_sql": "SELECT COUNT(*) FROM orders"},
    {"question": "total of orders", "gold_sql": "SELECT SUM(total) FROM orders"},
    {"question": "biggest order", "gold_sql": "SELECT MAX(total) FROM orders"},
    {"question": "orders by customer 10", "gold_sql": "SELECT COUNT(*) FROM orders WHERE customer_id = 10"},
]

run_settings = {"temperature": 0, "max_output_tokens": 200, "prompt_version": "v1"}

fake_models = {
    "model_small": {"price_per_million_output": 0.5, "seconds": 0.8, "answers": [
        "SELECT COUNT(*) FROM orders", "SELECT AVG(total) FROM orders",
        "SELECT MAX(total) FROM orders", "SELECT COUNT(*) FROM orders"]},
    "model_large": {"price_per_million_output": 5.0, "seconds": 3.5, "answers": [
        "SELECT COUNT(*) FROM orders", "SELECT SUM(total) FROM orders",
        "SELECT MAX(total) FROM orders", "SELECT COUNT(*) FROM orders WHERE customer_id = 10"]},
}
fake_output_tokens_per_answer = 40

print("settings used for every model:", run_settings)
for model_name, model_info in fake_models.items():
    correct_count = 0
    for case_index, test_case in enumerate(test_cases):
        gold_rows = cursor.execute(test_case["gold_sql"]).fetchall()
        predicted_rows = cursor.execute(model_info["answers"][case_index]).fetchall()
        if predicted_rows == gold_rows:
            correct_count += 1
    total_tokens = fake_output_tokens_per_answer * len(test_cases)
    cost = total_tokens / 1_000_000 * model_info["price_per_million_output"]
    print(model_name, "| correct", correct_count, "of", len(test_cases),
          "| seconds", model_info["seconds"], "| cost", f"{cost:.5f}")
```

Expected output:

```text
settings used for every model: {'temperature': 0, 'max_output_tokens': 200, 'prompt_version': 'v1'}
model_small | correct 2 of 4 | seconds 0.8 | cost 0.00008
model_large | correct 4 of 4 | seconds 3.5 | cost 0.00080
```

### **10.4 Estimate token cost, including caching and batch**

Prices below are made up for the arithmetic. Use the real price page of each provider.

Setup: 1,000 requests. Each request has a 1,500 token schema prefix (the same every time), a 100 token question, and an 80 token answer. Input costs 1.00 dollar per million tokens and output costs 4.00 dollars per million.

```python
input_price_per_million = 1.00
output_price_per_million = 4.00
prefix_tokens = 1500
question_tokens = 100
output_tokens = 80
request_count = 1000
cached_read_share_of_price = 0.10
batch_share_of_price = 0.50

input_tokens = prefix_tokens + question_tokens
plain_input_cost = input_tokens / 1_000_000 * input_price_per_million
output_cost = output_tokens / 1_000_000 * output_price_per_million
plain_total = (plain_input_cost + output_cost) * request_count

cached_input_tokens = prefix_tokens * cached_read_share_of_price + question_tokens
cached_input_cost = cached_input_tokens / 1_000_000 * input_price_per_million
cached_total = (cached_input_cost + output_cost) * request_count

batch_total = cached_total * batch_share_of_price

print("plain total:", round(plain_total, 3))
print("with caching:", round(cached_total, 3))
print("with caching and batch:", round(batch_total, 3))
```

Expected output:

```text
plain total: 1.92
with caching: 0.57
with caching and batch: 0.285
```

How each number is built:

Input tokens per request = prefix + question.

Input tokens = 1,500 + 100 = 1,600

Input cost per request = 1,600 / 1,000,000 x 1.00 = 0.0016 dollars

Output cost per request = 80 / 1,000,000 x 4.00 = 0.00032 dollars

Cost per request = 0.0016 + 0.00032 = 0.00192 dollars

Plain total = 0.00192 x 1,000 = 1.92 dollars

With prompt caching, assume cached tokens cost 10% of the normal input price. This is roughly true at Anthropic. Other providers use different rates, so check.

Cached prefix counts as = 1,500 x 0.10 = 150 token equivalents

Input token equivalents = 150 + 100 = 250

Input cost per request = 250 / 1,000,000 x 1.00 = 0.00025 dollars

Cost per request = 0.00025 + 0.00032 = 0.00057 dollars

Caching total = 0.00057 x 1,000 = 0.57 dollars

With batch on top, assume half price:

Batch total = 0.57 x 0.50 = 0.285 dollars

This ignores the small extra charge some providers add for writing the cache the first time. Over 1,000 requests it is minor. Also check in the provider's docs whether caching and batch discounts stack. At least one provider says they do, but rules differ and change. For an eval run, batch is a good fit because you do not need instant answers. Do not use batch for latency measurements, since it is asynchronous.

### **10.5 Choose the trade-off, not the top ranking**

Set a quality floor and a latency ceiling first, then pick the cheapest model that passes both.

```python
results = [
    {"model": "model_small", "correct": 38, "total": 50, "median_seconds": 0.9, "total_cost": 0.12},
    {"model": "model_medium", "correct": 44, "total": 50, "median_seconds": 1.6, "total_cost": 0.45},
    {"model": "model_large", "correct": 46, "total": 50, "median_seconds": 4.8, "total_cost": 2.10},
]
quality_floor = 0.85
latency_ceiling_seconds = 3.0

print("model         quality  median_s  cost    cost_per_correct")
for result in results:
    quality = result["correct"] / result["total"]
    cost_per_correct = result["total_cost"] / result["correct"]
    result["quality"] = quality
    print(f'{result["model"]:<13} {quality:<8.2f} {result["median_seconds"]:<9} '
          f'{result["total_cost"]:<7} {cost_per_correct:.4f}')

allowed = [r for r in results
           if r["quality"] >= quality_floor and r["median_seconds"] <= latency_ceiling_seconds]
if allowed:
    best_choice = min(allowed, key=lambda r: r["total_cost"])
    print("choice:", best_choice["model"])
else:
    print("choice: none meets the floor and ceiling")
```

Expected output:

```text
model         quality  median_s  cost    cost_per_correct
model_small   0.76     0.9       0.12    0.0032
model_medium  0.88     1.6       0.45    0.0102
model_large   0.92     4.8       2.1     0.0457
choice: model_medium
```

Quality = correct answers divided by total.

Small: 38 / 50 = 0.76

Medium: 44 / 50 = 0.88

Large: 46 / 50 = 0.92

Cost per correct answer = total cost divided by correct answers.

Small: 0.12 / 38 = 0.0032

Medium: 0.45 / 44 = 0.0102

Large: 2.10 / 46 = 0.0457

The large model has the best quality but is too slow (4.8 s against a 3.0 s ceiling) and costs about four and a half times more per correct answer than the medium model. The small model is cheap but below the quality floor. The medium model is the choice. Note the numbers are made up.

**Mind the noise.** With 50 questions, a score of 0.84 has a 95% interval of about 0.72 to 0.92 (the method is in the Phase 3 notes). A difference of one or two questions between models is not a real difference. Report the interval, or run the cases several times.

---

## **11. Workstream 10: Eval Suite and Regression Testing**

### **11.1 Three levels of tests**

| Level | What it tests | ShopSQL example |
|---|---|---|
| Component | One piece alone | The SQL safety check blocks DELETE. Schema loader returns the right tables |
| Pipeline | Several pieces in order | Question, schema lookup, model, SQL run, answer |
| Application | The whole product as a user sees it | Real-style questions in, final reply out |

Component tests are fast and run often. Application tests are slower and run before release. When an application test fails, the component and pipeline tests tell you where.

### **11.2 Version everything**

A result is only comparable if you know exactly what produced it. Save these with each run:

- Test cases (a dataset version or file hash)
- Prompts (a prompt version id)
- Config (temperature, effort, max tokens)
- Model name and snapshot date
- Code commit
- Results (raw outputs and scores)

Keep cases in plain files in git (JSONL or YAML) so a pull request shows exactly what changed.

### **11.3 Track experiments against baselines**

The baseline is the last accepted run. Every new run is compared with it, case by case. Look at which cases flipped from pass to fail, because an unchanged average can hide five new failures balanced by five new passes.

### **11.4 Add CI/CD gates**

Run the suite on every pull request. Fail the build if a rule breaks. The example below checks quality, latency and cost together.

```python
import sys

baseline = {"quality": 0.88, "median_seconds": 1.5, "cost_per_run": 0.40}
new_run = {"quality": 0.84, "median_seconds": 1.4, "cost_per_run": 0.55}

allowed_quality_drop = 0.02
allowed_latency_rise_share = 0.20
allowed_cost_rise_share = 0.20

problems = []
if baseline["quality"] - new_run["quality"] > allowed_quality_drop:
    problems.append("quality dropped too much")
if new_run["median_seconds"] > baseline["median_seconds"] * (1 + allowed_latency_rise_share):
    problems.append("latency rose too much")
if new_run["cost_per_run"] > baseline["cost_per_run"] * (1 + allowed_cost_rise_share):
    problems.append("cost rose too much")

if problems:
    print("GATE FAILED:", "; ".join(problems))
    sys.exit(1)
print("GATE PASSED")
```

Expected output:

```text
GATE FAILED: quality dropped too much; cost rose too much
```

How the gate decides:

Quality drop = baseline quality minus new quality = 0.88 - 0.84 = 0.04. The limit is 0.02, so it fails.

Latency limit = baseline median x (1 + 0.20) = 1.5 x 1.20 = 1.8 seconds. The new run is 1.4, so it passes.

Cost limit = baseline cost x (1 + 0.20) = 0.40 x 1.20 = 0.48 dollars. The new run is 0.55, so it fails.

Latency improved, but quality fell and cost rose. A gate that checked only latency would have passed this change.

**Why track all three together.** A gain in one can hide a loss in another. A cheaper model that is faster but 4 points worse is a trade, not an improvement. Write down which loss you accept.

**Tool note.** Common tools for this layer are Promptfoo (YAML cases, fits CI; reported in March 2026 as being acquired by OpenAI with the open source repo staying MIT licensed, so verify), DeepEval (pytest style), Inspect AI (agents and safety tasks) and lm-evaluation-harness (standard public benchmarks). Pick one for your suite and keep it.

---

## **12. Common Mistakes**

| Mistake | Why it hurts | Better approach |
|---|---|---|
| Choosing a model from a leaderboard rank | The rank measures something else | Shortlist from it, then run your own cases |
| One run per model | Random variation can flip the winner | Repeat runs, report mean and spread |
| Different prompts or settings per model | You compare the wrappers, not the models | Identical inputs, prompts, parameters and scoring |
| Comparing scores from different harnesses | Settings change scores a lot | Compare only same-harness, same-date runs |
| Ignoring reasoning tokens | Real cost is hidden | Track input, reasoning and answer tokens separately |
| Quality only, no cost or latency | The winner may be unaffordable or slow | Report quality, latency and cost together |
| Test set too small to see noise | Differences are noise | Use intervals; grow the set where it matters |
| Test cases never updated | The suite drifts from reality | Feed production failures back into the set |
| Using a judge without checking it | The judge may be biased | Compare the judge with human grades first |
| Presenting simulated data as real | Misleading | Label every simulated case and the report |
| Trusting old benchmark numbers | Benchmarks and leaderboards change | Note date, subset and harness with every number |

---

## **13. Project Setup 1 (Beginner): ShopSQL Model Comparison**

**Goal:** the proof of learning. Shortlist three models, build 50 cases, run all three with identical settings, and publish a quality, latency and cost table.

**Frameworks by layer (beginner)**

| Layer | Choice | Why |
|---|---|---|
| Language | Python 3.11 or newer | Standard for eval work |
| Data and database | SQLite (built into Python) | No server, easy to reset |
| Model access | The official Python SDK of each provider, or one gateway such as LiteLLM | Few moving parts; verify current packages |
| Scoring | Plain Python and `sqlite3` | You see every line of the logic |
| Results | CSV files and a Markdown report | Easy to read and diff |
| Version control | Git | Tracks cases and results |

**Folder layout**

```text
shopsql-model-eval/
  data/
    shop.db                 (simulated database)
    cases.jsonl             (50 cases)
  prompts/
    sql_prompt_v1.txt
  src/
    build_database.py
    check_cases.py
    run_models.py
    score_results.py
    make_report.py
  results/
    run_2026-11-20.csv
  report.md
  README.md
```

**Setup commands**

```bash
mkdir shopsql-model-eval && cd shopsql-model-eval
python -m venv .venv
source .venv/bin/activate
pip install python-dotenv pandas
pip install anthropic openai
git init
```

Check the current package names before you install. Put API keys in a `.env` file and add `.env` to `.gitignore`.

**Build order**

1. Write `build_database.py` to create the simulated shop database.
2. Write 50 cases in `cases.jsonl`. Run `check_cases.py` (like example 9) until it reports zero problems.
3. Run every gold query to confirm each one works and returns rows.
4. Write the prompt file. Keep one version only.
5. Write `run_models.py`. For each model and case, record the SQL, start and end time, input and output tokens, and any error. Use identical settings.
6. Write `score_results.py` using execution match.
7. Run each model three times on the full set. Save every raw run.
8. Compute quality, median and p95 latency, and cost with the real price page.
9. Read every failure and label its cause.
10. Write the report.

**Report template**

```text
# ShopSQL Model Comparison
Date, dataset version, prompt version
Note: all data is simulated.

## Setup
Models, settings (temperature, max tokens, reasoning effort), runs per model

## Results
| Model | Quality (95% interval) | Median s | p95 s | Cost per 1,000 questions |

## Failure analysis
Top 3 failure types per model with 2 examples each

## Decision
Chosen model, why, and the trade-off accepted

## Limits
What 50 cases cannot show
```

**Definition of done**

- 50 cases, all labeled `simulated`, no duplicates, every gold query runs.
- Three models run with identical settings, three runs each.
- Quality, p50 and p95 latency, and cost per 1,000 questions are in one table.
- Intervals or spread are shown.
- Failures were read and grouped.
- A decision is written with its trade-off.
- Dataset, prompt and results are saved in git.

**Best datasets and benchmarks for this project**

| Use | Source |
|---|---|
| Your main set | 50 simulated cases (you write them) |
| Extra realistic questions | Spider 1.0 dev set (many small databases) |
| Messier data and external knowledge | BIRD (12,751 pairs, 95 databases) |
| Enterprise difficulty (optional, advanced) | Spider 2.0 (632 tasks). Some parts need cloud accounts, so check cost |
| Model shortlist context | Public leaderboards. Always note date and settings |

---

## **14. Project Setup 2 (Production Level): ShopSQL Eval Suite**

**Goal:** a repeatable eval suite that runs in CI, tracks quality, latency and cost, and watches production.

**Tool choices (verify current options before you commit)**

| Need | Option | Notes |
|---|---|---|
| Standard public benchmarks | lm-evaluation-harness (EleutherAI) | Reference tool for many academic benchmarks. Weak signal for your own task |
| Custom task evals, agents, safety | Inspect AI (UK AI Security Institute) | Task, solver and scorer structure; good logs |
| CI prompt and model comparison | Promptfoo | YAML cases, runs in CI. Reported as acquired by OpenAI in 2026 with MIT repo kept, so verify |
| pytest style tests | DeepEval | Fits teams that already use pytest |
| Tracing and online scores | Langfuse (open source) or Braintrust, Arize Phoenix, LangSmith | Stores traces, datasets and scores |
| Model gateway | LiteLLM or OpenRouter | One call format for many models |
| CI | GitHub Actions | Runs the suite on pull requests |
| Storage | Git for cases, a database or the tracing tool for runs | Keep results versioned |

Why one of each, not all: each tool adds work. Start with a CI runner, a tracing store and a gateway. Add more only when a gap shows up.

**Folder layout**

```text
shopsql-eval-suite/
  evals/
    cases/
      component/        (safety check, schema loader)
      pipeline/         (end to end with real database)
      application/      (user-style questions)
    datasets/
      cases_v3.jsonl
    prompts/
      sql_prompt_v4.txt
    configs/
      eval_config.yaml
    scorers/
      execution_match.py
      read_only_check.py
      judge_explanation.py
  baselines/
    baseline_2026-11-20.json
  results/                (ignored by git except summaries)
  .github/workflows/eval.yml
  docs/
    model_choice.md
    runbook.md
```

**Config file example**

```yaml
suite_name: shopsql_eval
dataset_version: cases_v3
prompt_version: sql_prompt_v4

models:
  - name: model_small
    reasoning_effort: none
  - name: model_medium
    reasoning_effort: low
  - name: model_large
    reasoning_effort: medium

run_settings:
  temperature: 0
  max_output_tokens: 300
  trials_per_case: 3

thresholds:
  min_quality: 0.85
  max_quality_drop_vs_baseline: 0.02
  max_p95_seconds: 4.0
  max_cost_rise_vs_baseline: 0.20
  max_unsafe_sql_count: 0

online:
  sample_rate: 0.05
  always_score_errors: true
  alert_if_quality_below: 0.80
```

**Production checklist**

- Cases live in git with versions, and every case has `source` and `category`.
- Prompts, configs and model names are versioned together with results.
- Component, pipeline and application tests are separate and tagged.
- CI runs the fast suite on every pull request and the full suite nightly.
- The gate checks quality, latency and cost together, and a zero tolerance rule for unsafe SQL.
- A baseline file is stored and updated only by a reviewed change.
- Reasoning tokens, cache hits and batch use are logged per request.
- Judges are checked against human grades each quarter.
- Production traffic is logged, sampled, scored and plotted.
- Alerts reach a named owner.
- Failures from production become new test cases within a week.
- A new model release triggers a re-run of the comparison.
- API keys are in a secret store, never in git.

**Weekly operating routine**

| Day | Task |
|---|---|
| Monday | Review the last week's dashboard and alerts. Read 20 sampled production failures |
| Tuesday | Add new failure cases to the dataset. Review them for labels |
| Wednesday | Run the full suite and compare with the baseline. Look at flipped cases |
| Thursday | Check for new model releases and price changes. Re-run the shortlist if needed |
| Friday | Update the baseline if the changes were approved. Write a short note on what changed |

---

## **15. Quick Reference**

**Terms**

| Term | One line |
|---|---|
| Vibe testing | Judging by a few tries |
| Model eval | General ability of a model |
| Application eval | Does my product work on my task |
| Execution match | Same rows from predicted and gold SQL |
| p95 | The time 95% of requests beat |
| Contamination | Test seen in training |
| Saturation | Test too easy for top models |
| Reasoning tokens | Hidden thinking, billed as output |
| Baseline | Last accepted result |
| Gate | CI check that blocks a regression |

**Rules to remember**

- A model that is good on a benchmark may be wrong for your task. Run your own cases.
- Use the cheapest reliable check: code first, judge second, human for calibration.
- Offline suites gate releases. Online checks find the unknown. Feed failures back.
- Keep system metrics and quality metrics separate.
- A benchmark score needs its dataset, prompt, settings, scoring method and date.
- Compare Verified and Pro style scores before trusting a rank.
- Reasoning models: fix the effort setting, track reasoning tokens, run more trials.
- Compare models like for like: same inputs, prompts, parameters, scoring.
- Choose by quality floor, latency ceiling and lowest cost, not by rank.
- With 50 cases, small gaps are noise. Show intervals.
- Version cases, prompts, configs, models and results.
- Gate on quality, latency and cost together.
- Label simulated data.
- Verify tool versions and prices before you install or quote them.

---

## **16. Interview Answer**

**Question: How do you decide which model to use for a task, and how do you keep that decision safe?**

"I start by treating public benchmarks as a way to shortlist, not to decide. A high score on a general test tells me the model is capable, but it does not tell me it works on my task. I also check how old the benchmark is, whether it is saturated, and what settings the score used. For coding, for example, I would compare a model's score on an older set like SWE-bench Verified with its score on a newer, harder set like SWE-bench Pro. A big drop tells me the first number was flattering.

Then I build my own test set from the real task. For a Text-to-SQL helper I would write about fifty questions with gold queries, label any simulated data honestly, and score with execution match, because that is exact and free. I use an LLM judge only for things code cannot judge, and I check the judge against a human sample.

I run three shortlisted models with the same prompt, parameters and scoring. For reasoning models I fix the effort setting, count the thinking tokens as a separate cost, and run more trials because the results vary. I report quality with an interval, latency at the median and the 95th percentile, and cost with caching and batch pricing included. Then I pick the cheapest model that clears a quality floor and a latency ceiling, not simply the top ranked one.

To keep that decision safe, I turn the cases into a regression suite with component, pipeline and application tests. Everything is versioned, results are compared to a baseline, and the CI gate checks quality, latency and cost together so a gain in one cannot hide a loss in another. After release I log and sample live traffic, and every real failure becomes a new test case."