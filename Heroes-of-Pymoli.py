
# coding: utf-8

# In[958]:


# ...................................   OBSERVABLE TRENDS .............................................
#
# 1. 780 purchases were made yeilding revenues of $2379.77
# 2. Players re predomintley male (84%).  Females constitue only 14% of the players.  
#    Roughly 2% of the players did not disclose thioer gender. 
# 3. As expected from the players demographics, males made most of the purchases (652).
# 4. Average purchase price of the purchases across all demographics was $3.19
# 5. Most of the players were between the ages of 20 to 24. Under 10 and over 40 players were the smallest. 
# 6. Most purchasers were aged between 20 to 24. 
# 7. The top seller game was Oathbreaker, Last Hope of the Breaking Storm and generated most of the profit.


# In[959]:


# Dependencies and Setup
import pandas as pd
import numpy as np


# In[960]:


# Load the file
dataFile = "purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data_pd = pd.read_csv(dataFile)


# In[961]:


purchase_data_pd.head()


# In[962]:


# Purchasing Analysis (Total)

# Run basic calculations to obtain number of unique items, average price, etc.
# Create a summary data frame to hold the results
# Optional: give the displayed data cleaner formatting
# Display the summary data frame

# get number of unique purchases
unique_items = len(purchase_data_pd["Item ID"].value_counts())

# get the average price of items
avg_price = round(purchase_data_pd["Price"].mean(), 2)

# get number of purchased 
number_of_purchases = len(purchase_data_pd["Purchase ID"].value_counts())

# total revenue generated from sales
total_revenue = purchase_data_pd["Price"].sum()
total_revenue = round(total_revenue, 2)

# Create dataframe for number of items, avg sale price, number of purchases, and total revenue
purchase_summary = []
purchase_summary.append(unique_items)
purchase_summary.append("$" + str(avg_price))
purchase_summary.append(number_of_purchases)
purchase_summary.append("$" + str(total_revenue))

purchase_df = pd.DataFrame([purchase_summary], columns = ["Number of Unique Items", "Average Price", 
                                            "Number of Purchases", "Total Revenue"])

purchase_df.head()


# In[971]:


# Gender Demographics

# Percentage and Count of Male Players
# Percentage and Count of Female Players
# Percentage and Count of Other / Non-Disclosed

# Get rid off duplicates 1st. 
gender_dem_df = purchase_data_pd.drop_duplicates("SN", inplace=False)
gender_dem_df.head()

# Determine count of male players
is_male = gender_dem_df["Gender"] == "Male"
males_df = gender_dem_df[is_male]
males_count = males_df.shape[0]

# Determine count of female players
is_female = gender_dem_df["Gender"] == "Female"
females_df = gender_dem_df[is_female]
females_count = females_df.shape[0]

# Subtract males + females from player_count to determine number of Other/Non-Disclosed
other_non_disclosed_count = player_count - (males_count + females_count)

# Calculate percentages for males, females and other/non_discolsed
males_percentage = round(((males_count /player_count) * 100), 2)
females_percentage = round(((females_count /player_count) * 100), 2)
other_non_disclosed_percentage = round(((other_non_disclosed_count /player_count) * 100), 2)

# Create the dataframe for dempraphic data
demographics_df = pd.DataFrame({"Gender": ["Male", "Female", "Other / Non-Disclosed"], 
                                "Total Count": [males_count, females_count, other_non_disclosed_count],
                                "Percentage of Players": 
                                [males_percentage, females_percentage, other_non_disclosed_percentage],
                                }, 
                               columns = ["Gender", "Total Count", "Percentage of Players"])

demographics_df = demographics_df.set_index("Gender")
demographics_df.style.format({"Percentage of Players": "{:.2f}%"})  


# In[964]:


# Purchasing Analysis (Gender)

# Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# Create a summary data frame to hold the results
# Optional: give the displayed data cleaner formatting
# Display the summary data frame

# Purchases by male players
is_male = purchase_data_pd["Gender"] == "Male"
males_purchases_df = purchase_data_pd[is_male]
males_purchase_count = males_purchases_df.shape[0]
males_avg_purchase_price = males_purchases_df
males_total_spend = round((males_purchases_df["Price"].sum()), 2)
males_avg_spend = round((males_total_spend / males_purchase_count), 2)

