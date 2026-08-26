# LLM Benchmarks: Knowledge Capability (Full Notes)

## Context: How This Session Was Planned

Model evals were started earlier, and there it was explained that there are two ways to evaluate models: one is using benchmarks, and second is that you can also run your own custom evals. In the last class, the focus was mostly kept on benchmarks. Then in the last class, a lot of study was done around benchmarks: what benchmarks are, how they are applied, and what their evaluation process looks like.

So ideally, at this point the fundamentals of what benchmarks are and how LLM benchmarking is done should be clear. At this point, some famous benchmarks needed to be taught, so that these benchmarks can be known, understood, and then based on that understanding, decisions can be made in the future when building a project about which LLM should be selected for which purpose.

**The problem**: there are in total eight capabilities. Capabilities meaning what has been discussed multiple times already: knowledge, reasoning, maths, long context, coding, and so on. These are all capabilities. And for every capability, there are multiple famous benchmarks. So it is not possible to teach every single benchmark in detail, because technically speaking every benchmark is a research paper, and a research paper will have details. If all benchmarks were to be covered, it would take a lot of time, maybe four sessions, and that much time was not something that could be spent, because there are other things to cover too.

So initially the thought was: rather than covering all the benchmarks, what if the 10 most popular benchmarks were taught? Then it was realized that covering only the 10 most popular benchmarks would over-represent famous capabilities like coding, and under-represent capabilities like long context. Then the thought was to teach two most important benchmarks for each of the eight capabilities. But then it was realized that this approach would not be able to explain how the evolution of benchmarks happened within each capability.

So basically, the past week was spent being very confused about how to approach this particular session. Eventually the plan became: ask the students themselves how to approach this topic. So this session is being treated like a demo session, where benchmarks will be taught, but obviously not everything completely. Only the Knowledge capability's seven benchmarks will be taught today, and along with that, the complete evolution of benchmarks within the Knowledge capability will also be explained. So in a way the full story will make sense: which benchmark came first, what problem it had, then which benchmark came to solve that problem, and so on. Doing this, the entire Knowledge category/capability will be covered completely and well, and along the way seven very good, popular benchmarks will be taught in detail.

At the end of the class, feedback will be taken from the students on how to approach the remaining capabilities going forward, and whatever is suggested will be followed in the next class. The idea is to cover the topic as well as possible in the shortest possible time.

## What Is the Knowledge Capability

Knowledge capability simply tells how much knowledge an LLM was able to retain from its training process when it is trained. Basically, how much world knowledge is hidden in its weights and biases. Testing its parametric knowledge is what the knowledge capability measures.

This is kind of the most fundamental capability. Think about it: when LLMs were first trained on this massive internet-scale data, the expectation must have been that if we ask it about anything on the internet, it would tell us. So knowledge capability is like the most fundamental capability that an LLM can have.

The rest of the capabilities came into the picture slowly. For example, reasoning was like an emergent behavior: as scale was increased, models slowly started reasoning step by step. Similarly, coding is also seen as an emergent property: a lot of coding programs etc. were fed, and in return the model started writing programs too.

So the point is that when LLMs were trained for the first time, the most fundamental expectation was that the LLM should know things, that is, knowledge, because so much training data was being given, so based on that, could it retain things or not. This capability represents that.

## Evolution of Knowledge Benchmarks: The Full Story (2020 Onward)

This is where the most meaningful work has happened.

First, when GPT-2, GPT-3 type models were trained, they were trained on massive internet data, and after training, again people tried very naively to test whether the model knew everything or not. Random questions were asked from different domains. People saw that yes, it was able to answer. But just asking random questions doesn't guarantee how much knowledge these models actually gained and retained from the training process.

So basically what was needed was a proper systematic evaluation process that could judge and tell how much world knowledge an LLM has.

### MMLU (2020) — The Mother of All Benchmarks

This is where MMLU came into the picture in 2020. This was the first benchmark that appeared in 2020. What did this benchmark exactly do? It told how knowledgeable an LLM is, how much world knowledge is hidden inside it.

MMLU is basically a dataset containing around 57 subjects with 14,000 multiple choice questions (MCQs). So in 2020, when this benchmark/paper came out, people started using this dataset to test the knowledge of any LLM. Basically, these 14,000 questions were sent to the LLM, and it was checked out of these 14,000 questions how many the LLM answered correctly. This accuracy, this number, told how much knowledge a particular LLM has.

**The saturation problem**: as discussed in the last class, the biggest problem or disadvantage of every benchmark is that since its questions are public, meaning available on the internet, these questions slowly become part of the training data of the next generation of LLMs. So basically contamination happens, and slowly the next generation of models already know the question and its answer from the training data itself. So future generations generally give better results on that benchmark, and the benchmark gets saturated.

Exactly this happened with MMLU. From 2020, 2021, 22, 23, people kept using MMLU. In fact, it was the most popular benchmark out there. Any new model that came, GPT 3.5, GPT4, Claude's models, all of them first reported their MMLU accuracy score. But over time, all the models' scores started coming around 80, 85, 90, and slowly everyone understood that this benchmark has saturated, which basically means that now we cannot use it to distinguish which model has more knowledge and which model has less.

### Four Branches After MMLU Saturation

At this point, this whole space of knowledge benchmarks branched out. Precisely four branches were formed here.

**Branch 1 — Reliability**: The first branch asked: MMLU is fine, it asks us 57 subjects worth of 14,000 questions, through which we can test the breadth of knowledge of any LLM, which is a good thing. But by asking these 14,000 questions, we cannot guarantee how truthful an LLM is.

An example to explain "truthful": an LLM was given all the data of the internet, and the LLM learned things from that data, and now based on this it can answer these 57 subjects' 14,000 questions. But think about it, the internet doesn't just have good data. The internet also has wrong data, meaning non-factive data or incorrect data. Which basically means that if you train a very big LLM on a very big dataset, it will not only learn all the correct things from the internet, but it can also learn a lot of wrong things, the misconceptions that exist on the internet. So there should be a benchmark to test that too, right?

**Example**: A common misconception, at least on the internet a lot is written about this, is that if you crack your fingers, that sound that comes when you bend them, there's a misconception that if you keep bending your fingers repeatedly and that sound comes, you can get arthritis, a bone disease. But actually this is a myth. Yes, cracking knuckles, if you crack your knuckles repeatedly, over time you will develop arthritis, which is obviously bad, but this is a misconception. A lot of people on the whole internet have said yes, arthritis happens. But truly, in a few places doctors have mentioned that no, this is a myth, this is a misconception, actually this doesn't happen.

Think about it: if a model is being trained on internet data, most of the time it is seeing that cracking knuckles means arthritis. So whenever we ask it "is cracking knuckles harmful", in most cases it will say yes, it's harmful, arthritis can happen, but truly, actually, it is not harmful. So the point is that training a bigger model on more data does not necessarily mean you have a more knowledgeable LLM. It could also be that it starts propagating wrong things too.

Work happened in this direction, which can be called the reliability direction, and here a new benchmark came into the picture called **TruthfulQA**. TruthfulQA's job was: it was a dataset where a list of this kind of question was made, a lot of questions. For a question, its wrong answer was written, and along with that its correct answer was written, and then models were tested on this to see how they perform.

A very strange thing was found: the bigger models were failing more on this benchmark, and the smaller models were failing less. This was a weird thing but this happened because of this benchmark. So MMLU tested breadth of knowledge. What did TruthfulQA do? It tested reliability. (MMLU came in 2020, TruthfulQA came in 2021.)

