### **AI Evals Roadmap: LLMs, RAG and Agents**

Last reviewed: 31 October 2026.

---

### **1. The Core Idea**

Strong teams stop vibe-checking and run one loop: read real traces, name each failure mode, turn confirmed failures into test cases, grade with cheap code checks first and calibrated LLM judges second, keep a small human-labelled set to prove the judge can be trusted, run the suite in CI as a release gate, monitor production with online evals and A/B tests, and feed new failures back into the dataset.

The loop is: analyse, measure, improve, automate, repeat.

Trends that are now standard practice:

- **Error analysis before metrics.** Failure-specific binary pass/fail checks replace generic "helpfulness" scores.
- **Outcome-first agent grading.** Grade what the agent produced and the final environment state. Use trajectory data to debug, not as a rigid pass condition (see Phase 4).
- **Evals attached to traces.** Eval scores live on the same spans as the LLM and tool calls (see Phase 5).
- **Closing the loop.** Production failures flow into datasets; coding agents propose fixes that the eval suite verifies, with humans owning the release decision.
- **Protocol-neutral evals.** Agents now talk to tools over MCP and to other agents over A2A, so evals must not be tied to one framework.

The interview question this prepares you for: "How would you know your system works?" A strong answer names five things: a versioned test set, code and judge graders, a judge calibrated against human labels, an offline regression gate in CI, and online monitoring that feeds failures back into the test set.

---

### **2. Practices to Copy from High-Growth Teams**

- **Start from error analysis.** Read real traces, name failure modes, then build evals for those failures.
- **Code checks first.** Regex, schema, parse and import checks cost nothing and never flake. Use a judge only for subjective qualities.
- **Binary, per-criterion judges.** One judge per dimension, pass/fail plus a short reason, with an "unknown" option when evidence is insufficient.
- **Calibrate every judge** against hand-labelled traces and re-calibrate whenever the rubric or the judged model changes.
- **Grade outcomes, not the path.** Agents often find valid approaches the designer did not anticipate. Checking an exact tool sequence is brittle and punishes valid solutions.
- **Read transcripts.** Spot-check traces to confirm graders are fair and to catch graders that can be gamed.
- **Run several trials per task.** Agents are non-deterministic. Report pass@k and pass^k.
- **Simulate users with fixed fixtures.** Simulated personas plus recorded tool payloads give repeatable multi-turn runs.
- **Keep two suites.** Regression evals should stay near 100%. Capability (frontier) evals show headroom and graduate to regression once saturated.
- **Offline gate, then online A/B.** Pass offline thresholds first, then ramp traffic and watch resolution rate, CSAT and cost.
- **Every production failure becomes a regression case.** An LLM can read raw failure reasons and propose categories; humans confirm.
- **Measure efficiency after correctness:** steps, tool calls, tokens, latency and cost against an ideal path.
- **Tag each eval with the behaviour it tests.** Targeted evals beat more evals.
- **Know judge limits.** Judges need calibration, cost money at scale and cannot find patterns across millions of events.
- **Start early.** Evals get harder to build the longer you wait, because you end up reverse-engineering success criteria from a live system.

---

### **3. Core Vocabulary**

- **Task / test case:** an input with success criteria. **Trial:** one attempt; run several because outputs vary.
- **Grader (scorer):** logic that scores output. Types: code-based, model-based (LLM judge), human.
- **Transcript / trace / trajectory:** the full record of a run, including tool calls and reasoning.
- **Outcome:** the final state of the environment (for example, a refund row exists in the database). It can differ from what the agent claims.
- **Eval harness:** infrastructure that runs tasks, records, grades and aggregates. **Agent harness:** the scaffold that lets the model act as an agent. You evaluate both together.
- **Offline eval:** a curated dataset run before shipping. **Online eval:** scoring live traffic. **Ad-hoc:** exploring traces by hand.
- **Regression eval vs capability eval:** the first should stay near 100%; the second measures headroom.
- **pass@k:** at least one of k trials succeeds (can it ever do it). **pass^k:** all k trials succeed (can you rely on it). pass^k was popularised by tau-bench.
- **Judge TPR / TNR:** how often a judge correctly passes good outputs and fails bad ones, measured against human labels.
- **Reference-based vs reference-free:** the first needs a golden answer; in the second the judge decides without one.
- **Span-attached eval:** an evaluation score written onto a trace span so quality and telemetry sit in the same record.

