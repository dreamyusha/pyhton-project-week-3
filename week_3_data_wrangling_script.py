"""
Week 3 Assignment: Python & Data Wrangling (Pandas, Matplotlib & Seaborn)
Dataset: data.csv (Fitness Workout Logs - December 2020)

Topics & Assignment Objectives Covered:
1. Python Basics: Data structures (dicts, lists), custom functions, and modular scripting.
2. Reading & Inspecting CSV Data: Identifying missing values, duplicates, formatting issues, and outliers.
3. Data Cleaning in Pandas:
   - Removing exact duplicate rows.
   - Standardizing inconsistent date strings and parsing datetime objects.
   - Handling missing values (imputing numeric NaNs with median; dropping unrecoverable missing dates).
   - Correcting erroneous outlier values (Duration = 450 -> 45 mins).
4. Data Manipulation:
   - Filtering rows based on conditional criteria.
   - Creating derived feature columns (Calories_Per_Min, Pulse_Reserve, Intensity_Level, Day_of_Week).
   - Merging datasets using pd.merge() with a workout zone lookup table.
5. Data Visualization (Matplotlib & Seaborn):
   - Scatter & regression analysis of Pulse vs. Calories Burned.
   - Time-series trend and categorical comparison charts.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def classify_intensity(pulse: float) -> str:
    """Categorizes workout intensity based on average heart rate (BPM)."""
    if pulse >= 110:
        return "High"
    elif pulse >= 100:
        return "Moderate"
    return "Low"


def resolve_input_file() -> str:
    """Finds the input CSV file whether named data.csv or data_2.csv."""
    for candidate in ("data.csv", "data_2.csv"):
        if Path(candidate).exists():
            return candidate
    raise FileNotFoundError("Could not find 'data.csv' or 'data_2.csv' in the current directory.")


def load_and_inspect(filepath: str) -> pd.DataFrame:
    """Loads the raw CSV dataset and prints initial data quality diagnostics."""
    df = pd.read_csv(filepath)
    print("=" * 65)
    print("1. RAW DATASET INSPECTION")
    print("=" * 65)
    print(f"Loaded File  : {filepath}")
    print(f"Initial Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print("\nData Types:")
    print(df.dtypes)
    print("\nMissing Values per Column:")
    print(df.isnull().sum())
    print(f"\nExact Duplicate Rows: {df.duplicated().sum()}")
    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans duplicates, date formatting, missing values, and erroneous outliers."""
    df_clean = df.drop_duplicates().copy()

    # Standardize Date column (strip single quotes and parse mixed formats like '2020/12/01' & 20201226)
    df_clean["Date"] = df_clean["Date"].astype(str).str.replace("'", "", regex=False).str.strip()
    df_clean["Date"] = pd.to_datetime(df_clean["Date"], format="mixed", errors="coerce")

    # Drop rows where Date is missing (cannot reliably fabricate missing session date)
    df_clean = df_clean.dropna(subset=["Date"]).copy()

    # Impute missing Calories with the median value
    calories_median = df_clean["Calories"].median()
    df_clean["Calories"] = df_clean["Calories"].fillna(calories_median)

    # Fix typo outlier in Duration (450 minutes -> 45 minutes)
    df_clean.loc[df_clean["Duration"] > 120, "Duration"] = 45

    df_clean = df_clean.sort_values("Date").reset_index(drop=True)
    return df_clean


def engineer_and_merge_features(df: pd.DataFrame) -> pd.DataFrame:
    """Creates new derived columns and merges workout zone metadata."""
    df_feat = df.copy()

    # Create new columns
    df_feat["Calories_Per_Min"] = (df_feat["Calories"] / df_feat["Duration"]).round(2)
    df_feat["Pulse_Reserve"] = df_feat["Maxpulse"] - df_feat["Pulse"]
    df_feat["Intensity_Level"] = df_feat["Pulse"].apply(classify_intensity)
    df_feat["Day_of_Week"] = df_feat["Date"].dt.day_name()

    # Reference lookup table for Pandas merge demonstration
    zone_lookup = pd.DataFrame({
        "Intensity_Level": ["High", "Moderate", "Low"],
        "Heart_Rate_Zone": ["Zone 4 (Anaerobic)", "Zone 3 (Aerobic)", "Zone 2 (Fat Burn)"],
        "Recommended_Rest_Hrs": [48, 24, 12],
    })

    df_merged = pd.merge(df_feat, zone_lookup, on="Intensity_Level", how="left")
    return df_merged


