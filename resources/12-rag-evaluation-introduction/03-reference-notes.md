# **RAG Evaluation Strategy**

## **1. Where This Fits in the LLM Eval Playlist**

- LLM Eval has two branches:
  - **Model Eval** (already covered)
    - Standardized eval → benchmarks (knowledge/capability based)
    - Custom model eval → your own dataset for your own use case
  - **Application Eval** (starting now, main focus of playlist)
- Other concepts already covered: reference based vs reference free eval, online vs offline eval

## **2. Types of LLM Based Applications**

| Type | Example |
|---|---|
| Simple chatbot | Plain Q&A bot |
| RAG based chatbot | Retrieval + generation |
| Agent | Tool-using autonomous system |
| Multimodal app | Image generator |
| Fixed schema output app | Email classifier (support/refund/technical) |

- Only **RAG** and **Agents** will be taught in depth (most common in production)
- Simple chatbot / fixed schema output → considered easy, left for self-study
- Multimodal → different, not necessarily harder, but less common in production

## **3. Case Study: CampusX Doubt Solver**

- **Problem statement**: build a RAG chatbot for the LLM course only
- **Data source**: lecture transcripts (available for every lecture)
- **Flow**: transcripts → documents → fed to LLM → students ask doubts about the playlist
- Kept deliberately simple — goal is to master *evaluation*, not build a complex RAG system

## **4. The Three-Level Evaluation Framework**

> Core rule: any LLM based application is evaluated at 3 levels — **Component → Pipeline → Application**

### **Level 1: Component Level**

Evaluate retriever and generator **in isolation**, before connecting them.

**Step 1 – Build Retriever**
- Load documents → chunk → embed → store in vector DB → retrieve top-k on query

**Step 2 – Evaluate Retriever**
- **Recall** — of all correct/relevant docs, how many were retrieved
- **Precision** — of all retrieved docs, how many were actually relevant

**Step 3 – Build Generator**
- LLM that takes (question + context) → produces answer
- Built independently, context supplied manually (golden data), not yet from retriever

**Step 4 – Evaluate Generator**
- **Faithfulness** — is the answer grounded in the given context, or hallucinated
- **Relevance** — is the answer relevant to the question
- **Citation accuracy** — does it correctly cite the source (session/transcript link)

✅ Component level done once both retriever and generator pass evaluation independently.

### **Level 2: Pipeline Level**

**Step 5 – Build RAG Pipeline**
- Connect retriever + generator together

**Step 6 – Evaluate with the RAG Triad**

Three entities exist: **Question, Context, Answer** → one metric per pair:

| Pair | Metric | Meaning |
|---|---|---|
| Question ↔ Context | **Context Relevance** | Is retrieved context relevant to the question |
| Context ↔ Answer | **Faithfulness** | Is the answer grounded in context (no hallucination) |
| Question ↔ Answer | **Answer Relevance** | Is the answer relevant to the question |

- Together these three = **RAG Triad**
- Passing all three → pipeline level done

> Key idea: build and evaluate happen *together*, step by step — same as software engineering unit → integration → system testing. Not "build everything, then test at the end."

### **Level 3: Application Level**

**Step 7 – Quality Metrics**
- **Correctness** — is the answer factually correct
- **Completeness** — does it address *all* parts of a multi-part question
- **Style** — does the tone/explanation style match CampusX instructors

**Step 8 – Safety Metrics**
- Toxicity check
- PII (personally identifiable information) leakage check
- Jailbreak resistance check

**Step 9 – Ops Metrics**
- Latency
- Cost per query
- Token consumption

### **Summary Table — Eval Suite**

| Level | What's Tested | Key Metrics |
|---|---|---|
| Component | Retriever, Generator (isolated) | Recall, Precision, Faithfulness, Relevance, Citation Accuracy |
| Pipeline | Retriever + Generator connected | RAG Triad: Context Relevance, Faithfulness, Answer Relevance |
| Application | Full system | Correctness, Completeness, Style, Safety, Ops (latency/cost/tokens) |

