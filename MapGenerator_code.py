import bpy
import random
import math
import time
Object_lattice = [bpy.data.objects['Lattice']]
Lattice = [bpy.data.lattices['Lattice']]


num_lat_side = 2


points_x = Lattice[0].points_u
points_y = Lattice[0].points_v
for lat in range(num_lat_side*num_lat_side):
    try:
        lat = str(float(lat)/1000)
        exec("Object_lattice.append(bpy.data.objects['Lattice"+str(lat[1:])+"'])")
        exec("Lattice.append(bpy.data.lattices['Lattice"+str(lat[1:])+"'])")
        exec("bpy.data.lattices['Lattice"+str(lat[1:])+"'].points_u = points_x")
        exec("bpy.data.lattices['Lattice"+str(lat[1:])+"'].points_v = points_y")
    except:
        print("Lattice"+str(lat)+" doesn't exist")
        pass
    
print("")

###

#Convertir Object_latice y Lattice en listas de los mismos, y
#en deform_lattice, determinar segun su posicion global, su
#posicion en una matriz de objetos (Tambien hacer que los
#lattice tengan el mismo tamaño, y la separación entre ellos
#sea = a su tamaño).  Una vez generada, y determinado que 
#el mapa tenga la cantidad de tierra necesaria, modificar el 
#lattice, no antes.
# a)ir de izquierda a derecha como si fueran una misma matriz
# b)calcular una matriz y dar la lista de alturas necesaria para
#   calcular las adyacentes.

#a. Lattice_Vert_matrix es una lista de matrices(lattices) de listas,
#   aunque el programa utiliza una altura(x) para determinar la anterior,
#   aun a traves de listas.

