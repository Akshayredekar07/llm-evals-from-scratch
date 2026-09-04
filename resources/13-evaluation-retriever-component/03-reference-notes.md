# **Building and Evaluating the Retriever**

## 1. Session Goal

- Complete **component-level eval** — starting with the **retriever** (generator is next session)
- Two core RAG components:
  - **Retriever** — fetches relevant context for a query
  - **Generator** — produces an answer from query + context

## 2. Project Setup

**Folder structure:**
```
rag_eval_project/
├── data/     → lecture transcripts (knowledge base)
├── src/      → retriever.py, generator.py, rag_pipeline.py, UI code
├── evals/    → all evaluation pipelines
└── goldens/  → golden datasets
```

**Setup steps:**
- Transcripts (first ~8-9 sessions) copied into `data/`
- Virtual environment created with **UV**, Python 3.11
- Libraries installed: LangChain, OpenAI, DeepEval, Pytest, python-dotenv
- `.env` file created with OpenAI API key

## 3. Building the Retriever

**Core principle**: never build the whole app then test — build one component, test it, then move to the next (same as software dev: module → test → next module).

**Retriever mechanics:**
1. Query → converted to a vector via embedding model
2. Vector database (Chroma) searched for nearest K vectors
3. Nearest chunks returned = "context"

**Build pipeline (`retriever.py`):**

| Step | Detail |
|---|---|
| Load transcripts | Read `.txt` files line by line |
| Remove timestamps | Timestamp lines dropped — keeping them would badly hurt semantic quality |
| Track session metadata | Each line tagged with its session number (enables future citations) |
| Chunking | Chunk size = 750, overlap = 100 (initial, deliberately small) |
| Embedding | Model = `text-embedding-3-small` (OpenAI) |
| Vector DB | Chroma (`chroma_store` directory) |
| Retriever object | `as_retriever()`, K = 5 |

- First run creates the vector DB (takes time); later runs reuse it
- **Handling new documents**: add new transcript → delete `chroma_store` → rerun `retriever.py` (data ingestion is currently coupled with retrieval — acceptable since the focus here is evaluation, not production-grade engineering)
- Code intentionally kept simple/basic to keep focus on evaluation concepts, not production architecture

## 4. How a Retriever Fails — 2 Failure Modes

| Failure Mode | Description | Corresponding Metric |
|---|---|---|
| 1. Misses correct context | Retriever fails to bring back some/all of the actually-correct chunks | **Recall** |
| 2. Brings noise | Retriever brings correct chunks but also irrelevant ones | **Precision** |

**Definitions:**
- **Recall** = (correct chunks retrieved) / (total correct chunks that exist)
- **Precision** = (correct chunks retrieved) / (total chunks retrieved)

**Trade-off**: increasing K almost always increases recall but decreases precision (more results = more chances to catch correct ones, but also more noise). Ideal retriever = high recall AND high precision — hard to achieve both together.

**Reference-based check**: both recall and precision are **reference-based evaluations** — they need a golden dataset/golden context to know what "correct" looks like.

## 5. Golden Dataset — Wrong Approach vs Right Approach

### Wrong Approach: (Question, Chunk/Document IDs)

- Structure: Question column + correct-chunk-ID column
- Recall/precision calculated by comparing retrieved chunk IDs against the listed correct IDs

**Why it fails for most real RAG apps:**
1. **Not scalable to create** — someone must manually read a question and scan hundreds of chunks (e.g., 800+) to mark the correct ones, repeated for every question. Extremely tedious.
2. **Breaks on any chunking change** — changing chunk size/overlap regenerates all chunks with new IDs → the entire golden dataset becomes void → must be rebuilt from scratch every time parameters are tuned

**When it CAN work**: if documents are cleanly separated and chunking parameters are fixed and never tweaked (not the case here, since info spreads across sessions).

### ✅ Correct Approach: (Question, Ideal Answer) + LLM-as-Judge

- Structure: Question column + **Ideal Answer** column (answer based on actual course content, not Google)
- Big advantage: the **ideal answer never changes**, even if chunking parameters change → no need to rebuild the golden dataset when tuning chunk size, K, embedding model, etc.

**Calculating Recall (a.k.a. Contextual Recall in DeepEval):**
1. Send question to retriever → get K retrieved chunks
2. LLM-as-judge breaks the ideal answer into **atomic claims**
3. LLM checks each retrieved chunk for the presence of each claim
4. Recall = (claims found across retrieved chunks) / (total claims in ideal answer)
5. Repeat for all questions, average → overall Contextual Recall

