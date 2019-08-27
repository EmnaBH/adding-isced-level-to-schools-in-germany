
from lxml import etree
import csv
import re
import sys
import difflib

def normalize(x):
    return re.sub('[^a-z0-9-]+', '', x.lower()) 

print("starting script.")

path = "C:\\Users\\emnab\\OneDrive\\Desktop\\Hiwi\\GOAT\\Schools_levels.osm"
fileobject = open(path, encoding="utf8")
doc = etree.parse(fileobject)    

for node in doc.xpath ( "//node|way" ):
    try:
        name = None
        try:
           name = node.xpath("./tag[@k='name']")[0].attrib['v']
        except IndexError:
            try:
                name = node.xpath("./tag[@k='name:de']")[0].attrib['v']
            except IndexError:
                try:
                    name = node.xpath("./tag[@k='name:en']")[0].attrib['v']   
                except IndexError:    
                    sys.stdout.write('.')
                    continue

        n_name = normalize(name)
        found_levels = []
        print('searching for {} aka {} '.format(name, n_name))
        
        if any(word in n_name for word in ['grund-','grundsch']):
            found_levels.append(1)
        if any(word in n_name for word in ['haupt-','hauptsch','mittel-','mittelsch','real-','realsch','fördersch','gesamtsch']):
            found_levels.append(2)
        if any(word in n_name for word in ['gymnasium','berufss','fachobersch']):
            found_levels.append(3)


        if len(found_levels) > 0:
            value = ""
            for level in found_levels:
                value += str(level)+";"
            value = value[:-1]

            print('Inserting ' + value + ' into isced:level for '+ n_name)
            node.append(etree.XML("<tag k='isced:level' v='" + value + "' />"))
            


    except Exception as e:
        print(' exception: ' + str(e))  
        print(etree.tostring(node, pretty_print=True)) 
        print(e)
        exceptions += 1
        pass

print('writing changed file to disk')
doc.write("C:\\Users\\emnab\\OneDrive\\Desktop\\Hiwi\\GOAT\\output.osm", pretty_print=True, xml_declaration=True,  encoding="UTF-8")

print('DONE!')



 #   for tag in node.findall('tag'):
 #       print(tag.attrib)
    #name = node.xpath('tag[@k=name]')[0]
    #print(name.attrib)