### **Session Overview**

- This is the third and fourth session in this course.
- Plan for today: first a quick recap of what has been covered so far, then today's agenda.
- Today's session is interesting - some new things will be learned, and by the end of the session you will walk away having learned something good.

---

### **Quick Recap - What We Have Covered So Far**

- In this LLM Evals course, five things have been covered until now:
  - Why do we need evals.
  - What exactly are evals - covered both model-based and application-based types.
  - How does an LLM eval pipeline look - discussed a basic eval pipeline.
  - Why do we need multiple eval pipelines for a single application (discussed in the last session):
    - No LLM-based application works with just one eval pipeline attached and left as is.
    - Ideally you create multiple eval pipelines for a single application.
    - Reason 1: There are multiple failure points - failure can happen at component level, workflow level, and at the whole application level, so we need evals to monitor all three.
    - Reason 2: There are different risk categories - three categories were discussed: application quality, safety, and operations (latency and all types of operational metrics have separate evals).
  - What are the different eval methods through which we perform evaluation (discussed in the last video):
    - Programmatic methods.
    - LLM as a judge.
    - Evals with humans.

- This is the summary of everything covered in this course till now.

---

### **Today's Agenda**

- Today we are going to discuss a very important topic: **Offline Eval vs Online Eval**.
- Plan:
  - First, what offline eval is.
  - Then, what online eval is.
  - Then, the differences between the two.
- You will learn a lot in this process.

---

### **What Are Offline Evals**

- Good news: nothing new needs to be learned here - offline evals have already been studied.
- Whatever examples were discussed in the last two-three sessions where an eval pipeline was built and shown - all of that is an example of offline eval.
- **Core idea of offline eval:** If you attach any eval pipeline to your LLM application *before* deploying it, that is called offline eval.
- Example recap - the UPSC application discussed in the last video:
  - Built an LLM application that evaluates a UPSC mains mock paper exactly like a human would.
  - Step by step process discussed: built a golden dataset, used LLM-as-a-judge method, performed the evaluation.
  - This evaluation happens after the software is built but before deployment.
  - This means this is an example of an offline eval.
- **Simple definition:** Whenever you have an LLM-based application and you want to fully test it before deploying it to check whether it is fit for deployment, the evals you run there are called offline evals. As simple as that.
- So everything studied until now comes under offline eval - nothing new was learned, just a new name was given to what was already learned.

---

### **Main Purposes / Benefits of Offline Eval**

**Benefit 1: Pre-release testing**

- If you deploy without testing, you don't know how the software will behave in production, and any kind of risk can occur.
- Recall the case studies discussed at the very start of the course (Air Canada, ChatGPT cases) - you cannot deploy an LLM-based software into production without testing it.
- So the first benefit offline eval gives is the feature of pre-release testing - properly test before releasing.
- **Interesting extension - CI/CD automation:**
  - This entire process (building software, testing it, deploying it) is automated to such a level that you can simply create a gate: if the eval result is above 95%, then deploy the software (using CI/CD); if it is below 95%, don't deploy it.
  - In the future you will study that this testing/eval-running process is also automated.
  - Flow: you make changes in the software → code gets pushed to Git → CI triggers via GitHub Actions → the eval script kept there runs → you get a score → if the score is above threshold, the deployment pipeline auto-triggers → if the score is below threshold, you get a notification that eval tests failed.
  - So not only do you get pre-release testing, but if used properly, it also works as a **release gate** - eval passes → deploy properly; eval fails → rollback to previous version.

**Benefit 2: Comparing versions**

- Example: you have a choice - build your UPSC-type LLM-based software using a Claude model or an OpenAI model. How would you compare these two?
- Everything else stays the same (same code), only the model changes. Need to evaluate which model gives better results for your purpose.
- Method: build two versions of your software and run the same eval on both versions.
- Since the eval is the same, the golden dataset is the same - everything is the same, the field is level.
- From the results, you can easily identify that, say, Claude is scoring higher compared to OpenAI - meaning you will use Claude.
- This can be done for anything:
  - Comparing different prompts.
  - Comparing different models.
  - Comparing different rerankers.
  - Comparing different vector databases.
  - Comparing different architectures of your software application.
