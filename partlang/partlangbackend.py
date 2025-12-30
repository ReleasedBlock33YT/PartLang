from re import split
import sys

def runProgram(file):
    tempfile = "temp_partlang_output.py"

    try:
        compileProgram(file, tempfile)

        with open(tempfile, 'r') as f:
            code = f.read()

        exec(code, {})

    except FileNotFoundError:
        print(f"Error: Temporary file '{tempfile}' not found. Compilation may have failed.")
        sys.exit(1)

    finally:
        try:
            import os
            if os.path.exists(tempfile):
                os.remove(tempfile)
        except Exception as e:
            print(f"Warning: Could not delete temporary file '{tempfile}'. {e}")

def compileProgram(file, outFile, v=False):
	try:
		with open(file, 'r') as f:
			lines = f.readlines()
			for line in lines:
				parseLine(line, v)
		with open(outFile, 'w') as outF:
			outF.writelines(outputfile)
		
	except FileNotFoundError:
		print(f"Error: File '{file}' not found. Check the file paths, then try again.")
		sys.exit(1)
	return

outputfile = []
funcList = []
varsList = []
inList = []
# States
funcState = False
ifState = False
forState = False
whileState = False
elseState = False
elifState = False
tryState = False
catchState = False

def parseLine(lineInFile, v=False):
	global funcState
	global ifState
	global forState
	global whileState
	global elseState
	global elifState
	global tryState
	global catchState
	global varsList
	global funcList
	global inList

	stripped = lineInFile.strip()

	# Start by checking for comments, these lines will be ignored and will add to the output file.
	if (stripped.startswith("//")):
		x = stripped.replace("//", "#")
		outputfile.append(x + "\n")
		print(stripped) if v else None
		return

	# Next, check for empty lines, since they will just be ignored with "\n" added to the end.
	if (stripped == ""):
		outputfile.append("\n")
		return
	
	# Now, the rest of the syntax
	if (stripped.startswith("IF ")):
		if ifState or forState or whileState or elifState:
			print("PL00002: You are not allowed to have nested blocks, only functions can have these restaiants removed.")
			sys.exit(1)

		ifState = True									# Enable state
		condition = stripped[3:].strip()
		if checkFuncStatus():
			outputfile.append(f"	if {condition}:\n")
		else:
			outputfile.append(f"if {condition}:\n")
		print(stripped) if v else None
		return
	elif (stripped == "ENDIF"):
		if not ifState:
			if not elifState:
				if not elseState:
					print("PL00004: 'ENDIF' without a preceding 'IF', 'ELIF' or 'ELSE'.")
					sys.exit(1)
			elifState = False
		elif ifState:		# Here to make sure there is no errors or anything for python
			ifState = False
		outputfile.append("\n")			# Create newline in file after block
		print(stripped) if v else None
		return
	elif (stripped.startswith("ELIF ")):
		if not ifState:
			print("PL00003: 'ELIF' without a preceding 'IF'.")
			sys.exit(1)
		if forState or whileState or elifState:
			print("PL00002: You are not allowed to have nested blocks, only functions can have these restaiants removed.")
			sys.exit(1)
		ifState = False
		elifState = True
		condition = stripped[5:].strip()
		if checkFuncStatus():
			outputfile.append(f"	elif {condition}:\n")
		else:
			outputfile.append(f"elif {condition}:\n")
		print(stripped) if v else None
		return
	elif (stripped == "ELSE"):
		if not ifState:
			print("PL00005: 'ELSE' without a preceding 'IF'.")
			sys.exit(1)
		if forState or whileState or elifState:
			print("PL00002: You are not allowed to have nested blocks, only functions can have these restaiants removed.")
			sys.exit(1)
		ifState = False if ifState else ifState
		elifState = False if elifState else elifState
		elseState = True
		if checkFuncStatus():
			outputfile.append(f"	else:\n")
		else:
			outputfile.append(f"else:\n")
		print(stripped) if v else None
		return

	if (stripped.startswith("VAR ")):
		varName = stripped[4:].split('=')[0].strip()
		start_index = 4 + len(varName) + 3
		varValue = stripped[start_index:].strip()
		if not varValue:
			print(f"PL00001: Variable must be assigned a value. Use '=' to do so.")
			sys.exit(1)
		
		if checkStates():
			if checkFuncStatus():
				outputfile.append(f"\t\t{varName} = {varValue}\n")
			else:
				outputfile.append(f"\t{varName} = {varValue}\n")
		else:
			if checkFuncStatus():
				outputfile.append(f"\t{varName} = {varValue}\n")
			else:
				outputfile.append(f"{varName} = {varValue}\n")
		print(stripped) if v else None
		varsList.append(varName)
		return

	if (stripped.startswith("PRINT ")):
		toPrint = stripped[6:].strip()
		if checkStates():
			if checkFuncStatus():
				outputfile.append(f"\t\tprint({toPrint})\n")
			else:
				outputfile.append(f"\tprint({toPrint})\n")
		else:
			if checkFuncStatus():
				outputfile.append(f"\tprint({toPrint})\n")
			else:
				outputfile.append(f"print({toPrint})\n")
		print(stripped) if v else None
		return

	if (stripped.startswith("VOID ")):
		if checkStates():
			print("PL10001: Functions are not allowed inside control blocks.")
			sys.exit(1)
		if checkFuncStatus():
			print("PL10002: Nested functions are not allowed.")
			sys.exit(1)

		parts = stripped[5:].strip().split()  # split by spaces
		funcName = parts[0]                   # first word is function name
		params = ", ".join(parts[1:])         # rest are optional params
	
		funcState = True
		funcList.append(funcName)
		outputfile.append(f"def {funcName}({params}):\n")
		print(stripped) if v else None
		return
	elif (stripped == "ENDVOID"):
		if not funcState:
			print("PL10003: 'ENDVOID' without a preceding 'VOID'.")
			sys.exit(1)
		funcState = False
		outputfile.append("\n")			# Create newline in file after function
		print(stripped) if v else None
		return

	if (stripped.startswith("RET")):
		if not funcState:
			print("PL10004: Invalid return statement")
		
		# Handle optional return value
		returnValue = stripped[3:].strip()
		lineToEmit = f"return {returnValue}" if returnValue else "return"

		# Determine indentation based on current states
		indent = "\t\t" if checkStates() else "\t"

		# Python handles order, so it is fine to just append here.
		# Append the properly indented return line
		outputfile.append(f"{indent}{lineToEmit}\n")
		return

	if (stripped.startswith("TRY")):
		# Determine indentation
		indent = "\t" if checkStates() else ""
		if checkFuncStatus():
			indent += "\t"

		outputfile.append(f"{indent}try:\n")
		tryState = True
		print(stripped) if v else None
		return

	if (stripped.startswith("CATCH")):
		if not tryState:
			print("PL20001: 'CATCH' without a preceding 'TRY'.")
			sys.exit(1)

		tryState = False
		# Use the same indentation as the corresponding TRY
		indent = "\t" if checkStates() else ""
		if checkFuncStatus():
			indent += "\t"
		catchState = True

		outputfile.append(f"{indent}except Exception as e:\n")
		print(stripped) if v else None
		return


	if (stripped.startswith("ENDTRYCATCH")):
		if not catchState:
			print("PL20002: 'ENDTRYCATCH' without a preceding 'CATCH'.")
			sys.exit(1)
		catchState = False
		tryState = False
		outputfile.append("\n")			# Create newline in file after block
		print(stripped) if v else None
		return

	if (stripped.startswith("CTHROW ")):
		msg = stripped[7:].strip()
		smsg = msg.strip('"').strip("'")		# Strip quotes for error message display
		if not msg or msg == "":
			print("PL20003: CTHROW requires an error message.")
			sys.exit(1)
		else:
			print(stripped) if v else None
			print(f"UE00001: {smsg}")
			sys.exit(1)

	if (stripped.startswith("CALL ")):
		parts = stripped[5:].strip().split()  # split by spaces
		callName = parts[0]                    # first word is function name
		args = ", ".join(parts[1:])            # rest are optional arguments
	
		lineToEmit = f"{callName}({args})"
	
		if checkStates():
			if checkFuncStatus():
				outputfile.append(f"\t\t{lineToEmit}\n")
			else:
				outputfile.append(f"\t{lineToEmit}\n")
		else:
			if checkFuncStatus():
				outputfile.append(f"\t{lineToEmit}\n")
			else:
				outputfile.append(f"{lineToEmit}\n")