- All test files together = **Eval Suite**
- Some evals need a **golden dataset**; some don't

## **5. Tooling: DeepEval (chosen over Ragas)**

- Library used to implement all metrics above without writing custom code
- Syntax based on **Pytest** (Python's standard testing framework) → familiar if you know Pytest
- Already supports: answer relevancy, faithfulness, contextual precision/recall, contextual relevancy, toxicity, PII leakage

**Why DeepEval over Ragas:**
1. Ragas already covered in the Advanced RAG course
2. DeepEval has broader scope — works for agents, multi-turn chatbots, non-LLM apps, image-based apps
3. Expected to become an industry-standard benchmark library

## **6. Regression Testing**

**Definition**: running the full eval suite on the application to compare a new version against a previous baseline.

**Why it matters**: confirms objectively whether a new version is better/worse than the last, before deciding to deploy.

### Project Structure

```
project/
├── src/              → retriever.py, generator.py, rag_pipeline.py, API/UI code
├── evals/            → eval_retriever.py, eval_generator.py, eval_pipeline.py,
│                        eval_application.py, eval_safety.py, eval_ops.py
└── run_evals.py      → runs all eval files, generates full comparison report
```

### **Three Levels of Regression Testing**

| Level | Description | Tooling |
|---|---|---|
| **1. Basic** | Run once → get baseline numbers → manually compare on every re-run | None, manual |
| **2. Experiment Tracking** | Log configs + metric values per run → visualize on dashboard | MLflow / Confident AI / Weights & Biases |
| **3. CI/CD Gating** | Auto-run eval suite on every push → compare to baseline → auto block/allow deployment based on threshold | GitHub Actions (or similar CI tool) |

- CI/CD flow: push code change → eval suite triggers → compare vs baseline (e.g., threshold: not more than 3 points worse) → deploy if better, block if worse
- **Key principle**: focus on the *concept*, not a specific tool — no LLM-eval tool is a de facto standard yet (unlike MLflow for classic ML)

## **7. Online Evaluation (Post-Deployment)**

Evaluation does not stop after deployment. Four things are done:

1. **Capture Signals**
   - Latency, cost, thumbs up/down feedback per interaction
   - Tools: LangSmith, LangFuse, Confident AI
   - Concept name: **Tracing / Observability**

2. **Calculate Online Metrics**
   - Same offline metrics (faithfulness, relevance, correctness) recomputed live on production traffic

3. **Drift Detection**
   - Track a metric (e.g., faithfulness) over a rolling window (e.g., last 24 hours)
   - Sudden drop → drift detected → trigger alert → investigate/fix

4. **Self-Improving Loop**
   - Capture real production failures (bad chatbot responses)
   - Add them into the offline/golden dataset
   - Improves future offline evaluation and next model iterations

## **8. Full Roadmap (Next 4 Sessions)**

| Session | Focus |
|---|---|
| 1 | Component level eval — build + evaluate retriever, then generator (first hands-on use of DeepEval) |
| 2 | Build RAG pipeline + run RAG Triad metrics |
| 3 | Full application level evaluation |
| 4 | Regression testing + online evaluation |

## **9. Interview Answer Template — "How do you evaluate your RAG chatbot?"**

Use this structured answer:

1. **"I build an evaluation suite at three levels."**
   - Component level → retriever (recall, precision) + generator (faithfulness, relevance, citation accuracy)
   - Pipeline level → RAG Triad (context relevance, faithfulness, answer relevance)
   - Application level → correctness, completeness, style + safety (toxicity, PII, jailbreak) + ops (latency, cost, tokens)

2. **"Then I run regression testing"** using one of three levels (basic / experiment tracking / CI-CD) depending on company maturity.

3. **"Once I have a new baseline, I deploy — but evaluation continues online"**: tracing/observability, live metric recalculation, drift detection.

4. **"Errors caught in production feed back into my offline golden dataset"** for continuous improvement.

> Common mistake: most candidates just list 3–4 metric names (recall, precision, answer relevance) and stop there. Answering with the full structured framework signals depth of understanding and hands-on experience.