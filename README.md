# tkScenarist

Screen writing made simpler.


#### tkScenarist: internationalized

Retrouvez toute la **documentation en français** sur le
[wiki du projet]
(https://github.com/tarball69/tkScenarist/wiki/Accueil).

## Introduction

**tkScenarist** is a simple Python3/Tkinter application aiming to make
movie screen writing simpler for scenarists.

This software is a **freefullware** (see [below](#freefullware)).


## Copyright

tkScenarist - screen writing made simpler.

Copyright (c) 2014+ Raphaël Seban <motus@laposte.net>


## License

This software is licensed under **GNU GPL General Public License v3**.

License terms:

> This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

> This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

> You should have received a copy of the GNU General Public License
along with this program.

> If not, see http://www.gnu.org/licenses/


## Freefullware

What is a freefullware?

A **freefullware** is a new kind of software:

* Free as in Freedom;
* Free of charge (gratis);
* Ad-free (no advertisement at all);
* Donate-free (no 'Donate' button at all);
* 100% virus-free;
* no counterpart at all;
* really absolutely free;

Just get it and enjoy.

That's all, folks!


## Documentation

Please, feel free to visit our wiki wiki online documentation at:

https://github.com/tarball69/tkScenarist/wiki


## Features

At this time:

* All project management stays in one and unique project file
(extension: `.scn` or `.zip`, as if you like);

* In case of emergency, it is still possible to simply unzip this
project file and to get each project fragment into a simple text file:
the .zip archive internal structure has been thought this way to help
you mastering your data at any moment, in any case;

* First tab is project's data: title, subtitle, episode number/title,
author, author e-mail and phone (plus some stats info);

* Second tab is a `draft/extra notes` text zone you may need, in order
to keep some good idea along with your pitch/scenario;

* Third tab is the `pitch/concept` text zone where you should write all
the strongest steps of your story;

* If you're looking for inspiration, there is also a menu `Tools >
Story/pitch templates` utility dialog designed to simplify pitch
startups;

* Fourth tab is a great tool named `Characters`, where you can manage
all the characters of your story: name list, character's history log,
characters relations and so on;

* You also have a menu `Tools > Name database` utility dialog where you
can search amongst thousands of names coming from all origins;

* Fifth tab is the `Scenario` text zone, with scene browser, contextual
hints, character's log reminder, estimated page count and movie
duration;

* By now, a new menu `Tools > Scenario Elements Editor (SEE)` utility
dialog is available for finer script edition tuning;

* Sixth tab is the `Storyboard` panel, with scene browser, selected
scene preview, shot list manager, shot editor and character's log
reminder;

* Seventh tab is the `Resources` panel, including staff, events and
hardware main sections, plus several subsections, data form for
resource items and a visual planning widget;

* PDF export feature is now a multiple document user dialog with
several options;

* Software has been **fully translated to french** (metropolitan french
&ndash; fr_FR);


## Screenshots

![image](https://raw.githubusercontent.com/tarball69/tkScenarist/master/images/screenshots/screenshot-001.png)
![image](https://raw.githubusercontent.com/tarball69/tkScenarist/master/images/screenshots/screenshot-002.png)
![image](https://raw.githubusercontent.com/tarball69/tkScenarist/master/images/screenshots/screenshot-003.png)
![image](https://raw.githubusercontent.com/tarball69/tkScenarist/master/images/screenshots/screenshot-004.png)
![image](https://raw.githubusercontent.com/tarball69/tkScenarist/master/images/screenshots/screenshot-005.png)
![image](https://raw.githubusercontent.com/tarball69/tkScenarist/master/images/screenshots/screenshot-006.png)
![image](https://raw.githubusercontent.com/tarball69/tkScenarist/master/images/screenshots/screenshot-007.png)
![image](https://raw.githubusercontent.com/tarball69/tkScenarist/master/images/screenshots/screenshot-008.png)
![image](https://raw.githubusercontent.com/tarball69/tkScenarist/master/images/screenshots/screenshot-009.png)
![image](https://raw.githubusercontent.com/tarball69/tkScenarist/master/images/screenshots/screenshot-010.png)
![image](https://raw.githubusercontent.com/tarball69/tkScenarist/master/images/screenshots/screenshot-011.png)
![image](https://raw.githubusercontent.com/tarball69/tkScenarist/master/images/screenshots/screenshot-012.png)
![image](https://raw.githubusercontent.com/tarball69/tkScenarist/master/images/screenshots/screenshot-013.png)
![image](https://raw.githubusercontent.com/tarball69/tkScenarist/master/images/screenshots/screenshot-014.png)
![image](https://raw.githubusercontent.com/tarball69/tkScenarist/master/images/screenshots/screenshot-015.png)
![image](https://raw.githubusercontent.com/tarball69/tkScenarist/master/images/screenshots/screenshot-016.png)


## Development status

    Development Status :: 4 - Beta

Software has been:

* Linux:
    * TESTED OK for all distros;
* MacOS:
    * NOT YET TESTED;
* MS-Windows:
    * TESTED only on MS-Windows(tm) 8, but seems to work quite fine for
    the moment;

Any [feedback](https://github.com/tarball69/tkScenarist/issues) is
still the welcome.


## Installation

This program does *NOT* need to be installed in any way.

Simply download it, unzip it (into an `~/apps/` applications directory,
for example) and use it right now.


## Quick start

### Caution

This software runs only with **Python3** and **Tkinter** installed
on your machine.

**No dependencies**, no third-part lib to install on more.

If you have Python3 programming language correctly installed, Tkinter
library should also be installed **by default** as a Python standard
lib.

Any **ImportError** will mean either you are trying to launch the
software with Python2 or you don't have **Tkinter** library correctly
installed on your system.

Installing a Python3 version of the language **does not alter** an
already installed Python2 version in any way.

You may consider installing Python3 from:

https://www.python.org/downloads/ (Ctrl+click: open in new tab)

### Notice

Many major Linux distributions (e.g. Ubuntu, SuSE, etc) do already have
a **pre-installed** Python3/Tkinter package.

In this particular case, **you should *NOT* consider** to make any
special installation by yourself.

Simply download and use this program as is.

### MS-Windows&trade; users

Simply double-click on `tkscenarist.py` file to launch app.

#### Hint: no console app

Many MS-Windows&trade; users wonder why do they have a shell console
window coming up with the application on startup.

This is a quite normal Python default behaviour.

If you wish to use a Python application **without** its dedicated shell
console window, simply rename file extension from `.py` to `.pyw` and
then launch it again.

For the present case, this means you should rename `tkscenarist.py` to
`tkscenarist.pyw` and then run it once again.

### UNIX/Linux

Click on `tkscenarist.py` file if it has the executable sticky bit on
or open a shell console and launch file:

    $ python3 tkscenarist.py

That's all, folks!

Enjoy!
