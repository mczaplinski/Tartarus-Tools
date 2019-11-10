# Tartarus-Tools
VST and Sample Processing Environment

# Requirements:
	Tested with Python 3.6.8 (recommended because of dependencies, 09.02.2019)

# How to install

First make sure to update pip:
```
$ pip install --upgrade pip
```

Then you probably want to work in a virtualenv. Let's install it:
```
$ pip install --upgrade virtualenv
```

Now set up the virtual environment:
```
$ cd $my_work_dir
$ virtualenv my_venv (-p python3)  # or: python -m venv my_venv
$ my_env\Scripts\activate.bat      # may need admin. This activates the venv
```
Then install all requirements and dependencies:
```
$ cd $my_work_dir
$ pip install --upgrade -r requirements.txt
``` 
You may also want to update PyAudio to ASIO version with the script in etc\.
Finally, start jupyter notebook (if you want to open the *.ipynb files):
```bash
$ jupyter notebook
#or by starting:
start_notebook.bat
```
You can also just edit and run the scripts you need. Be sure to do this while the virtual environment is active.