# Purchases by female players
is_female = purchase_data_pd["Gender"] == "Female"
females_purchases_df = purchase_data_pd[is_female]
females_purchase_count = females_purchases_df.shape[0]
females_total_spend = round((females_purchases_df["Price"].sum()), 2)
females_avg_spend = round((females_total_spend / females_purchase_count), 2)

# Purchases - Other.Non dislosed
other_non_disclosed_purchase_count = number_of_purchases - (males_purchase_count + females_purchase_count)
other_non_disclosed_total_spend = round((total_revenue - (males_total_spend + females_total_spend)), 2)
other_non_disclosed_avg_spend = round((other_non_disclosed_total_spend / other_non_disclosed_purchase_count), 2)

# Create the dataframe for purchasing data analysis
purchase_by_gender_df = pd.DataFrame({"Gender": ["Male", "Female", "Other / Non-Disclosed"], 
                                    "Purchase Count": [males_purchase_count, females_purchase_count, 
                                                              other_non_disclosed_purchase_count],
                                    "Average Purchase Price": [males_avg_spend, females_avg_spend, other_non_disclosed_avg_spend],
                                    "Total Purchase Value": [males_total_spend, females_total_spend, other_non_disclosed_total_spend]}, 
                               columns = ["Gender", "Purchase Count", "Average Purchase Price", "Total Purchase Value"])

purchase_by_gender_df = purchase_by_gender_df.set_index("Gender")
purchase_by_gender_df

# Format total purchase values
purchase_summary_by_age.style.format({"Average Purchase Price": "${:,.2f}", "Total Purchase Value": "${:,.2f}"})


# In[965]:


# Age Demographics

# Establish bins for ages
# Categorize the existing players using the age bins. Hint: use pd.cut()
# Calculate the numbers and percentages by age group
# Create a summary data frame to hold the results
# Optional: round the percentage column to two decimal points
# Display Age Demographics Table
# Create the bins in which Data will be held

# Create the bins in which Data will be held
age_bins = [0, 9, 14, 19, 24, 29, 34, 39, 46]

# Create the labels for bins
age_groups_lables = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

# Add column of bins based on Age
age_demographic_df["Age Groups"] = pd.cut(gender_dem_df["Age"],age_bins, labels=age_groups_lables)

#Calculate total count and percentage of those counts by age groups
age_groupby = age_demographic_df.groupby("Age Groups")["SN"].nunique().reset_index()
age_groupby["Percentage of Players"] = round((age_groupby["SN"]/age_groupby["SN"].sum() *100), 2) 
age_summary = age_groupby[["Age Groups", "SN", "Percentage of Players"]].sort_values(["Age Groups"])
#age_summary = age_summary.reset_index(drop=True)

# format columns
age_summary["Percentage of Players"] = age_summary["Percentage of Players"].map("{:,.2f}%".format)

# set Indext to Age Groups
age_demos_summary = age_summary.set_index("Age Groups")
age_demos_summary = age_demos_summary.rename(columns = {"SN": "Total Count"}) 
age_demos_summary  


# In[966]:


# Purchasing Analysis (Age)
 
# Run basic calculations to obtain purchase count, avg. purchase price, 
# avg. purchase total per person etc. in the table below
# Create a summary data frame to hold the results
# Optional: give the displayed data cleaner formatting
# Display the summary data frame

# Make a list of purchase counts by age
age_under_10_purchase_count = age_demographic_df[(age_demographic_df["Age"] < 10)].count()[0]
age_10_to_14_purchase_count = age_demographic_df[(age_demographic_df["Age"] >= 10) 
                                                 & (age_demographic_df["Age"] <= 14)].count()[0]
age_15_to_19_purchase_count = age_demographic_df[(age_demographic_df["Age"] >= 15) 
                                                 & (age_demographic_df["Age"] <= 19)].count()[0]
age_20_to_24_purchase_count = age_demographic_df[(age_demographic_df["Age"] >= 20) 
                                                 & (age_demographic_df["Age"] <= 24)].count()[0]