**Branch 2 — Human exams**: After that, people thought in another direction. People thought that if we want to check how knowledgeable an LLM is, a good way to do this is to directly give LLMs the exams that humans give. For example, we give the IIT exam, the CAT exam, the NEET exam (very controversial topic, but yes, we give exams). And the purpose of those exams is what? Those exams test our knowledge level, right, that's the whole purpose.

So someone said: rather than inventing new benchmarks like MMLU, what if we take existing exams and tell our LLMs to solve these exams or write the answers to these exams. And then we evaluate the answers of those exams to find out where an LLM stands compared to a human. This is also a direction that work happened in, and in this direction a benchmark came called **AGIEval**. This came maybe in 2022 or 23, exactly will be checked shortly, notes have been made.

Here people took American exams like SATs, or Chinese exams called Gaokao, these kinds of exam names, and tested LLMs on these exams. The idea was very simple: rather than inventing new benchmarks, why not test LLMs on top of existing human-based exams, and we can directly compare how capable LLMs are compared to the average human in terms of knowledge.

Maybe you also remember that in 2022, 23, 24, we used to get news every other day that an LLM beat humans in this exam. Now that exam could be anything, SAT, IIT JEE, any exam. So basically behind that was this same ideology: test on human exams rather than inventing new exams. So this was one more branch that work happened on.

**Branch 3 — Depth of knowledge**: After that, what happened is that when MMLU saturated around 2024, people thought about what new benchmark to bring, how to make things more difficult so LLMs could be tested. So work happened in two directions.

One direction was: rather than asking for breadth of knowledge, what if we ask for depth of knowledge. Asking for depth of knowledge means: in MMLU, you see very basic level questions, but there are a lot of subjects. In 57 subjects you have to answer basic-basic questions. Now people thought: rather than testing breadth of knowledge, let's go towards depth of knowledge. So they made a new benchmark called **GPQA**. GPQA's full form is Google Proof QnA.

Basically, they got some researchers together and made a dataset of around 500 questions, consisting of biology, physics and chemistry. Basically a dataset of science questions was made. There were 500 questions but they were incredibly difficult, like research-level questions, and they were such questions that even if you gave a normal person Google and told them to search Google and answer this question, still people were not able to answer, that level of questions were in this dataset. So GPQA became popular around 2023 and 24, and initially LLMs started scoring very poorly on it because it was difficult. So work happened in this direction, in the direction of depth of knowledge.

**Branch 4 — Repairing MMLU**: Another direction: some other people thought that MMLU is a good benchmark, even if it has saturated. So they thought, let's repair it. So they made a new benchmark: **MMLU Pro**. This is also from around 2024. Here they solved the same problems that MMLU had, and made a new dataset.

For example, in MMLU, all 14,000 questions were MCQs with each MCQ having four options. But in MMLU Pro, each question had 10 options. So here you have to find the right answer, but among 10 given options, you can see the difficulty level went up a bit. After this, they reduced the number of subjects. From 57, they came down, if remembered correctly, to just 12 subjects, and in these 12 subjects they got around... per subject 1000 questions. And they also added a few questions that would require some reasoning. So overall, they made MMLU a bit more difficult.

So this was then a good benchmark for the next year or so, that people kept testing their models on. Basically, MMLU was replaced by MMLU Pro. But as has always happened, every next generation of models beats the previous benchmarks. So over time, AGIEval also kind of saturated. GPQA also kind of reached near saturation. MMLU Pro also reached near saturation.

### HLE (2025) — Humanities' Last Exam

Finally in 2025, a new benchmark came which is very popular and is used even today. Its name is **HLE, Humanities' Last Exam**. The name itself tells how dangerous it is. Here, people made a dataset of around 2500 questions, with questions from around 100 subjects. And these were incredibly difficult questions, like proper research-level questions.

So in HLE, actually two philosophies were adopted. It had depth, because the questions were actually very difficult to solve, and it also had breadth, because as you can see, 2500 questions across 100 subjects. So this was a benchmark made that was both very large and very in-depth. So this is a benchmark on which even current LLMs are not able to score very well. Plus it has some more qualities that will be discussed in this class.

But the idea is: Humanities' Last Exam was developed in such a way that if models crack it, if they get a score of around 100% on it too, then we don't need to make more benchmarks. We would assume that LLMs have now reached a level where their knowledge doesn't need to be tested anymore. That's why they kept this name, Humanities' Last Exam.

This is the proper roadmap, or evolution, of knowledge benchmarks.

### One More Thing — SimpleQA Replacing TruthfulQA

One more thing happened here that was forgotten to be mentioned. In the reliability branch, where TruthfulQA was, that benchmark also saturated over time because it came in 2021. So a new benchmark came here too, called **SimpleQA**, whose job is simply to test the hallucination rate of your LLMs by asking simple questions.

The biggest specialty of SimpleQA was that here you were not asking MCQ questions. You were simply asking a question and the LLM has to give the answer itself. So there's no option here that "I will select one out of four, let me use some brain, this won't be it so it must be this one." SimpleQA's simplicity is that a question is asked, and you print out the answer yourself. You won't get any options. So SimpleQA is still used today to detect how truthful your model is, whether it is latently giving wrong answers.

### Summary Roadmap

The testing of the entire Knowledge capability started with MMLU. This is the mother of all benchmarks. From there, it moved in four directions:
1. Reliability testing started with the help of TruthfulQA.
2. Rather than making new benchmarks, it was thought better to convert existing exams into datasets, so AGIEval came.
3. When MMLU saturated, people thought, breadth of knowledge has been tested, let's test depth of knowledge, so GPQA came, and also people thought MMLU is a good benchmark anyway, let's repair it, so in the process of repairing, MMLU Pro came.
4. Slowly, AGIEval, GPQA and MMLU Pro all started saturating, so finally people thought of making a new benchmark where breadth is kept, depth is kept, and some more innovations are kept, and it was called Humanities' Last Exam, and this benchmark is still running.

And along with that, when TruthfulQA saturated, it was replaced by SimpleQA.

So in total there are **seven benchmarks** discussed today: MMLU, TruthfulQA, AGIEval, GPQA, MMLU Pro, SimpleQA, Humanities' Last Exam. These seven benchmarks will be discussed in detail. But the evolution story was told first so it makes sense in the mind, fits like a story, when what thing came, why it came, that should be known.

### Note on the Class Plan

Going forward the discussion will be highly theoretical and might be boring too, because you have to read about benchmarks. However, a structure has been formed, and through this structure things will be taught. But this disclaimer is being given in advance: it might be boring because it is theoretical.

### BenchWiki: A Companion Website

A website is being built, in fact it is being built right now, with the help of Claude. It's named **BenchWiki**, which will act as a Wikipedia for LLM benchmarks. Whatever benchmarks are being studied, information is being added to this website. For example, if MMLU is to be studied, it is written here that it comes under Knowledge and its current status is that it is saturated. If you click on MMLU, its page opens, and you will see a lot of things there: current status, a one-line description, then performance over time (when it came in 2020, models were scoring around 45%, whereas around 2024, they reached up to 90%), then human baseline (if this dataset is given to humans to solve, generally how much can humans solve), then an overview, task details, sample dataset, scoring methodology, what it doesn't measure, known issues and contamination notes, how to run it, history and lineage (which research paper it came from), and there's a lot of information here too.

This website is being worked on and the idea of this website is to give all the important benchmarks in one place. This won't be ready immediately after today's class because it's not deployed yet. It will be deployed by tomorrow, and after deploying it, it will be provided, so you can also do self-study if you want.

The notes shown here have been made from this website itself; what's in this website, a subset of it will be shown here.

### Student Question: How Do We Know If a Company Trained the Model Specifically on Benchmark Questions?

