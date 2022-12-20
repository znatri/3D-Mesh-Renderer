######################
# Hardik Goel        #
# hgoel7@gatech.edu  #
# CS 3541 Project 5  #
# Date: 128-10-2022  #
######################

# Provided code for Subdivison and Geodesic Spheres

from __future__ import division
import traceback
import helper_methods

# parameters used for object rotation by mouse
mouseX_old = 0
mouseY_old = 0
rot_mat = PMatrix3D()

# Storage
V = [] # Vertex table - store all the vertex IDs
G = [] # Geometry table - store the actual 3D coordinates of a vertex
O = {} # Opposite table
currentCorner = 0

# Flags
currentCornerVisible = False
showRandomColors = False


# initalize things
def setup():
    size (800, 800, OPENGL)
    frameRate(30)
    noStroke()

# draw the current mesh (you will modify parts of this routine)
def draw():
    global G, V, O, currentCorner, currentCornerVisible, showRandomColors
    randomSeed(0)
    background (100, 100, 180)    # clear the screen to black

    perspective (PI*0.2, 1.0, 0.01, 1000.0)
    camera (0, 0, 6, 0, 0, 0, 0, 1, 0)    # place the camera in the scene
    
    # create an ambient light source
    ambientLight (102, 102, 102)

    # create two directional light sources
    lightSpecular (202, 202, 202)
    directionalLight (100, 100, 100, -0.7, -0.7, -1)
    directionalLight (152, 152, 152, 0, 0, -1)
    
    pushMatrix();

    stroke (0)                    # draw polygons with black edges
    fill (200, 200, 200)          # set the polygon color to white
    ambient (200, 200, 200)
    specular (0, 0, 0)            # turn off specular highlights
    shininess (1.0)
    
    applyMatrix (rot_mat)   # rotate the object using the global rotation matrix

    # THIS IS WHERE YOU SHOULD DRAW YOUR MESH
    
    for c in range(0, len(V), 3):
        beginShape()

        # Use if/else block to fill with random colors if showRandomColors flag is turned on fill(random(255), … , …)
        # Otherwise, normal fill is fill(255, 255, 255)
        if showRandomColors:
            fill(random(255), random(255), random(255))
        else:
            fill(255, 255, 255)

        # Use vertex function to draw 3 vertices
        vertex(G[V[c]][0], G[V[c]][1], G[V[c]][2])
        vertex(G[V[c + 1]][0], G[V[c + 1]][1], G[V[c + 1]][2])
        vertex(G[V[c + 2]][0], G[V[c + 2]][1], G[V[c + 2]][2])

        endShape(CLOSE)

    # Logic to make the current corner visible if currentCornerVisible is turned on
    if currentCornerVisible:
        pushMatrix()

        currV = G[V[currentCorner]]
        nextV = G[V[nextCorner(currentCorner)]]
        previousV = G[V[previousCorner(currentCorner)]]

        posX = (previousV[0] * 0.1) + (currV[0] * 0.8) + (nextV[0] * 0.1)
        posY = (previousV[1] * 0.1) + (currV[1] * 0.8) + (nextV[1] * 0.1)
        posZ = (previousV[2] * 0.1) + (currV[2] * 0.8) + (nextV[2] * 0.1)

        translate(posX, posY, posZ)
        noStroke()
        fill(255, 15, 0)
        sphere(0.1)
        popMatrix()
    
    popMatrix()

# read in a mesh file (this needs to be modified)
def read_mesh(filename):
    global G, V, O, currentCorner, currentCornerVisible, showRandomColors

    fname = "data/" + filename
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()

    # determine number of vertices (on first line)
    words = lines[0].split()
    num_vertices = int(words[1])
    print "number of vertices =", num_vertices

    # determine number of faces (on first second)
    words = lines[1].split()
    num_faces = int(words[1])
    print "number of faces =", num_faces

    # read in the vertices
    for i in range(0, num_vertices):
        words = lines[i+2].split()
        x = float(words[0])
        y = float(words[1])
        z = float(words[2])
        print "vertex: ", x, y, z
        # Update G table by appending (x, y, z)
        G.append([x, y, z])

    # read in the faces
    for i in range(0, num_faces):
        j = i + num_vertices + 2
        words = lines[j].split()
        nverts = int(words[0])
        if (nverts != 3):
            print "error: this face is not a triangle"
            exit()

        index1 = int(words[1])
        index2 = int(words[2])
        index3 = int(words[3])
        print "triangle: ", index1, index2, index3
        # Update V table by extending it by (index1, index2, index3)
        V += [index1, index2, index3]

    # Outside of these loops, instantiate the O table by calling the helper function you wrote
    computeOTable(G, V)

