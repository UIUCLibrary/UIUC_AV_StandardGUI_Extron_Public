# UIUC Standard AV System GUI - Extron ControlScript

This project provides common modules which drive the behavior of the UIUC Standard AV System GUI on Extron xi control processors using Extron Control Script 1.3r8.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

No installation of these project files are required. However, it is recommended that the latest version of Extron GlobalScripter, GUIDesigner, and Toolbelt be installed to deploy Control Script files to control processors and UI devices.

## Usage

Example files may be found in `/example`. To utilize these modules, the src files must be copied to the SFTP share on the Extron control processor. Create a directory named `modules` at the root of the SFTP share and copy the source files, located at `/src`, to this modules directory. Create an empty directory under `/user` named `states`.

To configure an Extron control processor, create a Global Scripter project and add your control processors and UI devices. Assign the GUI files, in `/gui` to the UI devices. Add the example `main.py` file as the project entry file. This contains code to allow the Control Script code to find the rest of the source files and to initialize the control system. It is recommended not to modify this file unless you know what you are doing.

In addition to `main.py`, `settings.py` needs to be modified to match your system hardware and imported into the control processor root of the Global Scripter project. If passwords are required to control your system hardware, it is recommended to use a `secrets_hardware.py` file to store these and import these into `settings.py`. 

The project can then be built to the controller through Global Scripter.

## Features

This project provides standardized, repeatable framework for Extron IPCP Pro xi control system deployment. The functionality of the project follows the standard campus GUI guidelines and is intended to closely match user functionality across multiple control system vendors.

## Requirements

Extron IPCP Pro xi control processors are required to utilize these modules. This project relies on Control Script xi 1.3r8. Code should be compatible with newer Control Script xi versions. This project does utilize features not found or disallowed in non-xi ControlScript.

`ConnectionHandler.py` provided by Extron and may be downloaded from [this thread](https://forum.extron.com/showthread.php?t=694&highlight=ConnectionHandler) in the [Extron Programmer Forums](https://forum.extron.com/index.php). This module may either be added to `/modules` in the SFTP share on the control processor or may be added to the Global Scripter project directly. There is not functional difference between these two locations.

## Contributing

*TBD*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Please create an issue or start a discussion.


