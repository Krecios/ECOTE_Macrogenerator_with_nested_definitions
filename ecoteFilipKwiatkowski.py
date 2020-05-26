import copy

lexems = []
dictionary = []
output = []


def lexer():
    stack = []
    with open('input.txt') as input:
        for line in input:
            if line[0] == '&':
                if 2 >= len(line) >= 1:
                    if len(stack) == 0:
                        print('ERROR: MACRO CLOSE STATEMENT WITHOUT OPENING FOUND')
                    else:
                        lexems.append("MACRO.END." + stack.pop())
                else:
                    if line[-1] == '\n':
                        lexems.append('MACRO.START.' + line[1:-1])
                        stack.append(line[1:-1])
                    else:
                        lexems.append('MACRO.START.' + line[1:])
                        stack.append(line[1:])
            elif line[0] == '$':
                if line[-1] == '\n':
                    lexems.append('MACRO.CALL.' + line[1:-1])
                else:
                    lexems.append('MACRO.CALL.' + line[1:])
            else:
                if line[-1] == '\n':
                    lexems.append('FREETEXT.' + line[:-1])
                else:
                    lexems.append('FREETEXT.' + line[:])
    if len(stack) != 0:
        for definition in stack:
            print('ERROR: DEFINITION OF MACRO WITH NO CLOSE STATEMENT ' + definition)


def parser(lexedFile, context):
    description = []
    defStart = False
    macroName = ''
    numberOfDef = 0
    for lexem in lexedFile:
        if defStart == True:
            description.append(lexem)
            if lexem[:12] == 'MACRO.START.':
                numberOfDef += 1
        if lexem[:12] == 'MACRO.START.' and defStart == False:
            defStart = True
            macroName = lexem[12:]
            for nest in context:
                if macroName == nest:
                    print('ERROR CANNOT NEST A MACRO WITH A')
                    defStart = False
        if lexem == 'MACRO.END.' + macroName:
            defStart = False
            macroDescription = {
                'name': macroName,
                'nested': numberOfDef,
                'context': context,
                'content': copy.deepcopy(description[:-1])
            }
            for definition in dictionary:
                if definition['name'] == macroDescription['name'] and definition['context'] == macroDescription['context']:
                    dictionary.remove(definition)
                    print('Macro "' + macroName + '" has been overwritten')
            dictionary.append(macroDescription)
            numberOfDef = 0
            description.clear()


def addNested():
    for macro in dictionary:
        if macro['nested'] != 0:
            tempContext = copy.deepcopy(macro['context'])
            tempContext.append(macro['name'])
            parser(macro['content'], tempContext)


def cleanDictionary():
    clean = False
    macroName = ''
    for definition in dictionary:
        tempContent = copy.deepcopy(definition['content'])
        cleanedContent = []
        for lexem in tempContent:
            if lexem[:12] == 'MACRO.START.' and clean == False:
                macroName = lexem[12:]
                clean = True
            if clean == False:
                cleanedContent.append(lexem)
            if lexem == 'MACRO.END.' + macroName:
                clean = False
                macroName = ''
        definition['content'] = copy.deepcopy(cleanedContent)


def showDictionary():
    for definition in dictionary:
        print(definition)


def createOutput(lexems, context):
    write = True
    macroName = ''
    callName = ''
    definitionFound = False
    global output
    for lexem in lexems:
        if lexem[:12] == 'MACRO.START.' and write == True:
            write = False
            macroName = lexem[12:]
        if lexem[:9] == 'FREETEXT.' and write == True:
            output.append(lexem)
        if lexem[:11] == 'MACRO.CALL.' and write == True:
            tempContext = copy.deepcopy(context)
            callName = lexem[11:]
            nestedCall = False
            for nest in tempContext:
                if nest == callName:
                    nestedCall = True
            if nestedCall == False:
                while definitionFound == False:
                    for definition in dictionary:
                        if definition['name'] == callName and definition['context'] == tempContext:
                            definitionFound = True
                            tempContext.append(callName)
                            createOutput(definition['content'], tempContext)
                    if definitionFound == False and len(tempContext) == 0:
                        print('MACRO "' + lexem[11:] +
                              '" has no definition in given context')
                        print(context)
                        break
                    if definitionFound == False and len(tempContext) != 0:
                        tempContext.pop()
            else:
                print('MACRO "' + lexem[11:] +
                      '" cannot be called for within its own definition in context:')
                print(context)
        definitionFound = False
        if lexem == 'MACRO.END.' + macroName:
            write = True
            macroName = ''


def writeOutput(output):
    outputFile = open('output.txt', 'w')
    for lexem in output:
        outputFile.write(lexem[9:] + '\n')


lexer()
# print(lexems)
parser(lexems, [])
#print('================================ DICTIONARY')
# showDictionary()
addNested()
#print('================================ DICTIONARY ====================== ADDED')
# showDictionary()
#print('================================ DICTIONARY ====================== ADDED ============== CEANED')
cleanDictionary()
# showDictionary()
createOutput(lexems, [])
# print(output)
writeOutput(output)

'''
TO DO:
Add assumptions
'''