- Whenever you have multiple possibilities and the question "which one should I choose" comes to mind, running your eval on multiple versions of the software will tell you the choice.

**Benefit 3: Regression testing**

- What is regression testing - it is the "test of change."
- Example: Version 1 of the software is already live. This is CampusX's chatbot that students interact with.
- Observation: whenever students ask about refunds, the chatbot answers a bit coldly - not sure why. This pattern was observed in production.
- Decision: improve this, because you always want the chatbot to talk in a good tone with students.
- Action taken: went into the system prompt and made changes - "you have to be very kind and very polite, answer nicely."
- Result of that change: the personality became too soft. Example: if someone asks the cost of the insider plan, and say the actual cost is 19,500, instead of saying 19,500 clearly, it very softly says "it's around 19,000" just to make sure it sounds impressive to the other person.
  (Not the best example, but the point: in a complex system, when you try to improve one thing, other things can break. Improving performance in one area can degrade performance in other areas. This is called **regression**.)
- Testing for this is important - whenever you are improving your software, you have to make sure that the thing you're improving does improve, but at the same time nothing else should break.
- Offline eval helps with this too:
  - Your golden dataset has different types of cases - different types of student questions (refund questions, pricing questions, course curriculum-related questions, etc.) - every type of case is covered.
  - Run eval on every type of question to see how results are coming for each type.
  - Example: if the success rate for refund-related questions was 90% before, after the prompt change it should stay around 90% - not drop to 80%.
  - If it drops to 80%, that shows there is some form of regression, and the change you just made should not be kept.
- **Core idea:** whenever you make a small change anywhere - system prompt, model, vector database, anything - nothing else should break. This can also be tested with the help of offline evals.

**Summary of offline eval benefits:**

- Testing before release.
- Comparing two versions when in doubt.
- Testing that nothing else breaks when making changes to existing software.
- These are the three biggest benefits that make offline evals essential - can't work without them.

---

### **Production Risks (What Happens After Deployment)**

- Suppose the software is built, offline eval is run on it, all results pass, and the software is now deployed. What next? What problems can occur in production?
- Three major problems will be faced once the software is deployed:

**Risk 1: Unanticipated inputs**

- Example: CampusX chatbot. During offline testing, a golden dataset was built with 200-500 questions expected from users, and the chatbot was tested only on these 200-500 questions.
- But once deployed, the chatbot is open to the real world - meaning students can ask ANY type of question, possibly things the model/software was never tested on.
- Examples of what might suddenly happen:
  - People might suddenly start mixing Hindi-English (Hinglish) - the model was mostly trained/fine-tuned expecting English since English conversation was anticipated.
  - Many ambiguous, half-formed questions where it's not even clear what the user is asking.
  - Angry rants where a question is hidden behind a lot of anger.
  - Many people will try adversarial prompt injections to somehow extract an answer from the chatbot that it shouldn't give.
  - Many edge-case scenarios you'll have to face.
- So in production, you get a much bigger superset of situations than whatever you tested against - the chatbot can face literally anything.

**Risk 2: Emergent and systematic failures**

- Small failures that won't show up in offline setup - they only appear in the picture once you deploy to production.
- Types of issues:
  - Problems that only show up at scale. Example: a new course is launched on CampusX, suddenly a lot of people come in, and there are thousands of concurrent users on the chatbot at once - latency suddenly increases. This could never be tested offline because you can't bring thousands of users into an offline test.
  - A subtle bias that only becomes visible across thousands of conversations. Example: the chatbot might be slightly biased against individuals from a non-technical background - but you'll only know this once the chatbot has chatted with thousands of people and a pattern emerges from that large volume of data (works fine with technical background users, develops a slight bias with non-technical users).
- Roughly speaking, many types of systematic failures can occur in production that you would not have anticipated beforehand - you cannot face these earlier, only in production.

**Risk 3: Drift**

