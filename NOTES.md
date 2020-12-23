# __Starbuck's Capstone Challenge__

Instructions for the project can be found in the Starbucks Project Workspace.

## __Dataset overview__
The program used to create the data simulates how people make purchasing decisions and how those decisions are influenced by promotional offers.

Each person in the simulation has some hidden traits that influence their purchasing patterns and are associated with their observable traits. People produce various events, including receiving offers, opening offers, and making purchases.

As a simplification, there are no explicit products to track. Only the amounts of each transaction or offer are recorded.

There are three types of offers that can be sent: 
 1. __buy-one-get-one (BOGO)__: In a BOGO offer, a user needs to spend a certain amount to get a reward equal to that threshold amount
 2. __discount__: In a discount, a user gains a reward equal to a fraction of the amount spent.
 3. __informational__: In an informational offer, there is no reward, but neither is there a requisite amount that the user is expected to spend.
 
Offers can be delivered via multiple channels. The basic task is to use the data to identify which groups of people are most responsive to each type of offer, and how best to present each type of offer.

## __Data Dictionary__
`profile.json` : Rewards program users (17000 users x 5 fields)
- gender: (categorical) M, F, O, or null
- age: (numeric) missing value encoded as 118
- id: (string/hash)
- became_member_on: (date) format YYYYMMDD
- income: (numeric)

`portfolio.json`: Offers sent during 30-day test period (10 offers x 6 fields)
- reward: (numeric) money awarded for the amount spent
- channels: (list) web, email, mobile, social
- difficulty: (numeric) money required to be spent to receive reward
- duration: (numeric) time for offer to be open, in days
- offer_type: (string) bogo, discount, informational
- id: (string/hash)

`transcript.json`: Event log (306648 events x 4 fields)
- person: (string/hash)
- event: (string) offer received, offer viewed, transaction, offer completed
- value: (dictionary) different values depending on event type
- offer id: (string/hash) not associated with any "transaction"
- amount: (numeric) money spent in "transaction"
- reward: (numeric) money gained from "offer completed"
- time: (numeric) hours after start of test


# __Build Your Data Science Project__

In this capstone project, you will leverage what you’ve learned throughout the program to build a data science project of your choosing. Your project deliverables are:

1. __A Github repository of your work.__
2. __A blog (or other medium for a write-up) post written for a technical audience.__

__or__

2. __A deployed web application powered by data.__

You'll follow the steps of the data science process that we've discussed:

- You will first define the problem you want to solve and investigate potential solutions.
- Next, you will analyze the problem through visualizations and data exploration to have a better understanding of what algorithms and features are appropriate for solving it.
- You will then implement the algorithms and metrics of your choice, documenting the preprocessing, refinement, and post-processing steps along the way.
- Afterwards, you will collect results about your findings, visualize significant quantities, validate/justify your results, and make any concluding remarks about whether your implementation adequately solves the problem.
- Finally, you will construct a blog post (or other medium for a write-up) to document all of the steps from start to finish of your project, or deploy your results into a web application.

## __Setting Yourself Apart__

An important part of landing a job or advancing your career as a data scientist is setting yourself apart through impressive data science projects. By now, you've completed several guided projects, and now's your chance to show off your skills and creativity. You'll receive a review of your project with feedback from a Udacity mentor, and they will focus on how your project demonstrates your skills as a well-rounded data scientist.

This project is designed to prepare you for delivering a polished, end-to-end solution report of a real-world problem in a field of interest. When developing new technology, or deriving adaptations of previous technology, properly documenting your process is critical for both validating and replicating your results.

## __Things you will learn by completing this project:__

- How to research and investigate a real-world problem of interest.
- How to accurately apply specific data science algorithms and techniques.
- How to properly analyze and visualize your data and results for validity.
- How to document and write a report of your work.