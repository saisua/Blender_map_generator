import bpy
import random
import math
import time
import mathutils
import collections
import bmesh

def remove_everything():
    try:
        bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
    except:
        pass
    bpy.ops.object.select_all(action="DESELECT")
    for a in bpy.data.objects:
        bpy.data.objects.remove(a, True)
    for a in bpy.data.lattices:
        bpy.data.lattices.remove(a)
    for a in bpy.data.meshes:
        bpy.data.meshes.remove(a)
    for a in bpy.data.materials:
        bpy.data.materials.remove(a)

Object_lattice = []
Lattice = []

#print(str(bpy.data.objects['Lattice']))
#print(str(bpy.data.objects['Lattice'].location))
#bpy.data.objects['Lattice'].location = (0,0,0)
#Object_lattice[0].location = (0,0,0)

remove_everything()

print("")

###Falta:

#-Editar lattices por separado
#-Crear rios https://es.wikipedia.org/wiki/Perfil_de_equilibrio_de_un_río   http://1.bp.blogspot.com/-vEa0yTSoufo/TWOkYNoTg0I/AAAAAAAAAHM/J3m-HG7yVa0/s1600/diagtext.gif (El exterior es mas probable, pero menos apto para vegetacion)

####Crear rios
#1-Aplicar modifiers
#2-Determinar puntos de mesh mas altos en base a los puntos de la lattice (punto_mesh = (punto_lattice/num_puntos_lattice)*num_puntos_mesh)
#3-Coger los 9 puntos de alrededor del punto actual * los 10 primeros no pueden haber sido cogidos ya*, y coger los puntos que estén más abajo que el punto actual (Bajar el más bajo), y volver a buscar los 9 de alrededor
#4-Hacer un diccionario con todos los puntos de altura > 0, 
#5-Si activado, aplicar formula equilibrio rio [Altura*(1-(x/Longitud)^(1-(Concavidad[0-0.5 0.48535]/h[0.571])))]


#https://blender-manual-i18n.readthedocs.io/ja/latest/modifiers/generate/subsurf.html#subsurf-performance

#((2^n+2)^2)/4
#n Subdivision level

