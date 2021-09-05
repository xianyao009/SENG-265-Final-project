import sys
import re
import fileinput

class SENJIFY:
    def __init__(self, input_stream):
        self.input_stream = input_stream
        self.cmd = {"on_off": 0, "width": 0, "indent": 0} #dictionary to store command
        self.if_lastline_is_newline = False # check if lastline is newline or not
        self.char_count = 0 #count the number of char in a line
        self.regex_compile = re.compile(r"{{ (\d+|\>|on|off|\!|\+>|\->)?(\d+)? }}") 
        self.result = []
        self.format()

    def format(self):
        for line in self.input_stream:
            completed_line = self.__operation(line)
            if completed_line:
                self.result.append(completed_line)
        self.__remove_last_newline()

        return self.result
        
    def __remove_last_newline(self): #remove the last "\n" in the list if it exists
        if len(self.result) >= 1: 
            for x in range(len(self.result) - 1):
                self.result[0] += self.result[1]
                self.result.remove(self.result[1])

            self.result[0] = self.result[0].rstrip("\n")           
 
    def __operation(self, line):
        is_command = self.regex_compile.match(line)

        if is_command: #extract formatting command from command
            regex_group = is_command.groups()
            if regex_group[0] == "on":
                self.cmd["on_off"] = 1
            elif regex_group[0] == "off":
                self.cmd["on_off"] = 0
            elif regex_group[0] == "+>":
                self.cmd["indent"] += int(regex_group[1])
                if self.cmd["indent"] > self.cmd["width"] - 20:
                    self.cmd["indent"] = self.cmd["width"]
            elif regex_group[0] == "->":
                self.cmd["indent"] -= int(regex_group[1])
                if self.cmd["indent"] < 0:
                    self.cmd["indent"] = 0
            elif regex_group[0] == ">":
                self.cmd["indent"] = int(regex_group[1])
            elif regex_group[0] == "!": 
                if self.cmd["on_off"] == 1:
                    self.cmd["on_off"] = 0
                elif self.cmd["on_off"] == 0:
                    self.cmd["on_off"] = 1
            elif regex_group[0].isnumeric():
                self.cmd["on_off"] = 1
                self.cmd["width"] = int(regex_group[0])  

            line = None #delete "{{ ? }}"
            

        if self.cmd["on_off"] == 1 and line != None:
            split = line.split()

            if split == []: 
                self.char_count = 0
                if self.if_lastline_is_newline:
                    return '\n'
                else:
                    self.if_lastline_is_newline = True
                    return '\n\n'

            self.if_lastline_is_newline = False

            if self.char_count == 0:
                formatted_line = "".join([" " for i in range(self.cmd["indent"])])
                self.char_count = self.cmd["indent"]
            else:
                formatted_line = ""

            for word in split:
                if self.char_count + len(word) >= self.cmd["width"]:
                    indent = "".join([" " for i in range(self.cmd["indent"])])
                    formatted_line = formatted_line + '\n' + indent
                    self.char_count = self.cmd["indent"]
                elif self.char_count != self.cmd["indent"]:
                    self.char_count += 1
                    formatted_line = formatted_line + ' '
                formatted_line = formatted_line + word
                self.char_count += len(word)
            return formatted_line # return formatted line if on_off is 1

        else:
            return line #return unformatted line if on_off is 0
                        

