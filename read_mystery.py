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

def create_detailed_analysis(data, global_means, temporal_mean):
    """Create detailed weather analysis plots"""
    print("✓ Creating detailed weather analysis...")
    
    # Convert to more reasonable units for visualization
    data_display = data / 1000  # Convert to more manageable scale
    temporal_mean_display = temporal_mean / 1000
    global_means_display = global_means / 1000
    
    fig = plt.figure(figsize=(20, 15))
    
    # 1. Time series with reference lines
    ax1 = plt.subplot(3, 3, 1)
    plt.plot(global_means_display, 'b-', linewidth=2)
    plt.axhline(y=np.mean(global_means_display), color='r', linestyle='--', alpha=0.7, label='Mean')
    plt.axhline(y=np.percentile(global_means_display, 95), color='orange', linestyle='--', alpha=0.7, label='95th percentile')
    plt.title('Global Mean Time Series (Scaled)')
    plt.xlabel('Time Index')
    plt.ylabel('Value (scaled units)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 2. Spatial distribution
    ax2 = plt.subplot(3, 3, 2)
    im2 = plt.imshow(temporal_mean_display, cmap='RdYlBu_r', aspect='auto')
    plt.title('Temporal Mean Distribution')
    plt.xlabel('Longitude Index')
    plt.ylabel('Latitude Index')
    plt.colorbar(im2, shrink=0.8)
    
    # 3. First time slice
    ax3 = plt.subplot(3, 3, 3)
    im3 = plt.imshow(data_display[:, :, 0], cmap='RdYlBu_r', aspect='auto')
    plt.title('First Time Slice')
    plt.colorbar(im3, shrink=0.8)
    
    # 4. Middle time slice
    ax4 = plt.subplot(3, 3, 4)
    mid_idx = data.shape[2] // 2
    im4 = plt.imshow(data_display[:, :, mid_idx], cmap='RdYlBu_r', aspect='auto')
    plt.title(f'Middle Time Slice (t={mid_idx})')
    plt.colorbar(im4, shrink=0.8)
    
    # 5. Last time slice
    ax5 = plt.subplot(3, 3, 5)
    im5 = plt.imshow(data_display[:, :, -1], cmap='RdYlBu_r', aspect='auto')
    plt.title('Last Time Slice')
    plt.colorbar(im5, shrink=0.8)
    
    # 6. Standard deviation map
    ax6 = plt.subplot(3, 3, 6)
    std_map = np.std(data_display, axis=2)
    im6 = plt.imshow(std_map, cmap='plasma', aspect='auto')
    plt.title('Standard Deviation')
    plt.colorbar(im6, shrink=0.8)
    
    # 7. Histogram
    ax7 = plt.subplot(3, 3, 7)
    sample_data = data_display.flatten()[::10000]
    plt.hist(sample_data[sample_data > 0], bins=50, alpha=0.7, color='skyblue')
    plt.title('Data Distribution (Sample)')
    plt.xlabel('Value (scaled)')
    plt.ylabel('Frequency')
    plt.yscale('log')
    
    # 8. Seasonal cycle
    ax8 = plt.subplot(3, 3, 8)
    if len(global_means_display) >= 12:
        months = len(global_means_display)
        years = months // 12
        if years > 0:
            monthly_means = np.zeros(12)
            for month in range(12):
                monthly_data = global_means_display[month::12]
                monthly_means[month] = np.mean(monthly_data)
            
            plt.plot(range(1, 13), monthly_means, 'o-', linewidth=2, markersize=8)
            plt.title('Seasonal Cycle')
            plt.xlabel('Month')
            plt.ylabel('Mean Value (scaled)')
            plt.xticks(range(1, 13))
            plt.grid(True, alpha=0.3)
    
    # 9. Geographic overlay
    ax9 = plt.subplot(3, 3, 9)
    im9 = plt.imshow(temporal_mean_display, cmap='RdYlBu_r', aspect='auto')
    
    # Add coordinate grid
    lat_ticks = np.arange(0, 720, 120)
    lon_ticks = np.arange(0, 1440, 240)
    lat_labels = [f"{90 - (tick * 0.25):.0f}°N" for tick in lat_ticks]
    lon_labels = [f"{-180 + (tick * 0.25):.0f}°E" for tick in lon_ticks]
    
    plt.xticks(lon_ticks, lon_labels, rotation=45)
    plt.yticks(lat_ticks, lat_labels)
    plt.title('Geographic Grid Overlay')
    plt.colorbar(im9, shrink=0.8)
    
    plt.tight_layout()
    plt.savefig('analysis/detailed_weather_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Saved detailed analysis as 'analysis/detailed_weather_analysis.png'")
    
    return fig

def create_final_comprehensive_plots(data, global_means):
    """Create final comprehensive analysis plots"""
    print("✓ Creating final comprehensive analysis...")
    
    # Scale data for visualization
    data_scaled = data / 1000
    global_means_scaled = global_means / 1000
    temporal_mean_scaled = np.mean(data_scaled, axis=2)
    
    # Find extreme events
    max_idx = np.argmax(global_means)
    min_idx = np.argmin(global_means)
    
    fig = plt.figure(figsize=(24, 18))
    
    # 1. Time series with extremes marked
    ax1 = plt.subplot(3, 4, 1)
    plt.plot(global_means_scaled, 'b-', linewidth=2)
    plt.scatter([max_idx], [global_means_scaled[max_idx]], color='red', s=100, zorder=5, label='Max event')
    plt.scatter([min_idx], [global_means_scaled[min_idx]], color='blue', s=100, zorder=5, label='Min event')
    plt.title('Global Time Series with Extremes')
    plt.xlabel('Time Index')
    plt.ylabel('Value (scaled)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 2. Spatial mean
    ax2 = plt.subplot(3, 4, 2)
    im2 = plt.imshow(temporal_mean_scaled, cmap='RdBu_r', aspect='auto')
    plt.title('Temporal Mean')
    plt.colorbar(im2, shrink=0.8)
    
    # 3. Extreme high event
    ax3 = plt.subplot(3, 4, 3)
    im3 = plt.imshow(data_scaled[:, :, max_idx], cmap='Reds', aspect='auto')
    plt.title(f'Extreme High Event (t={max_idx})')
    plt.colorbar(im3, shrink=0.8)
    
    # 4. Extreme low event
    ax4 = plt.subplot(3, 4, 4)
    im4 = plt.imshow(data_scaled[:, :, min_idx], cmap='Blues', aspect='auto')
    plt.title(f'Extreme Low Event (t={min_idx})')
    plt.colorbar(im4, shrink=0.8)
    
    # 5. Anomaly map
    ax5 = plt.subplot(3, 4, 5)
    anomaly = data_scaled[:, :, max_idx] - temporal_mean_scaled
    im5 = plt.imshow(anomaly, cmap='RdBu_r', aspect='auto')
    plt.title('Anomaly Pattern')
    plt.colorbar(im5, shrink=0.8)
    
    # 6. Variability map
    ax6 = plt.subplot(3, 4, 6)
    variability = np.std(data_scaled, axis=2)
    im6 = plt.imshow(variability, cmap='plasma', aspect='auto')
    plt.title('Variability (Std Dev)')
    plt.colorbar(im6, shrink=0.8)
    
    # 7. Distribution
    ax7 = plt.subplot(3, 4, 7)
    sample_data = data_scaled.flatten()[::5000]
    plt.hist(sample_data[sample_data > 0], bins=100, alpha=0.7, color='green')
    plt.title('Value Distribution')
    plt.xlabel('Value (scaled)')
    plt.ylabel('Frequency')
    plt.yscale('log')
    
    # 8. Seasonal analysis
    ax8 = plt.subplot(3, 4, 8)
    if len(global_means_scaled) >= 12:
        months = len(global_means_scaled)
        years = months // 12
        if years > 0:
            monthly_means = np.zeros(12)
            monthly_std = np.zeros(12)
            for month in range(12):
                monthly_data = global_means_scaled[month::12]
                monthly_means[month] = np.mean(monthly_data)
                monthly_std[month] = np.std(monthly_data)
            
            plt.errorbar(range(1, 13), monthly_means, yerr=monthly_std, 
                        marker='o', capsize=5, linewidth=2)
            plt.title('Seasonal Pattern')
            plt.xlabel('Month')
            plt.ylabel('Mean ± Std (scaled)')
            plt.xticks(range(1, 13))
            plt.grid(True, alpha=0.3)
    
    # 9-12. Time evolution snapshots
    time_indices = [0, data.shape[2]//4, data.shape[2]//2, data.shape[2]-1]
    titles = ['Early Period', 'Quarter Point', 'Mid Period', 'Late Period']
    
    for i, (time_idx, title) in enumerate(zip(time_indices, titles)):
        ax = plt.subplot(3, 4, 9 + i)
        im = plt.imshow(data_scaled[:, :, time_idx], cmap='RdYlBu_r', aspect='auto')
        plt.title(f'{title} (t={time_idx})')
        plt.colorbar(im, shrink=0.6)
    
    plt.tight_layout()
    plt.savefig('analysis/final_mystery_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Saved final analysis as 'analysis/final_mystery_analysis.png'")
    
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
            print(f"Hotspot during extreme global mean events: {max_lat:.2f}°N, {max_lon:.2f}°E")
    
    # Find the TRUE global maximum location
    print(f"\nGLOBAL MAXIMUM ANALYSIS:")
    global_max_location = np.unravel_index(np.argmax(data), data.shape)
    if data.shape[0] == 720 and data.shape[1] == 1440:
        true_max_lat = 90 - (global_max_location[0] * 0.25)
        true_max_lon = -180 + (global_max_location[1] * 0.25)
        true_max_time = global_max_location[2]
        true_max_value = data[global_max_location]
        print(f"True global maximum: {true_max_value:.2f} units")
        print(f"Location: {true_max_lat:.2f}°N, {true_max_lon:.2f}°E")
        print(f"Time index: {true_max_time}")
        
        # Geographic interpretation
        if 70 <= true_max_lat <= 80 and 130 <= true_max_lon <= 140:
            print(f"✓ ARCTIC REGION: Laptev Sea, Northern Siberia")
            print(f"  This makes meteorological sense for extreme precipitation!")

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
            fig1 = create_visualizations(data, global_means, temporal_mean)
            fig2 = create_detailed_analysis(data, global_means, temporal_mean)
            fig3 = create_final_comprehensive_plots(data, global_means)
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
