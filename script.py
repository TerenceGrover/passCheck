import string
import random
import argparse


# Create top-level parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')

# Create parser for "check" command
check_parser = subparsers.add_parser('check', help='check password strength')
check_parser.add_argument('password', type=str, help='password to check')

def check_password(password):
    # Here are the ideas.
    # 1. Check if password is longer than 8 characters
    # 2. Check if password contains at least one digit
    # 3. Check if password contains at least one uppercase letter
    # 4. Check if password contains at least one lowercase letter
    # 5. Check if password contains at least one special character
    # Once those are done, return a score between 0 and 10
    # Offer alternative passwords if the score is low which can be selected with digits in the command line. This will copy the password to the clipboard.

    return password


args = parser.parse_args()

if args.command == 'check':
    print(check_password(args.password))