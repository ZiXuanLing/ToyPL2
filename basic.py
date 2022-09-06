
DIGITS = "0123456789"

TT_INT    = "INT"
TT_FLOAT  = "FLOAT"
TT_PLUS   = "PLUS"
TT_MINUS  = "MINUS"
TT_MUL    = "MUL"
TT_DIV    = "DIV"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"

class Error(object):
    def __init__(self, pos_start, pos_end, error_name, detail) -> None:
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.detail = detail
    
    def as_string(self):
        res = f'{self.error_name}: {self.detail}'
        res += f'File {self.pos_start.fn}, line {self.pos_end.ln + 1}'
        return res


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, detail) -> None:
        super().__init__(pos_start, pos_end, "Illegal Character", detail)  


class Tokens(object):
    def __init__(self, type_, value_=None) -> None:
        self.type = type_
        self.value = value_
    
    def __repr__(self) -> str:
        """_summary_ debug

        Returns:
            str: _description_
        """
        if self.value:
            return f"{self.type}: {self.value}"
        return f"{self.type}"
    

class Position(object):
    def __init__(self, idx, ln, col, fn, ftxt) -> None:
        """_summary_

        Args:
            idx (_type_): _description_ 索引
            ln (_type_): _description_ 行号
            col (_type_): _description_ 列号
            fn (function): _description_ 文件名
            ftxt (_type_): _description_ 内容
        """
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt
    
    def advance(self, current_char):
        """_summary_ 读取下一个字符

        Args:
            current_char (_type_): _description_

        Returns:
            _type_: _description_
        """
        self.idx += 1
        self.col += 1
        
        if current_char == '\n':
            self.col = 0
            self.ln += 1
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


class lexer(object):
    def __init__(self, fn, text) -> None:
        """_summary_

        Args:
            fn (function): _description_ 来源
            text (_type_): _description_ 文本
        """
        self.fn = fn  
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text) # 位置
        self.current_char = None # 当前字符
        self.advance()
    
    def advance(self):
        self.pos.advance(self.current_char) # self.pos.idx + 1
        if self.pos.idx < len(self.text):
            self.current_char = self.text[self.pos.idx]
        else:
            self.current_char = None
    
    def make_tokens(self):
        tokens = []
        """
        1. 遍历text
        2. 遍历的过程中，分别判断获取的内容
        """
        while self.current_char != None:
            if self.current_char in (" ", "\t"):
                # 空格或制表符不处理
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Tokens(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Tokens(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Tokens(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Tokens(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Tokens(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Tokens(TT_RPAREN))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start=pos_start, pos_end=self.pos, detail=f"'{char}'")
        return tokens, None
    
    def make_number(self):
        """_summary_ 整数和小数
        """
        num_str = ''
        dot_count = 0 # 小数点个数
        
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count = 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        
        if dot_count == 0:
            return Tokens(TT_INT, int(num_str))
        else:
            return Tokens(TT_FLOAT, float(num_str))
            

def run(fn, text):
    lexer_t = lexer(fn, text)
    tokens, error = lexer_t.make_tokens()
    return tokens, error
