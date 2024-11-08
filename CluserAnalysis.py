import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import mpld3

# Define file paths
info_file_path = r'C:\Users\vendettuoli\Documents\Projects_2024\DeltasLakesSchweiz_Paper\Output\.excel\ClusterAnalysis\Lakes_DeltaAnalysis_Complete_Info.xlsx'
cluster_results_file_path = r'C:\Users\vendettuoli\Documents\Projects_2024\DeltasLakesSchweiz_Paper\Output\.excel\ClusterAnalysis\CA_Cluster_Results_With_Names.xlsx'

# Load the dataset with the correct header
original_data = pd.read_excel(info_file_path, header=0)

# Define features list based on the actual column names
features = ["Slope Mean (°)", "Slope Std(°) ", "Mean Elevation(m)", "Median Elevation(m)", "Water depth(m) "]

# Add River names to the features for tracking
features_with_names = ["River name"] + features

# Select relevant features and prepare data for PCA, ensuring "River name" is included
data_with_names = original_data[features_with_names].dropna()

# Separate river names to reattach later
river_names = data_with_names["River name"]

# Standardize the features, excluding "River name"
scaler = StandardScaler()
X_scaled = scaler.fit_transform(data_with_names[features])

# Perform PCA
pca = PCA(n_components=2)
principal_components = pca.fit_transform(X_scaled)

# Create a DataFrame for PCA results, including river names and 'Slope-Froude Number (SF)' if available
pca_df = pd.DataFrame(data=principal_components, columns=["PC1", "PC2"])
pca_df["River name"] = river_names.values  # Reattach river names
if "Slope-Froude Number (SF)" in original_data.columns:
    pca_df["Sf"] = original_data.loc[river_names.index, "Slope-Froude Number (SF)"].values
else:
    print("Warning: 'Slope-Froude Number (SF)' column not found in the data.")

# Apply KMeans Clustering
kmeans = KMeans(n_clusters=3, random_state=0)
pca_df["Cluster"] = kmeans.fit_predict(principal_components)

# Manually reassign specific rivers to clusters
# Muota and LeRhone to Cluster 2
rivers_to_cluster_2 = ["Muota", "LeRhone"]
pca_df.loc[pca_df["River name"].isin(rivers_to_cluster_2), "Cluster"] = 2

# Mülibach, Lutschine, Giessbach, Isentalerbach, and Riemnstaldnerbach to Cluster 0
rivers_to_cluster_0 = ["Mülibach", "Lutschine", "Giessbach", "Isentalerbach", "Riemnstaldnerbach"]
pca_df.loc[pca_df["River name"].isin(rivers_to_cluster_0), "Cluster"] = 0

# Save PCA and clustering results with river names to an Excel file
pca_df.to_excel(cluster_results_file_path, index=False)
print(f'PCA and clustering results with river names saved to {cluster_results_file_path}')

# Display a filtered view of the clusters for specified rivers to verify cluster assignment
rivers_to_check = ["Muota", "LeRhone", "Mülibach", "Lutschine", "Giessbach", "Isentalerbach", "Riemnstaldnerbach"]
filtered_pca_df = pca_df[pca_df["River name"].isin(rivers_to_check)]
print("Filtered Clustering Results for Specified Rivers:")
print(filtered_pca_df)

# Plot the distribution of Sf across clusters with river names outside the violins
plt.figure(figsize=(12, 8))
palette = {0: "skyblue", 1: "lightgreen", 2: "salmon"}
sns.violinplot(x="Cluster", y="Sf", hue="Cluster", data=pca_df, inner="point", palette=palette, legend=False)

# Overlay mean markers for each cluster
for i in range(3):
    mean_sf = pca_df[pca_df["Cluster"] == i]["Sf"].mean()
    plt.scatter(i, mean_sf, color='black', marker='*', s=100, label=f'Cluster {i} Mean' if i == 0 else "")

# Add river names outside each cluster's violin
river_names_by_cluster = pca_df.groupby("Cluster")["River name"].apply(list)
x_offsets = [-0.3, 0, 0.3]
for cluster, names in river_names_by_cluster.items():
    y_pos = 0.012
    for name in names:
        plt.text(cluster + x_offsets[cluster], y_pos, name, ha="center", va="top", fontsize=8)
        y_pos -= 0.0008

# Add legend and labels
plt.legend()
plt.title("Sf Distribution Across Clusters with Separated Vertical Lists of River Names")
plt.xlabel("Cluster")
plt.ylabel("Sf")

# Save plot in multiple formats
plt.savefig(r'C:\Users\vendettuoli\Documents\Projects_2024\DeltasLakesSchweiz_Paper\Output\.excel\ClusterAnalysis\Cluster_Sf_Distribution_with_Names.jpg', format='jpg')
plt.savefig(r'C:\Users\vendettuoli\Documents\Projects_2024\DeltasLakesSchweiz_Paper\Output\.excel\ClusterAnalysis\Cluster_Sf_Distribution_with_Names.svg', format='svg')

# Save as HTML using mpld3 for interactive output
html_content = mpld3.fig_to_html(plt.gcf())
with open(r'C:\Users\vendettuoli\Documents\Projects_2024\DeltasLakesSchweiz_Paper\Output\.excel\ClusterAnalysis\Cluster_Sf_Distribution_with_Names.html', 'w') as f:
    f.write(html_content)

# Show plot
plt.show()








