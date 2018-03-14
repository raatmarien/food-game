from cx_Freeze import setup,Executable

includefiles = ['Munro.ttf']

build_exe_options = {"packages": ["os"], "excludes": ["tkinter"], 'include_files':includefiles}

setup(
    name = 'Traffic Light Game',
    version = '1.0',
    description = 'Distributed under the GPLv3+',
    author = 'Marien Raat',
    options = {"build_exe": build_exe_options}, 
	executables = [Executable(script="main.py", targetName="tlg.exe")]
)
