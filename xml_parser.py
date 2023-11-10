"""
    Description: This is a tutorial about the standard xml parser, xml. It is a summarized copy of
                 Python document from https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree
    Date: 2023/11/6
    Author:
    Version: 0.1a
    Revision History:
        - 2023/11/6: v. 0.1a the initial version
"""
import xml.etree.ElementTree as ET
import pdb

tree = ET.parse('./xml_collections/country_data.xml')
root = tree.getroot()
print(root.tag, root.attrib)

# Traversing the element tree
for child in root:
    print(f'child attrib name: {child.get("name")}, {child.get("state")}')

# pdb.set_trace()
print("====================find('neighbor').attrib========================================")
neighbor = root.find('country').attrib
print(neighbor)


"""
country {'name': 'Liechtenstein'}
country {'name': 'Singapore'}
country {'name': 'Panama'}
"""
print("====================iter('neighbor')========================================")
for nbr in root.iter('neighbor'):
    print(nbr.tag, nbr.attrib)
"""
neighbor {'name': 'Austria', 'direction': 'E'}
neighbor {'name': 'Switzerland', 'direction': 'W'}
neighbor {'name': 'Malaysia', 'direction': 'N'}
neighbor {'name': 'Costa Rica', 'direction': 'W'}
neighbor {'name': 'Colombia', 'direction': 'E'}
"""
"""
for gdppc in root.iter('gdppc'):
    print(gdppc.text)
"""
print("============================================================")
for hostility in root.iter('hostility'):
    print("Hostility:", hostility.text)

print("============================================================")
for country in root.iter('country'):
    for neighbor in country.iter('neighbor'):
        print(country.get('name'), "==> neighbor country:", neighbor.get('name'))
        hostility = neighbor.find('hostility').text
        print("Is it hostile:", hostility)
print("============================================================")
for nbr in root.iter('neighbor'):
    print(nbr.get('name'), end=': ')
    print(nbr.find('hostility').text)
