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
    return password


args = parser.parse_args()

if args.command == 'check':
    print(check_password(args.password))