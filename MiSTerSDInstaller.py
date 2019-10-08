#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Angel
# Bio:	http://www.0ee.com/about
# Date: Sun Sep 22 11:21:55 CST 2019
# Usage: 
#	python MiSTerSDInstaller.py [device_path]
# SD-Installer-MiSTer, for: Mac OSX And Linux

import os, sys

from MiSTerCore import *
from Platform import *
from Updater import *

# all update mister files
UPDATE_MISTER_TUPLE = (
	'Main_MiSTer',
	'Menu_MiSTer',
	'SD-Installer-Win64_MiSTer',
)

RAR_SUFFIX = '.rar'
RAR_PREFIX = 'release_'
UNZIPPED_DIR = './unrar_folders/'

# Matching: keywords of download-file
DOWNLOADING_MATCH_FILE_KEYWORDS = (
	'menu_',
	'MiSTer_',
	RAR_SUFFIX,
)


'''
	confirm-input
'''
def confirm_input(device_name = None):
	confirm_keypad('erase', device_name)

'''
	try: make-unzipped dir
'''
def try_mk_unzipped_dir():
	# create a temporary directory
	if not os.path.exists(UNZIPPED_DIR):
		print2ln('Create unrar_folders: %s' % (UNZIPPED_DIR))
		os.mkdir(UNZIPPED_DIR, 0o755)

'''
	unrar
'''
def try_unrar_file(release_rar_file_name = None):
	print2ln('Extracting %s installation files...' % (release_rar_file_name))

	# unrar-file!
	unrar_file(".", release_rar_file_name, UNZIPPED_DIR)

'''
	find release-core-file, and prepare unrar
'''
def get_release_rar_file_name(current_mister_files = None):
	# find .rar file!
	release_result_list = [k for k in current_mister_files if k.endswith(RAR_SUFFIX) and RAR_PREFIX in k]

	# throws an exception if it does not match!
	if not release_result_list:
		raise Exception('Please check your network and confirm that the release package `%s2YYYMMdd%s` has been downloaded successfully!'\
		 % (RAR_PREFIX, RAR_SUFFIX))

	return release_result_list[0]

'''
	check: current mister files
'''
def check_current_mister_files():
	current_mister_files = get_old_mister_files()

	if not current_mister_files:
		raise Exception('current_mister_files is Nil!')

	return current_mister_files

'''
	check: device-name
'''
def check_device_name():
	cmd_list = sys.argv

	# argument-number: mismatch
	if len(cmd_list) <= 1:
		raise Exception('Please read README.md and specify an SD card device! eg: /dev/***')

	# get device-name
	device_name = cmd_list[1]

	# if this given device-name not exists, then raise Exception for tips!
	if not device_name or not disk_exists(device_name):
		raise Exception('Error: The device %s does not exist! Please check if the SD card is plugged in!' % (device_name))

	return device_name


# main-method
if __name__ == '__main__':
	# install: all dependency-libs
	install_all_dependencies()

	# get device-name
	device_name = check_device_name()

	# new-os-instance
	cmd_os = Platform.gen_os_instance(device_name, UNZIPPED_DIR)

	# print tips
	cmd_os.gen_install_tips()

	# 2nd: confirm-input
	confirm_input(device_name)

	# create updater
	updater = Updater(DOWNLOADING_MATCH_FILE_KEYWORDS, UPDATE_MISTER_TUPLE)

	# setup and upgrade-download!
	updater.setup_and_upgrade_download()

	# query again! must be non-nil
	current_mister_files = check_current_mister_files()

	# create a temporary directory
	try_mk_unzipped_dir()

	# find release-core-file, and prepare unrar
	release_rar_file_name = get_release_rar_file_name(current_mister_files)

	# unrar-file!
	try_unrar_file(release_rar_file_name)

	# exccute all method!
	cmd_os.execute(current_mister_files)

	# print EOF
	cmd_os.eof()
