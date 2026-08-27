# **Custom Model Evals**

**Agenda:** How to run a custom model eval.

**Problem Statement:** You are an AI engineer at ESPN Cricinfo. Cricinfo wants to launch a feature ("Ask Cricinfo") where any user can type a cricket question in plain English, and the system converts it into a SQL query, runs it on the database, and returns the answer — replacing the manual analyst team that used to do this live during matches. Your job: **select the one best LLM** to power this system.

---

## **Why This Matters**

- Model evals are of two types: **benchmarks** (test generic LLM capabilities like knowledge, reasoning, math) and **custom model evals** (test LLM performance on *your own* data/task)
- Leaderboards only give you a shortlist of good candidates — they cannot tell you which model is best for *your specific application*
- You can't just say "let's use the top model on the leaderboard" in a company — you need proper reasoning and evaluation before selecting a model

---

## **The Three-Stage Process**

```
Stage 1: Gather Requirements
    (task, cost ceiling, latency, context, deployment, correctness)
                |
                v
Stage 2: Shortlist 5-10 Candidate Models
    (use a leaderboard, filter by cost, rank by capability + latency)
                |
                v
Stage 3: Run Custom Model Eval
    (build golden dataset, test each model on your own task, compare results)
                |
                v
        Pick the Best Model
```

---

## **Stage 1: Gather Requirements**

| Requirement | Answer for this Application | Reasoning |
|---|---|---|
| **Task** | Text-to-SQL generation | LLM converts a natural-language cricket question into a SQL query |
| **Cost ceiling** | ₹3 lakhs / month | Business/product manager sets this budget based on what the feature is worth (a retention play — keeps users on the site longer, which drives ad revenue) |
| **Latency** | 2-3 seconds max | Users are asking questions live during a match out of curiosity; beyond ~3 seconds, users get impatient. Not a research-assistant type task where latency doesn't matter |
| **Context window** | Not a major consideration | Each question is a single, disjoint query — no multi-turn conversation, so context never grows large |
| **Deployment** | Public API is fine (no on-prem/open-source requirement) | No sensitive data involved; public APIs (OpenAI, Anthropic, etc.) are generally more reliable than self-hosted infrastructure |
| **Correctness** | Very high priority | Cricket fans are extremely finicky about records — a wrong answer becomes a viral screenshot and damages brand reputation. Cannot hallucinate |

**System Flow Diagram**

```
User types question (e.g. "who has scored the most runs against Bumrah")
                |
                v
   Text2SQL System: [Schema + System Prompt + Question] --> LLM
                |
                v
        LLM generates SQL query
                |
                v
        SQL runs on Database
                |
                v
        Result shown back to user
```

**System Prompt Template Used**

```
SYSTEM: You are a text-to-SQL generator. Given a database schema,
return a single SQL query that answers it. Use SQLite syntax.
Return only the SQL query, no explanation.

USER Schema:
CREATE TABLE "matches" (
  id, season, city, date, match_type, player_of_match, venue,
  team1, team2, toss_winner, winner, result, result_margin,
  target_overs, super_over, method, umpire1, umpire2
);

CREATE TABLE "deliveries" (
  match_id, inning, batting_team, bowling_team, over, ball,
  bowler, non_striker, batsman_runs, extra_runs, total_runs,
  extras_type, is_wicket, player_dismissed, dismissal_kind, fielder
);

Question: Which bowler has the best economy rate having bowled at
least 500 legal balls?
```

---

## **Cost Calculation - Full Worked Example**

**Step 1: Measure token usage per query**

- Input prompt (system prompt + schema + question) ≈ **400 tokens** (measured using a token counter tool)
- Output (the generated SQL query) ≈ **100 tokens**
- Input : Output ratio = **4:1**

**Step 2: Estimate daily query volume**

- Assumed average: **5,000 questions/day** (traffic is spiky — spikes happen on big match days like CSK vs MI, but this is an average estimate)

**Step 3: Basic monthly cost formula**

$$\text{Cost per query} = \left(\frac{\text{Input tokens} \times \text{Input rate}}{10^6}\right) + \left(\frac{\text{Output tokens} \times \text{Output rate}}{10^6}\right)$$

$$\text{Monthly Cost (USD)} = \text{Cost per query} \times \text{Queries/day} \times 30$$

$$\text{Monthly Cost (INR)} = \text{Monthly Cost (USD)} \times 95 \quad \text{(USD to INR conversion)}$$

**Step 4: Worked example — Claude Fable 5**

- Fable pricing: Input = $10 / million tokens, Output = $50 / million tokens

$$\text{Cost per query} = \frac{400 \times 10}{10^6} + \frac{100 \times 50}{10^6} = \frac{4000}{10^6} + \frac{5000}{10^6} = \frac{9000}{10^6} = \$0.009$$

