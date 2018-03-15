import bpy
import random
import math
import time
import mathutils

def remove_everything():
    for a in bpy.data.objects:
        bpy.data.objects.remove(a,True)
    for a in bpy.data.lattices:
        bpy.data.lattices.remove(a)
    for a in bpy.data.meshes:
        bpy.data.meshes.remove(a)

remove_everything()

try:
    Object_lattice = [bpy.data.objects['Lattice']]
    Lattice = [bpy.data.lattices['Lattice']]
except:
    data_lattice = bpy.data.lattices.new('Lattice')
    bpy.data.objects.new('Lattice', data_lattice)
    Object_lattice = [bpy.data.objects['Lattice']]
    Lattice = [bpy.data.lattices['Lattice']]
    Mesh = bpy.data.meshes.new('Map')
    Object_mesh = bpy.data.objects.new('Map', Mesh)
    Mesh.from_pydata([(1,1,0),(0,1,0),(-1,1,0),(1,0,0),(0,0,0),(-1,0,0),(1,-1,0),(0,-1,0),(-1,-1,0)], [], [(0,1,4,3),(1,2,5,4),(4,5,8,7),(3,4,7,6)])
    new_modifier = Object_mesh.modifiers.new("Subdivision", 'SUBSURF')
    new_modifier.levels = 6
    new_modifier.subdivision_type = "SIMPLE"
    new_modifier = Object_mesh.modifiers.new("Lattice", 'LATTICE')
    new_modifier.object = Object_lattice[0]
    Object_mesh.scale = (0.5,0.5,0.5)
    Object_lattice[0].scale = (72,72,72)
    Object_mesh.parent = Object_lattice[0]
    scn = bpy.context.scene
    scn.objects.link(Object_lattice[0])
    scn.objects.link(Object_mesh)
    #print(str(data_lattice))
    
bpy.context.scene.frame_set(1)    

#print(str(bpy.data.objects['Lattice']))
#print(str(bpy.data.objects['Lattice'].location))
bpy.data.objects['Lattice'].location = (0,0,0)
Object_lattice[0].location = (0,0,0)

print("")

###Falta:

#-Mover y rotar lattices automaticamente
#-Crear lattices



