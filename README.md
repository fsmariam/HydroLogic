# HydroLogic
A machine learning project to predict the functionality status of water pumps across Tanzania based on a variety of features including location, water quality, management structure, and technical specifications. It addresses a critical infrastructure challenge: identifying which water pumps are functional, need repairs, and are non-functional.

## Introduction
Access to clean and reliable water is fundamental to public health and socio-economic development. In Tanzania, ensuring sustainable water supply and sanitation services is a priority aligned with global initiatives like the Sustainable Development Goals (SDGs), particularly SDG 6, which emphasizes the availability and sustainable management of water and sanitation for all. The Ministry of Water has developed comprehensive guidelines, such as the Design, Construction, Supervision, Operation, and Maintenance (DCOM) manual, to support the planning and implementation of water supply projects across the country. 

## Problem Statement
Despite significant efforts, many communities in Tanzania still face challenges with non-functional or partially functional water pumps, leading to inconsistent access to clean water. Factors contributing to this issue include inadequate maintenance, environmental conditions, and technical failures. Addressing these challenges requires a systematic approach to predict and monitor water pump functionality, enabling timely interventions and resource allocation.

## Project Goal
The primary objective of this project is to develop machine learning models capable of predicting the functionality status of water pumps across Tanzania. By analyzing various factors such as location, water quality, management structures, and technical specifications, the project aims to identify which pumps are functional, which require repairs, and which are non-functional. This predictive capability will enhance maintenance operations, ensure better resource distribution, and ultimately improve access to clean water for communities.


## 📌 Naming Conventions  

Choose a consistent naming style that is self explanatory.
To ensure consistency, follow these naming conventions:  

### 1. **Variable & Function Names**  

```
Naming Style     Example               Use Case

snake_case      train_model()          ✅ Python functions, variables
PascalCase      WaterPumpClassifier    ✅ Class names
camelCase       getData()              ❌ Avoid in Python, used in JavaScript
```
✅ Recommended: Descriptive names that are self explanatory.

- Use **`snake_case`** for variable and function names:  
  ```python
  def preprocess_data():
      cleaned_data = remove_null_values(raw_data)
      return cleaned_data

- Use **`PascalCase`** for class names:
  ```python
  class WaterPumpClassifier:
    def train(self):
        pass
  ```
   
❌ Avoid using single-letter names or vague terms:

__Bad:__ Too vague
```
def d(): 
    x = y + z
```
#### 2. Constants (ALL_CAPS)
✅ Use uppercase with underscores for constants:
```
MAX_ITERATIONS = 1000
DATASET_PATH = "data/raw/water_pumps.csv"
```

#### 3. Filenames
✅ Use descriptive, lowercase filenames with underscores:
```
train_model.py
preprocess_data.py
```

❌ Avoid spaces, special characters, or CamelCase:
```
TrainModel.py  # Wrong capitalization  
preprocessData.py  # CamelCase (not recommended)  
evaluate results.py  # Spaces (avoid this) 
```

#### 4. Directory Naming:
✅ Use lowercase, plural names and underscores (_) if needed:
 ```python
  data/
  notebooks/
  scripts/
```

❌ Avoid CamelCase or spaces:
```
Data/    
NotebookFiles/  
```

#### 5. Git Branch Naming:

✅ Use a structured format like:
 ```
 feature/add-preprocessing
 bugfix/fix-missing-values

 Example: git checkout -b feature/train-waterpump-model
 ```

# 📁 Project Structure  

#### Project overview & setup instructions
```
│── 📜 .gitignore # Ignore unnecessary files (e.g., datasets, logs)
│── 📜 requirements.txt # Python dependencies (if using pip)
│── 📜 environment.yml # Conda environment file (optional)
│── 📂 data/ # Store datasets
│ ├── 📂 raw/ # Raw data (original, unmodified)
│ ├── 📂 processed/ # Cleaned & preprocessed data
│ ├── 📂 external/ # External datasets (if any)
│── 📂 notebooks/ # Jupyter notebooks for EDA & experiments
│ ├── data_exploration.ipynb
│ ├── feature_engineering.ipynb
│── 📂 src/ # Source code for the project
│ ├── 📜 preprocess.py # Data cleaning functions
│ ├── 📜 train.py # Model training script
│ ├── 📜 evaluate.py # Model evaluation script
│── 📂 models/ # Trained ML models & checkpoints
│── 📂 results/ # Model performance reports, figures, and logs
│── 📂 scripts/ # Helper scripts (e.g., automation)
│── 📂 tests/ # Unit tests to validate code
│── 📂 docs/ # Documentation, references, and reports
```

# References
https://design.maji.go.tz/index.php/Chapter_One%3AIntroduction_VOL1?utm_source=chatgpt.com
