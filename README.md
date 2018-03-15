
# Blender_map_generator

This program is a script made for the free 3d creation sowtware that allows the user to create infinite flat maps, whith heights
Visit: <a href=https://www.blender.org/ target="_blank">Blender 3D</a>

########
######## Functions
########

These are all functions and their arguments explained:

<font size="3">Function deform_lattice(map_width, map_height, min_height, max_height, add_height, variation_height, oLattice, Lattice, min_land, max_land, down_prob, stay_prob, up_prob, resolution_x, resolution_y):</font>

This is the most important function in the script and it does generate a random map, with the following arguments given:

##Map_width
It's the number of lattices in the x axis. This argument is needed since lattices can only be up to (64x,64y,64z) points.
Map_width goes from 0 to infinite.

##Map_height 
Same as Map_width, but the number of lattices in the <b>y</b> axis. If Map_height > Map_width, Map_height does apply to the x axis. 
Map_height goes from 0 to infinite.
  
Min_height
  This argument gives the function the lower height possible.
  Min_height goes from -infinite to infinite, but it should to be less than Max_height.
  
##Max_height
This argument gives the function the maximum height value possible.
Max_height goes from -infinite to infinite, but it should to be greater than Min_height.
  
##Add_height 
This argument gives the function how much height variation goes from one point(x) to the next one. 
Add_height goes from 0 to infinite. Values lower than 0 may cause the program not to work properly.

##Variation_height
This argument does limit the height between one point(y) to the next one.
Add_height goes from 1 to infinite. Values lower than 1 may cause the program not to work properly. 

##oLattice 
This argument should not be modified, since it is a <b>List</b> of the lattices' object data.
Don't modify this unless you know what you are doing.


##Lattice 
Again, this argument should not be modified, as it is a <b>List</b> of the lattices' lattice data. 
Don't modify this unless you know what you are doing.


###
##Min_land 
This variable is the minimum percentage of land (points > 0 * 100 / total of points) to call the map as valid.
Min_land goes from 0 to 100. It must be greater than Max_land, or blender will freeze.


##Max_land
This variable is the maximum percentage of land (points > 0 * 100 / total of points) to call the map as valid.
Max_land goes from 0 to 100. It must be greater than Min_land. Otherwise, blender will freeze.

<b> If Max_land - Min_land is a very low value (<35) it may take a long time to create the map. </b>
###

##Down_prob
Down_prob is the probability that height(x) will be greater than the next height. 
Down_prob goes from 0 to infinite. Values lower than 0 may cause the program not to work properly.


##Stay_prob 
Stay_prob is the probability that height(x) will be the same as the next height.
<b> Stay_prob does modify height(x,y), height(x-1,y), height(x,-y), and height(-x,-y) </b>
Stay_prob goes from0 to infinite. Values lower than 0 may cause the program not to work properly.


##Up_prob 
Up_prob is the probability that height(x) will be lower than the next height. 
Up_prob goes from 0 to infinite. Values lower than 0 may cause the program not to work properly. 


##Resolution_x 
Resolution_x is the number of points(x) the lattice has to modify the terrain.
Rasolution_x goes from 1 to 64.


##Resolution_y 
Resolution_y is the number of points(y) the lattice has to modify the terrain.
Rasolution_y goes from 1 to 64.




<font size="3"> reset_lattice(obLattice,Lattice): </font>

##oLattice
This argument should not be modified, since it is a <b>List</b> of the lattices' object data.
Don't modify this unless you know what you are doing.


##Lattice 
Again, this argument should not be modified, as it is a <b>List</b> of the lattices' lattice data.
Don't modify this unless you know what you are doing.




<font size="3"> create_map() </font>

Create_map has no arguments.

Create_map() just executes deform_lattice()
If you want to modify any predefined value, please, do it in this function.

