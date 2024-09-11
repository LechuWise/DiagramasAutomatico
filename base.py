import matplotlib.pyplot as plt
import networkx as nx
import csv

G = nx.Graph()


# with open("Objetos.csv", newline='') as csvfile:
#     data = csv.reader(csvfile, delimiter=' ', quotechar='|')

# print(data)

#Se debe de crear un script para agregar todos los elementos a este diccionario
coleccionNodos = [
    ("F5",{"Subnet":""}),
    ("Vlan1",{"Subnet":"10.90.20.0/24"}),
    ("Vlan2",{"Subnet":"10.90.20.0/24"}),
    ("Vlan3",{"Subnet":"10.90.20.0/24"}),
    ("Vlan4",{"Subnet":"10.90.20.0/24"}),
    ("Nodo1",{"Subnet":""}),
    ("Nodo2",{"Subnet":""}),
]

G.add_nodes_from(coleccionNodos)

#Se debe de crear un script para agregar todas las relaciones a este diccionario
coleccionVertices = [
    ("F5","Vlan1", {"weigth":.10}),
    ("F5","Vlan2", {"weigth":.10}),
    ("F5","Vlan3", {"weigth":.10}),
    ("F5","Vlan4", {"weigth":.10}),
    ("Nodo1","Vlan3"),
    ("Nodo2","Vlan4")
]


G.add_edges_from(coleccionVertices)


for node,diccionario in G.nodes(data=True):
    print(node)
    print(diccionario)
    print("====================")

segmentosDeRed = {node:(diccionario["Subnet"]) for node,diccionario in G.nodes(data=True)}

print(segmentosDeRed)



pos={
    "F5":(3.5,1),
    "Vlan1":(2,3),
    "Vlan2":(3,3),
    "Vlan3":(4,3),
    "Vlan4":(5,3),
    "Nodo1":(4,6),
    "Nodo2":(5,6),
}

pos_Label={
    "F5":(2.8,1),
    "Vlan2":(3,4),
    "Vlan1":(2,4),
    "Vlan3":(4,4),
    "Vlan4":(5,4),
    "Nodo1":(4,7),
    "Nodo2":(5,7),
}

options = {
    "font_size": 10,
    "font_color": "white",
    "node_size": 2000,
    "node_color": "black",
    "edgecolors": "black",
    "linewidths": 5,
    "width": 5,
}
#label_options = {"ec": "k", "fc": "white", "alpha": 0.7}
#nx.draw_networkx(G, **options)
nx.draw_networkx(G, pos=pos, **options)
nx.draw_networkx_labels(G, pos=pos_Label, labels=segmentosDeRed)
# nx.draw_networkx_labls(G,)
# Set margins for the axes so that nodes aren't clipped
ax = plt.gca()
ax.margins(0.20)
plt.axis("off")
plt.show()