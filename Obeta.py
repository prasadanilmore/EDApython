#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib 
import scipy
import matplotlib.pyplot as plt
import statistics


# ## Importing product data 


# product data
header = ["sku","desc","group"]
d_type = {"sku":"str","desc":"str","group":"str"}
product = pd.read_csv('002 product_data.csv', encoding='latin-1', sep=',', index_col=False, header=None, names=header,
                  dtype=d_type)


print(product.describe())


print(product.info())


print(product.head())



# Removing german characters
product["group"] = product["group"].str.replace("ä","a")
product["group"] = product["group"].str.replace("ö","o")
product["group"] = product["group"].str.replace("ü","u")
product["desc"] = product["desc"].str.replace("ä","a")
product["desc"] = product["desc"].str.replace("ö","o")
product["desc"] = product["desc"].str.replace("ü","u")


# In[7]:


print(product.head())


# ## Importing pick data


# pick data
headers = ["sku", "warehouse", "origin", "order_id", "order_position","pick_volume","order_quantity","date"]
dtypes = {'sku': 'str', 'warehouse': 'str', 'origin': 'category', 'order_id': 'str', "order_position":"str",
          "pick_volume":"int", "order_quantity":"category", "date":"str"}
parse_dates = ['date']
pick = pd.read_csv('003 pick_data.csv', encoding='latin-1', sep=',', index_col=False, header=None, names=headers,
                  dtype=dtypes, parse_dates=parse_dates


print(pick.info())


print(pick.describe())


print(pick.head())


# Merging data on sku


merge = pick.merge(product, on="sku")


# In[13]:


print(merge.info())


# In[14]:


print(merge.describe())


print(merge.head())


# ## Missing Values

print(product.isna().sum())



missing = product[product["desc"].isna()]
print(missing.describe())


for col in product.columns:
    pct_missing = np.mean(product[col].isnull())
    print('{} - {}%'.format(col, round(pct_missing*100)))


print(pick.isna().sum())



print(merge.isna().sum())


# ## Duplicate Value


duplicates = product.duplicated()
print(product[duplicates])


duplicates1 = pick.duplicated()
print(pick[duplicates1])


duplicates2 = merge.duplicated()
print(merge[duplicates2])


# Droping duplicates in merged dataframe


clean = merge.drop_duplicates()


print(clean.describe())

print(clean.info())


# To check if character removing worked. If noting is returned, it worked. Otherwise some error will be returned 
assert clean["group"].str.contains("ä").any() == False
assert clean["group"].str.contains("ö").any() == False
assert clean["group"].str.contains("ü").any() == False
assert clean["desc"].str.contains("ä").any() == False
assert clean["desc"].str.contains("ö").any() == False
assert clean["desc"].str.contains("ü").any() == False


# ## Outliers


# Removing outliers
mean = statistics.mean(list)
std_dev = statistics.stdev(list)
pos_outliers = mean + 3*std_dev
neg_outliers = mean - 3*std_dev

# outliers are above 1156 and below - 1033 in this dataset
o1 = clean[clean["pick_volume"] >= 1156]
o2 = o1[o1["pick_volume"] <= -1033]
print(o2.info())
# o1 is dataframe with values above 1156
# o2 is dataframe with values below -1033

print(o2.describe())

# percentage of lost data
print(100-(33683707/33888987*100))


# In[31]:


# Setting outliers within range
clean.loc[clean["pick_volume"] > 1156,"pick_volume"]=1156
clean.loc[clean["pick_volume"] < -1033,"pick_volume"]=-1033



print(clean.describe())


# seperating columns by day, date and time
clean['Time'] = pd.to_datetime(clean['date']).dt.time
clean['Date'] = pd.to_datetime(clean['date']).dt.date
clean['Day'] = pd.to_datetime(clean['date']).dt.day
clean['Month'] = pd.to_datetime(clean['date']).dt.month
clean['Year'] = pd.to_datetime(clean['date']).dt.year


# grouping data for parteto experiment
(clean.groupby("order_id")["pick_volume"].mean())


# In[40]:


print(clean.info())


# In[41]:


# exproting data
#clean.to_csv('C:/Users/Rashmi Dsouza/Desktop/Obeta warehouse/Obeta_clean.csv')


# In[ ]:


# grouping data for parteto experiment
data = clean.groupby("order_id")["pick_volume"]


# In[ ]:


df = pd.DataFrame(data)


print(df.mean())



fig,ax = plt.subplots()
ax.plot(df.index,df['pick_volume'])





