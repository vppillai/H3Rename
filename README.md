# Harmony 3 MPLABX project renamer

Renaming a H3 project in MPLABx is not straightforward. This tool does it in a reasonably sane manner. 

_Tested with : MPLABX `5.45` , Harmony Launcher `3.6.4`_

## Running the tool

```bash
usage: H3Rename [-h] [-l PROJECTNAME] -p PATH -n NPROJECT -c CONFIG -x NCONFIG

Tool to rename Harmon3 MPLABX projects. v1.1.0

optional arguments:
  -h, --help            show this help message and exit
  -l PROJECTNAME, --projectName PROJECTNAME
                        display name of the project if different from .X path

required arguments:
  -p PATH, --path PATH  Location of Project up to the .X
  -n NPROJECT, --nProject NPROJECT
                        updated project name without the .X
  -c CONFIG, --config CONFIG
                        Current config name
  -x NCONFIG, --nConfig NCONFIG
                        New config name
```

 > **Note:** If your project path and project display name are different, make sure you pass the correct argument to the `-l` flag. While renaming with `-l`, the project path will also be updated to match the new project name. In case you want the path to be different, it (The .X folder) can be directly renamed in file explorer. 

## EXE release

The executable was created using pyinstaller for people who have difficulty installing python.

```bash
pyinstaller --onefile .\H3Rename.py -i .\favicon.ico --clean
```

## License

"THE BEER-WARE LICENSE" (Revision 42): vysakhpillai@gmail.com wrote this file. As long as you retain this notice you can do whatever you want with this stuff. If we meet some day, and you think this stuff is worth it, you can buy me a beer in return —Vysakh P Pillai
