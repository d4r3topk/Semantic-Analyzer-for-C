import ply.lex as lex
import ply.yacc as yacc
import symtab
import re

d = {}

tokens = ['LPAREN','RPAREN','TYPE','SEP','ID','EQ','VAL']

l = []
lst = []
var_lst = []
call_lst = []
xtype = ''
val = ''
func_type = ''
line=0

def t_TYPE(t):
	r"(int|double|float|void|char)"
	global xtype
	xtype = str(t.value)
	return t

def t_ID(t):
	r"[a-zA-Z_]\w*\d*\_*"
	return t

def t_VAL(t):
	r"(\d+.?\d*)|(\'[a-zA-Z0-9]\')"
	global val
	if(re.match(r'\d+$',t.value)):
		val='int'
	elif(re.search(r'\d+.?\d*$',t.value)):
		val='float' #'double'
	elif(re.search(r'(\'[a-zA-Z0-9]\')',t.value)):
		val='char'

	return t

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_SEP = r"\,"
t_EQ = r"\="
t_ignore = " \t\n" 
func = ''

def t_error(t):
	print "Illegal character"
	print t.value
	t.lexer.skip(1)
	return t

#The grammar to match the sub section of semantic checks implemented
def p_declr(p):
	'''expr :	func_declr
					| var_declr
					| func_call
					| var_assign
					| func_call_assign'''
	return p


#To check for assignment of function call to variable
#Eg : int a = func()
def p_func_call_assign(p):
	'''func_call_assign : TYPE ID EQ func_call
											|	no_dec_func_call_assign'''
	global xtype
	global func_type
	if(func_type == 'void'):
		print "Function returns void! Can't assign"
	elif(func_type == xtype):
		print "Function call assignment match!"
	else:
		print "Type mismatch for assigning function return value"
	return p

#If the variable has already been declared
#Eg : a = func()
def p_no_dec_func_call_assign(p):
	'no_dec_func_call_assign : ID EQ func_call'
	global xtype
	if(xtype == ''):
		xtype = symtab.symtab[p[1]]
	return p

#To match assignment of variables to value
#Eg : int a = 40
def p_var_assign(p):
	'''var_assign : TYPE ID EQ VAL
								| no_dec_assign'''
	global xtype
	global val
	if(xtype == val):
		print "Correct semantics for variable assignment"	
	else:
		print "Incorrect semantics"
	return p

#If the variable has already been declared
#Eg : a = 40
def p_no_dec_assign(p):
	'no_dec_assign : ID EQ VAL'
	global xtype
	global val
	if(xtype == ''):
		xtype = symtab.symtab[p[1]]
	return p

#To match function call
#Eg func(a,b)
def p_func_call(p):
	'''func_call : ID LPAREN call_arg_list RPAREN
							 | ID LPAREN RPAREN'''
	global call_lst
	global func_type
	func_type = symtab.getFuncType(p[1])
	symtab.checkFunction(p[1],call_lst)
	return p

#To match arg list passed into function call
#Eg func(a,b,c)
def p_call_arg_list(p):
	'''call_arg_list : ID SEP call_arg_list
										| ID'''
	global call_lst
	call_lst.append(p[1])
	return p

#To match funcition declaration
#void func(int, int)
def p_func_declr(p):
	'''func_declr : TYPE ID LPAREN arg_list RPAREN
							|	TYPE ID LPAREN RPAREN'''
	global lst
	d[str(p[2])] = {'return_type':p[1],'arg_list':lst}
	symtab.setDataFunc( str(p[2]), d[str(p[2])]['return_type'], d[str(p[2])]['arg_list'] )
	symtab.printSymTab(symtab.symtab)
	lst = []
	return p

#To match argument list for funciton declaration
#void func(int,flot,char)
def p_arg_list(p):
	'''arg_list : TYPE SEP arg_list
							 | TYPE'''
	global lst
	lst.append(p[1])
	return p

#To match declaration of variables
#int a
def p_assign(p):
	'var_declr : TYPE id_list'
	global var_lst
	symtab.setDataVar(var_lst,p[1])
	var_lst = []
	symtab.printSymTab(symtab.symtab)
	return p

#ID List of variable declaration
#int a,b,c
def p_id_list(p):
	'''id_list : ID SEP id_list
					 | ID'''
	#Do something
	global var_lst
	var_lst.append(p[1])
	return p

#Error function
def p_error(p):
	if p:
		pass

lexer = lex.lex()
parser = yacc.yacc()
file1 = open('something.c','r')
for i in file1:
	line+=1
	symtab.setLine(str(line))
        parser.parse(i)
        print '-'*30
