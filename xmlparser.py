from lxml import etree

class Converter:

    def setup(self, filename):
        parser = etree.XMLParser(remove_comments=True)
        xmldoc = etree.parse(filename, parser = parser)
        root = xmldoc.getroot()
        result = [xmldoc, root]
        print("{\n" +  "\"" + root.tag + "\"" + ": {")
        return root

    def convert(self, filename, root):

        for detector in root.iter("Detector"):
            if detector.attrib =="type":
                dimensions = "INT32[192,256]".replace("[", " ").replace(",", " ").replace("]", " ").split()
                if len(dimensions) == 3 and dimensions[0] == "INT32":
                    dimensions.remove("INT32")
                    dimensions =[int(i) for i in mylist]
                    datalist = self.arraysplit(detector.text, dimensions)
                    print(datalist)

        for child in root:

            print("\"" + child.tag+ "\"" + ": {")

            for attribute in child.attrib:
                    data = child.get(attribute)
                    print("\t\"-" + attribute+  "\": \"" + data+ "\",")

            if child.text:
                text = child.text
                print("\t\"#text\": \"" + text+ "\"\n\t},")

                [self.convert(filename, child) for children in child]
        print("},")

    def arraysplit(data, dimensions):
        data = [int(i) for i in data]
        rows = dimensions[0]
        cols = dimensions[1]
        datalist = [data[x:x+cols] for x in range(0, len(data), cols)]
        return datalist

    def prettyprint(self, data):
        for row in data:
            for value in row:
                print (value, end = ' ')
            print("")



converter = Converter()
converter.convert("dataexample.xml",converter.setup("dataexample.xml"))
