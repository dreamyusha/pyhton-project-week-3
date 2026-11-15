# Week 3: Python & Data Wrangling

This repository contains the completed **Week 3 Assignment** for the Data Analyst Course, covering **Python fundamentals**, **data cleaning and wrangling with Pandas**, and **exploratory data visualization with Matplotlib and Seaborn**.

---

## Repository Structure

```text
├── README.md                      # Project documentation and assignment summary
├── requirements.txt               # Python package dependencies
├── .gitignore                     # Standard Python & environment ignore rules
├── data.csv                       # Raw input dataset (Fitness Workout Logs)
├── week3_data_wrangling.py        # End-to-end cleaning, wrangling & visualization script
├── cleaned_data.csv               # Output cleaned & feature-engineered dataset
├── week3_calories_vs_pulse.png    # Seaborn scatter & regression plot
└── week3_workout_trends.png       # Matplotlib & Seaborn time-series and bar charts
```

---

## Assignment Objectives & Workflow

### 1. Python Basics & Modular Scripting
- Uses Python data structures (`dict`, `list`) and modular, type-annotated functions (`load_and_inspect`, `clean_dataset`, `engineer_and_merge_features`, `create_visualizations`) to build a reproducible data pipeline.

### 2. Data Cleaning in Pandas (`data.csv`)
Starting from the raw 32-row fitness log dataset (`Duration`, `Date`, `Pulse`, `Maxpulse`, `Calories`), the script resolves all data quality issues:
- **Duplicate Removal:** Removed `1` exact duplicate record (`2020-12-12`), reducing rows from `32` to `31`.
- **Date Standardization & Missing Dates:** Stripped stray quotes (`'2020/12/01'`), standardized mixed date formats (`20201226` $\rightarrow$ `2020-12-26`), and dropped `1` row with an unrecoverable missing `Date`, leaving **`30` valid workout sessions**.
- **Missing Value Imputation:** Imputed `2` missing values in `Calories` using the dataset median (`291.2 kcal`).
- **Outlier Correction:** Corrected the data-entry typo in `Duration` on `2020-12-08` from `450` minutes to `45` minutes.

### 3. Filtering, Feature Engineering & Merging
- **Row Filtering:** Filtered high-burn workout sessions (`Calories > 300 kcal`), identifying `14` high-output sessions.
- **New Derived Columns:**
  - `Calories_Per_Min`: Calorie burn rate per minute (`Calories / Duration`).
  - `Pulse_Reserve`: Difference between peak and average heart rate (`Maxpulse - Pulse`).
  - `Intensity_Level`: Categorized into `Low` (`< 100 BPM`), `Moderate` (`100–109 BPM`), and `High` (`>= 110 BPM`).
  - `Day_of_Week`: Day name extracted from the parsed `Date` column.
- **Dataset Merging (`pd.merge`):** Joined the cleaned workout logs with a heart-rate zone lookup table on `Intensity_Level` to enrich records with `Heart_Rate_Zone` and `Recommended_Rest_Hrs`.

### 4. Data Visualization (Matplotlib & Seaborn)
- **`week3_calories_vs_pulse.png`:** Seaborn scatter plot with a linear regression trendline comparing `Pulse` vs. `Calories`, encoded by `Intensity_Level` and `Duration`.
- **`week3_workout_trends.png`:** Two-panel dashboard comparing daily calorie burn trends (`Mean = 306.9 kcal`) alongside average calories burned across intensity levels (`Low: 255.2 kcal`, `Moderate: 303.0 kcal`, `High: 393.6 kcal`).

---

## How to Run Locally

1. **Clone the repository and place `data.csv` in the root directory:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute the wrangling script:**
   ```bash
   python week3_data_wrangling.py
   ```