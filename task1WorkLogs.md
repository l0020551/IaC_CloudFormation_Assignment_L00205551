
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

Today, the S3 bucket will be integrated and a file's content concatenated to screen.

As I have no background in web development and the "Hello World" content of the tutorial looks basic on the webpage, I prompted an LLM to generate a HTML document that will be retrieved from the S3 buckets. Here is the prompt content:

```
I need a simple but cleanly designed HTML file. The file will just contain two lines of text in the header, the top line reading "Student: John Doe", the second line reading "Student ID: 123456789" , take liberties with remaining aesthetic design

```

OpenAI and Gemini were fed this prompt and the files produced can be found in this directory: `./Scripts/Task1/LLM_generated_html_files`.
On viewing the file content in a HTML renderer the ChatGPT HTML appeared to be the one that best met the needs for the task. The appropriate changes were made and saved in the main `Scripts` directory under `S3_student_info.html`.

The next step is accessing or mounting the S3 bucket so that the EC2 instance can access the file. This [tutorial](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AmazonS3.html) on aws was followed.

The S3 bucket was added to `Resources: WebsiteContentBucket` the integration of S3 and EC2 was attempted with the tutorial, but without success. 


After several attempts including using amazonQ to help debug, another LLM was prompted to help further debug. After feeding the script into the ChatGPT LLM, it gave feedback recommending using a loop to try pull the HTML from the S3 bucket. These changes are commented in the provided yaml script.  

These two LLMs recommended adding read permissions and adding a retry mechanism for the S3 upload to the webpage. On applying these changes, the script worked as desired. 

![Print to website](./screenshots/Task1_screens_shot.png)

To further improve the script, in the next entry the script will be further refined to not use a retry mechanism, rather than generating a new S3 bucket, it will recall one with the HTML file already loaded. 



**Date:** October 25th, 2026  
### Updates
During the week Amazon gave a notification as follows:[aws_notification](./screenshots/aws_notification.png)

The Linux version used in some scripts ran the previous week is out of support. The scripts need to be checked. 
On reviewing active repository scripts, the EC2instances are already running the AL2 successor; AL2023 or the latest Amazon image release `'/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2'`.

### Update to task 1
In the first working iteration, an s3 container is generated in the stack, The webpage html needs to be manually updated while the stack checks for an upload.
This is inefficient. In the next iteration, it will refence an existing s3 container. This will mean the userdata will not require a loop to check if a file has been added to the s3 bucket. Instead, it will recall the file from an existing bucket. This script is in this commit and push does this. 



***
