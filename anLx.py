import sys
import re

token_exprs = [
    (r'fun',			'FUNCTION'),
    (r'[ \t]+',			None),
    (r'[\n]+',			'ENDLINE'),
    (r'//[^\n]*\n',		None),
    (r"""/\*[^*]*\*+([^/*][^*]*\*+)*/""",              None),
    (r'(int|bool|char|string)','DATATYPE'),
    (r'=',                     'EQUAL'),
    (r':',                     'DOSPUNTOS'),
    (r'\(',                    'OP_PAR'),
    (r'\)',                    'CL_PAR'),
    (r'\[',                    'OP_BRA'),
    (r'\]',                    'CL_BRA'),
    (r'\{',                    'OP_KEY'),
    (r'\}',                    'CL_KEY'),
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
    (r'<>',			'INEQUAL'),
    (r'!=',                    'NOT_EQUAL'),
    (r'TRUE',                  'TRUE'),
    (r'FALSE',                 'FALSE'),
    (r'and',                   'AND'),
    (r'or',                    'OR'),
    (r'not',                   'NOT'),
    (r'if',                    'IF'),
    (r'then',                  'THEN'),
    (r'else',                  'ELSE'),
    (r'while',                 'WHILE'),
    (r'loop',                 'LOOP'),
    (r'do',                    'DO'),
    (r'end',                   'END'),
    (r'new',			'NEW'),
    (r'return',                'RETURN'),
    (r'[0-9]+',                'INT'),
    (r"'[\w|\d]{1}'",          'CHAR'),
    (r'\"[^\"]*\"',            'STRING'),
    (r'[A-Za-z][A-Za-z0-9_]*', 'IDENTIFIER')
]


syntac = {}

syntac['endline'] = 'ENDLINE'
syntac['return'] = 'RETURN'
syntac['open_par'] = 'OP_PAR'
syntac['close_par'] = 'CL_PAR'
syntac['open_bra'] = 'OP_BRA'
syntac['close_bra'] = 'CL_BRA'
syntac['open_key'] = 'OPEN_KEY'
syntac['close_key'] = 'CLOSE_KEY'
syntac['end'] = 'END'
syntac['new'] = 'NEW'
syntac['plus'] = 'PLUS'
syntac['minus'] = 'MINUS'
syntac['mult'] = 'MULT'
syntac['division'] = 'DIVISION'
syntac['greather'] = 'GREATHER'
syntac['less'] = 'LESS'
syntac['equal'] = 'EQUAL'
syntac['inequal'] = 'INEQUAL'
syntac['greather_than'] = 'GREATHER_THAN'
syntac['less_than'] = 'LESS_THAN'
syntac['function'] = 'FUNCTION'
syntac['tipobase'] = 'DATATYPE'
syntac['iden'] = 'IDENTIFIER'
syntac['dospuntos'] = 'DOSPUNTOS'
syntac['coma'] = 'COMA'
syntac['integ'] = 'INT'
syntac['true'] = 'TRUE'
syntac['false'] = 'FALSE'
syntac['endfile'] = 'ENDFILE'
syntac['and'] = 'AND'
syntac['not'] = 'NOT'
syntac['or'] = 'OR'
syntac['if'] = 'IF'
syntac['else'] = 'ELSE'
syntac['while'] = 'WHILE'
syntac['loop'] = 'LOOP'
syntac['char'] = 'CHAR'
syntac['string'] = 'STRING'
syntac['boolean'] = [ ['true'], ['false'] ]
#syntac['endline'] = [ ['nl'], ['nl','endline'] ]
syntac['tipo'] = [ ['tipobase'], ['open_bra', 'close_bra','tipo'] ]
syntac['operador'] = [ ['plus'], ['minus'], ['mult'], ['division'], ['greather'], ['less'], ['greather_than'], ['less_than'], ['equal'], ['inequal'], ['and'], ['or'] ]
syntac['param'] = [ ['iden','dospuntos','tipo'] ] #<- verificar
syntac['params'] = [ ['param'], ['param', 'coma', 'params'] ]
syntac['params2'] = [ ['open_par','close_par'], ['open_par', 'params', 'close_par'] ]
syntac['listexp'] = [ ['exp', 'listexp'], ['exp'] ]
syntac['chamada'] = [ ['iden', 'open_par', 'listexp', 'close_par'], ['iden', 'open_par', 'close_par'] ]
syntac['declvars'] = [ ['param', 'endline', 'declvars'], ['param', 'endline'] ]
#syntac['declvars2'] = [ ['declvars', 'endline'] ]
#syntac['var2'] = [ ['iden'], ['var2', 'open_bra', 'exp', 'close_bra'] ]
syntac['var'] = [ ['iden', 'open_bra', 'exp', 'close_bra'], ['iden', 'var'], ['iden'] ]
syntac['exp2'] = [ ['integ'],
			['boolean'],
			['char'],
			['string'],
			['new', 'opeb_bra', 'exp2', 'close_bra', 'tipo'], 
			['open_par', 'exp', 'close_par'],
			['not', 'exp'],
			['minus', 'exp'],
			['chamada'] ]
