# IaC Assignment 1

**Student:** Ruairí Ó hÓgartaigh  
**Student ID:** L00205551  


---

## Task 1: Printing S3 Data to a Website
**Date:** October 17th, 2026  
### Step 1: CloudFormation Tutorial
To get started on the assignment, the following tutorial and script were read and followed:

* **URL to tutorial:** [AWSCloudFormation/latest/UserGuide/gettingstarted](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/gettingstarted.walkthrough.html)
* **Date Accessed:** October 17th, 2026

---

### Step 2: Building on the content of the Tutorial Script
This tutorial gave basic insights into running one's first stack on AWS CloudFormation. Upon following the tutorial, it was clear that many of this task's components already exist in this stack. 

![Aws tutorial output](./screenshots/aws_tutorial.png)

The only thing missing was an S3 container storing the webpage text. Instead of running `echo "Hello World!"`, a text document needs to be retrieved from a mounted S3 bucket and its content concatenated (`cat`) to the screen. 

After reviewing and running the stack from this AWS-provided example (which can be found under `./Scripts/Task1/AWS_firstStack.yaml`), the next step was to see how to integrate S3 buckets. The following document was used for reference: [AWS S3 Buckets in YAML](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-S3-bucket.html).

---
### Step 3: S3 integration
**Date:** October 18th, 2026 

Today, the S3 bucket will be integrated and a file's content concatanated to screen.

As I have no background in web development and the "Hello World" content of the tutorial looks basic on the webpage, I prompted an LLM to generate a HTML document that will be retrieved from the S3 buckets. Here is the prompt content:

```
I need a simple but cleanly designed HTML file. The file will just contain two lines of text in the header, the top line reading "Student: John Doe", the second line reading "Student ID: 123456789" , take liberties with remaining asthetic design

```

OpenAI and Gemini were fed this prompt and the files produced can be found in this directory: `./Scripts/Task1/LLM_generated_html_files`.
On viewing the file content in a HTML renderer the ChatGPT HTML appeared to be the one that best met the needs for the task. The appropriate changes were made and saved in the main `Scripts` directory under `S3_student_info.html`.

The next step is accessing or mounting the S3 bucket so that the EC2 instance can access the file. This [tutorial](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AmazonS3.html) on aws was followed.

The S3 bucket was added to `Resources: WebsiteContentBucket` the integration of S3 and EC2 was attempted with the tutorial, but without success. 


After several attempts including using amazonQ to help debug, another LLM was prompted to help further debug. After feeding the script into the ChatGPT LLM, it gave feedback recommending using a loop to try pull the HTML from the S3 bucket. These changes are commented in the provided yaml script.  

These two LLMs recommended adding read permissions and adding a retry mechanism for the S3 upload to the webpage. On applying these changes, the script worked as desired. 

![Print to website](./screenshots/Task1_screens_shot.png)

To further improve the script, in the next entry the script will be further refined to not use a retry mechanism, rather than generating a new S3 bucket, it will recall one with the HTML file already loaded. 


***







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

On reviewing this script it has some useful content including VPC and database implementation. The script deviated on some points including using cloudfront for the web tier which is not nescessary for this application.

After probing the LLM further, a script close enough to the desired structure was generated. While it doesn't match, it contains the main building blocks that the final script should incorporate to run. This script can be found [here](./Scripts/Task2/SampleScripts/VPC2.yaml). Comments have been added for how these segments may fit together in the final script. 

--- 

**Date:** October 25th, 2026  
### Updates
During the week Amazon gave a notification as follows:[aws_notification](./screenshots/aws_notification.png)

The Linux version used in some scripts ran the previous week are out of support. The scripts need to be checked. 
On reviewing active repository scripts the EC2instances are already running the AL2 successor; AL2023 or the latest Amazon image release `'/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2'`.

### Update to task 1
In the first working iteration, an s3 container is generated in the stack, The webpage html needs to be manually updated while the stack checks for an upload.
This is inefficient. In the next iteration it will refence an exising s3 container. This will mean the userdata will not require a loop to check if a file has been added to the s3 bucket. Instead it will recall the file from an existing bucket. This script in this commit and push does this. 

### Task2 
Last week a script with a VPC template was generated. now it will be implemented. As  mentioned in the previous section, application scripts will be recalled from an existing s3 bucket. 

After spending hours debugging, the task has been broken down into to stages, 
 * Stage 1: GUI and appliation unning.
 * Stage 2: database integration. 


**Date:** October 25th, 2026  Recap:

* Updated task1 script to recall from existing s3 bucket.
* Added parameters for s3 buckets in both scripts 
* Reviewed instances and checked that they are still supported after notification from AWS.
* Added more content for task2, html and python scripts etc. 
* accessed ec2 terminal for debugging issues

### Next stage
 * Get python script running in EC2
 * push updates to webpage
 * push changes to database. 
 ---

 **Date:** October 26th, 2026

 After pushing changes yesterday, the task2 app was run locally, an SQL container, a python flask API webpage and a script to get and push data from met eireann to a database. Having it run locally with success, the next stage is to migrate it to the stack.
 
 Today's plan:
 * load html of task 2 using task 1 as a reference
 * integrate database
 * add ec2 to poll met eireann and push to dbc.

 After multiple failed attempts, a more finite approach has been decided, a new folder called [StandaloneTiers](./Scripts/Task2/StandaloneTiers/) has been created. Each Teir will be worked on until all  three are configured and operating as desired. Once all three independent scripts are running, then will be integrated into a singular stack. 

 First, a VPC was manually created for the application using the following steps from amazonQ 
[pic1](./screenshots/Screenshot%20From%202026-10-26%2016-10-54.png)
[pic2](./screenshots/Screenshot%20From%202026-10-26%2016-11-11.png)
[pic3](./screenshots/Screenshot%20From%202026-10-26%2016-11-24.png)

On generating the VPC, the manual scripts were run in the following order:
1. Database (the application layer and web layer are dependent on this)
2. Application layer (populate  the DBC with data)
3. Web layer.

* The database standalone script runs.
* After some debugging in the EC2 terminal the App standalone runs. the database needed to be decoupled and the met readings stored locally on the EC2 instance as an xml. [terminal debug](./screenshots/ec2_debug.png)

### Next Steps

* App and RDS standalones working in sync.
* Web standalone working
* All three working in sync
* Script merge. 


--- 

**Date:** October 27th, 2026 

* App ec2 stanalone has been debugged.
* next step is RDS communication integration
For this AmazonQ was questioned: [aws ec2 to RDS comms](./screenshots/ec2_rds_connection.png)

At this stage, after manually provisioning a VPC and debugging communication between the RDS and EC2 Instance, I am starting to understand how cloudformation stacks work. 

* At this stage I have a standalone RDS stack, a standalone app and the two integrated.
I have tidied the [App2Db.yaml](./Scripts/Task2/StandaloneTiers/App2Db.yaml) script. 
The next steps will be to generate the overall stack for task2. 
I think I will split this into two solutions:
1. One stack that does everything; VPC and RDS generation etc. 
2. Multi-stack solution; For real-world Ops I would partition the Database and VPC into there own stack as they are less ephemeral that the EC2 App and Web tiers. Rather than generate a new Database and VPC each stack call, existing istances can be called in paramters. 

### Next steps

1. test App2Db.yaml
2. Intergrate stanalone webpage stack
3. generate a standalone VPC stack
4. Generate an "All in one" stack
5. Tidy and streamline final task 2 solution.

---