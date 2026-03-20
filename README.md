# Power Outage Analysis
# Introduction
Power outages are a an issue of critical infrastucture failure in the United States. Power outages affect millions of people each year and disrupt daily life, business and safety. Outages are caused by a variety of factors including weather, equipment failure and human interference. By understanding common patterns behind outages and their impact, we can improve power grid stability and improve response strategies.

This project analyzes a dataset of major power outages in the U.S. from 2000 to 2016, created by Purdue University's Labratory for Advancing Sustainable Critical Infrastructure. The outages in this dataset are typically defined as events affecting at least 50,000 customers or of significant demand loss.

The central question of this analysis is: **Do outages caused by severe weather lead to greater demand loss compared to outages caused by other facotrs?**

This question focuses on different outage causes with demand loss as our measure of severity. Answering this question gives insight into how specific events result in more distruptive outages, giving us possible recommendations for infrastructure planning and risk mitigation in the future to build stronger systems for our communities.

The original dataset has 1534 rows (outages) and 57 columns (features). In this analysis, I'll focus on some selected most relevant columns listed below.


| Column | Description |
|--------|-------------|
| `YEAR` | Year an outage occurred |
| `MONTH` | Month an outage occurred |
| `U.S._STATE` | State the outage occurred in |
| `NERC.REGION` | North American Electric Reliability Corporation (NERC) region of the outage |
| `CLIMATE.REGION` | U.S. climate region (NCEI classification) |
| `ANOMALY.LEVEL` | Oceanic Niño Index (ONI) indicating El Niño/La Niña intensity |
| `CLIMATE.CATEGORY` | Climate condition category (e.g., normal, El Niño, La Niña) |
| `OUTAGE.START.DATE` | Date when the outage started |
| `OUTAGE.START.TIME` | Time when the outage started |
| `OUTAGE.RESTORATION.DATE` | Date when the restoration started |
| `OUTAGE.RESTORATION.TIME` | Time when the restoration started |
| `CAUSE.CATEGORY` | Main cause of the outage |
| `OUTAGE.DURATION` | Duration of the outage (minutes) |
| `DEMAND.LOSS.MW` | Peak demand loss during the outage (MW) |
| `CUSTOMERS.AFFECTED` | Number of customers affected |
| `TOTAL.PRICE` | Average electricity price in the state (cents/kWh) |
| `TOTAL.SALES` | Total electricity consumption in the state (MWh) |
| `TOTAL.CUSTOMERS` | Total number of electricity customers in the state |
| `POPPCT_URBAN` | Percentage of population living in urban areas |
| `POPDEN_URBAN` | Urban population density (persons per square mile) |
| `AREAPCT_URBAN` | Percentage of land area classified as urban |

# Data Cleaning and Explanatory Data Analysis
I started by cleaning the data to prepare it for analysis.

### Data Cleaning
I began by only keeping relevant columns for the analysis. This removes unrelated features and ensures the columns in my dataset aligned with the scope of the project.For this analysis, I'll be using the columns I included in the data dictionary above. 


Next, I combined the OUTAGE.START.DATE and OUTAGE.START.TIME columns into one Timestamp object in an OUTAGE.START column. I did the same for OUTAGE.RESTORATION.DATE and OUTAGE.RESTORATION.TIME to create a Timestamp object called OUTAGE.RESTORATION. After this, I dropped the old columns I used to make these two new columns.


Next, I checked my outcome variables, OUTAGE.DURATION, CUSTOMERS.AFFECTED, and DEMAND.LOSS.MW for values of 0. Values of 0 are likely evidence of missing values or improperly recorded data since major outages wouldn’t have a duration of 0 minutes, 0 customers affected, or 0 MW of energy lost. Before modifying them, I displayed how often zeros and missing values occur to better understand the structure of missingness.

I also evaluated missingness across all columns and found that DEMAND.LOSS.MW and CUSTOMERS.AFFECTED have substantial missing values, while OUTAGE.DURATION and the timestamp variables have a smaller number of missing values. This confirms that missingness should be analyzed later in the analysis.

To simplify urbanization-related information, I combined POPPCT_URBAN, POPDEN_URBAN, and AREAPCT_URBAN into one column, URBAN. Because these variables are on different scales, I started by standardizing each one and then averaging them. This produces a measure of urbanization that avoids any single variable dominating the new feature. After creating this feature, I dropped the original urbanization columns to reduce redundancy.