def deform_lattice(map_width, map_height, min_height, max_height, add_height, variation_height, oLattice, Lattice, min_land, max_land, down_prob, stay_prob, up_prob, resolution_x, resolution_y):
    print("-----------------------------")
    print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    print("           STARTING          ")
    print("-----------------------------")
    print("")
    
    Lattice_Vert_matrix = [[]]
    Lattice[0].points_u = resolution_x
    Lattice[0].points_v = resolution_y
    Lattice[0].points_w = 0
    
    points_x = resolution_x
    points_y = resolution_y

    for lat in range(1,(map_width*map_height)):
        try:
            lati = lat
            lat = float(lat)/1000
            while lat > 1:
                lat = lat / 10
            lat = str(lat)
            exec("Lattice.append(bpy.data.lattices['Lattice"+str(lat[1:])+"'])")
            exec("oLattice.append(bpy.data.objects['Lattice"+str(lat[1:])+"'])")
            exec("bpy.data.lattices['Lattice"+str(lat[1:])+"'].points_u = points_x")
            exec("bpy.data.lattices['Lattice"+str(lat[1:])+"'].points_v = points_y")
            #print("Lattice moved to (" + str((-(lati%map_width)*oLattice[len(oLattice)-1].scale[0])) + "," + str(((int(lati/map_width))*oLattice[len(oLattice)-1].scale[1])) + ", 0)")
            oLattice[len(oLattice)-1].location = (((lati%map_width)*oLattice[len(oLattice)-1].scale[0]),((int(lati/map_width))*oLattice[len(oLattice)-1].scale[1]),0)
            Lattice_Vert_matrix.append([])
        except:
            #print("Lattice"+str(lat[1:])+" doesn't exist")
            data_lattice = bpy.data.lattices['Lattice'].copy()
            obj_lattice = eval("bpy.data.objects.new('Lattice"+str(lat[1:])+"', data_lattice)")
            obj =  bpy.data.objects['Map'].copy()
            Mesh = bpy.data.objects['Map'].copy()
            bpy.context.scene.objects.active = None
            bpy.context.scene.objects.active = obj
            remove_modifier = obj.modifiers.get("Lattice")
            if remove_modifier != None:
                obj.modifiers.remove(remove_modifier)
            new_modifier = obj.modifiers.new("Lattice", 'LATTICE')
            new_modifier.object = obj_lattice
            while True:
                try:
                    obj.modifier_move_up("Lattice")
                except:
                    break
            #print("lattices:" + str(data_lattice))
            oLattice.append(obj_lattice)
            Lattice.append(data_lattice)        
            obj_lattice.scale = (72,72,72)
            obj.scale = (0.5,0.5,0.5)
            obj.parent = obj_lattice
            oLattice[len(oLattice)-1].location = (((lati%map_width)*oLattice[len(oLattice)-1].scale[0]),((int(lati/map_width))*oLattice[len(oLattice)-1].scale[1]),0)
            scn = bpy.context.scene
            scn.objects.link(obj_lattice)
            scn.objects.link(obj)
            Lattice_Vert_matrix.append([])

    bpy.context.scene.objects.active = None

    print("")
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
    
    if map_width >= map_height:
        map_size = map_width * map_width
    else:
        map_size = map_height * map_height
    
    print("map_size:" + str(map_size))
    print("Lattice_Vert_matrix:" + str(Lattice_Vert_matrix))
    print("Lattice:" + str(Lattice))
    
    Lattice_Vert_x_matrix = []
    for numpoints in range((Lattice_Vert_x*Lattice_Vert_y)*(map_size)):
        #print("")
        #print("numpoints:" + str(numpoints))
        
        if numpoints >= (Lattice_Vert_x*Lattice_Vert_y)*(map_width*map_height):
            print("Breaking because of the lack of lattices...")
            break
        
        contador += 1
        contador_x += 1
        print("latt,cont_y,cont_x,cont")
        print(str(latt),str(contador_y),str(contador_x), str(contador))
        
        #print(str((Lattice_Vert_x*Lattice_Vert_y)*map_width*map_height))
        
        #print("0:"+str(contador_y%Lattice_Vert_y))
        if ((contador_x == 0 or contador != 0) and 0 != (contador_y%Lattice_Vert_y)) or contador_y == 0:
            prob = random.randint(1,(down_prob+stay_prob+up_prob))
            if prob > stay_prob-1:
                added = float(random.randint(-down_prob,up_prob))
                if added != 0:
                    height = height + (added/abs(added))*add_height
            if contador_y > 0:      
                if contador_y - (int(latt_y/math.sqrt(map_size))*Lattice_Vert_y) > 0 and len(Lattice_Vert_x_matrix) > 0:
                    if (height > Lattice_Vert_matrix[latt][contador_y - (int(latt_y/math.sqrt(map_size))*Lattice_Vert_y)-1][contador] + add_height*variation_height or height < Lattice_Vert_matrix[latt][contador_y - (int(latt_y/math.sqrt(map_size))*Lattice_Vert_y)-1][contador] - add_height*variation_height) or (height > Lattice_Vert_x_matrix[contador-1] + add_height*variation_height  or height < Lattice_Vert_x_matrix[contador-1] - add_height*variation_height):
                        print("too much height [" + str(height) + "], xy")
                        height = (Lattice_Vert_matrix[latt][contador_y - (int(latt_y/math.sqrt(map_size))*Lattice_Vert_y)-1][contador]+Lattice_Vert_x_matrix[contador-1])/2
                else:
                    if contador_y - (int(latt_y/math.sqrt(map_size))*Lattice_Vert_y) > 0:
                        print(str(contador_y - (int(latt_y/math.sqrt(map_size))*Lattice_Vert_y)-1))
                        if (height > Lattice_Vert_matrix[latt][contador_y - (int(latt_y/math.sqrt(map_size))*Lattice_Vert_y)-1][contador] + add_height*variation_height or height < Lattice_Vert_matrix[latt][contador_y - (int(latt_y/math.sqrt(map_size))*Lattice_Vert_y)-1][contador] - add_height*variation_height):
                            print("too much height [" + str(height) + "], y")
                            height = Lattice_Vert_matrix[latt][contador_y - (int(latt_y/math.sqrt(map_size))*Lattice_Vert_y)-1][contador]
                            #print("new height: " +str(height)) 
                    if len(Lattice_Vert_x_matrix) > 0 and contador > 0:
                        if (height > float(Lattice_Vert_x_matrix[contador-1] + add_height*variation_height) or height < float(Lattice_Vert_x_matrix[contador-1] - add_height*variation_height)): 
                            print("too much height [" + str(height) + "], x")
                            height = Lattice_Vert_x_matrix[contador-1]
                            Lattice_Vert_x_matrix[contador-1] = height
                            #print("new height: " +str(height)) 
            
            else:
                if contador > 0 and contador_y > 0:
                    height = (Lattice_Vert_matrix[latt][contador_y - (int(latt_y/math.sqrt(map_size))*Lattice_Vert_y)-1][contador]+Lattice_Vert_x_matrix[contador-1])/2
                    Lattice_Vert_matrix[latt][contador_y - (int(latt_y/math.sqrt(map_size))*Lattice_Vert_y)-1][contador] = height
                    Lattice_Vert_x_matrix[contador-1] = height
                    Lattice_Vert_matrix[latt][contador_y - (int(latt_y/math.sqrt(map_size))*Lattice_Vert_y)-1][contador-1] = height
        else:
            print("---EXCEPCION---")
            if contador_x != 0 and len(Lattice_Vert_x_matrix) == 0:
                if contador_y != 0 and 0 == (contador_y%Lattice_Vert_y):
                    #print("latt-int:" + str(latt-int(math.sqrt(len(Lattice_Vert_matrix)))-1))
                    #print("Latt_y:" + str(Lattice_Vert_y-1))
                    #print("contador:" + str(contador))
                    #print("Latt_x:" + str(Lattice_Vert_x))
                    print("---INTERSECCION---")
                    height = float((Lattice_Vert_matrix[latt-1][contador_y%Lattice_Vert_y][Lattice_Vert_x-1] + Lattice_Vert_matrix[latt-int(math.sqrt(map_size))][Lattice_Vert_y-1][contador] + Lattice_Vert_matrix[latt-int(math.sqrt(map_size))-1][Lattice_Vert_y-1][Lattice_Vert_x-1]) / 3)
                    Lattice_Vert_matrix[latt-1][contador_y%Lattice_Vert_y][Lattice_Vert_x-1] = height
                    Lattice_Vert_matrix[latt-int(math.sqrt(map_size))][Lattice_Vert_y-1][contador] = height
                    Lattice_Vert_matrix[latt-int(math.sqrt(map_size))-1][Lattice_Vert_y-1][Lattice_Vert_x-1] = height
                else:
                    height = Lattice_Vert_matrix[latt-1][contador_y%Lattice_Vert_y][Lattice_Vert_x-1]
            else:
                print("lattice:" + str(latt-int(math.sqrt(len(Lattice_Vert_matrix)))))
                print("fila:" + str(Lattice_Vert_y))
                print("numero:" + str(contador))
                height = Lattice_Vert_matrix[latt-int(math.sqrt(map_size))][Lattice_Vert_y-1][contador]
        if height < min_height:
            height = min_height
        elif height > max_height:
            height = max_height
        print("new point position = ("+str(height)+")")
        Lattice_Vert_x_matrix.append(height)
        if contador >= Lattice_Vert_x - 1:
            if latt < len(Lattice_Vert_matrix):
                #print(str(latt) + "/" + str(map_size-1))            
                Lattice_Vert_matrix[latt].append(Lattice_Vert_x_matrix)
            #print("append [" + str(latt) , str(contador_y) + "] " + str(Lattice_Vert_x_matrix))
            Lattice_Vert_x_matrix = []
            latt += 1
            print("latt:" + str(latt))
            contador = -1
            print("")
            print("---")
            #print("")
            print("--Final de matriz(x)")
            if contador_x >= Lattice_Vert_x*math.sqrt(map_size)-1:
                #print("contador_y = " + str(contador_y))
                contador_x = -1
                contador_y += 1
                print("++Final de fila")
                if contador_y > Lattice_Vert_y*cont_latt-1:
                    latt_y += int(math.sqrt(map_size))
                    cont_latt += 1
                    
                    print("######Final de matriz######")
                    #print(latt_y)
                    #print(cont_latt)
                    #time.sleep(1)
                latt = int(latt_y)
            #print("")
    #print(str(Lattice_Vert_matrix))
    if True:
        print("starting land stat.")
        positive = 0
        for each_lattice in Lattice_Vert_matrix:
            for height_row in each_lattice:
                for each_height in height_row:
                    if each_height >= 0:
                        positive += 1
        stad = positive*100/(resolution_x*resolution_y*map_size)
        print(stad)
        if stad < min_land or stad > max_land:        
            create_map()
        else:
            for each_lattice in range(len(Lattice_Vert_matrix)):
                print("")
                print("applying lattice " + str(each_lattice))
                for height_row in range(len(Lattice_Vert_matrix[each_lattice])):
                    #print(Lattice_Vert_matrix[each_lattice][height_row])
                    for each_height in range(len(Lattice_Vert_matrix[each_lattice][height_row])):
                        #print("point[" + str((height_row)*(len(Lattice_Vert_matrix[each_lattice][0])) +each_height) + "]")
                        #print("modify point["+str(each_height)+ "," + str(height_row)+"] height = " + str(Lattice_Vert_matrix[each_lattice][height_row][each_height]))
                        if each_lattice < len(Lattice_Vert_matrix):    
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
    deform_lattice(5,3,-.035,.035,.005,5,Object_lattice,Lattice,35,75,1,2,1,32,32)
    #width, height, min_height, max_height, add_height, variation_height, object_lattice, lattice, min_land, max_land, down_prob, stay_prob, up_prob, resolution_x, resolution_y
    #default: (1,1,-.035,.035,.005,2,Object_lattice,Lattice,35,75,1,3,1,32,32)
    

create_map()