import xml.etree.ElementTree as ET
import os
# print (os.path.dirname('desk.xml'))
# path='/mnt/c/Users/gotom/Desktop/desk.xml'
# vmname='damnright!!!'
# ip='192.168.7.7'
# service='lin'
def modXML(path,vmname,ip,service):
    tree = ET.parse(path)
    root = tree.getroot()

    config = ET.Element("config")
    config.set('name', vmname)

    if(service=='win'):
        config.set('protocol', 'rdp')
    elif(service=='lin'):
        config.set('protocol', 'vnc')
    elif(service=='app'):
        config.set('protocol', 'vnc')
#-----------------------------------------------------------
    param = ET.SubElement(config, "param")
    param.set('name','hostname')
    param.set('value',ip)
#-----------------------------------------------------------
    param = ET.SubElement(config, "param")
    param.set('name','port')
    if(service=='win'):
        param.set('value','3389')
    elif(service=='lin'):
        param.set('value','5900')
    elif(service=='app'):
        param.set('value','5900')
#-----------------------------------------------------------
    if(service=='win'):
        param = ET.SubElement(config, "param")
        param.set('name','username')
        param.set('value','demo')

        param = ET.SubElement(config, "param")
        param.set('name','password')
        param.set('value','1234')

        param = ET.SubElement(config, "param")
        param.set('name','security')
        param.set('value','nla')

        param = ET.SubElement(config, "param")
        param.set('name','ignore-cert')
        param.set('value','true')

    root.insert(1, config)
    tree.write(path)
    
    for child in root:
        print(child.attrib)

if __name__ == '__main__':
    modXML()