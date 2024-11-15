# -*- coding: utf-8 -*-
"""advanced_revenue_optimization_analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Hsks94vSpLa675tv4jlQi8cVNBnQUcrw
"""

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class AdvancedRevenueAnalyzer:
    def __init__(self, allocation, pricing):
        self.allocation = allocation
        self.pricing = pricing

    def analyze_revenue_potential(self):
        """Analyze revenue potential and suggest optimizations"""
        # Convert pricing data to DataFrame
        pricing_df = pd.DataFrame(self.pricing)

        # Calculate potential metrics
        revenue_analysis = {}
        for booking_class in self.allocation.keys():
            class_data = pricing_df[pricing_df['Booking_Class'] == booking_class].iloc[0]
            seats = self.allocation[booking_class]

            # Calculate various revenue scenarios
            optimal_revenue = seats * class_data['Base_Fare'] * (1 - class_data['Risk_Factor'])
            peak_revenue = seats * class_data['Peak_Price'] * (1 - class_data['Risk_Factor'] * 0.8)
            off_peak_revenue = seats * class_data['Off_Peak_Price'] * (1 - class_data['Risk_Factor'] * 1.2)

            revenue_analysis[booking_class] = {
                'Seats': seats,
                'Base_Revenue': optimal_revenue,
                'Peak_Revenue': peak_revenue,
                'Off_Peak_Revenue': off_peak_revenue,
                'Revenue_Range': peak_revenue - off_peak_revenue,
                'Risk_Factor': class_data['Risk_Factor'],
                'Revenue_per_Seat': optimal_revenue / seats
            }

        return pd.DataFrame(revenue_analysis).T

    def suggest_class_consolidation(self):
        """Suggest booking class consolidation based on similar characteristics"""
        pricing_df = pd.DataFrame(self.pricing)

        # Create features DataFrame
        class_features = []
        for booking_class in self.allocation.keys():
            class_data = pricing_df[pricing_df['Booking_Class'] == booking_class].iloc[0]
            class_features.append({
                'Booking_Class': booking_class,
                'Base_Fare': class_data['Base_Fare'],
                'Risk_Factor': class_data['Risk_Factor'],
                'Allocated_Seats': self.allocation[booking_class]
            })

        features_df = pd.DataFrame(class_features)

        # Normalize features
        scaler = StandardScaler()
        features_to_normalize = ['Base_Fare', 'Risk_Factor', 'Allocated_Seats']
        normalized_features = scaler.fit_transform(features_df[features_to_normalize])

        # Perform clustering
        kmeans = KMeans(n_clusters=5, random_state=42)
        features_df['Cluster'] = kmeans.fit_predict(normalized_features)

        return features_df

    def optimize_peak_scheduling(self):
        """Optimize scheduling based on pricing tiers"""
        revenue_analysis = self.analyze_revenue_potential()

        # Sort classes by revenue per seat
        sorted_classes = revenue_analysis.sort_values('Revenue_per_Seat', ascending=False)

        # Create time slot recommendations
        time_slots = {
            'Morning_Peak': [],
            'Midday': [],
            'Evening_Peak': [],
            'Off_Peak': []
        }

        for booking_class in sorted_classes.index:
            revenue_data = revenue_analysis.loc[booking_class]
            peak_ratio = revenue_data['Peak_Revenue'] / revenue_data['Off_Peak_Revenue']

            if peak_ratio > 1.2:
                if len(time_slots['Morning_Peak']) < len(sorted_classes) // 4:
                    time_slots['Morning_Peak'].append(booking_class)
                else:
                    time_slots['Evening_Peak'].append(booking_class)
            elif peak_ratio > 1.1:
                time_slots['Midday'].append(booking_class)
            else:
                time_slots['Off_Peak'].append(booking_class)

        return time_slots

    def visualize_advanced_analysis(self):
        """Create advanced visualizations for analysis"""
        revenue_analysis = self.analyze_revenue_potential()

        # Create subplot with increased spacing
        fig = plt.figure(figsize=(22, 18))
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

        # 1. Revenue Potential by Class
        ax1 = fig.add_subplot(gs[0, 0])
        revenue_data = revenue_analysis[['Base_Revenue', 'Peak_Revenue', 'Off_Peak_Revenue']].head(10)
        revenue_data.plot(kind='bar', ax=ax1)
        ax1.set_title('Revenue Potential by Booking Class (Top 10)', pad=20)
        ax1.set_xlabel('Booking Class')
        ax1.set_ylabel('Revenue (USD)')
        ax1.tick_params(axis='x', rotation=45)

        # 2. Risk vs Revenue per Seat
        ax2 = fig.add_subplot(gs[0, 1])
        scatter = ax2.scatter(revenue_analysis['Risk_Factor'],
                            revenue_analysis['Revenue_per_Seat'],
                            alpha=0.6)
        for idx in revenue_analysis.index:
            ax2.annotate(idx,
                        (revenue_analysis.loc[idx, 'Risk_Factor'],
                         revenue_analysis.loc[idx, 'Revenue_per_Seat']),
                        xytext=(5, 5), textcoords='offset points')
        ax2.set_xlabel('Risk Factor')
        ax2.set_ylabel('Revenue per Seat (USD)')
        ax2.set_title('Risk vs Revenue Analysis', pad=20)

        # 3. Class Clustering Analysis
        ax3 = fig.add_subplot(gs[1, 0])
        class_clusters = self.suggest_class_consolidation()
        for cluster in range(5):
            cluster_data = class_clusters[class_clusters['Cluster'] == cluster]
            ax3.scatter(cluster_data['Base_Fare'],
                       cluster_data['Risk_Factor'],
                       label=f'Cluster {cluster}')
            for _, row in cluster_data.iterrows():
                ax3.annotate(row['Booking_Class'],
                           (row['Base_Fare'], row['Risk_Factor']),
                           xytext=(5, 5), textcoords='offset points')
        ax3.set_xlabel('Base Fare')
        ax3.set_ylabel('Risk Factor')
        ax3.set_title('Booking Class Clusters', pad=20)
        ax3.legend()

        # 4. Time Slot Distribution
        ax4 = fig.add_subplot(gs[1, 1])
        time_slots = self.optimize_peak_scheduling()
        slot_sizes = [len(classes) for classes in time_slots.values()]
        ax4.pie(slot_sizes, labels=time_slots.keys(), autopct='%1.1f%%')
        ax4.set_title('Recommended Time Slot Distribution', pad=20)

        plt.tight_layout()
        plt.show()

        return revenue_analysis, time_slots, class_clusters

