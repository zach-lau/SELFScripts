# SELF Scripts
Scripts designed to automate some of the adminstrative tasks for SELF funding. Note that paths are hardcoded in several places in these scripts and you should update these paths with the paths on your local file system.
## Warning
These scripts are meant to make things easier but they don't work for every application (e.g. if it wasn't saved as a fillable pdf!) so make sure to double check the output.
## Usage
Download zip of folders from drive. Change hardcoded zip folder name to the appropriate name in the scripts. The following scripts can be run
- `unzip.py`: this will recursively unzip the files in the file structure
- `parse.py`: this will parse the fields used in the SELF tracking spreadsheet
- `get_descriptions.py`: this will get the descriptions of the activities in a format appropriate for the semesterly progress report.
- `explore_fields.py`: this is a helper script to explore the fields available in the pdf
## Developing
If you want to add new functionality it will usually suffice to call the `run_for_each` function available in `parse.py`. As a general development principle put all "library" style functions in `parse.py` and user-facing functions should get their own script.
