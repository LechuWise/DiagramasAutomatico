import matplotlib.pyplot as plt
import networkx as nx
import PIL
import csv
from operator import itemgetter
# ==============================Funciones=================================
nombre = "nbm2padm6l.mx.nextgen.igrupobbva"
#Lectura de archivo .csv
def CargaDatos():
    csvfile = open(nombre + ".csv", "r")
    data = csv.reader(csvfile)
    for row in data:
        check = row[0]
        match check:
            case "SelfIP":
                listaSelfIP.append(row)
            case "Nodos":
                listaNodos.append(row)
            case "VirtualServer":
                listaVirtual.append(row)
            case "VlanBase":
                listaVlan.append(row)
            case "Rutas":
                listaRutas.append(row)
    csvfile.close()
#Pasar lista de numeros a direccion IP
def ListaDireccionIP(lista):
    direccionIP = ""
    for i in range(1, len(lista)):
        direccionIP = direccionIP + str(lista[i]) 
        if (i != (len(lista) -1)):
            direccionIP = direccionIP + "."
    #print(direccionIP)
    return direccionIP
#Objetos maximo y minimo
def LabelsObjetos(listaObjetos, desplazamiento):
    for i in range(0, len(listaVlan)):
        listatemp = []
        for j in range(0, len(listaObjetos)):
            if (listaObjetos[j][0] == i):
                listatemp.append(list(map(int, listaObjetos[j])))
        print(i)
        listaOrdenada = sorted(listatemp, key=itemgetter(4))
        #print(listaOrdenada) 
        if(len(listaOrdenada) > 0):
            minimo = ListaDireccionIP(listaOrdenada[0])
            maximo = ListaDireccionIP(listaOrdenada[-1])
            if(minimo == maximo):
                label = minimo
            else:
                label = minimo + "\n" + maximo
            print(label)
            #print(str(listaOrdenada[0]) + "\n" + str(listaOrdenada[-1]))
            #==============================================
            #================================================
            posTemp = list(pos[listaVlan[i][1]])
            '''print("Vlan")
            print(i)
            print("Posicion")
            print(posTemp)'''
            #0 es igual a el "Eje X", 1 es igual al "Eje Y"
            if posTemp[0] == 0.25: #Izquierda
                posTemp[0] = posTemp[0] - desplazamiento
            elif posTemp[0] == 0.75: #Derecha
                posTemp[0] = posTemp[0] + desplazamiento
            elif posTemp[1] == 0.75: #Arriba
                posTemp[1] = posTemp[1] + desplazamiento * 2.5
            elif posTemp[1] == 0.25: #Abajo
                posTemp[1] = posTemp[1] - desplazamiento * 2.5
            posLabel = list(posTemp)
            posLabel[1] = posLabel[1] + SubidaVlan*1.9
            pos_Labels.update({minimo: tuple(posLabel)})
            dictLabels.update({minimo: label})
            
    return 0

#Establecer pertenencia de red
def ValidarSegmentoRed(posicion, listaObjeto):
    for j in range(0, len(listaVlan)):
        segmentoObjeto = listaObjeto[posicion][2].split(".", 3)
        vlanTemporal = listaObjeto[posicion][2].split(".", 3)
        segmentoVlan = listaVlan[j][2].split(".", 3)
        segmentoObjeto = segmentoObjeto[0:-1]
        segmentoVlan = segmentoVlan[0:-1]
        direccionVlan = ".".join(segmentoVlan)
        direccionObjeto = ".".join(segmentoObjeto)
        if (direccionVlan == direccionObjeto):
            vlanTemporal.insert(0, j)
            return (True,j, vlanTemporal)
    return (False,j, listaObjeto[posicion][2].split(".", 3))
#Establecer posicion Label Objetos
def posicionLabelObjetos(nodos_validos, desplazamiento):
    LabelsObjetos(nodos_validos, desplazamiento)
    return 0