---

### **4. The Roadmap**

Phases are ordered by dependency, not by time. Move on when you can show the proof-of-learning item for the current phase.

#### **Phase 0: Foundations**

- Python, pytest, JSON/JSONL, basic SQL (you will query traces).
- Statistics you actually need: sampling, confidence intervals on a pass rate, comparing two runs (paired tests or bootstrapping), why 20 examples cannot prove an improvement, power analysis basics, Cohen's kappa for judge-human agreement.
- Classic ML evaluation refresher: precision, recall, F1, confusion matrix, train/dev/test splits and leakage.
- **Proof of learning:** build a 30-item dataset by hand for a small LLM feature and report the pass rate with a confidence interval.

#### **Phase 1: LLM Application Evals**

1. **Error analysis first.** Collect 50-100 real or realistic traces, read them, write short notes on what went wrong, group them into a failure taxonomy (open coding, then categories). Only then decide what to measure.
2. **Choose the grader per failure.** Code for deterministic things (schema validity, required fields, tool arguments, regex, latency). LLM judge for subjective ones (tone, policy adherence, completeness). If an assertion can do it, use the assertion.
3. **Write binary, single-criterion judges.** A clear definition, a few examples, and an "unknown" escape hatch. Prefer pass/fail plus a short reason over 1-10 scores.
4. **Calibrate the judge.** Hand-label 100-200 items, split into dev and held-out, report TPR/TNR or agreement, iterate on the prompt, and re-check periodically. Know the biases: position, verbosity, self-preference, leniency. Use a different model family for judging where practical.
5. **Build datasets in layers.** Golden set (human-verified), regression set (from past failures), synthetic set (generated for coverage, then reviewed), adversarial set. Version them and keep a held-out split.
6. **Know the metric families.** Exact match, BLEU/ROUGE (weak for open-ended output), embedding similarity, rubric judges, safety and toxicity, format adherence, latency, cost per task.
7. **Evaluate prompts, not just models.** Treat system prompts, tool descriptions and few-shot examples as versioned artefacts with their own regression tests.

**Proof of learning:** a small eval suite for a chatbot or extraction feature with 5 code checks and 2 calibrated judges, with judge TPR/TNR reported.

#### **Phase 2: Model Evals, Benchmarks and Eval Suites**

1. **Why vibe testing fails.** Study real failures such as the Air Canada chatbot case, where the airline was held responsible for wrong policy information its chatbot gave. Contrast deterministic software tests with probabilistic LLM systems.
2. **Model evals vs application evals.** Foundation-model capability is not product quality. Learn the workflow: task definition, success criteria, dataset, execution, analysis, iteration.
3. **Match the method to the behaviour.** Programmatic checks for deterministic behaviour, judges for semantic behaviour, humans for calibration and ambiguity, operational metrics for latency and cost.
4. **Offline vs online.** Offline suites gate releases and prevent regressions. Online evaluation covers unexpected inputs, changing user behaviour and drift. Separate automatically captured system metrics (latency, tokens, errors) from computed quality metrics (hallucination, relevance). Pipeline: log, sample, dashboard, alert, feed failures back to the offline set.
5. **Benchmark anatomy and pitfalls.** Dataset, prompts, run configuration, scoring method, aggregation. Pitfalls: contamination, saturation, overfitting to the benchmark, configuration gaming. Public benchmarks shortlist models; your domain evals decide.
6. **Knowledge benchmark progression.** MMLU and TruthfulQA, then human-exam sets such as AGIEval, then GPQA, MMLU-Pro, SimpleQA and Humanity's Last Exam. Understand why benchmarks keep getting harder as frontier models saturate them.
7. **Coding benchmark progression.** SWE-bench Verified saturated quickly; SWE-bench Pro was introduced to reduce contamination concerns by using actively maintained repositories. Compare a model's gap between the two before trusting a leaderboard rank.
8. **Reasoning models.** Evaluate at fixed reasoning-effort settings, track reasoning-token cost separately, and run more trials because variance is higher.
9. **Custom model evaluation.** Shortlist models by capability, latency, context window and cost. Build a custom dataset for your task (Text-to-SQL is a good example). Compare like for like: same inputs, prompts, parameters and scoring. Estimate token cost including prompt caching and batch discounts. Choose the best quality, latency and cost trade-off, not the top general ranking.
10. **Eval suite and regression testing.** Structure tests at component, pipeline and application level. Version test cases, configs, prompts, models and results. Track experiments against baselines. Add CI/CD gates. Track quality together with latency and cost so a gain in one does not hide a loss in another.

