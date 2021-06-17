#"THE BEER-WARE LICENSE" (Revision 42):
# <vysakhpillai@gmail.com> wrote this file. 
# As long as you retain this notice you can do whatever you want with this stuff. 
# If we meet some day, and you think this stuff is worth it, you can buy me a beer in return 
#                                                                        —※Vysakh P Pillai※

import os,sys
import shutil 
import re
import argparse
from colorama import init, Fore, Back, Style
from lxml import etree
import yaml

__version__="v1.1.0"

def replace_project_configuration(path,config,nConfig):
    #replace the project name present in config for programmer to go
    pass


def replace_configuration(path,config,nConfig):
    with open(f'{path}//nbproject//configurations.xml', "rt") as configIn:
        with open(f'{path}//nbproject//configurations_new.xml', "wt") as configOut:
            for line in configIn:
                configOut.write(re.sub(r'\b{input}\b'.format(input=config),nConfig,line))
    shutil.move(f'{path}//nbproject//configurations.xml',f'{path}//nbproject//configurations.xml.bkp')
    os.rename(f'{path}//nbproject//configurations_new.xml',f'{path}//nbproject//configurations.xml')


def update_project_xml(path,nProject,config,nConfig,inProjectName):
    nsMap={"ns":"http://www.netbeans.org/ns/project/1",
            "mns":'http://www.netbeans.org/ns/make-project/1'}

    projectTree = etree.parse(f'{path}//nbproject//project.xml')
    project=projectTree.getroot()

    if not inProjectName:
        inProjectName=os.path.basename(path)[:-2]

    projName=project.findall('ns:configuration/mns:data/mns:name',nsMap)[0]
    if projName.text==inProjectName:
        projName.text=nProject

    for conf in project.findall('ns:configuration/mns:data/mns:confList',nsMap):
        confName=conf.findall("./mns:confElem/mns:name",nsMap)[0]
        if confName.text==config:
            confName.text=nConfig
    
    projectTree.write(f'{path}//nbproject//project_new.xml', encoding="utf-8",xml_declaration=True)
    shutil.move(f'{path}//nbproject//project.xml',f'{path}//nbproject//project.xml.bkp')
    os.rename(f'{path}//nbproject//project_new.xml',f'{path}//nbproject//project.xml')

def update_settings_yml(path,nProject,config,nConfig):
    with open(f'{path}//..//src//config//{config}/{config}.mhc/settings.yml') as settingsFile:
        settings = yaml.load(settingsFile, Loader=yaml.FullLoader)
        settings["configName"]=nConfig
        settings["folderName"]=nProject
        settings["projectName"]=nProject
    shutil.move(f'{path}//..//src//config//{config}/{config}.mhc/settings.yml',f'{path}//..//src//config//{config}/{config}.mhc/settings.yml.bkp')
    
    with open(f'{path}//..//src//config//{config}/{config}.mhc/settings.yml','w+') as settingsFile:
        yaml.dump(settings,settingsFile)

def update_project_yml(path,nProject,config,nConfig):
    with open(f'{path}//..//src//config//{config}/{config}.mhc/project.yml') as settingsFile:
        settings = yaml.load(settingsFile, Loader=yaml.FullLoader)
    
    for file in settings["files"]:
        file["physicalPath"]=re.sub(r'\b{input}\b'.format(input=config),nConfig,file["physicalPath"])
        file["logicalPath"]=re.sub(r'\b{input}\b'.format(input=config),nConfig,file["logicalPath"])
    for setting in settings["settings"]:
        setting["value"]=re.sub(r'\b{input}\b'.format(input=config),nConfig,setting["value"])

    shutil.move(f'{path}//..//src//config//{config}/{config}.mhc/project.yml',f'{path}//..//src//config//{config}/{config}.mhc/project.yml.bkp')

    with open(f'{path}//..//src//config//{config}/{config}.mhc/project.yml','w+') as settingsFile:
        yaml.dump(settings,settingsFile)


def rename_mhc_folder(path,nProject,config,nConfig):
    os.rename(f'{os.path.dirname(path)}//src//config//{config}//{config}.mhc',f'{os.path.dirname(path)}//src//config//{config}//{nConfig}.mhc')

def rename_config_folder(path,nProject,config,nConfig):
    os.rename(f'{os.path.dirname(path)}//src//config//{config}',f'{os.path.dirname(path)}//src//config//{nConfig}')

def rename_project_folder(path,nProject):
    os.rename(path,f'{os.path.dirname(path)}//{nProject}.X')

def check_project(path,nProject):
    if not os.path.isdir(path):
        print(f'{Fore.RED}Project path does not exist')
        sys.exit(-1)
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_\-]+$', nProject):
        print(f'{Fore.RED}New project name is invalid')
        sys.exit(-2)
    if not os.path.basename(path).endswith('.X'):
        print(f'{Fore.RED}Invalid project path. Provide path till .X')
        sys.exit(-3)
    
def check_configuration(config,nConfig):
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_\-]+$', nConfig):
        print(f'{Fore.RED}New config name is invalid')
        sys.exit(-4)
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_\-]+$', config):
        print(f'{Fore.RED}Current config name is invalid')
        sys.exit(-5)

if __name__ == "__main__":
    init(autoreset=True)
    parser = argparse.ArgumentParser(
        description=f"Tool to rename Harmon3 MPLABX projects. {Fore.LIGHTMAGENTA_EX}{__version__}{Fore.RESET}", prog="H3Rename")
    parser.add_argument('-l', '--projectName', dest='projectName', help='display name of the project if different from .X path')
    requiredNamed = parser.add_argument_group('required arguments')
    requiredNamed.add_argument('-p', '--path', dest='path', help='Location of Project up to the .X', required=True)
    requiredNamed.add_argument('-n', '--nProject', dest='nProject', help='updated project name without the .X', required=True)
    requiredNamed.add_argument('-c', '--config', dest='config', help='Current config name', required=True)
    requiredNamed.add_argument('-x', '--nConfig', dest='nConfig', help='New config name', required=True)
    args = parser.parse_args()

    args.path=os.path.abspath(args.path)
    
    check_project(args.path,args.nProject)    
    check_configuration(args.config,args.nConfig)
    replace_configuration(args.path,args.config,args.nConfig)
    update_project_xml(args.path,args.nProject,args.config,args.nConfig,args.projectName)
    update_settings_yml(args.path,args.nProject,args.config,args.nConfig)
    update_project_yml(args.path,args.nProject,args.config,args.nConfig)
    rename_mhc_folder(args.path,args.nProject,args.config,args.nConfig)
    rename_config_folder(args.path,args.nProject,args.config,args.nConfig)  
    rename_project_folder(args.path,args.nProject)    
