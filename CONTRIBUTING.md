# Contributing

When contributing to this repository, please first discuss the change you wish to make via an issue.
Only use MIT compliant licenses.

## Coding Standard

1. We are [PEP 8](https://www.python.org/dev/peps/pep-0008/) compliant.
   Please use [flake8](http://flake8.pycqa.org/en/latest/) before pushing.
2. We use [mypy](http://mypy-lang.org/) to run static type checks on our codebase.
3. Check that you aren't ruining the coverage when adding a new issue. Test your converage vs master.
    Like so: `pipenv run pytest  --cov=comeback tests` (see [pytest-cov](https://github.com/pytest-dev/pytest-cov))
    More detailed: `pipenv run pytest --cov-report term-missing --cov=comeback tests`
## Pull Request Process

1. Update the README.md with details of changes to the interface, this includes new environment 
   variables, exposed ports, useful file locations and container parameters.
2. Increase the version numbers in any examples files and the README.md to the new version that this
   Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
3. You may merge the Pull Request in once you have the sign-off of one other developer, or if you 
   do not have permission to do that, you may request the reviewer to merge it for you.
4. When we will have tests, make sure they pass before pushing.