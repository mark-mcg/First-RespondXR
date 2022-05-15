#-------------------------------------------------------------------------------
# Name:        flow_data_generator
# Purpose:     Take the First RespondXR harms table and automatically generate
#               an interactive flow chart.
#
# Author:      Mark
#
# Created:     15/05/2022
# Copyright:   (c) Mark 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pandas as pd
from anytree import AnyNode, NodeMixin, RenderTree, Node, AsciiStyle, search
from anytree.exporter import JsonExporter

class FRNodeClass(NodeMixin):  # Add Node feature
    def __init__(self, name, description, id, parent=None, children=None):
        #super(MyClass, self).__init__()
        self.name = name
        self.description = description
        self.id = id
        self.parent = parent
        self.type = "Unused?"
        if children:
            self.children = children

    def __str__(self):
     return "FRNode(" + self.name + ", " + self.description + ", " + str(self.id) + ")"

primaryIndex = 'lifecycle'
secondaryIndex = 'subtopic'
leafType = "topic"
leafDescription = "description"

def main():
    df = pd.read_excel('Test Data.xlsx', sheet_name=0)
    #print(df)
    root = FRNodeClass("Root", "Root", "0")

    id = 1;
    # assume depth of 3 - root -> lifecycle -> subtopic -> topic
    for index, row in df.iterrows():
        primaryIndexNode = None
        secondaryIndexNode = None

        print("Parsing new row, searaching for...")
        print(row[primaryIndex], row[secondaryIndex])

        # insert node into tree...
        primaryResults = search.findall(root, filter_=lambda node: node.name in (row[primaryIndex]))
        if len(primaryResults) == 0:
            print("primary index node not found, creating...")
            primaryIndexNode = FRNodeClass(row[primaryIndex], "", id, root)
            id = id+1
            secondaryIndexNode = FRNodeClass(row[secondaryIndex], "", id, primaryIndexNode)
            id = id+1
        else:
            primaryIndexNode = primaryResults[0]
            print("primary index node found: " + str(primaryIndexNode))

            # check for presence of secondary index
            secondaryResults = search.findall(primaryIndexNode,  filter_=lambda node: node.name in (row[secondaryIndex]))

            if len(secondaryResults) == 0:
                print("secondary index node not found, creating...")
                secondaryIndexNode = FRNodeClass(row[secondaryIndex], "", id, primaryIndexNode)
                id = id+1
            else:
                secondaryIndexNode = secondaryResults[0]
                print("secondary index node found: " + str(secondaryIndexNode))


        # should now have primary and secondary branch nodes
        # now create our new leaf node
        leafNode = FRNodeClass(row[leafType], row[leafDescription], id, secondaryIndexNode)
        id = id+1

    print("Finished generating tree")
    # print(RenderTree(root, style=AsciiStyle()))
    for pre, _, node in RenderTree(root):
         treestr = u"%s%s" % (pre, node.name)
         print(treestr.ljust(8), node.description)

    exporter = JsonExporter(indent=2, sort_keys=True)
    jsondata = exporter.export(root)
    print(jsondata)
    f = open("tree.json", "w")
    f.write(jsondata)
    f.close()

if __name__ == '__main__':
    main()