#Generacion de nodos y vertices
def GeneracionNodos_Vertices(listaObjetos, TipoObjeto, desplazamiento, posDefault):
    nodos_validos = []
    nodos_invalidos = []
    for i in range(0, len(listaObjetos)):
        G.add_node(listaObjetos[i][1], image=images[TipoObjeto])
        validacion = ValidarSegmentoRed(i, listaObjetos)
        #print(validacion)
        if (validacion[0]==True):
            if(len(validacion[2]) > 1):
                nodos_validos.append(validacion[2])
            posTemp = list(pos[listaVlan[validacion[1]][1]])
            G.add_edge(listaObjetos[i][1], listaVlan[validacion[1]][1])
            #0 es igual a el "Eje X", 1 es igual al "Eje Y"
            if posTemp[0] == 0.25: #Izquierda
                posTemp[0] = posTemp[0] - desplazamiento
                if(TipoObjeto=="Ruta"):
                    segmentoObjeto = listaObjetos[i][2].split(".", 3)
                    dictLabels.update({listaObjetos[i][1]: "." + segmentoObjeto[3]})
                    posTemp[1] = posTemp[1] - desplazamiento/2
            elif posTemp[0] == 0.75: #Derecha
                posTemp[0] = posTemp[0] + desplazamiento
                if(TipoObjeto=="Ruta"):
                    segmentoObjeto = listaObjetos[i][2].split(".", 3)
                    dictLabels.update({listaObjetos[i][1]: "." + segmentoObjeto[3]})
                    posTemp[1] = posTemp[1] + desplazamiento/2
            elif posTemp[1] == 0.75: #Arriba
                posTemp[1] = posTemp[1] + desplazamiento * 2.5
                if(TipoObjeto=="Ruta"):
                    segmentoObjeto = listaObjetos[i][2].split(".", 3)
                    dictLabels.update({listaObjetos[i][1]: "." + segmentoObjeto[3]})
                    posTemp[0] = posTemp[0] - desplazamiento/2
            elif posTemp[1] == 0.25: #Abajo
                posTemp[1] = posTemp[1] - desplazamiento * 2.5
                if(TipoObjeto=="Ruta"):
                    segmentoObjeto = listaObjetos[i][2].split(".", 3)
                    dictLabels.update({listaObjetos[i][1]: "." + segmentoObjeto[3]})
                    posTemp[0] = posTemp[0] + desplazamiento/2
            pos.update({listaObjetos[i][1]: tuple(posTemp)})
            posLabel = list(posTemp)
        else:
            posLabel = list(posDefault)
            pos.update({listaObjetos[i][1]: posDefault})
            if(len(validacion[2]) > 1):
                nodos_invalidos.append(validacion[2])
        posLabel[1] = posLabel[1] + SubidaVlan*1
        pos_Labels.update({listaObjetos[i][1]: tuple(posLabel)})
    #print("====================NODOS VALIDOS=======================")
    #if(TipoObjeto != "Ruta"):
    #    posicionLabelObjetos(nodos_validos, desplazamiento)
    
    #print(nodos_validos)
    print("=======================================================")
    #sorted(nodos_validos, key=itemgetter(2))
    #print(sorted(nodos_validos, key=itemgetter(0)))
   # print(len(nodos_validos[0]))
    #print("====================NODOS INVALIDOS=====================")
    #print(nodos_invalidos)
# =======================================================================




# ==============================Imagenes=================================
icons = {
    "F5": "F5_Logo.png",
    "Vlan": "switch.png",
    "Vlan01": "vlan01.png",
    "Vlan02": "vlan02.png",
    "Vlan03": "vlan03.png",
    "Vlan04": "vlan04.png",
    "Vlan05": "vlan05.png",
    "Vlan06": "vlan06.png",
    "Vlan07": "vlan07.png",
    "Vlan08": "vlan08.png",
    "Vlan09": "vlan09.png",
    "Vlan010": "vlan10.png",
    "Vlan011": "vlan11.png",
    "Vlan012": "vlan12.png",
    "Virtual": "server.png",
    "Nodo": "nodos.png",
    "Ruta": "router.png"
}

# Carga de imagenes

images = {k: PIL.Image.open(fname) for k, fname in icons.items()}

# =======================================================================





# =================================Datos==================================
#Lista de datos
listaSelfIP = []
listaNodos = []
listaVirtual = []
listaVlan = []
listaRutas = []
CargaDatos()
#=========================Limpieza Segmentos Vlan=========================
#Asigna los segmentos de red correspondiente a la vlan, si no hay una selfIP queda sin asignar
for i in range(0, len(listaVlan)):
    nombreVlan=listaVlan[i][1]
    for direccion in listaSelfIP:
        if (nombreVlan == direccion[1]):
            listaVlan[i][2] = direccion[2]
            break
        else:
            listaVlan[i][2] = ""