# make sure proper error messages get reported when handling key presses
def keyPressed():
    try:
        handleKeyPressed()
    except Exception:
        traceback.print_exc()

# process key presses (call your own routines!)
def handleKeyPressed():
    global G, V, O, currentCorner, currentCornerVisible, showRandomColors

    if key == '1':
        G = []
        V = []
        O = {}
        read_mesh ('tetra.ply')
    elif key == '2':
        G = []
        V = []
        O = {}
        read_mesh ('octa.ply')
    elif key == '3':
        G = []
        V = []
        O = {}
        read_mesh ('icos.ply')
    elif key == '4':
        G = []
        V = []
        O = {}
        read_mesh ('star.ply')
    elif key == 'n': # next
        currentCorner = nextCorner(currentCorner)
    elif key == 'p': # previous
        currentCorner = previousCorner(currentCorner)
    elif key == 'o': # opposite
        currentCorner = oppositeCorner(currentCorner)
    elif key == 's': # swing
        currentCorner = swingCorner(currentCorner)
    elif key == 'd': # subdivide mesh
        (G, V, _) = subdivide()
    elif key == 'i': # inflate mesh
        G = inflate()
    elif key == 'r': # toggle random colors
        if not showRandomColors:
            showRandomColors = True
        else:
            showRandomColors = False
    elif key == 'c': # toggle showing current corner
        if not currentCornerVisible:
            currentCornerVisible = True
        else:
            currentCornerVisible = False
    elif key == 'q': # quit the program
        exit()

# remember where the user first clicked
def mousePressed():
    global mouseX_old, mouseY_old
    mouseX_old = mouseX
    mouseY_old = mouseY

# change the object rotation matrix while the mouse is being dragged
def mouseDragged():
    global rot_mat
    global mouseX_old, mouseY_old
    
    if (not mousePressed):
        return
    
    dx = mouseX - mouseX_old
    dy = mouseY - mouseY_old
    dy *= -1

    len = sqrt (dx*dx + dy*dy)
    if (len == 0):
        len = 1
    
    dx /= len
    dy /= len
    rmat = PMatrix3D()
    rmat.rotate (len * 0.005, dy, dx, 0)
    rot_mat.preApply (rmat)

    mouseX_old = mouseX
    mouseY_old = mouseY

# Helper methods for mesh
def nextCorner(cornerNum):
    # Find triangle number based on cornerNum
    # Note: the // is floor division in python
    triangleNum = cornerNum // 3
    return 3 * triangleNum + ((cornerNum + 1) % 3)

def previousCorner(cornerNum):
    # Use same idea as nextCorner function
    # But, instead of adding 1 to cornerNum in the return statement, you should subtract
    # Return 3 * triangleNum + ((cornerNum - 1) % 3)
    triangleNum = cornerNum // 3
    return 3 * triangleNum + ((cornerNum - 1) % 3)

def oppositeCorner(cornerNum):
    # Use the opposite-table dictionary
    global O
    return O[cornerNum]

def swingCorner(cornerNum):
    return nextCorner(oppositeCorner(nextCorner(cornerNum)))

def computeOTable(G, V):
    triple = []
    for i in range(len(V)):
        triple.append([min(V[nextCorner(i)], V[previousCorner(i)]), max(V[nextCorner(i)], V[previousCorner(i)]), i])

    sortedList = sorted(triple)
    for idx in range (0, len(sortedList), 2):
        cornerA = sortedList[idx][2]
        cornerB = sortedList[idx+1][2]

        O[cornerA] = cornerB
        O[cornerB] = cornerA

