import pyshorteners

def down_linker(text):
    s = pyshorteners.Shortener()
    return s.clckru.short(text)