age_25_to_29_purchase_count = age_demographic_df[(age_demographic_df["Age"] >= 25) 
                                                 & (age_demographic_df["Age"] <= 29)].count()[0]
age_30_to_34_purchase_count = age_demographic_df[(age_demographic_df["Age"] >= 30) 
                                                 & (age_demographic_df["Age"] <= 34)].count()[0]
age_35_to_39_purchase_count = age_demographic_df[(age_demographic_df["Age"] >= 35) 
                                                 & (age_demographic_df["Age"] <= 39)].count()[0]
age_over_40_purchase_count  = age_demographic_df[(age_demographic_df["Age"] >= 40)].count()[0]
purchase_count_by_age = [age_under_10_purchase_count, age_10_to_14_purchase_count, age_15_to_19_purchase_count,
                        age_20_to_24_purchase_count, age_25_to_29_purchase_count, age_30_to_34_purchase_count,
                        age_35_to_39_purchase_count, age_over_40_purchase_count]

# Make a list of purchase totals by age
age_under_10_purchase_total = age_demographic_df.loc[age_demographic_df['Age'] < 10, 'Price'].sum()
age_10_to_14_purchase_total = age_demographic_df.loc[(age_demographic_df['Age'] >= 10) 
                                                     & (age_demographic_df['Age'] <=14), 'Price'].sum()
age_15_to_19_purchase_total = age_demographic_df.loc[(age_demographic_df['Age'] >= 15) 
                                                     & (age_demographic_df['Age'] <=19), 'Price'].sum()
age_20_to_24_purchase_total = age_demographic_df.loc[(age_demographic_df['Age'] >= 20) 
                                                     & (age_demographic_df['Age'] <=24), 'Price'].sum()
age_25_to_29_purchase_total = age_demographic_df.loc[(age_demographic_df['Age'] >= 25) 
                                                     & (age_demographic_df['Age'] <=29), 'Price'].sum()
age_30_to_34_purchase_total = age_demographic_df.loc[(age_demographic_df['Age'] >= 30) 
                                                     & (age_demographic_df['Age'] <=34), 'Price'].sum()
age_35_to_39_purchase_total = age_demographic_df.loc[(age_demographic_df['Age'] >= 35) 
                                                     & (age_demographic_df['Age'] <=39), 'Price'].sum()
age_over_40_purchase_total  = age_demographic_df.loc[age_demographic_df['Age'] >= 40, 'Price'].sum() 

purchase_by_age_totals = [age_under_10_purchase_total, age_10_to_14_purchase_total, 
                          age_20_to_24_purchase_total, age_25_to_29_purchase_total,
                          age_15_to_19_purchase_total, age_30_to_34_purchase_total, 
                          age_35_to_39_purchase_total, 
age_over_40_purchase_total]

# Calculate average purchases by age and make a list of it
average_purchase_by_age = [round((age_under_10_purchase_total / age_under_10_purchase_count), 2),
                           round((age_10_to_14_purchase_total / age_10_to_14_purchase_count), 2),
                           round((age_15_to_19_purchase_total / age_15_to_19_purchase_count), 2),
                           round((age_20_to_24_purchase_total / age_20_to_24_purchase_count), 2),
                           round((age_25_to_29_purchase_total / age_25_to_29_purchase_count), 2),
                           round((age_30_to_34_purchase_total / age_30_to_34_purchase_count), 2),
                           round((age_35_to_39_purchase_total / age_35_to_39_purchase_count), 2),
                           round((age_over_40_purchase_total / age_over_40_purchase_count), 2)]

# Create the bins in which Data will be held
age_bins = [0, 9, 14, 19, 24, 29, 34, 39, 46]

# Create the labels for bins
age_groups_lables = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

# Add column of bins based on Age
age_demographic_df["Age Groups"] = pd.cut(gender_dem_df["Age"],age_bins, labels=age_groups_lables)

# Put the values in bins defined above
age_groupby = age_demographic_df.groupby("Age Groups")["SN"].nunique().reset_index()
age_groupby["Purchase Count"] = purchase_count_by_age 
age_groupby["Average Purchase Price"] = average_purchase_by_age
age_groupby["Total Purchase Value"] = purchase_by_age_totals
 
