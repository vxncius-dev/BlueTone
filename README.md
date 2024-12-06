# BlueTone - Color Temperature Adjustment Tool

**BlueTone** is a graphical application designed to help users adjust their screen's color temperature based on environmental lighting conditions. By using this tool, users can reduce eye strain caused by excessive blue light exposure and improve their overall screen experience. BlueTone also allows users to install and configure an essential system tool (`xsct`), which is required to adjust color temperature on the system.

## Features

- Adjust the screen color temperature in Kelvin based on predefined settings.
- Install and configure the `xsct` tool automatically if not present on the system.
- A simple, intuitive graphical interface built with **Kivy** and **KivyMD**.
- Installation and management of `xsct` from within the application, including moving it to a global directory and creating an alias for quick access.
- Customizable interface with a dark theme and primary blue color palette.

## Prerequisites

Before using BlueTone, the following software must be installed on your system:

1. **Python 3.x**
   - BlueTone is written in Python, and requires Python 3.6 or higher.
   
2. **Kivy** and **KivyMD**
   - The graphical user interface is built using Kivy and KivyMD. These libraries can be installed using `pip`.
   
3. **xsct (Screen Color Temperature Tool)**
   - `xsct` is the core tool used to adjust the color temperature of your screen. BlueTone will automatically attempt to install and configure it if not found.

## Installation

Follow the steps below to install and run BlueTone on your system.

### Step 1: Clone the Repository

Clone the BlueTone repository to your local machine using Git:

```bash
git clone https://github.com/vxncius-dev/BlueTone.git
cd BlueTone
```

### Step 2: Install Dependencies

Install the required dependencies, including Kivy, KivyMD, and others necessary for the application to run:

```bash
pip install -r requirements.txt
```

If the `xsct` tool is not already installed, BlueTone will attempt to install it automatically when run for the first time.

### Step 3: Run the Application

To run BlueTone, simply execute the following command:

```bash
python3 main.py
```

Upon starting, the app will check if `xsct` is installed. If not, it will prompt you to install it. Once installed, the app will allow you to adjust the color temperature of your screen based on predefined settings.

### Step 4: (Optional) Move to Global Directory and Create Alias

After the installation, you can move the `xsct` tool to a global directory and create an alias to run BlueTone from anywhere in your terminal. This step is optional but highly recommended for ease of use.

- The application will ask for your **sudo password** to proceed with these actions.
- The `xsct` tool will be moved to `/usr/local/bin/sct`.
- An alias will be created so you can run BlueTone by typing `BlueTone` anywhere in your terminal.

**To create the alias manually:**

```bash
# Add this line to your .bashrc or .zshrc file
alias BlueTone='python3 /path/to/BlueTone/main.py'

# Reload the shell configuration
source ~/.bashrc   # or source ~/.zshrc
```

## Usage

Once BlueTone is running, you'll be presented with a list of temperature settings. Simply select a temperature to adjust the screen's color temperature accordingly.

### Example Temperatures Available

- 1700K - Match flame, low pressure sodium lamps (LPS/SOX)
- 1850K - Candle flame, sunset/sunrise
- 2400K - Standard incandescent lamps
- 2550K - Soft white incandescent lamps
- 2700K - Soft white compact fluorescent and LED lamps
- 3000K - Warm white compact fluorescent and LED lamps
- 3200K - Studio lamps, photofloods
- 3350K - Studio 'CP' light
- 4100K - Horizon daylight
- 5000K - Tubular fluorescent or daylight compact fluorescent lamps (CFL)
- 6500K - LCD or CRT screen
- 15000K - Clear blue poleward sky

### Color Temperature Adjustment

- Clicking on any item will instantly adjust your screen's color temperature using the `xsct` tool.
  
If you encounter issues with the tool or have any questions, feel free to open an issue on GitHub.

## Screenshots

![image](https://github.com/user-attachments/assets/852921c6-73f0-43b0-8efb-4caa3b50a0d7)

## Troubleshooting

- **xsct not found**: If you receive an error that `xsct` is not installed, make sure you've allowed the app to install it automatically, or install it manually by following the instructions on the `xsct` GitHub page.
  
- **Permissions issues**: Ensure you have the necessary permissions to move files to system directories like `/usr/local/bin`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **Kivy** - For building the graphical user interface.
- **KivyMD** - For providing Material Design components to enhance the interface.
- **xsct** - For the screen color temperature adjustment tool.
- **Python** - For enabling the development of cross-platform applications with ease.

This README should provide all the necessary information to your users, making it easy for them to install, use, and troubleshoot your app.
