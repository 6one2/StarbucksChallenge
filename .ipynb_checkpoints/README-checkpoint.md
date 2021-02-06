# __Starbucks Capstone Challenge__
<div max-width="100%">
<img src="./docs/assets/niels-kehl-6hpbjaAubDc-unsplash.jpg" width="100%">
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
 3. __informational__: In an informational offer, there is no reward, but neither is there a requisite amount that the user is expected to spend.

Offers can be delivered via multiple channels. The basic task is to use the data to identify which groups of people are most responsive to each type of offer, and how best to present each type of offer.

> __The task was to combine transaction, demographic and offer data to determine which demographic groups respond best to which offer type.__

I chose first an exploratory approach. After data preparation and simplification due to a great number of missing values, I decided to visually explore the relationship between completion (for `bogo` and `discount` only) and the limited amount of customer demographics, namely:
- gender
- age
- date of registration
- income

From these observations I extracted relevant brackets for each categories and compare conversion rate for each possible groups.

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

## __Results Summary__

## __Licensing, Authors, Acknowledgements__

- [Udacity DataScience nanodegree](https://www.udacity.com/course/data-scientist-nanodegree--nd025)
- [Regression Tutorial](https://towardsdatascience.com/machine-learning-with-python-regression-complete-tutorial)
- [Linear Regression Interpretation](https://scikit-learn.org/dev/auto_examples/inspection/plot_linear_model_coefficient_interpretation.html#sphx-glr-auto-examples-inspection-plot-linear-model-coefficient-interpretation-py)
