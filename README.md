# EightiesBox

![Vector image of a cosmic BBS world. Planets are shaped like vintage modems, orbiting around a central terminal sun displaying an ASCII menu. Shooting stars symbolize data transfer protocols like xmodem, ymodem, and zmodem. On one of the planets, a concert is happening where music is played from mod files, visualized as colorful waves. Floating mail envelopes connected by beams of light indicate the fido network. The space is filled with a file listing, illuminated with ANSI colors.](./docs/eightiesbox.jpeg)

## Overview

EightiesBox is an ASCII/ANSI-based web platform that mimics the vintage mailbox BBSes from the 1980s. Utilizing a JavaScript frontend powered by Phaser, a 2D game engine that employs WebGL for speedy performance, EightiesBox offers a nostalgic interface for modern web browsers.

- **Technologies Used**: Socket.io, MongoDB, Phaser
- **ANSI Parser**: Modified version of `stransi`
- **Responsive Canvas**: Different canvas sizes based on screen width

## Canvas Sizing

| Screen Width | Canvas Size (x, y) |
| ------------ | ------------------ |
| < 640px      | 40 x 25            |
| < 960px      | 80 x 50            |
| >= 960px     | 120 x 80           |

## Features

- User login and registration through `userregistration.py`.
  ![User registration](./docs/userregistration.jpg)
- One-liners input capability via `oneliners.py`.
  ![ANSI](./docs/oneliners.jpg)
- Ability to display ANSI files located in the `ansi` directory.
  ![ANSI](./docs/ansi.jpg)

## Architecture

### Client Side

- `client.js`: Handles Socket.io parsing.
- `main.js`: Responsible for initializing the Phaser canvas.

### Server Side

- `app.py`: Orchestrates the application's core logic.
- `sessiondata.py`: Contains the `SessionData` class to manage user sessions.

#### Session Management Example

```python
def on_new_connection():
    request_sid = request.sid
    sid_data[request_sid] = SessionData()

def on_connection_close():
    request_sid = request.sid
    if request_sid in sid_data:
        del sid_data[request_sid]
```

The `SessionData` class contains fields for managing session-specific actions. Multiple tabs can be opened, each having a separate session.

## Installation & Setup

### Requirements

- Python 3.x

### Installation

1. Clone the repository.
2. Install the required Python packages:

```bash
pip install ochre flask pymongo flask_socketio bcrypt
```

(Install any other missing packages as needed.)

# MongoDB Installation

## Windows

1. **Download MongoDB**
    - Navigate to [MongoDB Community Download Page](https://www.mongodb.com/try/download/community).
    - Download the installer suitable for your Windows version.

2. **Installation**
    - Run the installer.
    - When prompted, choose to install MongoDB **without setting it up as a service**.

3. **Create Data Directory**
    - Open the Command Prompt as an administrator.
    - Run the following command to create a directory for MongoDB to store its data:
      ```
      mkdir C:\data
      ```

4. **Run MongoDB**
    - Navigate to the `bin` folder where `mongod.exe` is located, typically `C:\Program Files\MongoDB\Server\[version]\bin\`.
    - Run `mongod.exe`.

## macOS

1. **Download MongoDB**
    - Visit [MongoDB Community Download Page](https://www.mongodb.com/try/download/community).
    - Download the TGZ file.

2. **Installation**
    - Open the Terminal.
    - Extract the downloaded TGZ file.
    - Move the extracted files to the desired installation directory, e.g., `/usr/local/mongodb`.

3. **Create Data Directory**
    - In the Terminal, run:
      ```
      mkdir -p /data/db
      ```

4. **Run MongoDB**
    - Navigate to the `bin` folder inside your MongoDB installation directory.
    - Run `./mongod`.

## Linux (Ubuntu)

1. **Download MongoDB**
    - Open Terminal.
    - Import the MongoDB public key:
      ```
      wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
      ```
    - Create a list file for MongoDB:
      ```
      echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
      ```
    - Reload the package database:
      ```
      sudo apt-get update
      ```

2. **Installation**
    - Install MongoDB:
      ```
      sudo apt-get install -y mongodb-org
      ```
    - **Important:** Do not start the MongoDB service.

3. **Create Data Directory**
    - Run:
      ```
      sudo mkdir -p /data/db
      ```

4. **Run MongoDB**
    - Navigate to the `bin` folder inside the MongoDB installation directory.
    - Run `mongod`.

# Quickstart

Call

python app.py

Open the page using http://localhost:5000

# BBS Sysop Guide

## Accessing the BBS

- **URL**: Open your web browser and navigate to [http://localhost:5000](http://localhost:5000).
  
- **Registration**: Register an account using the username `sysop` and set a secure password.

## Start Page and Resolution

- The start page you see is located in the `ansi` directory.
- The layout can differ based on your screen resolution. It's advisable to use a high-resolution display for optimal sysop (admin) settings.

## Menu Editor

After the initial oneliners, you'll be prompted to navigate to the menu editor. Here's how you can manage it:

### Creating a Menu

- Navigate through options using the cursor keys and press `Enter` to create a menu.

#### Type

1. Press `Enter` to modify this field.
2. A popup will appear; navigate using cursor keys.
3. Press `Enter` to access the submenu that opens to the right.
4. Choose an option, for example, "Goto menu".

- Note: A number, like 01, 02, 03, etc., will populate the 'Type' field.

### Editing the ANSI

- Press `ESC` or cursor up to reveal the menu bar.
- Navigate to "Edit" using the cursor keys and select "Edit Text" to enter the ANSI editor for the current menu.
- Insert text as desired.
- Press `ESC` and navigate to `File -> Leave ANSI Editor` to return to the menu editor.

#### Saving ANSI

- ANSI files can be saved via `File -> Save as ANSI file`.

### Saving the Menu

1. Press `ESC` to reveal the menu bar.
2. Navigate using the cursor keys to the 'Save' option.
3. Enter a filename, recommended: `MAIN.MNU`.

- This will be the main menu displayed to every user upon login.

### Additional Fields

- You can add more fields by utilizing the "Type" and the "Data" fields in the menu editor.
- Enter the filenames in the `Data` field for the menus you'd like to navigate to. It's advisable to use uppercase filenames.

