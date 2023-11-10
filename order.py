import xml.etree.ElementTree as ET
import pdb

tree = ET.parse('cbcr.xml')
root = tree.getroot()
print(root.tag, root.attrib)

child_count = 0
for child in root:
    child_count += 1
#    print(child_count, child.tag, child.attrib)
    for irs8975 in child.findall('{http://www.irs.gov/efile}IRS8975ScheduleA'):
        #    for irs8975 in child.findall('IRS8975ScheduleA'):
        #        jurisdiction = irs8975.find('TaxJurisdictionCountryCd').text
        jurisdiction = irs8975.attrib
        print("Jurisiction:", jurisdiction)



"""
    for irs8975schedule in child.iter('TaxJurisdictionCountryCd'):
        jurisdictionCd = irs8975schedule.text
        print('jurisdiction code:', jurisdictionCd)
"""
# pdb.set_trace()
scheduleCount = 0
for IRS8975Schedule in root.iter('BusinessNameLine1Txt'):
    scheduleCount += 1
#    print(IRS8975Schedule.text)

print("scheduleCount  : ", scheduleCount)
