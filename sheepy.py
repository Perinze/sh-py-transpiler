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

test_operators = ["=", "!="]

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
    
    def is_var(obj: object) -> bool:
        return isinstance(obj, Var)

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
    def is_newline_exp(obj: object) -> bool:
        return isinstance(obj, NewlineExp)

class CommentExp:
    pass

class AssignExp:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value
    
    def is_assign_exp(obj: object) -> bool:
        return isinstance(obj, AssignExp)

class CdExp:
    def __init__(self, dir: Word):
        self.dir = dir
    
    def is_cd_exp(obj: object) -> bool:
        return isinstance(obj, CdExp)

class ExitExp:
    def __init__(self, exit_code: Word):
        self.exit_code = exit_code

    def is_exit_exp(obj: object) -> bool:
        return isinstance(obj, ExitExp)

class EchoExp:
    def __init__(self, args: list[Word]):
        self.args = args

    def is_echo_exp(obj: object) -> bool:
        return isinstance(obj, EchoExp)

class ForExp:
    def __init__(self, var: Word, iter: list[Word], body: list[object]):
        self.var = var
        self.iter = iter
        self.body = body

    def is_for_exp(obj: object) -> bool:
        return isinstance(obj, ForExp)

class TestExp:
    pass

class CmpTestExp(TestExp):
    def __init__(self, op: Word, lhs: Word, rhs: Word) -> None:
        super().__init__()
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def is_cmp_test_exp(obj: object) -> bool:
        return isinstance(obj, CmpTestExp)

class IfExp:
    def __init__(self, pred: list[TestExp], branch: list[list[object]]):
        self.pred = pred
        self.branch = branch

class WhileExp:
    def __init__(self, pred: TestExp, body: list[object]):
        self.pred = pred
        self.body = body

class CmdExp:
    def __init__(self, cmd: list[Word]):
        self.cmd = cmd

    def is_cmd_exp(obj: object) -> bool:
        return isinstance(obj, CmdExp)

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
            elif self.parse_exit(stmt):
                eprint("exit")
                continue
            elif self.parse_for(stmt):
                eprint("for")
                continue
            elif self.parse_if(stmt):
                eprint("if")
                continue
            elif self.parse_while(stmt):
                eprint("while")
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
        if Word.is_word_with(self.token[self.pos], "elif"):
            return True
        if Word.is_word_with(self.token[self.pos], "else"):
            return True
        if Word.is_word_with(self.token[self.pos], "fi"):
            return True
        return False

    # this method won't consume token
    def next_is_elif(self) -> bool:
        if Word.is_word_with(self.token[self.pos], "elif"):
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
    
    def parse_exit(self, stmt: list[object]):
        # same as above
        if Word.is_word_with(self.token[self.pos], "exit"):
            exit_code = None
            self.pos += 1
            if self.pos < len(self.token) and Word.is_word(self.token[self.pos]):
                exit_code = self.token[self.pos]
                self.pos += 1
            stmt.append(ExitExp(exit_code))
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
        # init for-exp fields
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

    # TODO only implemented eq test in subset 2
    def parse_pred(self) -> TestExp:
        testexp = self.parse_pred_comparation()
        if testexp != None:
            return testexp

    def parse_pred_comparation(self) -> TestExp:
        bak = self.pos
        # test keyword
        if Word.is_word_with(self.token[self.pos], "test"):
            self.pos += 1
        else:
            self.pos = bak
            return None
        lhs = None
        # lhs
        if Word.is_word(self.token[self.pos]):
            lhs = self.token[self.pos]
            self.pos += 1
        else:
            self.pos = bak
            return None
        # operator
        operator = None
        if Word.is_word(self.token[self.pos]):
            op = self.token[self.pos].str
            # check if operator is valid
            if not (op in test_operators):
                self.pos = bak
                return None
            operator = self.token[self.pos]
            self.pos += 1
        else:
            self.pos = bak
            return None
        # rhs
        rhs = None
        if Word.is_word(self.token[self.pos]):
            rhs = self.token[self.pos]
            self.pos += 1
        else:
            self.pos = bak
            return None
        # success
        return CmpTestExp(operator, lhs, rhs)

    def parse_if(self, stmt: list[object]):
        bak = (self.pos, stmt)
        # if
        if Word.is_word_with(self.token[self.pos], "if"):
            self.pos += 1
        else:
            self.pos, stmt = bak
            return False
        # init for-exp fields
        pred = []
        branch = []
        # first predicate
        test = self.parse_pred()
        if test != None:
            pred.append(test)
        else:
            self.pos, stmt = bak
            return False
        # newline TODO semicolon
        if self.pos < len(self.token) and Newline.is_newline(self.token[self.pos]):
            self.pos += 1
        else:
            self.pos, stmt = bak
            return False
        # then
        if self.pos < len(self.token) and Word.is_word_with(self.token[self.pos], "then"):
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
        # first body
        body = []
        if not self.parse_sequence(body):
            self.pos, stmt = bak
            return False
        branch.append(body)
        # elif loop
        while self.pos < len(self.token) and self.next_is_elif():
            self.pos += 1
            # predicate
            test = self.parse_pred()
            if test != None:
                pred.append(test)
            else:
                self.pos, stmt = bak
                return False
            # newline TODO semicolon
            if self.pos < len(self.token) and Newline.is_newline(self.token[self.pos]):
                self.pos += 1
            else:
                self.pos, stmt = bak
                return False
            # then
            if self.pos < len(self.token) and Word.is_word_with(self.token[self.pos], "then"):
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
            body = []
            if not self.parse_sequence(body):
                self.pos, stmt = bak
                return False
            branch.append(body)
        # else
        if self.pos < len(self.token) and Word.is_word_with(self.token[self.pos], "else"):
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
        body = []
        if not self.parse_sequence(body):
            self.pos, stmt = bak
            return False
        branch.append(body)
        # fi
        if self.pos < len(self.token) and Word.is_word_with(self.token[self.pos], "fi"):
            self.pos += 1
        else:
            self.pos, stmt = bak
            return False
        stmt.append(IfExp(pred, branch))
        return True
    
    def parse_while(self, stmt: list[object]):
        bak = (self.pos, stmt)
        # while
        if Word.is_word_with(self.token[self.pos], "while"):
            self.pos += 1
        else:
            self.pos, stmt = bak
            return False
        # init while-exp fields
        pred = None
        body = []
        # predicate
        pred = self.parse_pred()
        eprint(pred)
        if pred == None:
            self.pos, stmt = bak
            return False
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
        stmt.append(WhileExp(pred, body))
        return True
    
    def parse_cmd(self, stmt: list[object]):
        cmd = []
        # same as above
        while self.pos < len(self.token) and Word.is_word(self.token[self.pos]):
            cmd.append(self.token[self.pos])
            self.pos += 1
        stmt.append(CmdExp(cmd))
        return True

