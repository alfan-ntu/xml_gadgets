# xml_gadgets
This is a simple xml utility implemented in Python, including xml file parsing, traversing, searching by specified tag name ... in an input xml file. Also implemented includes tools to construct a tree structure. 

### Important Functions
- construct_xml_tree_structure(): Build the tree structure of the target xml file 
- element_with_attribute(): Determine if the element contains attributes or not
- element_with_text(): Determine if the element contains text or not
- search_element_by_path(): Search element using a XPath variable
- traverse_tree(): Traverse the xml file 

### Base Packages
1. The ElementTree XML API
2. Package lxml: an extended XML utility package based on ElementTree XML API

### Development Notes
1. Element: the main container object for both ElementTree API and lxml
   - Elements are 'lists' which means they can be accessed by specifying index
   - Elements may carry attributes listed in a dictionary container 'dict', i.e. key:value pairs
      e.g. <country name="Liechtenstein" continent="Europe">
   - Elements may contain text contents
   
# References
- https://docs.python.org/3/library/xml.etree.elementtree.html
- https://lxml.de/api/lxml-module.html
  - https://lxml.de/api/lxml.etree._ElementTree-class.html#getpath
  - https://lxml.de/api/lxml.etree._Element-class.html#getroottree

