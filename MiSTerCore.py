#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Angel
# Bio:	http://www.0ee.com/about
# Date: Sun Sep 22 11:21:55 CST 2019
# MiSTer-Core, for: Mac OSX And Linux

import base64, json, os, shutil

from Common import *

# GitHub Organizations
GLOBAL_ORGANIZATIONS = 'MiSTer-devel'

# python-dependency-libs
ALL_DEPENDENCIES = (
	'rarfile',
	'requests',
	'shutil',
)

# API-HOST: HTTP-Request-Headers
API_HEADERS = {
	'Host': 'api.github.com',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
}

# RAW-HOST: HTTP-Request-Headers
RAW_HEADERS = {
	'Host': 'raw.githubusercontent.com',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
}

# update_script repo name
UPDATE_SH_GIT_REPO_NAME = 'Updater_script_MiSTer'
# update.sh
UPDATE_DOT_SHELL = 'update.sh'

# Matching: keywords of download-file
DOWNLOADING_MATCH_FILE_KEYWORDS = None

# Commit: keywords of `.rbf file`
COMMIT_RBF_FILE_KEYWORDS = (
	'release',
	'add rbf',
)

'''
	Author
'''
class Author(object):
	"""docstring for Author"""
	def __init__(self):
		super(Author).__init__()

	name = 'Angel'
	bio = 'http://www.0ee.com/about'
	module_name = 'MiSTer'

'''
	install all dependency-libs
'''
def install_all_dependencies():
	install_dependencies(ALL_DEPENDENCIES)

'''
	match download file(from given-tuple)
'''
def set_global_downloading_match_file_keywords(match_tuple = None):
	if not match_tuple:
		raise Exception('match_tuple is Nil!')

	global DOWNLOADING_MATCH_FILE_KEYWORDS
	DOWNLOADING_MATCH_FILE_KEYWORDS = match_tuple

'''
	get repo: commit-list
'''
def gen_github_commit_http_request(github_username = None, remote_git_repo_name = None, page = 1, per_page = 30):
	request_url = 'https://api.github.com/repos/%s/%s/commits?page=%d&per_page=%d' % (github_username, remote_git_repo_name, page, per_page)
	return get_http_request(request_url, API_HEADERS)

'''
	request: raw-content
'''
def gen_github_raw_http_request(github_username = None, remote_git_repo_name = None, path = None):
	request_url = 'https://raw.githubusercontent.com/%s/%s/master/%s' % (github_username, remote_git_repo_name, path)
	return get_http_request(request_url, RAW_HEADERS)

'''
	whether it matches the characteristics of the downloaded file
'''
def is_in_download_keywords(latest_release_path = None):
	if not latest_release_path:
		raise Exception('latest_release_path is Nil!')

	for keywords in DOWNLOADING_MATCH_FILE_KEYWORDS:
		if keywords in latest_release_path:
			return True

	return False

'''
	get: old mister files!
'''
def get_old_mister_files():
	old_mister_files = []

	folder = '.'

	for root_dir in os.listdir(folder):
		file_path = os.path.join(folder, root_dir)
		if is_in_download_keywords(file_path):
			old_mister_files.append(file_path)

	return old_mister_files

'''
	delete: old mister files!
'''
def del_old_mister_files(old_mister_files = None):
	if not old_mister_files:
		return

	for old_mister in old_mister_files:
		print2ln('old_mister_file: %s has been deleted successfully!' % old_mister)
		os.remove(old_mister)

'''
	remove: from old_mister
'''
def remove_mister_from_old_files(old_mister_files = None, new_mister_file = None):
	if not new_mister_file:
		raise Exception('new_mister_file is Nil!')

	if not old_mister_files:
		return False

	for old_mister in old_mister_files:
		if new_mister_file in old_mister:
			old_mister_files.remove(old_mister)
			return True

	return False

'''
	recursive: parse tree
'''
def parse_tree(tree_url = None):
	if not tree_url:
		raise Exception('tree_url is Nil!')

	tree_response = get_http_request(tree_url, API_HEADERS)

	if not tree_response or tree_response.status_code != 200:
		raise Exception('tree_response is Nil! or tree_response.status_code != 200')

	tree_json_parse_obj = json.loads(tree_response.text)

	if not tree_json_parse_obj:
		raise Exception('tree_json_parse_obj is Nil!')

	latest_release_path = None
	latest_release_url = None

	if not tree_json_parse_obj['tree']:
		return (None, None)

	# last roll-file!
	reversed_tree_json_parse_list = list(reversed(tree_json_parse_obj['tree']))

	for latest_release_obj in reversed_tree_json_parse_list:
		latest_release_path = latest_release_obj['path']
		latest_release_url = latest_release_obj['url']

		print2ln('latest_release_path: %s' % latest_release_path)

		# parse: not `folder!`, EG: release_20190627.rar, menu_20190914.rbf, MiSTer_20190913
		if is_in_download_keywords(latest_release_path):
			break
		# trying to match: parse folder -> file
		elif latest_release_path.find('releases') != -1:
			latest_release_path, latest_release_url = parse_tree(latest_release_url)
			break

	# current match failed!
	if latest_release_path.find('releases') != -1:
		return (None, None)

	# current matching!!!
	return (latest_release_path, latest_release_url)

