#!/usr/bin/python3 -u
import sys
import re

t_SHEBANG = r'#!/bin/dash\n'
t_COMMENT = r'(#.*)\n'
t_SQUOTE = r'\'([^\']*)\''
t_DQUOTE = r'"([^"]*)"'
t_NEWLINE = r'\n'
t_ASSIGN = r'(\w+)=(\S+)'
t_VAR = r'\$(\w+)'
t_VARCURLY = r'\${(\w+)}'
t_WORD = r'(\S+)'
t_EMPTY = r'\s+'

test_str_cmp_operators = ["=", "!="]
test_file_access_operators = ["-r", "-w", "-x"]

def eprint(*args, **kwargs) -> None:
    #print(*args, file=sys.stderr, **kwargs)
    pass

def eeprint(*args, **kwargs) -> None:
    print(*args, file=sys.stderr, **kwargs)
    pass

def is_glob_str(s: str) -> bool:
    if '*' in s or '?' in s or '[' in s or ']' in s:
        return True
    return False

class Token:
    pass

class Word(Token):
    def __init__(self, str: str) -> None:
        super().__init__()
        self.str = str
    
    def is_word(obj: object) -> bool:
        return isinstance(obj, Word)
    
    def is_word_with(obj: object, str: str) -> bool:
        if not Word.is_word(obj):
            return False
        elif obj.str == str:
            return True
        return False

class Comment(Token):
    def __init__(self, content: str) -> None:
        super().__init__()
        self.content = content
    
    def is_comment(obj: object) -> bool:
        return isinstance(obj, Comment)

class SQuote(Word):
    def __init__(self, str: str, content: str) -> None:
        super().__init__(str)
        self.content = content

    def is_squote(obj: object) -> bool:
        return isinstance(obj, SQuote)

class DQuote(Word):
    def __init__(self, str: str, content: str) -> None:
        super().__init__(str)
        self.content = content

    def is_dquote(obj: object) -> bool:
        return isinstance(obj, DQuote)

class Newline(Token):
    def __init__(self) -> None:
        super().__init__()

    def is_newline(obj: object) -> bool:
        return isinstance(obj, Newline)

class Assign(Word):
    def __init__(self, str: str, name: str, value: str) -> None:
        super().__init__(str)
        self.name = name
        self.value = value
    
    def is_assign(obj: object) -> bool:
        return isinstance(obj, Assign)

class Var(Word):
    def __init__(self, str: str, name: str) -> None:
        super().__init__(str)
        self.name = name
    
    def is_var(obj: object) -> bool:
        return isinstance(obj, Var)

class Lexer:
    def __init__(self, input: str) -> None:
        self.input: str = input
        self.token: list[Token] = []
    
    def tokenize(self) -> list[Token]:
        self.shebang()
        while True:
            if self.lex_comment():
                continue
            elif self.lex_squote():
                continue
            elif self.lex_dquote():
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

    def shebang(self) -> None:
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
    
    def lex_dquote(self) -> bool:
        m = re.search(t_DQUOTE, self.input)
        if m == None:
            return False
        elif m.span()[0] == 0:
            self.token.append(DQuote(m.group(0), m.group(1)))
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
        
    def cut(self, span: tuple[int, int]) -> None:
        self.input = self.input[span[1]:]

class Typ:
    pass

class WordTyp(Typ):
    pass

class ListTyp(Typ):
    pass

class Exp:
    pass

class NewlineExp(Exp):
    def __init__(self) -> None:
        super().__init__()

    def is_newline_exp(obj: object) -> bool:
        return isinstance(obj, NewlineExp)

class CommentExp(Exp):
    def __init__(self, content: str) -> None:
        super().__init__()
        self.content = content

    def is_comment_exp(obj: object) -> bool:
        return isinstance(obj, CommentExp)

class ListExp(Exp):
    def __init__(self, list: list[tuple[Exp, Typ]]) -> None:
        super().__init__()
        self.list = list

    def is_list_exp(obj: object) -> bool:
        return isinstance(obj, ListExp)

class GlobExp(Exp):
    def __init__(self, str: str, typ: Typ) -> None:
        super().__init__()
        self.str = str
        self.typ = typ

    def is_glob_exp(obj: object) -> bool:
        return isinstance(obj, GlobExp)

class FormatExp(Exp):
    def __init__(self, list: list[Word]) -> None:
        super().__init__()
        self.list = list
    
    def is_format_exp(obj: object) -> bool:
        return isinstance(obj, FormatExp)