Finally, I corrected data types across the dataset. Numeric variables stored as objects were converted to numeric types. Similarly, categorical variables were converted to be strings and YEAR and MONTH were converted to integers. This ensures that any computation done later in the analysis can happen smoothly.


Below is the first 5 rows of this cleaned dataset.


<div style="max-height: 400px; overflow-y: auto; border: 1px solid #ccc;">
    <table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>YEAR</th>
      <th>MONTH</th>
      <th>U.S._STATE</th>
      <th>NERC.REGION</th>
      <th>CLIMATE.REGION</th>
      <th>ANOMALY.LEVEL</th>
      <th>CLIMATE.CATEGORY</th>
      <th>CAUSE.CATEGORY</th>
      <th>OUTAGE.DURATION</th>
      <th>DEMAND.LOSS.MW</th>
      <th>CUSTOMERS.AFFECTED</th>
      <th>TOTAL.PRICE</th>
      <th>TOTAL.SALES</th>
      <th>TOTAL.CUSTOMERS</th>
      <th>OUTAGE.START</th>
      <th>OUTAGE.RESTORATION</th>
      <th>URBAN</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2011</td>
      <td>7</td>
      <td>Minnesota</td>
      <td>MRO</td>
      <td>East North Central</td>
      <td>-0.3</td>
      <td>normal</td>
      <td>severe weather</td>
      <td>3060.0</td>
      <td>NaN</td>
      <td>70000.0</td>
      <td>9.28</td>
      <td>6.56e+06</td>
      <td>2.60e+06</td>
      <td>2011-07-01 17:00:00</td>
      <td>2011-07-03 20:00:00</td>
      <td>-0.51</td>
    </tr>
    <tr>
      <td>2014</td>
      <td>5</td>
      <td>Minnesota</td>
      <td>MRO</td>
      <td>East North Central</td>
      <td>-0.1</td>
      <td>normal</td>
      <td>intentional attack</td>
      <td>1.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>9.28</td>
      <td>5.28e+06</td>
      <td>2.64e+06</td>
      <td>2014-05-11 18:38:00</td>
      <td>2014-05-11 18:39:00</td>
      <td>-0.51</td>
    </tr>
    <tr>
      <td>2010</td>
      <td>10</td>
      <td>Minnesota</td>
      <td>MRO</td>
      <td>East North Central</td>
      <td>-1.5</td>
      <td>cold</td>
      <td>severe weather</td>
      <td>3000.0</td>
      <td>NaN</td>
      <td>70000.0</td>
      <td>8.15</td>
      <td>5.22e+06</td>
      <td>2.59e+06</td>
      <td>2010-10-26 20:00:00</td>
      <td>2010-10-28 22:00:00</td>
      <td>-0.51</td>
    </tr>
    <tr>
      <td>2012</td>
      <td>6</td>
      <td>Minnesota</td>
      <td>MRO</td>
      <td>East North Central</td>
      <td>-0.1</td>
      <td>normal</td>
      <td>severe weather</td>
      <td>2550.0</td>
      <td>NaN</td>
      <td>68200.0</td>
      <td>9.19</td>
      <td>5.79e+06</td>
      <td>2.61e+06</td>
      <td>2012-06-19 04:30:00</td>
      <td>2012-06-20 23:00:00</td>
      <td>-0.51</td>
    </tr>
    <tr>
      <td>2015</td>
      <td>7</td>
      <td>Minnesota</td>
      <td>MRO</td>
      <td>East North Central</td>
      <td>1.2</td>
      <td>warm</td>
      <td>severe weather</td>
      <td>1740.0</td>
      <td>250.0</td>
      <td>250000.0</td>
      <td>10.43</td>
      <td>5.97e+06</td>
      <td>2.67e+06</td>
      <td>2015-07-18 02:00:00</td>
      <td>2015-07-19 07:00:00</td>
      <td>-0.51</td>
    </tr>
  </tbody>
</table>
</div>


### Explanatory Data Analysis
#### Univariate Analysis
I started by exploratory data analysis with univariate analysis to visualize the distribution of single variables.

