import bpy
import random
Object_lattice = bpy.data.objects['LATTICE']
Lattice = bpy.data.lattices['Lattice']
print("")

###
#Convertir Object_latice y Lattice en listas de los mismos, y
#en deform_lattice, determinar segun su posicion global, su
#posicion en una matriz de objetos (Tambien hacer que los
#lattice tengan el mismo tamaño, y la separación entre ellos
#sea de 1/2 su tamaño).  Una vez generada, y determinado que 
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
    #Lattice_Vert_x = bpy.types.Lattice(bpy.types.ID(bpy.data.objects['OBJECT']))
    Lattice_Vert_x = Lattice.points_u
    Lattice_Vert_y = Lattice.points_v
    #print("max vert = (" + str(Lattice_Vert_x) + "," + str(Lattice_Vert_y) +")")
    #Lattice_Vert_y = Lattice.points()[1]
    contador = -1
    contador_y = 0
    height = ((random.randint(0,int((max_height-min_height)/(add_height)))*add_height)+min_height)
    #print("Starting height: " + str(height))
    Lattice_Vert_x_matrix = []
    for apoints in range((Lattice_Vert_x*Lattice_Vert_y)):
        contador += 1
        #print("contador = " + str(contador))
        #print(str(len(Lattice_Vert_matrix)),str(contador), str(height))
        if len(Lattice_Vert_matrix) > 0:
            if (height > Lattice_Vert_matrix[len(Lattice_Vert_matrix)-1][contador] + add_height or height < Lattice_Vert_matrix[len(Lattice_Vert_matrix)-1][contador] - add_height):
                #print("too much height [" + str(Lattice_Vert_matrix[len(Lattice_Vert_matrix)-1][contador]) + "], y")
                height = Lattice_Vert_matrix[len(Lattice_Vert_matrix)-1][contador]
                #print("new height: " +str(height)) 
        if len(Lattice_Vert_x_matrix) > 0:
            if (height > float(Lattice_Vert_x_matrix[contador-1] + add_height) or height < float(Lattice_Vert_x_matrix[contador-1] - add_height)): 
                #print("too much height [" + str(height) + "], x")
                height = Lattice_Vert_x_matrix[contador-1]
                #print("new height: " +str(height)) 
        if len(Lattice_Vert_matrix) > 0 and len(Lattice_Vert_x_matrix) > 0:
            if (height > Lattice_Vert_matrix[len(Lattice_Vert_matrix)-1][contador] + add_height or height < Lattice_Vert_matrix[len(Lattice_Vert_matrix)-1][contador] + add_height) or (height > Lattice_Vert_x_matrix[contador-1] + add_height  or height < Lattice_Vert_x_matrix[contador-1] - add_height):
                #print("too much height [" + str(height) + ", "+ str(Lattice_Vert_matrix[len(Lattice_Vert_matrix)-1][contador]) +"], xy")
                height = (Lattice_Vert_matrix[len(Lattice_Vert_matrix)-1][contador]+Lattice_Vert_x_matrix[contador-1])/2
                #print("new height: " +str(height)) 
        height = height + float(random.randint(-1,1)*add_height)
        if height < min_height:
            height = min_height
        elif height > max_height:
            height = max_height
        point_x = oLattice.data.points[apoints].co_deform[0]
        point_y = oLattice.data.points[apoints].co_deform[1]
        #print("new point["+str(apoints)+"] position = ("+str(point_x)+","+str(point_y)+","+str(height)+")")
        #The next line modifies the lattice even when may be too much or not enough land
        oLattice.data.points[apoints].co_deform = (point_x,point_y,height)
        Lattice_Vert_x_matrix.append(height)
        if contador >= Lattice_Vert_x - 1:
            #print("contador_y = " + str(contador_y))
            Lattice_Vert_matrix.append(Lattice_Vert_x_matrix)
            print(Lattice_Vert_x_matrix)
            Lattice_Vert_x_matrix = []
            contador = -1
            contador_y += 1
    #print(str(Lattice_Vert_matrix))
    TMP = []
    if 1:
        positive = 0
        for a in Lattice_Vert_matrix:
            for b in a:
                if b >= 0:
                    positive += 1
                    TMP.append(" " + str(round(b*1000+.1)/1000))
                else:
                    TMP.append(str(round(b,2)))
            print(TMP)
            TMP = []
        stad = positive*100/(len(Lattice_Vert_matrix)*len(Lattice_Vert_matrix[0]))
        #print(stad)
        if stad < min_land or stad > max_land:
            create_map()
    
            
def reset_lattice(oLattice,Lattice):
    for apoints in range((Lattice.points_u*Lattice.points_v)):
        oLattice.data.points[apoints].co_deform = (oLattice.data.points[apoints].co[0],oLattice.data.points[apoints].co[1],0)
    print("Lattice reseted")
 
def create_map():
    global Object_lattice,Lattice   
    deform_lattice(-.035,.035,.005,Object_lattice,Lattice,65,75)
    #min_height, max_height, add_height, object_lattice, lattice, min_land, max_land

reset_lattice(Object_lattice,Lattice)
create_map()