**Proof of learning:** shortlist three models for one task, build a 50-example custom dataset, run all three with identical settings, and publish a quality, latency and cost table.

#### **Phase 3: RAG Evals**

Evaluate retrieval and generation separately so you can tell where the fault is. A bad answer with good retrieval is a prompt or model problem. A bad answer with bad retrieval is a chunking, embedding or search problem.

**Retrieval metrics (need labelled relevant passages):**

| Metric | Question it answers |
| --- | --- |
| Hit rate@k | Did anything relevant show up in the top k? |
| Recall@k | Of what was needed, how much did we get? This is the ceiling on answer quality. |
| Precision@k | How much of what we showed the model was useful? |
| MRR | How high was the first relevant result? |
| nDCG@k | Ranking quality with graded relevance and position discount |
| Context precision / recall (Ragas-style) | LLM- or reference-based versions when passage labels are missing |

**Generation metrics:**

| Metric | What it checks |
| --- | --- |
| Faithfulness / groundedness | Every claim is supported by retrieved context (claims split out, each checked) |
| Answer relevance | The answer addresses the question |
| Answer correctness / completeness | Matches a reference answer; covers required facts |
| Citation accuracy | Each citation really supports its sentence |
| Refusal correctness | Declines when context lacks the answer, answers when it has it |
| Context utilisation | Retrieved chunks actually used (a cost signal) |

Also cover: permission and metadata filters (count any leaked passage as severe), chunking and embedding experiments, rerankers, hybrid search, query rewriting, long-context versus retrieval, multi-hop and unanswerable questions, and synthetic question generation (then human review). Published targets such as faithfulness above 0.8 (0.9+ in regulated domains) are rules of thumb. Set thresholds from your own risk.

**Four levels of RAG evaluation:**

1. **Component level.** Retriever alone (contextual recall, contextual precision, Recall@k, ranking-aware metrics). Generator alone, given known-good context (faithfulness, relevance).
2. **Pipeline level.** Score retrieve, assemble context, generate with the RAG Triad: context relevance, faithfulness, answer relevance. Strong components can still interact badly, so locate the root failure in retrieval, assembled context or generation.
3. **Application level.** Judge from the user's side: correctness, completeness, tone, format, persona, citation behaviour, plus per-query latency, tokens, cost and error rate.
4. **Safety level.** Harmful output, PII leakage, direct and indirect prompt injection (including instructions hidden in retrieved documents), jailbreaks, and poisoned retrieval content.

**Proof of learning:** build a RAG over a document set you know, write 50 questions including 10 unanswerable, measure retrieval and generation separately, change chunk size, and show the metric movement with confidence intervals.

#### **Phase 4: Agent Evals**

