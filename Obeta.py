#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib 
import scipy
import matplotlib.pyplot as plt


# ## Importing product data 

# In[2]:


# product data
header = ["sku","desc","group"]
d_type = {"sku":"str","desc":"str","group":"str"}
product = pd.read_csv('002 product_data.csv', encoding='latin-1', sep=',', index_col=False, header=None, names=header,
                  dtype=d_type)


# In[3]:


print(product.describe())


# In[4]:


print(product.info())


# In[5]:


print(product.head())


# In[6]:


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

# In[8]:


# pick data
headers = ["sku", "warehouse", "origin", "order_id", "order_position","pick_volume","order_quantity","date"]
dtypes = {'sku': 'str', 'warehouse': 'str', 'origin': 'category', 'order_id': 'str', "order_position":"str",
          "pick_volume":"int", "order_quantity":"category", "date":"str"}
parse_dates = ['date']
pick = pd.read_csv('003 pick_data.csv', encoding='latin-1', sep=',', index_col=False, header=None, names=headers,
                  dtype=dtypes, parse_dates=parse_dates)


# In[9]:


print(pick.info())


# In[10]:


print(pick.describe())


# In[11]:


print(pick.head())


# In[ ]:


# Merging data on sku


# In[12]:


merge = pick.merge(product, on="sku")


# In[13]:


print(merge.info())


# In[14]:


print(merge.describe())


# In[15]:


print(merge.head())


# ## Missing Values

# In[16]:


print(product.isna().sum())


# In[17]:


missing = product[product["desc"].isna()]
print(missing.describe())


# In[18]:


for col in product.columns:
    pct_missing = np.mean(product[col].isnull())
    print('{} - {}%'.format(col, round(pct_missing*100)))


# In[19]:


print(pick.isna().sum())


# In[20]:


print(merge.isna().sum())


# ## Duplicate Values

# In[21]:


duplicates = product.duplicated()
print(product[duplicates])


# In[22]:


duplicates1 = pick.duplicated()
print(pick[duplicates1])


# In[23]:


duplicates2 = merge.duplicated()
print(merge[duplicates2])


# In[ ]:


# Droping duplicates in merged dataframe


# In[24]:


clean = merge.drop_duplicates()


# In[25]:


print(clean.describe())


# In[26]:


print(clean.info())


# In[27]:


# To check if character removing worked. If noting is returned, it worked. Otherwise some error will be returned 
assert clean["group"].str.contains("ä").any() == False
assert clean["group"].str.contains("ö").any() == False
assert clean["group"].str.contains("ü").any() == False
assert clean["desc"].str.contains("ä").any() == False
assert clean["desc"].str.contains("ö").any() == False
assert clean["desc"].str.contains("ü").any() == False


# ## Outliers

# In[28]:


# Removing outliers
o1 = clean[clean["pick_volume"] <= 1156]
o2 = o1[o1["pick_volume"] >= -1033]
print(o2.info())
# o1 is dataframe with values below 1156
# o2 is dataframe with values below 1156 and above -1033 ie dataframe without outliers


# In[29]:


print(o2.describe())


# In[30]:


# percentage of lost data
print(100-(33683707/33888987*100))


# In[31]:


# Setting outliers within range
clean.loc[clean["pick_volume"] > 1156,"pick_volume"]=1156
clean.loc[clean["pick_volume"] < -1033,"pick_volume"]=-1033


# In[32]:


print(clean.describe())


# In[38]:


# seperating columns by day, date and time
clean['Time'] = pd.to_datetime(clean['date']).dt.time
clean['Date'] = pd.to_datetime(clean['date']).dt.date
clean['Day'] = pd.to_datetime(clean['date']).dt.day
clean['Month'] = pd.to_datetime(clean['date']).dt.month
clean['Year'] = pd.to_datetime(clean['date']).dt.year


# In[39]:


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


# In[ ]:


print(df)


# In[53]:


print(df.mean())


# In[54]:


# Exporting data for pareto experiment
#df.to_csv('C:/Users/Rashmi Dsouza/Desktop/Obeta warehouse/AVG_pick.csv')


# In[ ]:


#fig,ax = plt.subplots()
#ax.plot(df.index,df['pick_volume'])


# In[ ]:




