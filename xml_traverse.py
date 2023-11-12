"""
    Description: This is a xml tree structure processing gadget which
                1) builds the tree structure
                2) search a certain element
                3) update a specific element with input value
                 of the input xml file
    Date: 2023/11/12
    Author:
    Version: 0.1b
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
import os.path
import xml.etree.ElementTree as ET
import pdb
import inspect

DIRECT_CALL = 1
CALL_VIA_DUMP_DEBUG = 2


def get_caller_info(call_depth=DIRECT_CALL):
    """
    Return the caller's file name and line number

    @input call_depth: determine if the caller is from 'dump_debug_info(str)' or directly from the caller
    @return filename, linenumber
    """
    caller_frame = inspect.stack()[call_depth]
    caller_filename = caller_frame.filename
    caller_filename = os.path.basename(caller_filename)
    # assuming caller call this function immediately before using the file name and line number info.
    caller_lineno = caller_frame.lineno+1 if call_depth==DIRECT_CALL else caller_frame.lineno
    return caller_filename, caller_lineno


def dump_debug_info(str):
    """
    Dump debug information with caller filename and caller linenumber

    @input str: dump information
    """
    fn, lno = get_caller_info(CALL_VIA_DUMP_DEBUG)
    print(f'{fn}:{lno} {str}')


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
    """ Traverse the xml tree from input node, current, and record the level of this traverse
    @param current: current node name
    @param level: sub-level count
    """
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


def search_element(node, tag, attrib=None, attrib_value=None):
    """ Find a tag under a specified node and return the value

    @param node: specify the current node for this search
    @param tag
    @param attrib
    @param attrib_value
    @return qualified node
    """
    good_node = None
    for child in node.findall(tag):
        if len(child.attrib) > 0:
            # print(f'{tag} attribute has {len(child.attrib)} attributes: {child.attrib}')
            if attrib is not None:
                dump_debug_info(f'Node {node.tag} {attrib} value= {child.attrib[attrib]}')
                if child.attrib[attrib] == attrib_value:
                    fn, lno = get_caller_info()
                    print(f'{fn}:{lno} Target {child.tag} node is found...')
                    good_node = child

    return good_node


if __name__ == "__main__":
    # For experimental purpose only
    fn, lno = get_caller_info()
    print(f'current file name: {fn}, current line number: {lno}')

    tree = ET.parse('./xml_collections/country_data.xml')
    root = tree.getroot()

    # traverse_tree(root, 0)
    search_tag = 'neighbor'
    search_attrib = 'name'
    attrib_value = 'Malaysia'
    if search_element(root, search_tag, search_attrib, attrib_value) is not None:
        dump_debug_info(f'Tag {search_tag}: attrib:{search_attrib}={attrib_value} is found')
    else:
        dump_debug_info(f'Found no tag named: {search_tag}')

    for child in root:
        search_tag = 'neighbor'
        search_attrib = 'name'
        attrib_value = 'Malaysia'
        # Go one level deeper
        r_node = search_element(child, search_tag, search_attrib, attrib_value)
        if r_node is not None:
            print(f'Node identified: {r_node}')
            dump_debug_info(f'Target neighbor country {attrib_value} is found!')
            dump_debug_info(f'It\'s hostility status is: {r_node.find("hostility").text}')
