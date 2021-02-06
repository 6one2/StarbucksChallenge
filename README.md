# __Starbucks Capstone Challenge__
<div max-width="100%">
<img src="./docs/assets/niels-kehl-6hpbjaAubDc-unsplash.jpg" width="100%">
<br>
<span>Photo by <a href="https://unsplash.com/@photographybyniels?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Niels Kehl</a> on <a href="https://unsplash.com/s/photos/starbucks?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Unsplash</a></span>
</div>
<br>

_You can find a full commentary of this analysis [here](https://6one2.github.io/StarbucksChallenge/)._

## __Installation__
I used fairly standard libraries like `numpy`, `pandas`, `re`, `datetime`, `scipy`, `matplotlib`, `seaborn` for data wrangling and visualization.
I used `sqlalchemy` to store the results table and modified customers' profile table.
I used `sklearn` extensively in the model section.

## __Project Overview & Motivation__

During the Udacity Data Science Nanodegree program, I had access to data from Starbucks that simulates how people make purchasing decisions and how those decisions are influenced by promotional offers.

Each person in the simulation has some hidden traits that influence their purchasing patterns and are associated with their observable traits. People produce various events, including receiving offers, opening offers, and making purchases.

As a simplification, there are no explicit products to track. Only the amounts of each transaction or offer are recorded.

There are three types of offers that can be sent:
 1. __buy-one-get-one (BOGO)__: In a BOGO offer, a user needs to spend a certain amount to get a reward equal to that threshold amount
 2. __discount__: In a discount, a user gains a reward equal to a fraction of the amount spent.
 3. __informational__: In an informational offer, there is no reward, but neither is there a required amount that the user is expected to spend.

Offers can be delivered via multiple channels. The basic task is to use the data to identify which groups of people are most responsive to each type of offer, and how best to present each type of offer.

> __The task was to combine transaction, demographic, and offer data to determine which demographic groups respond best to which offer type.__

I chose first an exploratory approach (see [conversion section](devStarbucks.ipynb/#Who-is-converting-which-offer?)). After data preparation and simplification due to a great number of missing values, I decided to visually explore the relationship between completion (for `bogo` and `discount` only) and the limited amount of customer demographics, namely:
- gender
- age
- date of registration
- income

From these observations, I extracted relevant brackets for each category and compare the conversion rate for each possible group.

Finally, I tried to improve the analysis by adding a linear regression of the amount spent once an offer is viewed by the customer to gain a better understanding of the performance of each offer (section [Model](devStarbucks.ipynb/#Model)).

## __Project Structure__

```
.
├── README.md
├── code
│   ├── __init__.py
│   ├── __pycache__
│   ├── data_modeling.py
│   ├── data_visualization.py
│   ├── data_wrangling.py
│   └── starbucks_class.py
├── data
│   ├── db_results.db
│   ├── portfolio.json
│   ├── profile.json
│   └── transcript.json
├── devStarbucks.html
├── devStarbucks.ipynb
└── docs
    ├── _config.yml
    ├── assets
    └── index.md
```

The analysis is found in the main notebook [devStarbucks.ipynb](devStarbucks.ipynb). This notebook calls several custom modules found in `./code/`:

### Modules in `./code/`:
- `data_modeling.py`: functions for building, running and evaluating the model
- `data_visualization.py`: functions for creating the timeline visual representation.
- `data_wrangling.py`: functions for loading, filtering and manipulating data
- `starbucks_class.py`: two classes `Person` (keeping track of each customer) and `Event` (keeping track of each offer received) to help create the results table.

### Data Dictionaries and database in `./data/`:
`db_results.db`: This SQL database was not part of the original data, but was created to store the result table and modified customer profile. This database is created in section [Creating metrics for analysis](devStarbucks.ipynb/#Creating-metrics-for-analysis)

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

### GitHub page for full commentary in  `./docs/`:

## __Results Summary__

The exploratory approach was rather effective to provide insights on the conversion rates of selected subgroups but only for the `bogo` and `discount` offer types. The top-10 conversion rates tables are probably a good first step in the direction of improving the delivery of these offers (find example [here](devStarbucks.ipynb/#TOP-10-conversion-for-max-difference)).

The attempt to present a more granular quantification of the customers' performance with a linear regression model was tempered by the scarcity of data and the relatively small number of available features. The best model was found for the `discount` offer type but was yielding only a 62% r2 score and a large mean absolute error.

## __Licensing, Authors, Acknowledgements__

- [Udacity DataScience nanodegree](https://www.udacity.com/course/data-scientist-nanodegree--nd025)
- [Regression Tutorial](https://towardsdatascience.com/machine-learning-with-python-regression-complete-tutorial)
- [Linear Regression Interpretation](https://scikit-learn.org/dev/auto_examples/inspection/plot_linear_model_coefficient_interpretation.html#sphx-glr-auto-examples-inspection-plot-linear-model-coefficient-interpretation-py)
