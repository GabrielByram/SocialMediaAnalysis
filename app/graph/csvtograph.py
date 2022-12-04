import csv
from GraphUtil import *
from ast import literal_eval

import community as community_louvain
import matplotlib.cm as cm
import networkx as nx
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import colors as colorPalette

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'services'))

import CsvServices

# Draw Graphs with different layouts.
def drawDifferentLayoutGraphs(graph, connnected_component):
    # Plain Graph with no layout
    nx.draw(graph)
    plt.show()

    fig, ax = plt.subplots(figsize=(15, 9))
    ax.axis("off")
    plot_options = {"node_size": 15, "with_labels": False, "width": 0.15}
    nx.draw_networkx(connnected_component, pos=nx.random_layout(G), ax=ax, **plot_options)
    plt.show()

    # Spring Layout
    pos = nx.spring_layout(connnected_component, iterations=15, seed=1721)
    fig, ax = plt.subplots(figsize=(15, 9))
    ax.axis("off")
    plot_options = {"node_size": 15, "with_labels": False, "width": 0.15}
    nx.draw_networkx(G0, pos=pos, ax=ax, **plot_options)
    plt.show()

def getNodesFromGivenCommunity(communities , community_number):
    nodes = []

    for node_id in communities.keys():
        if(communities[node_id] == community_number):
            nodes.append(node_id)

    return nodes

# Draw graph with the communities.
def drawCommunityGraph(graph, communities,colors):
    communities_count = int(max(communities.values())) + 1
    
    fig, ax = plt.subplots(figsize=(15, 9))

    # Draws the graph with the given layout.
    pos = nx.spring_layout(graph)

    for index , color in enumerate(colors):
        nodes = getNodesFromGivenCommunity(communities, index)
        nx.draw_networkx_nodes(G0, pos, nodelist= nodes, node_size=30,
                        node_color=color,alpha = 1)
    
    nx.draw_networkx_edges(G0, pos, alpha=1)
    ax.set_title("Communities In Graph")
    plt.show()

def generateGraphFrom(file_loc):
    df = pd.read_csv('obama_trump_elon.csv')
    df["AuthorID"] = df["AuthorID"].str.replace("'", "")
    df["InReplyToUserID"] = df["InReplyToUserID"].str.replace("'", "")
    df["MentionsID"] = df["MentionsID"].str.replace("'", "")

    # This methods of structuring the nodes and edges is adding only AuthorID and MentionsID which is considered a path
    # From the AuthorID to MentionsID
    G = nx.from_pandas_edgelist(df, "AuthorID", "MentionsID")

    return G

G = generateGraphFrom('cristiano_neymar_realmadrid_championsleague.csv')

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

# louvian method
# compute the louvian communities to parition the graph.
partition = community_louvain.best_partition(G0)

# Get list of users by community
numOfCommunities = int(max(partition.values())) + 1

communityList = getCommunities(partition, numOfCommunities)

# Get csv of user info from users in each community
hasHeader = True
for communityNum in range(0, numOfCommunities):
    userInfo = getUserInfo(communityList, communityNum)
    CsvServices.CreateUsersInGraphCSV(userInfo, communityNum, hasHeader)
    hasHeader = False

# Get color maps.
color_maps = cm.get_cmap('tab20b',numOfCommunities)
color_list = [colorPalette.rgb2hex(color_maps(index)[:3]) for index in range(color_maps.N)]

#drawDifferentLayoutGraphs(G,G0)
drawCommunityGraph(G0,partition,color_list)
displayCommunityCharts(numOfCommunities,color_list)