1. **Outcome vs transcript.** "Your flight is booked" is a claim; a reservation row in the database is the outcome. Grade outcomes with code where possible. Use the trajectory to diagnose failures, and avoid hard-coding one correct tool sequence.
2. **Trajectory and tool-use diagnostics.** Tool selection, argument accuracy, ordering and parallelism, redundant calls, loops, premature exit, error recovery, step ratio and tool-call ratio against an ideal path, latency, cost, token use.
3. **Reliability.** Run multiple trials. Report pass@k and pass^k and track variance. An agent that is 80% on one try may be far lower when it must succeed every time.
4. **Environments and fixtures.** Sandboxes, recorded tool payloads and seeded databases make runs reproducible. Compare live and plan-only (dry-run) conditions and study the gap.
5. **Simulation.** LLM-simulated users with personas and goals, scenario libraries, multi-turn conversations, an independent judge, adversarial scripts, and noise or accent variation for voice.
6. **Failure recovery.** Inject realistic faults (tool errors, malformed results, unavailable services, missing information) and check that the agent notices, retries, falls back, replans or escalates. Measure recovery, not just success under ideal conditions.
7. **Agent safety.** Unauthorised or destructive actions, human-approval gates, permission boundaries, direct and indirect prompt injection that tries to hijack tool use, and attempts to extract secrets or exceed scope.
8. **Grader robustness.** Agents can exploit weak graders (editing tests, reading answer files, hard-coding expected outputs). Audit transcripts, isolate the grader from the agent's workspace, and make outcome checks hard to game.
9. **Tool and protocol evals (MCP and A2A).** For MCP servers, evaluate tool-description quality, tool selection when many tools are available, argument accuracy, and security (tool poisoning, over-broad permissions). For agent-to-agent handoffs, evaluate handoff quality and failure attribution across agents. Keep graders protocol-neutral so a change of framework does not invalidate your suite.
10. **Context, memory and long-horizon work.** Persistence correctness, forgetting, context loss across sessions, behaviour as context grows, and whether summaries or compaction drop critical facts.
11. **Agent types and their grading:**
    - *Coding agents:* fail-to-pass and pass-to-pass tests, static analysis, review.
    - *Conversational and support agents:* task resolution, policy adherence, tone, escalation correctness, state changes.
    - *Research agents:* groundedness, coverage, source quality, citation checks.
    - *Browser and computer-use agents:* task success in live or replayed environments, judging on screenshots and DOM state.
    - *Voice agents:* speech recognition error, latency, interruption handling, noise robustness.
    - *Multi-agent systems:* coordination, handoff quality, policy adherence, failure attribution.
12. **Benchmarks to know (and distrust a little).** SWE-bench family (Verified, Pro), tau-bench / tau2-bench, GAIA, BFCL, WebArena, OSWorld, Terminal-Bench, BrowseComp. Learn what each measures, how contamination and flawed tasks distort scores, and why maintainers keep removing broken tasks.

**Proof of learning:** build a tool-using agent (for example a support agent over a mock database) with 25 tasks, outcome checks, a simulated user and 5 trials per task. Report pass@1, pass@5 and pass^5.

#### **Phase 5: Observability, Production Evals and the Improvement Loop**

- **Traces first.** Without traces there is nothing to evaluate. Instrument LLM calls, tool calls and retrieval as spans.
- **OpenTelemetry GenAI conventions.** The GenAI semantic conventions (LLM calls, agent invocation, tool execution, retrieval, MCP) are the emerging vendor-neutral standard. As of mid-2026 they are still in Development status, not stable, and were moved out of the main semantic-conventions repository into a dedicated GenAI repository in June 2026. Several blogs claim they are stable; the primary registry says otherwise. Also know OpenInference and OpenLLMetry, which are widely used in practice.
- **Eval scores on spans.** Write judge and heuristic scores onto the same trace as the run, so a low score links directly to the failing step.
- **Online sampling.** Run cheap heuristics on all traffic and judges on a sample. Route low scores and user complaints to annotation queues. Track the cost of judging itself.
- **Behavioural signals.** Thumbs, regenerations, abandonment, escalations, model switches.
- **Failure discovery.** Have an LLM read raw failure reasons and propose categories, confirm with humans, and promote confirmed failures into the regression dataset.
- **CI/CD gates.** Cheap code graders on every commit; expensive judge suites on preview or nightly; block merges on regressions; version prompts and gate prompt promotion on eval results.
- **A/B testing.** Gradual ramps, guardrail metrics (CSAT, resolution rate, cost), novelty effects, concurrent experiments with clear attribution.
- **Model migration.** Use frontier and regression suites to adopt new models quickly and safely.
- **Cost control for evals.** Batch APIs for offline judge runs, prompt caching for long rubrics, smaller judge models for high-volume scoring, sampling for online judging.
- **Vendor risk.** The tooling market is consolidating (Promptfoo, Langfuse and Arize all changed owners in 2026). Prefer OTel-compatible instrumentation so you can swap backends.

**Proof of learning:** wire your Phase 4 agent into a tracing tool, add a GitHub Actions gate, and demonstrate a deliberate regression being caught.

#### **Phase 6: Safety and Specialised Domains**

