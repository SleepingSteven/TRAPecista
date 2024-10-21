# Help
Welcome to the help and documentation page for TRAP (Test Results Analysis Platform), where you can store and run scripts and interact with the Carvings and NXCALLS databases. This page serves as your starting point to understand and utilize TRAP effectively. Here's what you'll find in this documentation:

* Overview
* Files
* Jobs
* Permissions
* TRAP Package

## Overview
TRAP is a platform where you can upload, run, and publish scripts. They run on an isolated, containerized environment within CERN's OKD4 (Openshift) service. It makes distributing small pieces of code easier and makes them easier to maintain, with versioning and documented parameters.

## Files
The files tab is where you can upload, download, and manage your files. You can create new folders to organize your files, and you can upload files to those folders. The root folder is the top-level folder, and cannot be deleted. Additionally, you cannot upload files directly to the root folder.

To view the contents of a folder, click on the folder name. To upload, download, or delete a folder/file, right click on the folder/file name. To view the contents of a file, click on the file name. Images and text files can be viewed directly in the browser, and code will be displayed with syntax highlighting. If you are viewing one of these file types, you will see action buttons at the top of the display page that will allow you to delete or download the file. You can also view the file's metadata, including the file size, creation date, and last modified date. Finally, you are also able to run it if it is a script, which are automatically identified by the .py extension.

### Scripts
A script is a Python file that can be run in the TRAP environment. You can upload a script by simply uploading a Python file with the .py extension. Once uploaded, you can run the script by clicking the "Run" button in the file viewer.

Each script can also have a number of input parameters, which you can specify in the "Info" dialog in the "Script Parameters" section. You can give it a name and a default value, and specify whether the parameter is required or optional. When running the script, you can specify the values for these parameters, and the defaults will be pre-filled. These parameters can be accessed through the TRAP package, which is automatically imported when running a script. Below is an example of how to access these parameters in your script:

```python
PARAM1 = trap.params.get("PARAM1")
PARAM2 = trap.params.get("PARAM1", "default_value")
NON_EXISTING_PARAM = trap.params.get("NON_EXISTING_PARAM", "default_value")

print(f"{PARAM1 = }")
print(f"{PARAM2 = }")
print(f"{NON_EXISTING_PARAM = }")
```

Assuming the script is run with `PARAM1="text for param 1"` and `PARAM2="text for param 2"`, the output will be:

```bash
PARAM1 = 'text for param 1'
PARAM2 = 'text for param 2'
NON_EXISTING_PARAM = 'default_value'
```

These might be useful for specifying file paths, database connection strings, or other configuration values, that might change between different runs of the script. Instead of having to upload a different script for each configuration, you can simply specify the values when running the script, since editing is not allowed.

## Jobs
The Jobs section is where you can run your scripts and view the results. You can create new jobs by pressing the "New" button, selecting a script, and specifying the input parameters. You can also view the status of your jobs, including whether they are running, completed, or failed. You can view the output of your jobs, including any errors or warnings that occurred during execution, by clicking the corresponding Job ID.

## Permissions
The Permissions section is where you can view the permissions that have been granted to you, as well as ask for permissions from other an admin user.

## TRAP Package
The TRAP package is a Python package that is automatically imported when running a script. It contains a number of useful functions and classes that you can use in your scripts. It is divided into a number of modules, described below.

### Filesystem Module
The filesystem module contains functions for working with the remote filesystem. This is necessary since the scripts are run in a Docker container, and do not have access to the host filesystem. The remote filesystem is persistent, so any files you upload will be available to your scripts, and independent for every user. The filesystem module contains the following functions:

#### `trap.filesystem.save(path: str, contents: bytes, override: bool = False) -> None`
The save function saves the given contents to the specified path. If the file already exists, it will not be overwritten unless the override parameter is set to True. If the file does not exist, it will be created.

#### `trap.filesystem.save_file(local_path: str, remote_path: str, override: bool = False) -> None`
This is the same as `trap.filesystem.save(remote_path, open(local_path, "rb").read(), override)`. It is a convenience function and is preferable if the file you're trying to save has already been written to disk.

#### `trap.filesystem.load(path: str) -> bytes`
The load function loads the contents of the file at the specified path and returns it as bytes.

#### `trap.filesystem.open(file: str, mode: str = "r", encoding: Optional[str], newline: Optional[Literal["\n", "\r", "\r\n"]]) -> TextCloudFile | BinaryCloudFile`

The open function opens the file at the specified path and returns a file object, similarly to the built-in open function. The mode parameter specifies the mode in which the file should be opened, and can be one of the following:
* "r" - read mode
* "w" - write mode
* "a" - append mode
* "rb" - read binary mode
* "wb" - write binary mode
* "ab" - append binary mode

The encoding parameter specifies the encoding to use when reading or writing text files, ahe newline parameter specifies the newline character to use when reading or writing text files.

#### `trap.filesystem.ls(path: str) -> dict[str, list]`
The ls function lists the contents of the specified directory and returns a dictionary with two keys, "files" and "directories". The "files" key maps to a list of file names in the directory, and the "directories" key maps to a list of directory names in the directory.

#### `trap.filesystem.mkdir(path: str) -> None`
The mkdir function creates a new directory at the specified path. If the directory already exists, an error will be raised.

#### `trap.filesystem.remove(path: str) -> None`
The remove function removes the file or directory at the specified path. If the path does not exist, an error will be raised.

### Database Module
The database module contains classes and functions for working with the Carvings and other databases. Each database is a submodule of `trap.db`, so Carvings, for example, would be `trap.db.carvings`. It is important to note that `trap.db` submodules are not imported by running `import trap`, and must be imported using `import trab.db.carvings as cvg`, for example.

### `trap.db.[submodule].raw_query(query: str) -> list`
This method runs the specified query against the database identified by `[submodule]`.

### `class trap.db.[submodule].[TableName]`
All tables from `[submodule]` can be accessed as an SQL Alchemy object with this syntax. You can run queries using the standard SQL Alchemy syntax, like:
```python
import trap.db.carvings as cvg

print(cvg.CvgCircuit.query().filter(cvg.CvgCircuit.circuit_id > 300).all()) 
```

### Display Module
The display module contains functions for displaying data in the TRAP environment, such as tables and plots. They will appear in the output of the script when it is run.


#### `trap.display.display(filename: str, contents: Optional[bytes], local: bool = True, update: bool = False) -> None`
The display function displays the given contents in the TRAP environment. If the contents parameter is specified, the contents will be displayed directly. If not, the contents will be read from the file specified by the filename parameter. If the local parameter is set to True, the filename will be interpreted as a local file path, and the contents will be read from that file. Otherwise, the file will be read from the remote filesystem. If the update parameter is set to True, the TRAP display will only show one instance of this file, and subsequent calls will modify the existing one.


## Params Module
The params module contains functions for working with the script parameters.


### `trap.params.get(name: str, default: Optional[str]) -> str`
The get function gets the value of the parameter with the given name. If the parameter does not exist, the default value will be returned.