def deform_lattice(map_width = 2, map_height = 2, lattice_width = 72, lattice_height = 72, min_height = -.035, max_height = .035, add_height = .005, variation_height = 5, oLattice = [], Lattice = [], min_land = 35, max_land = 75, down_prob = 1, stay_prob = 1, up_prob = 1, resolution_x = 32, resolution_y = 32, subdivision_level = 5, sea = False, color = False, create_rivers = False, use_river_formula = False, concavity = 0.48535, erosion_per_unit = 0.001, minimum_erosion = 0.003):
    print("-----------------------------")
    print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    print("           STARTING          ")
    print("-----------------------------")
    print("")
    points_x = resolution_x
    points_y = resolution_y
    Objects = []
    Meshes = []
    if len(Lattice) <= len(oLattice):    
        counter = len(Lattice)
        oLattice = oLattice[:len(Lattice)]
    else:
        counter = len(oLattice)
        Lattice = Lattice[:len(oLattice)]
    lati = -1
    Lattice_Vert_matrix = [] 
    print("counter: " + str(counter))
    while counter < map_width*map_height+1:
        lati += 1
        lat = float(lati)/1000
        while lat > 1:
            lat = lat / 10
        lat = str(lat)
        error = 0
    
        Lattice_name = "Lattice" + str(lat[1:])
        Plane_name = "Plane" + str(lat[1:])
        
        try:
            does_exist = bpy.data.lattices[Lattice_name]
        except:
            error += 1
        try:
            does_exist = bpy.data.objects[Lattice_name]
        except:
            error += 1
        try:
            does_exist = bpy.data.meshes[Plane_name]
        except:
            error += 1
            #exec("bpy.data.lattices['Lattice"+str(lat[1:])+"'].points_u = points_x")
            #exec("bpy.data.lattices['Lattice"+str(lat[1:])+"'].points_v = points_y")
            #print("Lattice moved to (" + str((-(lati%map_width)*oLattice[len(oLattice)-1].scale[0])) + "," + str(((int(lati/map_width))*oLattice[len(oLattice)-1].scale[1])) + ", 0)")
            #oLattice[len(oLattice)-1].location = (((lati%map_width)*oLattice[len(oLattice)-1].scale[0]),((int(lati/map_width))*oLattice[len(oLattice)-1].scale[1]),0)
            #Lattice_Vert_matrix.append([])
        print("lati: " + str(lati))
            #print("Lattice"+str(lat[1:])+" doesn't exist")
        if error == 3 and counter < map_width*map_height:
            try:
                
                #data_lattice = bpy.data.lattices.new('Lattice')
                #obj_lattice = bpy.data.objects.new('Lattice', data_lattice)
                #Object_lattice = [bpy.data.objects['Lattice']]
                #Lattice = [bpy.data.lattices['Lattice']]
                
                data_lattice = bpy.data.lattices.new(Lattice_name)
                obj_lattice = bpy.data.objects.new(Lattice_name, data_lattice)   
                Mesh = bpy.data.meshes.new(Plane_name)
                obj = bpy.data.objects.new(Plane_name, Mesh)
                Mesh.from_pydata([(1,1,0),(0,1,0),(-1,1,0),(1,0,0),(0,0,0),(-1,0,0),(1,-1,0),(0,-1,0),(-1,-1,0)], [], [(0,1,4,3),(1,2,5,4),(4,5,8,7),(3,4,7,6)])
                counter += 1
                bpy.context.scene.objects.active = None
                bpy.context.scene.objects.active = obj
                try:
                    remove_modifier = obj.modifiers.get("Lattice")
                    if remove_modifier != None:
                        obj.modifiers.remove(remove_modifier)
                except:
                    pass
                new_modifier = obj.modifiers.new("Subdivision", 'SUBSURF')
                new_modifier.levels = 0
                new_modifier.subdivision_type = "SIMPLE"
                new_modifier = obj.modifiers.new("Lattice", 'LATTICE')
                new_modifier.object = obj_lattice
                #print("lattices:" + str(data_lattice))  
                obj_lattice.scale = (lattice_width,lattice_height,(lattice_width + lattice_height)/2)
                obj.scale = (0.5,0.5,0.5)
                #print("resolution_x: " + str(resolution_x))
                #print("tipo res: " + str(type(resolution_x)))
                #print("data_lattice " + str(data_lattice))
                #print("tipo data: " + str(type(data_lattice.points_u)))
                obj.parent = obj_lattice
                scn = bpy.context.scene
                scn.objects.link(obj_lattice)
                scn.objects.link(obj)
                oLattice.append(obj_lattice)
                Lattice.append(data_lattice) 
                Objects.append(obj)
                Meshes.append(Mesh)
                bpy.context.scene.frame_set(1)    
                data_lattice.points_u = resolution_x
                data_lattice.points_v = resolution_y
                data_lattice.points_w = 1
                Lattice_Vert_matrix.append([]) 
            
                oLattice[len(oLattice)-1].location = (((lati%map_width)*oLattice[len(oLattice)-1].scale[0]),((int(lati/map_width))*oLattice[len(oLattice)-1].scale[1]),0)
            except:
                print("Error")
                try:
                    bpy.data.meshes.remove(Mesh)
                    bpy.data.objects.remove(obj,True)
                    bpy.data.objects.remove(obj_lattice,True)
                except:
                    pass
                pass
            
        elif sea and counter == map_width*map_height:
            Plane_name = "Plane" + str(lat[1:])
            scn = bpy.context.scene
            Mesh = bpy.data.meshes.new(Plane_name)
            if color:
                lati = -1
                for num in range(2):    
                    while True:
                        try:
                            lati += 1
                            lat = float(lati2)/1000
                            while lat > 1:
                                lat = lat / 10
                            lat = str(lat)
                            material = bpy.data.materials['Material'+lat[1:]]
                        except:
                            material = bpy.data.materials.new('Material'+lat[1:])
                            break
                    if num > 0:
                        for obj in Objects:
                            material.diffuse_color = (0.061354,0.023289,0.0)
                            material.diffuse_shader = 'LAMBERT' 
                            material.diffuse_intensity = 1.0 
                            material.specular_color = (1,0.38923,0.003719)
                            material.specular_shader = 'BLINN'
                            material.specular_intensity = 0.5
                            obj_data = obj.data
                            obj_data.materials.append(material) 
                    else:    
                        obj = bpy.data.objects.new(Plane_name, Mesh)  
                        material.diffuse_color = (0.046482,0.489297,0.702919)
                        material.diffuse_shader = 'LAMBERT' 
                        material.diffuse_intensity = 1.0 
                        material.specular_color = (1,1,1)
                        material.specular_shader = 'BLINN'
                        material.specular_intensity = 0.5
                        material.specular_ior = 1.330
                        material.raytrace_mirror.use = True
                        material.raytrace_mirror.reflect_factor = 0.5
                        obj_data = obj.data
                        obj_data.materials.append(material)
            obj = bpy.data.objects.new(Plane_name, Mesh)
            Mesh.from_pydata([(1,1,0),(0,1,0),(-1,1,0),(1,0,0),(0,0,0),(-1,0,0),(1,-1,0),(0,-1,0),(-1,-1,0)], [], [(0,1,4,3),(1,2,5,4),(4,5,8,7),(3,4,7,6)])
            scn.objects.link(obj)
            obj.scale = ((lattice_width/2)*map_width,(lattice_height/2)*map_height,1)
            obj.location = ((lattice_width/2)*(map_width-1),(lattice_height/2)*(map_height-1),-0.0001)
            # + (lattice_width/4)                 +(lattice_height/4)
            counter += 1
    
    bpy.context.scene.objects.active = None

    print("")
    #print("Lattice = " + str(math.sqrt(len(Lattice_Vert_matrix))))
    Lattice_Vert_x = resolution_x
    Lattice_Vert_y = resolution_y
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
                        print("Latt_V_mat:" + str(Lattice_Vert_matrix))
                        print("Lat_Vert_mat: " + str(Lattice_Vert_matrix[latt]))
                        print(Lattice_Vert_matrix[latt][contador_y - (int(latt_y/math.sqrt(map_size))*Lattice_Vert_y)-1][contador])
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
    print(str(Lattice_Vert_matrix))
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
        if subdivision_level > 0:
            for obj in Objects:
                obj.modifiers['Subdivision'].levels = subdivision_level
    if create_rivers:
        shape_rivers(Objects, concavity, use_river_formula, erosion_per_unit, minimum_erosion)
    return [Object_lattice,Lattice]
                    
            