- **Safety and red teaming.** Prompt injection, jailbreaks, data exfiltration, tool misuse, over-refusal. Keep access control deterministic rather than relying on the model.
- **Runtime guardrails vs offline evals.** Guardrails block bad output live; evals measure how often they are needed. Test both, and measure the false-positive cost of guardrails.
- **Hallucination detection.** Claim-level checking and small purpose-built judge models for cheap per-request scoring.
- **Multimodal and voice.** Image and document understanding, speech quality, latency, interruption handling.
- **Fairness, privacy and compliance.** PII leakage, bias slices, audit trails.
- **Cost and latency engineering.** Cost per successful task, tokens per resolution, p95 latency.

#### **Phase 7: Advanced Topics**

- **Judge optimisation.** Prompt optimisers such as GEPA to raise agreement with human labels, judge ensembles, evaluating the evaluators, and replacing LLM judges with trained classifiers where volume justifies it.
- **Statistical rigour.** Power analysis, multiple comparisons, drift detection.
- **Benchmark validity.** Read the research on task-setup bugs in agent benchmarks and on leaderboard gaming (arXiv 2507.02825 and arXiv 2504.20879).
- **Eval-driven self-improvement.** Agents that mine traces, draft fixes and are verified by the suite, with humans owning the launch decision.
- **RL environments and verifiable rewards.** How eval design becomes a training signal, and how reward hacking mirrors grader gaming.

---

### **5. Syllabus Crosswalk (M7.1 to M7.9)**

The syllabus assumes you already know RAG and agent basics. If not, learn those first.

| Module | Covered in | Proof of learning |
| --- | --- | --- |
| M7.1 Introduction to LLM evals | Phase 1, 2 | Written post-mortem of a vibe-testing failure plus a 30-item dataset |
| M7.2 Methods and paradigms | Phase 1, 2 | Grader type chosen per failure mode; 100 human labels for the judge |
| M7.3 Offline vs online | Phase 2, 5 | Sampling, dashboard and a failure promoted into the dataset |
| M7.4 Model evals and benchmarking | Phase 2 | One benchmark dissected: dataset, prompts, scoring, pitfalls |
| M7.5 Knowledge benchmarks | Phase 2 | Notes on saturation: older versus harder benchmark for one model |
| M7.6 Custom model evals | Phase 2 | Quality, latency and cost table for three shortlisted models |
| M7.7 Eval suite and regression | Phase 2, 5 | CI gate that blocks a seeded regression |
| M7.8 RAG evals | Phase 3 | Project 1 in section 8 |
| M7.9 Agent evals | Phase 4, 6 | Project 2 in section 8 |

---

### **6. Metrics Cheat Sheet**

| Layer | Metrics |
| --- | --- |
| Output quality | Correctness, completeness, relevance, tone, format validity, policy adherence |
| Retrieval | Hit rate@k, recall@k, precision@k, MRR, MAP, nDCG@k, context precision/recall |
| Grounding | Faithfulness, hallucination rate, citation accuracy, refusal correctness |
| Agent behaviour | Task success, outcome verification, tool-selection and argument accuracy, step ratio, tool-call ratio, error recovery |
| Reliability | pass@k, pass^k, trial variance, flakiness rate |
| Judge quality | TPR, TNR, agreement or Cohen's kappa with humans, bias checks |
| Operations | Latency (p50/p95), cost per task, tokens (including reasoning tokens), time to resolution |
| Business | CSAT, resolution rate, retention, escalation rate, ship rate |
| Safety | Attack success rate, over-refusal rate, leakage incidents, unauthorised-action rate |

---

### **7. Tools: What to Learn and in What Order**

| Tool | Why learn it |
| --- | --- |
| **pytest + plain Python** | Start here; most good evals are simple assertions |
| **Promptfoo** | Config-as-code evals, CI gating, red teaming |
| **DeepEval (Confident AI)** | pytest-style LLM and RAG metrics |
| **Ragas** | RAG metrics and test-set generation |
| **Langfuse** | Self-hostable tracing, datasets, evals |
| **Arize Phoenix** | OTel-native tracing and evals |
| **LangSmith** | Strong for LangChain and LangGraph; offline, online, annotation queues |
| **Braintrust** | Eval-first platform; scorers, datasets, CI, production scoring |
| **MLflow (GenAI evaluation)** | Evaluation and tracing inside a widely used ML platform |
| **Inspect (UK AISI)** | Research-grade eval framework for models and agents |
| **OpenTelemetry / OpenInference / OpenLLMetry** | Vendor-neutral tracing |
| **Others to scan** | Galileo, W&B Weave (CoreWeave), Comet Opik, HoneyHive, Laminar, Patronus |

