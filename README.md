# Pytest Plugin Template

Template to create Pytest Plugins

First steps to develop a plugin is to create a `venv` and install the requirements:

```bash
python -m venv venv
source venv/bin/activate
```

Then the requirements (and the plugin needs to be installed):

```bash
pip install -r requirements.txt
```

> [!NOTE]  
> The plugin under development is installed in edit mode `-e`, meaning that there's no need to reinstall the plugins with modifications.

Run the first test with:

```bash
pytest -m hello -s
```
