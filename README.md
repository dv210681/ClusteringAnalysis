# ClusteringAnalysis
Clustering and Visualization of River Data for Sf Distribution Analysis
Overview
This Python script performs PCA and KMeans clustering on river data related to slope, elevation, and water depth metrics. The goal is to group rivers into clusters based on these features, visualize the distribution of the Slope-Froude Number (Sf) across clusters, and display river names alongside each cluster for easy identification. Certain rivers are manually reassigned to specific clusters based on expert insights.

Features
Principal Component Analysis (PCA): Reduces dimensionality of standardized river data for easier visualization.
KMeans Clustering: Groups rivers into three clusters based on selected features.
Manual Reassignment of Clusters: Allows specific rivers to be assigned to desired clusters.
Visualization: Creates a violin plot of Sf distribution with river names displayed next to each cluster for easy identification.
Output Files: Saves the results as JPG, SVG, and interactive HTML formats.
Prerequisites
To run this script, you need the following Python packages:

pandas
seaborn
matplotlib
sklearn (scikit-learn)
mpld3 (for generating interactive HTML plots)
Installing Dependencies
You can install all required packages with:

bash
Copia codice
pip install pandas seaborn matplotlib scikit-learn mpld3
Files and Directory Structure
Input File:

Lakes_DeltaAnalysis_Complete_Info.xlsx: Contains river data with columns for river names, slope, elevation, water depth, and the Slope-Froude Number (Sf).
Output Files (Generated by the script):

CA_Cluster_Results_With_Names.xlsx: Contains the PCA components, Sf values, cluster assignments, and river names.
Cluster_Sf_Distribution_with_Names.jpg: A static JPEG plot of Sf distribution across clusters.
Cluster_Sf_Distribution_with_Names.svg: An SVG version of the plot.
Cluster_Sf_Distribution_with_Names.html: An interactive HTML version of the plot.
Script Details
Step-by-Step Explanation of the Code
Load and Prepare Data:

The script loads the river data from Lakes_DeltaAnalysis_Complete_Info.xlsx.
Selects specific features for analysis: "Slope Mean (°)", "Slope Std(°) ", "Mean Elevation(m)", "Median Elevation(m)", "Water depth(m)".
Attaches the "River name" column for tracking river names throughout the analysis.
Standardize Features:

Standardizes the features (excluding "River name") to ensure each feature contributes equally to the PCA and clustering analysis.
Principal Component Analysis (PCA):

Reduces the standardized features to two principal components (PC1 and PC2) for visualization and clustering.
Creates a DataFrame that includes the PCA results (PC1, PC2), river names, and Slope-Froude Number (Sf) if available.
KMeans Clustering:

Groups the rivers into three clusters using KMeans clustering.
Adds a "Cluster" column to the DataFrame to record each river's assigned cluster.
Manual Reassignment of Specific Rivers:

To incorporate expert insights, certain rivers are reassigned to specific clusters:
Muota and LeRhone are reassigned to Cluster 2.
Mülibach, Lutschine, Giessbach, Isentalerbach, and Riemnstaldnerbach are reassigned to Cluster 0.
Save Results:

The updated DataFrame, which includes PCA results, river names, Sf values, and cluster assignments, is saved to CA_Cluster_Results_With_Names.xlsx.
Visualization:

Creates a violin plot displaying the distribution of Sf across clusters.
Displays river names in a vertical list outside each violin for easy identification.
Overlays mean Sf markers for each cluster.
Output Files:

The plot is saved in JPG, SVG, and HTML formats, providing both static and interactive visualization options.
Code Structure
Here’s the structure of the code:

python
Copia codice
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import mpld3

# Define file paths
info_file_path = r'C:\path\to\Lakes_DeltaAnalysis_Complete_Info.xlsx'
cluster_results_file_path = r'C:\path\to\CA_Cluster_Results_With_Names.xlsx'

# Load the dataset with the correct header
original_data = pd.read_excel(info_file_path, header=0)

# Define features for analysis
features = ["Slope Mean (°)", "Slope Std(°) ", "Mean Elevation(m)", "Median Elevation(m)", "Water depth(m) "]
features_with_names = ["River name"] + features

# Prepare data for PCA with river names attached
data_with_names = original_data[features_with_names].dropna()
river_names = data_with_names["River name"]
X_scaled = StandardScaler().fit_transform(data_with_names[features])

# PCA Transformation
pca = PCA(n_components=2)
principal_components = pca.fit_transform(X_scaled)
pca_df = pd.DataFrame(data=principal_components, columns=["PC1", "PC2"])
pca_df["River name"] = river_names.values

# Include Slope-Froude Number (Sf) if available
if "Slope-Froude Number (SF)" in original_data.columns:
    pca_df["Sf"] = original_data.loc[river_names.index, "Slope-Froude Number (SF)"].values

# KMeans Clustering
kmeans = KMeans(n_clusters=3, random_state=0)
pca_df["Cluster"] = kmeans.fit_predict(principal_components)

# Manual Reassignments
pca_df.loc[pca_df["River name"].isin(["Muota", "LeRhone"]), "Cluster"] = 2
pca_df.loc[pca_df["River name"].isin(["Mülibach", "Lutschine
