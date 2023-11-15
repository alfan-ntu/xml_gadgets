"""
    Description: This is a xml tree structure processing gadget which
                1) builds the tree structure
                2) search a certain element
                3) update a specific element with input value
                 of the input xml file
    Date: 2023/11/15
    Author:
    Version: 0.1d
    Revision History:
        - 2023/11/15: v. 0.1d preliminarily completed
        - 2023/11/9: v. 0.1a the initial version
    Reference:
            1) https://docs.python.org/3/library/xml.etree.elementtree.html
    ToDo's  :
        - Convert the implementation to a class implementation to create a gadget set
"""
import os.path
import xml.etree.ElementTree as ET
import inspect

from lxml import etree
import re, collections

DIRECT_CALL = 1
CALL_VIA_DUMP_DEBUG = 2


def get_caller_info(call_depth=DIRECT_CALL):
    """
    Return the caller's file name and line number

    @param call_depth: determine if the caller is from 'dump_debug_info(str)' or directly from the caller
    @return filename, linenumber
    """
    caller_frame = inspect.stack()[call_depth]
    caller_filename = caller_frame.filename
    caller_filename = os.path.basename(caller_filename)
    # assuming caller call this function immediately before using the file name and line number info.
    caller_lineno = caller_frame.lineno+1 if call_depth==DIRECT_CALL else caller_frame.lineno
    return caller_filename, caller_lineno


def dump_debug_info(str, detailed=True):
    """
    Dump debug information with caller filename and caller linenumber

    @param str: dump information
    @param detailed: boolean variable determining the display verbosity level, detailed output by default
    """
    if detailed:
        fn, lno = get_caller_info(CALL_VIA_DUMP_DEBUG)
        print(f'{fn}:{lno} {str}')
    else:
        print(str)


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
    """
    Breakdown the input dictionary to a series of key:value pairs

    @param dict: attribute list
    @return : list of key:value in the input attribute
    """
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
    # Note that element.findall(tag) only searches the immediately lower level
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


def construct_xml_tree_structure(root, display_tree):
    """
    Return a tree structure from the input root element

    @param root: root element
    @param display_tree: flag to determine if tree display is required or not
    @return xml_tree: tag, attribute iterates of the input xml tree
    """
    # Initialize an empty tree structure
    xml_tree = collections.OrderedDict()
    for element in root.iter():
        path = re.sub('\[[0-9]+\]', '', element.getroottree().getpath(element))
        if display_tree:
            print(f'path to the element {element.tag}: {element.getroottree().getpath(element)}')
        if path not in xml_tree:
            xml_tree[path] = []
        if len(element.keys()) > 0:
            # use extend function to add
            xml_tree[path].extend(attrib for attrib in element.keys() if attrib not in xml_tree[path])

    return xml_tree


def element_with_attribute(element):
    """
    Determine if the input element has attributes or not

    @param element: the xml element to check
    @return : True, if the element has attributes; False, otherwise
    """
    return bool(element.attrib)


def element_with_text(element):
    """
    Determine if the element has directly associated text content or not

    @param element: the xml element to check
    @return : True, if the element has text; False, otherwise
    """
    # return True if element.text is not None else False
    return not just_cr(element.text)

def search_element_by_path(root, path):
    """
    Search specific element using a full XPath

    @param root: root node of this search
    @param path: XPath to the element to search
    @return : the target element or None
    """
    dump_debug_info(f'Searching XPath {path}')
    element_found = root.xpath(path)
    if element_found is not None:
        for i in range(len(element_found)):
            if element_with_attribute(element_found[i]) is True:
                display_str = f'Element of the specified path {path} found! Attribute is {element_found[i].attrib}'
                dump_debug_info(display_str, False)
            else:
                print(f'Element without attributes!')
            if element_with_text(element_found[i]) is True:
                print(f'Check the text of the element found: {element_found[i].text}')
            else:
                print(f'Blank node element!')
    else:
        dump_debug_info(f'Could not find {path}!')

    return element_found


def search_function_exercise(root):
    """
    Exercises implemented functions on test xml file

    @param root: root element of the input xml file
    """
    # traverse_tree(root, 0)

    # Traverse the first level nodes for the target
    search_tag = 'neighbor'
    search_attrib = 'name'
    attrib_value = 'Malaysia'
    if search_element(root, search_tag, search_attrib, attrib_value) is not None:
        dump_debug_info(f'Tag {search_tag}: attrib:{search_attrib}={attrib_value} is found')
    else:
        dump_debug_info(f'Found no tag directly under root named: {search_tag}')

    # Traverse the tree and find the target element using tag, attribute and attribute value
    for child in root:
        search_tag = 'neighbor'
        search_attrib = 'name'
        attrib_value = 'Malaysia'
        # Go one level deeper
        r_node = search_element(child, search_tag, search_attrib, attrib_value)
        if r_node is not None:
            dump_debug_info(f'Target neighbor country {attrib_value} is found!')
            dump_debug_info(f'It\'s hostility status is: {r_node.find("hostility").text}')

    # Search the element by using a full XPath variable
    target_xpath = "/data/country[4]/neighbor[2]/hostility"
    element_found = search_element_by_path(root, target_xpath)
    if element_found is not None:
        dump_debug_info(f'Parent element tag: {element_found[0].getparent().get("name")}')


def find_and_update(root, path_to_target, new_value):
    """
    Find the element and update it's value

    @param root: root element of the xml tree
    @param path_to_target: path to the target element
    @param new_value: value to update to the target element
    @return : True, if update successfully; False, otherwise
    """
    target_element = search_element_by_path(root, path_to_target)
    if target_element is not None:
        print(f'Original text of {target_element[0].tag} is {target_element[0].text}; To be changed to {new_value}')
        target_element[0].text = new_value
        print(f'Updated text of {target_element[0].tag} is {target_element[0].text}')
        return True
    else:
        print(f'Specified target {path_to_target} not found!')
        return False


if __name__ == "__main__":
    # For experimental purpose only
    fn, lno = get_caller_info()
    print(f'current file name: {fn}, current line number: {lno}')

    # read in an external xml file and get the root element of the xml file
    target_xml = './xml_collections/country_data.xml'
    tree = etree.parse(target_xml)
    root = tree.getroot()

    # Test the function construct_xml_tree_structure()
    xml_tree = construct_xml_tree_structure(root, True)
    print(f'Display the tree structure:')
    for path, attrib in xml_tree.items():
        indent = path.count('/') - 1
        print('{0}{1}: {2}: [{3}]'.format('    ' * indent, indent, path.split('/')[-1], \
                                          ', '.join(attrib) if len(attrib) > 0 else '-'))

    # function exercising several xml utilities implemented
    # search_function_exercise(root)

    target_path = "/data/country[3]/rank"
    # target_path = "/data/country[4]/neighbor[3]"
    find_and_update(root, target_path, "68")
    tree.write(target_xml)