purchase_summary_by_age = age_groupby[["Age Groups", "Purchase Count",
                                       "Average Purchase Price", 
                                       "Total Purchase Value"]].sort_values(["Age Groups"])
purchase_summary_by_age = purchase_summary_by_age.reset_index(drop=True)

# set Indext to Age Groups
purchase_summary_by_age = purchase_summary_by_age.set_index("Age Groups")
purchase_summary_by_age

# Formatting prices and total purhcase values
purchase_summary_by_age.style.format({"Average Purchase Price": "${:.2f}", "Total Purchase Value": "${:,.2f}"})


# In[967]:


# Top Spenders
 
# Run basic calculations to obtain the results in the table below
# Create a summary data frame to hold the results
# Sort the total purchase value column in descending order
# Optional: give the displayed data cleaner formatting
# Display a preview of the summary data frame

top_spenders_df = age_demographic_df[["SN","Price","Item Name"]]
total_spent = top_spenders_df.groupby("SN").sum()
total_spent.sort_values(by = "Price", ascending = False, inplace = True)

# Get top 5 spenders names and make a list
top_spenders_names = list(total_spent.index.values)
top_names = [names[0], names[1], names[2], names[3], names[4]]

# Get top 5 spenders purchase values and make a list
total_purchase_values_0 = total_spent.iloc[0,0]
total_purchase_values_1 = total_spent.iloc[1,0]
total_purchase_values_2 = total_spent.iloc[2,0]
total_purchase_values_3 = total_spent.iloc[3,0]
total_purchase_values_4 = total_spent.iloc[4,0]
top_purchase_values = [total_spent.iloc[0,0], total_spent.iloc[1,0], total_spent.iloc[2,0], total_spent.iloc[3,0],
                      total_spent.iloc[4,0]]

# Get top 5 spenders nummber of purchased and make a list
top_purchase_counts_0 = top_spenders_df[top_spenders_df["SN"] == top_names[0]].count()[0]
top_purchase_counts_1 = top_spenders_df[top_spenders_df["SN"] == top_names[1]].count()[0]
top_purchase_counts_2 = top_spenders_df[top_spenders_df["SN"] == top_names[2]].count()[0]
top_purchase_counts_3 = top_spenders_df[top_spenders_df["SN"] == top_names[3]].count()[0]
top_purchase_counts_4 = top_spenders_df[top_spenders_df["SN"] == top_names[4]].count()[0]
top_purchase_counts = [top_purchase_counts_0, top_purchase_counts_1, top_purchase_counts_2, top_purchase_counts_3,
                       top_purchase_counts_4]

# Calculate average prices for the top spenders and male a list
avg_price_0 = total_purchase_values_0 / top_purchase_counts_0
avg_price_1 = total_purchase_values_1 / top_purchase_counts_1
avg_price_2 = total_purchase_values_2 / top_purchase_counts_2
avg_price_3 = total_purchase_values_3 / top_purchase_counts_3
avg_price_4 = total_purchase_values_4 / top_purchase_counts_4
avg_prices = [avg_price_0, avg_price_1, avg_price_2, avg_price_3, avg_price_4]

# Create the dictionary for transfer to dataframe later
top_spenders_dict = ({"Purchase Count": top_purchase_counts,
                    "Average Purchase Price": avg_prices,
                    "Total Purchase Value": top_purchase_values,
                    "SN": top_names})

## Put it all in a data frame
top_spenders_df = pd.DataFrame(top_spenders_dict)
top_spenders_df = top_spenders_df.set_index("SN")
top_spenders_df = top_spenders_df[["Purchase Count", "Average Purchase Price", "Total Purchase Value"]]

# Formatting prices
top_spenders_df.style.format({"Average Purchase Price": "${:.2f}", "Total Purchase Value": "${:.2f}"})


# In[968]:


# Most Popular sellers - top sellers
 
# Retrieve the Item ID, Item Name, and Item Price columns
# Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# Create a summary data frame to hold the results
# Sort the purchase count column in descending order
# Optional: give the displayed data cleaner formatting
# Display a preview of the summary data frame

top_sellers_df = age_demographic_df[["Item ID", "Item Name", "Price"]]
top_sellers = top_sellers_df.groupby("Item ID").count()
top_sellers.sort_values(by = "Item Name", ascending = False, inplace = True)
top_sellers_df = top_sellers_df.drop_duplicates(["Item ID", "Item Name"])