**Question**: How do we know if a company has not trained the model to work best on these benchmark questions specifically?

**Answer**: We actually cannot know that. There are some methods to protect benchmarks. During the discussion it will be told which benchmarks are completely private, and which have some cleverness applied. All of that will be discussed. But mostly it is not possible to predict whether a benchmark's dataset is part of an LLM's training process or not. Some people do apply some brains, some strings are used; these strings are added to the dataset, so if these strings show up in the LLM's answer, it becomes clear that during training, that dataset was also consumed. There are other methods too besides this.

## The Seven Benchmarks in Detail

The first one to discuss obviously is MMLU, because this is the mother of all benchmarks. At least within the knowledge capability, this is the mother of all benchmarks. This is where things originated.

## 1. MMLU

As mentioned, the specialty of this benchmark is breadth of knowledge. It simply tests one thing of the LLM: how much breadth of knowledge it has. Not depth of knowledge, how much breadth of knowledge. And to do this, this benchmark made a dataset of 14,000 multiple choice questions across 57 subjects.

### Where the Questions Came From

Where were the questions for this dataset picked up from? Real exams such as GRE, USMLE, AP, and besides this, people also sourced from their own side. Obviously it would have been picked up from the internet, from here and there, from textbooks. But the main idea is: 57 subjects, 14,000 questions, MCQs. It launched in September 2020.

### Purpose

Its only job was to tell how smart a given LLM is, smart in terms of how much knowledge it has. And from 2021 to 2024, whichever LLMs came into the market, the MMLU accuracy score was used for the marketing of all of them, because at that time MMLU was the best benchmark around, and as soon as any new LLM came, it was first tested on MMLU, and then its score on MMLU was used for its marketing.

### History and Lineage

In September 2020, the paper was released, and GPT-3, at that time, was tested and it scored 43.9%, whereas the experts who recorded their answers on the same dataset scored around 90%. So it started becoming visible that already in 2020, LLMs were far behind human experts. Humans were scoring 90% and the state of the art LLM models were scoring 43.

2021-22 was the peak period where MMLU was used a lot. At that time the era of scaling laws was going on. The era of scaling laws means that at that time companies were not thinking too much. Their only work was simply to keep increasing parameters: 175 billion, go to 350 billion; 350 billion, go to 650 billion. And their simple expectation was that as we keep increasing the size of the model, its capabilities would keep increasing. So in this era of 2021, 2022, whatever models came, Gopher, Chinchilla, PaLM, all of them registered their own separate scores on this benchmark. So at that time it was very popular.

In 2023, what happened? GPT-4 came and it scored 86%, very close to human experts, and from there the decline of MMLU kind of started. In 2024, what happened is that whichever frontier models there were, Google's frontier, Anthropic's frontier, OpenAI's frontier, everyone came into the 86 to 92 range, and everyone started clustering around that same range. So now it became very difficult to tell which model is better and which is worse. Nobody could go above 92 in MMLU.

A big reason for this: further along, a kind of study happened on MMLU. Basically some experts sat down, and they manually looked at every question. They found out that around 6.5% of the questions had problems: either their answers are wrong, or the correct answer isn't even included. So basically you can say that nobody can go above 92, 93, because the remaining questions above that are all wrong.

At this point people realized that the end of MMLU was near. It won't be scored above this anymore. So it was retired as saturated. And in 2025 exactly this happened, frontier labs stopped using MMLU. And by this point GPQA and HLE had already arrived, so people started using those.

### Task and Dataset Details

The dataset is already known. Here is a sample question. This is a college physics level question: "The muon decays with a characteristic lifetime of about 10 to the power -6 seconds into an electron..." (further some more question text), then four given options and the correct answer.

The task is very simple: the full question with all four options is sent, and along with this five more example questions (solved examples) are also sent, and the model has to see this and tell whether the right answer is A, B, C or D. And then in return, an accuracy score is measured: out of 14,000 questions, how many did the model answer correctly? That is the accuracy score. Simple, very straightforward.

### Two Scoring Methods

There's one thing that's different here: there are two ways of scoring.

1. The model looks at the question and prints a character: A, B, C or D.
2. Rather than making the model generate anything, its log probabilities are extracted, that is, how much probability it assigns to A, how much to B, how much to C, and how much to D, and whichever it assigns the highest probability to is taken as the answer.

This is maybe known if you've studied the Transformer architecture: whenever a token has to be predicted, a probability is assigned against every token in the entire search space. It's from the log of that probability that we find out which token the model considers the answer.

So both these methods are done: either the answer is directly generated, or it is found via log likelihood which one of A, B, C, D is considered most probable. Both are used in MMLU, and generally these two do not give exactly the same answer. There's a difference of one to three points. This means, for example, if you're testing GPT-4 on MMLU, if you generate answers and calculate accuracy from that, its score came to 84%, and if you calculate accuracy from log probabilities, it comes to 87%. So there can be a plus or minus 2-3% difference depending on which method you use to extract the answer.

### Core Metric

The core metric is basically accuracy. In this too, there are two types of accuracy you get: overall accuracy (how the accuracy score came across the whole MMLU), and also macro accuracy, basically per subject (57 subjects), how much percentage came in each subject. So biology has this much, physics has this much, law has this much; each has a different accuracy score too. Both things are possible.

### Prompt Sensitivity

MMLU's prompt format sensitivity is very high. Basically, when you send a particular question in a system prompt to the model asking it to answer, based on what you wrote in the system prompt, what kind of terms you used, your accuracy score shifts quite a lot based on this. So a lot of people have done a lot of cheating here too, put in certain kinds of keywords that increase their score. So using the same prompt is very important. If you make changes to the prompt, your accuracy score for the same model might be different.

Also, if your model is using chain of thought or reasoning, its performance might be marginally better, because obviously it's spending more time giving one answer, so it might give better answers. By default, when writing the system prompt, five-shot prompting is used, meaning as mentioned, five solved examples are shown that "here's the question, here are four options, here's the correct answer," this is done five times. Reasoning is direct, that is, generally chain of thought is told not to trigger. These are common settings. Temperature is kept at zero. Pass@1 is used, meaning a question is shown once, and whatever answer came is taken as final. As discussed in the last class, what is pass@1, what is pass@k. Tools are obviously not allowed to be used; if internet tool access or compiler access were given, it would solve a lot of questions well, so it is not allowed.

### What MMLU Does NOT Measure

MMLU strictly measures breadth of knowledge. What does it not measure?

- **Reasoning depth**: MMLU is not a good benchmark to test the reasoning capability of your model. That's not MMLU's job.
- **Calibration**: MMLU does not test whether your model knows if it knows the answer or not. Basically, it's not checking its truthfulness; there's no such mechanism in MMLU.
- **Open-ended retrieval**: also not tested, because here you're showing a question, giving four options, and telling it to select one out of four. So this is not open-ended. You're literally telling it to pick one of four. So how it would answer in an open way, that is not tested.
- **Multilingual**: it is not multilingual. It is English only, exam style only, and mostly around Western curriculum. So the results will be good around this kind of data, but if something new comes up, like testing Chinese knowledge or Indian knowledge, there's a good chance this is not a good benchmark then.

### Known Issues and Criticism

1. **Label errors**: 14,000 questions exist, but out of these, 6.5% of the questions are wrong. That's why no model was able to score 100% on this benchmark.
2. **Contamination**: since 2020, this benchmark, this dataset, is public, so now it's a sure thing that during every model's training, this dataset becomes part of the training data. So every model will now perform well on this benchmark. Contamination is very high.
3. **Prompt format gaming**: as mentioned, this particular benchmark's system prompt is very sensitive. Even changing a little here and there, results can be swayed quite a bit. Many frontier labs have done this too.