- Drift means: gradually, your offline eval (which was used for testing and deployment) becomes obsolete.
- Example: right now, the CampusX chatbot has all documents, pricing structures, course pages, curriculum pages, lecture transcripts loaded in - this is today's data.
- Over the years, changes happen: a course's price changes, a course's curriculum changes a bit, policies change a bit - as a business operates, its documents also gradually change.
- A year later, the documents given to the chatbot for RAG might look very different compared to a year ago's documents.
- But the test cases / golden dataset were built based on today's data. A year later, since the entire data has changed, its distribution has changed, the golden dataset and the whole eval pipeline become kind of obsolete.
- Because of that drift: the eval pipeline will still give good results when tested offline, but when taken online, you'll see a lot of negative feedback from users because they are not liking the chatbot's behavior.
- This happens because things keep changing but the eval setup is not being changed - so the eval setup becomes obsolete because of the drift that is happening.

**Summary of the three production risks:**

- User can ask any type of question - no control over this.
- Many types of emergent/systematic failures can occur - such as bias, latency increasing with concurrent load.
- Drift can come into the picture.

- **Conclusion:** Offline eval is necessary because testing before launch is necessary. But even after launch, there are many types of risks in production, and offline eval cannot cover those risks.
- **Reason:** offline evals work by having a golden dataset where you already provide correct answers, and evaluation happens on that basis. But the problem is - once you go to production, you no longer have a golden dataset. Now the user can ask anything, and you don't have correct answers for it. You also don't know in advance which student will ask what question tomorrow and what the correct answer to that would be.

---

### **What Are Online Evals**

- **Simplest definition:** Online eval is evaluating your system on live production traffic after deployment, as real users interact with it.
- It is a different type of evaluation that is run on production, *after* the software is deployed.
- **Biggest characteristic:** it works **without an answer key** - without a golden dataset. This is the biggest feature of online eval.
- This is why it is super critical - it helps ensure the deployed software keeps running correctly. It tells you whether something is going wrong online.
- In that sense, online evals are super important.

---

### **Offline vs Online - Key Differences**

- **Timing:**
  - Offline eval happens before deployment.
  - Online eval happens after deployment.

- **Data:**
  - Offline eval: you have a fixed dataset that you create (golden dataset).
  - Online eval: no such fixed dataset - you are working on live production traffic; you run online eval on whatever questions are actually being asked.

- **Answer key:**
  - Offline eval: mostly has an answer key (the golden dataset).
  - Online eval: no answer key - you have to estimate on the go what the correct answer might be.

- **Timing (repeated):**
  - Offline: before deployment.
  - Online: runs consistently after deployment.

- **Input:**
  - Offline eval: only the things you anticipate are given as input (whatever is put into the golden dataset).
  - Online eval: you cannot anticipate what may come - anything can come.

- **What it catches:**
  - Offline eval generally helps catch regressions.
  - Online eval can catch drift, any kind of surprise, any kind of emergent bug.

- **Best used for:**
  - Offline eval is best used for "gating" - if the score after offline evaluation is above threshold, you push/deploy directly via CI. Also best for version comparison via CI.
  - Online eval's simple job: drift detection, and telling you how your chatbot is actually performing in the real world.

- **Cost and speed:**
  - Offline eval is fast, cheap, and repeatable - because you're basically running simple code and an LLM on a small dataset.
  - Online eval can be needed at a much bigger scale - e.g., your chatbot might be talking to 500 people in a day, and you need to monitor those 500 conversations - this can be costly.
    - Sampling-type techniques are used here: rather than monitoring every one of, say, 50,000 conversations, you randomly sample around 1,000 conversations to monitor. This brings the cost down a bit.

---

### **Offline and Online Evals Are Not Rivals - They Are Complementary**

- It's not that online eval replaces offline eval.
- Both happen together, always. They are complementary - it's not that one exists and the other doesn't. Both existing together is very important.

- **A very important line (heard somewhere):**
  - Your offline eval checks whether your application is working **correctly** or not.
  - Your online eval tells you whether your application is running **normally** on production, at this point in time, or not.
  - These are the two main purposes.

---

### **Example: Correctness vs Normality**