def shape_rivers(Objects, Concavity=0.48535, Use_formula=False, erosion_per_unit = 0.001, minimum_erosion = 0.003):
    Height_dict = []
    Maps = []
    Meshes = []
    erosion = .005
    for num in range(len(Objects)):
        Meshes.append(Objects[num].data)
        print("num: " + str(num))
        mesh_vertices = Meshes[num].vertices
        mesh_vert_side = math.sqrt(len(mesh_vertices))
        try:
            bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
        except:
            pass
        bpy.ops.object.select_all(action="DESELECT")
        Objects[num].select = True
        bpy.context.scene.objects.active = Objects[num]
        try:
            bpy.ops.object.modifier_apply(apply_as="DATA",modifier="Subdivision")
            bpy.ops.object.modifier_apply(apply_as="DATA",modifier="Lattice")
        except:
            pass
        try:
            Meshes[num] = bpy.data.meshes[Meshes[num].name]
        except:
            pass
        bpy.ops.object.mode_set(mode="EDIT", toggle=False)
        Height_dict.append({})
        Maps.append({})
        mesh_vert = bmesh.from_edit_mesh(Meshes[num])
        if hasattr(mesh_vert.verts, "ensure_lookup_table"):
            mesh_vert.verts.ensure_lookup_table()
        for vert in range(len(mesh_vertices)):
            vert_height = (mesh_vert.verts[vert].co.to_tuple()[2])
            if vert_height >= 0 and vert < len(mesh_vertices) - mesh_vert_side and vert > mesh_vert_side and vert % mesh_vert_side != 0 and (vert - 1) % mesh_vert_side != 0:
                Height_dict[num][str(vert)] = vert_height
        Height_dict[num] = collections.OrderedDict(reversed(sorted(Height_dict[num].items(), key=lambda t: t[1])))
        erosion_list = {}
        river_order = {}
        order_dict = {}
        for anali_vert_for in list(Height_dict[num].keys()):
            print("vert_for: " + str(anali_vert_for))
            print("vert total: " + str(len(Height_dict[num])+(mesh_vert_side*4)))
            print("mesh_vert_side: " + str(mesh_vert_side)) 
            anali_vert = Height_dict[num][str(int(anali_vert_for))]
            surrounding_vert = {}
            try:
                surrounding_vert[str(int(anali_vert_for)-1)] = list(Meshes[num].vertices[int(anali_vert_for)-1].co)[2]
            except:
                pass
            try:
                surrounding_vert[str(int(anali_vert_for)+1)] = list(Meshes[num].vertices[int(anali_vert_for)+1].co)[2]
            except:
                pass
            try:
                surrounding_vert[str(int(int(anali_vert_for)-round(mesh_vert_side)-1))] = list(Meshes[num].vertices[int(int(anali_vert_for)-1-round(mesh_vert_side))].co)[2]
            except:
                pass
            try:
                surrounding_vert[str(int(int(anali_vert_for)-round(mesh_vert_side)))] = list(Meshes[num].vertices[int(int(anali_vert_for)-round(mesh_vert_side))].co)[2]
            except:
                pass
            try:
                surrounding_vert[str(int(int(anali_vert_for)-round(mesh_vert_side)+1))] = list(Meshes[num].vertices[int(int(anali_vert_for)-round(mesh_vert_side)+1)].co)[2]
            except:
                pass
            try:
                surrounding_vert[str(int(int(anali_vert_for)+round(mesh_vert_side)+1))] = list(Meshes[num].vertices[int(int(anali_vert_for)+round(mesh_vert_side)-1)].co)[2]
            except:
                pass
            try:
                surrounding_vert[str(int(int(anali_vert_for)+round(mesh_vert_side)))] = list(Meshes[num].vertices[int(int(anali_vert_for)+round(mesh_vert_side))].co)[2]
            except:
                pass
            try:
                surrounding_vert[str(int(int(anali_vert_for)+round(mesh_vert_side)-1))] = list(Meshes[num].vertices[int(int(anali_vert_for)+round(mesh_vert_side)-1)].co)[2]
            except:
                pass
            if len(surrounding_vert) <= 0:
                continue
            surrounding_vert = collections.OrderedDict(sorted(surrounding_vert.items(), key=lambda t: t[1]))
            print(list(surrounding_vert.keys()))
            
            try:
                erosion_list[anali_vert_for] += erosion_per_unit
            except:
                erosion_list[anali_vert_for] = erosion_per_unit
            try:
                order_dict[anali_vert_for] += 1
            except:
                order_dict[anali_vert_for] = 1
            for vertex in list(surrounding_vert.keys()):
                try:
                    erosion_list[vertex] += erosion_per_unit
                except:
                    erosion_list[vertex] = erosion_per_unit
            if anali_vert > list(surrounding_vert.values())[0]:
                erosion_list[list(surrounding_vert.keys())[0]] += erosion_list[anali_vert_for]
                river_order[anali_vert_for] = list(surrounding_vert.keys())[0]
                try:
                    order_dict[list(surrounding_vert.keys())[0]] += 1
                except:
                    order_dict[list(surrounding_vert.keys())[0]] = 1
        try:
            bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
        except:
            pass
        for apply_vert_for in list(Height_dict[num].keys()):
            if erosion_list[apply_vert_for] >= minimum_erosion:
                print("Pre-height:" + str(list(Meshes[num].vertices[int(apply_vert_for)].co)[2]) + "  variation: " + str(erosion_list[apply_vert_for]))
                Meshes[num].vertices[int(apply_vert_for)].co.z = erosion_list[apply_vert_for]
                print("applied river erosion vertex(" + str(apply_vert_for) + ") height: " + str(list(Meshes[num].vertices[int(apply_vert_for)].co)[2]))
        #print(river_order)

#shape_rivers([bpy.data.objects['Plane.0']],0.48535,False,0.000001,0.0000003)            

def reset_lattice(obLattice,Lattice):
    for each_lattice in Lattice:    
        for apoints in range((each_lattice.points_u*each_lattice.points_v)):
            for oLattice in obLattice:
                oLattice.data.points[apoints].co_deform = (oLattice.data.points[apoints].co[0],oLattice.data.points[apoints].co[1],0)
        print("Lattice reseted")

def create_map():
    global Object_lattice,Lattice
    deform_lattice(1,1,72,72,-.035,.07,.01,2,Object_lattice,Lattice,35,75,1,3,1,64,64,6,True,True,True,False,0.48535,0.00001,0.0001)
    #map_width, map_height, lattice_width, lattice_height, min_height, max_height, add_height, variation_height, object_lattice, lattice, min_land, max_land, down_prob, stay_prob, up_prob, resolution_x, resolution_y, subdivision_level, sea, color, create_rivers, use_river_formula, concavity, erosion_per_unit, minimum_erosion
    #default: (2,2,72,72,-.035,.035,.005,2,Object_lattice,Lattice,35,75,1,3,1,32,32,5,False,False,False,False,0.48535,0.001,0.003)
create_map()