syntac['exp'] = [ ['exp2', 'operador','exp'], ['exp2'] ]
syntac['cmdreturn'] = [ ['return'], ['return', 'exp'] ]
syntac['cmdatrib'] = [ ['var', 'equal', 'exp'] ]
syntac['cmdelseif'] = [ ['else', 'if', 'exp', 'endline', 'bloco'] ]
syntac['cmdif'] = [ ['if', 'exp', 'endline', 'bloco', 'else', 'endline', 'bloco', 'end'],
			['if', 'exp', 'endline', 'bloco', 'cmdelseif', 'else', 'endline', 'bloco', 'end'],
			['if', 'exp', 'endline', 'bloco', 'end'] ]
syntac['cmdwhile'] = [ ['while', 'exp', 'endline', 'bloco', 'loop'] ]
syntac['comando'] = [ ['chamada'], ['cmdif'], ['cmdwhile'], ['cmdatrib'], ['cmdreturn'] ]#, ['chamada'] ]
syntac['comando2'] = [ ['comando', 'endline', 'comando2'], ['comando','endline'] ]
syntac['func'] = [ ['function', 'iden', 'params2', 'dospuntos', 'tipo', 'endline', 'end','endline'], ['function', 'iden', 'params2', 'dospuntos', 'tipo', 'endline', 'bloco', 'end','endline'] ]
#syntac['mini02'] = [ ['endline','decl', 'mini0'], ['decl'], ['decl', 'mini0'] ]
syntac['mini0'] = [ ['endline', 'decls'], ['decls'] ]
#syntac ['mini02'] = [ ['mini0', 'mini02'], ['mini0'] ]
syntac['bloco'] = [['declvars', 'comando2'], ['declvars'], ['comando2']]
syntac['decl'] = [ ['gl'], ['func']]
syntac['decls'] = [ ['decl', 'decls'], ['decl', 'endfile'] ]
syntac['gl'] = [ ['iden','dospuntos','tipo','endline'] ]

def getTop(sL):
    return sL[len(sL)-1]

def getTok(top):
    return syntac[top[0]][top[1]][top[2]] 

def isValidTok(top):
    if (top[2]<len(syntac[top[0]][top[1]])):
       return True
    return False

def isValidCl(top):
    if (top[1]<len(syntac[top[0]])):
       return True
    return False

def isEnd(top):
    if(isinstance(syntac[top[0]], str)):
         return True
    return False

def getNext(top):
    return [getTok(top), 0, 0, top[3]]

def addToNextEnd(sL, pos):
    top = getTop(sL)
    while (isEnd(top)==False):
        top = getNext(top)
        top[3] = pos
        sL.append(top)
    return sL

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
            #print (match)
    token = ('', 'ENDFILE')
    tokens.append (token)
    return tokens

def syn(tokens):
	sL = []
	first = ['mini0', 0, 0, -1]
	sL.append(first)
	addToNextEnd(sL, 0)
	finalStruct = {}
	i = 0 
	it = 0
	maxToken = -1
	existNext = True
	while (i < len(tokens) ):
		token = tokens[i]
		text, tag = token
		top = sL.pop()
		if(syntac[top[0]] == tag):
			if (maxToken<i):
				maxToken = i
			finalStruct[i] = tag
			top = sL.pop()
			top[2] = top[2] + 1
			if (tag=='ENDFILE'):
				break;
			while (isValidTok(top)==False):
				top = sL.pop()
				top[2] = top[2] + 1
				#print (':')
				#print (sL)
					
                        #top[3] = i
                        sL.append (top)
			finalStruct[top[3]] = top[0]
			sL = addToNextEnd(sL, i)
			i = i + 1
		else:
			esperado = top[0]
			top = sL.pop()
			top[1] = top[1] + 1
			while (existNext and isValidCl(top)==False):
				if (len(sL)>1):
					top = sL.pop()
					top[1] = top[1] + 1
				else:
					existNext = False
			if (existNext == False):
				break;
			else:
				top[2] = 0
				sL.append (top)
				sL = addToNextEnd(sL, top[3])
				i = top[3] + 1
		it = it+1
	if (existNext==False):
		print ("\n ERROR:")
		print ("error en token:")
		print (tokens[maxToken+1])
		print ("")
		print (finalStruct)
	else:
		print ("\n Analisis sintactico correcto")
		print (finalStruct)

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
    syn(tokens)
