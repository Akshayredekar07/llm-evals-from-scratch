
### **Case Study 2: Selecting an LLM for a Fintech Customer-Support RAG Assistant**

**Role for this exercise:** You are the AI Engineering Manager at a fictional Indian UPI/fintech app, **"PayZo."** Product has asked for an AI support assistant that can answer user questions about failed transactions, refund status, KYC requirements, and chargeback timelines, by retrieving from PayZo's policy/FAQ knowledge base (RAG) and generating a grounded answer. Your job: pick the one best LLM to power it, using live, current model pricing and benchmark data.

This case study follows the exact same 3-stage process used in the Cricinfo text-to-SQL case study: **(1) gather requirements → (2) shortlist via a leaderboard → (3) run a custom eval.** The difference here is the task (RAG support chat instead of text-to-SQL) and that all pricing/benchmark numbers below are pulled from live sources as of **August 2026** rather than assumed.

---

### **Stage 1: Gather Requirements (as the Manager)**

| Requirement | Decision | Reasoning |
|---|---|---|
| **Task** | RAG-based support chatbot | Retrieve relevant policy/FAQ chunks + conversation context, generate a grounded natural-language answer |
| **Scale** | ~20,000 support queries/day | Estimated from PayZo's active user base and typical support-contact rate for a mid-size fintech app (manager's estimate, would be validated against real support-ticket volume in practice) |
| **Cost ceiling** | ₹5 lakhs/month | Set as the budget for this specific feature — support automation is expected to cut live agent headcount cost, so this ceiling leaves comfortable margin against agent-cost savings |
| **Latency** | 3-4 seconds acceptable | This is a support chat, not a live-event feature — users expect a "typing" response, not instant, but still shouldn't feel stuck |
| **Context window** | Matters moderately | Each request carries retrieved policy chunks + a short conversation history (not single disjoint questions like the text-to-SQL case) — so prompts are longer and models need reasonable context handling |
| **Deployment** | Public API acceptable | No requirement for on-prem/open-weight self-hosting for this exercise, though a real fintech would additionally need to confirm data-residency and RBI compliance with legal before finalizing this |
| **Correctness** | Very high priority | This involves real money — refund policy, KYC steps, dispute timelines. A wrong or hallucinated answer creates real financial/compliance risk, so correctness is weighted heavily over raw speed |

**System Flow Diagram**

```
User question ("why was my refund not credited yet?")
                |
                v
   Retrieve relevant policy/FAQ chunks from PayZo's knowledge base
                |
                v
   Build prompt: [System Prompt + Retrieved Context + Chat History + Question]
                |
                v
                LLM
                |
                v
        Grounded natural-language answer
                |
                v
            Shown to user
```

---

### **Cost Calculation - Step by Step**

**Step 1: Estimate tokens per request**

Unlike the text-to-SQL case (short fixed schema + short question), a RAG support prompt is bigger because it carries retrieved context:

- System prompt: ~150 tokens
- Retrieved policy/FAQ chunks: ~1,500 tokens
- Recent chat history: ~250 tokens
- User question: ~100 tokens
- **Total input ≈ 2,000 tokens**
- Generated answer: ~300 tokens output

**Step 2: Estimate volume**

- 20,000 queries/day × 30 days = **600,000 queries/month**

**Step 3: Cost formula (same formula used in the Cricinfo case study)**

$$\text{Cost per query (USD)} = \frac{(\text{Input Tokens} \times \text{Input Rate}) + (\text{Output Tokens} \times \text{Output Rate})}{10^6}$$

$$\text{Monthly Cost (USD)} = \text{Cost per query} \times \text{Monthly Queries}$$

$$\text{Monthly Cost (INR)} = \text{Monthly Cost (USD)} \times 95$$

**Step 4: Live pricing pulled from current leaderboards (August 2026)**