$$\text{Daily Cost} = 0.009 \times 5000 = \$45$$

$$\text{Monthly Cost (USD)} = 45 \times 30 = \$1350$$

$$\text{Monthly Cost (INR)} = 1350 \times 95 = ₹1,28,250 \approx ₹12.82 \text{ lakhs/month}$$

**Result:** ₹12.82 lakhs/month is roughly **4x over the ₹3 lakh budget** → Claude Fable 5 is rejected. Need a cheaper model (e.g. something in the Claude Sonnet tier, operating around 1x the base cost).

---

## **Cost Optimization: Prompt Caching**

- A large part of the prompt (system prompt + schema) stays **identical across every query** — only the user's question changes
- Model providers let you cache this repeated portion so you don't pay full input price every time
- **How it works:**
  - First query: costs slightly more (e.g. $12.50 instead of $10 per million tokens) because you're paying for input + cache-write
  - Every subsequent query within the cache's active window: costs much less (e.g. $1 instead of $10 per million tokens) since it's a cache hit
- **Cache refresh cycles:**
  - **5-minute cache:** resets if no query comes in within 5 minutes of the last one. Good for high-traffic apps (like Cricinfo, where a question arrives every few minutes)
  - **1-hour cache:** resets after 1 hour of inactivity. Good for lower-traffic apps (e.g. ~1,000 questions/day)
- Internally powered by a concept called **KV caching** (caching the Key/Value vectors used in the attention mechanism)
- **Savings example:** what would cost ~₹12 lakhs/month without caching could drop to roughly ₹6-7 lakhs/month with caching, since only the first query in each cache window pays full input price
- **Limitation:** prompt caching helps a lot when a large fixed portion of the prompt repeats (like this text-to-SQL system prompt + schema). It helps far less in RAG chatbots, where the retrieved context changes on every single query

---

## **Stage 2: Shortlist Candidate Models from a Leaderboard**

**Choosing the leaderboard**

- Ideally you'd use a dedicated text-to-SQL leaderboard, but the ones that exist (BIRD-SQL, Spider, LiveSQLBench) were rejected because:
  - They were **not updated** with the latest models
  - Some included fine-tuned/harness-based models rather than base LLMs, which aren't usable directly
- **Fallback approach:** use a **coding leaderboard** instead, treating "coding capability" as an alias/proxy for "SQL generation capability" (since SQL generation is a coding task)
- Leaderboard used: **llm-stats.com** — a third-party aggregator combining multiple coding benchmarks into one rating, and updated with the latest models (146 models total)

**Step 1: Understand blended pricing**

Many leaderboards show a single blended price instead of separate input/output rates, using a fixed ratio (commonly 4:1 input:output).

$$\text{Blended Price} = \frac{(4 \times \text{Input Rate}) + (1 \times \text{Output Rate})}{5}$$

**Worked example — Claude Fable 5** (Input $10, Output $50):

$$\text{Blended Price} = \frac{(4 \times 10) + (1 \times 50)}{5} = \frac{40 + 50}{5} = \frac{90}{5} = \$18 \text{ per million tokens}$$

Since this application's own input:output ratio (400:100 = 4:1) exactly matches the leaderboard's blended ratio, this single blended number can be used directly for cost calculation without separate input/output math:

$$\text{Monthly Cost} = \frac{(\text{Input Tokens} + \text{Output Tokens}) \times \text{Blended Price}}{10^6} \times \text{Queries/day} \times 30 \times 95$$

**Step 2: Filter by cost**

- Calculated this monthly cost for all 146 models
- Rejected every model whose monthly cost exceeded the budget (₹3-5 lakhs, depending on which budget version is used) — this left roughly 50-60 affordable models

**Step 3: Rank remaining models by capability + latency**

- Two factors considered: **coding/rating score** and **speed (characters/second)**
- Both normalized to a 0-1 range using min-max normalization:

$$\text{Normalized Value} = \frac{\text{Value} - \text{Minimum Value in Column}}{\text{Maximum Value} - \text{Minimum Value}}$$

- Combined into one score using a weighted formula:

$$\text{Score} = 0.9 \times \text{Normalized Rating Score} + 0.1 \times \text{Normalized Latency Score}$$

- **Why 90% weight to capability and only 10% to latency?** Because the model's output here is just a short SQL query (~100 tokens). Even a "slow" model prints 100 characters quickly. Latency would matter far more if the output were a long essay. So correctness/capability is prioritized heavily over raw speed.
- Sort all remaining models by this combined score, descending, to get the top 10 candidates

**Top 10 Shortlisted Models (from the leaderboard exercise)**

