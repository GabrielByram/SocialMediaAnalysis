import csv
from GraphUtil import *
from ast import literal_eval

import community as community_louvain
import matplotlib.cm as cm
import networkx as nx
import pandas as pd
from matplotlib import pyplot as plt

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'services'))

import CsvServices

df = pd.read_csv('obama_trump_elon.csv')
df["AuthorID"] = df["AuthorID"].str.replace("'", "")
df["InReplyToUserID"] = df["InReplyToUserID"].str.replace("'", "")
df["MentionsID"] = df["MentionsID"].str.replace("'", "")

# This methods of structuring the nodes and edges is adding only AuthorID and MentionsID which is considered a path
# From the AuthorID to MentionsID

G = nx.from_pandas_edgelist(df, "AuthorID", "MentionsID")

G_nodes = G.number_of_nodes()
G_edges = G.number_of_edges()
print("Nodes = ", G_nodes, " Edges = ",G_edges)

if nx.is_connected(G):
    print("The graph is connected")
else:
    print("The graph is not connected")

print(f"There are {nx.number_connected_components(G)} connected components in the Graph")

# Find largest component 
Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
G0 = G.subgraph(Gcc[0])

nx.draw(G0)
plt.show()

fig, ax = plt.subplots(figsize=(15, 9))
ax.axis("off")
plot_options = {"node_size": 15, "with_labels": False, "width": 0.15}
nx.draw_networkx(G0, pos=nx.random_layout(G), ax=ax, **plot_options)
plt.show()

pos = nx.spring_layout(G0, iterations=15, seed=1721)
fig, ax = plt.subplots(figsize=(15, 9))
ax.axis("off")
plot_options = {"node_size": 15, "with_labels": False, "width": 0.15}
nx.draw_networkx(G0, pos=pos, ax=ax, **plot_options)
plt.show()

# louvian method
# compute the best partition
partition = community_louvain.best_partition(G0)

# draw graph
pos = nx.spring_layout(G0)

# color the nodes according to their partition
cmap = cm.get_cmap('viridis', max(partition.values()) - 1)
nx.draw_networkx_nodes(G0, pos, partition.keys(), node_size=40,
                       cmap=cmap, node_color=list(partition.values()))
nx.draw_networkx_edges(G0, pos, alpha=0.5)
plt.show()

# Get list of users by community
numOfCommunities = int(max(partition.values())) + 1
communityList = getCommunities(partition, numOfCommunities)

# Get csv of user info from users in each community
hasHeader = True
for communityNum in range(0, numOfCommunities):
    userInfo = getUserInfo(communityList, communityNum)
    CsvServices.CreateUsersInGraphCSV(userInfo, communityNum, hasHeader)
    hasHeader = False

# Display fields of each community in different graphs with MatPlotLib
displayCommunityCharts(numOfCommunities)