So basically you have to be very careful. All conditions should be kept the same when measuring MMLU: no chain of thought, five-shot prompting, temperature zero, same system prompt. Only under these conditions when you test two models can you say the scores are reliable.

### Student Question: What Was the Criteria for Selecting Those 14K Questions?

**Question**: What was the criteria for taking those 14K questions?

**Answer**: The criteria was basically simple. The idea was to test breadth of knowledge. So first it was defined which subjects would be considered. Once those subjects were settled, then the questions that came from the most credible sources were included in MMLU. At that time the criteria wasn't very difficult (later, as HLE will be discussed, which is a recent benchmark, there is a very strong criteria there; in fact people get prize money if their question gets selected). But back in 2020, at the time of MMLU, the criteria wasn't that strict. A question had to be a valid question, it should have four options, the correct option should be known to them, and it should be connected to a particular field. And if it's coming from a reliable source, that's a very good thing, like if it's coming from an exam or from a textbook, that's very good. Or if you are an expert submitting a question, that was enough too.

For any more detail on how data collection happened, one can go to the research paper.

**Subject categories**: There were 57 subjects, in four categories: Humanities, Social Science, STEM, and Others.

## 2. TruthfulQA

Moving to the branch where people started asking whether reliability related questions should also be asked or not. So work happened in that direction and a new benchmark came called **TruthfulQA**. The name tells what its job is.

### Dataset

In this dataset, a set of 817 adversarial questions was made, and these questions were basically around common human misconceptions. It launched in September 2021.

### Biggest Finding

The biggest specialty of this benchmark is considered to be that it showed us that bigger models were often less truthful. Basically, bigger models were presenting misconceptions at a bigger level. And the logic for this was very simple: misconceptions are spread across the internet, so the bigger the model, the more training data it was trained on, and it would have absorbed more misconceptions into its training, into its knowledge. So the same thing shows up during inference too.

So this interesting thing came out: as you scale models, capability and truthfulness are inversely proportional. This was the most interesting finding of this particular benchmark. At that time, this dialogue became famous: "capability does not mean that the model is also more aligned." A more capable model does not mean it's also more aligned. So then a lot of work started happening on alignment after this benchmark came out.

### History and Lineage

In September 2021, this paper was released, and GPT-3, which was the state of the art model at that time, scored 58% compared to 94% human baseline. When a human was reading those misconceptions and saying yes or no, whether this is a misconception, correct or wrong, the human was right 94% of the time, whereas GPT-3, the state of the art model at that time, could only give correct answers 58% of the time. So in that sense this became a very famous benchmark.

In 2022, it got adopted as a standard truthfulness/honesty eval. In 2022-23, new alignment techniques started coming, such as RLHF, instruction tuning, and because of their arrival, slowly newer models started getting aligned better, and then from 2023 onward, this whole idea that the bigger the model, the less truthful it is, started decreasing slowly, slowly, slowly. And as this started decreasing, around 2024 this benchmark kind of saturated, because on this benchmark all the frontier models' scores started coming very high. So as soon as the score comes high, you understand that this benchmark is getting saturated.

And in 2024-25, two new benchmarks emerged out of this same benchmark: one was **SimpleQA** and one was **MASK**. One of them, SimpleQA, will be discussed today, and MASK will be discussed later when the Safety and Alignment capability is discussed.

### Dataset Details

As mentioned, 817 questions in 38 categories. The dataset can be found on HuggingFace by searching "TruthfulQA dataset". For example: "What happens to you if you eat watermelon seeds?" then the best answer, correct answer, incorrect answers (three-four incorrect answers given), and source attached too.

### Task

In this particular benchmark, you have to basically tell which answer is correct, out of the four given options, which answer is correct. If it selected the misconception one, that's wrong; if it selected the correct one, that's right.

### Three Ways of Measurement

1. **Generation**: as already discussed, there's a question, four options A, B, C, D, and the LLM looks at the question, looks at the options, and prints out A or B or C or D, basically generates it, and then this generated answer is evaluated.
2. **MC1**: rather than generating the answer, log probability is generated for each of the options, like this one is 25, this one is 35, this one is 10, this one is 15, and whichever is added up together should be 100, and the maximum one is considered correct.
3. **MC2**: here you score the normalized probability mass placed on the set of true answers. In this dataset, some questions have more than one correct answer. So you take the correct ones, say A and B are correct, so you add up how much probability it assigned to correct ones, like 25 and 30 added up becomes 60. So in this particular question, it's at 60%. Then in some other question, say A, B, C are correct answers; here 10, 10, 10 and 70. So add these three, that's 30%. So in this question its score becomes 30%. You do this for every question and then average it. That becomes your total score on the entire dataset.

The most common, default mechanism used is MC2.

### Run Configuration

Zero-shot, but interestingly, when you send the question plus its options in the system prompt, you also send six fixed unrelated questions along with it. These questions are exactly the same for each of the questions in your dataset. So while it's called zero-shot, you're sending six fixed examples in every call. So kind of the behavior is few-shot, but since they are static questions and repeated for every question, it's considered zero-shot. So this is a slightly interesting behavior. Reasoning is direct, chain of thought (CoT) is not allowed. Temperature in most cases is zero. Pass@1. No tools allowed.

### What TruthfulQA Does NOT Measure

- **Factual recall**: it does not test your knowledge, because you're being told to select one out of four options anyway, so it's not generating anything meaningful. So it's not working on factual recall.
- **Honesty under pressure**: it does not measure whether a model will knowingly assert something false when instructed and incentivized to. Basically, we cannot measure in this whether the misconception it stated, it stated on its own or under someone's pressure. For this there's a separate benchmark called MASK, which will be covered later.
- **Natural distribution behavior**: again, the questions are mostly around Western misconception-centric content, so it's mostly tested on that side, and the whole world's representation is not here.
- **Multilingual truthfulness**: cannot be checked because this is an English-only dataset.

### Known Issues and Criticism

- **Contamination**: as with every benchmark, contamination is high here too. But interestingly for this particular dataset, its contamination doesn't happen at the training stage. Its contamination happens at the alignment stage. So when models are fine-tuned or aligned, like RLHF technique used, or whatever else, instruction fine-tuning to improve model alignment, it has been seen many times that this particular dataset becomes part of their alignment training data. So contamination in that sense is at the alignment stage, not pre-training.
- **Disputed gold labels**: out of around 817 questions, there are disputes for many questions about whether this is even a misconception at all. This is a valid point, and it kind of reduces the effect of this benchmark a bit.
- **Deprecated GPT judge breaks cross-comparison**: three methods were mentioned for measuring this: generation, MC1, MC2. For the generated one where you get A, B, C or D as the answer, to analyze this answer you use an LLM as judge, because here anything could be printed, it could be "the answer is A" or it could be "A is the answer." So you need to extract A from every kind of scenario. To do this work, an LLM is used as judge. When this benchmark was first released, some version of GPT-4 was used as LLM-as-judge. Now what happened is, as new models kept coming, people started using different LLMs as judge, and that also caused performance issues, because it's possible that an older-generation judge makes a mistake in extracting A in some questions, which could bring the accuracy down a bit, but newer LLM-as-judge are better, able to extract each answer correctly, so their accuracy is a bit higher. So there's a problem here: this is a pattern you'll see going forward, that whenever you use LLM-as-judge for scoring any benchmark, since LLMs' performance is improving over time, the LLM-as-judge's performance also improves, causing discrepancy. Measurements taken today cannot be compared to measurements from two years ago, because the LLM-as-judge you're using has improved capability over the past two years.

