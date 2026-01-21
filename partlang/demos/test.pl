// Testing program made in PartLang
IN sys
VAR A = "Hello, World!"
VAR B = 42
VAR C = 60
VAR D = 10
VAR E = "User1234"
VAR F = 0
VAR G = ""
PRINT A

VOID AddAndPrint
MF B
MF D
B += 1
D -= 1
PRINT D
PRINT B
ENDVOID

// PARAM TEST
VOID SUBCRIBE USER
PRINT USER
PRINT "Thanks for subscribing!"
ENDVOID

VOID HI USER ACCOUNT
PRINT USER
PRINT "Thanks for subscribing!"
PRINT "Account: "
PRINT ACCOUNT
ENDVOID

// RET test
VOID RETEST PARA
MF G
IF PARA == 5
G = "PARA IS 5"
RET "PARA IS 5"
ENDIF
G = "PARA IS NOT 5"
RET "PARA IS NOT 5"
// Keep 'ENDVOID' for consistency
ENDVOID

// WHILE test
WHILE D > 0
CALL AddAndPrint
ENDWHILE

CALL SUBCRIBE "ChatGPT"
CALL HI "ChatGPT" E

CALL RETEST F
PRINT G
CALL RETEST 5
PRINT G

TRY
PRINT "In TRY block"
THROW "An error occurred"
CATCH
PRINT "In CATCH block"
CCODE sys.exit(1)
ENDTRYCATCH
