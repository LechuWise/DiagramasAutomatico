#!/bin/bash

genera_csv(){
    if [[ $1 == "Nodos" ]]
    then
        echo $1,$2,$3, $4 >> Objetos.csv
    elif [[ $1 == "VirtualServer" ]] 
    then
        echo $1,$2,$3, $4 >> Objetos.csv
    else
        echo $1,$2,$3 >> Objetos.csv
    fi
}

echo Escribe el nombre del QKView a analizar
read nombreQKView 
echo $nombreQKView
mkdir Analisis$nombreQKView
cp $nombreQKView.qkview Analisis$nombreQKView/
cd Analisis$nombreQKView
tar -xvf $nombreQKView.tar > /dev/null
cd config


arrayls=($(ls -d */))
particion=$"no"


for carpeta in ${arrayls[@]}
do
    if [[ $carpeta == "partitions/" ]]
    then
        particion="true"
    fi
done


echo "Hay perticiones"
echo $particion



# echo "SelfIP"
# echo Nombre
mapfile -t nombresSelfIP < <(grep -w "net self " bigip_base.conf --color)
# echo Direccion
mapfile -t direccionesSelfIP < <(grep -w "net self " bigip_base.conf --color -A 10 | grep -w "address" --color)
# echo Vlan
mapfile -t vlansSelfIP < <(grep -w "net self " bigip_base.conf --color -A 10 | grep -w "vlan" --color)
largo=${#nombresSelfIP[@]}
tipo="SelfIP"
for ((i=0; i<largo; i++))
do 
    nombresSelfIP[i]=$(echo ${nombresSelfIP[i]} | cut -d " " -f 3 | cut -d "/" -f 3)
    #echo ${nombresSelfIP[i]}
    direccionesSelfIP[i]=$(echo ${direccionesSelfIP[i]} | cut -d " " -f 2)
    #echo ${direccionesSelfIP[i]}
    vlansSelfIP[i]=$(echo ${vlansSelfIP[i]} | cut -d " " -f 2 | cut -d "/" -f 3)
    #echo ${vlansSelfIP[i]}
    genera_csv $tipo ${vlansSelfIP[i]} ${direccionesSelfIP[i]}
done
#==========================================================================#
if $particion == "true" 
then
    cd partitions/
    arrayParticiones=($(ls -d */))
    echo ${arrayParticiones[@]}
    for ruta in ${arrayParticiones[@]}
    do
        cd $ruta
        pwd
        # echo "SelfIP"
        # echo Nombre
        mapfile -t nombresSelfIP < <(grep -w "net self " bigip_base.conf --color)
        # echo Direccion
        mapfile -t direccionesSelfIP < <(grep -w "net self " bigip_base.conf --color -A 10 | grep -w "address" --color)
        # echo Vlan
        mapfile -t vlansSelfIP < <(grep -w "net self " bigip_base.conf --color -A 10 | grep -w "vlan" --color)
        largo=${#nombresSelfIP[@]}
        tipo="SelfIP"
        for ((i=0; i<largo; i++))
        do 
            nombresSelfIP[i]=$(echo ${nombresSelfIP[i]} | cut -d " " -f 3 | cut -d "/" -f 3)
            #echo ${nombresSelfIP[i]}
            direccionesSelfIP[i]=$(echo ${direccionesSelfIP[i]} | cut -d " " -f 2)
            #echo ${direccionesSelfIP[i]}
            vlansSelfIP[i]=$(echo ${vlansSelfIP[i]} | cut -d " " -f 2 | cut -d "/" -f 3)
            #echo ${vlansSelfIP[i]}
            cd ..
            cd ..
            genera_csv $tipo ${vlansSelfIP[i]} ${direccionesSelfIP[i]}
            cd partitions/
            cd $ruta
        done
        cd ..
        pwd
    done
    cd ..
fi

#=======================================================================#


# Hostname
mapfile -t hostName < <(grep -w "hostname" bigip_base.conf --color)
echo ${hostName[0]}



# echo Nodos
# echo Nombre
mapfile -t nombresNodos < <(grep -w "ltm node" bigip.conf --color)
# echo Direccion
mapfile -t direccionesNodos < <(grep -w "ltm node" bigip.conf -A 1 | grep address --color)
largo=${#nombresNodos[@]}
tipo="Nodos"
for ((i=0; i<largo; i++))
do 
    nombresNodos[i]=$(echo ${nombresNodos[i]} | cut -d " " -f 3 | cut -d "/" -f 3)
    echo ${nombresNodos[i]}
    direccionesNodos[i]=$(echo ${direccionesNodos[i]} | cut -d " " -f 2)
    echo ${direccionesNodos[i]}
    vlanNodos[i]=$(echo ${direccionesNodos[i]} | cut -d "." -f 1-3)
    genera_csv $tipo ${nombresNodos[i]} ${direccionesNodos[i]} ${vlanNodos[i]}
done

if $particion == "true" 
then
    cd partitions/
    arrayParticiones=($(ls -d */))
    echo ${arrayParticiones[@]}
    for ruta in ${arrayParticiones[@]}
    do
        cd $ruta
        pwd
        # echo Nombre
        mapfile -t nombresNodos < <(grep -w "ltm node" bigip.conf --color)
        # echo Direccion
        mapfile -t direccionesNodos < <(grep -w "ltm node" bigip.conf -A 1 | grep address --color)
        largo=${#nombresNodos[@]}
        for ((i=0; i<largo; i++))
        do 
            nombresNodos[i]=$(echo ${nombresNodos[i]} | cut -d " " -f 3 | cut -d "/" -f 3)
            #echo ${nombresNodos[i]}
            direccionesNodos[i]=$(echo ${direccionesNodos[i]} | cut -d " " -f 2)
            #echo ${direccionesNodos[i]}
            vlanNodos[i]=$(echo ${direccionesNodos[i]} | cut -d "." -f 1-3)
            #echo ${vlanNodos[i]}
            cd ..
            cd ..
            genera_csv $tipo ${nombresNodos[i]} ${direccionesNodos[i]} ${vlanNodos[i]}
            cd partitions/
            cd $ruta
        done
        cd ..
        pwd
    done
    cd ..
fi

#=======================================================================#



#echo Virtual Server
#echo Nombre
mapfile -t nombresVirtualServers < <(grep -w "ltm virtual " bigip.conf)
# echo Direccion
mapfile -t direccionesVirtualServers < <(grep -w "ltm virtual " bigip.conf -A 5| grep -w "destination")
largo=${#nombresVirtualServers[@]}
tipo="VirtualServer"
for ((i=0; i<largo; i++))
do 
    nombresVirtualServers[i]=$(echo ${nombresVirtualServers[i]} | cut -d " " -f 3 | cut -d "/" -f 3)
    #echo ${nombresVirtualServers[i]}
    direccionesVirtualServers[i]=$(echo ${direccionesVirtualServers[i]} | cut -d " " -f 2 | cut -d "/" -f 3)
    #echo ${direccionesVirtualServers[i]}
    vlanVS[i]=$(echo ${direccionesVirtualServers[i]} | cut -d "." -f 1-3)
    genera_csv $tipo ${nombresVirtualServers[i]} ${direccionesVirtualServers[i]} ${vlanVS[i]}
done


if $particion == "true" 
then
    cd partitions/
    arrayParticiones=($(ls -d */))
    echo ${arrayParticiones[@]}
    for ruta in ${arrayParticiones[@]}
    do
        cd $ruta
        pwd
        # echo Nombre
        mapfile -t nombresVirtualServers < <(grep -w "ltm virtual" bigip.conf --color)
        # echo Direccion
        mapfile -t direccionesVirtualServers < <(grep -w "ltm virtual" bigip.conf -A 1 | grep address --color)
        largo=${#nombresVirtualServers[@]}
        for ((i=0; i<largo; i++))
        do 
            nombresVirtualServers[i]=$(echo ${nombresVirtualServers[i]} | cut -d " " -f 3 | cut -d "/" -f 3)
            #echo ${nombresVirtualServers[i]}
            direccionesVirtualServers[i]=$(echo ${direccionesVirtualServers[i]} | cut -d " " -f 2 | cut -d "/" -f 3)
            vlanVS[i]=$(echo ${direccionesVirtualServers[i]} | cut -d "." -f 1-3)
            #echo ${direccionesVirtualServers[i]}
            genera_csv $tipo ${nombresVirtualServers[i]} ${direccionesVirtualServers[i]} ${vlanVS[i]}
            cd ..
            cd ..
            genera_csv $tipo ${nombresVirtualServers[i]} ${direccionesVirtualServers[i]} ${vlanVS[i]}
            cd partitions/
            cd $ruta
        done
        cd ..
        pwd
    done
    cd ..
fi

#=======================================================================#

# echo Lista Vlan
mapfile -t nombresVlans < <(grep -w "net vlan" bigip_base.conf --color)
largo=${#nombresVlans[@]}
tipo="VlanBase"
direccion="0"
for ((i=0; i<largo; i++))
do 
    #echo ${nombresVlans[i]}
    nombresVlans[i]=$(echo ${nombresVlans[i]} | cut -d " " -f 3 | cut -d "/" -f 3)
    #echo ${nombresVlans[i]}
    genera_csv $tipo ${nombresVlans[i]} $direccion
done
#==========================================================================
if $particion == "true" 
then
    cd partitions/
    arrayParticiones=($(ls -d */))
    echo ${arrayParticiones[@]}
    for ruta in ${arrayParticiones[@]}
    do
        cd $ruta
        pwd
        # echo Lista Vlan
        mapfile -t nombresVlans < <(grep -w "net vlan" bigip_base.conf --color)
        largo=${#nombresVlans[@]}
        tipo="VlanBase"
        direccion="0"
        for ((i=0; i<largo; i++))
        do 
            #echo ${nombresVlans[i]}
            nombresVlans[i]=$(echo ${nombresVlans[i]} | cut -d " " -f 3 | cut -d "/" -f 3)
            #echo ${nombresVlans[i]}
            cd ..
            cd ..
            genera_csv $tipo ${nombresVlans[i]} $direccion
            cd partitions/
            cd $ruta
        done
        cd ..
        pwd
    done
    cd ..
fi

#=======================================================================#


# echo Rutas
mapfile -t nombresRutas < <(grep -w "net route" bigip.conf)
mapfile -t direccionesRutas < <(grep -w "net route" bigip.conf --color -A 5 | grep -w "gw" --color)
largo=${#nombresRutas[@]}
tipo="Rutas"
for ((i=0; i<largo; i++))
do 
    nombresRutas[i]=$(echo ${nombresRutas[i]} | cut -d " " -f 3 | cut -d "/" -f 3)
    #echo ${nombresRutas[i]}
    direccionesRutas[i]=$(echo ${direccionesRutas[i]} | cut -d " " -f 2)
    #echo ${direccionesRutas[i]}
    genera_csv $tipo ${nombresRutas[i]} ${direccionesRutas[i]}
done
#==========================================================================
if $particion == "true" 
then
    cd partitions/
    arrayParticiones=($(ls -d */))
    echo ${arrayParticiones[@]}
    for ruta in ${arrayParticiones[@]}
    do
        cd $ruta
        pwd
        mapfile -t nombresRutas < <(grep -w "net route" bigip.conf)
        mapfile -t direccionesRutas < <(grep -w "net route" bigip.conf --color -A 5 | grep -w "gw" --color)
        largo=${#nombresRutas[@]}
        tipo="Rutas"
        for ((i=0; i<largo; i++))
        do 
            nombresRutas[i]=$(echo ${nombresRutas[i]} | cut -d " " -f 3 | cut -d "/" -f 3)
            #echo ${nombresRutas[i]}
            direccionesRutas[i]=$(echo ${direccionesRutas[i]} | cut -d " " -f 2)
            #echo ${direccionesRutas[i]}
            cd ..
            cd ..
            genera_csv $tipo ${nombresRutas[i]} ${direccionesRutas[i]}
            cd partitions/
            cd $ruta
        done       
        cd ..
        pwd
    done
    cd ..
fi

#=======================================================================#



#Creacion de archivos JSON
#mkdir ../../Resultado/
mv Objetos.csv ../../Resultado/
cd ..
cd ..
cd Resultado
mv Objetos.csv $nombreQKView.csv
cat $nombreQKView.csv
cd ..
rm -r Analisis$nombreQKView

