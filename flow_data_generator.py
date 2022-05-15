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
from anytree import AnyNode, NodeMixin, RenderTree
from anytree.exporter import JsonExporter

class FRNodeClass(NodeMixin):  # Add Node feature
    def __init__(self, typeName, description, id, parent=None, children=None):
        super(MyClass, self).__init__()
        self.typeName = typeName
        self.description = description
        self.id = id
        self.parent = parent
        if children:
            self.children = children


def main():
    df = pd.read_excel('Test Data.xlsx', sheet_name=0)
    print(df)
    root = FRNodeClass()

    # assume depth of 3 - root -> lifecycle -> subtopic -> topic


if __name__ == '__main__':
    main()
