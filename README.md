# ocr-tts

## Description

This is a basic script which is intended to help people with sight issues read text 
content in video games which would otherwise be hard or impossible to read.

The initial use case is based on the game [Stray](https://store.steampowered.com/app/1332010/Stray/) 
which features a hovering text box floating around the screen, but always of the same 
size. 

If properly configured, this script will read out loud the content of the text box 
each time the player takes a screenshot of the game with the text box visible.

Please read below how to install, configure and run the script. At this time there is no standalone 
executable, but will try to package one in the near future. This is still a WIP. 

## How to install

This script requires a number of external dependencies. Please install them as described in the Requirements section 
below.

### Requirements

#### A text editor

You will need to edit a file. The regular notepad in windows will most likely break it, so I recommend downloading
and installing [Visual Studio Code](https://code.visualstudio.com/download) for this. It is also a very good text editor
in general. 

#### Python

This script requires Python 3.9 or above. Download it from here: https://www.python.org/downloads/

Install it normally, but make sure to click on the checkbox to add it to the `PATH` variable.

#### Tesseract

Tesseract is the OCR software that will read the text from the screenshot. It is a 3rd party stand-alone that needs to 
be installed on the system separately. You will most likely need the x64 version. 

Download the latest version of tesseract for windows from UB-Mannheim https://github.com/UB-Mannheim/tesseract/wiki

The version used when creating this script can be found at this link: 
https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.2.0.20220712.exe (link may expire in time)

The folder where this is installed needs to be added to the `PATH` variable. Check where it was installed and make a 
note of the path. It will most likely be either `C:\Program Files\Tesseract-OCR` or 
`C:\Program Files (x86)\Tesseract-OCR`

Instructions on how to add a folder to the `PATH` variable can be found [here](docs/env_variables.md). 

#### Screenshots 

The script waits for a screenshot to be created in a given folder and compares that screenshot to a given template to 
identify the section of the screenshot where the text can be found. In our use case that is a text box.

For example given [this screenshot](test_data/SCREENSHOT.png) the template file will need to be 
[like this](test_data/TEMPLATE_1.png)

The template file must match the resolution of the screenshot, so you will need to first play the game up until you 
can take a first screenshot with the text box at your normal resolution, then create the template file by cropping out 
the textbox from the screenshot and saving it separately. 

Make a note of the location where you saved the template file, we will need it to configure the script to find it later.

Note: You only need to do this once, the script will find similar text boxes in subsequent screenshots even if they 
have different text. However, it will only work for text boxes of identical size. It will not work for text boxes that 
appear when you find collectables for example.

### Setting up the script

You can clone this repo, or click on the green `Code` button in the upper right and click on `Download ZIP` to download 
the repo files, then extract them to any location. 

There are three important files in this location:
1. `main.py` -> the actual script file
2. `install.bat` -> a helper script that will install the requirements for the actual script
3. `run.bat` -> a helper script that will run the actual script for you
4. `settings.yaml` -> this is where the paths to the screenshots and the template need to be configured. This is just
an example. You will need to edit it and replace the paths with your correct paths.

Run the file `install.bat` to install the requirements for this script. It will create a new folder named `env`. This is
where a copy of python with all it needs is located. Don't delete it unless something goes wrong. Ignore it for now.

Open the file `settings.yaml` with a text editor like [Visual Studio Code](https://code.visualstudio.com/download) and 
edit the paths you see there by pasting the paths to your screenshot folder and to the template file. Keep the `'` 
apostrophes as they are in the given example. 

### Running the script

If you have configured it as described until now you can run the script by double clicking on the `run.bat` file. 
A black command prompt will appear and it will tell you that it is waiting for screenshots.

You can now start playing the game and when you see a text box you want to be read out loud take a screenshot. The 
window opened by the script will print out the text it recognized and you will hear Windows read the text back to you.