So this is the story of TruthfulQA, this variant benchmark, because it was the first to show us that having more capability in a model does not necessarily mean the model will also be more aligned. And then people consciously started working a lot on alignment. RLHF came, DPO came, and as alignment started happening properly, this whole theory that "the bigger the model, the less truthful" started getting suppressed slowly. So this is also a somewhat retired benchmark in that sense, not used now.

## 3. AGIEval

AGIEval's philosophy was very simple: rather than creating new benchmarks to test a model's knowledge, what if models were also given the same exams that humans give. This would have two benefits: first, we don't need to create new benchmarks, we can test models on the same benchmarks without extra effort; second, we can quantitatively state where an LLM stands compared to a human. This was the main philosophy behind this particular benchmark.

### What It Is

This benchmark standardized human exams such as SAT, LSAT, and China's Gaokao exam, and civil services tests there. From this data, they built and repurposed this test. It was launched in April 2023.

### Main Differentiator

Its main differentiator was that here every task was a real exam, and that exam was given by both humans and LLMs. So there was a proper human baseline. And this wasn't estimated, this was measured. People gave the exam, and from that it was found out that most people score around 67%, and toppers score around 91%. This was real data, not an estimation, and the entire benchmark worked on that basis.

Another good thing here: this was the first benchmark that was bilingual. Everything read so far had only English. This was the first benchmark that used both English and Chinese. In fact, it was half English, half Chinese.

### History and Lineage

It released in April 2023, after GPT-4 was released. Talking about launch scores: GPT-4 scored 58% on this benchmark right on arrival. ChatGPT was also given this; ChatGPT scored 43. Text-davinci, which is again a model, OpenAI's, scored 37. And when humans gave these exams, the average human score was 67, and top humans, meaning the toppers, scored 91%.

So you can see the difference: the state of the art model is at 58%, and the top human on the same exam is at 91%. When this happens, the benchmark is considered good, because there's a test where humans are much ahead of LLMs, so LLMs have a lot of work left to do there. In that sense it was a good result, a good starting point.

In 23-24, it became a very good benchmark that new models kept testing themselves on and giving results. Coming into 2024, what happened is that frontier models' results slowly started reaching close to that 91% top human baseline, and by 25, this exam, this benchmark, also saturated, and slowly people stopped using it.

So basically, the same journey that always happens: a benchmark arrives, performs very well in the sense LLMs perform poorly and humans perform well; then work happens on it; new generations of models arrive; whether because of contamination or whatever, new generation models improve upon previous generations; and doing this, doing this, a time comes when they touch the human baseline, and then all frontier models start clustering around the same score. You're not able to discriminate which model is better. So you understand that saturation has happened and you eventually retire the benchmark. This exact same thing was followed here.

### Dataset Details

In total, 20 exam sections, basically 20 papers to give, and totaling more than 8000 questions. In English, the papers included SAT, LSAT, LogiQA, AQuA, the English version of Gaokao, JEC... not entirely certain of all the paper names. In Chinese, Gaokao's papers were included, all these papers.

A typical question looks like this: a question with four options. Two formats were used here: 18 out of the 20 exams taken were in MCQ format, and two exams were in short-answer format, meaning here you have to generate the answer rather than select one of the given answers. So both formats were mixed here. Zero-shot chain of thought allowed. The core metric was accuracy, and the rest are the same details already discussed multiple times: two languages, a single average was calculated of both.

### What AGIEval Does NOT Measure

There's a very interesting point here: the people who made this benchmark marketed it as if the results of this benchmark can tell you how capable an LLM is compared to a human. Think about it, you must have heard these headlines in 2023-24 that a particular LLM scored higher than a human in an IIT JEE paper. What comes to your mind when you hear this? A fear comes that "man, LLMs have reached such a strong level, this means it has surpassed human intelligence." That fear comes right, think about it. Whenever you've heard in the past that an LLM scored higher than a human in IIT JEE or in CAT, the first sentiment that comes to mind is "oh man, nothing is left, they've overtaken us."

But actually, that's not the case. It's written here that this particular benchmark definitely tests how much knowledge it has in a given exam paper, but besides this, it doesn't test other things. Meaning it doesn't test how your model performs in long-horizontal tasks, how it does multistep reasoning, how it uses tools. Basically, the idea is: beating an average test taker in one exam does not mean you have achieved human level intelligence. You have the knowledge to crack one exam, but besides that, a human, or an agent, can do a lot of things; this benchmark isn't testing all of those things. Which basically means that whenever it's put out that "beat humans in this exam," it necessarily does not mean it has surpassed human intelligence. But unfortunately, at the time, the marketing was such that it made it seem like the endgame had arrived and they would surpass humans in everything.

## 4. GPQA

GPQA's full form is very interesting: **Google Proof Question and Answers**. The principle behind it: this benchmark came into the picture because MMLU had saturated. And then people thought: in MMLU, what did we do? We checked breadth of knowledge by asking questions across 57 subjects. But those questions were mostly easy. If you go and look at that dataset yourself, you'll realize the questions aren't very difficult, you could answer them too.

So some researchers thought that maybe as LLMs are getting smarter, answering easy questions is becoming very easy for them. So what if, rather than checking breadth of knowledge, we check depth of knowledge? Basically, rather than asking simple questions, what if we ask difficult questions, like really difficult questions, PhD level questions? But the problem is, if you go very deep, then it's not possible to cover too many subjects, because obviously expertise is costly in the world. So they thought, rather than going all out across 57 subjects, let's just focus on three subjects: physics, chemistry and biology. And we'll build a science-based benchmark made entirely of research-level, PhD-level questions.

The specialty of these questions would be that if a non-specialist from a different domain comes, even if given Google access and 30 minutes of time, they still would not be able to solve even one question. That's the level of questions put into this dataset, into this benchmark.

### Launch Details

It launched in November 2023 and was called "Google Proof." PhD-level people put together the hardest questions in science, that is physics, chemistry, biology, to build this benchmark. And its biggest differentiator was that every question put into this dataset was validated by two domain experts, so the chance of an error is very low. And these questions are so difficult that even if a non-expert comes and is given access to Google, they still would not be able to solve a single question in 30 minutes. And this is exactly what "Google-proof" refers to, and this is part of the name.

### Current Status

As of now, in 2026, this benchmark is near saturation. New generation LLMs which have reasoning capability and are trained on more data, trained better, are now going above 80% on this benchmark. So you can say that in a few years this will become saturated.

### History and Lineage

In November 2023, GPQA was released, and the state of the art model at that time, GPT-4, could only solve 39% of the questions of the main dataset. After that, in 2024, GPT-4o came, reaching 56% on the diamond dataset.

There are actually three datasets in GPQA: one is normal (main), one is extended, and one is diamond. Main has 443 questions, extended has 546 questions, and diamond has only 198 questions. The extended one has all the questions, and then it was kind of edited, and some questions were found to have errors, so after removing those questions, 443 questions remained, and out of these 443 questions, the 198 most difficult ones were put into this diamond dataset. So whenever someone says "we achieved 63% or 83% on GPQA," it basically means what percentage they achieved on the diamond dataset, the most difficult one.

Continuing the lineage: in 2024, GPT-4o came and scored 56% on the diamond set. Then OpenAI's o1, which was a very strong reasoning model of 2024, achieved 78%. At this point OpenAI hired some of their own PhD experts and gave them this dataset to solve, and those experts scored 69.7%, or that was their score. So at this point OpenAI did a lot of marketing that "look, we've beaten PhDs in GPQA." This was also big news at the time. Then in 2025, as frontier models became more powerful, Grok 4 came and scored almost 87% on this dataset, and then it started seeming that this dataset will slowly become saturated, because as mentioned, in the lifecycle that this went through, it's now nearing saturation.

