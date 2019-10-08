#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Angel
# Bio:	http://www.0ee.com/about
# Date: Sun Sep 22 11:21:55 CST 2019
# Platform, for: Mac OSX And Linux

from MiSTerCore import *

RAR_SUFFIX = '.rar'

RENAME_MATCH_FILE_DICT = {
	'menu_': 'menu.rbf',
	'MiSTer_': 'MiSTer',
}

MISTER_VOLUME_NAME = 'MiSTer_Data'
UBOOT_VOLUME_NAME = 'UBOOT'


'''
	platform
'''
class Platform(object):
	"""docstring for Platform"""
	def __init__(self, device_name = None, unzipped_dir = None):
		super(Platform, self).__init__()
		self.check_dev_keywords = None
		self.default_device_name = None
		self.device_name = device_name
		self.mister_install_dir = None
		self.clean_objects = None
		self.MISTER_PART = None
		self.UBOOT_PART = None

	'''
		not-implements
	'''
	def _not_impl_(self):
		raise Exception('this method not impl!')

	'''
		execute
	'''
	def execute(self, current_mister_files = None):
		self._not_impl_()

	'''
		Create an OS-instance
	'''
	@staticmethod
	def gen_os_instance(device_name = None, unzipped_dir = None):
		if IS_MACOSX:
			cmd_os = MacOSX(device_name, unzipped_dir)
		elif IS_LINUX:
			cmd_os = Linux(device_name, unzipped_dir)

		if not cmd_os:
			raise Exception('cmd_os is Nil!')

		return cmd_os

	'''
		After getting the installation: the copied file name
	'''
	@staticmethod
	def get_install_cp_file_name(origin_name = None):
		if not origin_name:
			raise Exception('origin_name is Nil!')

		# return new mapping-file-name
		for k, v in RENAME_MATCH_FILE_DICT.items():
			if k in origin_name:
				return v

		raise Exception('origin_name %s not exists!' % (origin_name))

	'''
		install-tips
	'''
	def gen_install_tips(self):
		self_name = type(self).__name__
		print_fill_tips('''\
####################################################################################
#                                                                                  #
# MiSTer install script for %s by %s, %s                                           
#                                                                                  #
# IMPORTANT: Use this script at your own risk!!                                    #
# It WILL WIPE ALL DATA on the device you specify!!                                #
# On standard %s this is usually %s but make sure to double check!                 
#                                                                                  #
# Prerequisites:                                                                   #
# * python.version >= 2.7                                                          #
# * pip ~ pip3                                                                     #
#                                                                                  #
####################################################################################
	''' % (self_name, Author.name, Author.bio, self_name, self.default_device_name))

	'''
		partition-disk
	'''
	def partition_disk(self):
		self._not_impl_()

	'''
		umount
	'''
	def umount(self):
		self._not_impl_()

	'''
		write-uboot
	'''
	def write_uboot(self):
		self._not_impl_()

	'''
		(dd-command)writing-uboot
	'''
	def writing_uboot(self, uboot_volume_name = None):
		if not self.unzipped_dir or not uboot_volume_name or not self.UBOOT_PART:
			raise Exception('self.unzipped_dir is Nil! uboot_volume_name is Nil! or self.UBOOT_PART is Nil!')

		print2ln('Writing uboot image to the %s partition (sudo may ask for your password)...' % (uboot_volume_name))
		exec_shell('sudo dd if=%s/files/linux/uboot.img of=%s bs=64k' % (self.unzipped_dir, self.UBOOT_PART))

	'''
		mount
	'''
	def mount(self):
		self._not_impl_()

	'''
		copy: mister-files
	'''
	def copy_mister_files(self, current_mister_files = None):
		if not current_mister_files:
			raise Exception('current_mister_files is Nil!')

		print2ln('Copying MiSTer files...')

		# if `volume` not exists, then raise Exception!
		if not os.path.exists(self.mister_install_dir):
			raise Exception('Error: %s is not mounted, something probably went wrong during the parititioning step.' % (self.mister_install_dir))

		# deep-copy folder from `unrar_folders` to `install_dir`
		copytree(self.unzipped_dir + '/files/', self.mister_install_dir)

		import shutil

		# copy left MiSTer files!
		for current_mister in current_mister_files:
			if RAR_SUFFIX in current_mister:
				continue

			print2ln('Copying file `%s` to dir: `%s`' % (current_mister, self.mister_install_dir))
			shutil.copy(current_mister, self.mister_install_dir + '/%s' % (Platform.get_install_cp_file_name(current_mister)))

		# copy shell-file
		try_copy_update_dot_sh_file(self.mister_install_dir)

	'''
		clean
	'''
	def clean(self):
		self._not_impl_()

	'''
		eject
	'''
	def eject(self):
		self._not_impl_()

	'''
		eof
	'''
	def eof(self):
		print2ln('''All done. Put the SD card into your MiSTer and start it up.
Connect a keyboard to the MiSTer and hit F12 to bring up the menu.')
Refer to the MiSTer wiki for further information.''')