# Get the list of top sellers names
top_sellers_ids = [top_sellers.index[0], top_sellers.index[1], top_sellers.index[2], 
                   top_sellers.index[3], top_sellers.index[4]]

# Build the top sellers list of names
top_sellers_name_0 = top_sellers_df.loc[top_sellers_df["Item ID"] == top_sellers_ids[0], "Item Name"].item()
top_sellers_name_1 = top_sellers_df.loc[top_sellers_df["Item ID"] == top_sellers_ids[1], "Item Name"].item()
top_sellers_name_2 = top_sellers_df.loc[top_sellers_df["Item ID"] == top_sellers_ids[2], "Item Name"].item()
top_sellers_name_3 = top_sellers_df.loc[top_sellers_df["Item ID"] == top_sellers_ids[3], "Item Name"].item()
top_sellers_name_4 = top_sellers_df.loc[top_sellers_df["Item ID"] == top_sellers_ids[4], "Item Name"].item()
top_sellers_names  = [top_item_name_0, top_item_name_1, top_item_name_2, top_item_name_3, top_item_name_4]

# build the top sellers list of prices
top_sellers_price_0 = top_sellers_df.loc[top_sellers_df["Item Name"] == top_sellers_names[0], "Price"].item()
top_sellers_price_1 = top_sellers_df.loc[top_sellers_df["Item Name"] == top_sellers_names[1], "Price"].item()
top_sellers_price_2 = top_sellers_df.loc[top_sellers_df["Item Name"] == top_sellers_names[2], "Price"].item()
top_sellers_price_3 = top_sellers_df.loc[top_sellers_df["Item Name"] == top_sellers_names[3], "Price"].item()
top_sellers_price_4 = top_sellers_df.loc[top_sellers_df["Item Name"] == top_sellers_names[4], "Price"].item()
top_sellers_prices  = [top_sellers_price_0, top_sellers_price_1, top_sellers_price_2, top_sellers_price_3,top_sellers_price_4]

# get the list of top sellers purchase ounts
top_sellers_counts = [top_sellers.iloc[0,0], top_sellers.iloc[1,0], top_sellers.iloc[2,0],
                   top_sellers.iloc[3,0], top_sellers.iloc[4,0]]

# Make a list of calculated total values for top sellers
top_sellers_total_values = [(top_sellers.iloc[0,0] * top_sellers_price_0), (top_sellers.iloc[1,0] * top_sellers_price_1), 
                          (top_sellers.iloc[2,0] * top_sellers_price_2), (top_sellers.iloc[3,0] * top_sellers_price_3), 
                          (top_sellers.iloc[4,0] * top_sellers_price_4)]

# Create the dictionary for transfer to dataframe later
top_sellers_dict = {
    "Item ID": top_sellers_ids,
    "Item Name": top_sellers_names,
    "Purchase Count": top_sellers_counts,
    "Item Price": top_sellers_prices,
    "Total Purchase Value": top_sellers_counts,
    "SN": top_names}

# Put it all in a data frame
top_sellers_df = pd.DataFrame(top_sellers_dict)
#top_sellers_df = top_sellers_df.set_index("SN")
top_sellers_df = top_sellers_df[["Item ID", "Item Name", "Purchase Count", "Item Price", "Total Purchase Value"]]
top_sellers_df = top_sellers_df.set_index("Item ID")

# Formatting prices
top_sellers_df.style.format({"Item Price": "${:.2f}", "Total Purchase Value": "${:.2f}"})


# In[969]:


# Most Profitable Items
 
# Sort the above table by total purchase value in descending order
# Optional: give the displayed data cleaner formatting
# Display a preview of the data frame

most_profitable_df = age_demographic_df[["Item ID","Item Name", "Price"]]
most_profitable = most_profitable_df.groupby("Item ID").sum()
most_profitable.sort_values(by = "Price", ascending = False, inplace = True)
most_profitable_df = most_profitable_df.drop_duplicates(["Item ID", "Price"])