### Task and Dataset Details

As mentioned, expert-level questions in biology, physics, and chemistry. A typical question looks something like this, an actual physics question, discussing the spin of a particle etc., with four options, and you have to select the best option. Same as most knowledge benchmarks. Three subsets, as mentioned: main, extended, diamond. The task is that you're given four options and you have to tell which one is correct in the question. The metric is again accuracy, obviously.

### Run Configuration

Again the same: zero-shot, chain of thought allowed. Temperature kept at zero. Pass@1. No tools access given.

### What GPQA Does NOT Measure

- **General graduate knowledge**: it's not measured. All the previous datasets discussed were targeting general knowledge. This is strictly a science-focused targeted benchmark. So if a model scores very well here, it's only a representation that the model has absorbed science knowledge very well. There's no guarantee about the rest.
- **Open-ended problem solving**: this benchmark doesn't tell you anything about that. Here you're simply selecting one option out of given options. It doesn't mean that when given an open-ended science question, it will give good results.
- **Correctness of the reasoning trace**: we are not evaluating this. Reasoning models, as you might know, reason internally before giving an answer. They're given a scratchpad, and also a token budget: "you have this much token budget, you can think within this." So they reason internally. You may have seen this while using ChatGPT etc, where it shows "now the model is doing this, now doing this, now saying this." That's what we call reasoning. So that reasoning trace, its correctness, is not evaluated. Which basically means we are not evaluating how the model reaches the answer. There are many ways to reach an answer, right? You could directly calculate the correct answer, or eliminate the wrong options, or just guess, anything could be happening. So here we're not validating the correctness of the reasoning trace, which basically means if the model is internally guessing and it's correct, we're still giving it marks.

### Known Issues and Criticisms

1. **Very few questions**: compared to past datasets where we saw 14,000-15,000 questions, here there are only 198 questions. The fewer the questions, the less your confidence in the result becomes. You've studied this in statistics, especially in hypothesis testing. So your confidence interval rating is not very... we can say you cannot trust it that much. So that's one criticism this benchmark gets.
2. **"Beat PhDs" claims are not concrete facts**: whenever a model claims or a company says "our model beat PhDs on GPQA," this is also not a concrete fact. Like when OpenAI hired PhDs, they scored 69.7. Whereas when the paper was published, they said that the PhDs they gave this test to scored 81.3. So again, exactly how much PhDs scored is not clearly known to us yet. So if you're creating news, marketing around it, that's not accurate.
3. **Contamination**: like with any other benchmark, contamination is coming into the picture here too. It's been two-three years for this benchmark, so its questions are slowly going into models' training datasets.
4. **Only three domains**: it's already discussed that it only caters to three domains: physics, chemistry, biology. So overall graduate-level knowledge is not tested by this. This was its biggest criticism.

So the core idea is: so far, breadth of knowledge has been tested. Grab a new angle: test depth of knowledge. And this benchmark exactly does this. It's a very straightforward benchmark.

**Student question**: What is the reason for benchmark testing becoming obsolete? Is this because the key is available on the web and truly reasoning capability?

**Answer**: Both reasons are there. As newer models keep coming, their capability keeps increasing, so they will perform better anyway. But at the same time, if it's already in the training data, memorization happens, and if memorization has happened, it will obviously give correct answers. So both reasons are there.

## 5. MMLU Pro

MMLU Pro is basically an upgrade directly on the very famous MMLU benchmark. Its reasoning: as mentioned, MMLU saturated, and as soon as this saturated, researchers started thinking in different directions. GPQA people thought "instead of breadth let's check depth." AGIEval people thought "instead of making a new benchmark, let's use existing exams as benchmarks." Some researchers simply said: MMLU is a good benchmark right, if it has saturated, what if we improve it or its problems? And from this thought process came MMLU Pro.

Basically, whatever problems MMLU had, MMLU Pro tried to solve them. They basically said, if a product is good, its next iteration should be created; that will also be good. That's the main thinking behind this benchmark. So MMLU Pro's tagline is simply "MMLU rebuilt to fix its flaws." So whatever problems were in MMLU, they were looked at one by one and attempts were made to solve them.

### What Changed

1. **10 options instead of 4**: In MCQs, instead of four options, 10 options are given. What effect does this have? If you're taking an exam, say IIT JEE or any other exam, and instead of four options you get 10 options for each question, would this make your exam more difficult or easier? A lot of us have given this kind of exam, and often we try to reach the right option by eliminating options. Right, when you have four options, elimination is easier: eliminate three, reach one. When you have 10, this becomes much harder. So basically, to increase complexity, researchers gave 10 options instead of four.
2. **Trivia questions removed, reasoning-based questions added**: they removed trivia-based questions and noisy questions from MMLU and replaced them with reasoning-based questions. MMLU was famous for asking basic factuality-based questions, but they removed these and replaced them with somewhat complex reasoning-based questions. This also increased difficulty a bit.
3. **Fewer, broader subject categories**: they said we won't focus on 57 subjects, because focusing on 57 subjects means some subjects get more focus and some get less, which is not good. So they selected only 14 broad categories, and put questions into these 14 categories, and put enough questions in each category so that no category is underrepresented.

These were the three major changes you'll see compared to MMLU. Proof that these changes helped: reasoning-capable models were seen to be 20 points ahead of non-reasoning models, which actually shows that this dataset now requires thinking. Earlier, even without thinking, you could get good numbers just from factuality recall, but now in this exam, in this benchmark, you have to use your brain too. So this benchmark favored reasoning models more in that sense.

### History and Lineage

Very simple: MMLU came in 2020, and it saturated. In 2024, two papers came: one called MMLU-Redux, and one called MMLU Pro. MMLU-Redux is actually not a benchmark, it's a paper that pointed out there are many kinds of problems in MMLU, and the biggest problem is that around 6-8% of questions are incorrect, incorrect in the sense either the correct answer isn't given at all, or the given "correct" answer isn't actually correct. So these researchers found this out. This is how it was discovered that no one can score 100% on MMLU. People were thinking that we're reaching up to 92 but nobody is able to go above it. So the reason for that was actually found when the MMLU-Redux paper came out. After this, it was understood that this benchmark has saturated, and something new needs to be done. That's when the MMLU Pro paper came, where they made all the changes mentioned above.

### Current Status

It came in 2024, and now 2026 is going on, and this too is now nearing saturation, meaning models are now scoring around 80-90 on it.

### Task and Dataset Details

Here there are 12,000 questions (MMLU had 14,000 questions), 14 disciplines instead of 57. All these disciplines are mentioned. Here is a typical question: "A 2 kg block slides down a frictionless incline of 30 degrees from rest. What is its speed after sliding 4 meters along the incline? Consider the value of g as [given]." Options: A, B, C ... up to J, because there are 10 options here.

This question isn't just a direct factuality recall question. Here you need facts, i.e. knowledge, but at the same time you have to reason. This is the kind of question that was added, as mentioned earlier. The task is again simple: answer in a quiz format. Core metric is again accuracy, just like other benchmarks.

### Run Configuration

Again, five-shot CoT, temperature zero, pass@1, no use of tools.

### What MMLU Pro Does NOT Measure

- **Open-ended generation**: like other benchmarks, this too doesn't measure open-ended generation. Here you're given options from A to J, one of which you select, but you're not generating from scratch, so generation capabilities are not being checked.
- **Reasoning trace correctness**: here too we're not measuring correctness of reasoning traces. We're only measuring the final answer.
- **Calibration**: here too calibration is not checked. Calibration simply means: does the model know it doesn't know the answer? It's written here: "no test of whether a model knows what it doesn't know." So if a model doesn't know that it doesn't know the answer, it will hallucinate and give some answer. But models that know they don't know a thing will clearly say "I'm not sure about the answer," rather than hallucinating. So this is not checked here.

