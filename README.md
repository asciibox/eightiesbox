# EightiesBox

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
- One-liners input capability via `oneliners.py`.
- Ability to display ANSI files located in the `ansi` directory.

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
pip install ochre flask pymongo flask_socketio
```

(Install any other missing packages as needed.)

Download mongoDB from https://www.mongodb.com/try/download/community

Install it without installing it as server. Create a directory called c:\data. Go to the bin folder in which the mongod.exe resides. Start mongod.exe.

Without mongoDB it won't go further than the login page.

# Quickstart

Call

python app.py
