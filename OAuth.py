#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Angel
# Bio:	http://www.0ee.com/about
# Date: Thu Oct  3 21:28:54 CST 2019
# OAuth Manager(GitHub-Token)

from Common import *


'''
	class of: OAuth
'''
class OAuth(object):
	# for: github-oauth
	OAUTH_FILENAME = 'oauth.txt'
	# apply for GitHub-Token
	APPLY_GITHUB_TOKEN_URL = 'https://github.com/settings/tokens'

	"""docstring for OAuth"""
	def __init__(self):
		super(OAuth, self).__init__()
		self.token = None
		print2ln('Create OAuth!')

	'''
		load: content of `oauth-file`
	'''
	def load(self):
		print2ln('Load OAuth...')
		oauth_line = None

		try:
			with open(self.OAUTH_FILENAME, 'r') as oauth_file:
				oauth_line = oauth_file.read()
		except Exception as e:
			print2ln('oauth_file `%s` not exists, ignore OAuth!' % (self.OAUTH_FILENAME))
			pass

		if not oauth_line:
			print2ln('oauth_file is Nil, ignore!')
			return

		self.token = oauth_line.split(NEXT_LINE_STR)[0].strip()

		if len(self.token) != 40:
			raise Exception('token error: please check you token `%s`  is correct!' % (self.token))

		print2ln('Load oauth_file OK! token is: %s' % (self.get_token_with_hidden_str()))

	'''
		get: token with `hidden string: *`
	'''
	def get_token_with_hidden_str(self):
		token_len = len(self.token)
		# hidden-token by `*`
		sub_token_len = int(token_len / 2)

		return self.token[:sub_token_len].ljust(token_len, '*')

	'''
		gen: oauth-headers
	'''
	def gen_oauth_headers(self):
		if not self.token:
			return None

		return { 'Authorization': 'token %s' % (self.token) }
