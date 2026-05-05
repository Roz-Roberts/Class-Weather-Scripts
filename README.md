# Class-Weather-Scripts
A collection of python scripts for a class on synoptic and mesoscale dynamics. 

## Running scripts

Scripts live in the `Scripts` directory and are run through `main.py`.

List available scripts:

```powershell
.\.venv\Scripts\python.exe main.py list
```

Run a script:

```powershell
.\.venv\Scripts\python.exe main.py run script_name
```

## Terminal autocomplete

The CLI supports Click shell completion for script names. After completion is
enabled, typing a partial script name such as `pack` after the `run` command can
complete to `packages_list`.

Click includes built-in completion support for Bash, Zsh, and Fish. For Bash,
run this from the project directory:

```bash
eval "$(_MAIN_PY_COMPLETE=bash_source python main.py)"
```

For Zsh:

```zsh
eval "$(_MAIN_PY_COMPLETE=zsh_source python main.py)"
```

For Fish:

```fish
env _MAIN_PY_COMPLETE=fish_source python main.py | source
```

PowerShell is not one of Click's built-in completion shells. In PowerShell, use
`main.py list` to see script names, or use Git Bash, Zsh, or Fish for Click tab
completion.

## Debugging scripts

### Package list

`Scripts/packages_list.py` prints all project packages listed in `pyproject.toml`
along with the installed version found in the current Python environment. This is
useful for checking which packages are available after adding or updating
dependencies with `uv`.

Run it with:

```powershell
.\.venv\Scripts\python.exe main.py run packages_list
```