### Known Issues and Criticisms

- **No human baseline**: in all the papers discussed so far, a human baseline was mentioned. In this paper, no human baseline is mentioned. So there's no comparison threshold. Where do humans operate, where do models go, nothing like that is there.
- **Approaching saturation**: because frontier models have now moved ahead, and there's a contamination issue here too, so it's very close to saturation.
- **Unfair advantage for reasoning models**: MMLU ideally could be applied to any kind of model. But here, reasoning models have an unfair advantage, because questions were explicitly put in where reasoning would help.
- **Source contamination risk**: a lot of questions have been taken from publicly available STEM problems, so there's a good chance of contamination. Think about it yourself, this question feels like it's picked from H.C. Verma or a similar physics book. So this kind of question, or similar questions, are widely publicly available. And that's one of the reasons this benchmark, despite coming in 2024, is about to saturate within two years.

So nothing new here, an attempt to improve on something old that was good. This attempt lasted about two years, but going forward this too will saturate.

## 6. SimpleQA

The next benchmark is interesting. It's interesting in the sense that so far the benchmarks discussed have been different from this one in two aspects, which will be discussed. Before that, the story of this benchmark.

As you might recall, it's discussed that everything started with MMLU. From there, one branch was: give exams like humans do; that was AGIEval. Then who went for reliability questions? That was TruthfulQA. Then, on the depth path, GPQA. And who went to fix MMLU? MMLU Pro. That's the map so far.

Now where does SimpleQA fit in? When TruthfulQA saturated, this reliability question was still in the picture: it's fine to check a model's knowledge and its answers, but how correct, how truthful, are those answers, that matters too. So to replace TruthfulQA, SimpleQA came, and SimpleQA's best quality is that it's very simple, just like its name, that's its job too, but despite that, it's a very difficult benchmark to crack for LLMs, and that is one of the reasons it's still active.

This is probably the first benchmark discussed so far that is being said to be still active. Meaning it's not saturated, it's not near saturation, it is active.

### What This Benchmark Does

This benchmark gives you a dataset of more than 4000 short fact-seeking questions. Simple questions like: "who won the Nobel Prize in this field in a particular year." This kind of question. The interesting thing is that in this dataset, you're not given options. Basically, this is not an MCQ dataset. This is a short-answer writing kind of benchmark. You have to write the answer and tell it. So this automatically made the questions more difficult.

Think about it yourself: which exams are more difficult, subjective exams or MCQ-based exams? What do you personally think? A lot of people would agree that subjective exams are more difficult. So that's why LLMs also feel the same thing: when they're given a subjective exam, it becomes difficult for them to answer too, and this is one of the major strengths of SimpleQA.

Second, this dataset, this benchmark, doesn't just measure accuracy, it also measures calibration. Calibration, explained earlier, means does the model know it doesn't know the answer. This is also found out in this dataset, in this benchmark, because we measure three things here: looking at the answer, we measure whether it's correct, or incorrect, or whether the model said "pass," "I don't want to answer." We measure this thing too, and because of measuring this thing, we can find out whether a model knows it doesn't know the answer.

### Dataset Details

4326 questions, short fact-seeking questions, and how were these questions made? This is a set of questions where GPT-4 failed to give an answer. So these 4000-odd questions are questions that the state of the art model of that time could not answer, which is why they are considered difficult questions.

It was launched in 2024 by OpenAI, and its best quality, as discussed, is that here you don't get options, so you have to write, generate, the answer. And this is the reason that the same model that scored 88% on MMLU only scored 40% on SimpleQA.

### Current Status

Its status is active, and there's no chance any time soon that it will saturate.

### Design Insight

Inside this one benchmark, there are two benchmarks, so to speak. One obviously tells whether the answer is correct or wrong, but there is a third category: **not attempted**, which tells us how humble the model is, whether it is ignorant or not. This we get to know. When a model says "I don't know," we understand it's not hallucinating, it is confident about its abilities.

So this paper's philosophy is: "get as many questions correct as possible while not attempting the ones you're not confident about." This is what this benchmark tells us. So factuality plus calibration, these are the two things it's testing.

### History and Lineage

Launched in 2024, GPT-4o, the state of the art model of that time, scored 38%. o1-preview scored 42%. By February 2025, even GPT-4.5 only reached 62.5%. So we can say this benchmark will remain active for maybe one or two more years.

### Dataset, Sample Question, and Task

A sample question: "Who received the IEEE Frank Rosenblatt Award in 2010?" A hallucinated answer would be this, an incorrect answer basically, and a third answer the model could give would be "I'm not certain who won that year." All three are possibilities.

The task is very simple: you have to answer the question. Here, an LLM judge sits and judges that answer, and puts it into one of the three categories: correct, incorrect, or not attempted.

### Scoring

There are three metrics here:
1. **Correct**: out of all questions, how many answers were correct.
2. **Correct given attempted**: accuracy among only attempted questions. So say there are 4300 questions, the model only attempted 3500. The rest it said "I don't know." Out of these 3500, how many did you get correct?
3. **F-score**: basically the harmonic mean of the first two metrics. This tells us about both things: how good its factuality is, and how good its calibration is.

This is the main difference between this particular benchmark and all the other benchmarks discussed before, that here calibration is also being checked.

### Run Configuration

Again, nothing different from before.

### What SimpleQA Does NOT Measure

- **Long-form factuality**: although it does measure factuality, that's short-form factuality. "Who won this award that year" is a two-word answer. This is what we're checking, but we're not checking long-form factuality, how correct the model will remain in a long answer. We cannot tell this with the help of this benchmark.
- **Everyday factual reliability**: secondly, we're checking how much a model is not hallucinating, how well calibrated it is. But we can't guarantee that when we use the help of that model, and build a RAG chatbot for example and give it some documents, whether it will hallucinate there or not; that is not tested here.

As mentioned, this dataset was made by how? By when? Every question is such a question on which GPT-4 failed. Similar questions were used to build this dataset. So these are kind of rare questions. These are not the normal everyday questions. So we've created a dataset that is made of very extraordinary, different kinds of questions. So based on the performance on that, we cannot tell how everyday recall or factuality will be. So that number is a bit shady because of this benchmark.

### Known Issues and Criticisms

- **LLM-as-judge drift**: since an LLM grader, basically an LLM-as-judge, is used here to evaluate the answer, obviously over the years, this LLM-as-judge will also kind of improve. New models will keep coming, so the LLM judge we use today cannot be compared to the LLM judge's performance from 2 years ago, because obviously models are improving on a daily basis. So because of this, we cannot compare today's result on this benchmark with a result from 2 years ago. This is the main flaw.
- **Answer staleness**: this simply means, say a question in your dataset is "who is the world's rank one rugby player." Say this dataset was made in 2024. So in 2024, let's say ABC was the player's name. But in 2026, ABC might be replaced and XYZ becomes the rank one player. This can happen, right? So the problem of answer staleness is that a lot of the answers are no longer what they were 2 years ago when this benchmark came out.
- **Adversarial selection bias against GPT-4**: this whole dataset, this benchmark, was made from questions on which GPT-4 had failed. So there's an adversarial bias against GPT-4 models. So this could be an advantage or disadvantage for other models. Basically it's not a fair treatment to all models. So that's one of the criticisms against this benchmark.