class AssignExp(Exp):
    def __init__(self, name: str, value: Exp, typ: Typ) -> None:
        super().__init__()
        self.name = name
        self.value = value
        self.typ = typ
    
    def is_assign_exp(obj: object) -> bool:
        return isinstance(obj, AssignExp)

class CdExp(Exp):
    def __init__(self, dir: Word) -> None:
        super().__init__()
        self.dir = dir
    
    def is_cd_exp(obj: object) -> bool:
        return isinstance(obj, CdExp)

class ExitExp(Exp):
    def __init__(self, exit_code: Word) -> None:
        super().__init__()
        self.exit_code = exit_code

    def is_exit_exp(obj: object) -> bool:
        return isinstance(obj, ExitExp)

class ReadExp(Exp):
    def __init__(self, arg: Word) -> None:
        super().__init__()
        self.arg = arg

    def is_read_exp(obj: object) -> bool:
        return isinstance(obj, ReadExp)

class EchoExp(Exp):
    def __init__(self, args: list[Word]) -> None:
        super().__init__()
        self.args = args

    def is_echo_exp(obj: object) -> bool:
        return isinstance(obj, EchoExp)

class ForExp(Exp):
    def __init__(self, var: Word, iter: list[Word], body: list[object]) -> None:
        super().__init__()
        self.var = var
        self.iter = iter
        self.body = body

    def is_for_exp(obj: object) -> bool:
        return isinstance(obj, ForExp)

class TestExp(Exp):
    def __init__(self) -> None:
        super().__init__()

    def is_test_exp(obj: object) -> bool:
        return isinstance(obj, TestExp)

class FileAccessTestExp(TestExp):
    def __init__(self, op: Word, file: Word) -> None:
        super().__init__()
        self.op = op
        self.file = file

    def is_file_access_test_exp(obj: object) -> bool:
        return isinstance(obj, FileAccessTestExp)

class CmpTestExp(TestExp):
    def __init__(self, op: Word, lhs: Word, rhs: Word) -> None:
        super().__init__()
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def is_cmp_test_exp(obj: object) -> bool:
        return isinstance(obj, CmpTestExp)

class IfExp(Exp):
    def __init__(self, pred: list[TestExp], branch: list[list[object]]) -> None:
        super().__init__()
        self.pred = pred
        self.branch = branch

    def is_if_exp(obj: object) -> bool:
        return isinstance(obj, IfExp)

class WhileExp(Exp):
    def __init__(self, pred: TestExp, body: list[object]) -> None:
        super().__init__()
        self.pred = pred
        self.body = body

    def is_while_exp(obj: object) -> bool:
        return isinstance(obj, WhileExp)

class CmdExp(Exp):
    def __init__(self, cmd: list[Word]) -> None:
        super().__init__()
        self.cmd = cmd

    def is_cmd_exp(obj: object) -> bool:
        return isinstance(obj, CmdExp)

