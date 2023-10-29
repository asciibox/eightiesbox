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
| < 1280p      | 80 x 50            |
| >= 1280px    | 120 x 60           |

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

On Linux Python is pre-installed, on Windows you must make sure to download the correct installer

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

   This are the instructions for Ubuntu 22

   - Open Terminal.
   Run:
   ```
   wget https://repo.mongodb.org/apt/ubuntu/dists/jammy/mongodb-org/6.0/multiverse/binary-amd64/mongodb-org-server_6.0.11_amd64.deb
   ```

2. **Install the deb package**


   Run:
   ```
   sudo dpkg -i mongodb-org_6.0.x_amd64.deb
   ```


3. **Create Data Directory**

   - Run:
     ```
     sudo mkdir -p /data/db
     ```
4. **Run MongoDB**
   - Navigate to the `/usr/bin` folder
   - Start the application `mongod`

5. **Permissions**

   If it still does not work, make sure the directory has got the correct permissions
   - Run:
   ```
   sudo chown -R mongodb:mongodb /data/db
   ```

   Replace mongodb:mongodb with your username


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

# BBS advantages

Setting up a BBS, is a legal and often hobbyist activity aimed at creating a community, fostering discussions, or sharing information.
While it may be considered retro or unconventional given the current technological landscape, it's not criminal or harmful in the way that terrorist activities are.
Rather than causing harm, many people find value in the more intimate, text-based interactions that BBSes offer, as well as the sense of community that they can provide.

## Exploitative Data Practices of Major Tech Corporations

The issue of data privacy and the ever-increasing monetization of user data by large tech companies is a growing concern for many people. In this context, BBSes could offer several advantages:

### Privacy-Focused

One of the distinct advantages of Bulletin Board Systems (BBS) is their focus on text-based communication, which inherently limits the amount of personal information being shared.
Unlike mainstream social media platforms, where sharing images and videos is common, BBS users often communicate using only text.
This reduces the likelihood of unintentional oversharing of personal or sensitive information, such as locations, faces, or other identifiable markers.

Less Data Collection: Since BBSes are generally not commercial and don't rely on advertising for revenue, they have less incentive to collect user data.

### No Profiling

BBS operators generally don't have the means or the interest in performing detailed user profiling like large tech companies do.

### Direct Ownership

The data on a BBS usually resides in a single server, often owned by an individual or a small group, rather than being distributed across multiple data centers worldwide.
