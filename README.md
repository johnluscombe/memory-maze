![Memory Maze](assets/memory-maze-logo.png "Memory Maze")

### How good is your memory?

Watch the path, and see if you can repeat it exactly. Be careful, you only have 3 incorrect guesses!

### What level can ***you*** get to?

## Developing

- Make sure [Python 3.6+](https://www.python.org/) is installed.
- Clone the repo.
- Run with `python -m memorymaze` (or `python3 -m memorymaze` in Unix-like environments).

Easy as that! This game uses Tkinter, which ships with the standard installation of Python, so no third-party libraries should be required.

## Building as a .exe

> This is only applicable to Windows environments.

- (Optional) Create a virtual environment and activate it.
    - `python -m venv venv` (or `python -m venv [desired-virtual-environment-name]`)
    - `venv/Scripts/activate.bat` (or `source venv/bin/activate` on Unix-like environments)
- Install PyInstaller: `pip install pyinstaller`.
- Run `pyinstaller memory-maze.spec`.
- A `memory-maze.exe` is available in the `dist` directory.
