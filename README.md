
# Blender_map_generator

This program is a script made for the free 3d creation sowtware that allows the user to create infinite flat maps, whith heights
Visit: <a href=https://www.blender.org/ target="_blank">Blender 3D</a>

########
######## Functions
########

These are all functions and their arguments explained:

Function deform_lattice(map_width, map_height, min_height, max_height, add_height, variation_height, oLattice, Lattice, min_land, max_land, down_prob, stay_prob, up_prob, resolution_x, resolution_y):

This is the main function in the script and it does generate a random map, with the following arguments given:

<dt> Map_width
<dd> It's the number of lattices in the x axis. This argument is needed since lattices can only be up to 64 (x,y,z) points.

<dt> Map_height
<dd> Same as Map_width, but the number of lattices in the <b>y</b> axis. 
