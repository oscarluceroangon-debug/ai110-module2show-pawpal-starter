# PawPal+ Project Reflection

## 1. System Design
#Read from here
 Some required core actions that this app should have is adding a pet, scheduling a walk, seeing what today's tasks.
 There should be four classes Owner, Pet, Task, Scheduler. Each class would hold different information. Owner: Owners's name, their pet/s, their address, and their age. Pets: Type of animal,Name, breed, pet's age, task and .Task: description, date, due time, and completion status. Scheduler: time, priority,perference. 

 Some methods for Owner would be displaying their pets, and also displaying their info: address,name,age. Some methodes for Pet would be adding pet, removing pet and displaying their name,age,breed, and type of animal. Some methods for Task would be seeing the description, and date for the task. Additional, another method would be showing if a task is complete. Some method for scheduler would be making or cancling a scheduler
 #Stop here
**a. Initial design**

- Briefly describe your initial UML design.
The UML initial design had it so the owner could add pets, pet's info, and their info.Additionally, tbey also had a scheduler amd task maker that showed them the task they have to do or if they wanted to create a new task.
- What classes did you include, and what responsibilities did you assign to each?
I created four classes: Owner, Pet, Task, Scheduler. Owner had the responsibilitiy of having the pets, and their info. Pet had the responsibilitiy of showing their info: age,name,breed, type of animal, and owner. Task has the responsibilitiy of showing which task need to be compeleted, the date of task, and the description. Scheduler had the task of selecting the time, priority and perference.
**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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