| Rank | Model | Benchmark Score | Monthly Cost (INR) | Throughput (chars/sec) | Weighted Score | Notes |
|---|---|---|---|---|---|---|
| 1 | GPT-5.6 Terra | 46.0 | ₹4,47,300 | 57 | 0.909 | Top candidate, expensive |
| 2 | Kimi K3 | 44.9 | ₹4,83,084 | 4 | 0.883 | Very slow throughput |
| 3 | Muse Spark 1.1 | 38.3 | ₹1,65,501 | 266 | 0.823 | US-only, not usable |
| 4 | Grok 4.5 | 40.5 | ₹2,50,488 | 24 | 0.817 | |
| 5 | Claude Sonnet 5 | 40.4 | ₹2,84,760 | 15 | 0.814 | In the 5-10 shortlist |
| 6 | GPT-5.6 Luna | 39.3 | ₹1,78,920 | 22 | 0.798 | Skipped (same family as Terra) |
| 7 | GLM-5.2 | 39.0 | ₹1,21,666 | 9 | 0.791 | |
| 8 | Qwen3.7 Max | 38.9 | ₹1,56,555 | 5 | 0.789 | |
| 9 | MiniMax M3 | 35.4 | ₹42,941 | 171 | 0.761 | Very cheap, not far behind on score |
| 10 | Gemini 3.6 Flash | 32.8 | ₹2,41,542 | 265 | 0.736 | Skipped |

