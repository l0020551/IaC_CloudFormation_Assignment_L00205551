


## Task 2: Three tier system

**Date:** October 17th, 2026  

### Introduction
For the three-tier system, a basic weather application will be implemented.
* In the application layer an EC2 instance will run a bash script calling curl commands to get the weather and forecast for the ATU Donegal campus.
* In the web layer the current weather and forecast will be displayed and update on a minute-by-minute basis
* Every hour a curl command will update values to the database.

### Met Eirinn API
The API used is provided by Met Éireann and can be accessed [here](https://data.gov.ie/dataset/met-eireann-forecast-api). 
As it is not a key component of this assignment, an LLM was used to generate a bash script that gets the weather forecast.
A cronjob call in `UserData` will be used to update the weather readings at fixed intervals with the readings overwriting the previous readings. 

### What can be re-used from task 1
* From task 1 the EC2 instance architecture can be reused. 
* The S3 should remain to hold bash scripts used to execute the curl commands. It may also be useful if the web tier were to implement icons to represent current weather states. 


### What is new
* An EFS (Elastic File system) may be overkill for this application. 
* A VPC may make sense and the database and application tier would ideally be on a private layer with the web tier on the public layer. 
* A database will need to be generated. 


### VPC
AmazonQ was asked:

`I am building a 3 tier application in CloudFromation, how can I implement a VPC?`

It gave a clear answer: [amazoonQ  on VPCs](./screenshots/VPC_question_to_amazonQ.png)



On further prompting amazonQ, it gave me an example of implementing a VPC on a stack. The example of this can be found [here](./Scripts/Task2/SampleScripts/VPC.yaml) [AmazonQ_VPC_prompt2](./screenshots/AmazonQ_prompt2.png)

On reviewing this script it has some useful content including VPC and database implementation. The script deviated on some points including using cloudfront for the web tier which is not necessary for this application.

After probing the LLM further, a script close enough to the desired structure was generated. While it doesn't match, it contains the main building blocks that the final script should incorporate to run. This script can be found [here](./Scripts/Task2/SampleScripts/VPC2.yaml). Comments have been added for how these segments may fit together in the final script. 

--- 


### Task2 
Last week, a script with a VPC template was generated. Now it will be implemented. As  mentioned in the previous section, application scripts will be recalled from an existing s3 bucket. 

After spending hours debugging, the task has been broken down into two stages, 
 * Stage 1: GUI and application running.
 * Stage 2: database integration. 


**Date:** October 25th, 2026,  Recap:

* Updated task1 script to recall from existing s3 bucket.
* Added parameters for s3 buckets in both scripts 
* Reviewed instances and checked that they are still supported after notification from AWS.
* Added more content for task2, html and python scripts etc. 
* Accessed ec2 terminal for debugging issues

### Next stage
 * Get python script running in EC2
 * Push updates to webpage
 * Push changes to database. 
 ---

 **Date:** October 26th, 2026

 After pushing changes yesterday, the task2 app was run locally, an SQL container, a python flask API webpage and a script to get and push data from Met Eireann to a database. Having it run locally with success, the next stage is to migrate it to the stack.
 
 Today's plan:
 * Load html of task 2 using task 1 as a reference
 * Integrate database
 * Add ec2 to poll Met Eireann and push to database.

 After multiple failed attempts, a more finite approach has been decided. A new folder called [stand-alone Tiers](./Scripts/Task2/StandaloneTiers/) has been created. Each tier will be worked on until all  three are configured and operating as desired. Once all three independent scripts are running, then they will be integrated into a singular stack. 

 First, a VPC was manually created for the application using the following steps from amazonQ 
[pic1](./screenshots/Screenshot%20From%202026-10-26%2016-10-54.png)
[pic2](./screenshots/Screenshot%20From%202026-10-26%2016-11-11.png)
[pic3](./screenshots/Screenshot%20From%202026-10-26%2016-11-24.png)

On generating the VPC, the manual scripts were run in the following order:
1. Database (the application layer and web layer are dependent on this)
2. Application layer (populate  the database with data)
3. Web Layer.

* The database stand-alone script runs.
* After some debugging in the EC2 terminal, the App stand-alone runs. The database needed to be decoupled, and the met readings stored locally on the EC2 instance as an xml. [terminal debug](./screenshots/ec2_debug.png)

### Next Steps

* App and RDS standalones working in sync.
* Web standalone working
* All three working in sync
* Script merge. 


--- 

**Date:** October 27th, 2026 

* App ec2 stand-alone has been debugged.
* Next step is RDS communication integration
For this AmazonQ was questioned: [aws ec2 to RDS comms](./screenshots/ec2_rds_connection.png)

At this stage, after manually provisioning a VPC and debugging communication between the RDS and EC2 Instance, I am starting to understand how cloudformation stacks work. 

* At this stage I have a standalone RDS stack, a standalone app and the two integrated.
I have tidied the [App2Db.yaml](./Scripts/Task2/StandaloneTiers/App2Db.yaml) script. 
The next step will be to generate the overall stack for task2. 
I think I will split this into two solutions:
1. One stack that does everything; VPC and RDS generation, etc. 
2. Multi-stack solution; For real-world Ops I would partition the Database and VPC into their own stack as they are less ephemeral than the EC2 App and Web tiers. Rather than generate a new Database and VPC for each stack call, existing instances can be called in parameters. 

### Next steps

1. test App2Db.yaml
2. Integrate stanalone webpage stack
3. generate a standalone VPC stack
4. Generate an "All in one" stack
5. Tidy and streamline final task 2 solutions.

---

**Date:** October 28th, 2026 

An hour of work on this project was done today. Nginx script outputs to webpage but requires further debugging.

### Next steps

1. test App2Db.yaml
2. debug webpage stack
3. generate a standalone VPC stack
4. Generate an "All in one" stack
5. Tidy and streamline final task 2 solutions.

---

**Date:** October 30th, 2026 

I got amazonQ to generate a stack based on the VPC manually generated. Due to circular definitions with two tiers having overlapped inbound and outbound security group rules, it took some debugging to get the final stack to validate and deploy.


---
**Date:** October 30th, 2026 

At this stage, I don't have time to debug the webapp.
The plan is to deploy the standalone tiers individually and validating function before merging them into a single file and the alternative structure I would actually use for Ops.  

Here are screenshots of the stand-alone deployments; the tiers require a VPC to interface so the VPC boots first. The database next as the app needs a database to write to, and the webpage needs to read from. [stack order](./screenshots/Screenshot%20From%202026-10-31%2010-24-57.png). A database and two EC2 instances are generated [ec2s](./screenshots/Screenshot%20From%202026-10-31%2010-25-20.png).

Next, the real-world Ops folder will be implemented. This is where the three-tier system will be broken into three scripts, VPC, RDS, and operations. In a real-world scenario of this weather app, I think the database should not be tethered to the stack containing the EC2 app and web layers. In this use case data in the database would ideally persist through updates to the app and web implementation, if in the shared stack, deletion would wipe the database, backups of the database may be an option. Creating it separately once and pointing to it when deploying updates makes the most sense. The same logic stands for the VPC too.  

VPC and database stacks were updated manually for the [realWorldOpsSolution](./Scripts/Task2/realWorldOpsSolution/) folder. The integration of the webpage apps was assisted by an LLM to remove duplicate parameters and resources (It was taking a long time to do it manually). Once the Ops folder was completed, the folder was uploaded to an LLM to merge all stack's content from VPC to Apps. Manually doing this was avoided as I understand the resources and parameters in use. Manually merging the stack content would take addiditional time I don't have.   [MergeStacks](./screenshots/Screenshot%20From%202026-10-31%2015-27-52.png). 

After running this full stack I am glad I split the stack into smaller, manageable pieces. Roll-out of this in cloud formations took significatlly longer than the one time per session spin-up of the VPC and RDS before debugging the application and web layers. 



