from os import read, write


def myreadline():
    index = 0
    line = ""
    buff = read(0, 100)
    string = buff.decode()
    
    while index < len(string):
        current_char = string[index]
        if current_char == '\n':
            return line
        
        line += current_char
        index += 1;
        
        if index == 100:
            buff =  read(0,100)
            string = ibuf.decode()
            index = 0
            
    return "" # EOF reached
