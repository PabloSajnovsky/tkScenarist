
# Getting started

## <a name="summary"/>Summary

* [Downloading the application](#download)
    * [Official release versions](#official-release-versions)
    * [Daily build](#daily-build)
    * [Forks and pull requests](#forks-and-pull-requests)
* [Installing tkScenarist](#install)
    * [General purpose](#general-purpose)
    * [Pre-requisites](#pre-requisites)
    * [UNIX/Linux](#unixlinux)
    * [MS-Windows&trade;](#ms-windows)
    * [Bug report](#bug-report)
* [First steps](#getting_started)
    * [Lauching app](#launching-app)
        * [Into MS-Windows&trade;](#into-ms-windows)
        * [Into UNIX/Linux](#into-unixlinux)
    * [How does it work?](#how-does-it-work)
    * [Going further](#going-further)
* [Quick nav](#quick-nav)


## <a name="download"/>Downloading the application

### <a name="official-release-versions"/>Official release versions

It is **highly recommended** for users to download *ONLY* official
release versions of `tkScenarist` software application.

Official release versions stay at GitHub's [Releases](https://github.com/tarball69/tkScenarist/releases) web page and are
sorted from **most recent** to **oldest**.

Click on `zip` link (MS-Windows&trade; users, recommended) or `tar.gz`
link (UNIX/Linux users, optional) to download a compressed archive of
the release, then unzip the archive with your favourite tool.

Copy the unzipped folder you obtained into a safe directory e.g. let's
say into some private `apps` folder.

Your software is now ready for trying out!

Return to [summary](#summary).

### <a name="daily-build"/>Daily build

Some explorers may wish to go further and get the latest unofficial
release versions with the most experimental features of `tkScenarist`.

To do this, simply click on the **Download ZIP** button you may find on
the [right-hand side](https://github.com/tarball69/tkScenarist) of
GitHub project's main page.

**CAUTION**: unofficial `daily build` versions are *NOT* guaranteed to
work in any manner.

**You play with these at your own risks**.

Return to [summary](#summary).

### <a name="forks-and-pull-requests"/>Forks and pull requests

People willing to improve files from the project are suggested to study
GitHub's official documentation about **[forks](https://help.github.com/articles/fork-a-repo)** and **[pull requests](https://help.github.com/articles/using-pull-requests/)**.

Thank you for trying to help us.

Return to [summary](#summary).


## <a name="install"/>Installing tkScenarist

### <a name="general-purpose"/>General purpose

This program does *NOT* need to be installed in any way.

Simply [download](#download) it, unzip it (into an `apps` private
directory, for example) and use it right now.

Return to [summary](#summary).

### <a name="pre-requisites"/>Pre-requisites

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

<https://www.python.org/downloads/> (Ctrl+click: open in new tab)

Return to [summary](#summary).

### <a name="unixlinux"/>UNIX/Linux

Many major Linux distributions (e.g. Ubuntu, SuSE, etc) do already have
a **pre-installed** Python3/Tkinter package.

In this particular case, **you should *NOT* consider** to make any
special installation by yourself.

Simply [download](#download) and use this program as is.

Return to [summary](#summary).

### <a name="ms-windows"/>MS-Windows&trade;

Many MS-Windows&trade; users wonder why do they have a shell console
window coming up with the application on startup.

This is a quite normal Python default behaviour.

If you wish to use a Python application **without** its dedicated shell
console window, simply rename file extension from `.py` to `.pyw` and
then launch it again.

For the present case, this means you should rename `tkscenarist.py` to
`tkscenarist.pyw` and then run it once again.

Return to [summary](#summary).

### <a name="bug-report"/>Bug report

Anyway and whatever happens, please report troubleshootings by posting
a short message on GitHub's **[bugtracker](https://github.com/tarball69/tkScenarist/issues)**.

Thank you to help us improving `tkScenarist` for the benefit of all.

Return to [summary](#summary).


## <a name="getting_started"/>First steps

### <a name="launching-app"/>Launching app

#### <a name="into-ms-windows"/>Into MS-Windows&trade;

Simply double-click on `tkscenarist.py` file to launch app.

**Notice** : if you chose to [get rid of console app](#ms-windows),
you should double-click on `tkscenarist.pyw` file instead of the
genuine `tkscenarist.py` file.

Return to [summary](#summary).

#### <a name="into-unixlinux"/>Into UNIX/Linux

Click on `tkscenarist.py` file if it has the 'executable' sticky bit on
or open a shell console and launch file:

<pre class="codeblock">
    $ cd go/to/the/right/place # e.g. tkScenarist folder
    $ python3 tkscenarist.py
</pre>

Return to [summary](#summary).

##### <a name="the-executable-sticky-bit"/>The 'executable' sticky bit

To set the 'executable' sticky bit on, simply do a:

<pre class="codeblock">
    $ cd go/to/the/right/place # e.g. tkScenarist folder
    $ chmod +x tkscenarist.py
</pre>

Since then, it will be possible to simply (double) click on
`tkscenarist.py` file into your favourite file manager and to launch
`tkScenarist` app visually.

Return to [summary](#summary).

### <a name="how-does-it-work"/>How does it work?

`tkScenarist` application software works with tabs allowing writers to
get all essentials in a single hand.

Tabs are ordered along with some natural and/or intuitive way:

1. finding a project's title;
1. adding some subtitle and episode number/title (optional);
1. writing personal notes on a draft, to help shaping the story;
1. writing the strongest steps of the story into a pitch/concept text
zone;
1. managing movie characters, with their own history logs and
relationships;
1. finally, writing the scenario itself;
1. storyboard is an extra tool for small projects aiming to keep all in
one hand;
1. same thing for resources.

On top of this, one may find useful tools, such as:

* a **name database**, where you can search amongst thousands of names
coming from all origins over the planet;
* **story/pitch templates** manager: pick up templates from other
people or write your own (you could share with the world);
* a **scenario elements editor** (SEE) made for finer scenario script
tuning and fancier look'n'feel.

Please, note playing with the SEE look'n'feel features would *NOT*
impact PDF exportations in any way, as printable PDF documents follow
strict policies for their look'n'feel, in order to match professional
submission.

Return to [summary](#summary).

### <a name="going-further"/>Going further

People willing to learn much more about `tkScenarist` software
application are suggested to dive into the whole online documentation
available on **[GitHub's wiki pages](https://github.com/tarball69/tkScenarist/wiki/)**.

Return to [summary](#summary).

---

#### <a name="quick-nav"/>Quick nav

* **App by tabs**
    * ['Title/Data' tab](en_tab_title_data.html)
    * ['Draft/Notes' tab](en_tab_draft_notes.html)
    * ['Pitch/Concept' tab](en_tab_pitch_concept.html)
    * ['Characters' tab](en_tab_characters.html)
    * ['Scenario' tab](en_tab_scenario.html)
    * ['Storyboard' tab](en_tab_storyboard.html)
    * ['Resources' tab](en_tab_resources.html)
* **Extra tools**
    * [Name database](en_tools_name_db.html)
    * [Story/pitch templates](en_tools_pitch_templates.html)
    * [Scenario Elements Editor (SEE)](en_tools_scenario_elements_editor.html)

Return to [homepage](index.html).
