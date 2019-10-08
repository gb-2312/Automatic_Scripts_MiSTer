#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Angel
# Bio:	http://www.0ee.com/about
# Date: Tue Oct  1 23:30:37 CST 2019
# Pip-Module

from Common import *

# pip-host: HTTP-Request-Headers
PIP_DOWNLOAD_HEADERS = {
	'Host': 'bootstrap.pypa.io',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
}


'''
	request: pip-file(get-pip.py)
'''
def request_pip():
	request_url = 'https://bootstrap.pypa.io/get-pip.py'
	return (request_url, get_urllib_request(request_url, PIP_DOWNLOAD_HEADERS))

'''
	request and saving: pip-file(get-pip.py)
'''
def download_pip():
	request_url, pip_response = request_pip()

	if not pip_response:
		raise Exception('pip_response is Nil!')

	save_path = request_url[request_url.rfind('/') + 1:]

	if not save_path:
		raise Exception('save_path is Nil!')

	with open(save_path, 'w') as pip_file:
		pip_file.write(pip_response)

	return save_path

'''
	check or install: pip
'''
def check_pip():
	if check_local_pip():
		print2ln('You\'ve already install pip!')
		return

	# confirm: install-pip
	confirm_install_pip()

	# get pip file-name
	pip_file_name = download_pip()

	# install pip cmd
	install_pip_cmd = '%s %s' % (sys.executable, pip_file_name)

	if IS_MACOSX or IS_LINUX:
		install_pip_cmd = 'sudo ' + install_pip_cmd

	# install pip
	exec_shell(install_pip_cmd)

'''
	check local is install pip?
'''
def check_local_pip():
	check_pip_cmd = 'pip --version'

	if sys.version_info.major == 3:
		check_pip_cmd = 'pip3 --version'

	p = subprocess.Popen(check_pip_cmd, shell = True, stdout = subprocess.PIPE)
	out = p.stdout.readlines()

	if not out:
		return False

	return True

'''
	confirm install pip
'''
def confirm_install_pip(pip_name = None):
	confirm_keypad('install', pip_name)


# main-method
if __name__ == '__main__':
	check_pip()
