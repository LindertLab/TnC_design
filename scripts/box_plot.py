#!/usr/bin/env python3
"""
Create box plots for troponin structures.
Separate figures: Cardiac and Skeletal, each with two box plots side by side.
Each figure takes half the space.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

# Set style for clean plots
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 1000
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans', 'sans-serif']




run_columns = [f'Run_{i}' for i in range(1, 101)]

def extract_probabilities(df):
    """Extract probability values: average over runs for each position."""
    available_runs = [col for col in run_columns if col in df.columns]
    avg_per_position = df[available_runs].mean(axis=1).values
    avg_per_position = avg_per_position[~np.isnan(avg_per_position)]
    return avg_per_position

def format_p_value_2sf(p_value):
    """Format p-value to 2 significant figures with leading zeros."""
    from math import floor, log10
    
    if p_value == 0:
        return '0.00'
    
    if p_value >= 1:
        # For values >= 1, use 2 significant figures
        exp = floor(log10(abs(p_value)))
        coeff = p_value / (10 ** exp)
        return f'{coeff:.2f}e{exp}' if exp > 0 else f'{p_value:.2f}'
    else:
        # For values < 1, calculate decimal places needed for 2 significant figures
        exp = floor(log10(abs(p_value)))
        # Number of decimal places = -exp + 1 (to show 2 significant figures)
        decimal_places = max(0, -exp + 1)
        return f'{p_value:.{decimal_places}f}'

def create_boxplot_figure(df1, df2, label1, label2, color1, color2, 
                          output_file, title_prefix=""):
    """
    Create a figure with two box plots side by side.
    """
    # Extract probabilities
    prob1 = extract_probabilities(df1)
    prob2 = extract_probabilities(df2)
    
    if len(prob1) == 0 or len(prob2) == 0:
        print(f"Warning: No probability values found")
        return
    
    # Perform t-test
    t_stat, p_value = ttest_ind(prob1, prob2)
    
    # Create figure with 1x2 subplots (half dimensions)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 5))
    
    # Calculate statistics for reference lines
    mean1 = np.mean(prob1)
    median1 = np.median(prob1)
    mean2 = np.mean(prob2)
    median2 = np.median(prob2)
    
    # Plot 1: First dataset
    bp1 = ax1.boxplot([prob1], 
                      patch_artist=True,
                      widths=0.6,
                      showmeans=True,
                      meanline=True)
    
    for patch in bp1['boxes']:
        patch.set_facecolor(color1)
        patch.set_alpha(0.7)
        patch.set_edgecolor('black')
        patch.set_linewidth(1.5)
    
    for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        if element in bp1:
            plt.setp(bp1[element], color='black', linewidth=1.5)
    
    # Add subtle reference lines for mean and median (no labels)
    ax1.axhline(y=mean1, color='gray', linestyle='--', linewidth=1, alpha=0.4)
    ax1.axhline(y=median1, color='gray', linestyle=':', linewidth=1, alpha=0.4)
    
    ax1.set_ylabel("Wildtype Probability", fontsize=12)
    ax1.set_title(label1, fontsize=14, pad=10)
    ax1.set_xticklabels([])
    ax1.set_ylim([0, 1])
    ax1.set_yticks(np.arange(0, 1.1, 0.1))
    ax1.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    # Plot 2: Second dataset
    bp2 = ax2.boxplot([prob2], 
                      patch_artist=True,
                      widths=0.6,
                      showmeans=True,
                      meanline=True)
    
    for patch in bp2['boxes']:
        patch.set_facecolor(color2)
        patch.set_alpha(0.7)
        patch.set_edgecolor('black')
        patch.set_linewidth(1.5)
    
    for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        if element in bp2:
            plt.setp(bp2[element], color='black', linewidth=1.5)
    
    ax2.axhline(y=mean2, color='gray', linestyle='--', linewidth=1, alpha=0.4)
    ax2.axhline(y=median2, color='gray', linestyle=':', linewidth=1, alpha=0.4)
    
    ax2.set_ylabel("Wildtype Probability", fontsize=12)
    ax2.set_title(label2, fontsize=14, pad=10)
    ax2.set_xticklabels([])
    ax2.set_ylim([0, 1])
    ax2.set_yticks(np.arange(0, 1.1, 0.1))
    ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    # Add overall title
    if title_prefix:
        fig.suptitle(title_prefix, fontsize=16, y=0.98)
    
    # Format p-value and t-statistic to 2 significant figures
    p_display = format_p_value_2sf(p_value)
    t_display = f'{t_stat:.2f}'
    
    # Add t-test and p-value in a box at the bottom center
    ttest_text = f't-test: t = {t_display}, p = {p_display}'
    fig.text(0.5, 0.02, ttest_text, 
             ha='center', fontsize=11, 
             color='gray', alpha=0.9,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                      edgecolor='lightgray', linewidth=0.8))
    
    plt.tight_layout(rect=[0, 0.05, 1, 0.98])
    
    # Save the plot
    plt.savefig(output_file, dpi=1000, bbox_inches='tight')
    
    plt.close()
#!/usr/bin/env python3
"""
Create box plots for troponin structures.
Separate figures: Cardiac and Skeletal, each with two box plots side by side.
Each figure takes half the space.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

