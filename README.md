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