# Engineering Game Plan Template

## Customer & Engagement Overview

The Virtual Shopping Assistant powered by generative AI is a tool that mimics the experience of an in-store salesperson online and is aimed at revolutionizing the online shopping experience. This advanced technology will understand customer preferences, suggest personalized product recommendations, provide detailed product information, and answer customer queries in real time. This AI assistant will enhance customer satisfaction, increase sales, and position this customer as a leader in retail innovation.


### Problem Statement



### Success Criteria

With the rise of online shopping, there's a growing demand for personalized and efficient shopping experiences. Success for this engagement will be to develop and deploy this AI-driven virtual assistant leveraging MSFT technology stack to cater to modern consumers' needs.

### Definition of Done
### Constraints


## Proposed Development Plan (architecture & coding plan)

### Machine Learning Projects

## Responsible AI Requirements

> CSE is now required to adhere to the Responsible AI Lifecycle (RAIL) and apply the [Responsible AI Baseline Requirements](https://aka.ms/CSEAIBaselineReqs) to all ML/AI projects. A successful CSE engagement may have requirements in the Envision, Define, and Prototype stages of the lifecycle.  
>
> *Have you ensured that the following requirements have been met?*  
>
> - [Responsible AI Baseline Requirements](https://aka.ms/CSEAIBaselineReqs) documentation has been completed for applicable stage of project and attached as Appendix or added to Artifact Hub (link to Artifact Hub document).
>
> - Initial CSE Ethics Check completed
>
> - All CSE stakeholders and team members on this engagement have completed the [Introduction to Responsible AI course](https://learn.microsoft.com/activity/S3332473/launch/#/). (25-min. duration)
>
> - Indicate if your project is a Sensitive Use or if additional/conditional guidance has been provided by CSE Ethics review committee or Office of Responsible AI.
>
> **Note:** In certain cases (e.g., if your project employs facial recognition), there may be [specific requirements](https://microsoft.sharepoint.com/sites/ResponsibleAI/SitePages/Part-B--Specific-Requirements(1).aspx) to consider and an [additional document](https://aka.ms/CSEAISpecificReqs) created.  

Add the link to the Responsible AI BAseline Requirements document here

## Data Management

> In this section, describe the current state of the customer’s data that we will use for this project.
>
> - What is the data?
> - Where is the data?
> - What work must be done to make the data usable for this project?
>   - Does the data need to be tagged, cleaned, etc?
>   - Are the classes imbalanced?  Are there missing fields?
> - Is the data available now?
>   - If so, where?
>   - If not, has a sample been seen? When will it be available? How will it be collected? If the data is synthetic, how are you generating the data?
> - How will you model the data?  
> - What risks are there with the customer’s data?

**Example:** *The customer have data from weekly inventory reports and daily POS transactions. The inventory data have 'on hand', 'on order' and 'out of stock' information for each product and distribution center.
Daily point of sale transaction data is aggregated weekly and has information for each store on 'unit of sale', 'on hand' and 'on order.'
Customer manages the database tables, and we can access data either to query data from specific tables or Azure Data Lake Solution(ADLS).
In order to make the data usable for this project, The data integrity needs to be confirmed, and clean the data.  The data is available now, and we have access to the data.*

## Data Governance

> What are the privacy, security or regulatory restrictions on data collection, access, movement, encryption?
>
> What is the plan on how to comply (and monitor compliance) to these restrictions?

Insert Data Governance content here…

## ML Testing

>Describe the testing approach for ML and DS components of the project:
>
> - What is the test strategy for the proposed ML approaches? 
> - How will the model(s) be validated? 
> - How will you use unit tests, integration testing, and other testing strategies to test the ML models, and other DS components?

Insert ML Testing content here…

## ML Maintenance

>Describe the drift detection and/or model adaptation strategy considerations that support maintenance and uphold representativeness of the ML solution over time:
>
> - How will the model(s) be monitored and maintained through time?
> - What are some likely drift scenarios? What types of drift might occur? Ex. Gradual, abrupt
> - Describe the model adaptation strategy for the proposed ML approaches.
> - Describe the drift detection strategy for the proposed ML approaches, if applicable. 

## ML Risk Assessment

Complete the ML Risk Assessment below by marking whether the assessment is Green, Yellow or Red. Tally the count and report this at the bottom.

|Green ||Yellow||Red||
|----------|-----------|------------|-|-|-|
|**Problem Space** ||||||
|Cutting edge ML application in our focus areas|x|Straight-forward, textbook problem|x|Data analysis, BI|x|
|**Data** ||||||
|Sufficient quantity, clean|x|Limited, noisy|x|Insufficient|x|
|**Label** ||||||
|Well-defined, available or can be derived|x|Needs manual work|x|No obvious way to obtain|x|
|**Feasibility** ||||||
|No obvious blockers, customer expectations realistic|x|Experimental, time/customer pressure makes risky|x|Success unlikely, unrealistic expectations|x|
|**Production Prospects** ||||||
|Drop-in replacement for existing production system, committed customer|x|No immediate production plans, but required proof point and line of sight|x|One off, no production plan|x|
|**Customer Team** ||||||
|Available to code-with, strong ML skills |x|Has one or two to code with, learners|x|No-one to code with|x|
|**Ethics** ||||||
|CSE Ethics Committee passed with no concerns, or not applicable. |x|CSE Ethics Committee passed with cautionary guidance|x|CSE Ethics Committee requested further review before deployment |x|
|**Total Green** ||**Total Yellow**||**Total Red**||

Mitigation
> Describe steps to mitigate any yellow/red flags

### Leveraging Prior Work

FFModel

## Risks & Issues

|Risk / Issue |Likelihood |Impact| Exposure |Mitigation| 
|-|-|-|-|-|
|No product catalog dataset is readily available.|-|-|-|-|


## Customer Handoff and Production Planning

This will be used for upskilling and internal testing. There is no current plan to put into Production.


## Proposed Strawman Sprint Schedule
|Milestone|Sprint|Date|Type|User stories/Focus/Deliverable (examples)|
|-|-|-|-|-|
|**1**|0|< start >|prep|Write user stories, prioritize backlog, spike on X, Y|
| |1|+ 1 wk|prep|Get CI/CD pipeline working, data clean and simplest ML model integrated|
||2|+ 2 wks|execution|Implement stories A, B with Customer|
||3|+ 3 wks|execution|Implement stories C, D with Customer|
|**2**|4|+ 4 wks|prep|Update backlog, spike sprint, refine hypotheses|
||5|+ 5 wks|execution|Implement stories E, F with Customer|
||6|+ 6 wks|execution|Implement stories G, H with Customer|
||7|+ 7 wks|follow-up|Integrate onsite / virtual work into Milestone 2 Epic|
||8|+ 8 wks|follow-up|Customer handoff|
|**3**|9|+ 9 wks|prep|Update Release Plan|
||10|+ 10 wks|prep|Generalize reusable code for OSS|
||11|+ 11 wks|prep|Product team feedback|
||12|+ 12 wks|follow-up|Retrospective|