#=========================INICIALZIACION DE POSICIONES=========================
pos={
    "F5":(0.5,0.5),
}
posicionVlan=[(0.25,0.5), (0.5,0.75), (0.75,0.5), (0.5,0.25),
               (0.25,0.75), (0.65,0.75), (0.75,0.25), (0.35,0.25),
               (0.25,0.25), (0.35,0.75), (0.75,0.75), (0.7,0.25)]
#posLabelVlan =[(0.25,0.6), (0.5,0.82), (0.75,0.6), (0.5,0.32),
 #              (0.25,0.75), (0.65,0.75), (0.75,0.25), (0.35,0.25),
  #             (0.25,0.25), (0.35,0.75), (0.75,0.75), (0.7,0.25)]

SubidaVlan=0.03
#posLabelVlan = list(posicionVlan[i])


# =======================================================================
            
#=========================INICIALZIACION Labels=========================
pos_Labels={
    "F5":(0.5,0.52),
}

dictLabels={
    "F5": "",
} 
# =======================================================================



# Creacion de nodos y vertices
G = nx.Graph()

G.add_node("F5", image=images["F5"])
imagenVlan = "Vlan"
posLabelVlan = [0,0]
for i in range(0, len(listaVlan)):
    #direccionVlan = listaVlan[j][2].split(".", 3)
    imagenVlan = "Vlan0" + str(i + 1)
    print(imagenVlan)
    G.add_node(listaVlan[i][1], image=images[imagenVlan])
    dictLabels.update({listaVlan[i][1]: listaVlan[i][1] + "\n" + listaVlan[i][2]})
    if (listaVlan[i][2]!=""):
        G.add_edge("F5", listaVlan[i][1])
    posLabelVlan = list(posicionVlan[i])
    #posLabelVlan[1] = posLabelVlan[1] + SubidaVlan
    if (i%2 != 0):
        posLabelVlan[1] = posLabelVlan[1] + (SubidaVlan/1.4)#Default 2
    else:
        posLabelVlan[1] = posLabelVlan[1] + (SubidaVlan * 1)#Default *2
    pos_Labels.update({listaVlan[i][1]: tuple(posLabelVlan)})
    pos.update({listaVlan[i][1]: posicionVlan[i]})

#Se ajusta la posicion default
GeneracionNodos_Vertices(listaNodos, "Nodo", 0.1, (0.01,1.2))
GeneracionNodos_Vertices(listaVirtual, "Virtual", 0.2, (0.8,-0.1))#default 0.99, -0.3
GeneracionNodos_Vertices(listaRutas, "Ruta", -0.07, (0.9,0.9))

#print(dictLabels)
print("==============================================")
#print(pos_Labels)
# Get a reproducible layout and create figure
#pos = nx.spring_layout(G, seed=1734289230)
fig, ax = plt.subplots()

nx.draw_networkx(
    G,
    pos=pos,
    ax=ax,
    arrows=True,
    with_labels=False,
    arrowstyle="-",
    min_source_margin=0,
    min_target_margin=0,
    node_color="white",
)

#Parametros para la caja de texto
label_options = {"ec": "k", "fc": "white", "alpha": 0.8}

nx.draw_networkx_labels(
    G,
    bbox=label_options,
    pos=pos_Labels, 
    labels=dictLabels,
    font_size = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 6, #default 5
    )
# Transform from data coordinates (scaled between xlim and ylim) to display coordinates
tr_figure = ax.transData.transform
# Transform from display to figure coordinates
tr_axes = fig.transFigure.inverted().transform

# Select the size of the image (relative to the X axis)
icon_size = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.09 #default 0.06
icon_center = icon_size / 2.0

ax.set_title(nombre)
# Add the respective image to each node
for n in G.nodes:
    xf, yf = tr_figure(pos[n])
    xa, ya = tr_axes((xf, yf))
    # get overlapped axes and plot icon
    a = plt.axes([xa - icon_center, ya - icon_center, icon_size, icon_size])
    a.imshow(G.nodes[n]["image"])
    a.axis("off")
plt.box(False)
plt.show()