Model pricing below reflects current published API rates as of late August 2026. Anthropic's current API pricing is $5/$25 per million input/output tokens for Claude Opus 5, $2/$10 for Sonnet 5 (an introductory rate through August 31, 2026), $1/$5 for Haiku 4.5, and $10/$50 for Fable 5. Grok 4.6 offers frontier-tying quality at $2/$6 per million tokens, and GPT-5.6 Sol was cut to $4/$20 on August 21, 2026, moving it under Claude Opus 5 on pricing. OpenAI's GPT-5.6 lineup splits into three tiers — Sol, Terra ($2/$12), and Luna ($0.20/$1.20) — with Terra and Luna both cut further in price on July 30, 2026.

| Model | Input $/M | Output $/M | Source |
|---|---|---|---|
| Claude Opus 5 | $5.00 | $25.00 | Anthropic official pricing (BenchLM.ai mirror) |
| Claude Fable 5 | $10.00 | $50.00 | Anthropic official pricing |
| Claude Sonnet 5 | $2.00 | $10.00 | Anthropic official pricing (introductory rate through Aug 31, 2026) |
| Claude Haiku 4.5 | $1.00 | $5.00 | Anthropic official pricing |
| GPT-5.6 Sol | $4.00 | $20.00 | OpenAI (post Aug 21, 2026 price cut) |
| GPT-5.6 Terra | $2.00 | $12.00 | OpenAI |
| GPT-5.6 Luna | $0.20 | $1.20 | OpenAI |
| Grok 4.6 | $2.00 | $6.00 | xAI |
| Gemini 3.6 Flash | $0.75 | $3.75 | Google (approx., matched to Gemini 3.7 Flash rate) |
| Kimi K3 | $3.00 | $15.00 | Moonshot AI (list price; open-weight, cheaper blended rate available via some hosts) |
| DeepSeek V4 Flash | $0.14 | $0.28 | DeepSeek |

**Step 5: Worked calculation for every model**

$$\text{Cost per query} = \frac{(2000 \times \text{Input Rate}) + (300 \times \text{Output Rate})}{10^6}$$

**Example — Claude Sonnet 5:**

$$\text{Cost per query} = \frac{(2000 \times 2) + (300 \times 10)}{10^6} = \frac{4000 + 3000}{10^6} = \frac{7000}{10^6} = \$0.007$$

$$\text{Monthly Cost (USD)} = 0.007 \times 600{,}000 = \$4{,}200$$

$$\text{Monthly Cost (INR)} = 4{,}200 \times 95 = ₹3{,}99{,}000 \approx ₹3.99 \text{ lakhs}$$

**Full cost table for all 11 candidate models**

| Model | Cost/Query (USD) | Monthly Cost (USD) | Monthly Cost (INR) | Within ₹5L Budget? |
|---|---|---|---|---|
| Claude Opus 5 | $0.0175 | $10,500 | ₹9.98 lakhs | No |
| Claude Fable 5 | $0.0350 | $21,000 | ₹19.95 lakhs | No |
| Claude Sonnet 5 | $0.0070 | $4,200 | ₹3.99 lakhs | Yes |
| Claude Haiku 4.5 | $0.0035 | $2,100 | ₹2.00 lakhs | Yes |
| GPT-5.6 Sol | $0.0140 | $8,400 | ₹7.98 lakhs | No |
| GPT-5.6 Terra | $0.0076 | $4,560 | ₹4.33 lakhs | Yes |
| GPT-5.6 Luna | $0.00076 | $456 | ₹0.43 lakhs | Yes |
| Grok 4.6 | $0.0058 | $3,480 | ₹3.31 lakhs | Yes |
| Gemini 3.6 Flash | $0.0026 | $1,575 | ₹1.50 lakhs | Yes |
| Kimi K3 | $0.0105 | $6,300 | ₹5.99 lakhs | No (close miss) |
| DeepSeek V4 Flash | $0.0004 | $218 | ₹0.21 lakhs | Yes |

**Result of Stage 1 cost filtering:** Claude Opus 5, Claude Fable 5, GPT-5.6 Sol, and Kimi K3 are rejected on cost. **7 models remain within budget**: Claude Sonnet 5, Claude Haiku 4.5, GPT-5.6 Terra, GPT-5.6 Luna, Grok 4.6, Gemini 3.6 Flash, and DeepSeek V4 Flash.

