
## Setup

### pyenv & pipenv

> pyenv versions

```
* system (set by /Users/home/.pyenv/version)
  3.9.11
```

> pyenv local 3.9.11

> pyenv versions

```
  system
* 3.9.11 (set by /Users/home/xxxxxx/.python-version)
```

> which pipenv

```
/Users/home/.pyenv/shims/pipenv
```

> pipenv --python 3.9

```
Creating a virtualenv for this project...
Pipfile: /Users/home/Workspace/xxxxxx/Pipfile
Using /opt/homebrew/bin/python3.9 (3.9.12) to create virtualenv...
⠏ Creating virtual environment...created virtual environment CPython3.9.12.final.0-64 in 3633ms
...
✔ Successfully created virtual environment! 
```

> pipenv install -r requiremenets.txt 

```
Requirements file provided! Importing into Pipfile...
Pipfile.lock not found, creating...
Locking [dev-packages] dependencies...
Locking [packages] dependencies...
Building requirements...
Resolving dependencies...
✔ Success! 
Updated Pipfile.lock (6dfe7e)!
Installing dependencies from Pipfile.lock (6dfe7e)...
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 5/5 — 00:00:04
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```

% pipenv --venv
> /Users/{name}/.local/share/virtualenvs/xxxxxx-9QIHdYVj

% pipenv --rm  
> Removing virtualenv (/Users/{name}/.local/share/virtualenvs/xxxxxx-9QIHdYVj)...