'''
	parse: release-folder!
'''
def parse_release(tree_url = None, old_mister_files = None):
	latest_release_path, latest_release_url = parse_tree(tree_url)

	if not latest_release_path or not latest_release_url:
		raise Exception('latest_release_path is Nil! or latest_release_url is Nil!')

	if remove_mister_from_old_files(old_mister_files, latest_release_path):
		print2ln('latest_release_path: %s has already downloaded!' % latest_release_path)
		return True

	print2ln('%s: %s' % (latest_release_path, latest_release_url))

	blob_response = get_http_request(latest_release_url, API_HEADERS)

	if not blob_response or blob_response.status_code != 200:
		raise Exception('blob_response is Nil! or blob_response.status_code != 200')

	blob_json_parse_obj = json.loads(blob_response.text)

	if not blob_json_parse_obj:
		raise Exception('blob_json_parse_obj is Nil!')

	if not 'content' in blob_json_parse_obj:
		raise Exception('blob_json_parse_obj is missing key: content')

	print2ln('Downloading file: %s' % latest_release_path)

	# parse blob-data(base64)
	base64_decode = base64.b64decode(blob_json_parse_obj['content'])
	if not base64_decode:
		raise Exception('base64_decode is Nil!')

	# save file!
	with open(latest_release_path, 'wb') as release_file:
		release_file.write(base64_decode)

	return True

'''
	match: last commit, if success, then save from blob-data to (path)file
'''
def parse_last_commit(github_username = None, remote_git_repo_name = None, old_mister_files = None):
	if not github_username or not remote_git_repo_name:
		raise Exception('github_username or remote_git_repo_name is Nil!')

	commit_response = gen_github_commit_http_request(github_username, remote_git_repo_name)

	if not commit_response or commit_response.status_code != 200:
		raise Exception('commit_response is Nil! or commit_response.status_code != 200')

	commit_json_parse_list = json.loads(commit_response.text)

	if not commit_json_parse_list:
		raise Exception('commit_json_parse_list is Nil!')

	for commit_unit in commit_json_parse_list:
		if commit_unit['commit'] and [commit_rbf_keyword for commit_rbf_keyword in COMMIT_RBF_FILE_KEYWORDS if commit_rbf_keyword in commit_unit['commit']['message'].lower()] and commit_unit['commit']['tree']:
			# Always match the last submitted record
			tree_url = commit_unit['commit']['tree']['url']
			print2ln('tree_url: %s' % tree_url)

			if parse_release(tree_url, old_mister_files):
				break

'''
	direct raw-save!
'''
def direct_raw_save(github_username = None, remote_git_repo_name = None, path = None):
	if not github_username or not remote_git_repo_name or not path:
		raise Exception('github_username is Nil! or remote_git_repo_name is Nil! or path is Nil!')

	remote_response = gen_github_raw_http_request(github_username, remote_git_repo_name, path)

	if not remote_response or remote_response.status_code != 200:
		raise Exception('remote_response is Nil! or remote_response.status_code != 200')

	save_path = path[path.rfind('/') + 1:]

	with open(save_path, 'w') as release_file:
		release_file.write(remote_response.text)

'''
	clean-up: bad files
'''
def clean_up_bad_files():
	print2ln('Clean-up bad files OR empty files!')
	old_mister_files = get_old_mister_files()

	if not old_mister_files:
		return

	bad_mister_files = []

	for old_mister in old_mister_files:
		# file-size == 0(empty), need re-dl
		if not os.path.getsize(old_mister):
			bad_mister_files.append(old_mister)

	if not bad_mister_files:
		return

	del_old_mister_files(bad_mister_files)

'''
	upgrade-download
'''
def upgrade_download(update_mister_tuple = None, oauth_headers = None):
	# oauth_headers: not nil!
	if oauth_headers:
		API_HEADERS.update(oauth_headers)

	# clean-up bad files
	clean_up_bad_files()

	# load and prepare for delete stale version: old-mister-file-list
	old_mister_files = get_old_mister_files()

	# possible upgrade: new-mister-file-list
	for update_unit in update_mister_tuple:
		parse_last_commit(GLOBAL_ORGANIZATIONS, update_unit, old_mister_files)

	# saving update-mister-script
	direct_raw_save(GLOBAL_ORGANIZATIONS, UPDATE_SH_GIT_REPO_NAME, UPDATE_DOT_SHELL)

	# at last, delete oldest mister files!
	del_old_mister_files(old_mister_files)

'''
	try: copy update.sh into dest_folder
'''
def try_copy_update_dot_sh_file(dest_folder = None):
	if not dest_folder:
		raise Exception('dest_folder is Nil!')

	# file not exists, ignore!
	if not os.path.isfile(UPDATE_DOT_SHELL):
		return

	shutil.copy(UPDATE_DOT_SHELL, dest_folder)

'''
	read updater repository_list from updater_repository_list.txt
'''
def read_updater_repository_list():
	repository_list_result = None

	try:
		with open('updater_repository_list.txt', 'r') as updater_repository_list_file:
			repository_list_result = updater_repository_list_file.read()
	except Exception as e:
		print2ln('updater_repository_list not exists, read default repository_list')
		pass

	if not repository_list_result:
		return None

	return repository_list_result.split(NEXT_LINE_STR)
