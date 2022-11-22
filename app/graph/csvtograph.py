import csv
from ast import literal_eval

import networkx as nx
import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('tweets_user.csv')
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

nx.draw(G)
plt.show()

fig, ax = plt.subplots(figsize=(15, 9))
ax.axis("off")
plot_options = {"node_size": 15, "with_labels": False, "width": 0.15}
nx.draw_networkx(G, pos=nx.random_layout(G), ax=ax, **plot_options)
plt.show()

pos = nx.spring_layout(G, iterations=15, seed=1721)
fig, ax = plt.subplots(figsize=(15, 9))
ax.axis("off")
plot_options = {"node_size": 15, "with_labels": False, "width": 0.15}
nx.draw_networkx(G, pos=pos, ax=ax, **plot_options)
plt.show()
