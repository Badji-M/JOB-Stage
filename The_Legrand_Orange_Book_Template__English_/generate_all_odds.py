import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Wedge, FancyArrowPatch, Circle, Rectangle
import numpy as np
import os

# Load data
base_score_final = pd.read_stata('base_score_final.dta')
base_score_indicateur = pd.read_stata('base_score_indicateur.dta')

# Generate for all ODDs
for odd_num in range(1, 18):
    odd_str = f'ODD{odd_num}'
    
    try:
        # Get ODD data
        odd_global = base_score_final[base_score_final['ODD'] == odd_str]['score'].values[0]
        odd_indicators = base_score_indicateur[base_score_indicateur['ODD'] == odd_str].copy()
        odd_indicators = odd_indicators.sort_values('score')
        
        print(f"{odd_str}: score={odd_global:.4f}, {len(odd_indicators)} indicateurs")
        
        # Create figure
        fig = plt.figure(figsize=(14, 10), dpi=300)
        
        # ===== SUBPLOT 1: GAUGE WITH NEEDLE =====
        ax1 = plt.subplot(2, 1, 1, aspect='equal')
        ax1.set_xlim(-1.2, 1.2)
        ax1.set_ylim(-0.3, 1.2)
        ax1.axis('off')
        
        # Draw gauge - Wedge zones (semicircle 0-180 degrees)
        center = (0, 0)
        radius_outer = 1.0
        radius_inner = 0.75
        
        # Colors for each zone - inversé
        colors = ['#003D82', '#0055B8', '#4A90E2', '#87CEEB']  # Dark to light blue
        angles = [(0, 45), (45, 90), (90, 135), (135, 180)]
        
        for color, (angle_start, angle_end) in zip(colors, angles):
            wedge = Wedge(center, radius_outer, angle_start, angle_end, 
                          width=radius_outer-radius_inner, facecolor=color, edgecolor='none')
            ax1.add_patch(wedge)
        
        # Inner circle (white)
        inner_circle = Circle(center, radius_inner, color='white', zorder=2)
        ax1.add_patch(inner_circle)
        
        # Threshold labels
        thresholds = [1.0, 0.75, 0.5, 0.25, 0.0]
        threshold_angles = np.array([0, 45, 90, 135, 180])
        
        for threshold, angle in zip(thresholds, threshold_angles):
            angle_rad = np.radians(angle)
            x = 1.15 * np.cos(angle_rad)
            y = 1.15 * np.sin(angle_rad)
            ax1.text(x, y, f'{threshold:.2f}', ha='center', va='center', 
                    fontsize=10, fontweight='bold', color='black')
        
        # Draw needle (AIGUILLE A DROITE)
        needle_angle = 180 - (odd_global * 180)  # Inverse: 0 = droite, 180 = gauche
        needle_angle_rad = np.radians(needle_angle)
        needle_length = 0.85
        
        needle_x = needle_length * np.cos(needle_angle_rad)
        needle_y = needle_length * np.sin(needle_angle_rad)
        
        # Needle line
        ax1.plot([0, needle_x], [0, needle_y], color='black', linewidth=3, zorder=3)
        
        # Center dot
        center_dot = Circle((0, 0), 0.05, color='black', zorder=4)
        ax1.add_patch(center_dot)
        
        # Score text - avec plus d'espace
        ax1.text(0, -0.15, f'{odd_global:.2f}', ha='center', va='top', 
                fontsize=36, fontweight='bold', color='#003D82')
        ax1.text(0, -0.38, f'Score Global {odd_str}', ha='center', va='top', 
                fontsize=12, fontweight='bold', color='black')
        
        # ===== SUBPLOT 2: PERFORMANCE BARS =====
        ax2 = plt.subplot(2, 1, 2)
        
        # Get indicator codes and scores
        indicator_codes = odd_indicators['code_ODD2'].values
        indicator_scores = odd_indicators['score'].values
        
        # Color by performance zone
        def get_bar_color(score):
            if score < 0.3:
                return '#87CEEB'
            elif score < 0.6:
                return '#4A90E2'
            elif score < 0.8:
                return '#0055B8'
            else:
                return '#003D82'
        
        bar_colors = [get_bar_color(s) for s in indicator_scores]
        
        # Horizontal bars
        y_pos = np.arange(len(indicator_codes))
        bars = ax2.barh(y_pos, indicator_scores, color=bar_colors, edgecolor='gray', linewidth=0.5, height=0.65)
        
        # Customize
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(indicator_codes, fontsize=9, fontweight='bold')
        ax2.set_xlabel('Score (0 a 1)', fontsize=11, fontweight='bold')
        ax2.set_xlim(0, 1.0)
        ax2.grid(axis='x', alpha=0.3, linestyle='--', linewidth=0.5)
        
        # Add score values on bars
        for i, (bar, score) in enumerate(zip(bars, indicator_scores)):
            ax2.text(score + 0.02, i, f'{score:.2f}', va='center', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        
        # Save figure
        os.makedirs('Pictures/graphs', exist_ok=True)
        output_path = f'Pictures/graphs/{odd_str}_scores.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        
        print(f"  [OK] saved")
        
    except Exception as e:
        print(f"  [ERROR] {str(e)}")
        continue

print("\nAll ODD graphs generated successfully!")
