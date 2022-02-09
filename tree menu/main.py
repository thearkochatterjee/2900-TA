import sys

# For installing anytree use following command:
# pip install anytree
from anytree import Node, RenderTree

# For downloading the software needed to run the DotExporter see site below.
# https://anytree.readthedocs.io/en/2.8.0/exporter/dotexporter.html#anytree.exporter.dotexporter.DotExporter
from anytree.exporter import DotExporter

# Open Menu Item Text File
# File must follow the format of:
# Name of Node, Parent Node
# Note: the parent node must be created prior to the child node in the text file
doc = open("menuitems.txt")
itemmenu = doc.readlines()
doc.close()

# Creating Menu Starting Node
menu = Node("menu")

# Dictionary of existing nodes
nodes = {"menu": menu}

# Updating dictionary of exisitng nodes and building menu tree
for item in itemmenu:
    msg = item.strip().split(",")
    if msg[1] in nodes.keys():
        tempnode = Node(msg[0], nodes[msg[1]])
        nodes[msg[0]] = tempnode
    else:
        sys.exit("Error: Parent node does not exist\nParent node: " + msg[1] + "\nChild node: " + msg[0])

# Displaying Tree in Console
for pre, fill, node in RenderTree(menu):
    print("%s%s" % (pre, node.name))

# Displaying Tree as a png image
DotExporter(menu).to_picture("menu.png")

# Menu Interaction
print("\n\nMenu:")
selected = menu
while not selected.is_leaf:
    for index, val in enumerate(selected.children):
        print(str(index + 1) + ". " + val.name)
    selecteditem = int(input("Selected Item:"))
    selected = selected.children[selecteditem-1]

print("\nItem Selected:")
print(selected.name)