class Parser:
    def __init__(self, token: list[Token]) -> None:
        super().__init__()
        self.token = token
        self.pos = 0
        #self.stmt = []

    def parse(self) -> None:
        stmt = []
        self.parse_sequence(stmt)
        return stmt
    
    def parse_sequence(self, stmt: list[Exp]) -> bool:
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
            elif self.parse_read(stmt):
                eprint("read")
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

    # methods below won't consume token, just detect

    def pos_out_of_range(self) -> bool:
        return self.pos >= len(self.token)
    
    def next_is_comment(self) -> bool:
        if self.pos_out_of_range():
            return False
        if Comment.is_comment(self.token[self.pos]):
            return True
        return False

    def next_is_word(self) -> bool:
        if self.pos_out_of_range():
            return False
        if Word.is_word(self.token[self.pos]):
            return True
        return False

    def next_is_word_with(self, expect: str) -> bool:
        if self.pos_out_of_range():
            return False
        if Word.is_word_with(self.token[self.pos], expect):
            return True
        return False

    def next_is_newline(self) -> bool:
        if self.pos_out_of_range():
            return False
        if Newline.is_newline(self.token[self.pos]):
            return True
        return False

    def next_is_assign(self) -> bool:
        if self.pos_out_of_range():
            return False
        if Assign.is_assign(self.token[self.pos]):
            return True
        return False

    def next_is_terminator(self) -> bool:
        if self.pos_out_of_range():
            return False
        if self.next_is_word_with("done"):
            return True
        if self.next_is_word_with("elif"):
            return True
        if self.next_is_word_with("else"):
            return True
        if self.next_is_word_with("fi"):
            return True
        return False

    # methods below will consume token

    def consume_next_comment(self) -> Comment:
        if self.next_is_comment():
            c = self.token[self.pos]
            self.pos += 1
            return c
        return None

    def consume_next_word(self) -> Word:
        if self.next_is_word():
            word = self.token[self.pos]
            self.pos += 1
            return word
        return None

    def consume_next_word_if_is(self, expect: str) -> bool:
        if self.next_is_word_with(expect):
            self.pos += 1
            return True
        return False

    def consume_next_newline(self) -> bool:
        if self.next_is_newline():
            self.pos += 1
            return True
        return False

    def consume_next_assign(self) -> Assign:
        if self.next_is_assign():
            t = self.token[self.pos]
            self.pos += 1
            return t
        return None

    # parsers below

    def parse_newline(self, stmt: list[Exp]) -> bool:
        if self.consume_next_newline():
            stmt.append(NewlineExp())
            return True
        return False
    
    def parse_comment(self, stmt: list[object]) -> bool:
        # same as above
        if (c := self.consume_next_comment()) != None:
            stmt.append(CommentExp(c.content))
            self.pos += 1
            return True
        return False

    def var_extractor(s: str) -> FormatExp:
        pat = r'\$(\w+|{\w+})'
        it = re.finditer(pat, s)
        prev = 0
        spanlist = []
        isvar = []
        n = 0
        for m in it:
            span = m.span()
            if prev < span[0]:
                spanlist.append((prev, span[0]))
                isvar.append(False)
                n += 1
            spanlist.append((span[0], span[1]))
            isvar.append(True)
            n += 1
            prev = span[1]
        if prev < len(s):
            spanlist.append((prev, len(s)))
            isvar.append(False)
            n += 1
        fmtlist = []
        for i in range(n):
            word = s[spanlist[i][0]:spanlist[i][1]]
            if isvar[i]:
                name = re.sub(r'[${}]', '', word)
                fmtlist.append(Var(word, name))
            else:
                fmtlist.append(Word(word))
        return FormatExp(fmtlist)

    # s must have no white space
    def str_exp_mapper(s: str) -> tuple[Exp, Typ]:
        fmtexp = Parser.var_extractor(s)
        is_glob = False
        for word in fmtexp.list:
            if is_glob_str(word.str):
                is_glob = True
                break
        if is_glob:
            return (GlobExp(fmtexp), ListTyp())
        else:
            return (fmtexp, WordTyp())
    
    def parse_assign(self, stmt: list[Exp]) -> bool:
        if (t := self.consume_next_assign()) != None:
            value = t.value
            typ = None
            value_str_list = re.split(' +', value)
            exp_typ_list = list(map(Parser.str_exp_mapper, value_str_list))
            list_exp = ListExp(exp_typ_list)
            typ = ListTyp
            stmt.append(AssignExp(t.name, list_exp, typ))
            return True
        return False
    
    def parse_cd(self, stmt: list[object]) -> bool:
        if self.consume_next_word_if_is("cd"):
            arg = None
            if (t := self.consume_next_word()) != None:
                arg = t
            stmt.append(CdExp(arg))
            return True
        return False
    
    def parse_exit(self, stmt: list[Exp]) -> bool:
        if self.consume_next_word_if_is("exit"):
            exit_code = None
            if self.next_is_word():
                exit_code = self.consume_next_word()
            stmt.append(ExitExp(exit_code))
            return True
        return False
    
    def parse_read(self, stmt: list[Exp]) -> bool:
        if self.consume_next_word_if_is("read"):
            arg = self.consume_next_word()
            stmt.append(ReadExp(arg))
            return True
        return False
    
    def parse_echo(self, stmt: list[Exp]) -> bool:
        if self.consume_next_word_if_is("echo"):
            args = []
            while (next_arg := self.consume_next_word()) != None:
                args.append(next_arg)
            stmt.append(EchoExp(args))
            return True
        return False
    
    def parse_for(self, stmt: list[Exp]) -> bool:
        bak = (self.pos, stmt)
        # init for-exp fields
        var = None
        iter = []
        body = []
        # for
        if not self.consume_next_word_if_is("for"):
            self.pos, stmt = bak
            return False
        # loop-var
        if (t := self.consume_next_word()) != None:
            var = t
        else:
            self.pos, stmt = bak
            return False
        # in
        if not self.consume_next_word_if_is("in"):
            self.pos, stmt = bak
            return False
        # iterable
        while (t := self.consume_next_word()) != None:
            iter.append(t)
        # newline TODO semicolon
        if not self.consume_next_newline():
            self.pos, stmt = bak
            return False
        # do
        if not self.consume_next_word_if_is("do"):
            self.pos, stmt = bak
            return False
        # newline TODO semicolon
        if not self.consume_next_newline():
            self.pos, stmt = bak
            return False
        # body
        if not self.parse_sequence(body):
            self.pos, stmt = bak
            return False
        # done
        if not self.consume_next_word_if_is("done"):
            self.pos, stmt = bak
            return False
        stmt.append(ForExp(var, iter, body))
        return True

    # TODO only implemented eq test in subset 2
    def parse_pred(self) -> TestExp:
        if (testexp := self.parse_pred_file_access()) != None:
            return testexp
        if (testexp := self.parse_pred_str_cmp()) != None:
            return testexp
        return None

    def parse_pred_file_access(self) -> TestExp:
        bak = self.pos
        # test keyword
        if not self.consume_next_word_if_is("test"):
            self.pos = bak
            return None
        # operator
        operator = None
        if (t := self.consume_next_word()) != None:
            op = t.str
            # check if operator is valid
            if not (op in test_file_access_operators):
                self.pos = bak
                return None
            operator = t
        else:
            self.pos = bak
            return None
        # file
        file = None
        if (t := self.consume_next_word()) != None:
            file = t
        else:
            self.pos = bak
            return None
        # success
        return FileAccessTestExp(operator, file)

    def parse_pred_str_cmp(self) -> TestExp:
        bak = self.pos
        # test keyword
        if not self.consume_next_word_if_is("test"):
            self.pos = bak
            return None
        lhs = None
        # lhs
        if (t := self.consume_next_word()) != None:
            lhs = t
        else:
            self.pos = bak
            return None
        # operator
        operator = None
        if (t := self.consume_next_word()) != None:
            op = t.str
            # check if operator is valid
            if not (op in test_str_cmp_operators):
                self.pos = bak
                return None
            operator = t
        else:
            self.pos = bak
            return None
        # rhs
        rhs = None
        if (t := self.consume_next_word()) != None:
            rhs = t
        else:
            self.pos = bak
            return None
        # success
        return CmpTestExp(operator, lhs, rhs)

    def parse_if(self, stmt: list[Exp]) -> bool:
        bak = (self.pos, stmt)
        # init for-exp fields
        pred = []
        branch = []
        # if
        if not self.consume_next_word_if_is("if"):
            self.pos, stmt = bak
            return False
        # first predicate
        if (test := self.parse_pred()) != None:
            pred.append(test)
        else:
            self.pos, stmt = bak
            return False
        # newline TODO semicolon
        if not self.consume_next_newline():
            self.pos, stmt = bak
            return False
        # then
        if not self.consume_next_word_if_is("then"):
            self.pos, stmt = bak
            return False
        # newline TODO semicolon
        if not self.consume_next_newline():
            self.pos, stmt = bak
            return False
        # first body
        body = []
        if not self.parse_sequence(body):
            self.pos, stmt = bak
            return False
        branch.append(body)
        # elif loop
        while self.consume_next_word_if_is("elif"):
            # predicate
            if (test := self.parse_pred()) != None:
                pred.append(test)
            else:
                self.pos, stmt = bak
                return False
            # newline TODO semicolon
            if not self.consume_next_newline():
                self.pos, stmt = bak
                return False
            # then
            if not self.consume_next_word_if_is("then"):
                self.pos, stmt = bak
                return False
            # newline TODO semicolon
            if not self.consume_next_newline():
                self.pos, stmt = bak
                return False
            # body
            body = []
            if not self.parse_sequence(body):
                self.pos, stmt = bak
                return False
            branch.append(body)
        # else
        if self.next_is_word_with("else"):
            if not self.consume_next_word_if_is("else"):
                self.pos, stmt = bak
                return False
            # newline TODO semicolon
            if not self.consume_next_newline():
                self.pos, stmt = bak
                return False
            # body
            body = []
            if not self.parse_sequence(body):
                self.pos, stmt = bak
                return False
            branch.append(body)
        # fi
        if not self.consume_next_word_if_is("fi"):
            self.pos, stmt = bak
            return False
        stmt.append(IfExp(pred, branch))
        return True
    
    def parse_while(self, stmt: list[Exp]) -> bool:
        bak = (self.pos, stmt)
        # init while-exp fields
        pred = None
        body = []
        # while
        if not self.consume_next_word_if_is("while"):
            self.pos, stmt = bak
            return False
        # predicate
        if (pred := self.parse_pred()) == None:
            self.pos, stmt = bak
            return False
        # newline TODO semicolon
        if not self.consume_next_newline():
            self.pos, stmt = bak
            return False
        # do
        if not self.consume_next_word_if_is("do"):
            self.pos, stmt = bak
            return False
        # newline TODO semicolon
        if not self.consume_next_newline():
            self.pos, stmt = bak
            return False
        # body
        if not self.parse_sequence(body):
            self.pos, stmt = bak
            return False
        # done
        if not self.consume_next_word_if_is("done"):
            self.pos, stmt = bak
            return False
        stmt.append(WhileExp(pred, body))
        return True
    
    def parse_cmd(self, stmt: list[Exp]) -> bool:
        cmd = []
        while self.next_is_word():
            cmd.append(self.consume_next_word())
        stmt.append(CmdExp(cmd))
        return True

