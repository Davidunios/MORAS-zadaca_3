def _parse_symbols(self):
    
    self._init_symbols()

   
    self._iter_lines(self._parse_labels)

    
    self._num_vars = 16
    self._iter_lines(self._parse_variables)




def _parse_labels(self, line, p, o):
    if line[0] == "(":
        splitted = line[1:].split(")")
        label = splitted[0]

        if len(label) == 0 or len(splitted) > 2 or len(splitted[1]) > 0:
            self._flag = False
            self._line = o
            self._errm = "Invalid label"
        else:
            self._labels[label] = str(p)
        return ""
    else:
        return line



def _parse_variables(self, line, p, o):
    if line[0] != "@":
        return line

    l = line[1:]

    if l.isdigit():
        return line

    if l in self._labels:
        return "@" + self._labels[l]

    if l not in self._variables:
        self._variables[l] = str(self._num_vars)
        self._num_vars += 1

    return "@" + self._variables[l]




def _init_symbols(self):
    self._labels = {
        "SCREEN": "16384",
        "KBD": "24576",
        "SP": "0",
        "LCL": "1",
        "ARG": "2",
        "THIS": "3",
        "THAT": "4"
    }

    for i in range(0, 16):
        self._labels["R" + str(i)] = str(i)