---

### **Stage 2: Shortlist Using a Live Leaderboard (Artificial Analysis)**

Instead of a coding-specific leaderboard (used in the text-to-SQL case), this task calls for a **general intelligence/reasoning leaderboard**, since RAG support chat needs broad comprehension and instruction-following rather than pure coding skill. The **Artificial Analysis Intelligence Index** is used here.

The public Artificial Analysis Intelligence Index snapshot (August 26, 2026) ranks Claude Opus 5 first at 63.0%, ahead of Claude Fable 5 (62.1%) and Grok 4.6 (60.9%) among 181 models. Further down the same index, Sonnet 5 scores 53.35, GPT-5.6 Terra scores 54.95, GPT-5.6 Luna scores 51.24, and Gemini 3.5/3.6 Flash scores around 50.2.

**Step 1: Normalize Intelligence Index score (min-max, 0-1)**

$$\text{Normalized Score} = \frac{\text{Score} - \text{Minimum Score in Set}}{\text{Maximum Score} - \text{Minimum Score}}$$

**Step 2: Normalize throughput (tokens/sec, illustrative estimates for the 7 shortlisted models)**

Note: exact live per-model throughput wasn't pulled for every model in this exercise — the figures below are reasonable relative estimates for illustration, consistent with each model's known tier (flagship vs. lightweight). In a real evaluation you would pull live 7-day rolling throughput numbers directly from Artificial Analysis or llm-stats.com for each candidate.

| Model | Intelligence Index | Throughput (tok/s, est.) |
|---|---|---|
| Claude Sonnet 5 | 53.35 | 85 |
| Claude Haiku 4.5 | ~36 (est., lightweight tier) | 140 |
| GPT-5.6 Terra | 54.95 | 90 |
| GPT-5.6 Luna | 51.24 | 160 |
| Grok 4.6 | 60.9 | 120 |
| Gemini 3.6 Flash | 50.2 | 180 |
| DeepSeek V4 Flash | ~40 (est., lightweight tier) | 200 |

**Step 3: Scoring formula (correctness weighted heavier than speed, since this is a financial support task)**

$$\text{Score} = 0.8 \times \text{Normalized Intelligence Score} + 0.2 \times \text{Normalized Throughput Score}$$

*(Compare to the text-to-SQL case study, which used 0.9/0.1 — here latency gets a bit more weight than in the SQL case because the output is a multi-sentence answer, not a 100-token query, so raw speed has more visible impact on user experience.)*

**Step 4: Normalization worked example — Grok 4.6**

Intelligence scores in set: min = 36, max = 60.9, range = 24.9

$$\text{Normalized Intelligence (Grok 4.6)} = \frac{60.9 - 36}{24.9} = \frac{24.9}{24.9} = 1.00$$

Throughput values in set: min = 85, max = 200, range = 115

$$\text{Normalized Throughput (Grok 4.6)} = \frac{120 - 85}{115} = \frac{35}{115} = 0.304$$

$$\text{Final Score (Grok 4.6)} = (0.8 \times 1.00) + (0.2 \times 0.304) = 0.800 + 0.061 = 0.861$$

**Step 5: Final ranking of all 7 in-budget models**

| Rank | Model | Normalized Intelligence | Normalized Throughput | Final Score | Monthly Cost |
|---|---|---|---|---|---|
| 1 | **Grok 4.6** | 1.000 | 0.304 | **0.861** | ₹3.31 lakhs |
| 2 | **Gemini 3.6 Flash** | 0.570 | 0.826 | **0.621** | ₹1.50 lakhs |
| 3 | **GPT-5.6 Luna** | 0.612 | 0.652 | **0.620** | ₹0.43 lakhs |
| 4 | **GPT-5.6 Terra** | 0.761 | 0.043 | **0.617** | ₹4.33 lakhs |
| 5 | **Claude Sonnet 5** | 0.697 | 0.000 | **0.558** | ₹3.99 lakhs |
| 6 | DeepSeek V4 Flash | 0.161 | 1.000 | 0.329 | ₹0.21 lakhs |
| 7 | Claude Haiku 4.5 | 0.000 | 0.478 | 0.096 | ₹2.00 lakhs |

