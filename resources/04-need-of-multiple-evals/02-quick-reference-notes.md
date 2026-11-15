# **LLM Evals - Revision Notes**

One LLM application usually needs **more than one eval pipeline**. There are two reasons:

1. There are multiple failure points.
2. There are multiple risk categories.

---

## **Reason 1: Multiple Failure Points**

### **Example: RAG chatbot**

Flow: Query -> Retriever -> Vector DB -> Retrieved documents + Query -> Generator (LLM) -> Answer

| Component | What to check |
|---|---|
| Retriever | Given a query, did it fetch the right, relevant documents? |
| Generator | Is the answer faithful (grounded) to the given context? No extra facts added. |

### **Why component evals alone are not enough**

- Retriever has K = 5, so it returns the top 5 documents.
- Only the 5th document has the right answer ("ML course is 8 weeks").
- The first 4 documents are irrelevant, and one of them mentions a Python course of 6 weeks.
- The generator gives more weight to the top documents, so it answers "6 weeks".

Result:

- Retriever: worked (right document was in the top 5).
- Generator: worked (did not make up facts, followed its prompt).
- Final answer: **wrong**.

Fix: add a **reranker** so the best document moves to the top. We only find this problem with a **workflow-level eval**.

### **Workflow evals are still not enough**

Even if the retriever, generator and workflow all pass, the app can still be too slow (for example, 10 seconds per answer). So we also need an **application-level eval** (latency and similar checks).

### **Three levels of failure points**

| Level | What it covers | Examples |
|---|---|---|
| Component | Each part on its own | System prompt, retriever, reranker, query rewriter, embedding model, vector DB, output parser, tool selector, memory, guardrails |
| Workflow | How parts work together | RAG workflow, agent workflow, multi-turn chat workflow |
| Application | The whole app | Latency, token cost per query, time to first token |

---

## **Reason 2: Risk Categories**

Each failure point (component, workflow, application) can fail in different ways. For example:

- **Application:** Answer must be correct and helpful, and also safe (no leaking another user's phone or email).
- **Workflow:** Answer must be grounded, and also not cost too much.
- **Component:** Retriever must fetch the right documents, and also do it fast.

### **Three broad risk categories**

| Category | Question it answers |
|---|---|
| Application Quality | Does the app do its job well? Are answers correct, relevant and complete? |
| Safety | Is the output harmless? |
| Operations | Can it run fast, cheap and reliably when deployed? |

### **Application Quality risks**

| App type | Risks |
|---|---|
| General LLM app (for example, summarizer) | Correctness and accuracy, relevance, completeness, instruction following (format, length) |
| RAG | Context relevance, retriever recall, groundedness / faithfulness, citation accuracy |
| Agent | Tool selection, parameter correctness, task completion, error recovery |
| Multi-turn chatbot | Context retention, clarification behavior |

### **Safety risks**

- Toxicity
- Harmful content (self-harm, weapons, illegal activity)
- Bias (same quality of answer for every user)
- Privacy (no leaking personal data like card or contact details)
- Prompt injection and jailbreak resistance

### **Operational risks**

- Latency
- Cost per request
- Token efficiency
- Error / failure rate
- Latency under load

---

## **Summary**

- Build **different eval pipelines** for different risk categories. For example: one for correctness, one for safety, one for latency.
- Almost every real LLM app has **more than one eval pipeline**, because of:
  1. Multiple failure points (component, workflow, application).
  2. Multiple risk categories (quality, safety, operations).