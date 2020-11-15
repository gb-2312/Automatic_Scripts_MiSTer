# Automatic-Scripts: MiSTer SD card installer and rbf updater

This script automates the creation of a MiSTer SD card on MacOSX or Linux, inspire from: 
[SD-Installer-macos_MiSTer](https://github.com/michaelshmitty/SD-Installer-macos_MiSTer).   
And this script support upgrade `.rbf` files to the latest version from repository-list!  
It covers up until the
[step "Get a core"](https://github.com/MiSTer-devel/Main_MiSTer/wiki/Setup-Guide#get-a-core)
in the MiSTer Wiki Setup Guide.  

Tested on MacOSX High Sierra 10.13.6, CentOS 7 and Debian GNU 8.

Running this script on an empty SD card will install the following:
* Linux OS img for the HPS.
* A recent MiSTer binary.
* A recent MiSTer menu core.
* [Locutus73's MiSTer update script](https://github.com/MiSTer-devel/Updater_script_MiSTer)

Once your SD card is ready you can put it into your MiSTer board, configure a controller and run
[the MiSTer update script](https://github.com/MiSTer-devel/Updater_script_MiSTer).  
This will install the latest versions of the MiSTer binary, the menu and the MiSTer cores.  
Make sure your MiSTer board is connected to the Internet using ethernet.

## Prerequisites
* [python 2.7 or later](https://python.org)
* pip(if not install, then open a terminal and running: `python -m ensurepip` or `python Pip.py`)
* unrar(only used for `MiSTer SD card installer`):  
	(MacOSX: install using [homebrew](https://brew.sh), `brew install unrar`)  
	(CentOS: add 3rd-party repo, `yum install unrar`)  
	(Debian/Ubuntu: `apt-get install unrar`)  
	Or manually compile the software source code from [rarlib](https://www.rarlab.com)

## Usage
Open a terminal, clone this repository and change into the directory.

```bash
git clone https://github.com/gb-2312/Automatic_Scripts_MiSTer.git
cd Automatic_Scripts_MiSTer
```

## 1.About and resolve GitHub v3 request frequency
This script is written based on GitHub v3, but the GitHub v3 API 
has a limit on the frequency of requests from anonymous users!!  
Therefore, we recommend that users register and apply for GitHub-Token 
to increase the number of requests.  
You can create file: `oauth.txt`, and paste your GitHub-Token.  
Please visit and setting GitHub-Token: https://github.com/settings/tokens .  
(Be careful keep your Token safety and don't leak out!! This is very important!)  
(Token: Read-only permissions are sufficient!)  
Otherwise without GitHub-Token, you maybe wait for 1 hour and try again!  

## 2.Using SD card installer
Find out your SD card device. This is important because the script will wipe everything
on that device and selecting the wrong device could lead to data loss!!!

First, keep your SD card unplugged and list the currrently known disks:  

in MacOSX using:
```bash
diskutil list
```
in Linux using:
```bash
fdisk -l
```

Then insert your SD card and issue the command again. Your SD card should now show up in the list.  
Usually, in MacOSX it's `/dev/disk2`, in Linux it's `/dev/sdb` but not always, must be attention!!!  

in MacOSX using:
```bash
diskutil list
```
in Linux using:
```bash
fdisk -l
```

Now run the MiSTer SD card installer script with the correct disk, for example:  

in MacOSX it's `/dev/disk2`,  
in Linux it's `/dev/sdb`.  

Some commands require the sudo command so you may be prompted for your password.  

in MacOSX using:
```bash
python MiSTerSDInstaller.py /dev/disk2
```
in Linux using:
```bash
python MiSTerSDInstaller.py /dev/sdb
```

If everything went well you should now have a clean MiSTer SD card which you can put into your
MiSTer board and boot from.

Once booted you will be greeted by the MiSTer interface. Attach a keyboard and make sure your
MiSTer board is connected to the internet through the ethernet interface.
Hit F12 on the keyboard and navigate to Scripts. Then open the root directory, select the
update script `update.sh` and hit enter.  
[The MiSTer update script](https://github.com/MiSTer-devel/Updater_script_MiSTer) will now install
the latest versions of the MiSTer binary, the menu and the available MiSTer cores.

## 3.Using rbf updater
You can use the MiSTerUpdater script to upgrade your local MiSTer file to the latest version.  

in MacOSX, Linux or Windows:
```bash
python MiSTerUpdater.py
```
If you want to upgrade or add new MiSTer file(s) of github-repository-project-name, you can edit:  

`updater_repository_list.txt`  

If all upgrade done. Please copy all successfully downloaded files of the current directory to the root directory of the SD card.  
Ensuring that the same type of `.rbf` file retains only the latest one.

## Problems, issues
If you run into any problems,
[open an issue](../../issues), thanks!
