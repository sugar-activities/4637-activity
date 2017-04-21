#!/usr/bin/python

from subprocess import Popen

def say(text):
    Popen(['espeak', '-v', 'es', text])


def main():
	say(a)#que es esto?

if __name__ == "__main__":
    main()
