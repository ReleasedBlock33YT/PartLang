import argparse
import partlangbackend
import sys

parser = argparse.ArgumentParser(description="PartLang compiler")
parser.add_argument("mode", help="Type of operation. Use 'help' to view all modes.")
parser.add_argument("file", nargs='?', default=None, help="Input file")
parser.add_argument("out", nargs='?', default=None ,help="Output file - Used for 'compile' mode")

args = parser.parse_args()

if (args.mode == "help"):
	print("Available modes:")
	print("  help       Show this help message")
	print("  compile    Compile PartLang source code")
	print("  Vcompile   Compile PartLang source code with verbose logging")
	print("  run        Execute PartLang source code directly")
	sys.exit(0)

# "Compile" requires an output file
# "Run" only needs input file, so "out" needs to be optional
# Mode 'functions' will be called to handle each operation - uses different file 'backend'
if (args.mode == "run"):
	partlangbackend.runProgram(args.file)
elif (args.mode == "compile"):
	if (args.out is None):
		print("Error: Output file must be specified for 'compile' mode.")
		sys.exit(1)
	elif (args.file is None):
		print("Error: Input file must be specified for 'compile' mode.")
		sys.exit(1)
	partlangbackend.compileProgram(args.file, args.out)
elif (args.mode == "Vcompile"):
	if (args.out is None):
		print("Error: Output file must be specified for 'Vcompile' mode.")
		sys.exit(1)
	elif (args.file is None):
		print("Error: Input file must be specified for 'compile' mode.")
		sys.exit(1)
	partlangbackend.compileProgram(args.file, args.out, True)