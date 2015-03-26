#symbol table

symtab={}
h=''

#Get line number from fun_var_declr.py
def setLine(a):
	global h
	h=a

#Function to add functions in symbol table.
def setDataFunc(fname,ret_type,args):
	print "Inserting into symtab - FUNCTION."
	l = args
	l_length = len(args)
	symtab[fname]=(ret_type,l)

#Function to add variables in symbol table.
def setDataVar(vname,var_type):
	print "Inserting into symtab - VARIABLE."
	for i in vname:
		symtab[i]=var_type

#Printing the symbol table.
def printSymTab(d):
	print "Printing Symtab"
	for x in d:
		if(type(d[x]) is tuple):
			print x, " | ",d[x][0]," | ",d[x][1]
		else:
			print x," | ",d[x]

def getFuncType(func_name):
	if(func_name in symtab):
		return symtab[func_name][0]

#Checking whether the function call meets the parameter list in symtab by checking the types of those variables in symtab.
def checkFunction(fname,args):
	print "Checking function name"
	params_passed = args
	if fname not in symtab.keys():
		print "\nline",h,": ERROR : The function : ",fname," does not exist."
		return
	elif fname in symtab.keys():
		print "Function exists."
		params_symtab = symtab[fname][1]
	
	print "Checking number of parameters"
	if(len(params_symtab)!=len(params_passed)):
		print "\nline",h,": ERROR : The number of parameters do not match. Expected ",len(params_symtab),". Got ",len(params_passed),"."
		return
	else:
		print "Number of parameters correct."
		if(len(params_passed) is not 0):
			print "Checking for parameter mismatch"
			for i in range(0,len(params_passed)):
				print(symtab[params_passed[i]],"------",params_symtab[i])
				if(symtab[params_passed[i]]!=params_symtab[i]):
					print "\nline",h,": ERROR : parameter[",str(i),"] does not match. Expected ",params_symtab[i],". Got ",symtab[params_passed[i]],"."
					return
				else:
					print "Parameter match correct."
					pass 
		else:
			print "No parameters in function"


		
#setDataFunc('Getter','int','int','double','float')
#setDataVar('a','int')
#setDataVar('b','char')
#print('Symbol Table\n')
#printSymTab(symtab)
#checkFunction('Getter','double','double')