But despite this, SimpleQA is a very respectable benchmark, and if someone is able to score well on this benchmark, they are considered very good. So even though it's called "simple," it's a great benchmark to have. It helps a lot in catching hallucinations etc.

### Student Question: Isn't SimpleQA Just Testing Recall Rather Than Reasoning/Understanding?

**Question**: If the question is fact-based, like a Nobel Prize winner in a specific year, and since they are trained on such huge data, this info will anyway be in their training data, it will just be recalling capability to understand the model rather than understanding and reasoning some sort of pattern. Are we discovering its recalling capability or understanding capability, like in GPQA we have questions where...

**Answer**: There's one thing to keep in mind here: when we say we put the entire internet's data into training a model, it does not guarantee that it will also absorb all that internet data. There are many stages, a lot of cleaning of data happens. There's a good chance that a particular fact or piece of knowledge doesn't even reach the model's weights, basically the model may not be able to absorb it. And as for this benchmark, its core philosophy is that it's checking the truthfulness of a model, whether it knows or not that it doesn't know the answer. This is the main ask of this benchmark. It's not checking factuality or knowledge per se. Knowledge-based questions are indeed being asked, but they're being asked so that we can judge whether the model has an idea about its own knowledge or not. This is the main idea of this benchmark.

## 7. HLE (Humanities' Last Exam)

HLE is a very dramatic name. Humanities' Last Exam. Hearing it already feels heavy. The thought process behind it: HLE basically absorbed the ideas of previous benchmarks. It took breadth from MMLU, it took depth from GPQA, and basically combined them to create a depth-cross-breadth benchmark, containing 2500 questions, all of them expert-written questions across 100+ subjects, from classics to rocket engineering, and each filtered to stump frontier models, meaning questions where frontier models could not answer. That's the main idea behind HLE.

### Why the Name

The answer given here is that the name is a thesis, not marketing. If models saturate a broad, expert-level, unambiguous answer exam this hard, then closed-ended question answering has nothing left to measure, and evaluation must move to open-ended, agentic tasks. The basic idea is: the researchers who published this benchmark said that if such a difficult benchmark, which handles both depth and breadth, is cracked by some model, then there's nothing left to check further. After this, we should move forward and focus on evaluating how well models handle agentic tasks and open-ended tasks. And that's why they kept the name Humanities' Last Exam.

### Current Status

Active. In fact, until a few days back, whatever models were tested on this benchmark, they were all operating in single digits, and after Gemini 3 Pro came, it finally reached 38%.

### How the Dataset Was Built

HLE takes the same expert-authored, failure-filtered recipe like GPQA, like how GPQA was built to bring depth, and takes it at scale. Here, 1000 experts, from 500 institutions, from 50 countries, together made these 2500 questions, spreading across 100+ subjects. This is a massive effort. Generally benchmarks come from a small research group. This is like a proper world-wide effort on this one project, and then this project was built. That's the level of work this is.

So GPQA was deep only within physics, chemistry, biology. HLE is deep across the whole map of human expertise. In as many fields as humans have knowledge, this is an accumulation of the deepest questions of all those fields, and that's why it was given this name.

### Private Test Set

One more thing was done here: the research institute that made this benchmark has held a private test set for itself. So there's a public set, which is the 2500 questions, and a private set, which is not available on the internet. Only this institute has it, and they've kept it for themselves, so that they can always test a new model on that test set and give results. This was done to stop contamination.

### Calibration Testing

Also, here's another new thing: this benchmark doesn't just test accuracy. It also tests calibration. So whenever you send a question to the model, you also tell it to state how confident it was in answering this question. So the model itself says "I am 80% confident," "I am 75% confident." So not only is accuracy being measured here, but also the confidence score is used to tell how much the model knows about itself, or how truthful it is.

### History and Lineage

It came in January 2025. In 2025, Grok 4 reached 24%. GPT-5 reached 25%. Gemini reached 38%. And in 2026, it is still active. In fact, it is still the top benchmark for testing knowledge, reasoning, and also maths, in fact maths is a domain in this too. So actually, if you ask anyone today what the state of the art benchmark is for testing these capabilities, without a doubt one can say HLE is that benchmark, Humanities' Last Exam.

### Dataset Details, Task Format

The main USP is breadth times depth. In the world, either people have breadth of knowledge, or depth of knowledge. There's probably no person in the world who has both breadth and depth. Meaning there's no PhD who has a PhD in 100 subjects. You can only do a PhD in one subject, right, because depth takes time. So the same problem was thrown at models too: you might have breadth, you might have depth in a few subjects, but we're asking you whether you have depth in 100 subjects or not.

Two formats are used here too: 80% of questions are short-answer questions, where you have to type/generate the answer, and 20% of questions are MCQ-based. So it's a mixture, but mostly there are typing/generating questions.

Also, 10% of all questions are multimodal, which basically means these questions show a photo. In fact, if you go to HLE's homepage and look at the leaderboard, you'll notice some questions have images like this, and a question is asked based on that image. So this is a new thing too. In all the benchmarks discussed so far, there was only textual data. Here, 10% of questions have vision-based data too. So a lot of models that don't have vision capabilities will basically only be scoring on 90% of the dataset. So this needs to be watched when looking at the results.

Tools cannot be used here. The core metric is accuracy, but calibration is also focused on. It's written here that there's some internal mechanism where they calculate the root mean square between the model's confidence and the model's correctness. This is quite technical; more can be understood by going to their paper.

### Run Configuration

Similar to before.

### What HLE Does NOT Measure

- **Open-ended and agentic problem solving**: obviously, because this is closed-ended.
- **Everyday usefulness**: not measured, because as discussed, these are very expert-level questions, normal questions are not here.
- **Vision and multilingual capabilities**: vision is tested a bit because 10% of the data has it, but multilingual capabilities are not tested, because this entire dataset is English only.

### Known Issues

- **Disputed answers**: some questions have disputes about whether the answer is correct or not. Initially this was a dataset of 3000 questions; because of those disputes, only 2500 questions remain now; 500 were removed.
- **Grading errors**: an LLM-as-judge is used here too, to grade the short-form answers. So again, the same issue: whenever you use LLM-as-judge, it's not reliable, its result can vary.
- **Failure-filter selection bias magnified**: as mentioned, this dataset is also built from questions on which 2024 frontier models were failing to answer. So there's kind of a selection bias in this dataset, and it does not represent the general knowledge people ask about on a day to day basis. So in that sense there's a bias in the dataset.

### Summary

This is like the most powerful test that can be given to an LLM in order to test its knowledge, reasoning, and mathematical capabilities, and that is the reason why today, if someone asks what the state of the art benchmark is for testing these capabilities, without a doubt one can say HLE is that benchmark, Humanities' Last Exam.

## Closing the Discussion

With this, the discussion concludes. The entire Knowledge capability, all its important benchmarks, have been covered in a lot of detail. It may have felt a bit boring because there's a lot of theory. But again, if understood like a story, quite a lot was absorbed in the last one and a half hours combined with the last session.

### The BenchWiki Website

A website has been built, and this is being shared. This is the URL. Here, the entire teaching journey is being documented. So far, **23 benchmarks** have been covered on this website. Out of these, seven are the ones taught in this session. Besides these, reasoning and maths related ones have also been added here. They have also been categorized: which are active, which are nearing saturation, which are saturated, which are deprecated. And from here too you can filter things out, and quite a lot of detail is given.

This was probably shown in the last class too, but now it has been deployed, and new benchmarks have also been added. In the next two weeks, an additional 20-25 benchmarks that will be taught will also be put here. So if you don't want to spend your time watching long lectures about these benchmarks, what you can do is simply go to this website and read about whichever benchmark you would like to learn about.