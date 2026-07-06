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
Yes, some things from my design changed during implementation. 
- If yes, describe at least one change and why you made it.
One thing that changed during implementation was my scheduling. I had not added a sorting for my scheduling so they weren't organize. Additional some attributes that I thought were part of one class were swithced to others, such as time being moved to another class. 
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
Some consider that my scheduler consider is time, priority and preferences. 
- How did you decide which constraints mattered most?
While running the test, and with the help of AI, we were able to have all constraints fixed at once. An example being a warning for where time and priority were the same, which showed the user that these two clash with one another and needs to be fixed. 
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
One tradeoff I noticed my scheduler make was having less attributes and placing those attributes to other classes.
- Why is that tradeoff reasonable for this scenario?
This tradeoff was good because this allowed scheduler to not have the same attributes of other classes, allowing for better flow and communication between classes. 
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
Some things that I used the AI tool for during this project was refactoring, debugging, and explaning code which I didn't understand. Additionally, I created many different test with the AI tool which allow for easier debugging. 
- What kinds of prompts or questions were most helpful?
Some questions that were helpful for me were asking the AI tool too explain what they wanted to add or remove. Additionally, some prompts that helped were one shot promting where I gave an example of what I wanted something to look like and they created something that I liked.
**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
One moment where I didn't accept an AI suggestion was where they wanted to touch another file to created a bug test, however I didn't allow it and asked the tool to work on another file. 
- How did you evaluate or verify what the AI suggested?
I was able to evaluate this AI suggested by asking the AI what was the purpose of touching another file, where they gave me a response, that felt like they were doing extra steps that could mess other part of the code up. 
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
Some behaviors that I tested was the sorting schedule method.
- Why were these tests important?
This was an important test because if users entered scheduled task at the same time and same priority, it could lead to an error. 
**b. Confidence**

- How confident are you that your scheduler works correctly?
I think out of 5 stars I would say 4 stars
- What edge cases would you test next if you had more time?
Some edge cases I would do is having more than one pet have the same priority.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The part I was happy with in this project was the pawpal_system. I felt that the AI tool helped me find lots of issues that could've lead to big errors when it came to using the app 
**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I think I would like to add my own type of classes. I felt like lots of the classes and methods were selected for us which limited what we could have done with the AI tool. 
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I learned that desiging a system takes a lot of work especially since some attributes or methods can look like they fit in one class but don't and make it harder for users to use the app. 
