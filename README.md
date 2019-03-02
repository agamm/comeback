

<p align="center">
	<img alt="comeback logo" src="https://user-images.githubusercontent.com/1269911/53277678-c7574a80-370d-11e9-8fc1-1b47fe0e8550.png" />
	<br />
	
</p>
<p align="center">
<a href="https://github.com/ambv/black/blob/master/LICENSE" alt="License: MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License" /></a>
<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/comeback.svg">
<img src="https://img.shields.io/badge/production-not%20ready-orange.svg" alt="Prodcution" />
</p>

**Comeback** - **Project restoration in one command, auto open everything!**. comeback helps you open your project's ide/browser/terminal (and more!) all at once - so you wouldn't have to do it manually. Get right back to the business of actually developing. 

## How much time does this save?
If it takes you an average of 2 minutes to open all of your project's tools, then you waste about 8.5 hours a year per project, not to mention the friction it adds to start really working :O


## Example
1) In the project directory, we have `.comeback` recipe:
```yaml
vscode: 
  cwd: ~/dev/myproject
chrome:
  url: http://localhost:8080/
```
2) Open a terminal in the project dir and run `comeback`  
> *This .comeback recipe will open vscode in the `~/dev/myproject` path, and open chrome at the `http://localhost:8080/` url.*
 
## How to run locally (current install)
#### Local:
`pipenv shell`  
`pipenv install -e .`  
`comeback --help`  
`cd example`
`comeback # and see the magic`  
#### Global (via pip):
`pip install -e /path/to/comeback`  
(the directory must have the setup.py file in it)  

> Sometimes on linux you may need to configure site-pacakges to be in path like so:  
`export PATH="$PATH:~/path/to/python/site-packages"`  


## Current plugins:
![pycharm logo](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/PyCharm_Logo.svg/48px-PyCharm_Logo.svg.png)
![chrome logo](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Google_Chrome_icon_%28September_2014%29.svg/48px-Google_Chrome_icon_%28September_2014%29.svg.png)
![vscode logo](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Visual_Studio_Code_1.17_icon.svg/48px-Visual_Studio_Code_1.17_icon.svg.png)

## Why not bash/batch?
- It isn't cross-platform.
- It's more abstract to interact with your project's programs.
- With more plugins added every day interacting with programs is much easier. 
  - Why write your own when it's done for you? (DRY)

## How to write a plugin
1) Create a new directory in `comeback/plugins` with the name of the program you want to interact with.
2) Add a `__init__.py` file in that directory
3) Create a `main.py` file with:
	- `run_plugin(arg0, arg1...)` - start the plugin, make sure this is cross-platform.  
	
You may want to see the [CONTRIBUTING.md](https://github.com/agamm/comeback/blob/master/CONTRIBUTING.md) if you decide to add a plugin.

## Ideas of `.comeback` recipes for each kind of developer:
- comeback for frontend developers: 
    - open chrome with live reload 
    - open sublime in the specific project path
    - open a terminal with `npm run start`
- comeback for backend developers:
    - open goland in the specific project path
    - open postman with the project-specific routes
    - open a terminal and run the server
- comeback for game developers:
    - open the ide in the specific project path
    - open chrome with the relevant docs
    - open the terminal to view logs
- comeback for hackers:
    - open tmux with the relevant sessions
    - open FF
    - open IDA

## Notes
 - Use application specific settings temporarily to open the application in the desired state (thanks @MaorCore)
 - Tests, tests and tests.
 
## Contributing
[Active contributes](https://github.com/agamm/comeback/graphs/contributors)
See the [CONTRIBUTING.md](https://github.com/agamm/comeback/blob/master/CONTRIBUTING.md) file

