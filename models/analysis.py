#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
analysis.py - Data analysis module

Performs data loading, cleaning, analysis, and visualization.

Structure:
1. Imports
2. Configuration/Constants
3. Helper Functions
4. Data Loading
5. Data Cleaning
6. Data Analysis
7. Visualization
8. Main Function
"""

# ============================== IMPORTS ======================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, Dict, List

# Optional imports (handle with try-except if needed)
try:
    import scipy.stats as stats
except ImportError:
    pass

# ============================= CONFIGURATION ================================

# Constants
DATA_DIR = "data"
OUTPUT_DIR = "results"
PLOT_FORMAT = "png"  # or 'svg', 'pdf'

# Style configuration
plt.style.use("seaborn")
sns.set_palette("husl")

# ============================ HELPER FUNCTIONS ==============================

def create_dir_if_not_exists(directory: str) -> None:
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_plot(fig, name: str, dpi: int = 300) -> None:
    """
    Save matplotlib figure to output directory.
    
    Args:
        fig: matplotlib figure object
        name: filename without extension
        dpi: resolution for raster formats
    """
    create_dir_if_not_exists(OUTPUT_DIR)
    path = os.path.join(OUTPUT_DIR, f"{name}.{PLOT_FORMAT}")
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    print(f"Saved plot to {path}")

# ============================= DATA LOADING ================================

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from CSV/Excel file.
    
    Args:
        file_path: Path to data file
        
    Returns:
        Loaded pandas DataFrame
    """
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format")

# ============================= DATA CLEANING ===============================

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform data cleaning operations.
    
    Args:
        df: Raw DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    # Handle missing values
    df = df.dropna()  # or use fillna() with appropriate strategy
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Convert data types if needed
    # df['date_column'] = pd.to_datetime(df['date_column'])
    
    return df

# ============================= DATA ANALYSIS ===============================

def compute_descriptive_stats(df: pd.DataFrame) -> Dict:
    """
    Compute basic descriptive statistics.
    
    Args:
        df: Cleaned DataFrame
        
    Returns:
        Dictionary of statistics
    """
    return {
        'mean': df.mean(numeric_only=True),
        'median': df.median(numeric_only=True),
        'std': df.std(numeric_only=True),
        'correlation': df.corr(numeric_only=True)
    }

def perform_advanced_analysis(df: pd.DataFrame) -> Dict:
    """
    Perform more sophisticated analysis.
    
    Args:
        df: Cleaned DataFrame
        
    Returns:
        Dictionary with analysis results
    """
    results = {}
    
    # Example: t-test between two groups
    # group1 = df[df['group'] == 'A']['value']
    # group2 = df[df['group'] == 'B']['value']
    # results['t_test'] = stats.ttest_ind(group1, group2)
    
    return results

# ============================ VISUALIZATION ================================

def plot_distributions(df: pd.DataFrame) -> None:
    """
    Plot distributions of numeric variables.
    
    Args:
        df: DataFrame to visualize
    """
    numeric_cols = df.select_dtypes(include=np.number).columns
    
    for col in numeric_cols:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(df[col], kde=True, ax=ax)
        ax.set_title(f"Distribution of {col}")
        save_plot(fig, f"dist_{col}")

def plot_correlations(df: pd.DataFrame) -> None:
    """
    Plot correlation heatmap for numeric variables.
    
    Args:
        df: DataFrame with numeric columns
    """
    numeric_df = df.select_dtypes(include=np.number)
    if len(numeric_df.columns) < 2:
        return
    
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(
        numeric_df.corr(),
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        ax=ax
    )
    ax.set_title("Correlation Heatmap")
    save_plot(fig, "correlation_heatmap")

# ============================= MAIN FUNCTION ================================

def main():
    """Main analysis workflow."""
    print("Starting analysis...")
    
    # 1. Load data
    data_path = os.path.join(DATA_DIR, "dataset.csv")  # change as needed
    try:
        df = load_data(data_path)
        print(f"Loaded data with shape: {df.shape}")
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    # 2. Clean data
    df_clean = clean_data(df)
    print(f"After cleaning, shape: {df_clean.shape}")
    
    # 3. Perform analysis
    stats = compute_descriptive_stats(df_clean)
    advanced_results = perform_advanced_analysis(df_clean)
    
    # 4. Visualize
    plot_distributions(df_clean)
    plot_correlations(df_clean)
    
    # 5. Save results (optional)
    # results_path = os.path.join(OUTPUT_DIR, "analysis_results.txt")
    # with open(results_path, 'w') as f:
    #     f.write(str(stats))
    
    print("Analysis completed!")

if __name__ == "__main__":
    main()