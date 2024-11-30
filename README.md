# PySANEBridge

## SANE

[SANE](http://www.sane-project.org/) is a scanner API written for Linux machines allowing generalisation of a supported scanner to a common interface.

In simple terms, that means that as long as you have a device running linux close to a supported scanner, you can turn that scanner into a wireless enabled machine.

In my particular setup, a Raspberry Pi 3B+ running raspbian (debian) hosts the SANE service. This enables remote scanning on a relatively old HP machine which has no WiFi functionality.

## That's SANE, what is this package?

PySANEBridge is mostly to experiment with PyQT, however the idea originally came around as the current SANE frontends are... lacking on Windows.

As the underlying technolgies are PyQT and ssh, this package is portable on both Windows and Linux (tested on Windows 11 and Ubuntu 24.04).

Obviously, as an experimental package, the functionalities are both limited and cumbersome. **I never intended for this to be a tool used by others.**

You are, of course, welcome to build on (or take from!) the ideas present here.

## Installation

If you still want to experiment with using this package, it can be installed and used.

It is pip installable, though not present on PyPi. As such, you must do a local install.

This can be done with the following steps:

1. `git clone` this repository
2. `pip install ./PySANEBridge` (optionally, use the `-e` flag for an "editable" install that can be used for development)

The install is mostly for the dependencies, therefore you may manually install those and skip on the install of this package. They are located in `pyproject.toml`.

## Usage

### Settings

Settings can be changed by editing the `settings.ini` file.

This file is generated by the `Settings` class, and will regenerate with defaults if deleted.

The available settings are as follows:

#### userhost

This must be the `user@host` string used to ssh into the machine running SANE. 

This defaults to `localhost`, but should be changed to the address of your machine. In my case it is `pi@pisane`, since I'm using an ssh config that allows me to ssh into that machine at that address.

```
Note:
It is important that you can ssh into your target machine without entering a password.
An ssh-key is the best solution to this.
```

#### resolution

This is the _scan_ resolution in DPI

Defaults to `300`

```
Note:
Values below 75 will raise an exception, the minimum available scan DPI for SANE
```

```
Tip:
The DPI of the file can be set on save.
```

#### skip_scan

Used for testing purposes, skips the actual scanning if `True`, reading from a file located at `tests/load.png`.

Defaults to `False`

## User Interface

On running the `main.py` script, you will be greeted with a window which has 3 buttons: Scan, Save and Clear

![image](https://github.com/user-attachments/assets/3cde0336-19d7-4e3c-bc20-0245633bee2f)

### Scan

This button attempts to connect to the server and perform a `scanimage` command, then return the file.

If skip_scan is True, it will instead load the file from `tests/load.png`

You can scan as many times as you want, and the result will be loaded into the terminal.

Images will be previewed within the main window at a reduced size (400px width).

### Save

This saves all scanned images as a single pdf.

You can choose your filename and output DPI here

![image](https://github.com/user-attachments/assets/49556eca-9cb9-4772-80b0-b1bfd3e28cad)

```
Note:
Files will be enforced to pdf format. Any other file type will be ignored.

e.g.
  saving "foo.png" will produce "foo.pdf"
```

### Clear

The clear button will remove all stored images.

```
Warning!
This does not ask for confirmation
```

#### Remove

Short of clearing the whole scan storage, you can remove individual pages using the Remove button

![image](https://github.com/user-attachments/assets/21d55736-dcd9-4db6-b58b-321f32d938d1)

## Contributions

Contributions are always welcome, feel free to submit a pull request or an issue if you are inclined to do so!

Thanks for reading :)