**Shortlist for custom eval (top 5):** Grok 4.6, Gemini 3.6 Flash, GPT-5.6 Luna, GPT-5.6 Terra, Claude Sonnet 5.

DeepSeek V4 Flash and Claude Haiku 4.5 are dropped despite being extremely cheap — their intelligence scores are too far behind for a task where correctness on financial/policy answers is the top priority. This mirrors the text-to-SQL case study lesson: **cost filtering comes first, but the cheapest surviving option isn't automatically worth testing if its capability score is too weak for a correctness-critical task.**

---

### **Stage 3: Run the Custom Eval**

**Building the golden dataset**

Since this is RAG (not SQL), the golden dataset and correctness check look different from the text-to-SQL case:

- Golden dataset = a set of (user question, retrieved context, correct/expected answer with key facts) triples, written and validated by the support/policy team
- Recommended composition for a support assistant: mix of categories — failed transactions, refund timelines, KYC document requirements, chargeback/dispute process, account freeze reasons — with a mix of easy (single-fact lookup) and hard (multi-step policy reasoning, edge cases) questions
- Example golden dataset size for this exercise: **20 questions**, similar scale to the text-to-SQL case study, across the 5 categories above

**Correctness-checking logic for RAG (different from the SQL table-comparison method)**

Since there's no SQL result table to diff here, correctness for a RAG answer is typically checked with a **key-fact / claim-matching approach**:

1. For every golden question, define the **required facts** the answer must contain (e.g. "refund timeline is 5-7 business days," "requires PAN and Aadhaar for KYC")
2. Generate the model's answer using the full RAG pipeline (retrieval + generation)
3. Check whether the model's answer contains all required facts and does **not** contradict or hallucinate any policy detail
4. This is usually done either manually, or by using a second "judge" LLM prompted specifically to check the generated answer against the required facts (an **LLM-as-judge** setup) — a technique to be covered in a later class on application evals
5. Mark each question as pass/fail based on whether all required facts are present and no hallucination occurred
6. Calculate accuracy = (questions passed) / (total questions) for each model

**Running the eval across the 5 shortlisted models**

```
For each of the 5 shortlisted models:
    For each of the 20 golden questions:
        1. Retrieve relevant policy chunks
        2. Build the full prompt (system + context + history + question)
        3. Send to the model, get generated answer
        4. Check generated answer against required facts (pass/fail)
    Calculate accuracy = passed / 20
Compare accuracy, cost, and latency across all 5 models
```

**Illustrative results (worked example for this case study)**

The table below is an illustrative example of what a completed custom eval might show, following the same format as the Cricinfo case study. These are not live test results — a real evaluation would require actually running each model against PayZo's real policy documents and a validated golden dataset.

| Model | Illustrative Accuracy | Monthly Cost | Notes |
|---|---|---|---|
| Grok 4.6 | ~88% | ₹3.31 lakhs | Strong overall reasoning, but sometimes less precise on multi-step policy edge cases |
| Gemini 3.6 Flash | ~80% | ₹1.50 lakhs | Fast and cheap; occasionally misses nuance in multi-fact answers |
| GPT-5.6 Luna | ~75% | ₹0.43 lakhs | Very cheap, decent for simple lookups, weaker on hard multi-step questions |
| GPT-5.6 Terra | ~85% | ₹4.33 lakhs | Reliable, but costlier than Grok for similar accuracy |
| Claude Sonnet 5 | ~90% | ₹3.99 lakhs | Best accuracy in the set, especially strong at not contradicting policy details (low hallucination) |

**Final Decision (as the Manager)**

