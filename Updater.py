#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Angel
# Bio:	http://www.0ee.com/about
# Date: Sun Sep 22 11:21:55 CST 2019
# Updater, for: Windows, Mac OSX And Linux

from MiSTerCore import *
from OAuth import *


'''
	updater
'''
class Updater(object):
	"""docstring for Updater"""
	def __init__(self, downloading_match_file_keywords = None, update_mister_tuple = None):
		super(Updater, self).__init__()
		self.downloading_match_file_keywords = downloading_match_file_keywords
		self.update_mister_tuple = update_mister_tuple
		self.oauth = OAuth()
		self.oauth.load()
		print2ln('Prepare download files...')

	'''
		read and set: updater config-file(if not exists or empty, then upgrade from default-repository-list)
	'''
	def set_updater_repository_list(self):
		repository_list = read_updater_repository_list()

		# deal as default:
		if not repository_list:
			return

		gen_repository_list = []

		for repository in repository_list:
			current_repository = repository.strip(' ')
			if not current_repository:
				continue

			gen_repository_list.append(current_repository)

		if not gen_repository_list:
			return

		self.update_mister_tuple = gen_repository_list

	'''
		install-tips
	'''
	def gen_install_tips(self):
		self_name = type(self).__name__
		print_fill_tips('''\
####################################################################################
#                                                                                  #
# MiSTer %s script by %s, %s                                                       
#                                                                                  #
# IMPORTANT: Use this script is limited by the request frequency of GitHub API v3. #
# If the prompt is frequent, please wait for 1 hour and try again!                 #
# Or you can create file: `%s`, and paste your GitHub-Token.                       #
# Please visit and setting GitHub-Token: %s .                                      
# (Be careful keep your Token safety and do not leak out! This is very important!) #
# (Token: Read-only permissions are sufficient!)                                   #
#                                                                                  #
# Prerequisites:                                                                   #
# * python.version >= 2.7                                                          #
# * pip ~ pip3                                                                     #
#                                                                                  #
####################################################################################
	''' % (self_name, Author.name, Author.bio, OAuth.OAUTH_FILENAME, OAuth.APPLY_GITHUB_TOKEN_URL))

		update_mister_ln = ''.join(('%s[' % (NEXT_LINE_STR)) + str(unit) + ']' for unit in self.update_mister_tuple)
		print2ln('Prepare to upgrade repository files!%s %s' % (NEXT_LINE_STR, update_mister_ln))

	'''
		setup and upgrade: download!
	'''
	def setup_and_upgrade_download(self, upgrade_tips = False):
		# upgrade-tips
		if upgrade_tips:
			self.gen_install_tips()

		# set match-tuple
		set_global_downloading_match_file_keywords(self.downloading_match_file_keywords)

		# oauth-headers, allow nil
		oauth_headers = self.oauth.gen_oauth_headers()

		# upgrade and download, delete oldest files!
		upgrade_download(self.update_mister_tuple, oauth_headers)

		# upgrade-tips
		if upgrade_tips:
			self.eof()

	'''
		eof
	'''
	def eof(self):
		print2ln('''All done. Please copy all successfully downloaded files of the current directory to the root directory of the SD card.
Ensuring that the same type of `.rbf` file retains only the latest one.''')
