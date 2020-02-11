import requests
import hashlib
import sys


def request_api_data(query):
    url = 'https://api.pwnedpasswords.com/range/'+query
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}')
    return res


def get_pass_leaks_count(hashes, hash_to_check=" "):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_pass_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} has been hacked {count} I would reconsider using it')
        else:
            print(f'it appears that password {password} has not been hacked')
    return 'ok'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
