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

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