'''
	system of: linux
'''
class Linux(Platform):
	"""docstring for Linux"""
	def __init__(self, device_name = None, unzipped_dir = None):
		super(Linux, self).__init__()
		self.check_dev_keywords = '/dev/sd'
		self.default_device_name = self.check_dev_keywords + 'b'
		self.device_name = device_name
		self.unzipped_dir = unzipped_dir
		self.mister_install_dir = './mnt/%s/' % (MISTER_VOLUME_NAME)
		self.clean_objects = (
			self.unzipped_dir,
			self.mister_install_dir,
			'./mnt',
		)
		self.MISTER_PART = self.device_name + str(1)
		self.UBOOT_PART = self.device_name + str(2)

	def partition_disk(self):
		# Note : Uboot and FSBL code is loaded from partition with a2 ID (can be any of the 4 partitions in the MBR) see :
		# https://www.intel.com/content/dam/www/programmable/us/en/pdfs/literature/hb/cyclone-v/cv_5v4.pdf
		# Page 3481 (Section A-13) "Flash Memory Devices for Booting"
		# However Uboot (the Uboot that comes with MiSTer) will try to boot linux from partition 1
		# Here we create a partition 1 that takes all the remaining space of the SD card from sector 4096+
		# and partition 2 which spans from sector 2048 to 4095 (for Uboot and the FSBL code)
		print2ln('Creating SD Card partition table')

		# delete all-partitions
		exec_shell('''fdisk %s << EOF
d
1
d
w
EOF
''' % (self.device_name))

		# sync
		exec_shell('sync')

		# create two-partitions: 
		#	sdX1: `MiSTer_Data`
		#	sdX2: `UBOOT`
		exec_shell('''fdisk %s << EOF
n
p
2
2048
+3M
n
p
1
8192

t
1
7
t
2
a2
w
EOF
''' % (self.device_name))

		# sync
		exec_shell('sync')

		self.write_uboot()

		print2ln('Creating the %s partition' % (MISTER_VOLUME_NAME))

		exec_shell('sudo mkfs.exfat -n "%s" %s' % (MISTER_VOLUME_NAME, self.MISTER_PART))

		exec_shell('sudo mkfs.exfat -n "%s" %s' % (UBOOT_VOLUME_NAME, self.UBOOT_PART))

		print2ln('Syncing')

		# sync
		exec_shell('sync')

	def umount(self):
		device_name_matches = self.device_name + '*'

		print2ln('Unmounting %s potentially mounted partitions (sudo may ask for your password)' % (device_name_matches))

		exec_shell('sudo umount %s' % (device_name_matches))

	def write_uboot(self):
		self.writing_uboot(UBOOT_VOLUME_NAME)

	def mount(self):
		print2ln('Mounting the disk')

		# create mounted folder!
		if not os.path.exists(self.mister_install_dir):
			print2ln('Create mounted folders: %s' % (self.mister_install_dir))
			os.makedirs(self.mister_install_dir, 0o755)

		exec_shell('sudo mount -t exfat %s %s' % (self.MISTER_PART, self.mister_install_dir))

	def clean(self):
		import shutil

		# removing relevant spotlight-folders
		for clean_object in self.clean_objects:
			try:
				shutil.rmtree(clean_object)
				print2ln('Remove: %s successfully!' % (clean_object))
			except Exception as e:
				pass

	def execute(self, current_mister_files = None):
		self.umount()
		self.partition_disk()
		self.mount()
		self.copy_mister_files(current_mister_files)
		self.umount()
		self.clean()


'''
	system of: mac osx
'''
class MacOSX(Platform):
	"""docstring for MacOSX"""
	def __init__(self, device_name = None, unzipped_dir = None):
		super(MacOSX, self).__init__()
		self.check_dev_keywords = '/dev/disk'
		self.default_device_name = self.check_dev_keywords + str(2)
		self.device_name = device_name
		self.unzipped_dir = unzipped_dir
		self.mister_install_dir = '/Volumes/%s' % (MISTER_VOLUME_NAME)
		self.clean_objects = (
			self.unzipped_dir,
			'.Spotlight-V100',
			'.fseventsd',
		)
		self.UBOOT_PART = self.device_name + 's2'

	def partition_disk(self):
		print2ln('Partitioning SD card...')

		# using: diskutil format usb device
		exec_shell('diskutil partitionDisk %s MBR ExFAT %s R ExFAT %s 3M' % (self.device_name, MISTER_VOLUME_NAME, UBOOT_VOLUME_NAME))

	def umount(self):
		print2ln('Unmounting SD card...')

		# unmount-disk: /dev/xxx
		exec_shell('diskutil unmountDisk %s' % (self.device_name))

	def write_uboot(self):
		print2ln('Fixing the SD card partition table to support %s (sudo may ask for your password)..' % (UBOOT_VOLUME_NAME))
		print2ln('You may see a message \'could not open MBR file\' which is safe to ignore.')

		# fixing
		exec_shell("sudo fdisk -d %s | sed 'n;s/0x07/0xA2/g' | sudo fdisk -ry %s" % (self.device_name, self.device_name))

		self.writing_uboot(UBOOT_VOLUME_NAME)

	def clean(self):
		print2ln('Disabling Spotlight indexing and removing relevant Spotlight folders...')

		# disable spotlight-indexing
		exec_shell('mdutil -d %s' % (self.mister_install_dir))

		# removing relevant spotlight-folders
		for clean_object in self.clean_objects:
			try:
				shutil.rmtree(clean_object)
				print2ln('Remove: %s successfully!' % (clean_object))
			except Exception as e:
				pass

	def eject(self):
		print2ln('Ejecting SD card (this can take a few seconds)...')

		# eject device
		exec_shell('diskutil eject %s' % (self.device_name))

	def execute(self, current_mister_files = None):
		self.partition_disk()
		self.copy_mister_files(current_mister_files)
		self.umount()
		self.write_uboot()
		self.clean()
		self.eject()