- Recall the UPSC grader example - the paper-checking system discussed in the last class.
- In offline evaluation of that system, what were we trying to do? We were checking if this grader evaluates UPSC papers exactly the way a human evaluator would.
- Measure of correctness there: the marks given by the grader to a particular answer should be close to the marks a human gave.
- **Correctness definition here:** how close the marks your system gives are to the marks a human gave.

- Now suppose this system has been offline-evaluated, you're satisfied, and you deployed it.
- **Question:** Can correctness be measured in the online setup, after deployment, at this moment?
- **Answer: No.**
- **Why:** at this point, for the answer being evaluated, you don't know what marks a human would have given - you simply don't have a golden dataset for this particular answer being evaluated right now. There is no human perspective available in production - this answer was never evaluated by a human. Your system is evaluating it for the very first time directly. So you cannot measure correctness here.

- **What can be checked online instead:** whether the system is running **normally**.
- **How to figure out "normal" without knowing correctness:**
  - Check what the distribution of scores was last week.
  - Plot a graph: what was the distribution of scores for all answers evaluated last week.
  - If this week's distribution of all evaluations is similar, you can say your system is behaving the same way it was behaving last week - and if last week was fine, today is probably fine too.
  - This becomes your baseline, and you keep comparing against that baseline in production.
  - If suddenly, in some particular week, the distribution of your evaluations changes a lot - you'd say something abnormal has happened. This gives you a trigger to go investigate what went wrong.

- **Example with numbers:**
  - Evaluating 1,000 people's papers in a week. Student 1 got 300 marks, Student 2 got 456 marks, Student 3 got 700 marks, and so on - you can plot this distribution.
  - Over a few weeks, you notice the baseline distribution stays roughly the same.
  - But in some particular week, suddenly the evaluations start giving very high scores (around 900, 800, 700) - the distribution has clearly changed.
  - Comparing week-to-week distributions like this shows you something is different this week - something is off. (Could be due to a different underlying trend too, e.g., very intelligent students suddenly took the exam - but either way, you now know to investigate.)
  - Online eval doesn't guarantee correctness - in some cases it can, in some cases it can't. But it mostly tells you whether your application is behaving normally or not. That is the purpose of online eval.

- This was just a constructed example to explain the difference between "correctness" and "normal" - not meant to be applicable everywhere exactly like this.

---

### **Q&A: How Do We Actually Estimate Quality Without a Correct Answer**

- Question raised: online eval has no answer key - how do we actually estimate quality?
- Several approaches exist:
  - Some metrics don't require knowing the correct answer at all. Example: **faithfulness** in a RAG chatbot.
    - Faithfulness means: was the answer generated purely from the retrieved context or not?
    - You already have the context and you already have the generated answer - you can ask an LLM whether the answer was generated from the context. Faithfulness can be figured out this way.
  - So in many cases, you can compute a metric's answer without knowing the correct answer.
  - In some scenarios, you don't have a correct answer key, so you have to find a workaround (jugaad). Example: the UPSC case - no correct answer available, so the baseline-distribution comparison approach was used (comparing against last week's distribution to check normal behavior).
  - Either the metric doesn't need a correct answer at all (like faithfulness), or the metric does need a correct answer and then you have to think of a workaround to reach a conclusion.

- **Another example - measuring correctness in the online setting using user feedback:**
  - Question: can correctness be measured in the online setup after deployment? For any new question, there's no correct answer available, so how do you know your chatbot is making a mistake?
  - Answer: Use a signal like **thumbs up / thumbs down**.
  - If in the last hour a lot of conversations are getting thumbs-down ratings, that indicates something is wrong - the chatbot is giving wrong answers.
  - This is again a workaround (jugaad) way to find out whether correctness is being maintained - **user feedback** becomes the alternative/proxy for correctness.

---

### **General Metrics and Signals Tracked via Online Evaluation**

- This will be discussed in detail next.

---

### **Building an Online Evaluation Pipeline**

**Step 1: Logging**

