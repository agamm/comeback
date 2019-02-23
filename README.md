
### Comeback: Project restoration in one command, go right back to where you were
![comeback](https://user-images.githubusercontent.com/1269911/53277678-c7574a80-370d-11e9-8fc1-1b47fe0e8550.png) 

[THIS IS A WORK IN PROGRESS]

**Comeback** is a tool that helps you open your projects ide/browser/terminal (and more!) all at once - so you wouldn't have to do it manually. Get right back to business. It's like virtualenv for your project development tooling state.

### How much time does this save?
If it takes you an average of 2 minutes to open all of your porject tools, then you waste about 8.5 hours a year per project opening your projects, not to mention the friction it adds to start really working :O

### Example
1) In the project directory we have `.comeback` file:
```yaml
vscode: 
  cwd: ~/dev/myproject
chrome:
  url: http://localhost:8080/
```
2) Open a terminal in the project dir and run `comeback`
 -- this will open vscode in the `~/dev/myproject` path, and open chrome at the `http://localhost:8080/` url. This way all of the burden of starting my project is thrown away, and I'm right back developing when I left off, wow, right?!
 
### How to run locally (current install)
`pipenv shell`  
`pipenv install -e .`  
`comeback --help`  

### Why not bash/batch?
- It isn't os agnostic.
- I would like to have a more abstract way to restore my project (maybe adding more features in the future like positioning etc...)
- The moment this repo has a bunch of plugins, it would be much nicer to interact with all the programs rather than using bash (not to mention not being DRY)

### Future
 - Add window positioning (maybe https://pyautogui.readthedocs.io/en/latest/introduction.html)
 - Use application specific settings temporarily to open the application in the desired state (thanks @MaorCore)
 - Make os commands easier to use in plugins
 - Tests, tests and tests.
 
### Contributing
See the `CONTRIBUTING.md` file
