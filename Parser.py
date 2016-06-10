from lxml import etree
import json


class Parser(object):



    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        data = self.__convert(self.filename, self.__setup(self.filename))
        return data

    def __setup(self, filename):
        parser = etree.XMLParser(remove_comments=True)
        xmldoc = etree.parse(filename, parser = parser)
        root = xmldoc.getroot()
        return root

    def __convert(self, filename, root):
        datadictionary = {root.tag:
         {child.tag:
                {grandchild.tag:
                {attribute: self.__getname(attribute, grandchild) for attribute in grandchild.attrib}
            for grandchild in child

                }
             for child in root
            }
        }
        for child in root:
            for grandchild in child:
                if grandchild.text:
                    if "Detector" in grandchild.tag and any("type" in s for s in grandchild.attrib):
                        dimensions = grandchild.attrib["type"].replace("[", " ").replace(",", " ").replace("]", " ").split()
                        if len(dimensions) == 3 and dimensions[0] == "INT32":
                            dimensions.remove("INT32")
                            dimensions =[int(i) for i in dimensions]
                            cleaned_array = self.__arraysplit(grandchild.text.split(), dimensions)
                            datadictionary[root.tag][child.tag][grandchild.tag].update({"data" : cleaned_array})

                    else:
                        try:
                            datadictionary[root.tag][child.tag][grandchild.tag].update({"#text" : float(grandchild.text)})
                        except:
                            datadictionary[root.tag][child.tag][grandchild.tag].update({"#text" : grandchild.text})
        return datadictionary

    def __getname(self, attribute,child):
        try:
            return float(child.get(attribute))
        except:
            return child.get(attribute)


    def __arraysplit(self, data, dimensions):
        data = [int(i) for i in data]
        rows = dimensions[0]
        cols = dimensions[1]
        datalist = [data[x:x+cols] for x in range(0, len(data), cols)]
        return datalist


    def dump_as_dict(self):
        return self.parse()

    def dump_as_json(self):
        data =  self.parse()
        json_str= json.JSONEncoder().encode(data)
        return json_str

    def dump_to_file(self, output_file):
        data=  self.parse()
        with open(output_file, 'w') as f:
            json.dump(data, f)
        print("Dumped to %s" %(output_file))




p = Parser("Data Examples/psBioSANS.xml")
print(p.dump_as_json())
p.dump_to_file("newfile.json")
