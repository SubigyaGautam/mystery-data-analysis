#!/usr/bin/env python3
"""
Comprehensive Investigation of mystery.npy file
Weather Data Analysis and Visualization
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os

def basic_analysis(data):
    """Basic statistical analysis of the data"""
    print("=" * 60)
    print("BASIC DATA ANALYSIS")
    print("=" * 60)
    
    print(f"Data type: {data.dtype}")
    print(f"Shape: {data.shape}")
    print(f"Number of dimensions: {data.ndim}")
    print(f"Total elements: {data.size}")
    print(f"Memory usage: {data.nbytes / (1024*1024):.2f} MB")
    
    print(f"\nStatistical Information:")
    print(f"Min value: {np.min(data):.2f}")
    print(f"Max value: {np.max(data):.2f}")
    print(f"Mean: {np.mean(data):.2f}")
    print(f"Std deviation: {np.std(data):.2f}")
    print(f"Median: {np.median(data):.2f}")
    
    # Check for special values
    nan_count = np.isnan(data).sum()
    inf_count = np.isinf(data).sum()
    zero_count = (data == 0).sum()
    negative_count = (data < 0).sum()
    
    print(f"\nData Quality:")
    print(f"NaN values: {nan_count}")
    print(f"Infinite values: {inf_count}")
    print(f"Zero values: {zero_count}")
    print(f"Negative values: {negative_count}")

def analyze_dimensions(data):
    """Analyze what each dimension might represent"""
    print("\n" + "=" * 60)
    print("DIMENSIONAL ANALYSIS")
    print("=" * 60)
    
    height, width, depth = data.shape
    print(f"Dimension 0 (height): {height}")
    print(f"Dimension 1 (width): {width}")  
    print(f"Dimension 2 (depth): {depth}")
    
    # Common geospatial resolutions
    print(f"\nGeospatial Analysis:")
    print(f"Height/Width ratio: {height/width:.3f}")
    
    # Check if this matches common lat/lon grids
    if height == 720 and width == 1440:
        print("✓ This matches a 0.25° global grid (720x1440)!")
        print("  - Latitude: 90°S to 90°N in 0.25° steps")
        print("  - Longitude: 180°W to 180°E in 0.25° steps")
        lat_res = 180 / height
        lon_res = 360 / width
        print(f"  - Latitude resolution: {lat_res:.3f}°")
        print(f"  - Longitude resolution: {lon_res:.3f}°")
    
    # Analyze third dimension
    print(f"\nThird dimension analysis (depth={depth}):")
    if depth > 100:
        print("  - Likely time dimension (many time steps)")
        print(f"  - Could be ~{depth//30:.0f} months or {depth//12:.0f} years of data")
    elif depth < 50:
        print("  - Could be atmospheric levels or short time series")

def temporal_analysis(data):
    """Analyze temporal patterns"""
    print("\n" + "=" * 60)
    print("TEMPORAL PATTERN ANALYSIS")
    print("=" * 60)
    
    # Calculate global means for each time step
    global_means = np.nanmean(data, axis=(0, 1))
    
    print(f"Time series statistics:")
    print(f"Min global mean: {np.min(global_means):.2f}")
    print(f"Max global mean: {np.max(global_means):.2f}")
    print(f"Mean of means: {np.mean(global_means):.2f}")
    print(f"Std of means: {np.std(global_means):.2f}")
    
    # Look for seasonal patterns
    if len(global_means) >= 12:
        # Calculate potential seasonal cycle
        print(f"\nSeasonal Analysis (assuming monthly data):")
        months = len(global_means)
        years = months // 12
        if years > 0:
            monthly_means = np.zeros(12)
            for month in range(12):
                monthly_data = global_means[month::12]
                monthly_means[month] = np.mean(monthly_data)
            
            max_month = np.argmax(monthly_means) + 1
            min_month = np.argmin(monthly_means) + 1
            print(f"Highest values in month {max_month}")
            print(f"Lowest values in month {min_month}")
            print(f"Seasonal amplitude: {np.max(monthly_means) - np.min(monthly_means):.2f}")
    
    return global_means

def spatial_analysis(data):
    """Analyze spatial patterns"""
    print("\n" + "=" * 60)
    print("SPATIAL PATTERN ANALYSIS")
    print("=" * 60)
    
    # Calculate temporal mean
    temporal_mean = np.nanmean(data, axis=2)
    
    print(f"Spatial statistics:")
    print(f"Min spatial value: {np.nanmin(temporal_mean):.2f}")
    print(f"Max spatial value: {np.nanmax(temporal_mean):.2f}")
    
    # Find extreme locations
    max_loc = np.unravel_index(np.nanargmax(temporal_mean), temporal_mean.shape)
    min_loc = np.unravel_index(np.nanargmin(temporal_mean), temporal_mean.shape)
    
    # Convert to lat/lon if this is a global grid
    if data.shape[0] == 720 and data.shape[1] == 1440:
        max_lat = 90 - (max_loc[0] * 0.25)
        max_lon = -180 + (max_loc[1] * 0.25)
        min_lat = 90 - (min_loc[0] * 0.25)
        min_lon = -180 + (min_loc[1] * 0.25)
        
        print(f"\nExtreme locations (if global 0.25° grid):")
        print(f"Maximum at: {max_lat:.2f}°N, {max_lon:.2f}°E")
        print(f"Minimum at: {min_lat:.2f}°N, {min_lon:.2f}°E")
    
    return temporal_mean

def create_visualizations(data, global_means, temporal_mean):
    """Create visualizations"""
    print("\n" + "=" * 60)
    print("CREATING VISUALIZATIONS")
    print("=" * 60)
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 15))
    
    # 1. Time series plot
    ax1 = plt.subplot(2, 3, 1)
    plt.plot(global_means, 'b-', linewidth=1)
    plt.title('Global Mean Time Series')
    plt.xlabel('Time Index')
    plt.ylabel('Value')
    plt.grid(True, alpha=0.3)
    
    # 2. Spatial mean map
    ax2 = plt.subplot(2, 3, 2)
    im2 = plt.imshow(temporal_mean, cmap='RdYlBu_r', aspect='auto')
    plt.title('Temporal Mean (Spatial Pattern)')
    plt.xlabel('Longitude Index')
    plt.ylabel('Latitude Index')
    plt.colorbar(im2, shrink=0.8)
    
    # 3. Histogram
    ax3 = plt.subplot(2, 3, 3)
    plt.hist(data.flatten()[::10000], bins=50, alpha=0.7, color='green')
    plt.title('Data Distribution (Sample)')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.yscale('log')
    
    # 4. First time slice
    ax4 = plt.subplot(2, 3, 4)
    im4 = plt.imshow(data[:, :, 0], cmap='RdYlBu_r', aspect='auto')
    plt.title('First Time Slice')
    plt.xlabel('Longitude Index')
    plt.ylabel('Latitude Index')
    plt.colorbar(im4, shrink=0.8)
    
    # 5. Middle time slice
    ax5 = plt.subplot(2, 3, 5)
    mid_idx = data.shape[2] // 2
    im5 = plt.imshow(data[:, :, mid_idx], cmap='RdYlBu_r', aspect='auto')
    plt.title(f'Middle Time Slice (t={mid_idx})')
    plt.xlabel('Longitude Index')
    plt.ylabel('Latitude Index')
    plt.colorbar(im5, shrink=0.8)
    
    # 6. Last time slice
    ax6 = plt.subplot(2, 3, 6)
    im6 = plt.imshow(data[:, :, -1], cmap='RdYlBu_r', aspect='auto')
    plt.title('Last Time Slice')
    plt.xlabel('Longitude Index')
    plt.ylabel('Latitude Index')
    plt.colorbar(im6, shrink=0.8)
    
    plt.tight_layout()
    plt.savefig('analysis/mystery_data_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Saved visualization as 'analysis/mystery_data_analysis.png'")
    
    return fig

def identify_weather_events(data, global_means):
    """Identify interesting weather events"""
    print("\n" + "=" * 60)
    print("WEATHER EVENT IDENTIFICATION")
    print("=" * 60)
    
    # Look for extreme events in time series
    threshold_high = np.percentile(global_means, 95)
    threshold_low = np.percentile(global_means, 5)
    
    extreme_high = np.where(global_means > threshold_high)[0]
    extreme_low = np.where(global_means < threshold_low)[0]
    
    print(f"Extreme Events Analysis:")
    print(f"High threshold (95th percentile): {threshold_high:.2f}")
    print(f"Low threshold (5th percentile): {threshold_low:.2f}")
    print(f"Number of extreme high events: {len(extreme_high)}")
    print(f"Number of extreme low events: {len(extreme_low)}")
    
    if len(extreme_high) > 0:
        print(f"\nExtreme HIGH events at time indices: {extreme_high[:10]}")
    if len(extreme_low) > 0:
        print(f"Extreme LOW events at time indices: {extreme_low[:10]}")
    
    # Analyze spatial patterns during extreme events
    if len(extreme_high) > 0:
        extreme_high_pattern = np.mean(data[:, :, extreme_high], axis=2)
        print(f"\nDuring extreme HIGH events:")
        print(f"Peak spatial value: {np.nanmax(extreme_high_pattern):.2f}")
        
        # Find hotspot during extreme events
        max_loc = np.unravel_index(np.nanargmax(extreme_high_pattern), extreme_high_pattern.shape)
        if data.shape[0] == 720 and data.shape[1] == 1440:
            max_lat = 90 - (max_loc[0] * 0.25)
            max_lon = -180 + (max_loc[1] * 0.25)
            print(f"Hotspot location: {max_lat:.2f}°N, {max_lon:.2f}°E")

def main():
    """
    Comprehensive investigation of the mystery.npy file
    """
    filepath = "mystery.npy"
    
    try:
        # Check if file exists
        if not os.path.exists(filepath):
            print(f"Error: File '{filepath}' not found!")
            return
        
        print("=" * 60)
        print("MYSTERY DATA INVESTIGATION")
        print("=" * 60)
        print(f"File: {filepath}")
        print(f"File size: {os.path.getsize(filepath) / (1024*1024):.2f} MB")
        
        # Load the numpy array
        print("Loading numpy array...")
        data = np.load(filepath)
        
        # Run comprehensive analysis
        basic_analysis(data)
        analyze_dimensions(data)
        global_means = temporal_analysis(data)
        temporal_mean = spatial_analysis(data)
        
        # Create visualizations
        try:
            fig = create_visualizations(data, global_means, temporal_mean)
            plt.show()
        except Exception as e:
            print(f"Visualization error (matplotlib may not be available): {e}")
        
        # Identify weather events
        identify_weather_events(data, global_means)
        
        print("\n" + "=" * 60)
        print("INVESTIGATION COMPLETE")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error during investigation: {e}")

if __name__ == "__main__":
    main()
