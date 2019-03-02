[THIS IS A WORK IN PROGRESS]

# Comeback: Project restoration in one command, auto open everything!
![comeback](https://user-images.githubusercontent.com/1269911/53277678-c7574a80-370d-11e9-8fc1-1b47fe0e8550.png) 


**Comeback** is a tool that helps you open your project's ide/browser/terminal (and more!) all at once - so you wouldn't have to do it manually. Get right back to the business of really developing. It's like virtualenv for your project's development tooling state. Just add a configuration file and off you go.

## How much time does this save?
If it takes you an average of 2 minutes to open all of your project's tools, then you waste about 8.5 hours a year per project, not to mention the friction it adds to start really working :O

## Example
1) In the project directory, we have `.comeback` file:
```yaml
vscode: 
  cwd: ~/dev/myproject
chrome:
  url: http://localhost:8080/
```
2) Open a terminal in the project dir and run `comeback`
 -- this will open vscode in the `~/dev/myproject` path, and open chrome at the `http://localhost:8080/` url. This way all of the burden of starting my project is thrown away, and I'm right back developing when I left off, wow! right?
 
## How to run locally (current install)
`pipenv shell`  
`pipenv install -e .`  
`comeback --help`  
`cd example`
`comeback # and see the magic`  
or Install globally via pip  
`pip install -e /path/to/comeback`  
(the directory must have the setup.py file in it)  
Sometimes on linux you may need to configure site-pacakges to be in path like so:  
`export PATH="$PATH:~/path/to/python/site-packages"`  
*Later it would be installed normally with pip install comeback*

## Why not bash/batch?
- It isn't cross-platform.
- I would like to have a more abstract way to restore my project (maybe adding more features in the future like window positioning etc...)
- The moment this repo has a bunch of plugins, it would be much nicer to interact with all the programs rather than using bash manually for each tool (not to mention not being DRY)

## How to write a plugin
1) Create a new directory with the name of the tool you want to interact with
2) Add a `__init__.py` file in that directory
3) Create a `main.py` file with two functions:
	- `cb_test` - used to check if the plugin can run
	- `cb_start` - actually start the plugin, write per each os (you can use the utils helper)

## Ideas of `.comeback` confs for each kind of developer:
- comeback for frontend developers: 
    - open chrome with live reload 
    - open sublime in the specific project path
    - open a terminal with `npm run start`
- comeback for backend developers:
    - open goland in the specific project path
    - open postman with the project specific routes
    - open a terminal and run the server
- comeback for game developers:
    - open the ide in the specific project path
    - open chrome with the relevant docs
    - open the terminal to view logs
- comeback for hackers:
    - open tmux with the relevant sessions
    - open FF
    - open IDA

## Future
 - Add window positioning (maybe https://pyautogui.readthedocs.io/en/latest/)
 - Use application specific settings temporarily to open the application in the desired state (thanks @MaorCore)
 - Make os commands easier to use in plugins
 - Open programs in an async fashion, why wait?
 - Tests, tests and tests.
 - Add the ability to run globally and choose which project.
 
## Contributing
See the `CONTRIBUTING.md` file
