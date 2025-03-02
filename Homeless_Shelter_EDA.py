# -*- coding: utf-8 -*-
"""

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m-lH0r1FCkL2dd8gApmJArisUS0YYNBk

# Preparing Dataset
"""

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from matplotlib.backends.backend_pdf import PdfPages


sns.set(style="whitegrid", context="talk")

def load_dataset(file_path):
    try:
        data = pd.read_excel(file_path)
        print("Dataset loaded successfully.")
        return data
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

def print_dataset_summary(data):
    print("Data Information:")
    print(data.info())
    print("\nFirst 10 Rows:")
    print(data.head(10))
    print("\nSummary Statistics (Numerical):")
    print(data.describe())
    print("\nSummary Statistics (Categorical):")
    print(data.describe(include=['O']))
    print("\nMissing Values:")
    print(data.isnull().sum())

# Function to run t-tests and report on the differences between program models
def run_statistical_tests(data):
    # Split the data into Emergency and Transitional groups
    emergency = data[data['PROGRAM_MODEL'] == 'Emergency']
    transitional = data[data['PROGRAM_MODEL'] == 'Transitional']
    
    # Calculate the means for occupancy rates
    mean_beds_emergency = emergency['OCCUPANCY_RATE_BEDS'].mean()
    mean_beds_transitional = transitional['OCCUPANCY_RATE_BEDS'].mean()
    mean_rooms_emergency = emergency['OCCUPANCY_RATE_ROOMS'].mean()
    mean_rooms_transitional = transitional['OCCUPANCY_RATE_ROOMS'].mean()
    
    print("\nMean Occupancy Rates:")
    print(f"Beds - Emergency: {mean_beds_emergency:.2f}, Transitional: {mean_beds_transitional:.2f}")
    print(f"Rooms - Emergency: {mean_rooms_emergency:.2f}, Transitional: {mean_rooms_transitional:.2f}")
    
    # Perform Welch's t-tests 
    t_beds, p_beds = stats.ttest_ind(emergency['OCCUPANCY_RATE_BEDS'].dropna(), 
                                     transitional['OCCUPANCY_RATE_BEDS'].dropna(), 
                                     equal_var=False)
    t_rooms, p_rooms = stats.ttest_ind(emergency['OCCUPANCY_RATE_ROOMS'].dropna(), 
                                       transitional['OCCUPANCY_RATE_ROOMS'].dropna(), 
                                       equal_var=False)
    
    print("\nT-test Results for Occupancy Rates:")
    print(f"Beds: t-stat = {t_beds:.4f}, p-value = {p_beds:.4f}")
    print(f"Rooms: t-stat = {t_rooms:.4f}, p-value = {p_rooms:.4f}")
    
    # Check significance at alpha = 0.05
    alpha = 0.05
    if p_beds < alpha:
        print("There is a significant difference in bed occupancy rates between program models.")
    else:
        print("No significant difference found in bed occupancy rates.")
    
    if p_rooms < alpha:
        print("There is a significant difference in room occupancy rates between program models.")
    else:
        print("No significant difference found in room occupancy rates.")
    
    # T-test for service user count
    t_users, p_users = stats.ttest_ind(emergency['SERVICE_USER_COUNT'].dropna(),
                                       transitional['SERVICE_USER_COUNT'].dropna(),
                                       equal_var=False)
    mean_users_emergency = emergency['SERVICE_USER_COUNT'].mean()
    mean_users_transitional = transitional['SERVICE_USER_COUNT'].mean()
    
    print("\nService User Count Analysis:")
    print(f"Emergency Mean: {mean_users_emergency:.2f}, Transitional Mean: {mean_users_transitional:.2f}")
    print(f"T-test: t-stat = {t_users:.4f}, p-value = {p_users:.4f}")
    
    if p_users < alpha:
        print("Service User Count differs significantly between program models.")
    else:
        print("No significant difference in Service User Count between program models.")


