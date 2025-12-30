# PartLang

PartLang is a custom programming language that transpiles to Python and can be run or compiled using the same compiler backend.
PartLang was made by a solo developer (me)

## Features
- Functions (`VOID`)
- Parameters
- Control flow (`IF`, `WHILE`)
- Try/Catch (`TRY`, `CATCH`, `THROW`)
- Compiler escape hatches (`CCODE`, `CTHROW`)
- Single-pass compiler
- Shared compile/run pipeline
- Includes a demo PartLang file (`test.pl`)

## Example
```partlang
VOID HI USER
PRINT USER
ENDVOID

CALL HI "ChatGPT"
```

## Demo
Each release includes a test.pl file containing example PartLang code.

To Run a file:
``` batch
python partlang.py run test.pl
```
	
To Compile a file:
Non-verbose:
```batch
python partlang.py compile test.pl test.py
```
	
Verbose:
```batch
python partlang.py Vcompile test.pl test.py
```
		
To show all options:
```batch
python partlang.py help

```
