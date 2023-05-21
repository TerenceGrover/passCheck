import string
import random
import argparse
from collections import deque
# import pyperclip

# Create top-level parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')

# Create parser for "check" command
check_parser = subparsers.add_parser('check', help='check password strength')
check_parser.add_argument('password', type=str, help='password to check')

indicators = {
        'length': False,
        'digit': False,
        'uppercase': False,
        'lowercase': False,
        'special': False
    }

details = {
    'length': 'Password should be at least 8 characters long',
    'digit': 'Password should contain at least one digit',
    'uppercase': 'Password should contain at least one uppercase letter',
    'lowercase': 'Password should contain at least one lowercase letter',
    'special': 'Password should contain at least one special character'
}

new_details = deque([])

def check_password(password):
    # Here are the ideas.
    # 1. Check if password is longer than 8 characters
    indicators['length'] = len(password) >= 8
    if not indicators['length']:
        new_details.append('❌ ' + details['length'])
        return 0
    # 2. Check if password contains at least one digit
    indicators['digit'] = any(char.isdigit() for char in password)
    # 3. Check if password contains at least one uppercase letter
    indicators['uppercase'] = any(char.isupper() for char in password)
    # 4. Check if password contains at least one lowercase letter
    indicators['lowercase'] = any(char.islower() for char in password)
    # 5. Check if password contains at least one special character
    indicators['special'] = any(char in string.punctuation for char in password)
    # Once those are done, return a score between 0 and 10
    score = 0
    for indicator, val in indicators.items():
        if val:
            score += 2
            new_details.appendleft('✅ ' + details[indicator])
        else:
            new_details.append('❌ ' + details[indicator])
    return score
    # Offer alternative passwords if the score is low which can be selected with digits in the command line. This will copy the password to the clipboard.


def check_common(password):
    with open('common_passwords.txt') as f:
        common_passwords = f.read().splitlines()
    return password in common_passwords

args = parser.parse_args()

if args.command == 'check':
    if len(args.password) < 8:
        print('Password is too short')
        exit()
    print('\n')
    print('======================= PASS STRENGTH =======================')
    print('Pass level is: ' + str(check_password(args.password)))
    print(check_common(args.password) and '❌ Password is commonly found on password lists' or '✅ Password is NOT commonly found on password lists')
    print('\n')
    print('=============== WAYS TO IMPROVE YOUR PASSWORD ===============')
    for detail in new_details:
        print(detail)
    print('\n')