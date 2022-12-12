# Databricks notebook source
import pandas as pd

# COMMAND ----------

# MAGIC %md
# MAGIC #Import from git

# COMMAND ----------

# MAGIC %md
# MAGIC ## Vaccines

# COMMAND ----------

url_data = (r'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv')

data_csv_vaccines = pd.read_csv(url_data)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Hospitalization

# COMMAND ----------

url_data_hospitalization = (r'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/hospitalizations/covid-hospitalizations.csv')

data_csv_hospitalization = pd.read_csv(url_data_hospitalization)

# COMMAND ----------

# MAGIC %md
# MAGIC #Data Exploration

# COMMAND ----------

import matplotlib.pyplot as plt
import seaborn as sns

# COMMAND ----------

# MAGIC %md
# MAGIC ## Vaccines

# COMMAND ----------

data_csv_vaccines.head()

# COMMAND ----------

data_csv_vaccines.describe().T

# COMMAND ----------

data_csv_vaccines.columns

# COMMAND ----------

data_csv_vaccines.info()

# COMMAND ----------

data_csv_vaccines.dtypes

# COMMAND ----------

# Verificando dados nulos
data_csv_vaccines.isna().sum()

# COMMAND ----------

data_csv_vaccines.isnull().sum().sort_values(ascending=False).head()

# COMMAND ----------

for col_name in data_csv_vaccines.columns:
    if data_csv_vaccines[col_name].dtypes == 'object':
        unique_cat = len(data_csv_vaccines[col_name].unique())
        print("Feature '{col_name}' has {unique_cat} unique   categories".format(col_name=col_name, unique_cat=unique_cat))

# COMMAND ----------

categorical_attributes = list(data_csv_vaccines.select_dtypes(include=['object']).columns)
numerical_attributes = list(data_csv_vaccines.select_dtypes(include=['float64', 'int64']).columns)
print('categorical_attributes:', categorical_attributes)
print('numerical_attributes:', numerical_attributes)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Hospitalization

# COMMAND ----------

data_csv_hospitalization.head()

# COMMAND ----------

data_csv_hospitalization.describe().T

# COMMAND ----------

data_csv_hospitalization.columns

# COMMAND ----------

data_csv_hospitalization.info()

# COMMAND ----------

data_csv_hospitalization.dtypes

# COMMAND ----------

data_csv_hospitalization.isna().sum()

# COMMAND ----------

data_csv_hospitalization.isnull().sum().sort_values(ascending=False).head()

# COMMAND ----------

for col_name in data_csv_hospitalization.columns:
    if data_csv_hospitalization[col_name].dtypes == 'object':
        unique_cat = len(data_csv_hospitalization[col_name].unique())
        print("Feature '{col_name}' has {unique_cat} unique   categories".format(col_name=col_name, unique_cat=unique_cat))

# COMMAND ----------

categorical_attributes = list(data_csv_hospitalization.select_dtypes(include=['object']).columns)
numerical_attributes = list(data_csv_hospitalization.select_dtypes(include=['float64', 'int64']).columns)
print('categorical_attributes:', categorical_attributes)
print('numerical_attributes:', numerical_attributes)

# COMMAND ----------

# MAGIC %md
# MAGIC # Some agregations on data

# COMMAND ----------

# MAGIC %md
# MAGIC ## Vaccination

# COMMAND ----------

vaccinesPerCountry = pd.DataFrame(data_csv_vaccines.sort_values('date').groupby("location")['people_vaccinated_per_hundred'].last().reset_index(name ='People vaccinated per hundred'))
vaccinesPerCountry.head()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Hospitalization

# COMMAND ----------

data_csv_hospitalization = data_csv_hospitalization.loc[data_csv_hospitalization['indicator'] == 'Daily ICU occupancy per million']
data_csv_hospitalization = data_csv_hospitalization.loc[data_csv_hospitalization['date'] > '2022-06-01']


# COMMAND ----------

hospitalizationPerCountry = pd.DataFrame(data_csv_hospitalization.sort_values('date').groupby("entity")['value'].mean().reset_index(name ='Hospitalization per milion'))
hospitalizationPerCountry.rename(columns = {'entity' : 'location'}, inplace = True)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Hospitalization and Vaccination

# COMMAND ----------

covidPerCountry = pd.merge(vaccinesPerCountry, hospitalizationPerCountry, on='location', how='inner')

# COMMAND ----------

# MAGIC %md
# MAGIC #Visualization

# COMMAND ----------

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(12,12)) 
sns.heatmap(data=covidPerCountry.corr(),annot=True,linewidths=0.2,cmap='coolwarm', square=True);