Pick one open-source stack (pytest plus DeepEval or Promptfoo, plus Langfuse or Phoenix) and one commercial platform to try on a free tier. Several tools changed owners in 2026, so check licence terms and self-hosting conditions before committing. Understanding the concepts matters more than the tool.

---

### **8. Capstone: Two Connected Projects**

Build the RAG assistant first, then plug it into a customer-support agent as a tool. Together they exercise every metric family above.

#### **Project 1: Company Knowledge and Policy Assistant (RAG)**

- **Corpus:** 50-100 product docs, FAQs, refund and internal policies, API docs and onboarding guides, with metadata (source, section, effective date, permissions, product area).
- **Stack:** LangChain for loaders, embeddings and retriever; LangGraph for query rewrite, retrieve, grade context, generate, cite; Ragas to diagnose metrics; DeepEval for pytest-style gates; LangSmith, Langfuse or Phoenix for traces.
- **Golden set:** 100-300 questions covering easy, ambiguous, multi-hop, outdated-document, irrelevant and no-answer cases, each with an expected answer, expected source and unacceptable claims.
- **Evaluate retrieval and generation separately,** then end to end. Compare chunk size, top-k, embeddings, hybrid search, reranking and query rewriting, and record every experiment.
- **Gates and monitoring:** DeepEval tests that fail when faithfulness, answer relevance or context recall drop, run in GitHub Actions. Trace each query's document IDs, scores, latency and cost. Sample live traffic and send low scores to human review.
- **Safety cases:** permission leaks, PII, instructions injected into documents, correct refusals.

#### **Project 2: CloudNotes Customer-Support Agent (LangGraph)**

A fictional note-taking SaaS gives you clear success criteria, real tools and dangerous actions to guard.

- **Tools:** the RAG assistant as a search tool; account lookup; billing and refunds; ticket create, update and escalate; human handoff. Expose them over MCP so you can also run tool-level evals.
- **Guardrails:** refuse unauthorised refunds, never expose another user's data, confirm before destructive actions.
- **Why LangGraph:** explicit state, routing, retries and human-in-the-loop checkpoints, and traceable tool spans.
- **Scenarios:** 50-100 covering normal requests, ambiguous requests, tool failures and policy violations, each run several times. Example personas: Tanvi asks for a refund outside the policy window; Rohit asks to see another user's invoice; Meera reports a billing error while the billing tool is down.
- **Three evaluation layers:** final response, trajectory (diagnostic), and single-step tool calls. Check the current Ragas and DeepEval docs for LangGraph support (tool-call accuracy metrics, node and tool span tracing).
- **Extra metrics:** escalation accuracy, cost per resolved ticket, human override rate, safety compliance, p50 and p95 latency.

#### **Which Tool for Which Job**

| Tool | Use it for |
| --- | --- |
| Ragas | Diagnosing why a RAG answer failed (retrieval versus generation metrics) |
| DeepEval | Code-first tests that fail a build; agent and tool-call regression tests |
| LangSmith | Experiments, datasets, human annotation, LangGraph traces, online evals |
| Arize Phoenix | Trace inspection and component-level debugging |
| Langfuse | Production observability, prompt versions, cost and latency dashboards |

Do not use every tool for everything. Give each one the job it is strongest at.

#### **Build Order**

| Stage | Build | Evaluate |
| --- | --- | --- |
| 1 | Baseline RAG and 100-question golden set | Vibe-test failures, graders, judge calibration, model shortlist |
| 2 | RAG improvements | Retrieval and generation metrics, DeepEval regression tests, RAG safety cases |
| 3 | Support agent, tools, scenarios | Outcome graders, user simulator, pass@k and pass^k |
| 4 | Failure injection and safety tests | Tool-call accuracy, recovery, prompt injection, grader-gaming audit |
| 5 | Tracing, dashboard, CI | Online sampling, CI gate, baselines, failure-to-dataset loop |
| 6 | Red-team suite, cost tuning | Write-up and portfolio polish |