## Pseudocode from helper guide ##
# Variable for numEdges, which is len(V) // 2
# Make a temporary data structure for the newGTable and newVTable
# Initialize empty dictionary for midpoints
# For loop: going through the O table. Need to have a and b as iterators
#   Endpoint1 = G[V[previousCorner(a)]]
#   Endpoint2 = similar but use nextCorner function
#   Calculate midpoint which is endpoint1 + endpoint2 * 1/2
#       Use Pvector mult
#   Find midpointIndex which ○ is len(newGTable)
#   Append the midpoint to the newGTable
#   Update the midpoints dictionary with the midpointIndex
#      Midpoints[a] = midpointIndex
#      Do the same for midpoints[b]
# For loop: go from 0 to len(V) and add 3 each time to the iterator x
#   Make 2 new index variables to make your life easier
#      y = x + 1
#      z = x + 2
# 
#   Note that newVTable is a list in Python. So you can use the extend function to attach more items to this list
#   We need to add 4 sets of items to newVTable
#       (V[x], midpoints[z], midpoints[y])
#       (midpoints[z], V[y], midpoints[x])
#       (midpoints[y], midpoints[x], V[z])
#       (midpoints[x], midpoints[z], midpoints[y])
# Return newGTable, newVTable, computeOTable(newGTable, newVTable)
#   In the handleKeyPressed section, for key 'd', you can update the global variables you made
#   for G, V, and O by calling this subdivide helper function

def subdivide():
    global G, V, O, currentCorner, currentCornerVisible, showRandomColors

    numEdges = len(V) // 2
    newGTable = []
    newVTable = []
    midpoints = {}

    for val in G:
        newGTable.append(val)

    for a, b in O.items():
        endpoint1 = [
            G[V[previousCorner(a)]][0], 
            G[V[previousCorner(a)]][1], 
            G[V[previousCorner(a)]][2]
        ]
        endpoint2 = [
            G[V[nextCorner(a)]][0], 
            G[V[nextCorner(a)]][1], 
            G[V[nextCorner(a)]][2]
        ]
        midpoint = [
            (endpoint1[0] + endpoint2[0])/2, 
            (endpoint1[1] + endpoint2[1])/2, 
            (endpoint1[2] + endpoint2[2])/2
        ]
        midpointIdx = len(newGTable)
        newGTable.append(midpoint)
        midpoints[a] = midpointIdx
        midpoints[b] = midpointIdx

    for x in range(0, len(V), 3):
        y = x + 1
        z = x + 2
        newVTable.extend([V[x], midpoints[z], midpoints[y]])
        newVTable.extend([midpoints[z], V[y], midpoints[x]])
        newVTable.extend([midpoints[y], midpoints[x], V[z]])
        newVTable.extend([midpoints[x], midpoints[y], midpoints[z]])

    return newGTable, newVTable, computeOTable(newGTable, newVTable)

def inflate():
    global G
    normalizedValues = []
    for vertexID in G:
        magnitude = sqrt((
            vertexID[0] * vertexID[0]) + (vertexID[1] * vertexID[1]) + (vertexID[2] * vertexID[2]
        ))
        normalizedValues.append([
            vertexID[0]/magnitude, 
            vertexID[1]/magnitude, 
            vertexID[2]/magnitude
        ])
    return normalizedValues

# Credit to egoode6@gatech.edu for the debug code and slides
def print_mesh():
    print "Vertex table (maps corner num to vertex num):"
    print "corner num\tvertex num:"
    for c, v in enumerate(V):
        print c, "\t\t", v
    print ""

    print "Opposite table (maps corner num to opposite corner num):"
    print "corner num\topposite corner num"
    for c, o in O.iteritems():
        print c, "\t\t", o
    print ""

    print "Geometry table (maps vertex num to position): "
    print "vertex num\tposition:"
    for v, g in enumerate(G):
        print v, "\t\t", g
    print ""

    print ""
    print ""
