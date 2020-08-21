import requests
import hashlib
import sys
import string

def request_api_data(query_char):
	url = 'https://api.pwnedpasswords.com/range/'+query_char
	resp = requests.get(url)
	if resp.status_code != 200:
		raise RuntimeError(f'Error fetching: {resp.status_code}, check your code and type again.')
	return resp

def get_password_leaks_count(hashes, hash_to_check):
	hashes = (line.split(':') for line in hashes.text.splitlines())
	for h, count in hashes:
		if h == hash_to_check:
			return count
	return 0

def pwned_api_check(password):
	sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	first5_char, tail = sha1password[:5], sha1password[5:]
	response = request_api_data(first5_char)
	return get_password_leaks_count(response, tail)

def main(args):
	for password in args:
		count = pwned_api_check(password)
		if count:
			print(f'{password} was hacked {count} times...you should probably change it.')
		else:
			print(f'{password} not found.Its safe to use.')
	return 'Done!!'

with open('passwords.txt', 'r') as file:
	passwords = file.readlines()
	for password in passwords:
		passwords[passwords.index(password)] = password[:len(password)-1]
	sys.exit(main(passwords))