First, I examined the distribution of outage duration. This allowed me to visualize how outage lengths vary across events and whether the distribution is concentrated among shorter outages more extreme durations.


<h3>Distribution of Outage Duration</h3>
<iframe src="duration_hist.html" width="100%" height="500"></iframe>


Then, I looked at the distribution of customers affected. This allowed me to see the scale of the outages and show whether most events impact a few customers or if a small number of large-scale outages dominate the dataset.


<h3>Distribution of Customers Affected</h3>
<iframe src="customers_hist.html" width="100%" height="500"></iframe>


#### Bivariate Analysis
Next, I examined the relationships between 2 variables to see if patterns emerged when visualized.


I began by examining the relationship between Outage Duration and Demand Loss. I expected to see a positive association because the longer an outage lasts, the more demand is lost over time. 


<h3>Outage Duration vs Demand Loss</h3>
<iframe src="duration_vs_demand.html" width="100%" height="500"></iframe>


Next, I visualized the relationship between urbanization and customers affected. I expected to see a positive association because outages in more urbanized areas are likely to impact a larger number of customers due to higher population density. This helps assess whether urbanization is a predictor of outage scale.


<h3>Urbanization vs Customers Affected</h3>
<iframe src="urban_vs_customers.html" width="100%" height="500"></iframe>


Lastly, I plotted outage duration against customers affected to see if longer outages impact more people. This helps determine whether outage severity is driven primarily by duration, scale or both.


<h3>Outage Duration vs Customers Affected</h3>
<iframe src="duration_vs_customers.html" width="100%" height="500"></iframe>


#### Grouping and Aggregation 
I grouped the dataset by NERC Region to see the distribution of outages by region. This provides a way to see which regions experience more severe outages.
open 
Grouped table 1

Then, I group by cause category to see how different types of outage causes vary in frequency and impact. This helps us identify whether certain causes are associated with specific type of outages.

Grouped 2

Fianlly, I used a pivot table to summarize average outage duration and demand loss across regions and cause. This allows for a simple comparison of how outage characteristics differ across key dimensions.

Pivot table


# Assessment of Missingness
#### MNAR Analysis


#### Missing Dependency
##### Cause

##### Month


# Hypothesis Testing
I will be testing whether outages caused by severe weather lead to greater demand loss on average compared to outages caused by other factors. The relevant columns are DEMAND.LOSS.MW and CAUSE.CATEGORY. I will use outages where CAUSE.CATEGORY is “severe weather” and compare them to all other categories.


**Null Hypothesis: ** On average, the demand loss from severe weather outages is the same as the demand loss from outages caused by other factors.
 

**Alternate Hypothesis: ** On average, the demand loss from severe weather outages is greater than the demand loss from outages caused by other factors.


**Test statistic: ** Difference in means. Specifically, mean demand loss (severe weather) − mean demand loss (other causes). 


I performed a permutation test with 10,000 simulations to generate the null distribution of the test statistic.


I got a p-value of BLANK, indicating strong evidence against the null hypothesis at a 0.05 significance level.


This plot shows the observed difference in means compared to the distribution of differences generated under the null hypothesis.


# Framing a Prediction Problem
My model will predict the cause of a power outage, specifically whether it is due to severe weather or not. This is a binary classification problem.


The metric I'm using is the F1 score, since class imbalance is likely and F1 balances precision and recall.


At the time of prediction, I would have variables such as state, NERC region, climate region, anomaly level, year, month, total sales, total price, total customers, and urbanization metrics.


# Baseline Model
My model is a binary classification model.


My model's features are NERC.REGION, ANOMALY.LEVEL, YEAR, and URBAN.


The predicted column was CAUSE.CATEGORY, encoded as 1 for severe weather and 0 for other causes.


# Final Model
My final model used features:


I added BLANK to BLANK


I used GridSearchCV to select the best hyperparameters for the DecisionTreeClassifier. These were:


BLANK

# Fairness Analysis
My groups for the fairness analysis are 


I decided to use these groups because 


My evaluation metric will be 

**Null Hypothesis:** The model is fair.


**Alternative Hypothesis:** The model is unfair. 

I performed a permutation test with 10000 trials. My significance level is the standard 0.05, and I got a p_value of 0.0 so because this is below the significance level, I reject the null hypothesis. The model is significantly different in terms of F1 score for longer vs shorter outages.