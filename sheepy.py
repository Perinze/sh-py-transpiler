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
    
    def is_assign(obj: object) -> bool:
        return isinstance(obj, Assign)

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

class NewlineExp:
    pass

class CommentExp:
    pass

class AssignExp:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

class CdExp:
    def __init__(self, dir: Word):
        self.dir = dir

class EchoExp:
    def __init__(self, args: list[Word]):
        self.args = args

class ForExp:
    def __init__(self, var: Word, iter: list[Word], body: list[object]):
        self.var = var
        self.iter = iter
        self.body = body

class CmdExp:
    def __init__(self, cmd: list[Word]):
        self.cmd = cmd

class Parser:
    def __init__(self, token: list[object]):
        self.token = token
        self.pos = 0
        #self.stmt = []

    def parse(self):
        stmt = []
        self.parse_sequence(stmt)
        return stmt
    
    def parse_sequence(self, stmt: list[object]) -> bool:
        bak = (self.pos, stmt)
        while True:
            if self.pos >= len(self.token):
                eprint("parse done")
                return True
            elif self.next_is_terminator():
                eprint("block terminate")
                return True
            elif self.parse_comment(stmt):
                eprint("comment")
                continue
            elif self.parse_newline(stmt):
                eprint("newline")
                continue
            elif self.parse_assign(stmt):
                eprint("assign")
                continue
            elif self.parse_cd(stmt):
                eprint("cd")
                continue
            elif self.parse_echo(stmt):
                eprint("echo")
                continue
            elif self.parse_for(stmt):
                eprint("for")
                continue
            elif self.parse_cmd(stmt):
                eprint("cmd")
                continue
            else:
                eprint("fail")
                self.pos, stmt = bak
                return False

    # this method won't consume token
    def next_is_terminator(self) -> bool:
        if Word.is_word_with(self.token[self.pos], "done"):
            return True
        return False

    def parse_newline(self, stmt: list[object]) -> bool:
        # no need to check out of range since this method is called
        # for non-empty token list
        if Newline.is_newline(self.token[self.pos]):
            stmt.append(NewlineExp())
            self.pos += 1
            return True
        return False
    
    def parse_comment(self, stmt: list[object]) -> bool:
        # same as above
        if Comment.is_comment(self.token[self.pos]):
            stmt.append(CommentExp())
            self.pos += 1
            return True
        return False
    
    def parse_assign(self, stmt: list[object]) -> bool:
        # same as above
        t = self.token[self.pos]
        if Assign.is_assign(t):
            stmt.append(AssignExp(t.name, t.value))
            self.pos += 1
            return True
        return False
    
    def parse_cd(self, stmt: list[object]) -> bool:
        # same as above
        if Word.is_word_with(self.token[self.pos], "cd"):
            self.pos += 1
            arg = None
            if self.pos < len(self.token) and Word.is_word(self.token[self.pos]):
                arg = self.token[self.pos]
                self.pos += 1
            stmt.append(CdExp(arg))
            return True
        return False
    
    def parse_echo(self, stmt: list[object]):
        # same as above
        if Word.is_word_with(self.token[self.pos], "echo"):
            args = []
            self.pos += 1
            while self.pos < len(self.token) and Word.is_word(self.token[self.pos]):
                args.append(self.token[self.pos])
                self.pos += 1
            stmt.append(EchoExp(args))
            return True
        return False
    
    def parse_for(self, stmt: list[object]):
        bak = (self.pos, stmt)
        # for
        if Word.is_word_with(self.token[self.pos], "for"):
            self.pos += 1
        else:
            self.pos, stmt = bak
            return False
        var = None
        iter = []
        body = []
        # loop-var
        if self.pos < len(self.token) and Word.is_word(self.token[self.pos]):
            var = self.token[self.pos]
            self.pos += 1
        else:
            self.pos, stmt = bak
            return False
        # in
        if self.pos < len(self.token) and Word.is_word_with(self.token[self.pos], "in"):
            self.pos += 1
        else:
            self.pos, stmt = bak
            return False
        # iterable
        while self.pos < len(self.token) and Word.is_word(self.token[self.pos]):
            iter.append(self.token[self.pos])
            self.pos += 1
        # newline TODO semicolon
        if self.pos < len(self.token) and Newline.is_newline(self.token[self.pos]):
            self.pos += 1
        else:
            self.pos, stmt = bak
            return False
        # do
        if self.pos < len(self.token) and Word.is_word_with(self.token[self.pos], "do"):
            self.pos += 1
        else:
            self.pos, stmt = bak
            return False
        # newline TODO semicolon
        if self.pos < len(self.token) and Newline.is_newline(self.token[self.pos]):
            self.pos += 1
        else:
            self.pos, stmt = bak
            return False
        # body
        if not self.parse_sequence(body):
            self.pos, stmt = bak
            return False
        # done
        if self.pos < len(self.token) and Word.is_word_with(self.token[self.pos], "done"):
            self.pos += 1
        else:
            self.pos, stmt = bak
            return False
        stmt.append(ForExp(var, iter, body))
        return True
    
    def parse_cmd(self, stmt: list[object]):
        cmd = []
        # same as above
        while self.pos < len(self.token) and Word.is_word(self.token[self.pos]):
            cmd.append(self.token[self.pos])
            self.pos += 1
        stmt.append(CmdExp(cmd))
        return True

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