import sys
import re

token_exprs = [
    #(r'(void|float|int) \w*\([\w*,]*\w\)\{\n\}',	'FUNCTION'),
    (r'[ \n\t]+',              None),
    (r'//[^\n]*\n',          'COMENT'),
    (r"""/\*[^*]*\*+([^/*][^*]*\*+)*/""",              'COMENT'),
    (r'(int|bool|char|string)','DATATYPE'),
    (r'fun',	'FUNCTION'),
    (r'=',                     'EQUAL'),
    (r'\(',                    'OPEN_PARENTHESIS'),
    (r'\)',                    'CLOSE_PARENTHESIS'),
    (r'\[',                    'OPEN_BRACKET'),
    (r'\]',                    'CLOSE_BRACKET'),
    (r'\{',                    'OPEN_KEY'),
    (r'\}',                    'CLOSE_KEY'),
    (r'\,',                    'COMA'),
    (r';',                     'SEMICOLON'),
    (r'\+',                    'PLUS'),
    (r'-',                     'MINUS'),
    (r'\*',                    'MULT'),
    (r'/',                     'DIVISION'),
    (r'<=',                    'LESS_THAN'),
    (r'<',                     'LESS'),
    (r'>=',                    'GREATHER_THAN'),
    (r'>',                     'GREATHER'),
    (r'=',                     'EQUAL'),
    (r'!=',                    'NOT_EQUAL'),
    (r'and',                   'AND'),
    (r'or',                    'OR'),
    (r'not',                   'NOT'),
    (r'if',                    'IF'),
    (r'then',                  'THEN'),
    (r'else',                  'ELSE'),
    (r'while',                 'WHILE'),
    (r'do',                    'DO'),
    (r'end',                   'END'),
    (r'return',                'RETURN'),
    (r'[\d]+\.[\d]+',         'FLOAT'),
    (r'[0|1]{1}',             'BOOL'),
    (r'[0-9]+',                'INT'),
    #(r'\"[\w|\d]{1}\"',        'CHAR'),
    (r'\"[^\"]*\"',              'STRING'),
    (r'[A-Za-z][A-Za-z0-9_]*', 'IDENTIFIER')
]

def lex(characters, token_exprs):
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag:
                    token = (text, tag)
                    #print (text, tag, pos)
                    tokens.append(token)
                break
        if not match:
            sys.stderr.write('[ERROR] Illegal character: %s\n' % characters[pos])
            #sys.exit(1)
            pos = pos + len(characters[pos])
        else:
            pos = match.end(0)
    return tokens

def get_tokens(characters, token_expr):
    return lex(characters,token_expr)

if __name__ == '__main__':
    filename = sys.argv[1]
    file = open(filename)
    characters = file.read()
    file.close()
    tokens = get_tokens(characters,token_exprs)
    for token in tokens:
        print (token)