def create_visualizations(data, pdf_handle):
    if 'OCCUPANCY_DATE' in data.columns:
        data['OCCUPANCY_DATE'] = pd.to_datetime(data['OCCUPANCY_DATE'], errors='coerce')
    
    # 1. Scatter plot: Actual Capacity vs Occupied Beds
    plt.figure(figsize=(9, 6))
    sns.scatterplot(x='CAPACITY_ACTUAL_BED', y='OCCUPIED_BEDS', data=data, hue='PROGRAM_MODEL', palette="Set2")
    plt.title('Actual Capacity vs Occupied Beds')
    plt.xlabel('Actual Bed Capacity')
    plt.ylabel('Occupied Beds')
    pdf_handle.savefig()
    plt.close()
    
    # 2. Boxplot: Occupied Beds by Program Model
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='PROGRAM_MODEL', y='OCCUPIED_BEDS', data=data, palette="Pastel1")
    plt.title('Occupied Beds by Program Model')
    plt.xlabel('Program Model')
    plt.ylabel('Occupied Beds')
    plt.xticks(rotation=45)
    pdf_handle.savefig()
    plt.close()
    
    # 3. Histogram: Distribution of Service User Count
    plt.figure(figsize=(8, 6))
    sns.histplot(data['SERVICE_USER_COUNT'].dropna(), bins=20, kde=True, color='skyblue')
    plt.title('Distribution of Service User Count')
    plt.xlabel('Service User Count')
    plt.ylabel('Frequency')
    pdf_handle.savefig()
    plt.close()
    
    # 4. Time series: Occupied Beds over Time
    if 'OCCUPANCY_DATE' in data.columns:
        plt.figure(figsize=(12, 6))
        sns.lineplot(x='OCCUPANCY_DATE', y='OCCUPIED_BEDS', data=data, marker='o', color='coral')
        plt.title('Occupied Beds Over Time')
        plt.xlabel('Date')
        plt.ylabel('Occupied Beds')
        pdf_handle.savefig()
        plt.close()
    
    # 5. Boxplot: Occupied Beds by Sector
    if 'SECTOR' in data.columns:
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='SECTOR', y='OCCUPIED_BEDS', data=data, palette="Set3")
        plt.title('Occupied Beds by Sector')
        plt.xlabel('Sector')
        plt.ylabel('Occupied Beds')
        pdf_handle.savefig()
        plt.close()
    
    # 6. Boxplot: Service User Count by Overnight Service Type
    if 'OVERNIGHT_SERVICE_TYPE' in data.columns:
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='OVERNIGHT_SERVICE_TYPE', y='SERVICE_USER_COUNT', data=data, palette="coolwarm")
        plt.title('Service User Count by Overnight Service Type')
        plt.xlabel('Overnight Service Type')
        plt.ylabel('Service User Count')
        plt.xticks(rotation=45)
        pdf_handle.savefig()
        plt.close()
    
    # 7. Boxplot: Service User Count by Capacity Type
    if 'CAPACITY_TYPE' in data.columns:
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='CAPACITY_TYPE', y='SERVICE_USER_COUNT', data=data, palette="Accent")
        plt.title('Service User Count by Capacity Type')
        plt.xlabel('Capacity Type')
        plt.ylabel('Service User Count')
        pdf_handle.savefig()
        plt.close()
    
    # 8. Boxplot: Occupancy Rate (Beds) by Program Model
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='PROGRAM_MODEL', y='OCCUPANCY_RATE_BEDS', data=data, palette="Blues")
    plt.title('Occupancy Rate (Beds) by Program Model')
    plt.xlabel('Program Model')
    plt.ylabel('Occupancy Rate (Beds)')
    pdf_handle.savefig()
    plt.close()
    
    # 9. Violin Plot: Occupancy Rate (Beds) Distribution
    plt.figure(figsize=(12, 8))
    sns.violinplot(x='PROGRAM_MODEL', y='OCCUPANCY_RATE_BEDS', data=data, palette="Pastel2")
    plt.title('Distribution of Occupancy Rate (Beds)')
    plt.xlabel('Program Model')
    plt.ylabel('Occupancy Rate (Beds)')
    pdf_handle.savefig()
    plt.close()
    
    # 10. Violin Plot: Occupancy Rate (Rooms) Distribution
    plt.figure(figsize=(12, 8))
    sns.violinplot(x='PROGRAM_MODEL', y='OCCUPANCY_RATE_ROOMS', data=data, palette="Pastel2")
    plt.title('Distribution of Occupancy Rate (Rooms)')
    plt.xlabel('Program Model')
    plt.ylabel('Occupancy Rate (Rooms)')
    pdf_handle.savefig()
    plt.close()
    
    # 11. Heatmap: Correlation among key variables
    columns_of_interest = ['SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 'OCCUPIED_BEDS', 
                           'CAPACITY_ACTUAL_ROOM', 'OCCUPIED_ROOMS', 'OCCUPANCY_RATE_BEDS', 'OCCUPANCY_RATE_ROOMS']
    cols = [col for col in columns_of_interest if col in data.columns]
    if len(cols) > 1:
        corr = data[cols].corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Matrix')
        pdf_handle.savefig()
        plt.close()
    
    # 12. Count plot: Number of entries per Program Model
    plt.figure(figsize=(10, 6))
    sns.countplot(x='PROGRAM_MODEL', data=data, palette="viridis")
    plt.title('Count by Program Model')
    plt.xlabel('Program Model')
    plt.ylabel('Count')
    pdf_handle.savefig()
    plt.close()
    
    # Count plot: Number of entries per Sector (if available)
    if 'SECTOR' in data.columns:
        plt.figure(figsize=(10, 6))
        sns.countplot(x='SECTOR', data=data, palette="magma")
        plt.title('Count by Sector')
        plt.xlabel('Sector')
        plt.ylabel('Count')
        pdf_handle.savefig()
        plt.close()

def main():
    file_path = '/content/Homeless Shelter Data.xlsx'
    data = load_dataset(file_path)
    if data is None:
        return
    
    print_dataset_summary(data)
    
    run_statistical_tests(data)
    
    # Save plots in a PDF report
    pdf_file = 'output_report.pdf'
    with PdfPages(pdf_file) as pdf:
        create_visualizations(data, pdf)
    print(f"\nReport has been saved to '{pdf_file}'.")

if __name__ == "__main__":
    main()
