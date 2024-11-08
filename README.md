# ClusteringAnalysis
Clustering and Visualization of River Data for Sf Distribution Analysis
Overview

README for Cluster Analysis with Manual Reassignment of Rivers
Overview
This script performs Principal Component Analysis (PCA) and KMeans clustering on river slope and elevation data, while ensuring specific rivers are assigned to predefined clusters. After clustering, the results are saved in multiple formats, and a violin plot displays the distribution of a slope-related variable (Sf) across clusters with annotated river names.

Requirements
Python 3.x
Required libraries:
pandas
seaborn
matplotlib
sklearn
mpld3
You can install the libraries with:

bash
Copia codice
pip install pandas seaborn matplotlib scikit-learn mpld3
File Structure and Paths
Input File
Lakes_DeltaAnalysis_Complete_Info.xlsx: An Excel file containing river data, including river names, slope, elevation, and additional metrics. This file is located at:
makefile
Copia codice
C:\Users\vendettuoli\Documents\Projects_2024\DeltasLakesSchweiz_Paper\Output\.excel\ClusterAnalysis\Lakes_DeltaAnalysis_Complete_Info.xlsx
Output Files
Clustering Results (Excel): The final PCA and clustering results with river names are saved to:

makefile
Copia codice
C:\Users\vendettuoli\Documents\Projects_2024\DeltasLakesSchweiz_Paper\Output\.excel\ClusterAnalysis\CA_Cluster_Results_With_Names.xlsx
Cluster Distribution Plot: The violin plot with annotated river names is saved in three formats:

JPG: Cluster_Sf_Distribution_with_Names.jpg
SVG: Cluster_Sf_Distribution_with_Names.svg
HTML (interactive): Cluster_Sf_Distribution_with_Names.html
Usage
Run the script by executing the following command in your terminal or command prompt:

bash
Copia codice
python cluster_analysis.py
Code Explanation
Import Libraries:

The necessary libraries (pandas, seaborn, matplotlib, sklearn, and mpld3) are imported.
File Paths:

Paths for the input Excel file and output files are defined.
Load Dataset:

The dataset is loaded from the Excel file with headers to ensure the correct column names are read.
The columns required for PCA and clustering are specified under features, which include slope and elevation metrics.
Data Preparation:

The river names are preserved separately for reassignment and labeling.
Only the selected features (excluding river names) are standardized using StandardScaler.
Principal Component Analysis (PCA):

PCA is applied to reduce the feature space to two principal components (PC1 and PC2), allowing for easier visualization and clustering.
KMeans Clustering:

KMeans clustering is performed with 3 clusters, and the results are added to the pca_df DataFrame.
Manual Cluster Reassignment:

Specific rivers are manually reassigned to desired clusters as follows:
Cluster 2: Muota and LeRhone
Cluster 0: Mülibach, Lutschine, Giessbach, Isentalerbach, and Riemnstaldnerbach
This is done by directly setting the Cluster column values for these rivers.
Save Results:

The pca_df DataFrame, containing PCA results, cluster assignments, and river names, is saved to an Excel file.
Visualization:

A violin plot displays the distribution of Sf across the clusters.
Each cluster is shown with a unique color.
River names are displayed outside the violin plot for each cluster, positioned vertically for clarity.
Save Plot:

The plot is saved in three formats: JPG, SVG, and HTML (interactive with mpld3).
Key Parameters
n_clusters: Number of clusters for KMeans (n_clusters=3). This can be modified within the code to change the number of clusters.
Example Output
The output will include:

An Excel file (CA_Cluster_Results_With_Names.xlsx) with PCA components, cluster assignments, Sf values, and river names.
A violin plot showing the Sf distribution across clusters, with each cluster annotated with river names positioned outside the violin.
Notes
Manual Reassignment: Specific rivers are manually reassigned to certain clusters based on domain knowledge or prior requirements.
Plot Customization: The colors and positioning of river names in the plot can be adjusted in the code by modifying the palette dictionary and x_offsets list.
Example of Key Code Sections
Manual Cluster Reassignment
python
Copia codice
# Manually reassign specific rivers to clusters
# Muota and LeRhone to Cluster 2
rivers_to_cluster_2 = ["Muota", "LeRhone"]
pca_df.loc[pca_df["River name"].isin(rivers_to_cluster_2), "Cluster"] = 2

# Mülibach, Lutschine, Giessbach, Isentalerbach, and Riemnstaldnerbach to Cluster 0
rivers_to_cluster_0 = ["Mülibach", "Lutschine", "Giessbach", "Isentalerbach", "Riemnstaldnerbach"]
pca_df.loc[pca_df["River name"].isin(rivers_to_cluster_0), "Cluster"] = 0
Violin Plot with River Names
python
Copia codice
# Add river names outside each cluster's violin
river_names_by_cluster = pca_df.groupby("Cluster")["River name"].apply(list)
x_offsets = [-0.3, 0, 0.3]
for cluster, names in river_names_by_cluster.items():
    y_pos = 0.012
    for name in names:
        plt.text(cluster + x_offsets[cluster], y_pos, name, ha="center", va="top", fontsize=8)
        y_pos -= 0.0008
Troubleshooting
KeyError for Column Names: Ensure that the exact column names in the Excel file match the features list in the code.
Missing Libraries: Install required libraries via pip if any ModuleNotFoundError appears.
FileNotFoundError: Verify the file paths are correct and accessible.
