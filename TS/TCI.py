class TCI:
    codigoR = None
    def __init__(self):
        # Contadores
        self.countTemp = 0
        self.countLabel = 0
        # Code
        self.code = ''
        self.funcs = ''
        self.natives = ''
        self.inFunc = False
        self.inNatives = False
        # Lista de Temporales
        self.temps = []
        # Lista de Nativas
        self.printString = False
        self.conString = False
        self.powString = False
        self.Pow = False
        self.compareString = False

    #------------------------------------------------REINICIO-----------------------------------------------
            
    def cleanAll(self):
        # Contadores
        self.countTemp = 0
        self.countLabel = 0
        # Code
        self.code = ''
        self.funcs = ''
        self.natives = ''
        self.inFunc = False
        self.inNatives = False
        # Lista de Temporales
        self.temps = []
        # Lista de Nativas
        self.printString = False
        TCI.codigoR = TCI()
    
    #------------------------------------------------CODIGO-----------------------------------------------
    
    def getHeader(self):
        ret = '/*----HEADER----*/\npackage main;\n\nimport (\n\t"fmt";\n\t"math"\n)\n\n'
        if len(self.temps) > 0:
            ret += 'var '
            for temp in range(len(self.temps)):
                ret += self.temps[temp]
                if temp != (len(self.temps) - 1):
                    ret += ", "
            ret += " float64\n"
        ret += "var P, H float64;\nvar stack [30101999]float64;\nvar heap [30101999]float64;\n\n"
        return ret

    def getCode(self):
        return f'{self.getHeader()}{self.natives}\n{self.funcs}\nfunc main(){{\n{self.code}\n}}'

    def codeIn(self, code, tab="\t"):
        if(self.inNatives):
            if(self.natives == ''):
                self.natives = self.natives + '/*-----NATIVES-----*/\n'
            self.natives = self.natives + tab + code
        elif(self.inFunc):
            if(self.funcs == ''):
                self.funcs = self.funcs + '/*-----FUNCS-----*/\n'
            self.funcs = self.funcs + tab +  code
        else:
            self.code = self.code + '\t' +  code

    def addComment(self, comment):
        self.codeIn(f'/* {comment} */\n')
    
    def getInstance(self):
        if TCI.codigoR == None:
            TCI.codigoR = TCI()
        return TCI.codigoR

    def addSpace(self):
        self.codeIn("\n")

    #------------------------------------------------TEMPORALES-----------------------------------------------
    
    def addTemp(self):
        temp = f't{self.countTemp}'
        self.countTemp += 1
        self.temps.append(temp)
        return temp

    #------------------------------------------------ETIQUETAS-----------------------------------------------
        
    def newE(self):
        label = f'L{self.countLabel}'
        self.countLabel += 1
        return label

    def putE(self, label):
        self.codeIn(f'{label}:\n')

    #------------------------------------------------SALTO-----------------------------------------------
    
    def GoTo(self, label):
        self.codeIn(f'goto {label};\n')
    
    #------------------------------------------------CONDICIONES-----------------------------------------------
    
    def addIf(self, left, right, op, label):
        self.codeIn(f'if {left} {op} {right} {{goto {label};}}\n')

    #------------------------------------------------EXPRESIONES-----------------------------------------------
    
    def addExp(self, result, left, right, op):
        self.codeIn(f'{result}={left}{op}{right};\n')
    
    def addMod(self, result, left, right):
        self.codeIn(f'{result}=math.Mod({left},{right});\n')
    
    #------------------------------------------------FUNCIONES-----------------------------------------------
    
    def addBeginFunc(self, id):
        if(not self.inNatives):
            self.inFunc = True
        self.codeIn(f'func {id}(){{\n', '')
    
    def addEndFunc(self):
        self.codeIn('return;\n}\n');
        if(not self.inNatives):
            self.inFunc = False

    #------------------------------------------------STACK-----------------------------------------------
        
    def setStack(self, pos, value):
        self.codeIn(f'stack[int({pos})]={value};\n')
    
    def getStack(self, place, pos):
        self.codeIn(f'{place}=stack[int({pos})];\n')

    #------------------------------------------------ENTORNO-----------------------------------------------
    
    def newEnv(self, size):
        self.codeIn(f'P=P+{size};\n')

    def callFun(self, id):
        self.codeIn(f'{id}();\n')

    def retEnv(self, size):
        self.codeIn(f'P=P-{size};\n')

    #----------------------------------------------HEAP-------------------------------------------------------

    def setHeap(self, pos, value):
        self.codeIn(f'heap[int({pos})]={value};\n')

    def getHeap(self, place, pos):
        self.codeIn(f'{place}=heap[int({pos})];\n')

    def nextHeap(self):
        self.codeIn('H=H+1;\n')

    #---------------------------------------------INSTRUCCIONES----------------------------------------------
    def addPrint(self, type, value):
        if type=='d':
            self.codeIn(f'fmt.Printf("%{type}", int({value}));\n')
        elif type=='f':
            self.codeIn(f'fmt.Printf("%{type}", {value});\n')
        else:
            self.codeIn(f'fmt.Printf("%{type}", int({value}));\n')
    
    def printTrue(self):
        self.addPrint("c", 116)
        self.addPrint("c", 114)
        self.addPrint("c", 117)
        self.addPrint("c", 101)

    def printFalse(self):
        self.addPrint("c", 102)
        self.addPrint("c", 97)
        self.addPrint("c", 108)
        self.addPrint("c", 115)
        self.addPrint("c", 101)
    
    #----------------------------------NATIVAS------------------------------------
    
    def fPrintString(self):
        if(self.printString):
            return
        self.printString = True
        self.inNatives = True

        self.addBeginFunc('printString')
        # Label para salir de la funcion
        returnE = self.newE()
        # Label para la comparacion para buscar fin de cadena
        compareE = self.newE()

        # Temporal puntero a Stack
        tempP = self.addTemp()

        # Temporal puntero a Heap
        tempH = self.addTemp()

        self.addExp(tempP, 'P', '1', '+')

        self.getStack(tempH, tempP)

        # Temporal para comparar
        tempC = self.addTemp()

        self.putE(compareE)

        self.getHeap(tempC, tempH)

        self.addIf(tempC, '-1', '==', returnE)

        self.addPrint('c', tempC)

        self.addExp(tempH, tempH, '1', '+')

        self.GoTo(compareE)

        self.putE(returnE)
        self.addEndFunc()
        self.inNatives = False

    def fconString(self):
        if(self.conString):
            return
        self.conString = True
        self.inNatives = True
        self.addBeginFunc('addString')
        returnE = self.newE()
        compareE = self.newE()
        tempH = self.addTemp()
        temp1 = self.addTemp()
        temp2 = self.addTemp()
        tempL = self.addTemp()
        self.addExp(tempH, 'H', '', '')
        self.addExp(temp1, 'P', '1', '+')
        self.getStack(tempL,temp1)
        self.addExp(temp2, 'P', '2', '+')
        tempC = self.addTemp()
        self.putE(compareE)
        self.getHeap(tempC,tempL)
        self.addIf(tempC, '-1', '==', returnE)
        self.setHeap('H',tempC)
        self.addExp('H', 'H', '1', '+')
        self.addExp(tempL, tempL, '1', '+')
        self.GoTo(compareE)
        self.putE(returnE)
        returnE = self.newE()
        compareE = self.newE()
        self.getStack(tempL,temp2)
        self.putE(compareE)
        self.getHeap(tempC,tempL)
        self.addIf(tempC, '-1', '==', returnE)
        self.setHeap('H',tempC)
        self.addExp('H', 'H', '1', '+')
        self.addExp(tempL, tempL, '1', '+')
        self.GoTo(compareE)
        self.putE(returnE)
        self.setHeap('H','-1')
        self.addExp('H', 'H', '1', '+')
        self.setStack('P',tempH)
        self.addEndFunc()
        self.inNatives = False
        return

    def fpowString(self):
        if(self.powString):
            return
        self.powString = True
        self.inNatives = True
        self.addBeginFunc('powString')
        returnE = self.newE()
        compareE = self.newE()
        loopE = self.newE()
        tempH = self.addTemp()
        temp1 = self.addTemp()
        temp2 = self.addTemp()
        tempL = self.addTemp()
        tempR = self.addTemp()
        self.addExp(tempH, 'H', '', '')
        self.addExp(temp1, 'P', '1', '+')
        self.getStack(tempL,temp1)
        self.addExp(temp2, 'P', '2', '+')
        self.getStack(tempR,temp2)
        tempC = self.addTemp()
        self.putE(compareE)
        self.getHeap(tempC,tempL)
        self.addIf(tempC, '-1', '==', loopE)
        self.setHeap('H',tempC)
        self.addExp('H', 'H', '1', '+')
        self.addExp(tempL, tempL, '1', '+')
        self.GoTo(compareE)
        self.putE(loopE)
        self.addIf(tempR, '1', '==', returnE)
        self.addExp(tempR, tempR, '1', '-')
        self.getStack(tempL,temp1)
        self.GoTo(compareE)
        self.putE(returnE)
        self.setHeap('H','-1')
        self.addExp('H', 'H', '1', '+')
        self.setStack('P',tempH)
        self.addEndFunc()
        self.inNatives = False
        return

    def fPow(self):
        if(self.Pow):
            return
        self.Pow = True
        self.inNatives = True
        self.addBeginFunc('Pow')
        returnE = self.newE()
        compareE = self.newE()
        pE = self.newE()
        temp1 = self.addTemp()
        temp2 = self.addTemp()
        tempL = self.addTemp()
        tempR = self.addTemp()
        self.addExp(temp1, 'P', '1', '+')
        self.getStack(tempL,temp1)
        self.addExp(temp2, 'P', '2', '+')
        self.getStack(tempR,temp2)
        tempC = self.addTemp()
        self.getStack(tempC,temp1)
        zeroE = self.newE()
        self.addIf(tempR, '0', '>', compareE)
        self.GoTo(zeroE)
        self.putE(compareE)
        self.addIf(tempR, '1', '==', returnE)
        self.addExp(tempL, tempL, tempC, '*')
        self.addExp(tempR, tempR, '1', '-')
        self.GoTo(compareE)
        self.putE(returnE)
        self.setStack('P',tempL)
        self.GoTo(pE)
        self.putE(zeroE)
        self.setStack('P','1')
        self.putE(pE)
        self.addEndFunc()
        self.inNatives = False
        return

    def fcompareString(self):
        if(self.compareString):
            return
        self.compareString = True
        self.inNatives = True
        self.addBeginFunc('compareString')
        returnE = self.newE()
        compareE = self.newE()
        evE = self.newE()
        efE = self.newE()
        temp1 = self.addTemp()
        temp2 = self.addTemp()
        tempL = self.addTemp()
        tempR = self.addTemp()
        tempCL = self.addTemp()
        tempCR = self.addTemp()
        self.addExp(temp1, 'P', '1', '+')
        self.getStack(tempL,temp1)
        self.addExp(temp2, temp1, '1', '+')
        self.getStack(tempR,temp2)
        self.putE(compareE)
        self.getHeap(tempCL,tempL)
        self.getHeap(tempCR,tempR)
        self.addIf(tempCL,tempCR,'!=',efE)
        self.addIf(tempCL,'-1','==',evE)
        self.addExp(tempL, tempL, '1', '+')
        self.addExp(tempR, tempR, '1', '+')
        self.GoTo(compareE)
        self.putE(evE)
        self.setStack('P','1')
        self.GoTo(returnE)
        self.putE(efE)
        self.setStack('P','0')
        self.putE(returnE)
        self.addEndFunc()
        self.inNatives = False
        return