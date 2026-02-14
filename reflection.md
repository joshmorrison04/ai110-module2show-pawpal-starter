# PawPal+ Project Reflection

## 1. System Design

**3 Core Actions**
- Add a pet to owner profile with basic pet and user info
- Generate a daily plan and display
- Track daily task progress (what has been completed and what’s in progress)

**a. Initial design**

My initial UML design was a small, class-based model with clear ownership and scheduling responsibilities: an owner contains pets, pets contain tasks, and a scheduler generates a daily plan from availability and task data.

Classes and responsibilities:
- `Owner`: Represents a pet owner, stores their name and list of owned pets, and provides the ability to add pets to the profile.
- `Pet`: Represents a pet, storing the pet’s name and its list of current tasks.
- `Scheduler`: Represents the scheduling component that holds availability data and generates a daily care plan.
- `Task`: Represents a care task with metadata (name, description, duration, priority, status) and supports updating status, duration, and priority.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. I added explicit relationships and helpers to reduce ambiguity and improve performance: `Pet` now keeps a reference to its `Owner`, tasks are stored in a dictionary keyed by name for faster lookup, and `Scheduler` now accepts the list of pets it schedules. I also standardized task statuses and added basic validation for duration/priority to prevent inconsistent state.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My scheduler prioritizes task priority over perfect time optimality. When time is limited, it schedules higher-priority tasks first and may leave lower-priority tasks unscheduled rather than trying to perfectly pack every minute.

That tradeoff is reasonable because the app’s goal is to ensure essential care (feeding, medication, walks) happens reliably. A simpler “priority-first” strategy is easier to explain to users and avoids risky over-optimization that could push critical tasks out of the plan.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI for design brainstorming and quick sanity checks on class responsibilities, then for refactoring suggestions (naming, data structures) and small debugging help when tests failed. The most helpful prompts were specific and scoped, like “suggest a data structure for fast task lookup by name” and “review this class for single-responsibility issues.”

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

An AI suggestion was to auto-sort tasks by duration to “maximize total tasks.” I didn’t accept it because it could delay critical tasks. I compared the suggestion to the project goal (reliable care first) and verified by running the tests and checking sample schedules to ensure high-priority tasks remained first.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested adding pets to an owner, creating tasks, updating task status, and generating a daily plan that respects priority and available time. These tests were important because they cover the core user flows and verify that scheduling logic doesn’t break basic data integrity.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I’m reasonably confident for typical scenarios with a few pets and tasks, especially for priority handling. Next, I would test edge cases like zero availability, tasks longer than any time slot, equal priorities with tie-breaking, and large numbers of tasks to ensure consistent ordering and performance.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I’m most satisfied with the clean separation between owner/pet/task data and the scheduler logic, which made it easier to reason about and test.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would add a more flexible scheduling model (time windows and recurring tasks) and improve the UI to make priorities and plan changes more transparent.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Clear constraints and explicit priorities prevent over-complication; AI is most useful when you ask focused questions and then verify suggestions against your actual requirements and tests.

---

## 6. Additional AI Collaboration Reflections

- Which Copilot features were most effective for building your scheduler?

Copilot Chat was most effective for brainstorming scheduling approaches and validating design choices, while inline suggestions were helpful for small refactors (naming, list/dict operations) and boilerplate class methods.

- Give one example of an AI suggestion you rejected or modified to keep your system design clean.

I rejected a suggestion to merge `Owner` and `Pet` data into a single “profile” class because it blurred responsibilities. Keeping them separate preserved a clean domain model and made scheduling logic easier to test.

- How did using separate chat sessions for different phases help you stay organized?

Using separate chats for design, implementation, and testing kept context focused and reduced conflicting advice. It also made it easier to track decisions and avoid re-litigating earlier design choices.

- Summarize what you learned about being the “lead architect” when collaborating with powerful AI tools.

I learned that the lead architect role is about setting constraints, defining priorities, and approving changes based on requirements—not accepting suggestions by default. AI accelerates exploration, but the human must own the system’s goals, tradeoffs, and final design.