# Set style for clean plots
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 1000
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans', 'sans-serif']




run_columns = [f'Run_{i}' for i in range(1, 101)]

def extract_probabilities(df):
    """Extract probability values: average over runs for each position."""
    available_runs = [col for col in run_columns if col in df.columns]
    avg_per_position = df[available_runs].mean(axis=1).values
    avg_per_position = avg_per_position[~np.isnan(avg_per_position)]
    return avg_per_position

def format_p_value_2sf(p_value):
    """Format p-value to 2 significant figures with leading zeros."""
    from math import floor, log10
    
    if p_value == 0:
        return '0.00'
    
    if p_value >= 1:
        # For values >= 1, use 2 significant figures
        exp = floor(log10(abs(p_value)))
        coeff = p_value / (10 ** exp)
        return f'{coeff:.2f}e{exp}' if exp > 0 else f'{p_value:.2f}'
    else:
        # For values < 1, calculate decimal places needed for 2 significant figures
        exp = floor(log10(abs(p_value)))
        # Number of decimal places = -exp + 1 (to show 2 significant figures)
        decimal_places = max(0, -exp + 1)
        return f'{p_value:.{decimal_places}f}'

def create_boxplot_figure(df1, df2, label1, label2, color1, color2, 
                          output_file, title_prefix=""):
    """
    Create a figure with two box plots side by side.
    """
    # Extract probabilities
    prob1 = extract_probabilities(df1)
    prob2 = extract_probabilities(df2)
    
    if len(prob1) == 0 or len(prob2) == 0:
        print(f"Warning: No probability values found")
        return
    
    # Perform t-test
    t_stat, p_value = ttest_ind(prob1, prob2)
    
    # Create figure with 1x2 subplots (half dimensions)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 5))
    
    # Calculate statistics for reference lines
    mean1 = np.mean(prob1)
    median1 = np.median(prob1)
    mean2 = np.mean(prob2)
    median2 = np.median(prob2)
    
    # Plot 1: First dataset
    bp1 = ax1.boxplot([prob1], 
                      patch_artist=True,
                      widths=0.6,
                      showmeans=True,
                      meanline=True)
    
    for patch in bp1['boxes']:
        patch.set_facecolor(color1)
        patch.set_alpha(0.7)
        patch.set_edgecolor('black')
        patch.set_linewidth(1.5)
    
    for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        if element in bp1:
            plt.setp(bp1[element], color='black', linewidth=1.5)
    
    # Add subtle reference lines for mean and median (no labels)
    ax1.axhline(y=mean1, color='gray', linestyle='--', linewidth=1, alpha=0.4)
    ax1.axhline(y=median1, color='gray', linestyle=':', linewidth=1, alpha=0.4)
    
    ax1.set_ylabel("Wildtype Probability", fontsize=12)
    ax1.set_title(label1, fontsize=14, pad=10)
    ax1.set_xticklabels([])
    ax1.set_ylim([0, 1])
    ax1.set_yticks(np.arange(0, 1.1, 0.1))
    ax1.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    # Plot 2: Second dataset
    bp2 = ax2.boxplot([prob2], 
                      patch_artist=True,
                      widths=0.6,
                      showmeans=True,
                      meanline=True)
    
    for patch in bp2['boxes']:
        patch.set_facecolor(color2)
        patch.set_alpha(0.7)
        patch.set_edgecolor('black')
        patch.set_linewidth(1.5)
    
    for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        if element in bp2:
            plt.setp(bp2[element], color='black', linewidth=1.5)
    
    ax2.axhline(y=mean2, color='gray', linestyle='--', linewidth=1, alpha=0.4)
    ax2.axhline(y=median2, color='gray', linestyle=':', linewidth=1, alpha=0.4)
    
    ax2.set_ylabel("Wildtype Probability", fontsize=12)
    ax2.set_title(label2, fontsize=14, pad=10)
    ax2.set_xticklabels([])
    ax2.set_ylim([0, 1])
    ax2.set_yticks(np.arange(0, 1.1, 0.1))
    ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    # Add overall title
    if title_prefix:
        fig.suptitle(title_prefix, fontsize=16, y=0.98)
    
    # Format p-value and t-statistic to 2 significant figures
    p_display = format_p_value_2sf(p_value)
    t_display = f'{t_stat:.2f}'
    
    # Add t-test and p-value in a box at the bottom center
    ttest_text = f't-test: t = {t_display}, p = {p_display}'
    fig.text(0.5, 0.02, ttest_text, 
             ha='center', fontsize=11, 
             color='gray', alpha=0.9,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                      edgecolor='lightgray', linewidth=0.8))
    
    plt.tight_layout(rect=[0, 0.05, 1, 0.98])
    
    # Save the plot
    plt.savefig(output_file, dpi=1000, bbox_inches='tight')
    
    plt.close()