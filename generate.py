"""Main function for password generator.
"""

import argparse

from random_tools import densePassword, memorablePassword


def main(args):
    if args.mode is None:
        # Find out what mode the user wants
        while True:
            mode = input('Enter a password mode [dense|memorable] (d/m): ')
            # Replace shorthand
            if mode in ('d', ''):
                mode = 'dense'
            elif mode == 'm':
                mode = 'memorable'
            # Validate input
            if mode in ('dense', 'memorable'):
                break
            else:
                print('Invalid mode. Try again.')
    else:
        mode = args.mode
    # Generate and print password
    if mode == 'dense':
        print('Generating entropy-dense password...')
        password = densePassword(16)
    elif mode == 'memorable':
        print('Generating memorable password...')
        password = memorablePassword()
    else:
        print(f'Error: invalid password mode: {mode}')
        input('Press enter to exit.')
        exit()
    print(f'New password: {password}')
    input('Press enter to exit.')


if __name__ == '__main__':
    p = argparse.ArgumentParser()

    p.add_argument('--mode', '-m', type=str, choices=('dense', 'memorable'),
                   help='Specify whether to generate a dense or memorable password.')

    args = p.parse_args()
    
    main(args)
