# -*- coding: utf-8 -*-
"""advanced_feature_analysis_selection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Hsks94vSpLa675tv4jlQi8cVNBnQUcrw
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

def print_feature_importance_summary(models):
    """Print feature importance summary for all models"""
    for target_type, forecaster in models.items():
        print(f"\n{target_type.replace('_', ' ').title()} Model - Top 10 Features:")
        print("=" * 60)
        print(f"{'Feature':<40} {'Importance':>10}")
        print("-" * 60)

        # Get feature importance from the model
        importances = pd.DataFrame({
            'feature': forecaster.model.feature_names_in_,
            'importance': forecaster.model.feature_importances_
        }).sort_values('importance', ascending=False)

        # Print top 10 features
        for _, row in importances.head(10).iterrows():
            print(f"{row['feature']:<40} {row['importance']:>10.4f}")
        print("-" * 60)

def plot_feature_importance_comparison(models):
    """Create feature importance comparison visualization"""
    plt.figure(figsize=(15, 8))

    # Collect feature importance data
    all_importances = {}
    for target_type, forecaster in models.items():
        importances = pd.DataFrame({
            'feature': forecaster.model.feature_names_in_,
            'importance': forecaster.model.feature_importances_
        }).sort_values('importance', ascending=False)

        all_importances[target_type] = importances.set_index('feature')['importance']

    # Create comparison dataframe
    comparison_df = pd.DataFrame(all_importances)

    # Plot heatmap
    plt.subplot(1, 2, 1)
    sns.heatmap(comparison_df.head(10), annot=True, fmt='.3f', cmap='YlOrRd')
    plt.title('Top 10 Features Importance Across Models')
    plt.xlabel('Models')
    plt.ylabel('Features')

    # Plot correlation between target variables
    target_vars = ['no_show', 'cancellation', 'overbooking', 'denied_boarding']
    corr_matrix = df[target_vars].corr()

    plt.subplot(1, 2, 2)
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm')
    plt.title('Target Variable Correlation')

    plt.tight_layout()
    plt.show()

def plot_temporal_patterns(df):
    """Plot temporal patterns for all target variables with better formatting"""
    # Safely extract temporal features
    df = df.copy()

    # Safely extract hour from time string
    def extract_hour(time_str):
        try:
            if ':' in str(time_str):
                return int(str(time_str).split(':')[0])
            return int(str(time_str)[:2])
        except:
            return 12

    # Process temporal features
    df['Hour'] = df['Dep_time'].apply(extract_hour)
    df['DayOfWeek'] = pd.to_datetime(df['Dep_Date']).dt.dayofweek
    df['Month'] = pd.to_datetime(df['Dep_Date']).dt.month

    target_vars = ['no_show', 'cancellation', 'overbooking', 'denied_boarding']

    # Create temporal pattern plots with increased figure size and spacing
    plt.figure(figsize=(20, 6))

    # Hour patterns
    hourly_means = df.groupby('Hour')[target_vars].mean()
    print("\nHourly Patterns (Average Values):")
    print("=" * 60)
    print(hourly_means.round(4))

    plt.subplot(1, 3, 1)
    sns.heatmap(hourly_means.T, cmap='YlOrRd', annot=True, fmt='.3f',
                cbar_kws={'label': 'Average Rate'})
    plt.title('Patterns by Hour', pad=20)
    plt.xlabel('Hour of Day', labelpad=10)
    plt.ylabel('Event Type', labelpad=10)

    # Day of week patterns
    daily_means = df.groupby('DayOfWeek')[target_vars].mean()
    print("\nDaily Patterns (Average Values):")
    print("=" * 60)
    print(daily_means.round(4))

    plt.subplot(1, 3, 2)
    sns.heatmap(daily_means.T, cmap='YlOrRd', annot=True, fmt='.3f',
                cbar_kws={'label': 'Average Rate'})
    plt.title('Patterns by Day of Week', pad=20)
    plt.xlabel('Day of Week (0=Monday)', labelpad=10)
    plt.ylabel('Event Type', labelpad=10)

    # Monthly patterns
    monthly_means = df.groupby('Month')[target_vars].mean()
    print("\nMonthly Patterns (Average Values):")
    print("=" * 60)
    print(monthly_means.round(4))

    plt.subplot(1, 3, 3)
    sns.heatmap(monthly_means.T, cmap='YlOrRd', annot=True, fmt='.3f',
                cbar_kws={'label': 'Average Rate'})
    plt.title('Patterns by Month', pad=20)
    plt.xlabel('Month', labelpad=10)
    plt.ylabel('Event Type', labelpad=10)

    # Adjust layout to prevent overlap
    plt.tight_layout(w_pad=3.0)  # Increase spacing between subplots
    plt.show()

def main():
    print("Loading data...")
    df = pd.read_csv('forecasting_booking_12m.csv')
    print(f"Dataset shape: {df.shape}")

    if 'models' in globals():
        print("\nPrinting Feature Importance Summary...")
        print_feature_importance_summary(models)

        print("\nGenerating Feature Importance Comparison Plot...")
        plot_feature_importance_comparison(models)

        print("\nAnalyzing Temporal Patterns...")
        plot_temporal_patterns(df)
    else:
        print("Please run this after model training when 'models' variable is available.")

if __name__ == "__main__":
    main()