- The first step in an online evaluation pipeline is very important - it's called **logging**.
- **Basic idea:** your chatbot is live in production and people are talking to it. Before you can evaluate anything, you first need to record everything that is happening / every conversation currently taking place, somewhere.
- Obviously, if you don't record it, it will be lost - and if it's lost, what would you even run evaluation on?
- **Core idea:** capture a structured, replayable record of every conversation turn.
- Example: if CampusX's chatbot is deployed on the website and 50,000 conversations happen in a day, you store these 50,000 conversations properly.
- **What gets stored for each conversation:**
  - A conversation ID for every conversation.
  - A turn ID for every turn within it (I say something, chatbot replies, I say something, chatbot replies).
  - A user ID for the person having the conversation.
  - A session ID.
  - A timestamp for when the conversation is happening.
  - What question the user asked.
  - What context was generated in the process of answering that question (for a RAG chatbot).
  - What output the chatbot gave based on that context and question.
  - Many operational things too, such as:
    - Latency in milliseconds.
    - How many tokens were spent in the prompt.
    - Completion tokens.
    - Total cost.
    - Whether any error occurred, and if so, its status code.
  - Any additional signals the user is giving:
    - Behavioral metrics such as thumbs up / thumbs down.
    - Whether the conversation is being escalated - e.g., user says "I don't want to talk to you, connect me to a human" or gives their email ID to be mailed.
    - Whether the user is asking the same question repeatedly, rephrasing it, because they feel the chatbot isn't helping them.
  - Everything gets stored.

- **Tool for storing all of this:** a tool like **LangSmith**.
  - Previously covered on YouTube - built a chatbot and stored every conversation on LangSmith.
  - In LangSmith you have different projects; inside a project you can see all conversations, and store everything - what the user sent, what the output was, plus a lot of metadata.

- **Engineering properties of logging:**
  - **Non-blocking:** logging is itself an operation. You need to run the chatbot and also do the logging - these should not block each other. Doing both together should not increase latency. It should be non-blocking - meaning the conversation happens normally on one side and the logging happens automatically on the other side; combining both operations should not increase latency.
  - **Durable and queryable:** use something like a data warehouse type tool or an observability tool such as LangSmith, where this entire information gets stored in a very structured way, and the best part is you can fetch it back anytime in the future.
  - **Late signal attachment:** many user signals don't arrive immediately during the conversation - they come later. Example: the user escalated by emailing su@campsx.in a day after the conversation happened - not helped during the chat, so mailed the next day. This escalation happened a day after the conversation, but it still needs to be recorded against that conversation. You'll need the conversation ID to figure out that this escalation belongs to that same conversation. So you need to track this too.
  - **PII handling:** if during the conversation the user shared sensitive personal information with the chatbot - phone number, address, card number - you need to remove it or blur it or mask it before storing it in LangSmith, so that in the future no teammate or employee can extract that information from LangSmith. Privacy must be maintained. (Masking is what's typically done since it's textual information.)

- PII = Personal Identifiable Information - phone number, card number, date of birth, Aadhaar number, etc. - anything like this shared with the chatbot gets masked before storing.

- This is what logging is about - why it's needed and how it's done.

---

### **Step 2: Types of Signals - Computed vs Captured**

- Before discussing step 2 further, need to establish what matters in online evaluation - what kind of signals to focus on, what tells you whether your chatbot is working correctly or not.
- There are two types of signals to focus on:

**Captured signals**

- Already present - you just need to store them somewhere. No calculation/computation needed.
- Examples:
  - Thumbs up / thumbs down - a signal the user gives directly during the conversation; you directly pick it up and store it in LangSmith as-is.
  - Latency - how much time the chatbot took to answer a particular question; you just pick up whatever time it took and store it directly. Nothing to calculate.
  - Cost per conversation - how many tokens were spent, how much money it cost - again something you don't need to calculate; the LLM provider tells you, or it's precomputed. No real-time calculation needed.
  - Token usage - simply counting, nothing to compute.
- These are examples/signals you simply capture and store in LangSmith - no calculation needed.

**Computed signals**

- These need to be calculated, figured out.
- Example: you want to see, in the online production setup, what your chatbot's **faithfulness** is.
- This is something you won't get simply by storing the chat - you need to build an evaluator for it.
- An online evaluator: you send the chat to this online evaluator, and it computes/calculates the faithfulness score for you.
- This is an example of a quantity/metric/signal that needs to be computed.
- Other examples that need to be computed:
  - Answer relevance.
  - Correctness.
  - Hallucination.
  - Toxicity.
  - Bias and fairness.