#### **Optional Extras**

- A coding or browser agent evaluator using SWE-bench or WebArena-style tasks, with outcome grading and pass^k.
- An MCP server evaluator: tool-description quality, tool-selection accuracy and a small security test set.
- A short write-up on one surprising finding, such as a judge that disagreed with humans or a flawed benchmark task.

#### **What to Publish for Each Project**

Architecture diagram, dataset design and failure taxonomy, evaluation code and metric definitions, before and after experiment results, trace screenshots showing a diagnosed failure, the CI pipeline that blocks regressions, and a lessons-learned note on retrieval, tool-call and safety failures.

---

### **9. Reading and Watching List**

Starred items are the first to read.

- \* Anthropic, *Demystifying evals for AI agents* (January 2026)
- \* Pragmatic Engineer and Hamel Husain, *A pragmatic guide to LLM evals for devs* (December 2025)
- \* DoorDash Engineering, *Building Ask DoorDash, Part 3: Evaluation* (June 2026)
- \* Replit, *Closing the loop: Evaluating and improving Replit Agent at scale* (June 2026)
- LangChain, *How we build evals for Deep Agents* and *Agent Evaluation Readiness Checklist* (March 2026)
- Browser Use, *How we built scalable evaluation infrastructure for AI web agents* (February 2026)
- Google Cloud, *Four eval engineering lessons* (October 2026)
- Vercel, *AI agent evaluation frameworks: how Vercel approaches evals in production*
- Sierra, *Simulations: the secret behind every great agent*; Decagon, *The evaluation engine behind Decagon's AI agents*
- Raindrop, *Thoughts on Evals* (contrarian view on online LLM judges)
- Papers: Ragas (arXiv 2309.15217); agentic benchmark flaws (arXiv 2507.02825); The Leaderboard Illusion (arXiv 2504.20879)
- OpenTelemetry GenAI semantic conventions (primary repository and registry)
- LangChain docs, *Evaluate a complex agent*; DeepEval RAG guide and LangGraph integration; Ragas LangGraph agent evaluation; Arize LLM evaluation guides
- Ragas, DeepEval, Promptfoo, Langfuse and Phoenix documentation

---

### **10. Progress Checklist**

- [ ] Stats refresher and a hand-built 30-item dataset
- [ ] Error analysis on 50+ traces, vibe-testing post-mortem, grader chosen per failure
- [ ] Calibrated judge (TPR/TNR), three-model shortlist, custom dataset, quality / latency / cost table
- [ ] RAG baseline, 100-question golden set, retrieval metrics
- [ ] Generation metrics, chunking experiment, DeepEval regression tests, RAG safety cases
- [ ] LangGraph support agent with five tools and tracing
- [ ] Simulated users, 50-100 scenarios, pass@k and pass^k over repeated runs
- [ ] Trajectory diagnostics, tool-call metrics, injected failures, agent safety tests, grader-gaming audit
- [ ] OTel-based tracing with eval scores on spans, online sampling, dashboard, failures promoted into the dataset
- [ ] CI gate that blocks a seeded regression, baselines and experiment tracking
- [ ] Red-team suite across RAG and agent, cost and latency tuning
- [ ] Write-up and portfolio polish

---

### **11. Caveats**

**Corrected from the original draft:**

- Removed leftover drafting notes and a reference to a private syllabus rating (8/10 for interviews, 10/10 for on-the-job impact), which was an opinion rather than a fact about the field.
- Adjusted agent grading so trajectory is a diagnostic, not a rigid pass condition.
- Corrected the Phoenix licence description: it is source-available under the Elastic License 2.0, not OSI open source.
- Noted that OpenTelemetry GenAI conventions are still in Development, despite blogs calling them stable.

**Things to keep in mind:**

- Vendor case-study figures (for example Browser Use's 200 traces and 87% judge agreement, Notion's 10x issue throughput) are reported by vendors and not independently audited.
- Article titles and dates in section 9 were not individually checked, except Anthropic's *Demystifying evals for AI agents*.
- SWE-bench Verified versus Pro gap figures appear in vendor blogs only.
- RAG thresholds such as 0.8 faithfulness are heuristics, not standards.
- The tooling market changes quickly; re-check section 7 for ownership and licence changes before committing to a vendor.