"""Functions for generating cryptographically secure random data.

Word list retrieved from https://github.com/first20hours/google-10000-english.
"""

import sys
import os
import math
import requests


def randomInteger(a, b):
    """Returns a random integer on the range [a, b).

    Args:
        a: Minimum possible integer (inclusive).
        b: Maximum possible integer (exclusive).
    """
    # Perform input checks
    if int(a) != a or int(b) != b:
        raise TypeError('a and b must be integers.')
    if a >= b:
        raise ValueError('a must be less than b.')
    #
    diff = b - a
    if diff == 1:  # Only one possible output
        return a
    else:
        # Calculate number of bytes to generate
        number_of_bytes = math.ceil(math.log(diff, 256))
        # Calculate bitmask to remove excess bits
        bitmask = int('1' * math.ceil(math.log(diff, 2)), 2)
        i = -1
        # Generate random ints until one is in the desired range
        # Seems bad, but looks like it's the only way to ensure statistical uniformity
        while (i < 0 or i >= diff):
            i = int.from_bytes(os.urandom(number_of_bytes), 'little') & bitmask
        
        return i + a

def randomChoice(a):
    """Chooses a random element from the given iterable.

    Args:
        a: array-like object to draw elements from.
    """
    return a[randomInteger(0, len(a))]

def shuffle(a):
    """Shuffles the given iterable.

    Args:
        a: array-like object to shuffle.
    """
    T = type(a)
    a = list(a)
    a = [a.pop(randomInteger(0, len(a))) for i in range(len(a))]
    # Convert a back to its original type
    if T == str:
        a = ''.join(a)
    else:
        try:
            a = T(a)
        except:
            pass
    
    return a

def randomLower():
    """Returns a random lowercase letter."""
    return randomChoice('abcdefghijklmnopqrstuvwxyz')

def randomUpper():
    """Returns a random uppercase letter."""
    return randomChoice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

def randomDigit():
    """Returns a random digit."""
    return randomChoice('0123456789')

def randomSpecial():
    """Returns a random special character."""
    return randomChoice('!#$%&()*+,-./:;<=>?@[]^_`{|}~')

def randomFloat(bits=64):
    """Returns a random float on the range [0, 1].

    Args:
        bits: Number of bits to use for the float.
    """
    N = 2**bits
    return float(randomInteger(0, N)) / float(N - 1)

def randomBool(p=None):
    """Returns a random bool.

    Args:
        p: Probability that the bool is True.
    """
    if p is None:  # Nothing special
        return bool(randomInteger(0, 2))
    # Perform input checks
    if float(p) != p:
        raise TypeError(f'p must be a float. Given: {type(p)}')
    if p < 0 or p > 1:
        raise ValueError(f'p must be on range [0, 1]. Given: {p}')
    r = p  # r is balanced between True and False
    # Move r until it is not balanced anymore
    while r == p:
        r = randomFloat()
    
    return r < p

def randomPin(digits):
    """Returns a random PIN.

    Args:
        digits: Number of digits.
    """
    return ''.join([randomDigit() for i in range(digits)])

def getWordList(path='wordlist.txt'):
    """Returns the list of the words stored in the given file.
    """
    def replacechars(s, fromchars, tochar):
        for c in fromchars:
            s = s.replace(c, tochar)
        return s

    try:
        if os.path.exists(path):
            # Read words from file
            with open(path) as f:
                words = f.read()
            savewhendone = False
        else:
            # Download words
            url = 'https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears.txt'
            words = requests.get(url).content.decode()
            savewhendone = True
    except Exception as e:
        print('%s: %s' % (str(type(e))[8:-2], e), file=sys.stderr)
        exit()
    words = words.lower().strip(' \t\n\r\x0b\x0c')
    # Replace all whitespace with newlines
    words = replacechars(words, ' \t\n\r\x0b\x0c', '\n')
    # Convert to list
    words = words.split('\n')
    # Remove empty strings
    words = [w for w in words if w]

    if savewhendone:
        with open(path, 'w+') as f:
            f.write('\n'.join(words))
    
    return words

def randomWord(min_len=1, max_len=None, wordList=None):
    """Returns a random word.

    WARNING: Hangs if the list does not contain any words of the specified length.

    Args:
        min_len: Minimum number of characters in the word.
        max_len: Maximum number of characters in the word.
        wordList: List of words to choose from.
    """
    # Acquire list of words
    if wordList is None:
        wordList = getWordList()
    # Pick random words until one matches the requirements
    word = ''
    if max_len is None:
        while len(word) < min_len:
            word = randomChoice(wordList)
    else:
        while (len(word) < min_len or len(word) > max_len):
            word = randomChoice(wordList)
    
    return word

def densePassword(length=32, lower=True, upper=True, digits=True, special=True):
    """Returns a secure, high entropy-density password that may be difficult to memorize.

    Args:
        length: Length of password to generate.
        lower: Include lowercase letters.
        upper: Include uppercase letters.
        digits: Include digits.
        special: Include special characters.
    """
    out = ''
    # Add as many characters of each kind as can fit
    while len(out) < length:
        # Create buffer to hold potential new characters
        newchars = ''
        # Add random characters to the buffer
        if upper:
            newchars += randomUpper()
        if lower:
            newchars += randomLower()
        if digits:
            newchars += randomDigit()
        if special:
            newchars += randomSpecial()
        # If the password can fit all the new characters, add them
        if len(out) + len(newchars) <= length:
            out += newchars
        else:  # The password can only fit some of the new characters
            # Randomly select (without replacement) from the new
            # characters and add them until the password is full
            newchars = list(newchars)
            while len(out) <= length:
                out += newchars.pop(randomInteger(0, len(newchars)))
    
    assert len(out) == length

    return shuffle(out)

def memorablePassword(minWords=7, maxWords=10,
                      minDigits=3, maxDigits=5,
                      minPad=2, maxPad=7,
                      minWordLength=4, maxWordLength=None,
                      wordList=None):
    """Returns a secure and long, but feasibly memorizable, password.

    Args:
        minWords: Minimum number of words to include.
        maxWords: Maximum number of words to include.
        minDigits: Minimum number of padding digits.
        maxDigits: Maximum number of padding digits.
        minPad: Minimum size of special character padding.
        maxPad: Maximum size of special character padding.
        minWordLength: Minimum length of words.
        maxWordLength: Maximum length of words.
        wordList: List to draw words from.
    """
    # Acquire word list
    if wordList is None:
        wordList = getWordList()
    # Generate special character padding
    padding = randomSpecial() * randomInteger(minPad, maxPad + 1)
    # Generate padding digits
    digitLen = randomInteger(minDigits, maxDigits + 1)
    digits = (randomPin(digitLen), randomPin(digitLen))
    # Generate word-deliminating character
    sep = randomSpecial()
    # Generate words
    wordCount = randomInteger(minWords, maxWords + 1)
    words = [randomWord(minWordLength, maxWordLength, wordList) for i in range(wordCount)]
    # Randomize the capitalization of each word
    words = [w.upper() if randomBool() else w.lower() for w in words]

    return padding + digits[0] + sep + sep.join(words) + sep + digits[1] + padding