**Note on Muse Spark 1.1:** rejected despite ranking well — this model (Meta's) is only usable within the US, which rules it out for this application.

**Five Models Actually Selected for Testing (live demo)**

1. **GPT-5.6 Terra** — top-ranked candidate, from OpenAI
2. **Kimi K3** — heavily hyped recently (2.7 trillion parameters, open-weight, from Moonshot AI, claimed to rival Fable 5 at 1/3rd the cost)
3. **Grok 4.5** — included out of curiosity
4. **Claude Sonnet 5** — only Anthropic-family model in the shortlist
5. **MiniMax M3** — representative pick among the cheap Chinese open-weight models (GLM, Qwen, MiniMax)

(GPT-5.6 Luna and Gemini 3.6 Flash were skipped — Luna was skipped because Terra, from the same family, would likely outperform it anyway.)

---

## **Stage 3: Run the Custom Model Eval**

**The 12-Step Implementation Process**

```
1.  Get the dataset (IPL data, 2008-2024, from Kaggle)
2.  Load/filter the data into a database (SQLite; trimmed to 2020-2024)
3.  Extract the database schema (tables, columns, types)
4.  Build the golden dataset (20-50 questions, written/validated by
    a data analyst or LLM-assisted)
5.  Validate the golden dataset (run each golden query, catch SQL errors)
6.  Store the golden dataset in CSV format
7.  Check the end-to-end flow (send 1 test question through the
    full pipeline to confirm it works)
8.  Pick candidate models (map each model to its API identifier,
    e.g. via OpenRouter)
9.  Build the evaluator (logic to compare generated SQL's result
    against the golden SQL's result)
10. Build the orchestrator (main script that loops through models
    and questions)
11. Run all the models (execute the full evaluation)
12. Make the decision (compare final accuracy/cost/latency and
    select the best model)
```

**Step-by-step detail**

**1-3: Data setup**
- Downloaded full IPL ball-by-ball dataset (2008-2024) from Kaggle
- Trimmed to 2020-2024 to keep the evaluation simpler/faster
- Loaded into a SQLite database with two tables: `matches` and `deliveries`
- Extracted the schema into a `schema.sql` file — this schema is what gets embedded in the system prompt so the LLM knows the table/column structure

**4-6: Building the golden dataset**
- A golden dataset = a set of (question, correct SQL query) pairs, ideally written/validated by a human data analyst
- Best practice: keep the question distribution representative of real user questions — e.g. out of 50 questions: 10 easy, 20 medium, 20 hard, and vary query types (joins, subqueries, window functions, etc.)
- In this class: 20 deliberately **hard/"brutal"** questions were used (not fully representative, but useful to expose differences between models)
- Each golden query was run against the database to confirm it executes without SQL errors before being trusted as "ground truth"
- Final golden dataset stored as a CSV with: question, golden SQL query, expected row count, and whether row order matters (i.e. whether an `ORDER BY` clause is required)

**7: Flow check**
- Before testing all 5 candidate models, one full end-to-end test was run with a throwaway model (GPT-4o) just to confirm: question → prompt → LLM → SQL query pipeline works correctly

**8: Candidate model setup**
- All 5 models were accessed through **OpenRouter** — a single platform/API that provides access to models from many different providers (OpenAI, Anthropic, Grok, Chinese open-weight models, etc.), integrates directly with LangChain (`ChatOpenRouter`), and avoids writing separate integration code per provider
- Each model mapped to its OpenRouter "slug" (identifier) in a small lookup list

**9: Building the evaluator — how correctness is checked**

Correctness is checked by **comparing query results, not query text**, because multiple different SQL queries can produce the same correct result (string/character matching would incorrectly fail valid alternate queries).

**Comparison logic:**
1. Run the **golden query** on the database → get Table A
2. Run the **LLM-generated query** on the database → get Table B
3. Check if `#rows in Table A == #rows in Table B` — if not, immediately mark as incorrect
4. **Normalize values** in both tables (e.g. treat `2.0` and `2` as equal; treat `2.999` and `2.99` as equal where appropriate)
5. Convert both tables' rows into lists of tuples
6. If the query is **not order-sensitive** (no `ORDER BY` needed): sort both lists before comparing, since row order may legitimately differ between two valid queries
7. If the query **is order-sensitive** (an `ORDER BY` clause is required): compare without sorting — if it matches without sorting, both the values and the order are correct
8. If Table A == Table B after this process → the generated query is **correct**; otherwise it's **incorrect**

**10-11: Orchestration and running**
- The `main.py` orchestrator: loads schema, loads golden dataset, connects to database, then for each of the 5 models — loops through every golden question, sends it to the model, executes the generated SQL, executes the golden SQL, and calls the evaluator to mark match/mismatch
- Cost consideration: with 5 models × 20 questions = 100 LLM calls in this demo. At larger scale (e.g. 5 models × 500 questions = 2,500 calls), evaluation itself starts costing real money — so golden dataset size is also a budget trade-off (typical range: 50 to 500 questions)

**12: Final Results from the Live Evaluation**

| Model | Accuracy | Observation |
|---|---|---|
| **GPT-5.6 Terra** | ~80-95% | Strong performance, but most expensive to run |
| **Kimi K3** | ~50-55% | Multiple SQL syntax errors; also very slow (heavy reasoning model). Despite huge hype/media buzz, underperformed badly on this specific task — a strong lesson that leaderboard hype does not guarantee task-specific performance |
| **Grok 4.5** | ~90% | No SQL errors at all; fast; ended as one of the two finalists |
| **Claude Sonnet 5** | ~85% | Very fast, no SQL errors; ended as the other finalist |
| **MiniMax M3** | ~65% | Cheapest by far, but noticeably more SQL errors than the American models |

**Final Decision**

- Two finalists: **Grok 4.5** and **Claude Sonnet 5** — close in accuracy, cost, and speed
- Personal lean: towards **Claude Sonnet 5**, based on perceived reliability of Anthropic's API/infrastructure rather than raw benchmark numbers alone
- When a team genuinely can't decide between very close finalists, an internal **team vote** is also a legitimate way to break the tie
- Important caveat: 20 questions is a small dataset — each question carries 5% weight on accuracy. Ideally the golden dataset should be larger, and for more statistical confidence you can run the full evaluation multiple times (e.g. 5 runs) and average the results, since each API call is independent

---

## **Key Lessons from This Case Study**

- **Leaderboards filter, custom evals decide.** A model topping a general leaderboard (like Kimi K3 did) can still perform poorly on your specific task.
- **Cost, latency, and correctness must all be defined as explicit requirements before touching a leaderboard** — this prevents bias toward whatever model is ranked #1.
- **Weighting in your scoring formula should reflect your actual task.** Here, latency got only 10% weight because the output (a short SQL query) is small regardless of which model generates it.
- **Prompt caching can meaningfully cut cost** when a large, fixed portion of your prompt (like a schema-heavy system prompt) repeats across most queries.
- **Correctness must be checked by comparing execution results, not exact text**, since multiple valid SQL queries can produce the identical correct answer.
- **Small differences between finalists (like Grok 4.5 vs Claude Sonnet 5) may come down to non-benchmark factors** — API reliability, vendor trust, existing infrastructure — not just the raw accuracy number.

---

## **Quick Revision Cheat Sheet**

| Question | Answer |
|---|---|
| Two types of model evals | Benchmarks (generic capability) and Custom Model Evals (task-specific) |
| Three-stage model selection process | 1. Gather requirements → 2. Shortlist via leaderboard → 3. Run custom eval |
| Blended price formula (4:1 ratio) | (4 × Input Rate + 1 × Output Rate) / 5 |
| Normalization formula | (Value − Min) / (Max − Min) |
| Scoring formula used in this case study | 0.9 × Normalized Rating + 0.1 × Normalized Latency |
| Why low weight on latency here | Output is a short SQL query (~100 tokens); speed barely matters for such small outputs |
| How correctness is verified | Run both golden and generated SQL on the DB, compare result tables (with/without sorting depending on ORDER BY sensitivity) |
| Platform used to access multiple model APIs in one place | OpenRouter |
| Final two candidates | Grok 4.5 and Claude Sonnet 5 |
| Biggest surprise in the results | Kimi K3 — heavily hyped on release, but weak accuracy and slow speed on this specific task |