- So there are two categories of signals we pay attention to in the production setup: ones that need to be computed, and ones we simply capture and store.
- These are general quantities relevant to the chatbot - similar quantities probably exist in normal (non-LLM) software too; this isn't unique to LLM-based software.

---

### **Pipeline Flow for Captured Quantities**

- Logging → since a captured quantity (like latency) needs no calculation, go directly to the next step: **Dashboarding**.
- Every production setup has a dashboard where you display these quantities over time - e.g., latency over the last 1 hour, last 24 hours, last 1 week, last 6 months, etc.
- If you're observing a captured quantity that needs no computation, you send it directly to your dashboard, where you simply see its graph, and from that graph you understand whether your system is behaving normally or not.
- **Example:** you launch a course, 500 people come to the website at once and start chatting with the chatbot - suddenly the chatbot's reply time (latency) increases. The graph, which was flat, suddenly spikes up. Seeing this graph tells you something is wrong. You quickly allocate more resources (e.g., on AWS, start more EC2 instances, adjust load balancer, manage traffic somehow), and after a while the latency comes back down automatically.

- **Next stage after dashboarding: Alerting**
  - You won't watch a graph all day - your engineer isn't watching the graph 24 hours (could be on leave, sleeping, etc.).
  - So you set up alerts: if a quantity crosses a threshold, an alert is created - e.g., via Slack, email, or (less commonly) WhatsApp - so that as soon as the threshold is crossed, the concerned team/engineer gets an alert (e.g., "latency has gone above 4 seconds/4 milliseconds"). They then quickly go and normalize things.

- **Flow for a captured quantity:** Log it → present it on a dashboard → set up an alert system.
- This is NOT the flow for computed quantities - that's discussed next.

- **LangSmith demo mentioned:**
  - Under Monitoring, select your project, and there's already a built-in dashboard showing graphs: trace latency, error rate, LLM call count, LLM latency, cost graphs, etc.
  - You can select time windows: last 1 hour, 3 hours, 6 hours, etc.
  - These quantities are always viewed aggregated - what matters is not the latency in the current single chat, but the aggregated latency over, say, the last hour.
  - A single conversation in isolation doesn't matter much for dashboarding - latency can go up/down in one conversation, but if latency is increasing across many conversations in the last hour, that means the average latency is going up, indicating a system-level problem.
  - Alerts section in LangSmith: select a project, name the alert, select which metric to alert on, set a condition (e.g., alert when feedback metric exceeds X in the last 5 minutes), and connect it to Slack, PagerDuty, or your own API.

---

### **Pipeline Flow for Computed Quantities**

