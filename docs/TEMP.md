# Temporary Information

This is a temporary file for a forgetful amateur developer who needs reminders.

## Virtual Environment

### How to create a virtual environment

First make sure that `pip` and `venv` are installed. If not, simply run

```bash
sudo nala install python3-pip python3.12-venv -y
```

Then run

```bash
python3 -m venv .venv
```

Make sure that `.venv` is included in you `.gitignore` file.

### How to activate the virtual environment

Run

```bash
source .venv/bin/activate
```

### How to deactivate the virtual environment

Run

```bash
deactivate
```

## Packages that are needed

These are the packages that have been installed:

- `pyyaml` (`pyyaml-6.0.3`)

To install them inside the virtual environment run:

```bash
pip install pyyaml 
```