#		testStates(stripped)				# debug, comment out on release

		print(stripped) if v else None
		return


	if stripped.startswith("WHILE "):
		if checkStates():
			print("PL00002: You are not allowed to have nested blocks, only functions can have these restaiants removed.")
			sys.exit(1)
		lhs, rhs, op = splitStatement(stripped[6:].strip(), ["<=", ">=", "==", "!=", "<", ">"])
		if not op or not rhs:
			print(
				"PL00006-1: Invalid WHILE statement. Comparison operator missing or incorrect."
				if not op
				else "PL00006-2: Invalid WHILE statement. Right-hand side of comparison missing."
				if not rhs
				else ""
			)
			sys.exit(1)
		whileState = True
		if checkFuncStatus():
			outputfile.append(f"\twhile {lhs} {op} {rhs}:\n")
		else:
			outputfile.append(f"while {lhs} {op} {rhs}:\n")
	if stripped.startswith("ENDWHILE"):
		if not whileState:
			print("PL00007: 'ENDWHILE' without a preceding 'WHILE'.")
			sys.exit(1)
		whileState = False
		outputfile.append("\n")			# Create newline in file after block
		print(stripped) if v else None
		return

	if stripped.startswith("MF "):
		varName = stripped[3:].split('=')[0].strip()
		if checkStates():
			if checkFuncStatus():
				outputfile.append(f"\t\tglobal {varName}\n")
			else:
				outputfile.append(f"\tglobal {varName}\n")
		else:
			if checkFuncStatus():
				outputfile.append(f"\tglobal {varName}\n")
			else:
				outputfile.append(f"global {varName}\n")
		
		print(stripped) if v else None
		return

	if (stripped.startswith("THROW ")):
		# This will append a raise statement to the output file depending on the argument
		errorMessage = stripped[6:].strip()
		if checkStates():
			if checkFuncStatus():
				outputfile.append(f"\t\traise Exception({errorMessage})\n")
			else:
				outputfile.append(f"\traise Exception({errorMessage})\n")
		else:
			if checkFuncStatus():
				outputfile.append(f"\traise Exception({errorMessage})\n")
			else:
				outputfile.append(f"raise Exception({errorMessage})\n")

		print(stripped) if v else None
		return

	if (stripped.startswith("IN ")):
		packageName = stripped[3:].strip()
		# Imports can't be in control blocks or functions, but logic will be here to error if so.
		if checkStates() or checkFuncStatus():
			print("PL30001: Imports must be at the top level, outside of functions or control blocks.")
			sys.exit(1)
		outputfile.append(f"import {packageName}\n")
		inList.append(packageName)
		print(stripped) if v else None
		return

	if (stripped.startswith("CCODE ")):
		customCode = stripped[6:].strip()
		if checkStates():
			if checkFuncStatus():
				outputfile.append(f"\t\t{customCode}\n")
			else:
				outputfile.append(f"\t{customCode}\n")
		else:
			if checkFuncStatus():
				outputfile.append(f"\t{customCode}\n")
			else:
				outputfile.append(f"{customCode}\n")

		print(stripped) if v else None
		return

	for var in varsList:
		if stripped.startswith(var + " ="):
			varValue = stripped[len(var) + 2:].strip()
			if checkStates():
				if checkFuncStatus():
					outputfile.append(f"\t\t{var} = {varValue}\n")
				else:
					outputfile.append(f"\t{var} = {varValue}\n")
			else:
				if checkFuncStatus():
					outputfile.append(f"\t{var} = {varValue}\n")
				else:
					outputfile.append(f"{var} = {varValue}\n")
			return
		if stripped.startswith(var + " +="):
			varValue = stripped[len(var) + 3:].strip()
			if checkStates():
				if checkFuncStatus():
					outputfile.append(f"\t\t{var} += {varValue}\n")
				else:
					outputfile.append(f"\t{var} += {varValue}\n")
			else:
				if checkFuncStatus():
					outputfile.append(f"\t{var} += {varValue}\n")
				else:
					outputfile.append(f"{var} += {varValue}\n")
			return
		if stripped.startswith(var + " -="):
			varValue = stripped[len(var) + 3:].strip()
			if checkStates():
				if checkFuncStatus():
					outputfile.append(f"\t\t{var} -= {varValue}\n")
				else:
					outputfile.append(f"\t{var} -= {varValue}\n")
			else:
				if checkFuncStatus():
					outputfile.append(f"\t{var} -= {varValue}\n")
				else:
					outputfile.append(f"{var} -= {varValue}\n")
			return
		if stripped.startswith(var + " *="):
			varValue = stripped[len(var) + 3:].strip()
			if checkStates():
				if checkFuncStatus():
					outputfile.append(f"\t\t{var} *= {varValue}\n")
				else:
					outputfile.append(f"\t{var} *= {varValue}\n")
			else:
				if checkFuncStatus():
					outputfile.append(f"\t{var} *= {varValue}\n")
				else:
					outputfile.append(f"{var} *= {varValue}\n")
			return
		if stripped.startswith(var + " /="):
			varValue = stripped[len(var) + 3:].strip()
			if checkStates():
				if checkFuncStatus():
					outputfile.append(f"\t\t{var} /= {varValue}\n")
				else:
					outputfile.append(f"\t{var} /= {varValue}\n")
			else:
				if checkFuncStatus():
					outputfile.append(f"\t{var} /= {varValue}\n")
				else:
					outputfile.append(f"{var} /= {varValue}\n")
			return
		print(stripped) if v else None

def checkStates():
	return True if ifState or forState or whileState or elseState or elifState or tryState or catchState else False

def checkFuncStatus():
	return True if funcState else False

def splitStatement(statement, operators):
	for op in sorted(operators, key=len, reverse=True):
		if op in statement:
			parts = statement.split(op, 1)
			lstatement = parts[0].strip()
			rstatement = parts[1].strip()
			return lstatement, rstatement, op
	return statement.strip(), None, None

def setAllStatesTo(value):
	global funcState
	global ifState
	global forState
	global whileState
	global elseState
	global elifState
	funcState = value
	ifState = value
	forState = value
	whileState = value
	elseState = value
	elifState = value
	return

def testStates(stripped):
	# DEBUG: Check states and print them
	print("")
	print(str(stripped))		# You never know if "stripped" is a string or not....
	print(str(funcState))
	print(str(ifState))
	print(str(forState))
	print(str(whileState))
	print(str(elseState))
	print(str(elifState))
	print("")