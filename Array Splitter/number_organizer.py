from lxml import etree
from pprint import pprint

class Practice:

    def arraysplit(self, data, dimensions):
        data = [int(i) for i in data]
        rows = dimensions[0]
        cols = dimensions[1]
        datalist = [data[x:x+cols] for x in range(0, len(data), cols)]
        return datalist

    def setup(self, filename):
        parser = etree.XMLParser(remove_comments=True)
        xmldoc = etree.parse(filename, parser = parser)
        root = xmldoc.getroot()
        result = [xmldoc, root]
        print("{\n" +  "\"" + root.tag + "\"" + ": {")
        return root


    def convert(self, filename, root):
        dimensions = "INT32[192,256]".replace("[", " ").replace(",", " ").replace("]", " ").split()
        if len(dimensions) == 3 and dimensions[0] == "INT32":
            dimensions.remove("INT32")
            dimensions =[int(i) for i in dimensions]
            data = self.arraysplit(root.text.split(), dimensions)
            self.prettyprint(data)

    def prettyprint(self, data):
        for row in data:
            for value in row:
                print (value, end = ' ')
            print("")



practice = Practice()
practice.convert("numbers.xml", practice.setup("numbers.xml"))
