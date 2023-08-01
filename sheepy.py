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

class Word:
    def __init__(self, str: str):
        self.str = str
    
    def is_word(obj: object) -> bool:
        return isinstance(obj, Word)
    
    def is_word_with(obj: object, str: str) -> bool:
        if not Word.is_word(obj):
            return False
        elif obj.str == str:
            return True
        return False

class Comment:
    def __init__(self, content: str):
        self.content = content
    
    def is_comment(obj: object) -> bool:
        return isinstance(obj, Comment)

class SQuote(Word):
    def __init__(self, str: str, content: str):
        super().__init__(str)
        self.content = content

class Newline:
    def is_newline(obj: object) -> bool:
        return isinstance(obj, Newline)

class Assign(Word):
    def __init__(self, str: str, name: str, value: str):
        super().__init__(str)
        self.name = name
        self.value = value

class Var(Word):
    def __init__(self, str: str, name: str):
        super().__init__(str)
        self.name = name

class Lexer:
    def __init__(self, input: str):
        self.input = input
        self.token = []
    
    def tokenize(self) -> list[object]:
        self.shebang()
        while True:
            if self.lex_comment():
                continue
            elif self.lex_squote():
                continue
            elif self.lex_newline():
                continue
            elif self.lex_assign():
                continue
            elif self.lex_var():
                continue
            elif self.lex_varcurly():
                continue
            elif self.lex_word():
                continue
            elif self.lex_empty():
                continue
            elif self.eof():
                eprint("lex done")
                return self.token
            else: # failed
                eprint("failed")
                return None

    def shebang(self):
        m = re.search(t_SHEBANG, self.input)
        if m.span()[0] == 0: # match at ln 0 col 0
            self.cut(m.span())
        eprint(self.input)

    def lex_comment(self) -> bool:
        m = re.search(t_COMMENT, self.input)
        if m == None:
            return False
        elif m.span()[0] == 0:
            self.token.append(Comment(m.group(1)))
            self.cut(m.span())
            return True
        return False
    
    def lex_squote(self) -> bool:
        m = re.search(t_SQUOTE, self.input)
        if m == None:
            return False
        elif m.span()[0] == 0:
            self.token.append(SQuote(m.group(0), m.group(1)))
            self.cut(m.span())
            return True
        return False
    
    def lex_newline(self) -> bool:
        m = re.search(t_NEWLINE, self.input)
        if m == None:
            return False
        elif m.span()[0] == 0:
            self.token.append(Newline())
            self.cut(m.span())
            return True
        return False

    def lex_assign(self) -> bool:
        m = re.search(t_ASSIGN, self.input)
        if m == None:
            return False
        elif m.span()[0] == 0:
            self.token.append(Assign(m.group(0), m.group(1), m.group(2)))
            self.cut(m.span())
            return True
        return False

    def lex_var(self) -> bool:
        m = re.search(t_VAR, self.input)
        if m == None:
            return False
        elif m.span()[0] == 0:
            self.token.append(Var(m.group(0), m.group(1)))
            self.cut(m.span())
            return True
        return False

    def lex_varcurly(self) -> bool:
        m = re.search(t_VARCURLY, self.input)
        if m == None:
            return False
        elif m.span()[0] == 0:
            self.token.append(Var(m.group(0), m.group(1)))
            self.cut(m.span())
            return True
        return False

    def lex_word(self) -> bool:
        m = re.search(t_WORD, self.input)
        if m == None:
            return False
        elif m.span()[0] == 0:
            self.token.append(Word(m.group(1)))
            self.cut(m.span())
            return True
        return False

    def lex_empty(self) -> bool:
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

class Stmt:
    def __init__(self, comment: Comment):
        self.comment = comment

class Echo(Stmt):
    def __init__(self, comment: Comment, args: list[Word]):
        super().__init__(comment)
        self.args = args

class Parser:
    def __init__(self, token: list[object]):
        self.token = token
        self.stmt = []
    
    def parse(self):
        while True:
            if self.token == []:
                eprint("parse done")
                return self.stmt
            elif self.parse_echo():
                continue
            else:
                eprint("parse failed")
                return None
    
    def parse_echo(self):
        i = 0
        comment = None
        if Word.is_word_with(self.token[i], "echo"):
            args = []
            i += 1
            while Word.is_word(self.token[i]):
                args.append(self.token[i])
                i += 1
            if Comment.is_comment(self.token[i]):
                comment = self.token[i]
                i += 1
            if Newline.is_newline(self.token[i]):
                i += 1
            self.stmt.append(Echo(comment, args))
            self.cut(i)
            return True
        else:
            return False
    
    def cut(self, i: int):
        self.token = self.token[i:]

class Transpiler:
    def __init__(self):
        self.header = "#!/usr/bin/python3 -u\n"
        self.body = ""
        self.token = []

    def transpile(self) -> str:
        return self.header + self.body

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: sheepy.py FILE")
        exit(0)
    filename = sys.argv[1]
    with open(filename) as f:
        lexer = Lexer(f.read())
        token = lexer.tokenize()
        eprint(token)
        parser = Parser(token)
        stmt = parser.parse()
        eprint(stmt)