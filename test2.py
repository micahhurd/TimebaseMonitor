instr = "56,1,0,153,0,0;56,1,0,153,0,0;56,1,0,153,0,0;5,1,2,34,B_3_1_1,0;5,1,2,34,C_9841,0;"

results = []
index = instr.find('C_')
while index >= 0:
    length = instr[index:].find(',')
    assert length > 0
    results.append(instr[index+2:index+length])
    instr = instr[index+length:]
    index = instr.find('C_')


length = instr[4].find(',')
print(length)