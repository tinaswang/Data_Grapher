from lxml import etree

class Converter:

    def setup(self, filename):
        parser = etree.XMLParser(remove_comments=True)
        xmldoc = etree.parse(filename, parser = parser)
        root = xmldoc.getroot()
        print("{\n" +  "\"" + root.tag + "\"" + ": {")
        return xmldoc

    def convert(self, filename, root):


        for child in root:
            print("\"" + child.tag+ "\"" + ": {")
            for attribute in child.attrib:
                    data = child.get(attribute)
                    print("\t\"-" + attribute+  "\": \"" + data+ "\",")
            if child.text:
                if child.tag =="Detector":
                    if any("type" in s for s in child.attrib):
                        dimensions = "INT32[192,256]".replace("[", " ").replace(",", " ").replace("]", " ").split()
                        if len(dimensions) == 3 and dimensions[0] == "INT32":
                            dimensions.remove("INT32")
                            dimensions =[int(i) for i in dimensions]
                            data = self.arraysplit(child.text.split(), dimensions)
                            self.prettyprint(data)
                else:
                    print("\t\"#text\": \"" + child.text+ "\"\n\t},")
            [self.convert(filename, child) for children in child]
    #        if (len(root[2])):
        print("}")
    #        else:
    #            print("},")

    def arraysplit(self, data, dimensions):
        data = [int(i) for i in data]
        rows = dimensions[0]
        cols = dimensions[1]
        datalist = [data[x:x+cols] for x in range(0, len(data), cols)]
        return datalist

    def prettyprint(self, data):
        print("\t-data: \"")
        for row in data:
            for value in row:
                print (value, end = ' ')
            print(" ")
        print("\"\n}")

converter = Converter()
converter.convert("dataexample.xml",converter.setup("dataexample.xml").getroot())
