# IaC Assignment 1

**Student:** Ruairí Ó hÓgartaigh  
**Student ID:** L00205551  

---
The outputs of this markdown became a bit of a mess as I would circle back to task 1 while working on task 2. The work entries for both have been parsed into the following markdown files in this folder. Entries are dated and log the work and though process on the given day. 
* [Task1](./task1WorkLogs.md)
* [Task2](./task2WorkLogs.md)

---

## Task 1

Task 1 was a straight forward task in this assigment, as will be apparent reading the logs. An AWS example privided a large portion of this assingment's requirements [AWS sample yaml](./Scripts/Task1/AWS_firstStack.yaml). S3 bucket integration provided some difficulty but was useful to know  when working on task 2.
---
## Task 2

Task 2 was a bit more complicated, I dreamt a bit too big at the start and it stalled initial progression. By parsing the tasks into more manageable pieces, like first manually generating a VPC to properly understand elemental relationships, the stack pieces began to fall into place. I now have a much better understanding of cloudformations and the benefits of stacks but also how to debug issues with EC2s via the SSM terminal . 

In the process of  developing the final script I made several scripts for different elements. Reading through the logs you will find that during the development process I came to favour a multi-stack approach to development. I favour stand alone stack instances for more constant elements of the development such as the VPC and RDS. During development sessions I would use an existing VPC, spin-up and RDS and then commence work on the app and web ec2 instances. In hindsight I am glad this approach was taken, when the final stack containing all elements was spun-up, it took significantly longer to deploy. This large and  cumbersome stack would have slowed development significantly had all tiers been developed in the one stack. 

My preferred multi-stack solution is [here](./Scripts/Task2/realWorldOpsSolution/).
For the "One stack solution", the stack can be found here [here](./Scripts/Task2/OneFileSolution/), (I got an LLM to merge the stacks in the previous folder).

---

