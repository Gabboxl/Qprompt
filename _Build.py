##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import os.path as op
from xml.etree import ElementTree

import auxly
import auxly.filesys as fsys
from auxly import shell
from ubuild import main, menu
from qprompt import Menu

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

@menu("v")
def check_version():
    with fsys.Cwd(".", __file__):
        shell.call("_Check_Versions.py")

@menu("t")
def run_tests():
    with fsys.Cwd("tests", __file__):
        shell.call("_Run_Tests.py")

@menu
def package():
    Menu(install_package_locally, upload_to_pypi).main(header="Package")

@menu
def docs():
    Menu(readme_excerpt, all_docs, open_docs).main(header="Docs")

@menu
def browse():
    def github(): auxly.open("https://github.com/jeffrimko/qprompt")
    def pypi(): auxly.open("https://pypi.org/project/qprompt/")
    def docs(): auxly.open("https://qprompt.readthedocs.io/")
    Menu(github, pypi, docs).main()

def install_package_locally():
    with fsys.Cwd("lib", __file__):
        shell.call("_Install_Package.py")

def upload_to_pypi():
    with fsys.Cwd("lib", __file__):
        shell.call("_Upload_PyPI.py")

def readme_excerpt():
    tempxml = "temp.xml"
    shell.call(f"asciidoctor -b docbook -o {tempxml} README.adoc")
    e = ElementTree.parse(tempxml).getroot()
    fsys.delete(tempxml)
    ns = {'db': 'http://docbook.org/ns/docbook', 'xml': 'http://www.w3.org/XML/1998/namespace'}
    rst = ""
    for sect in ["_introduction", "_status", "_requirements", "_installation"]:
        xml = ElementTree.tostring(e.find(f".//db:section[@xml:id='{sect}']", ns)).decode("utf-8")
        fsys.File(tempxml).write(xml)
        rst += shell.strout(f"pandoc -r docbook -w rst --base-header-level=2 {tempxml}")
        rst += "\n\n"
    fsys.File(r"doc\source\readme_excerpt.rst").write(rst)
    fsys.delete(tempxml)
    print("Readme excerpt generated.")

def all_docs():
    readme_excerpt()
    with fsys.Cwd("doc", __file__):
        shell.call("make html")

def open_docs():
    index = r"doc\build\html\index.html"
    if not op.isfile(index):
        docs()
    auxly.open(index)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    main()