- Two realistic finalists: **Claude Sonnet 5** (highest accuracy, strongest at avoiding hallucination on financial/policy facts) and **Grok 4.6** (close second on accuracy, noticeably cheaper)
- Given that this is a **correctness-critical fintech use case** — a wrong refund-policy answer creates real compliance and customer-trust risk — the manager's call here would lean towards **Claude Sonnet 5**, accepting the roughly ₹0.7 lakh/month cost premium over Grok 4.6 in exchange for lower hallucination risk on financial facts
- If PayZo's real budget pressure were tighter, **Gemini 3.6 Flash** would be the pragmatic fallback — noticeably cheaper (₹1.50 lakhs vs ₹3.99 lakhs) for a manageable accuracy trade-off, suitable if paired with a stricter "escalate to human agent" fallback for low-confidence answers
- As in the text-to-SQL case study: this decision should not be treated as final from a 20-question golden set alone. Before shipping, the real next steps would be to (a) expand the golden dataset to 100+ questions covering more edge cases, (b) run multiple evaluation passes for statistical confidence, and (c) pilot the chosen model with a small percentage of real traffic before full rollout

---

### **Key Differences From the Cricinfo Text-to-SQL Case Study**

| Aspect | Text-to-SQL Case | RAG Support Case |
|---|---|---|
| Leaderboard used | Coding leaderboard (llm-stats.com) | General intelligence leaderboard (Artificial Analysis Intelligence Index) |
| Correctness check | Compare SQL execution result tables | Compare generated answer against required facts (LLM-as-judge or manual) |
| Latency weight in scoring | 10% (output is a short SQL query) | 20% (output is a longer conversational answer, latency more visible to user) |
| Prompt size | Small, fixed (schema + short question) | Larger, variable (retrieved context + chat history) |
| Biggest cost driver | Output tokens (blended 4:1 ratio) | Both input (retrieved context) and output tokens |
| Correctness stakes | Public embarrassment risk (wrong cricket stat) | Financial/compliance risk (wrong refund/KYC info) |

---

### **Quick Revision Cheat Sheet**

| Question | Answer |
|---|---|
| Same 3-stage process reused here | Yes — gather requirements → shortlist via leaderboard → custom eval |
| Cost formula | (Input tokens × Input rate + Output tokens × Output rate) / 1,000,000, then × monthly volume × 95 for INR |
| Budget set for this case | ₹5 lakhs/month |
| Models rejected purely on cost | Claude Opus 5, Claude Fable 5, GPT-5.6 Sol, Kimi K3 |
| Leaderboard used for shortlisting | Artificial Analysis Intelligence Index |
| Scoring formula used | 0.8 × normalized intelligence + 0.2 × normalized throughput |
| Top 5 shortlisted for custom eval | Grok 4.6, Gemini 3.6 Flash, GPT-5.6 Luna, GPT-5.6 Terra, Claude Sonnet 5 |
| How correctness is checked in RAG (vs SQL table-diff) | Key-fact/claim matching, often via an LLM-as-judge |
| Manager's final pick | Claude Sonnet 5 (best accuracy/hallucination trade-off for a correctness-critical fintech task) |
| Cheaper fallback option | Gemini 3.6 Flash, if budget pressure is tighter |

---

### **Sources Used for Live Pricing and Benchmark Data (August 2026)**

- Claude API pricing (Opus 5, Sonnet 5, Haiku 4.5, Fable 5): BenchLM.ai — Claude API Pricing, August 2026
- Grok 4.6 / GPT-5.6 Sol pricing and quality comparison: FelloAI — How Much Does AI Cost in 2026
- GPT-5.6 tier pricing (Sol/Terra/Luna) and price-cut history: Swfte.com — AI Model Leaderboard August 2026
- Artificial Analysis Intelligence Index scores (Opus 5, Fable 5, Grok 4.6): BenchLM.ai — Artificial Analysis Intelligence Index Leaderboard, August 2026
- Full Intelligence Index score table (Sonnet 5, GPT-5.6 Terra/Luna, Gemini 3.5/3.6 Flash): BenchmarkList.com — Artificial Analysis Intelligence Index Benchmark Scores