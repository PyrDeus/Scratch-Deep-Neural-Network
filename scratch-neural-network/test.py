#!/usr/local/bin/python3

from window import Screen

s = Screen(200, 200)
print(id(s))
print(type(id(s)))

print(type(type(Screen)))


string:str = None

print(string is None)
print(string is str)
