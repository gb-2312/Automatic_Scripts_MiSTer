#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Angel
# Bio:	http://www.0ee.com/about
# Date: Tue Oct  1 23:05:42 CST 2019
# Common-Toolkit

import imp, os, platform, shutil, stat, subprocess, sys

NEXT_LINE_STR = '\n'

IS_WINDOWS = platform.system().lower() == 'windows'
IS_LINUX = platform.system().lower() == 'linux'
IS_MACOSX = platform.system().lower() == 'darwin'


'''
	print: with 2line
'''
def print2ln(msg):
	print(msg + NEXT_LINE_STR)

'''
	print fill tips
'''
def print_fill_tips(content = None):
	if not content:
		return

	unit_list = content.split(NEXT_LINE_STR)

	if not unit_list:
		return

	head_line_len = None
	head_line_sign = None

	for unit in unit_list:
		if not head_line_len:
			head_line_len = len(unit)
			head_line_sign = unit[:1]

		print(unit[:head_line_len - 1] + head_line_sign if len(unit) > head_line_len else unit)

'''
	http-get
'''
def get_http_request(request_url = None, headers = None):
	if not request_url or not headers:
		raise Exception('request_url is Nil! or headers is Nil!')

	print2ln('request_url: %s' % request_url)

	import requests
	return requests.get(request_url, headers = headers)

'''
	urllib: http-get
'''
def get_urllib_request(request_url = None, headers = None):
	if not request_url or not headers:
		raise Exception('request_url is Nil! or headers is Nil!')

	print2ln('request_url: %s' % request_url)

	if sys.version_info.major == 2:
		import urllib2
	elif sys.version_info.major == 3:
		import urllib.request as urllib2

	request = urllib2.Request(request_url)

	for k, v in headers.items():
		request.add_header(k, v)

	response = None
	response_content = None

	try:
		response = urllib2.urlopen(request)
		if not response:
			raise Exception('response is Nil!')

		response_content = response.read()
		if not response_content:
			raise Exception('response_content is Nil!')

	except Exception as e:
		raise Exception(e)
	finally:
		if response:
			response.close()

	return response_content

'''
	check /dev/*** exists?
'''
def disk_exists(path):
	try:
		return stat.S_ISBLK(os.stat(path).st_mode)
	except Exception as e:
		return False

'''
	copy-tree
'''
def copytree(src, dst, symlinks = False, ignore = None):
	import shutil

	for item in os.listdir(src):
		s = os.path.join(src, item)
		d = os.path.join(dst, item)
		if os.path.isdir(s):
			shutil.copytree(s, d, symlinks, ignore)
		else:
			shutil.copy2(s, d)

'''
	exec: shell-command
'''
def exec_shell(statement = None):
	if not statement:
		raise Exception('statement is Nil!')

	p = subprocess.Popen(statement, shell = True, stdout = subprocess.PIPE)
	if not p:
		return

	out = p.stdout.readlines()
	for line in out:
		print(line)

'''
	unrar-file
'''
def unrar_file(path = None, file_name = None, unrar_path = None):
	if not path or not file_name or not unrar_path:
		raise Exception('path is Nil! or file_name is Nil! or unrar_path is Nil!')

	import rarfile
	rar_file = rarfile.RarFile(os.path.join(path, file_name))
	rar_file.extractall(unrar_path)

'''
	install all dependency-libs
'''
def install_dependencies(dependencies = None):
	if not dependencies:
		return

	for install_lib in dependencies:
		count = 2

		while count:
			try:
				imp.find_module(install_lib)
				print2ln('You\'ve already install pip module: %s' % (install_lib))
				break
			except Exception as e:
				print2ln('Detected that `%s` module is not installed, start installing now' % (install_lib))

				install_lib_cmd = 'install %s' % (install_lib)

				if sys.version_info.major == 3:
					install_lib_cmd = 'pip3 ' + install_lib_cmd
				elif sys.version_info.major == 2:
					install_lib_cmd = 'pip ' + install_lib_cmd
				else:
					raise Exception('this: sys.version_info.major == %d not be supported! ' % (sys.version_info.major))

				if IS_MACOSX or IS_LINUX:
					install_lib_cmd = 'sudo ' + install_lib_cmd

				print2ln(install_lib_cmd)
				exec_shell(install_lib_cmd)
				count -= 1
				continue

'''
	confirm: keypad input
'''
def confirm_keypad(func_name = None, object_name = None):
	if not func_name or not object_name:
		raise Exception('func_name is Nil! or object_name is Nil!')

	# must be input the correct `char`
	while True:
		terminal_input = ''
		warn_msg = 'Warn: This will %s %s, are you sure you want to continue ? [y/n] ' % (func_name, object_name)

		if sys.version_info.major == 3:
			terminal_input = input(warn_msg)
		elif sys.version_info.major == 2:
			terminal_input = raw_input(warn_msg)

		input_result = terminal_input.lower()
		if not input_result:
			continue

		# NO, then quit
		if input_result == 'n':
			print2ln('You\'ve quit! Welcome to use next time!')
			sys.exit(-1)
		# YES, then break this loop and exec next logic!
		elif input_result == 'y':
			break
