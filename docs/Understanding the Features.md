# Understanding the Features

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


### 2. construction_year

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
