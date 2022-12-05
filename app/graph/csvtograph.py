import csv
from GraphUtil import *
from ast import literal_eval

import community as community_louvain
import matplotlib.cm as cm
import networkx as nx
import pandas as pd
from operator import itemgetter
from matplotlib import pyplot as plt

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'services'))

import CsvServices

df = pd.read_csv('combine_all_dataset.csv')
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

# partition centrality
partition_centrality = nx.degree_centrality(G0)
max_partition_centrality = max(partition_centrality.items(), key=itemgetter(1))

# partition closeness
partition_closeness = nx.closeness_centrality(G0)
max_partition_closeness = max(partition_closeness.items(), key=itemgetter(1))

# partition betweenness
partition_betweenness = nx.betweenness_centrality(G0)
max_partition_betweenness = max(partition_betweenness.items(), key=itemgetter(1))

# Display the partition centrality,  closeness and betweenness
print("---Centrality---")
print(f"the node with id {max_partition_centrality[0]} has a degree centrality of {max_partition_centrality[1]:.2f} which is the maximum of the Graph")
print(f"the node with id {max_partition_closeness[0]} has a closeness centrality of {max_partition_closeness[1]:.2f} which is the maximum of the Graph")
print(f"the node with id {max_partition_betweenness[0]} has a betweenness centrality of {max_partition_betweenness[1]:.2f} which is the maximum of the Graph")

# Assign colors based on partition value
color_list = []

for parts in partition.values():
    if parts == 0:
        color_list.append('blue')
    elif parts == 1:
        color_list.append('green')
    elif parts == 2:
        color_list.append('red')
    elif parts == 3:
        color_list.append('orange')
    elif parts == 4:
        color_list.append('black')
    elif parts == 5:
        color_list.append('purple')
    elif parts == 6:
        color_list.append('olive')
    elif parts == 7:
        color_list.append('gold')
    elif parts == 8:
        color_list.append('violet')
    elif parts == 9:
        color_list.append('limegreen')
    elif parts == 10:
        color_list.append('darkorange')
    elif parts == 11:
        color_list.append('darkred')
    elif parts == 12:
        color_list.append('darkblue')
    elif parts == 13:
        color_list.append('grey')
    elif parts == 14:
        color_list.append('aqua')
    elif parts == 15:
        color_list.append('magenta')
    elif parts == 16:
        color_list.append('maroon')
    elif parts == 17:
        color_list.append('cyan')
    elif parts == 18:
        color_list.append('teal')
    elif parts == 19:
        color_list.append('indigo')      
    else:
        color_list.append('white')

# color for central node
node_central = ['44196397','1406990690']
color_central = ['orange','blue']

user_name = {}
for node in node_central:
    userdetail = getUser(node)
    for user in userdetail.data:
        #print(dir(user))
        print(user.username)
        user_name[node] = user.username

# Color the nodes according to their partition
cmap = cm.get_cmap('viridis', max(partition.values()) - 1)
nx.draw_networkx_nodes(G0, pos, partition.keys(), node_size=65,
                       cmap=cmap,alpha=0.6, node_color=color_list)
#Central Node
nx.draw_networkx_nodes(G0, pos, nodelist=node_central, node_size= 300,
                       cmap=cmap, node_shape="o", node_color=color_central)
nx.draw_networkx_edges(G0, pos, alpha=0.5, edge_color="black")
nx.draw_networkx_labels(G,pos,labels=user_name,font_size=12,font_color='red')
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