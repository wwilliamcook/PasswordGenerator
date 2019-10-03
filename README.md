# PasswordGenerator
Cryptographically secure password generator. Uses `os.urandom` and aims for statistical uniformity for all stochastic operations. Supports two modes of password generation:
* **Dense** - generates high entropy-density passwords that tend to be more difficult to memorize, but are good for usage with a password manager.
* **Memorable** - generates long, more feasibly memorable passwords using words and predictable organization. Inspired by [XKCD](https://xkcd.com/936/).

## Usage
For easy in-browser use, see the full-featured web app demo [here](https://wwilliamcook.github.io/PasswordGenerator/).

For use with Python, the `main` function is located in `generate.py`, so just run that file with Python. It can be used with or without command line arguments, with the same degree of functionality either way.
Run `python generate.py -h` to see available command line options or just run `python generate.py` to use the built-in UI.

## Dependencies
The libraries used in this code were chosen to avoid external dependencies. Here is a list of the imports:
* `sys`
* `os`
* `math`
* `requests`
* `argparse`

## Credits
The word list used for *memorable* mode is pulled from [Josh Kaufman's google-10000-english](https://github.com/first20hours/google-10000-english).
