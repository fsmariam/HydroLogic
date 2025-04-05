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

