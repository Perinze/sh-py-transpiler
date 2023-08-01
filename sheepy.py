#!/usr/bin/python3 -u
import sys
import re

t_SHEBANG = r'#!/bin/dash\n'
t_COMMENT = r'(#.*)\n'
t_SQUOTE = r'\'([^\']*)\''
t_NEWLINE = r'\n'
t_ASSIGN = r'(\w+)=(\S+)'
t_VAR = r'\$(\w+)'
t_VARCURLY = r'\${(\w+)}'
t_WORD = r'(\S+)'
t_EMPTY = r'\s+'

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Comment:
    def __init__(self, content: str):
        self.content = content

class SQuote:
    def __init__(self, content: str):
        self.content = content

class Newline:
    pass

class Assign:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

class Var:
    def __init__(self, name: str):
        self.name = name

class Word:
    def __init__(self, str: str):
        self.str = str

class Transpiler:
    def __init__(self, input: str):
        self.input = input
        self.header = "#!/usr/bin/python3 -u\n"
        self.body = ""
        self.token = []

    def transpile(self) -> str:
        self.shebang()
        self.parse()
        return self.header + self.body

    def shebang(self):
        m = re.search(t_SHEBANG, self.input)
        if m.span()[0] == 0: # match at ln 0 col 0
            self.cut(m.span())
        eprint(self.input)
    
    def parse(self):
        while True:
            if self.parse_comment():
                continue
            elif self.parse_squote():
                continue
            elif self.parse_newline():
                continue
            elif self.parse_assign():
                continue
            elif self.parse_var():
                continue
            elif self.parse_varcurly():
                continue
            elif self.parse_word():
                continue
            elif self.parse_empty():
                continue
            elif self.eof():
                eprint("parse done")
                eprint(self.token)
                return
            else: # failed
                eprint("failed")
                return
    
    def parse_comment(self) -> bool:
        m = re.search(t_COMMENT, self.input)
        if m == None:
            return False
        elif m.span()[0] == 0:
            self.token.append(Comment(m.group(1)))
            self.cut(m.span())
            return True
        return False
    
    def parse_squote(self) -> bool:
        m = re.search(t_SQUOTE, self.input)
        if m == None:
            return False
        elif m.span()[0] == 0:
            self.token.append(SQuote(m.group(1)))
            self.cut(m.span())
            return True
        return False
    
    def parse_newline(self) -> bool:
        m = re.search(t_NEWLINE, self.input)
        if m == None:
            return False
        elif m.span()[0] == 0:
            self.token.append(Newline())
            self.cut(m.span())
            return True
        return False

    def parse_assign(self) -> bool:
        m = re.search(t_ASSIGN, self.input)
        if m == None:
            return False
        elif m.span()[0] == 0:
            self.token.append(Assign(m.group(1), m.group(2)))
            self.cut(m.span())
            return True
        return False

    def parse_var(self) -> bool:
        m = re.search(t_VAR, self.input)
        if m == None:
            return False
        elif m.span()[0] == 0:
            self.token.append(Var(m.group(1)))
            self.cut(m.span())
            return True
        return False

    def parse_varcurly(self) -> bool:
        m = re.search(t_VARCURLY, self.input)
        if m == None:
            return False
        elif m.span()[0] == 0:
            self.token.append(Var(m.group(1)))
            self.cut(m.span())
            return True
        return False

    def parse_word(self) -> bool:
        m = re.search(t_WORD, self.input)
        if m == None:
            return False
        elif m.span()[0] == 0:
            self.token.append(Word(m.group(1)))
            self.cut(m.span())
            return True
        return False

    def parse_empty(self) -> bool:
        m = re.search(t_EMPTY, self.input)
        if m == None:
            return False
        elif m.span()[0] == 0:
            self.cut(m.span())
            return True
        return False
    
    def eof(self) -> bool:
        return self.input == ""
        
    def cut(self, span: tuple[int, int]):
        self.input = self.input[span[1]:]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: sheepy.py FILE")
        exit(0)
    filename = sys.argv[1]
    with open(filename) as f:
        transpiler = Transpiler(f.read())
        print(transpiler.transpile())