# Item IDs
most_profitable_ids = [most_profitable.index[0], most_profitable.index[1], most_profitable.index[2],
            most_profitable.index[3], most_profitable.index[4]]

# Build the top sellers list of names
most_profitable_name_0 = most_profitable_df.loc[most_profitable_df["Item ID"] == most_profitable_ids[0], "Item Name"].item()
most_profitable_name_1 = most_profitable_df.loc[most_profitable_df["Item ID"] == most_profitable_ids[1], "Item Name"].item()
most_profitable_name_2 = most_profitable_df.loc[most_profitable_df["Item ID"] == most_profitable_ids[2], "Item Name"].item()
most_profitable_name_3 = most_profitable_df.loc[most_profitable_df["Item ID"] == most_profitable_ids[3], "Item Name"].item()
most_profitable_name_4 = most_profitable_df.loc[most_profitable_df["Item ID"] == most_profitable_ids[4], "Item Name"].item()
most_profitable_names  = [top_item_name_0, top_item_name_1, top_item_name_2, top_item_name_3, top_item_name_4]

# build the top sellers list of prices
most_profitable_price_0 = most_profitable_df.loc[most_profitable_df["Item ID"] == most_profitable_ids[0], "Price"].item()
most_profitable_price_1 = most_profitable_df.loc[most_profitable_df["Item ID"] == most_profitable_ids[1], "Price"].item()
most_profitable_price_2 = most_profitable_df.loc[most_profitable_df["Item ID"] == most_profitable_ids[2], "Price"].item()
most_profitable_price_3 = most_profitable_df.loc[most_profitable_df["Item ID"] == most_profitable_ids[3], "Price"].item()
most_profitable_price_4 = most_profitable_df.loc[most_profitable_df["Item ID"] == most_profitable_ids[4], "Price"].item()
most_profitable_prices  = [most_profitable_price_0, most_profitable_price_1, most_profitable_price_2,
                           most_profitable_price_3,most_profitable_price_4]

# Build the list of purchase counts
most_profitable_df = age_demographic_df[["Item ID", "Item Name", "Price"]].groupby("Item Name").count()

most_profitable_count_0 = most_profitable_count_df.loc[most_profitable_df.index == most_profitable_names[0], "Item ID"].item()
most_profitable_count_1 = most_profitable_count_df.loc[most_profitable_df.index == most_profitable_names[1], "Item ID"].item()
most_profitable_count_2 = most_profitable_count_df.loc[most_profitable_df.index == most_profitable_names[2], "Item ID"].item()
most_profitable_count_3 = most_profitable_count_df.loc[most_profitable_df.index == most_profitable_names[3], "Item ID"].item()
most_profitable_count_4 = most_profitable_count_df.loc[most_profitable_df.index == most_profitable_names[4], "Item ID"].item()
most_profitable_counts = [most_profitable_count_0, most_profitable_count_1, most_profitable_count_2,
                          most_profitable_count_3, most_profitable_count_4]

# Make a list of calculated total values for top sellers
most_profitable_total_values = [(most_profitable.iloc[0,0] * most_profitable_price_0), (most_profitable.iloc[1,0] * most_profitable_price_1), 
                                (most_profitable.iloc[2,0] * most_profitable_price_2), (most_profitable.iloc[3,0] * most_profitable_price_3), 
                                (most_profitable.iloc[4,0] * most_profitable_price_4)]


# Create the dictionary for transfer to dataframe later
most_profitable_dict = {"Item ID": most_profitable_ids,
                       "Item Name": most_profitable_names,
                       "Purchase Count": most_profitable_counts,
                       "Item Price": most_profitable_prices,
                       "Total Purchase Value": most_profitable_counts,
                      "SN": top_names}

# Put it all in a data frame
most_profitable_df = pd.DataFrame(most_profitable_dict)
most_profitable_df = most_profitable_df.set_index(["Item ID", "Item Name"])
most_profitable_df = most_profitable_df[["Purchase Count", "Item Price", "Total Purchase Value"]]

# Formatting prices
most_profitable_df.style.format({"Item Price": "${:.2f}", "Total Purchase Value": "${:.2f}"})


# In[970]:


get_ipython().system('jupyter nbconvert --to script Heroes-of-Pymoli.ipynb')

