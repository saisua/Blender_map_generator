
# Blender_map_generator

This program is a script made for the free 3d creation sowtware that allows the user to create infinite flat maps, whith heights
Visit: <a href=https://www.blender.org/ target="_blank">Blender 3D</a>

########
######## Functions
########

These are all functions and their arguments explained:

<font size="3">Function deform_lattice(map_width, map_height, min_height, max_height, add_height, variation_height, oLattice, Lattice, min_land, max_land, down_prob, stay_prob, up_prob, resolution_x, resolution_y):</font>

This is the most important function in the script and it does generate a random map, with the following arguments given:

<dt> Map_width </dt>
<dd> It's the number of lattices in the x axis. This argument is needed since lattices can only be up to (64x,64y,64z) points. </dd>
<dd> Map_width goes from 0 to infinite. </dd>

<dt> Map_height </dt>
<dd> Same as Map_width, but the number of lattices in the <b>y</b> axis. If Map_height > Map_width, Map_height does apply to the x axis. </dd>
<dd> Map_height goes from 0 to infinite. </dd>
  
<dt> Min_height </dt>
<dd> This argument gives the function the lower height possible. </dd>
<dd> Min_height goes from -infinite to infinite, but it should to be less than Max_height. </dd>
  
<dt> Max_height </dt>
<dd> This argument gives the function the maximum height value possible. </dd>
<dd> Max_height goes from -infinite to infinite, but it should to be greater than Min_height. </dd>
  
<dt> Add_height </dt>
<dd> This argument gives the function how much height variation goes from one point(x) to the next one. </dd>
<dd> Add_height goes from 0 to infinite. Values lower than 0 may cause the program not to work properly. </dd>

<dt> Variation_height  </dt>
<dd> This argument does limit the height between one point(y) to the next one. </dd>
<dd> Add_height goes from 1 to infinite. Values lower than 1 may cause the program not to work properly. </dd>

<dt> oLattice </dt>
<dd> This argument should not be modified, since it is a <b>List</b> of the lattices' object data. </dd>
<dd> Don't modify this unless you know what you are doing. </dd>


<dt> Lattice </dt>
<dd> Again, this argument should not be modified, as it is a <b>List</b> of the lattices' lattice data. </dd>
<dd> Don't modify this unless you know what you are doing. </dd>


###
<dt> Min_land </dt>
<dd> This variable is the minimum percentage of land (points > 0 * 100 / total of points) to call the map as valid. </dd>
<dd> Min_land goes from 0 to 100. It must be greater than Max_land, or blender will freeze. </dd>


<dt> Max_land </dt>
<dd> This variable is the maximum percentage of land (points > 0 * 100 / total of points) to call the map as valid. </dd>
<dd> Max_land goes from 0 to 100. It must be greater than Min_land. Otherwise, blender will freeze. </dd>

<b> If Max_land - Min_land is a very low value (<35) it may take a long time to create the map. </b>
###

<dt> Down_prob </dt>
<dd> Down_prob is the probability that height(x) will be greater than the next height. </dd>
<dd> Down_prob goes from 0 to infinite. Values lower than 0 may cause the program not to work properly. </dd>


<dt> Stay_prob </dt>
<dd> Stay_prob is the probability that height(x) will be the same as the next height. </dd>
<dd><b> Stay_prob does modify height(x,y), height(x-1,y), height(x,-y), and height(-x,-y) </b></dd>
<dd> Stay_prob goes from0 to infinite. Values lower than 0 may cause the program not to work properly. </dd>


<dt> Up_prob </dt>
<dd> Up_prob is the probability that height(x) will be lower than the next height. </dd>
<dd> Up_prob goes from 0 to infinite. Values lower than 0 may cause the program not to work properly. </dd>


<dt> Resolution_x </dt>
<dd> Resolution_x is the number of points(x) the lattice has to modify the terrain. </dd>
<dd> Rasolution_x goes from 1 to 64. </dd>


<dt> Resolution_y </dt>
<dd> Resolution_y is the number of points(y) the lattice has to modify the terrain. </dd>
<dd> Rasolution_y goes from 1 to 64. </dd>

<font size="3"> reset_lattice(obLattice,Lattice): </font>

<dt> oLattice </dt>
<dd> This argument should not be modified, since it is a <b>List</b> of the lattices' object data. </dd>
<dd> Don't modify this unless you know what you are doing. </dd>


<dt> Lattice </dt>
<dd> Again, this argument should not be modified, as it is a <b>List</b> of the lattices' lattice data. </dd>
<dd> Don't modify this unless you know what you are doing. </dd>


<font size="3"> create_map() </font>

Create_map has no arguments.

Create_map() just executes deform_lattice()
If you want to modify any predefined value, please, do it in this function.

