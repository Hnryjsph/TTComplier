import enum
import sys


class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # Operators.
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211


class Token:
    def __init__(self, tokenText: str, tokenKind: TokenType):
        self.text = tokenText
        self.kind = tokenKind

    @staticmethod
    def checkIfKeyword(tokenText) -> TokenType | None:
        for kind in TokenType:
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source  # This is the source code of the language
        self.curChar = ''  # Current character
        self.curPos = -1  # current position in the string
        self.nextChar()

    # Process the next Character
    def nextChar(self) -> str:
        # Goes to the next char and shows that we have reached theb end of the source code
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = "\0"  # EOF (Have reached the end of the source code)
        else:
            self.curChar = self.source[self.curPos]

    # Returns the lookahead character
    def peek(self) -> str:
        # Look at the last character and return it only if the next position is not beyond
        # The len of the source
        if self.curPos + 1 >= len(self.source):
            return "\0"

        return self.source[self.curPos + 1]

    # Invalid token found print error message and exit
    def abort(self, message: str) -> None:
        sys.exit("Lexing error: " + message)

    # Skip whitespace except newLines, which we will use to indicate of a statement

    def skipWhiteSpace(self) -> None:
        while self.curChar == " " or self.curChar == '\t' or self.curChar == 'r':
            self.nextChar()

    def getToken(self) -> Token:

        self.skipWhiteSpace()
        self.skipComments()

        token = None

        if self.curChar == "+":
            token = Token(self.curChar, TokenType.PLUS)

        elif self.curChar == "-":
            token = Token(self.curChar, TokenType.MINUS)

        elif self.curChar == "*":
            token = Token(self.curChar, TokenType.ASTERISK)

        elif self.curChar == "/":
            token = Token(self.curChar, TokenType.SLASH)

        elif self.curChar == "\n":
            token = Token(self.curChar, TokenType.NEWLINE)

        elif self.curChar == "\0":
            token = Token("", TokenType.EOF)

        elif self.curChar == "=":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)

            else:
                token = Token(self.curChar, TokenType.EQ)

        elif self.curChar == ">":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()

                token = Token(lastChar + self.curChar, TokenType.GTEQ)

            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == "<":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()

                token = Token(lastChar + self.curChar, TokenType.LTEQ)

            else:
                token = Token(self.curChar, TokenType.LT)

        elif self.curChar == "!":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()

                token = Token(lastChar + self.curChar, TokenType.NOTEQ)

            else:
                self.abort("Expected !=, got !" + self.peek())

        elif self.curChar == '\"':
            # Get the characters bettween quotations
            special_character = ['\r', '\n', '\t', '\\', '%']
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\"':
                # I wont allow special characters in the string like newline

                if self.curChar in special_character:
                    self.abort("Illegal characters in the string")
                self.nextChar()
            tokText = self.source[startPos: self.curPos]

            token = Token(tokText, TokenType.STRING)

        elif self.curChar.isdigit():
            startPos = self.curPos

            while self.peek().isdigit():
                self.nextChar()

            if self.peek() == ".":
                self.nextChar()

                if not self.peek().isdigit():
                    self.abort("Illegal character in number")

                while self.peek().isdigit():
                    self.nextChar()

            tokText = self.source[startPos: self.curPos + 1]
            token = Token(tokText, TokenType.NUMBER)

        elif self.curChar.isalpha():
            startPos = self.curPos

            while self.peek().isalnum():
                self.nextChar()

            tokText = self.source[startPos: self.curPos + 1]
            keyword = Token.checkIfKeyword(tokText)

            if keyword == None:
                token = Token(tokText, TokenType.IDENT)
            else:
                token = Token(tokText, keyword)

        else:
            # For an unknown token
            self.abort("Unkown Token: " + self.curChar)

        self.nextChar()
        return token

    def skipComments(self) -> None:
        if self.curChar == "#":
            while self.curChar != "\n":
                self.nextChar()
