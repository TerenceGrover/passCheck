import string
import random
import argparse
from collections import deque
import pyperclip
import getpass

# Gets the username of the current user
username = getpass.getuser()
print('Welcome ' + username + '!')

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
        'special': False,
        'word': False
    }

details = {
    'length': 'Password should be at least 8 characters long',
    'digit': 'Password should contain at least one digit',
    'uppercase': 'Password should contain at least one uppercase letter',
    'lowercase': 'Password should contain at least one lowercase letter',
    'special': 'Password should contain at least one special character',
    'word': 'Password should not contain a common word',
    'username': 'Password should not contain any personal info like username, name, etc...'
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
    # 6. Check if password contains a common word
    indicators['word'] = not contains_dictionary_word(password, words)
    # 7. Check if password contains personal info
    indicators['username'] = not check_sequence(password, username)
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

def load_words(word_file):
    """Load words from a file into a set."""
    with open(word_file) as f:
        return set(word.strip().lower() for word in f)

def contains_dictionary_word(password, words):
    """Check if a password contains a word from the dictionary."""
    password_lower = password.lower()
    for i in range(len(password)):
        for j in range(i + 1, len(password) + 1):
            if password_lower[i:j] in words:
                return True
    return False

def check_sequence(password, username):
    for i in range(len(username) - 3):
        sequence = username[i:i+4].lower()
        if sequence in password.lower():
            return True
    return False

def generate_alternative_passwords(password, num):
    return [password + ''.join(random.choices(string.ascii_lowercase, k=3)) for _ in range(num)]


args = parser.parse_args()
words = load_words('word_file.txt')

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
    print('======================== UPGRADED OPTIONS ==========================')
    print('press digit to copy password to clipboard')
    alternatives = generate_alternative_passwords(args.password, 5)
    for i, alt in enumerate(alternatives, start=1):
        print(f"{i}. {alt}")
    choice = input("Enter the number of the password you want to use, or 'n' to cancel: ")
    if choice.isdigit() and 1 <= int(choice) <= len(alternatives):
        chosen_password = alternatives[int(choice) - 1]
        # Copy the password to clipboard
        pyperclip.copy(chosen_password)