class Translator:
    def __init__(self, ast: list[Exp]) -> None:
        self.ast = ast
        self.glob_import = False
        self.os_import = False
        self.subprocess_import = False
        self.sys_import = False

    def translate(self) -> str:
        header = "#!/usr/bin/python3 -u\n"
        body = self.translate_sequence(self.ast)
        if self.glob_import:
            header += "import glob\n"
        if self.os_import:
            header += "import os\n"
        if self.subprocess_import:
            header += "import subprocess\n"
        if self.sys_import:
            header += "import sys\n"
        return header + body
    
    def translate_sequence(self, explist: list[object], indent: int = 0) -> str:
        body = ""
        beginning_of_line = True
        shift_str = indent * 4 * " "
        for exp in explist:
            if beginning_of_line:
                body += shift_str
                beginning_of_line = False
            # TODO insert space between cmd and trailing comment
            # which require another state
            increment = self.translate_newline(exp)
            if increment != "":
                beginning_of_line = True
                body += increment
                continue
            increment = self.translate_comment(exp)
            if increment != "":
                beginning_of_line = True
                body += increment
                continue
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
            increment = self.translate_read(exp)
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
            increment = self.translate_if(exp, indent)
            if increment != "":
                body += increment
                continue
            increment = self.translate_while(exp, indent)
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
    
    def translate_newline(self, exp: Exp) -> str:
        if NewlineExp.is_newline_exp(exp):
            return "\n"
        return ""

    def translate_comment(self, exp: Exp) -> str:
        if CommentExp.is_comment_exp(exp):
            return f"#{exp.content}"
        return ""
    
    # TODO implement word str only
    # check variable as a whole word
    def translate_word(self, word: Word) -> str:
        if SQuote.is_squote(word):
            return word.str
        if DQuote.is_dquote(word):
            return word.str
        if Var.is_var(word):
            name = word.name
            if re.fullmatch(r'\d+', name): # sys.argv[name]
                self.sys_import = True
                return f"sys.argv[{name}]"
            else:
                return name
        return self.translate_word_str(word.str)
    
    # check variable embedded in a word
    def translate_word_str(self, word: str) -> str:
        if '$' in word:
            m = re.search(r'\$(.+)', word)
            if m != None:
                var = "{" + m.group(1) + "}"
                new_content = re.sub(r'\$.+', var, word)
                word = 'f"' + new_content + '"'
                return word
        if is_glob_str(word):
            self.glob_import = True
            return f"sorted(glob.glob(\"{word}\"))"
        #if re.fullmatch(r'\d+', word):
        #    return word
        return f"'{word}'"
    
    def translate_cd(self, exp: Exp) -> str:
        if CdExp.is_cd_exp(exp):
            self.os_import = True
            fmt = "os.chdir({})"
            code = fmt.format(self.translate_word(exp.dir))
            return code
        return ""
    
    def translate_value(self, exp: Exp, typ: Typ = Typ()) -> str:
        if ListExp.is_list_exp(exp):
            elem_str_list = []
            for e, t in exp.list:
                elem_str_list.append(self.translate_value(e, t))
            if len(elem_str_list) == 1:
                return elem_str_list[0]
            else:
                return f"[{', '.join(elem_str_list)}]"
        elif GlobExp.is_glob_exp(exp):
            self.glob_import = True
            return f"sorted(glob.glob(\"{exp.str}\"))"
        elif FormatExp.is_format_exp(exp):
            substrs = []
            for word in exp.list:
                if Var.is_var(word):
                    substrs.append("{" + word.name + "}")
                else:
                    substrs.append(word.str)
            fmt_str_content = "".join(substrs)
            return f'f"{fmt_str_content}"'
    
    def translate_assign(self, exp: Exp) -> str:
        if AssignExp.is_assign_exp(exp):
            fmt = "{} = {}"
            name = exp.name
            #value = self.translate_word_str(exp.value)
            value = self.translate_value(exp.value)
            code = fmt.format(name, value)
            return code
        return ""
    
    def translate_exit(self, exp: Exp) -> str:
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
    
    def translate_read(self, exp: Exp) -> str:
        if ReadExp.is_read_exp(exp):
            self.sys_import = True
            #fmt = "{}sys.stdin.readline().strip()"
            fmt = "{}input()"
            arg = None
            if exp.arg == None:
                arg = ""
            else:
                arg = f"{exp.arg.str} = "
            code = fmt.format(arg)
            return code
        return ""
    
    def translate_echo(self, exp: Exp) -> str:
        if EchoExp.is_echo_exp(exp):
            fmt = "print({})"
            args: list[str] = list(map(self.translate_word, exp.args))
            code = fmt.format(", ".join(args))
            return code
        return ""

    def translate_for(self, exp: Exp, indent: int) -> str:
        if ForExp.is_for_exp(exp):
            fmt = "for {} in {}:\n"
            var = exp.var.str
            iterlist = list(map(self.translate_word, exp.iter))
            for_header = fmt.format(var, ", ".join(iterlist))
            body = self.translate_sequence(exp.body, indent+1)
            return for_header + body
        return ""

    def translate_pred(self, pred: TestExp) -> str:
        if FileAccessTestExp.is_file_access_test_exp(pred):
            self.os_import = True
            code_flag = None
            if pred.op.str == '-r':
                code_flag = "os.R_OK"
            elif pred.op.str == '-w':
                code_flag = "os.W_OK"
            elif pred.op.str == '-x':
                code_flag = "os.X_OK"
            code_file = self.translate_word(pred.file)
            code = "os.access({}, {})".format(code_file, code_flag)
            return code
        if CmpTestExp.is_cmp_test_exp(pred):
            code_op = None
            if pred.op.str == "=":
                code_op = "=="
            else:
                code_op = pred.op.str
            code_lhs = self.translate_word(pred.lhs)
            code_rhs = self.translate_word(pred.rhs)
            code = "{} {} {}".format(code_lhs, code_op, code_rhs)
            return code
        return ""

    def translate_if(self, exp: Exp, indent: int) -> str:
        if IfExp.is_if_exp(exp):
            iffmt = "if {}:\n"
            pred_str = self.translate_pred(exp.pred[0])
            if_header = iffmt.format(pred_str)
            body = self.translate_sequence(exp.branch[0], indent+1)
            code = if_header + body
            eliffmt = "elif {}:\n"
            for i in range(1, len(exp.pred)):
                pred_str = self.translate_pred(exp.pred[i])
                elif_header = eliffmt.format(pred_str)
                body = self.translate_sequence(exp.branch[i], indent+1)
                code += elif_header + body
            if len(exp.branch) > len(exp.pred): # else
                else_header = "else:\n"
                body = self.translate_sequence(exp.branch[-1], indent+1)
                code += else_header + body
            return code
        return ""

    def translate_while(self, exp: Exp, indent: int) -> str:
        if WhileExp.is_while_exp(exp):
            fmt = "while {}:\n"
            pred_str = self.translate_pred(exp.pred)
            header = fmt.format(pred_str)
            body = self.translate_sequence(exp.body, indent+1)
            code = header + body
            return code
        return ""

    def translate_cmd(self, exp: Exp) -> str:
        if CmdExp.is_cmd_exp(exp):
            self.subprocess_import = True
            fmt = "subprocess.call([{}])"
            args: list[str] = list(map(self.translate_word, exp.cmd))
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
        translator = Translator(stmt)
        code = translator.translate()
        print(code)

def repl_test(filename: str) -> tuple[list[Token], list[Exp]]:
    with open(filename) as f:
        lexer = Lexer(f.read())
        token = lexer.tokenize()
        parser = Parser(token)
        stmt = parser.parse()
        return (token, stmt)