- Now the most interesting part: how to track a computed quantity in production.
- **Example: Hallucination.**
- Goal: check in real time whether the chatbot is hallucinating - needs to be tested in production.
- **Pipeline:**
  - **Step 1 - Logging:** same as before - if you're running 500 conversations a day, log each of the conversations using a tool like LangSmith.
  - **Step 2 - Set up an evaluator:**
    - This evaluator is a **reference-free** evaluator.
    - Recap of reference-based vs reference-free (from last class):
      - If you have an answer key in your golden dataset - that's reference-based evaluation (example: the UPSC case).
      - If there's no golden dataset and no correct answer key - that's reference-free evaluation.
    - Here: need to figure out the hallucination rate - is the chatbot hallucinating on any given question?
    - Question: is there a golden dataset here? Is there a correct answer key? No - it's not available. So this is a reference-free evaluation, but evaluation still needs to happen.
    - **Solution: use LLM-as-a-judge.**
      - Bring in a somewhat more powerful LLM.
      - Show it the retrieved context, the question the user asked, and the output the original LLM generated.
      - Ask it to determine whether the LLM is hallucinating or not.
      - Basically, write a detailed rubric to guide this judge LLM on where the original LLM might be hallucinating.

  - **Problem: cost of running the evaluator on everything.**
    - Question: can this evaluator (LLM-as-a-judge with a rubric) be applied to all 500 conversations?
    - If you have 500 conversations a day and need to check hallucination for all of them using an LLM-as-a-judge evaluator, running it on all 500 would be very, very costly - you're already paying for the 500 conversations from your chatbot, and now paying to evaluate them too could more than double your cost.
    - **Solution: Sampling.** Randomly select, say, 1,000 conversations out of the total (example numbers used loosely), and run your evaluator (LLM-as-a-judge) only on those sampled conversations.
    - This evaluator computes a quantity - hallucination rate - and that quantity is then sent to the dashboard, just like the captured quantities above, and from there you create alerts.
    - So the overall flow is the same as the captured-quantity flow, with two additions: sampling is needed (to save cost), and there's an extra evaluation step in between where you compute the value (hallucination rate).

  - **Is random sampling the best strategy?**
    - Question: is randomly sampling from all conversations the best strategy, or is there something better?
    - Idea 1: Ignore conversations that got a thumbs-up - most likely the student is happy with the chatbot's performance there, so hallucination is unlikely there (not an exact fact, but a good signal - keeping those wouldn't help much).
    - Idea 2: Focus more on conversations that got thumbs-down.
    - Also focus on: conversations that ended abruptly, conversations where escalation happened, conversations where the user is repeatedly rephrasing the same question, conversations involving money/refunds/admissions/fees, etc.
    - **Core idea:** not all conversations are the same. Use **stratified sampling**:
      - First divide all conversations into categories.
      - Then pull more samples from the categories that are "problematic" (e.g., a lot of money-related talk, or thumbs-down received) and fewer samples from normal categories.
      - This gives sampled conversations with a much better chance of correctly detecting hallucination.
    - (Note: to categorize conversations like this, you'd need a small model to detect which conversations have thumbs-down, which involve certain kinds of talk, etc. - this is a technicality, just to illustrate that sampling isn't plain random sampling, it's stratified sampling.)

- **Full flow recap for a computed quantity (online eval):**
  - Log everything.
  - Do sampling (stratified, ideally).
  - Set up your evaluator - the evaluator performs evaluation on the sampled conversations and gives back a metric.
  - Aggregate that metric over a time period and show it on the dashboard.
  - If a threshold is crossed, trigger the alerting system.
  - This is the entire flow for online eval. This is just one evaluation pipeline - you set up multiple such evaluators/pipelines like this.

---

### **LangSmith Demo - Evaluators**

- Under "Evaluators" → "Get started with evaluators" → "Show all templates" - many options are available.
- Categories seen:
  - **Security:** e.g., PII leakage (checks whether the chatbot is leaking any personal information) - works via LLM-as-a-judge behind the scenes. Prompt injection detection is separate. Code injection detection is separate.
  - **Safety:** toxicity has a separate evaluator; bias and fairness has a separate one.
  - **Quality:** hallucination has a separate evaluation pipeline; correctness has a separate one; conciseness; conversation quality checker.
  - **Trajectory:** this is actually for agents, not for chatbots.
  - Separate evaluators for image-based chatbots and voice-based chatbots.

- **Setting up a hallucination evaluator (walkthrough):**
  - Click on the hallucination evaluator, give it a name.
  - Select the application to run this evaluation on (an org can have multiple applications).
  - Select which model to use for LLM-as-a-judge (OpenAI, Claude, etc.) and provide your API key, plus settings like temperature.
  - Provide the prompt that will be given to your LLM-as-a-judge - define the rubric for detecting hallucination, give site-specific instructions, some reminders, some context (this will be covered in more detail later).
  - Then specify the output format you want back.
  - Then you get two options: run this evaluator on **tracing** or on a **dataset**.
    - **Running on tracing (i.e., on the logs):** this makes it an **online evaluator**.
    - **Running on a dataset:** since datasets live in the offline setup, this makes it an **offline evaluator**.
  - So LangSmith is an overall evaluation platform - you can do both online and offline evaluation on it.

- **Datasets in LangSmith:**
  - Under "Datasets and Experiments" you can create a new dataset and add examples to it - i.e., build your own dataset.
  - Select that dataset in an evaluator to make it an offline evaluator, or select tracing to make it an online evaluator.
  - Also has an option "Run an experiment" that gives you code to conduct offline experiments (to be covered in future sessions).
  - LangSmith provides the complete setup: create datasets, run offline experiments, do logging, do monitoring, do alerting, and run both online and offline evaluators. It's a complete evaluation platform.

---

### **The Self-Improving Loop - Closing the Loop Between Online and Offline**

- Recall from the first class: when a problem/failure occurs in production, in a particular conversation, you pick that conversation up and make it part of your dataset.
- This is the "Deploy and Monitor" part discussed earlier - when a failure happens in production, it's picked up and added to the offline dataset.
- In LangSmith, while looking at tracing, if some particular conversation has a problem (identified by you/your team), there's an option at the top: **"Add to Dataset."**
  - Clicking this adds that particular conversation to your offline dataset.
  - Next time you run offline evaluation, you run it on the updated dataset.
- This is how the loop closes - offline and online stay in sync, working together all the time.
- There's also an option to **annotate** - a particular conversation can be added to an annotation queue, and you can note what went right, what went wrong.
- Basically, you keep annotating the data coming in online and turning it into part of your offline dataset.
- This becomes a full circle:
  - Offline evaluation happens → goes to production → failures happen in production → those failures are picked up and added back to the offline dataset → offline evaluations are run again → deploy → new failures come up → the cycle continues.
- This is how the entire thing works - the **self-improving loop**: online failures get picked up and added to the offline dataset, becoming part of offline evaluation.

---

### **Wrap-up**

- That's all for today - the goal was to give an overall idea about online evaluation.
- Nothing was shown practically/hands-on today - just an overview of why it happens, how it happens, what the flow of things is.
- Very beginner-level class - no more depth planned for today.

---

### **Q&A Round**

**Q: Suppose a dashboard shows faithfulness = 0.87, toxicity/latency = 3 - is the bot good? How do we judge by evaluating a dashboard?**

- Every metric has a **baseline** defined, and that baseline generally comes from your offline evaluation.
- You compare against that baseline.
- Example: faithfulness = 0.87 and your baseline is 0.85 → 0.87 is better than 0.85 → you'd be happy.
- But if suddenly, in the last 24 hours, the faithfulness score drops to 0.75, that is concerning against the 0.85 baseline - this would trigger alerting, or you'd go and make improvements in the system.

**Q: If offline metric increases from 92 to 99, is that good for online production?**

- Depends - the question is incomplete: which quantity is going from 92 to 99? And is it the case that while this one metric went from 92 to 99, some other quantity dropped?
- If everything is improving well, then obviously it's a good thing.
- But improvement in one metric should not cause another metric to drop - because that's exactly what happens in LLM-based systems: improving one thing can cause regression, and other things can drop. That should not happen.

---

### **Mindset Note / Course Direction**

- Recall the point made before starting this course: after completing this course, you won't just think "I need to build a chatbot / I need to build a RAG chatbot," pick up an API, build software, and be done.
- Your level will go up - a mindset shift happens where you start thinking about how your chatbot will work correctly for thousands/lakhs/crores of people.
- That's the idea of this playlist - it's meant to set you apart from the competition, because not many people are studying this right now. Learning this gives you value - useful in interviews or when presenting yourself.
- This is technically the second lecture in the playlist, but there's clearly a lot of potential in this whole topic.

**What's next in the course:**

- How to build a golden dataset.
- How to run offline evals.
- How to run online evals.
- Along the way, some interesting tools and libraries will be used:
  - LangSmith (already seen).
  - DeepEval - a library.
  - Ragas - a library.
- Next up: **Benchmarks** - recall the earlier distinction between model-level LLM evals and application-level LLM evals. Everything discussed so far has been application-level. One or two sessions will now cover model-level evals, where benchmarks etc. will be studied, and then the course will move to application-level evals.

- Plan: aim to complete this playlist within this month (today is the 8th) - plus/minus one week.

- Next class - see you then. Good night.