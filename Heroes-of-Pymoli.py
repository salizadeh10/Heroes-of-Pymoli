
# coding: utf-8

# In[121]:


# Dependencies and Setup
import pandas as pd
import numpy as np


# In[122]:


# Load the file
dataFile = "purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data_pd = pd.read_csv(dataFile)


# In[123]:


purchase_data_pd.head()


# In[124]:


player_count = len(purchase_data_pd["SN"].value_counts())
print("Total Number of Players: " + str(player_count))


# In[125]:


# Purchasing Analysis (Total)
# Run basic calculations to obtain number of unique items, average price, etc.
# Create a summary data frame to hold the results
# Optional: give the displayed data cleaner formatting
# Display the summary data frame


# In[126]:


# get number of unique purchases
unique_items = len(purchase_data_pd["Item ID"].value_counts())
print("Number of unique purchase items: " + str(unique_items))


# In[127]:


# get the average price of items
avg_price = round(purchase_data_pd["Price"].mean(), 2)
print("Average price of items is: " + str(avg_price))


# In[128]:


# get number of purchased 
number_of_purchases = len(purchase_data_pd["Purchase ID"].value_counts())
print("Number of items purchased: " + str(number_of_purchases))


# In[129]:


# total revenue generated from sales
total_revenue = purchase_data_pd["Price"].sum()
print("Total revenue is: " + str(total_revenue))


# In[130]:


# Create dataframe for number of items, avg sale price, number of purchases, and total revenue

purchase_summary = []
purchase_summary.append(unique_items)
purchase_summary.append("$" + str(avg_price))
purchase_summary.append(number_of_purchases)
purchase_summary.append("$" + str(total_revenue))

purchase_df = pd.DataFrame([purchase_summary], columns = ["Number of Unique Items", "Average Price", 
                                            "Number of Purchases", "Total Revenue"])
purchase_df.head()


# In[131]:


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
demographics_df = pd.DataFrame({"Gender": ["Male", "Female", "Other / Non-Disclosed"], "Percentage of Players": 
                                [males_percentage, females_percentage, other_non_disclosed_percentage],
                                        "Total Count": [males_count, females_count, other_non_disclosed_count]}, 
                               columns = ["Gender", "Percentage of Players", "Total Count"])

demographics_df = demographics_df.set_index("Gender")
demographics_df.style.format({"Percentage of Players": "{:.2f}%"})  


# In[132]:


# Purchasing Analysis (Gender)
# Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# Create a summary data frame to hold the results
# Optional: give the displayed data cleaner formatting
# Display the summary data frame


# In[133]:


# Purchase counts by Gender column

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
purchase_analysis_df = pd.DataFrame({"Gender": ["Male", "Female", "Other / Non-Disclosed"], 
                                    "Purchase Count": [males_purchase_count, females_purchase_count, 
                                                              other_non_disclosed_purchase_count],
                                    "Average Purchase Price": [males_avg_spend, females_avg_spend, other_non_disclosed_avg_spend],
                                    "Total Purchase Value": [males_total_spend, females_total_spend, other_non_disclosed_total_spend]}, 
                               columns = ["Gender", "Purchase Count", "Average Purchase Price", "Total Purchase Value"])

purchase_analysis_df = purchase_analysis_df.set_index("Gender")
purchase_analysis_df


# In[134]:


# Age Demographics
# Establish bins for ages
# Categorize the existing players using the age bins. Hint: use pd.cut()
# Calculate the numbers and percentages by age group
# Create a summary data frame to hold the results
# Optional: round the percentage column to two decimal points
# Display Age Demographics Table


# In[138]:


# Create the bins in which Data will be held
# Age bins are 0, 10, 15, 19, 25, 30, 35, 40
age_bins = [0, 9, 14, 19, 24, 29, 34, 39, 44]

# Create the labels for bins
age_groups_lables = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

# Add column of bins based on Age
age_demographic_df = gender_dem_df
age_demographic_df["Age Groups"] = pd.cut(gender_dem_df["Age"],age_bins, labels=age_groups_lables)


#Calculate total count and percentage of those counts by age groups
age_groupby = age_demographic_df.groupby('Age Groups')['SN'].nunique().reset_index()
age_groupby["Percentage of Players"] = 100 * age_groupby["SN"]/age_groupby["SN"].sum()
age_summary = age_groupby[["Age Groups", "Percentage of Players", "SN" ]].sort_values(["Age Groups"])
age_summary = age_summary.reset_index(drop=True)

# format columns
age_summary["Percentage of Players"] = age_summary["Percentage of Players"].map("{:,.2f}".format)

# set Indext to Age Groups
age_demos_summary = age_summary.set_index("Age Groups")
age_demos_summary = age_demos_summary.rename(columns = {"SN": "Total Count"}) 
age_demos_summary


# In[101]:


get_ipython().system('jupyter nbconvert --to script Heroes-of-Pymoli.ipynb')

