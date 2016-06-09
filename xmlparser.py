from lxml import etree
from pprint import pprint
import json


class Converter(object):

    def __init__(self):
        self.newdata = None

    def setup(self, filename):
        parser = etree.XMLParser(remove_comments=True)
        xmldoc = etree.parse(filename, parser = parser)
        root = xmldoc.getroot()
        return root

    def convert(self, filename, root):
        datadictionary = {root.tag:
         {child.tag:
                {grandchild.tag:
                {attribute: self.getname(attribute, grandchild) for attribute in grandchild.attrib}
            for grandchild in child

                }
             for child in root
            }
        }
        for child in root:
            for grandchild in child:
                if grandchild.text:
                    if grandchild.tag =="Detector" and any("type" in s for s in grandchild.attrib):
                        dimensions = grandchild.attrib["type"].replace("[", " ").replace(",", " ").replace("]", " ").split()
                        if len(dimensions) == 3 and dimensions[0] == "INT32":
                            dimensions.remove("INT32")
                            dimensions =[int(i) for i in dimensions]
                            cleaned_array = self.arraysplit(grandchild.text.split(), dimensions)
                            datadictionary[root.tag][child.tag][grandchild.tag].update({"data" : cleaned_array})

                    else:
                        datadictionary[root.tag][child.tag][grandchild.tag].update({"#text" : grandchild.text})
        return datadictionary

    def getname(self, attribute,child):
        return child.get(attribute)


    def arraysplit(self, data, dimensions):
        data = [int(i) for i in data]
        rows = dimensions[0]
        cols = dimensions[1]
        datalist = [data[x:x+cols] for x in range(0, len(data), cols)]
        return datalist


    def dump_as_dictionary(self, filename):
        datadictionary =  self.convert(filename, self.setup(filename))
        return datadictionary

    def dump_as_json(self, filename):
        datadictionary =  self.convert(filename, self.setup(filename))
        jsonstrings = json.JSONEncoder().encode(datadictionary)
        return jsonstrings

    def dump_as_json_file(self, writefile):
        datadictionary =  self.convert(filename, self.setup(filename))
        jsonstrings = json.dumps(datadictionary)
        with open(writefile, 'w') as f:
            json.dump(datadictionary, f)





converter = Converter()
datadictionary=converter.dump_as_json("dataexample.xml")
print(datadictionary)
datadictionary=converter.dump_as_dictionary("dataexample.xml")
