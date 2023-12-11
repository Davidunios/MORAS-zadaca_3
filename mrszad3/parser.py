
class Parser:
    from parseLines import _parse_lines, _parse_line
    from parseComms import _parse_commands, _parse_command, _init_comms
    from parseSymbs import _parse_symbols, _parse_labels, _parse_variables, _init_symbols
    from parseMacros import _parseMacro, _parseMacros, _handleMacro, _findMacros
    
    def __init__(self, filename):
       
        try:
            self._file = open(filename + ".asm", "r")
        except:
            Parser._error("File", -1, "Cannot open source file")
            return

        self._lines = []
       
        try:
            self._read_lines()
        except:
            Parser._error("File", -1, "Cannot read source file.")
            return

        
        self._flag = True
        self._line = -1   
        self._errm = ""   

        
        self._parse_lines()
        if self._flag == False:
            Parser._error("PL", self._line, self._errm)
            return

        self._parseMacros()
        if self._flag == False:
            Parser._error("ML", self._line, self._errm)
            return

        self._labels = {}
        self._variables = {}

        self._parse_symbols()
        if self._flag == False:
            Parser._error("SYM", self._line, self._errm)
            return

        self._parse_commands()
        if self._flag == False:
            Parser._error("COM", self._line, self._errm)
            return

        try:
            self._outfile = open(filename + ".hack", "w")
        except:
            Parser._error("File", -1, "Cannot open output file")
            return

        try:
            self._write_file()
        except:
            Parser._error("File", -1, "Cannot write to output file")
            return

    def _read_lines(self):
        n = 0
        for line in self._file:
            self._lines.append((line, n, n))
            n += 1

    def _write_file(self):
        for (line, p, o) in self._lines:
            self._outfile.write(line)
            if (line[-1] != "\n"):
                self._outfile.write("\n")
            
    
    def _iter_lines(self, func):
        newlines = []
        i = 0
        for (line, p, o) in self._lines:
            newline = func(line, i, o)
            if (self._flag == False):
                break
            if (len(newline) > 0):
                newlines.append((newline, i, o))
                i += 1
        self._lines = newlines

    @staticmethod
    def _error(src, line, msg):
        if len(src) > 0 and line > -1:
            print("[" + src + ", " + str(line) + "] " + msg)
        elif len(src) > 0:
            print("[" + src + "] " + msg)
        else:
            print(msg)


if __name__ == "__main__":
    Parser("test")
