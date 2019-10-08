#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Angel
# Bio:	http://www.0ee.com/about
# Date: Sun Sep 22 11:21:55 CST 2019
# Usage: 
#	python MiSTerUpdater.py
# MiSTer-Updater, for: Windows, Mac OSX And Linux

from MiSTerCore import *
from Updater import *

# all update mister files
UPDATE_MISTER_TUPLE = (
	'Main_MiSTer',
	'Menu_MiSTer',
	'Altair8800_Mister',
	'Atari2600_MiSTer',
	'Atari800_MiSTer',
	'ColecoVision_MiSTer',
	'Gameboy_MiSTer',
	'Genesis_MiSTer',
	'MSX_MiSTer',
	'NeoGeo_MiSTer',
	'NES_MiSTer',
	'SMS_MiSTer',
	'SNES_MiSTer',
	'TurboGrafx16_MiSTer',
)

# Matching: keywords of download-file
DOWNLOADING_MATCH_FILE_KEYWORDS = (
	'menu_',
	'MiSTer_',
	'.rbf',
)


# main-method
if __name__ == '__main__':
	# install: all dependency-libs
	install_all_dependencies()

	# create updater
	updater = Updater(DOWNLOADING_MATCH_FILE_KEYWORDS, UPDATE_MISTER_TUPLE)

	# setting updater repository-list from config-file
	updater.set_updater_repository_list()

	# setup and upgrade-download!
	updater.setup_and_upgrade_download(True)
