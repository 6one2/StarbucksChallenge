<div max-width="100%">
<img src="./assets/niels-kehl-6hpbjaAubDc-unsplash.jpg" width="100%">
<span>Photo by <a href="https://unsplash.com/@photographybyniels?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Niels Kehl</a> on <a href="https://unsplash.com/s/photos/starbucks?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Unsplash</a></span>
</div>


# __Background__

In the final project for my DataScience degree at [Udacity](https://www.udacity.com/course/data-scientist-nanodegree--nd025), I had access to a data set containing simulated data that mimics customer behavior on the Starbucks rewards mobile app. Over the period of 30 days, Starbucks sends out 0 to 6 offers to users of the mobile app. An offer can be merely an advertisement for a drink (called `informational` offer) or an actual offer such as a `discount` or `bogo` (buy one get one free).

Associated with the time-line of events for all participants, came the demographic profile of each individuals with details on their `gender`, `age`, `income`, the date their profile was registered on the app (`become_member_on`).
In order to drive customer to the stores, it is paramount to understand how each customer interacts with the app, and in particular how each customer reacts to a specific offer.

I first focused my interested on how often the offers were viewed, and then on how this was leading to some kind of conversion into sales.

My approach was first exploratory, and therefore I tried to visualize clusters of behavior among  customers groups. Then, I tried to model these behaviors to predict how future participants might interact with each offer.


# __What an interaction looks like ?__

In the picture below (figure 1) you'll find the time-line of events for one customer. You'll see 4 offers (3 `bogo` and 1 `discount`). All offers have specific durations (in this exmaple: 7, 3, 7, and 5 days respectively). they also have different level of difficulty, or amount that need to be spent to be rewarded.

To give an example, a user could receive a discount offer _buy 10 dollars get 2 off_. The offer is valid for 10 days from receipt. If the customer accumulates at least 10 dollars in purchases during the validity period, the customer completes the offer.

<div max-width="100%">
<img src="./assets/Timeline.png" width="100%">
<p style="text-align:center; font-style:italic">
Figure 1. Time-line of events for one customer. Red lines represent the reception of an offer. Blue lines represent the moment the offer was viewed. Yellow lines show when an offer was completed. Black lines (solid and dashed) represent the occurence of a transaction.
</p>
</div>

However, there are a few things to watch out for in this data set and in our analysis:

- Customers do not opt into the offers that they receive; in other words, a user can receive an offer, never actually view the offer, and still complete the offer. For example, a user might receive the "buy 10 dollars get 2 dollars off offer", but the user never opens the offer during the 10 day validity period. The customer spends 15 dollars during those ten days. There will be an offer completion record in the data set; however, the customer was not influenced by the offer because the customer never viewed the offer. This will require to filter out the completions that occured before an offer is viewed.

- The data set actually differentiates 10 offers (4 `bogo`, 4 `discount`, and 2 `informational`). The specificity of each offer is found in its _difficulty_ (amount of dollars needed to complete the offer), and its _duration_ (number of days of activity). Since the goal of this analysis was to find which offer was preferred by which customer and not to address the effect of difficulty and duration per se, we decided to group them together and simplify our analysis by looking at the overall response to `bogo`, `discount`, and `informational` offers.

- Distribution of offers type:
<div style="width: 100%; overflow: hidden;">
    <div style="width:40% ; float: left; text-align: right"> <img src="./assets/offer_dist.png" width="200px"></div>
    <div style="margin-left:45%"> Considering that there are find 4 sub-offers in <code>bogo</code>, 4 sub-offers in <code>discount</code> but only 2 sub-offers in <code>informational</code>, is is clear that all offers sub-types were equally present (10% each).</div>
</div>

- The completion is straight forward for the `bogo` and `discount` offers, and I will use this indicator to measure success in this cases. However, the measurement of success for the `informational` offers requires much more discussion as many metrics of success can be implemented.


# __Offer Response__

After filtering out customers with no demographic information (n = 2,175), the few customers that never received any offers (n = 5), and the customers that did not made any transactions (n = 333), I found that 88% of the 14,487 customers left viewed all the offers presented to them, 99% of them viewed over 66% of the offers preswented to them, but more importantly that all customers viewed at least 50% of tht offer presented to them.

<div>
<p style="text-align:center; font-family:courier; font-size:150%">
    "All customers viewed at least 50% of the offers presented to them. 88% of the customers viewed all the offers presented to them."
</p>
</div>

With an average viewing rate of 97% accross all offers, and all customers interacting positively with the app (> 50% viewing for all), we can now focus our attention to the conversion from viewing to actual sales.


# __Offer Conversion__

As mentioned earlier the conversion for both the `bogo` and the `discount` offers was very clear: _offer marked as completed in the `transcript` data set_. For this reason and the fact that the presentation rate of these 2 offers were similar, I chose to focus on the comparison of these 2 offers only in the rest of this section.

I considered a conversion when an offer was completed only after the offer was viewed. The overall conversion rate was 41.5% for the `bogo` offers and 46.1% for the `discount` offers. I then labeled customers as successful at converting the offer if they showed individually 50% or higher conversion rate.

<div max-width="100%">
<img src="./assets/AgeIncome.png" width="100%">
<p style="text-align:center; font-style:italic">
Figure 2. Customers age versus income. The orange dots represent the customers that completed the offers (<code>bogo</code> on the left panel, and <code>discount</code> on the right panel) and blue dots represent customers that did not completed the offers. The size of the dots represent the gender of the customers.
</p>
</div>

<div style="width: 100%; overflow: hidden;">

</div>

<div style= "max-width: 100%; overflow: hidden;">
    <div style="width:50% ; float: left; text-align: right"><img src="./assets/AgeIncome.png" width="100%"></div>
    <div style="margin-left:50%; text-align: center"><img src="./assets/AgeIncome.png" width="100%"></div>
<!-- <img src="./assets/AgeIncome.png" width="100%"> -->
<p style="text-align:center; font-style:italic">
Figure 3. Caption.
</p>
</div>

# __Final Thoughts:__

 - Not all users receive the same offer, and that is the challenge to solve with this data set.
 - simplified dataset
