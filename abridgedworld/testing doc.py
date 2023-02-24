import os
import xml.etree.ElementTree as ET

game_name = 'Game_name'
video_title ='video_title'
print(f"{os.getcwd()}\games.xml")
tree = ET.parse(f"{os.getcwd()}/games.xml")
root = tree.getroot()

# adding a game ot the xml file
attrib = {'name': game_name}
element = root.makeelement('game', attrib)
root.append(element)

# # adding an video title to the xml file
attrib = {'video_title': video_title}
subelement = root[0].makeelement('video', attrib)
ET.SubElement(root[0], 'video', {})
# root[0].text = 'seconditemabc'



# create a new XML file with the new element
tree.write('games.xml')