def deform_lattice(min_height, max_height, add_height, oLattice, Lattice, min_land, max_land):
    Lattice_Vert_matrix = []
    for lattices in Lattice:
        Lattice_Vert_matrix.append([])
    #print("Lattice = " + str(math.sqrt(len(Lattice_Vert_matrix))))
    Lattice_Vert_x = Lattice[0].points_u
    Lattice_Vert_y = Lattice[0].points_v
    #print("max vert = (" + str(Lattice_Vert_x) + "," + str(Lattice_Vert_y) +")")
    contador = -1
    contador_x = -1
    contador_y = 0
    latt = 0
    latt_y = 0
    cont_latt = 1
    height = ((random.randint(0,int((max_height-min_height)/(add_height)))*add_height)+min_height)
    #print("Starting height: " + str(height))
    Lattice_Vert_x_matrix = []
    for apoints in range((Lattice_Vert_x*Lattice_Vert_y)*len(Lattice_Vert_matrix)):
        contador += 1
        contador_x += 1
        print("latt,cont_y,cont_x,cont")
        print(str(latt),str(contador_y),str(contador_x), str(contador))
        ###
        # El siguiente if no funciona como deberia 
        # Deberia afectar a todos los puntos que estan entre dos o mas matrices
        # Osea, dejar pasar si:
        # -contador < numero de puntos(x)
        # -contador_x = numero de puntos(x) * numero de lattices(x)
        # ???-contador_y != (numero de puntos(y) * int(numero de lattices(y)*(cont_latt - 1)) + 1  
        # ???-contador_y != (numero de puntos(y) * int(numero de lattices(y)/(cont_latt - 1)) + 1  
        ##
        
        if contador_y != (Lattice_Vert_y * int(*(cont_latt - 1)) + 1 and contador_x = numero de puntos(x) * numero de lattices(x) and contador < numero de puntos(x):
        #if (contador_y-((latt-int(contador_x/Lattice_Vert_x)x)*Lattice_Vert_y) != 0) or (len(Lattice_Vert_x_matrix) != 0 and contador == 0):
        #if (len(Lattice_Vert_x_matrix) != 0 and contador == 0) or (contador_y-(latt-int(contador_x/Lattice_Vert_x)*Lattice_Vert_y) != 0):
            if (contador_y-(latt-int(contador_x/Lattice_Vert_x))*Lattice_Vert_y) > 0:
                if (height > Lattice_Vert_matrix[latt][(contador_y-(latt-int(contador_x/Lattice_Vert_x))*Lattice_Vert_y)-1][contador] + add_height or height < Lattice_Vert_matrix[latt][(contador_y-(latt-int(contador_x/Lattice_Vert_x))*Lattice_Vert_y)-1][contador] - add_height):
                    #print("too much height [" + str(Lattice_Vert_matrix[len(Lattice_Vert_matrix)-1][contador]) + "], y")
                    height = Lattice_Vert_matrix[latt][(contador_y-(latt-int(contador_x/Lattice_Vert_x))*Lattice_Vert_y)-1][contador]
                    #print("new height: " +str(height)) 
            if len(Lattice_Vert_x_matrix) > 0 and contador > 0:
                if (height > float(Lattice_Vert_x_matrix[contador-1] + add_height) or height < float(Lattice_Vert_x_matrix[contador-1] - add_height)): 
                    #print("too much height [" + str(height) + "], x")
                    height = Lattice_Vert_x_matrix[contador-1]
                    #print("new height: " +str(height)) 
            if (contador_y-(latt-int(contador_x/Lattice_Vert_x))*Lattice_Vert_y) > 0 and len(Lattice_Vert_x_matrix) > 0:
                if (height > Lattice_Vert_matrix[latt][(contador_y-(latt-int(contador_x/Lattice_Vert_x))*Lattice_Vert_y)-1][contador] + add_height or height < Lattice_Vert_matrix[latt][(contador_y-(latt-int(contador_x/Lattice_Vert_x))*Lattice_Vert_y)-1][contador] + add_height) or (height > Lattice_Vert_x_matrix[contador-1] + add_height  or height < Lattice_Vert_x_matrix[contador-1] - add_height):
                    #print("too much height [" + str(height) + ", "+ str(Lattice_Vert_matrix[len(Lattice_Vert_matrix)-1][contador]) +"], xy")
                    height = (Lattice_Vert_matrix[latt][(contador_y-(latt-int(contador_x/Lattice_Vert_x))*Lattice_Vert_y)-1][contador]+Lattice_Vert_x_matrix[contador-1])/2
                    #print("new height: " +str(height)) 
            height = height + float(random.randint(-1,1)*add_height)
        else:
            print("---EXCEPCION---")
            if contador != 0 and len(Lattice_Vert_x_matrix) == 0:
                height = Lattice_Vert_matrix[latt-1][contador_y-(latt-int(contador_x/Lattice_Vert_x))*Lattice_Vert_y][Lattice_Vert_x-1]
                if contador_y != 0:
                    height = (Lattice_Vert_matrix[latt-1][contador_y-(latt-int(contador_x/Lattice_Vert_x))*Lattice_Vert_y][Lattice_Vert_x-1] + Lattice_vert_matrix[latt-math.sqrt(Lattice_Vert_matrix)][Lattice_Vert_y][len(Lattice_Vert_x_matrix)] + Lattice_vert_matrix[latt-math.sqrt(Lattice_Vert_matrix)-1][Lattice_Vert_y][Lattice_Vert_x])/3
                    Lattice_Vert_matrix[latt-1][contador_y-(latt-int(contador_x/Lattice_Vert_x))*Lattice_Vert_y][Lattice_Vert_x-1] = height
                    Lattice_vert_matrix[latt-math.sqrt(Lattice_Vert_matrix)][Lattice_Vert_y][len(Lattice_Vert_x_matrix)] = height
                    Lattice_vert_matrix[latt-math.sqrt(Lattice_Vert_matrix)-1][Lattice_Vert_y][Lattice_Vert_x] = height
            else:
                if contador_y != 0:
                    height = Lattice_Vert_matrix[int(latt-math.sqrt(len(Lattice_Vert_matrix)))][Lattice_Vert_y][len(Lattice_Vert_x_matrix)]
        if height < min_height:
            height = min_height
        elif height > max_height:
            height = max_height
        print("new point position = ("+str(height)+")")
        Lattice_Vert_x_matrix.append(height)
        if contador >= Lattice_Vert_x - 1:
            Lattice_Vert_matrix[latt].append(Lattice_Vert_x_matrix)
            #print("append [" + str(latt) , str(contador_y) + "] " + str(Lattice_Vert_x_matrix))
            Lattice_Vert_x_matrix = []
            latt += 1
            contador = -1
            print("")
            print("--Final de matriz(x)")
            if contador_x >= Lattice_Vert_x*math.sqrt(len(Lattice_Vert_matrix)) -1:
                #print("contador_y = " + str(contador_y))
                contador_x = -1
                contador_y += 1
                print("++Final de fila")
                if contador_y > Lattice_Vert_y*cont_latt:
                    latt_y += int(math.sqrt(len(Lattice_Vert_matrix)))
                    cont_latt += 1
                    print("######Final de matriz######")
                    #print(latt_y)
                    #print(cont_latt)
                    #time.sleep(1)
                latt = int(latt_y)
            print("")
    #print(str(Lattice_Vert_matrix))
    if True:
        print("starting land stat.")
        positive = 0
        for each_lattice in Lattice_Vert_matrix:
            for height_row in each_lattice:
                for each_height in height_row:
                    if each_height >= 0:
                        positive += 1
        stad = positive*100/(len(Lattice_Vert_matrix[0])*len(Lattice_Vert_matrix[0][0])*len(Lattice_Vert_matrix))
        print(stad)
        if stad < min_land or stad > max_land:        
            create_map()
        else:
            for each_lattice in range(len(Lattice_Vert_matrix)):
                #print("lattice " + str(each_lattice))
                for height_row in range(len(Lattice_Vert_matrix[each_lattice])-1):
                    #print(Lattice_Vert_matrix[each_lattice][height_row])
                    for each_height in range(len(Lattice_Vert_matrix[each_lattice][height_row])):
                        #print("modify point["+str(each_height)+ "," + str(height_row)+"] height = " + str(int(Lattice_Vert_matrix[each_lattice][height_row][each_height])))
                        #print("point[" + str((height_row)*(len(Lattice_Vert_matrix[each_lattice][0])) +each_height) + "]")
                        point_x = oLattice[each_lattice].data.points[(height_row)*(len(Lattice_Vert_matrix[each_lattice][0]))+each_height].co_deform[0]
                        point_y = oLattice[each_lattice].data.points[(height_row)*(len(Lattice_Vert_matrix[each_lattice][0]))+each_height].co_deform[1]
                        oLattice[each_lattice].data.points[(height_row)*(len(Lattice_Vert_matrix[each_lattice][0]))+each_height].co_deform = (point_x,point_y,Lattice_Vert_matrix[each_lattice][height_row][each_height])
                #print(oLattice[each_lattice])             
            
def reset_lattice(obLattice,Lattice):
    for each_lattice in Lattice:    
        for apoints in range((each_lattice.points_u*each_lattice.points_v)):
            for oLattice in obLattice:
                oLattice.data.points[apoints].co_deform = (oLattice.data.points[apoints].co[0],oLattice.data.points[apoints].co[1],0)
        print("Lattice reseted")
 
def create_map():
    global Object_lattice,Lattice   
    deform_lattice(-.035*2,.035*2,.005*2,Object_lattice,Lattice,0,100)
    #min_height, max_height, add_height, object_lattice, lattice, min_land, max_land

reset_lattice(Object_lattice,Lattice)
create_map()