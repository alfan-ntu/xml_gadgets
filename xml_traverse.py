"""
    Description: This is a xml tree structure processing gadget which
                1) builds the tree structure
                2) search a certain element
                3) update a specific element with input value
                 of the input xml file
    Date: 2023/11/9
    Author:
    Version: 0.1a
    Revision History:
        - 2023/11/9: v. 0.1a the initial version
    Reference:
            1) https://docs.python.org/3/library/xml.etree.elementtree.html
    ToDo's  :
        - Search an element
        - Update an element
        - Add search and replace function
        - Convert the implementation to a class implementation to create a gadget set
"""
import xml.etree.ElementTree as ET
import pdb


def tab_combo(level):
    """ Compose tab combos to adjust the print output display """
    tabc = ""
    for i in range(level):
        tabc += "\t"
    return tabc


def just_cr(s):
    """ Test if the input string is simply or contains new line character """
    if s.__contains__('\n'):
        return True
    else:
        return False


def breakdown_dict(dict):
    """ Breakdown the input dictionary to a series of key:value pairs"""
    element_idx = 1
    rstr = ""
    for key, value in dict.items():
        rstr = rstr + key + ":" + value
        if element_idx < len(dict):
            rstr += "/"
        element_idx += 1
    return rstr


def traverse_tree(current, level):
    """ Traverse the xml tree from input node, current, and record the level of this traverse """
    tabc = tab_combo(level)
    if len(current.attrib) == 0:
        if just_cr(current.text):
            print(f'{tabc}level#{level} tag: {current.tag}')
        else:
            print(f'{tabc}level#{level} tag: {current.tag}, value: {current.text}')
    else:
        print(f'{tabc}level#{level} tag: {current.tag}, attrib: {breakdown_dict(current.attrib)}')

    level += 1
    for child in current:
        traverse_tree(child, level)


if __name__ == "__main__":
    tree = ET.parse('./xml_collections/country_data.xml')
    root = tree.getroot()

    traverse_tree(root, 0)
