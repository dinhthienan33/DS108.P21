import pandas as pd
import numpy as np
import re
import os
import zipfile
import urllib.request

# Define paths
data_url = "https://d396qusza40orc.cloudfront.net/getdata%2Fprojectfiles%2FUCI%20HAR%20Dataset.zip"
zip_file_path = "human_activity.zip"
data_dir = "human_activity"
dataset_path = os.path.join(data_dir, "UCI HAR Dataset")

def download_data():
    """Step 1: Download and extract the dataset if it doesn't exist"""
    # Skip download if dataset already exists
    if not os.path.exists(dataset_path):
        # Download the zip file if it doesn't exist
        if not os.path.exists(zip_file_path):
            print("Downloading dataset...")
            urllib.request.urlretrieve(data_url, zip_file_path)
        
        # Create directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Extract the zip file
        print("Extracting dataset...")
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(data_dir)
    
    print("Dataset is ready.")

def process_data():
    """Steps 2-9: Process the data according to instructions"""
    
    # Step 2: Read data (This is for the PDF report)
    # The actual reading of the README.txt will be done separately
    
    # Read training data
    print("Reading training data...")
    X_train = pd.read_csv(os.path.join(dataset_path, "train/X_train.txt"), sep=r'\s+', header=None)
    y_train = pd.read_csv(os.path.join(dataset_path, "train/y_train.txt"), header=None, names=["Activity"])
    subject_train = pd.read_csv(os.path.join(dataset_path, "train/subject_train.txt"), header=None, names=["Subject"])
    
    # Read test data
    print("Reading test data...")
    X_test = pd.read_csv(os.path.join(dataset_path, "test/X_test.txt"), sep=r'\s+', header=None)
    y_test = pd.read_csv(os.path.join(dataset_path, "test/y_test.txt"), header=None, names=["Activity"])
    subject_test = pd.read_csv(os.path.join(dataset_path, "test/subject_test.txt"), header=None, names=["Subject"])
    
    # Step 3: Assign attribute names
    print("Assigning attribute names...")
    features = pd.read_csv(os.path.join(dataset_path, "features.txt"), sep=r'\s+', header=None, 
                           names=["feature_id", "feature_name"])
    feature_names = features["feature_name"].values
    
    # Set feature names as column names for X_train and X_test
    X_train.columns = feature_names
    X_test.columns = feature_names
    
    # Step 4: Merge data
    print("Merging datasets...")
    # Merge training data: y_train, subject_train, X_train
    X_train_data = pd.concat([y_train, subject_train, X_train], axis=1)
    
    # Merge test data: y_test, subject_test, X_test
    X_test_data = pd.concat([y_test, subject_test, X_test], axis=1)
    
    # Merge train and test data
    X_data = pd.concat([X_train_data, X_test_data], axis=0)
    
    # Step 5: Extract mean and standard deviation features
    print("Extracting mean and standard deviation features...")
    # Get column names
    col_names = X_data.columns
    
    # Find indices of columns with 'mean()' or 'std()' in their names
    mean_cols = [col for col in col_names if re.search(r'mean\(\)', col)]
    std_cols = [col for col in col_names if re.search(r'std\(\)', col)]
    
    # Select only the columns we want (including 'Activity' and 'Subject')
    selected_cols = ['Activity', 'Subject'] + mean_cols + std_cols
    X_mean_std = X_data[selected_cols]
    
    # Step 6: Rename attributes to be more meaningful
    print("Renaming attributes...")
    # Define patterns to replace as per the table in instructions
    patterns = {
        r'^t': 'Time domain: ',
        r'^f': 'Frequency domain: ',
        r'-': ', ',
        r'mean\(\)': 'mean value',
        r'std\(\)': 'standard deviation value',
        r'-X': ' on X axis',
        r'-Y': ' on Y axis',
        r'-Z': ' on Z axis',
        r'AccJerk': 'acceleration jerk',
        r'Acc': 'acceleration',
        r'GyroJerk': 'angular velocity jerk',
        r'Gyro': 'angular velocity',
        r'Mag': 'magnitude'
    }
    
    # Apply the replacements
    new_col_names = X_mean_std.columns.to_list()
    for i, col in enumerate(new_col_names):
        if col not in ['Activity', 'Subject']:
            for pattern, replacement in patterns.items():
                col = re.sub(pattern, replacement, col)
            new_col_names[i] = col
    
    X_mean_std.columns = new_col_names
    
    # Step 7: Calculate average of each variable for each activity and subject
    print("Calculating averages by Activity and Subject...")
    tidy_data = X_mean_std.groupby(['Activity', 'Subject']).mean().reset_index()
    
    # Step 8: Replace Activity IDs with descriptive names
    print("Replacing Activity IDs with descriptive names...")
    activity_labels = pd.read_csv(os.path.join(dataset_path, "activity_labels.txt"), 
                                  sep=r'\s+', 
                                  header=None, 
                                  names=["Activity_ID", "Activity_Name"])
    
    # Method 2: Using merge 
    # Save the original Activity column (which contains IDs) as a separate column
    tidy_data["Activity_ID"] = tidy_data["Activity"]
    
    # Merge with activity labels
    tidy_data = pd.merge(tidy_data, activity_labels, left_on="Activity_ID", right_on="Activity_ID")
    
    # Replace the Activity column with Activity_Name and drop redundant columns
    tidy_data["Activity"] = tidy_data["Activity_Name"]
    tidy_data = tidy_data.drop(["Activity_Name", "Activity_ID"], axis=1)
    
    # Step 9: Save the tidy data
    print("Saving tidy data to CSV...")
    tidy_data.to_csv("tidy_data.csv", index=False)
    
    print(f"Tidy data has been created with {tidy_data.shape[0]} rows and {tidy_data.shape[1]} columns.")
    return tidy_data

if __name__ == "__main__":
    # Step 1: Download and prepare data
    download_data()
    
    # Steps 2-9: Process data and create tidy dataset
    tidy_data = process_data()
    
    print("Processing complete. The tidy data has been saved as 'tidy_data.csv'.") 