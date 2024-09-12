# DiagramasAutomatico
Programas usados para generar diagramas de la solucion implementada


La generacion de diagramas es un proceso de dos pasos

Para diagramas de F5 se necesita el archivo .qkview

Se deben de poner el script extractorVlan.sh y el .qkview en la misma carpeta ademas de crear en ese mismo nivel una carpeta llamada Resultado
en esta carpeta se almacenara el excel generado con los objetos del qkview proporcionado.

Este excel se debe de pasar a una carpeta donde este el script pruebas.py junto con los png anexados
para que el script funcione se requieren las siguientes librerias
matplotlib
networkx
numpy

En la variable nombre se debe de modificar para poner el nombrel del .csv correspondiente

Editar la variable subidaVlan define que tanto se alejan las vlan del equipo principal

font_size define el tamaño de los nombres y direccion 

icon_size define el tamaño de las imagenes

ajustando la posicion default se modifica el tamaño del diagrama

editando estos valores se puede ajustar las dimensiones del diagrama segun la arquitectura que se tenga

