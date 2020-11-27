import xml.etree.ElementTree as ET

tree = ET.parse('xmlexample.xml')
root = tree.getroot()
print(root.tag)
#for child in root:
 #   print ('Tag is:',child.tag)
  #  print ('Attrib is:',child.attrib)
   # for subchild in child:
    #    print("Sub Tag is:", subchild.tag)
     #   print("Sub Attrib is:", subchild.attrib)


#item = [elem.tag for elem in root.iter()]
#for elem in root.iter():
#    item=elem.tag
#    print ('All Elements: ', item)

#for product in root.iter('year'):
 #   print(product.text)

# Find all movies coming out in year xxxx:
#for try1 in root.findall("./genre/decade/movie/[year='1992']"):
 #   print(try1.attrib)

# Find all movies that are available in multiple formats (search on attribut):
for movie in root.findall("./genre/decade/movie/format/[@multiple='Yes']") :
    print("doesn't work:", movie.attrib)
for movie2 in root.findall("./genre/decade/movie/format/[@multiple='Yes']..") : #use .. inside of XPath to return the parent element of the current element. use .... to go 2 levels higher
    print("works:", movie2.attrib)


# Find and replace:
b2tf = root.find("./genre/decade/movie[@title='Back 2 the Future']")
b2tf.attrib["title"] = "Back to the Future"
print("Title is corrected to:", b2tf.attrib["title"])
tree.write("correctedMovie.xml") # export to a new xml file

# search for multiple format movies and correct the multiple setting using regular expression
import re
for form in root.findall("./genre/decade/movie/format"):
    #search for the commas in the format text
    match = re.search(',', form.text)
    if match:
        form.set('multiple','Yes')
    else:
        form.set('multiple','No')
tree.write("correctedMovie.xml")


# moving elements and fix the decade data errors
action = root.find("./genre[@category='Action']")
new_decade = ET.SubElement(action, 'decade')
new_decade.attrib["years"] = '2000s' # Add new decade 2000s to the category "Action"
xmen = root.find("./genre/decade/movie[@title='X-Men']")
dec2000s = root.find("./genre[@category='Action']/decade[@years='2000s']")
dec2000s.append(xmen) #Add X-Men to the decade 2000s
dec1990s = root.find("./genre[@category='Action']/decade[@years='1990s']")
dec1990s.remove(xmen) #remove X-Men from the decade 1990s
tree.write("correctedMovie.xml")