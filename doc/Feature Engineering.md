# Data Preprocessing and Feature Engineering Steps

Below are the results of data exploration and details of the features with relation to other features and how to handle them. We categorize features based on having null/missing values and how to handle them, categorical features and how to encode them and features that need standardization or normalization.

## 1. Data Cleaning:

### Handle Nulls: Impute or remove null values where feasible to ensure all features are usable.
In this dataset there are two types of null values: missing values and 0 values that are not counted as missing but in context they are missing values.

#### Missing Values (0s that are not counted as missing values):

 - population: 21381 rows
 - construction_year: 20302
 - water_quality, quality_group: unknown as value
 
 - gps_height: 20438
 - latitude & longtitude: 1812 
```
Latitude and Longtitude have 0 values for the following features:
region_code: (11(3), 17(1057) and 19(752) and
district_code (1(1057), 2(264) and 6(488))) 
```
- Num_private: 58643 (Can be dropped as over 90% are 0s)
- **amount_tsh: 41639** (The 0s here don't seem to be showing missing values, just shows the feature is not relevant, so might not need imputation or dropping, probably only encoding could be better.)

#### Convert Categoricals: Convert categorical columns (e.g., 'scheme_management') into numerical encodings using label/one-hot techniques.
  - Recorded_by has only one value for all and doesn't add anything to data, so can be dropped
  - Region and Region_code are the same, we could use Region_code for machine learning and drop Region then
  - quantity has a duplicate quantity_group, one needs to be dropped.
  - waterpoint_type and waterpoint_type_group are very similar, waterpoint_type_group can be kept as the other has duplicate values.
  - extraction_type and extraction_type_group are also very similar
  - water_quality and quality_group are also similar
  - payment and payment_type are exactly the same


#### Data Transformation:

#### Standardize/Normalize: Apply standardization on location coordinates and static head (amount_tsh) to scale their values appropriately.

#### Datetime Handling: Convert 'date_recorded' to a datetime format or extract year/month for use in models.

#### Feature Selection:

#### Prioritize Features: Use correlation analysis and feature selection techniques to identify the most important predictors of pump functionality, focusing on variables like water quality, management structure, and technical specs.

#### Class Balancing:

#### Assess class distribution of 'status_group'. If imbalance exists, apply re-sampling techniques (e.g., SMOTE, Over-sampling) to ensure balanced learning.

#### Model Selection:

Choose models suited for handling both numerical and categorical features, such as random forest or gradient boosting, ensuring all features are appropriately encoded.

----------------------------------------------------------------
Details of some features to better understand them.
### 1. amont_tsh:
Total static head (amount of water available to waterpoint).
But in water engineering terms, __"total static head" (TSH)__ usually refers to:

The __vertical distance__ (in meters) from the water source (like a well or borehole) to the __discharge point__ (where water comes out).
So in theory, it represents the __energy or pressure needed to get water from the source to the surface__. It isn’t a measure of volume but more like a technical specification.

##### 🧠 Interpreting amount_tsh = 0 in Context
🕳️ Water Source:

- __Shallow well, spring, borehole__ are all __gravity-fed__ or __surface-close sources__.
  - These don’t typically require mechanical pressure, water often rises naturally or needs minimal lifting.

##### 🏗️ Extraction Type Group:

- __Hand pump, gravity:__
  - Hand pumps don't use measured pressure or "static head" in the same way mechanical/electric pumps do.
  - Gravity systems don't need "lifting" power — the water flows naturally due to elevation differences.

##### 🚰 Waterpoint Type:

- __Communal standpipe, hand pump:__
  - These are simple, low-tech systems that may not require or track amount_tsh at all.
    
🧩 __What This All Suggests?__
The fact that 0 amount_tsh is strongly associated with:

- Simple, low-tech systems
- Gravity-fed or surface-close sources
- Manual operation

This flips the interpretation: _amount_tsh = 0 doesn't mean "data missing" — it often means "no measurable static head needed" or it's just not applicable._

```
amount_tsh = 0: 41,639 rows → majority
amount_tsh > 0: ~17,761 rows → minority, but significant enough to keep as numeric range of non-zero values goes up to 350,000
```
__How to handle?__
- 1. Use It as a Continuous Feature

- But log-transform it — this kind of data is usually very skewed (long tail with a few huge values like 350,000).
import numpy as np
```
df['amount_tsh_log'] = df['amount_tsh'].replace(0, 1)  # avoid log(0)
df['amount_tsh_log'] = np.log(df['amount_tsh_log'])
```
- This transformation makes the distribution more normal
- Keeps relative differences (e.g. 1000 is more than 10, but now on a compressed scale)
2. Still Keep a Binary Indicator

Because amount_tsh = 0 could still signal low-tech systems, which could affect pump reliability differently.
```
df['has_static_head'] = (df['amount_tsh'] > 0).astype(int)
```
🎯 __Why This Dual Approach Helps__
```
Feature	Meaning	Use in model
has_static_head	Whether the pump is gravity/manual	Categorical (0/1)
amount_tsh_log	Intensity/scale of water pressure	Continuous (log scale)
```

This lets the model:
- Learn differences between manual vs mechanical
- Also consider how powerful/heavy-duty the system is


# 2. construction_year

- __Problem:__ 20,709 out of 59,400 are 0 → effectively missing (~35%)
- 0 is not a real year → needs to be treated as missing
- When valid, it can be used to calculate pump_age: 
```
# Mark 0s as NaN for construction_year
df['construction_year'] = df['construction_year'].replace(0, np.nan)

# Extract year from date_recorded
df['recorded_year'] = pd.to_datetime(df['date_recorded']).dt.year

# Compute age (where we have data)
df['pump_age'] = df['recorded_year'] - df['construction_year']
```
__What to do with missing pump_age?__

- Option 1: Impute (e.g. median pump_age by region or waterpoint_type)
- Option 2: Add a binary flag missing_age
- Option 3: Leave as NaN if the model handles it (e.g. XGBoost, CatBoost)

# 3. 