class Translator:
    def __init__(self, ast: list[object]):
        #self.header = "#!/usr/bin/python3 -u\n"
        self.ast = ast
        self.glob_import = False
        self.os_import = False
        self.subprocess_import = False
        self.sys_import = False

    def translate(self) -> str:
        header = "#!/usr/bin/python3 -u\n"
        body = self.translate_sequence(self.ast)
        if self.os_import:
            header += "import os\n"
        if self.subprocess_import:
            header += "import subprocess\n"
        return header + body
    
    def translate_sequence(self, explist: list[object], indent: int = 0) -> str:
        body = ""
        beginning_of_line = True
        shift_str = indent * 4 * " "
        for exp in explist:
            if beginning_of_line:
                body += shift_str
                beginning_of_line = False
            increment = self.translate_newline(exp)
            if increment != "":
                beginning_of_line = True
                body += increment
                continue
            #increment = self.translate_comment(exp)
            #if increment != "":
            #    beginning_of_line = True
            #    body += increment
            #    continue
            increment = self.translate_assign(exp)
            if increment != "":
                beginning_of_line = True
                body += increment
                continue
            increment = self.translate_cd(exp)
            if increment != "":
                beginning_of_line = True
                body += increment
                continue
            increment = self.translate_exit(exp)
            if increment != "":
                body += increment
                continue
            increment = self.translate_echo(exp)
            if increment != "":
                body += increment
                continue
            increment = self.translate_for(exp, indent)
            if increment != "":
                body += increment
                continue
            increment = self.translate_cmd(exp)
            if increment != "":
                body += increment
                continue
            # none of these matches
            eprint("translate clause not implemented")
            return "error: not valid exp"
        return body
    
    def translate_newline(self, exp: object) -> str:
        if NewlineExp.is_newline_exp(exp):
            return "\n"
        return ""
    
    # TODO implement word str only
    # check variable as a whole word
    def translate_word(self, word: Word) -> str:
        if Var.is_var(word):
            return word.name
        return self.translate_word_str(word.str)
    
    # check variable embedded in a word
    def translate_word_str(self, word: str) -> str:
        if '*' in word:
            self.glob_import = True
            return f"sorted(glob.glob(\"{word}\"))"
        return f"'{word}'"
    
    def translate_cd(self, exp: object) -> str:
        if CdExp.is_cd_exp(exp):
            self.os_import = True
            fmt = "os.chdir({})"
            code = fmt.format(self.translate_word(exp.dir))
            return code
        return ""
    
    def translate_assign(self, exp: object) -> str:
        if AssignExp.is_assign_exp(exp):
            fmt = "{} = '{}'"
            name = exp.name
            value = exp.value # TODO: naive, cannot process variable
            code = fmt.format(name, value)
            return code
        return ""
    
    def translate_exit(self, exp: object) -> str:
        if ExitExp.is_exit_exp(exp):
            self.sys_import = True
            fmt = "sys.exit({})"
            if exp.exit_code == None:
                exit_code = ""
            else:
                exit_code = exp.exit_code.str
            code = fmt.format(exit_code)
            return code
        return ""
    
    def translate_echo(self, exp: object) -> str:
        if EchoExp.is_echo_exp(exp):
            fmt = "print({})"
            args: list[str] = map(self.translate_word, exp.args)
            code = fmt.format(", ".join(args))
            return code
        return ""

    def translate_for(self, exp: object, indent: int) -> str:
        if ForExp.is_for_exp(exp):
            fmt = "for {} in {}:\n"
            var = exp.var.str
            iterlist = map(self.translate_word, exp.iter)
            for_header = fmt.format(var, ", ".join(iterlist))
            body = self.translate_sequence(exp.body, indent+1)
            return for_header + body

    def translate_cmd(self, exp: object) -> str:
        if CmdExp.is_cmd_exp(exp):
            self.subprocess_import = True
            fmt = "subprocess.call([{}])"
            args: list[str] = map(self.translate_word, exp.cmd)
            code = fmt.format(", ".join(args))
            return code
        return ""

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
        translator = Translator(stmt)
        code = translator.translate()
        print(code)

def repl_test(filename: str) -> tuple[object, object]:
    with open(filename) as f:
        lexer = Lexer(f.read())
        token = lexer.tokenize()
        parser = Parser(token)
        stmt = parser.parse()
        return (token, stmt)