# Pedagogy rules

The engine optimizes for **accurate performance that transfers**, not watch time, visual novelty, or
the number of facts mentioned. These rules translate established instructional guidance into an
authoring contract. They are defaults, not claims that one recipe fits every learner or subject.

## 1. Start with performance and context

Before selecting content or media, state:

- who the learner is and what prerequisite knowledge can be assumed;
- where and why the learning will be used;
- an observable terminal performance;
- the conditions under which it must be performed;
- measurable success criteria and the cost of common errors.

Break complex performance into component skills and sequence prerequisites before dependents.
Carnegie Mellon’s Eberly Center recommends alignment among objectives, assessments, and
instructional strategies; it also recommends student-centered, measurable objectives using action
verbs rather than vague verbs such as “understand.”

## 2. Design backward from acceptable evidence

For every objective:

1. Define what learner work would demonstrate success.
2. Choose practice that elicits the same cognitive process.
3. Choose feedback that helps the learner correct that work.
4. Only then choose explanation, example, and media.

Match evidence to the objective. Recognition questions do not establish that a learner can diagnose,
decide, perform, justify, or create. Use scenarios, classification, prediction, ordering, error
detection, completion problems, explanations, products, or demonstrations when those are the target.

## 3. Build a model-to-independence path

For unfamiliar or complex skills:

1. Explain the goal and relevant cues.
2. Model a worked example, including expert self-questioning and decisions.
3. Ask the learner to complete a partially worked example or guided case.
4. Fade support toward independent performance.
5. Give a different surface context for transfer.

The IES practice guide recommends interleaving worked example solutions with problem-solving
exercises. Renkl et al. (2002) found that a smooth transition from example study to problem solving
using faded completion problems supported learning better than abrupt independent problem solving in
the studied context.

For simple recall, do not manufacture a long worked example. Use the least support that enables
successful effort.

## 4. Practice retrieval and space important learning

Retrieval means attempting to recall or use information before seeing the answer. It is not replaying
the same explanation. Require commitment, then reveal the answer with an explanation.

- Retrieve prerequisite knowledge when it becomes relevant.
- Revisit important objectives after a delay, not only in adjacent scenes.
- Mix earlier objectives into later episodes and follow-up activities.
- Vary surface details while preserving the underlying principle.
- Use pre-questions only when they orient attention rather than unfairly assess untaught material.

The IES guide recommends spacing learning over time and using quizzing for retrieval and spaced
exposure. Dunlosky et al. (2013) rated practice testing and distributed practice as broadly useful
techniques based on the literature they reviewed.

## 5. Teach discrimination and transfer deliberately

When learners must decide **which** rule, category, or procedure applies:

- contrast examples and non-examples;
- highlight the defining feature rather than superficial resemblance;
- interleave types that learners must discriminate;
- ask the learner to justify the choice using a cue or criterion.

For objectives at `apply` or above, include a transfer task whose surface context differs from the
modeled example. Do not call a cosmetically changed number or name “novel.” Butler et al. (2017)
reported that retrieving and applying knowledge to different examples improved transfer to new
examples in their experiments.

## 6. Give explanatory feedback

Feedback follows learner commitment and does more than mark right/wrong. Depending on the task, it
states:

- the correct answer, action, or quality criterion;
- why it works;
- why the likely alternative fails;
- which cue or process to use next time;
- how the reasoning changes under an important boundary condition.

Use corrective feedback for factual errors, process feedback for procedures, elaborative feedback for
reasoning, and comparative feedback for discrimination. The IES guide also recommends deep
explanatory questions such as “What caused this?”, “How did this occur?”, “What if?”, and “How does
this compare?”

## 7. Manage video cognitive load

- **Signal:** point to the exact element currently being explained.
- **Segment:** make one conceptual move per beat and pause at natural boundaries.
- **Weed:** remove decoration, sounds, anecdotes, labels, and motion that do not serve the objective.
- **Match modality:** combine narration with complementary graphics rather than dense duplicate text.
- **Embed active learning:** questions, predictions, pause-and-do work, and guiding prompts.

Brame (2016) synthesizes these principles for educational video and emphasizes cognitive load,
engagement, and active learning. Shorter is useful only when it follows from tight segmentation; do
not omit needed modeling, practice, or feedback to hit an arbitrary duration.

## 8. Use story only when it performs instructional work

Direct narrator-only instruction is the default. A case, scenario, character, metaphor, or plot may
be used for:

- an authentic decision context;
- a persistent example whose state changes;
- perspective comparison;
- consequence visibility;
- retrieval cues that map cleanly to the real task.

“Fun,” “engaging,” “cinematic,” and “memorable” are not sufficient rationales by themselves. Remove
narrative beats that do not explain, model, cue, practice, provide feedback, retrieve, or transfer an
objective. Always translate a metaphor back to the real concept.

## 9. Coverage is explicit

Every truth-layer fact is `required` or `excluded` with a reason. Required facts map to objectives and
then to beats. This prevents both accidental omission and fact-dump scripts. A fact can be available
in reference material without becoming spoken content if it is not needed for the terminal
performance.

## 10. What the gate can and cannot establish

`lint_instruction.py` checks traceability, alignment dependencies, minimum practice/feedback,
representation implementation, transfer, provenance, and obvious passive/redundant patterns. It
cannot prove that the explanation is correct, the examples are psychologically optimal, or learners
will retain and transfer the skill. Pair it with source/SME review, adversarial script review, and
learner performance evidence when available.

## Sources

- Institute of Education Sciences, U.S. Department of Education. *Organizing Instruction and Study
  to Improve Student Learning* (2007):
  https://ies.ed.gov/ncee/wwc/PracticeGuide/20072004
- Carnegie Mellon University, Eberly Center. “Articulate Your Learning Objectives”:
  https://www.cmu.edu/teaching/designteach/design/learningobjectives.html
- Brame, C. J. (2016). “Effective Educational Videos: Principles and Guidelines for Maximizing
  Student Learning.” *CBE—Life Sciences Education*, 15(4), es6:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC5132380/
- Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., & Willingham, D. T. (2013).
  “Improving Students’ Learning With Effective Learning Techniques.”
  https://doi.org/10.1177/1529100612453266
- Renkl, A., Atkinson, R. K., Maier, U. H., & Staley, R. (2002). “From Example Study to Problem
  Solving: Smooth Transitions Help Learning.” https://doi.org/10.1080/00220970209599510
- Butler, A. C., Black-Maier, A. C., Raley, N. D., & Marsh, E. J. (2017). “Retrieving and Applying
  Knowledge to Different Examples Promotes Transfer of Learning.”
  https://doi.org/10.1037/xap0000142