def create_visualizations(df: pd.DataFrame) -> None:
    """Generates Matplotlib and Seaborn visualizations for the cleaned dataset."""
    sns.set_theme(style="whitegrid", palette="deep")

    # ---------------------------------------------------------
    # Chart 1: Seaborn Scatter Plot (Pulse vs. Calories Burned)
    # ---------------------------------------------------------
    plt.figure(figsize=(8, 5))
    sns.scatterplot(
        data=df,
        x="Pulse",
        y="Calories",
        hue="Intensity_Level",
        size="Duration",
        sizes=(60, 220),
        alpha=0.85,
    )
    sns.regplot(
        data=df,
        x="Pulse",
        y="Calories",
        scatter=False,
        color="#2c3e50",
        line_kws={"linestyle": "--", "linewidth": 1.5, "label": "Linear Trend"},
    )
    plt.title("Workout Pulse vs. Calories Burned (Cleaned Dataset)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Average Pulse (BPM)", fontsize=11)
    plt.ylabel("Calories Burned (kcal)", fontsize=11)
    plt.legend(title="Intensity / Duration", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig("week3_calories_vs_pulse.png", dpi=150)
    plt.close()

    # ---------------------------------------------------------
    # Chart 2: Multi-Panel Time Series & Intensity Comparison
    # ---------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Left Panel: Daily Calories Trend
    axes[0].plot(df["Date"], df["Calories"], marker="o", color="#1f77b4", linewidth=2, markersize=5)
    axes[0].axhline(
        df["Calories"].mean(),
        color="#d62728",
        linestyle="--",
        linewidth=1.2,
        label=f"Mean ({df['Calories'].mean():.1f} kcal)",
    )
    axes[0].set_title("Daily Calorie Burn Trend (Dec 2020)", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Session Date", fontsize=10)
    axes[0].set_ylabel("Calories Burned (kcal)", fontsize=10)
    axes[0].tick_params(axis="x", rotation=45)
    axes[0].legend()

    # Right Panel: Average Calories by Intensity Level
    order = ["Low", "Moderate", "High"]
    sns.barplot(
        data=df,
        x="Intensity_Level",
        y="Calories",
        hue="Intensity_Level",
        order=order,
        estimator="mean",
        errorbar=None,
        legend=False,
        ax=axes[1],
        palette=["#6baed6", "#3182bd", "#08519c"],
    )
    axes[1].set_title("Average Calories Burned by Intensity Level", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("Intensity Level", fontsize=10)
    axes[1].set_ylabel("Mean Calories Burned (kcal)", fontsize=10)

    for container in axes[1].containers:
        axes[1].bar_label(container, fmt="%.1f", padding=3, fontsize=9)

    plt.tight_layout()
    plt.savefig("week3_workout_trends.png", dpi=150)
    plt.close()


def main() -> None:
    input_path = resolve_input_file()
    raw_df = load_and_inspect(input_path)
    cleaned_df = clean_dataset(raw_df)
    final_df = engineer_and_merge_features(cleaned_df)

    # Filter rows: High-burn sessions (> 300 kcal)
    high_burn_df = final_df[final_df["Calories"] > 300]

    print("\n" + "=" * 65)
    print("2. CLEANED & ENRICHED DATASET SUMMARY")
    print("=" * 65)
    print(f"Final Shape: {final_df.shape[0]} rows x {final_df.shape[1]} columns")
    print(f"Remaining Missing Values: {final_df.isnull().sum().sum()}")
    print(f"High-Burn Sessions (> 300 kcal): {len(high_burn_df)} sessions")
    print("\nSummary Statistics (Cleaned):")
    print(final_df[["Duration", "Pulse", "Maxpulse", "Calories", "Calories_Per_Min"]].describe().round(2))

    # Save cleaned dataset and charts
    final_df.to_csv("cleaned_data.csv", index=False)
    create_visualizations(final_df)
    print("\nSaved 'cleaned_data.csv', 'week3_calories_vs_pulse.png', and 'week3_workout_trends.png'.")


if __name__ == "__main__":
    main()