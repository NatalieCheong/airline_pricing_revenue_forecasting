# -*- coding: utf-8 -*-
"""qualitative_target_revenue_optimization.ipynb

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

class QuantitativeTargets:
    def __init__(self, revenue_analysis, allocation, pricing):
        self.revenue_analysis = revenue_analysis
        self.allocation = allocation
        self.pricing = pd.DataFrame(pricing)

    def calculate_revenue_targets(self):
        """Calculate specific revenue targets by class and time period"""
        current_metrics = self.analyze_current_performance()

        targets = {
            "revenue_targets": {
                "overall": self._set_overall_targets(current_metrics),
                "by_class": self._set_class_targets(current_metrics),
                "by_time": self._set_time_targets(current_metrics)
            },
            "risk_targets": self._set_risk_targets(current_metrics),
            "occupancy_targets": self._set_occupancy_targets(current_metrics)
        }

        return targets

    def analyze_current_performance(self):
        """Analyze current performance metrics"""
        current = {
            "total_revenue": sum(self.revenue_analysis['Base_Revenue']),
            "avg_revenue_per_seat": sum(self.revenue_analysis['Base_Revenue']) / sum(self.allocation.values()),
            "class_performance": self.revenue_analysis['Revenue_per_Seat'].to_dict(),
            "risk_rates": self.pricing.set_index('Booking_Class')['Risk_Factor'].to_dict(),
            "current_occupancy": sum(self.allocation.values()) / 400  # assuming 400 seats capacity
        }

        return current

    def _set_overall_targets(self, current):
        """Set overall revenue improvement targets"""
        return {
            "current_daily_revenue": current["total_revenue"],
            "target_daily_revenue": current["total_revenue"] * 1.15,  # 15% improvement target
            "revenue_improvement": current["total_revenue"] * 0.15,
            "target_revenue_per_seat": current["avg_revenue_per_seat"] * 1.15,
            "timeframe": "Next 6 months",
            "key_metrics": {
                "current_rev_per_seat": current["avg_revenue_per_seat"],
                "target_rev_per_seat": current["avg_revenue_per_seat"] * 1.15,
                "improvement_percentage": "15%"
            }
        }

    def _set_class_targets(self, current):
        """Set targets by booking class"""
        class_targets = {}

        # Group classes by performance
        high_yield = {k: v for k, v in current["class_performance"].items()
                     if v > current["avg_revenue_per_seat"] * 1.2}
        mid_yield = {k: v for k, v in current["class_performance"].items()
                    if current["avg_revenue_per_seat"] * 0.8 <= v <= current["avg_revenue_per_seat"] * 1.2}
        low_yield = {k: v for k, v in current["class_performance"].items()
                    if v < current["avg_revenue_per_seat"] * 0.8}

        # Set targets for each group
        for class_type, classes in [("premium", high_yield),
                                  ("mid_tier", mid_yield),
                                  ("economy", low_yield)]:
            improvement_target = 0.20 if class_type == "premium" else \
                               0.15 if class_type == "mid_tier" else 0.10

            class_targets[class_type] = {
                "classes": list(classes.keys()),
                "current_average": sum(classes.values()) / len(classes),
                "target_increase": f"{improvement_target*100}%",
                "target_revenue": {k: v * (1 + improvement_target)
                                 for k, v in classes.items()},
                "suggested_actions": self._get_class_actions(class_type)
            }

        return class_targets

    def _set_time_targets(self, current):
        """Set targets by time period"""
        return {
            "peak_morning": {
                "target_occupancy": 0.95,
                "target_premium_mix": 0.40,  # 40% premium classes
                "revenue_premium": 1.25  # 25% premium over base fare
            },
            "midday": {
                "target_occupancy": 0.85,
                "target_premium_mix": 0.30,
                "revenue_premium": 1.15
            },
            "evening_peak": {
                "target_occupancy": 0.90,
                "target_premium_mix": 0.35,
                "revenue_premium": 1.20
            },
            "off_peak": {
                "target_occupancy": 0.75,
                "target_premium_mix": 0.25,
                "revenue_premium": 1.10
            }
        }

    def _set_risk_targets(self, current):
        """Set risk reduction targets"""
        avg_risk = sum(current["risk_rates"].values()) / len(current["risk_rates"])

        return {
            "current_avg_risk": avg_risk,
            "target_avg_risk": avg_risk * 0.85,  # 15% risk reduction
            "by_class_type": {
                "premium": {
                    "current": sum(v for k, v in current["risk_rates"].items()
                                 if k in ["J", "Y"]) / 2,
                    "target": 0.05  # 5% target risk rate
                },
                "mid_tier": {
                    "current": sum(v for k, v in current["risk_rates"].items()
                                 if k in ["C", "B", "D", "W", "H"]) / 5,
                    "target": 0.10  # 10% target risk rate
                },
                "economy": {
                    "current": sum(v for k, v in current["risk_rates"].items()
                                 if k not in ["J", "Y", "C", "B", "D", "W", "H"]) /
                             (len(current["risk_rates"]) - 7),
                    "target": 0.15  # 15% target risk rate
                }
            }
        }

    def _set_occupancy_targets(self, current):
        """Set occupancy and overbooking targets"""
        return {
            "current_occupancy": current["current_occupancy"],
            "target_occupancy": min(current["current_occupancy"] * 1.10, 0.95),
            "by_class": {
                "premium": 0.90,
                "mid_tier": 0.85,
                "economy": 0.80
            },
            "overbooking_limits": {
                "peak": 1.15,  # 15% overbooking
                "off_peak": 1.10  # 10% overbooking
            }
        }

    def _get_class_actions(self, class_type):
        """Get specific actions for each class type"""
        actions = {
            "premium": [
                "Increase base fare by 10-15% during peak hours",
                "Implement loyalty program benefits",
                "Add premium services",
                "Reduce risk rate to 5%"
            ],
            "mid_tier": [
                "Optimize pricing with 5-10% increases",
                "Implement flexible booking conditions",
                "Target 85% occupancy rate",
                "Reduce risk rate to 10%"
            ],
            "economy": [
                "Dynamic pricing based on demand",
                "Implement advance purchase discounts",
                "Target 80% occupancy rate",
                "Manage risk rate to 15%"
            ]
        }
        return actions[class_type]

def print_quantitative_targets(targets):
    """Print detailed quantitative targets"""
    print("\nQUANTITATIVE TARGETS FOR REVENUE OPTIMIZATION")
    print("=" * 50)

    # Overall Revenue Targets
    print("\n1. Overall Revenue Targets:")
    print(f"   Current Daily Revenue: ${targets['revenue_targets']['overall']['current_daily_revenue']:,.2f}")
    print(f"   Target Daily Revenue: ${targets['revenue_targets']['overall']['target_daily_revenue']:,.2f}")
    print(f"   Expected Improvement: ${targets['revenue_targets']['overall']['revenue_improvement']:,.2f}")
    print(f"   Timeframe: {targets['revenue_targets']['overall']['timeframe']}")

    # Class-Specific Targets
    print("\n2. Class-Specific Targets:")
    for class_type, data in targets['revenue_targets']['by_class'].items():
        print(f"\n   {class_type.upper()}:")
        print(f"   • Classes: {', '.join(data['classes'])}")
        print(f"   • Current Average Revenue: ${data['current_average']:,.2f}")
        print(f"   • Target Increase: {data['target_increase']}")
        print("   • Suggested Actions:")
        for action in data['suggested_actions']:
            print(f"     - {action}")

    # Time-Based Targets
    print("\n3. Time-Based Targets:")
    for period, metrics in targets['revenue_targets']['by_time'].items():
        print(f"\n   {period.replace('_', ' ').upper()}:")
        print(f"   • Target Occupancy: {metrics['target_occupancy']:.0%}")
        print(f"   • Target Premium Mix: {metrics['target_premium_mix']:.0%}")
        print(f"   • Revenue Premium: {metrics['revenue_premium']:.0%}")

    # Risk Management Targets
    print("\n4. Risk Management Targets:")
    risk_targets = targets['risk_targets']
    print(f"   Current Average Risk: {risk_targets['current_avg_risk']:.1%}")
    print(f"   Target Average Risk: {risk_targets['target_avg_risk']:.1%}")

    # Occupancy Targets
    print("\n5. Occupancy Targets:")
    occ_targets = targets['occupancy_targets']
    print(f"   Current Occupancy: {occ_targets['current_occupancy']:.1%}")
    print(f"   Target Occupancy: {occ_targets['target_occupancy']:.1%}")
    print("   Class-Specific Targets:")
    for class_type, target in occ_targets['by_class'].items():
        print(f"   • {class_type}: {target:.0%}")

def main():
    # Calculate revenue analysis
    revenue_analysis = pd.DataFrame({
        class_: {
            'Base_Revenue': allocation[class_] * next(item['Base_Fare'] for item in pricing if item['Booking_Class'] == class_),
            'Peak_Revenue': allocation[class_] * next(item['Peak_Price'] for item in pricing if item['Booking_Class'] == class_),
            'Off_Peak_Revenue': allocation[class_] * next(item['Off_Peak_Price'] for item in pricing if item['Booking_Class'] == class_),
            'Revenue_per_Seat': next(item['Base_Fare'] for item in pricing if item['Booking_Class'] == class_)
        }
        for class_ in allocation.keys()
    }).T

    print("Initializing Quantitative Targets Analysis...")
    print(f"Number of booking classes: {len(allocation)}")
    print(f"Total allocated seats: {sum(allocation.values())}")

    # Initialize and calculate targets
    qt = QuantitativeTargets(revenue_analysis, allocation, pricing)
    targets = qt.calculate_revenue_targets()

    # Print the targets
    print_quantitative_targets(targets)

if __name__ == "__main__":
    main()