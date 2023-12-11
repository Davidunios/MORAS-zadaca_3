def _parseMacros(self):
    macros = self._findMacros()
    if not self._flag:
        return

    whiles = len([x for x in macros if x[0] == "$WHILE"])
    ends = len([x for x in macros if x[0] == "$END"])
    
    self._whileCount = whiles
    self._whileCounter = 0
    self._whileStack = []
    self._offset = 0
    
    if whiles != ends:
        self._flag = False
        self._line = -1
        self._errm = "Unclosed while blocks or too many end blocks" 
        return

    changes = [self._handleMacro(macro) for macro in macros]
    if not len(changes):
        return
    
    
    for (change, idx) in changes:
        index = idx + self._offset
        self._lines[index] = (change[0], index, -1)            
        for i in range(1, len(change)):
            self._lines.insert(index + i, (change[i], index + i, -1))

        self._offset += len(change) - 1
    
def _handleMacro(self, macro):
    (macroName, idx, args) = macro
    
    if macroName == "$MV":
        return ([
            f"@{args[0]}",
            "D=M",
            f"@{args[1]}",
            "M=D"
        ], idx)

    if macroName == "$SWP":
        return ([
            f"@{args[0]}",
            "D=M",
            f"@SWAP_MACRO_TEMP",
            "M=D",
            f"@{args[1]}",
            "D=M",
            f"@{args[0]}",
            "M=D",
            f"@SWAP_MACRO_TEMP",
            "D=M",
            f"@{args[1]}",
            "M=D",
        ], idx)

    if macroName == "$SUM":
        return ([
            f"@{args[0]}",
            "D=M",
            f"@{args[1]}",
            "D=D+M",
            f"@{args[2]}",
            "M=D",
        ], idx)

    if macroName == "$WHILE":
        changes = ([
            f"(WHILE_MACRO_{self._whileCounter})",
            f"@{args[0]}",
            "D=M",
            f"@END_MACRO_{self._whileCounter}",
            "D;JEQ"
        ], idx)

        self._whileStack.append(self._whileCounter)
        self._whileCounter += 1
        return changes

    if macroName == "$END":
        end_number = self._whileStack.pop()

        return ([
            f"@WHILE_MACRO_{end_number}",
            "0;JMP",
            f"(END_MACRO_{end_number})"
        ], idx)
    
    self._flag = False
    self._line = b
    self._errm = "Uknown macro " + macroName 
    return
        
def _findMacros(self):
    macros = []
    for i in range(len(self._lines)):
        (line, p, o) = self._lines[i]

        if line[0] != '$':
            continue

        if line == "$END":
            macros.append(('$END', i, []))
            continue

        if '(' not in line:
            self._flag = False
            self._line = i
            self._errm = "Missing macro bracket" + line
            return []

        if ')' not in line:
            self._flag = False
            self._line = i
            self._errm = "Missing macro bracket" + line
            return []

        if line.count('(') > 1:
            self._flag = False
            self._line = i
            self._errm = "Invalid macro syntax (" + "(".join(line.split('(')[2:])
            return []
            
        if line.count(')') > 1:
            self._flag = False
            self._line = i
            self._errm = "Invalid macro syntax )" + ")".join(line.split(')')[2:])
            return []

        obracket = line.index('(')
        cbracket = line.index(')')

        if cbracket < obracket:
            self._flag = False
            self._line = i
            self._errm = "Invalid macro syntax " + line[cbracket:]
            return []

        macroName = line[:obracket]
        args = line[obracket + 1:cbracket].split(',')

        if macroName == "$MV":
            if len(args) != 2:
                self._flag = False
                self._line = i
                self._errm = "Invalid macro argument count " + line
                return []

            macros.append((macroName, i, args))

        elif macroName == "$SWP":
            if len(args) != 2:
                self._flag = False
                self._line = i
                self._errm = "Invalid macro argument count " + line
                return []

            macros.append((macroName, i, args))

        elif macroName == "$SUM":
            if len(args) != 3:
                self._flag = False
                self._line = i
                self._errm = "Invalid macro argument count " + line
                return []

            macros.append((macroName, i, args))

        elif macroName == "$WHILE":
            if len(args) != 1:
                self._flag = False
                self._line = i
                self._errm = "Invalid macro argument count " + line
                return []

            macros.append((macroName, i, args))
        else:
            self._flag = False
            self._line = i
            self._errm = "Unknown macro " + line

    return macros
        

def _parseMacro(self):
    pass