def print_optimization_recommendations(revenue_analysis, time_slots, class_clusters):
    """Print detailed optimization recommendations"""
    print("\nADVANCED OPTIMIZATION RECOMMENDATIONS")
    print("=" * 50)

    # Revenue Optimization
    print("\n1. Revenue Optimization Opportunities:")
    top_revenue = revenue_analysis.nlargest(5, 'Revenue_per_Seat')
    print("\nTop 5 Revenue Generating Classes:")
    for idx in top_revenue.index:
        print(f"   • {idx}: ${top_revenue.loc[idx, 'Revenue_per_Seat']:.2f} per seat")

    # Time Slot Recommendations
    print("\n2. Time Slot Optimization:")
    for slot, classes in time_slots.items():
        print(f"\n   {slot}:")
        print(f"   • Recommended Classes: {', '.join(classes)}")

    # Class Consolidation
    print("\n3. Class Consolidation Opportunities:")
    for cluster in range(5):
        cluster_classes = class_clusters[class_clusters['Cluster'] == cluster]['Booking_Class'].tolist()
        mean_fare = class_clusters[class_clusters['Cluster'] == cluster]['Base_Fare'].mean()
        mean_risk = class_clusters[class_clusters['Cluster'] == cluster]['Risk_Factor'].mean()
        print(f"\n   Cluster {cluster}:")
        print(f"   • Classes: {', '.join(cluster_classes)}")
        print(f"   • Average Fare: ${mean_fare:.2f}")
        print(f"   • Average Risk: {mean_risk:.1%}")
        print(f"   • Suggested Action: {'Consolidate' if len(cluster_classes) > 3 else 'Maintain'}")

    # Risk Management
    print("\n4. Risk Management Strategies:")
    high_risk_threshold = revenue_analysis['Risk_Factor'].quantile(0.75)
    high_risk = revenue_analysis[revenue_analysis['Risk_Factor'] > high_risk_threshold]
    print(f"\n   High Risk Classes (Risk > {high_risk_threshold:.1%}):")
    for idx in high_risk.index:
        print(f"   • {idx}: {high_risk.loc[idx, 'Risk_Factor']:.1%} risk factor")

def main():
    # Initialize with previous results
    # Note: You'll need to pass your allocation and pricing results here
    analyzer = AdvancedRevenueAnalyzer(allocation, pricing)

    # Run advanced analysis
    revenue_analysis, time_slots, class_clusters = analyzer.visualize_advanced_analysis()

    # Print recommendations
    print_optimization_recommendations(revenue_analysis, time_slots, class_clusters)

if __name__ == "__main__":
    main()