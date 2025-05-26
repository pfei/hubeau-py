> ⚠️ **Pre-Alpha Notice**
>
> This project is in a **very early, pre-alpha state**.  
> The goal is to become a solid, typed, and reference Python client for the Hubeau APIs.
> Expect rapid changes, breaking updates, and incomplete coverage.
> Contributions, feedback, and issue reports are very welcome!

# hubeau-py

Pythonic, typed, and modern client for the Hubeau water data APIs.

## Features

- Typed, Pythonic client for the Hubeau water data APIs
- Easy querying of water quality and station data
- Returns results as Pydantic models for type safety
- Ready for use in data science workflows (e.g., with pandas)

## Development Model

- Modern Python (**3.13+**)
- Strict typing throughout the codebase
- [Poetry](https://python-poetry.org/) for dependency and environment management
- Linting, formatting, and type checking enforced (ruff, black, mypy)
- Follows the [src-layout](https://realpython.com/python-application-layouts/) for package structure

## Quickstart

```python
from hubeau_py.client import HubeauClient
client = HubeauClient()
stations = client.get_stations("Agen")
print(stations)
```

## Example Notebook

A continuously updated example notebook is available in [`examples/demo.ipynb`](examples/demo.ipynb).

- This notebook demonstrates the main features of `hubeau-py` and provides practical usage examples.
- You can run it locally using Jupyter Notebook or JupyterLab:

```
$ poetry run jupyter notebook examples/demo.ipynb
```

or, after activating the virtual environment:

```
$ jupyter notebook examples/demo.ipynb
```

- The notebook should be expanded as new functionalities are added to the package.

For more about Jupyter, see the [official documentation](https://jupyter.org/documentation).

## Development

- Install dependencies:

```
$ poetry install
```

- Run tests:

```
$ poetry run pytest
```

- Lint code:

```
$ poetry run ruff check src/
```

- Format code:

```
$ poetry run black src/
```

- Type check:

```
$ poetry run mypy src/
```

## How Imports Work

This project uses the [src-layout](https://realpython.com/python-application-layouts/) and [Poetry](https://python-poetry.org/) for dependency and environment management.

When you run:

```
$ poetry install
```

Poetry installs your package in **editable mode** (like `pip install -e .`).  
This means you can import your code from anywhere in the project, including notebooks and tests, using:

```python
from hubeau_py.client import HubeauClient
```

**You must always run code (scripts, notebooks, tests) in the Poetry environment** so that imports work correctly:

### Recommended: Poetry Commands

- For notebooks:
  - Launch with `poetry run jupyter notebook` or select the `.venv` interpreter in VS Code.
- For tests:
  - Run with `poetry run pytest`
- For scripts:
  - Run with `poetry run python your_script.py`
- Or enter a Poetry-managed shell: `poetry shell`
  and now run: python, pytest, etc.

### Alternative: Activate the Virtual Environment Manually

If you prefer, you can activate the `.venv` directly (for example, in a terminal or before launching Jupyter/VS Code):

```
$ source .venv/bin/activate
```

Once activated, any Python or pip command will use the project environment.

> **Note:**  
> Whether you use `poetry run ...`, `poetry shell`, or activate `.venv` directly, you’re using the same environment managed by Poetry.  
> This ensures all imports (like `from hubeau_py.client import HubeauClient`) work as expected in scripts, tests, and notebooks.

> **Windows users:**  
> It is recommended to use [WSL2](https://learn.microsoft.com/en-us/windows/wsl/) for a smoother Unix-like experience.  
> If you prefer native Windows, you will need to adapt the commands and environment activation steps to your setup.

For more, see the [Poetry documentation](https://python-poetry.org/docs/basic-usage/).

## VS Code Users

A `.vscode/settings.json` is included to provide a consistent development environment for VS Code users:

- Automatically uses the Poetry-managed virtual environment
- Formats code on save with Black
- Organizes imports on save
- Runs mypy type checking with the correct interpreter

Feel free to adjust these settings for your personal workflow if needed.

> **Customizing VS Code settings**
>
> The `.vscode/settings.json` file in this repository provides recommended project settings for all contributors.
>
> If you want to adjust these settings for your personal workflow **without affecting version control**, you can:
>
> - **Override settings in your personal (user) settings:**  
>   Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`), type `Preferences: Open User Settings (JSON)`, and add your overrides there.  
>   User settings take precedence over workspace settings for most editor preferences.
>
> - **Avoid committing unintended changes:**  
>   If you do change `.vscode/settings.json`, double-check with `git status` before committing, and use `git restore .vscode/settings.json` to undo accidental edits.
>
> For more details, see the [VS Code documentation on settings](https://code.visualstudio.com/docs/configure/settings).

## Inspect Scripts

The [`scripts/inspect_*.py`](scripts/) scripts allow you to quickly explore the field types and example values returned by each Hubeau API endpoint. These tools are useful for:

- Understanding the structure of API responses
- Maintaining and updating Pydantic models
- Debugging data issues or undocumented fields

**Usage:**

```python
$ poetry run python scripts/inspect_station_pc.py
$ poetry run python scripts/inspect_operation_pc.py
```

You can adjust the `n` parameter in each script (edit the script and change `n=10`, for example) to control how many records are fetched and inspected.

## License

MIT License © Pierre Feilles
