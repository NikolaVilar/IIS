### Change python version while using poetry

```
poetry env info
-> Executable
poetry env remove Executable
pyenv local 3.9.13
pyenv which python
-> Path
-> Change python version in pyproject.toml
-> Delete poetry lock
poetry env use Path
poetry install
-> install missing libraries by hand by using poetry add <name>
```