**Calculating Precision (a.k.a. Contextual Precision in DeepEval):**
1. Same retrieved chunks
2. LLM-as-judge checks each chunk individually: "Does this chunk help produce the ideal answer? Yes/No"
3. Basic precision = (chunks marked useful) / (total chunks retrieved)
4. **Rank-aware refinement**: precision is computed cumulatively at each rank position (1, 2, 3...) and then averaged — this rewards retrievers that rank correct chunks higher, even when the raw precision ratio is identical between two retrievers

> Example: Case A (correct, correct, noise, noise, noise) scores a higher average contextual precision than Case B (noise, noise, noise, correct, correct) — even though both have the same 2/5 basic precision — because A ranks the correct ones first.

## 6. Methods to Build a Golden Dataset

| Method | Description | Pros | Cons |
|---|---|---|---|
| 1. Hand-authored | Fully manual, based on real subject knowledge | Most accurate | Not scalable |
| 2. LLM-assisted drafting (used here) | Upload transcripts to an LLM, generate Q&A pairs one at a time, human reviews carefully | Fast, low cost/effort | Risk of LLM inventing content not actually taught |
| 3. DeepEval Synthesizer module | Automated dataset generation from chunks | Built into DeepEval | Poor question quality in practice (unnatural phrasing, irrelevant focus) — not used for this project |
| 4. Mined from production logs | Positive-feedback interactions (thumbs up) added as golden entries | Real user language | Can't be the starting method — need initial entries first |

- **Method actually used**: #2 — 15 questions generated one at a time via LLM, manually reviewed, saved as `retriever_goldens.json`

## 7. DeepEval Code Structure (3 Core Concepts)

| Concept | Meaning |
|---|---|
| **LLM Test Case** | Represents ONE row of the golden dataset (input, expected output, retrieval context, actual output) |
| **Metric** | What dimension to evaluate (e.g., Contextual Recall, Contextual Precision, Answer Relevancy). Configurable: judge LLM, threshold, `include_reason=True` |
| **`evaluate()` function** | Runs the metric(s) against the test case(s), returns scores |

**Eval script logic (`eval_retriever.py`):**
1. Load golden dataset JSON (15 rows)
2. Loop over each row → call retriever → get 5 context chunks
3. Build an `LLMTestCase` per row: input (question), expected_output (ideal answer), retrieval_context (retrieved chunks), actual_output (placeholder, since generator not built yet)
4. Define metrics: `ContextualRecallMetric`, `ContextualPrecisionMetric` (with threshold, judge model, include_reason)
5. Call `evaluate(test_cases, metrics)`

**Common setup gotcha**: running the eval script directly from inside `evals/` causes `ModuleNotFoundError: No module named 'src'`. Fix: add `__init__.py` to both `src/` and `evals/`, then run as a module:
```
python3 -m evals.eval_retriever
```

## 8. Iterative Improvement Log

| Run | Change Made | Contextual Recall | Contextual Precision | Failed Test Cases (of 15) |
|---|---|---|---|---|
| Baseline | Chunk size 750, overlap 100, K=5 | 80 | 80 | 5 |
| Run 2 | Chunk size → 1000, overlap → 150 | 97 | 83 | 3 |
| Run 3 | + Reranker added | slightly lower | 85 | 2 |
| Run 4 | + Embedding model upgraded to `text-embedding-3-large` | 99 | 85 | 3 |
| Run 5 | K reduced 5 → 3 | — | 84 (dropped slightly) | — |

**Key levers for improving retriever quality:**
- **Chunk size / overlap** — bigger chunks captured more complete context here, boosting recall significantly
- **Reranker** — reorders retrieved chunks so meaningful ones rank higher → improves rank-aware (contextual) precision
- **Embedding model quality** — upgrading to a larger embedding model improved recall further
- **K value** — a trade-off lever; lowering K didn't meaningfully help precision here
- Note: with only 15 rows in the golden dataset, some run-to-run variance is expected even with identical settings

**Final state achieved**: Recall 95+, Precision ~85 — considered a good retriever.

**Remaining ideas not yet tried**: better-quality reranker model, larger chunking settings (e.g., 1500/200).

## 9. Where This Leaves Us

- ✅ Retriever built
- ✅ Retriever evaluated (Contextual Recall + Contextual Precision, using golden dataset + LLM-as-judge)
- ✅ Retriever improved iteratively
- ⏭ Next: build and evaluate the **Generator** (next session)

## Quick Reference: Key Terms

| Term | Meaning |
|---|---|
| Recall | % of correct/needed info actually retrieved |
| Precision | % of retrieved info that's actually useful |
| Contextual Recall | LLM-as-judge recall using claim-matching against an ideal answer |
| Contextual Precision | LLM-as-judge precision, rank-aware |
| Golden Dataset | Reference dataset used for reference-based evals |
| LLM as a Judge | Using an LLM to score/evaluate outputs instead of manual/programmatic scoring |
| Reranker | Component that reorders retrieved chunks by relevance |
| K | Number of chunks retrieved per query |