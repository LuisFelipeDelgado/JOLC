# --------------------
# Luis Delgado
# --------------------

from Abstract.NodoAST import NodoAST
from Instrucciones.MStructs import MStruct
from Instrucciones.AStructs import AStruct
from Instrucciones.Parametro import Parametro
from Instrucciones.Structs import Struct
from Instrucciones.MArreglos import MArreglos
from Instrucciones.AArreglos import AArreglos
from Instrucciones.Continue import Continue
from Expresiones.Nativas import ENativas, ExpresionNativa
from TS.Tipo import TIPO, TIPOS
import os
import re
from Excepciones.Excepcion import Excepcion
import sys

sys.setrecursionlimit(3000)

errores = []
reservadas = {
    'print'     : 'RPRINT',
    'println'   : 'RPRINTLN',
    'if'        : 'RIF',
    'end'       : 'REND',
    'else'      : 'RELSE',
    'elseif'    : 'RELSEIF',
    'while'     : 'RWHILE',
    'for'       : 'RFOR',
    'in'        : 'RIN',
    'true'      : 'RTRUE',
    'false'     : 'RFALSE',
    'break'     : 'RBREAK',
    'function'  : 'RFUNC',
    'return'    : 'RRETURN',
    'continue'  : 'RCONTINUE',
    'log'       : 'RLOG',
    'log10'     : 'RLOG10',
    'sin'       : 'RSEN',
    'cos'       : 'RCOS',
    'tan'       : 'RTAN',
    'sqrt'      : 'RSQRT',
    'Int64'     : 'RINT',
    'Float64'   : 'RFLOAT',
    'Bool'      : 'RBOOL',
    'Char'      : 'RCHAR',
    'String'    : 'RSTRING',
    'Vector'   : 'RARREGLO',
    'parse'     : 'RPARSE',
    'trunc'     : 'RTRUNC',
    'float'     : 'RFLOAT2',
    'string'    : 'RSTRING2',
    'length'    : 'RLENGTH',
    'struct'    : 'RSTRUCT',
    'mutable'   : 'RMUTABLE',
    'nothing'   : 'RNOTHING',
    'global'   : 'RGLOBAL',
}

tokens  = [
    'PUNTOCOMA',
    'DOBLEDOS',
    'DOSPUNTOS',
    'PARA',
    'PARC',
    'LLAVEA',
    'LLAVEC',
    'CORA',
    'CORC',
    'COMA',
    'PTO',
    'MAS',
    'MENOS',
    'POR',
    'DIV',
    'POT',
    'MOD',
    'MENORQUE',
    'MAYORQUE',
    'IGUALIGUAL',
    'MENORIGUAL',
    'MAYORIGUAL',
    'DIFERENTE',
    'IGUAL',
    'AND',
    'OR',
    'NOT',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'ID'
] + list(reservadas.values())

# Tokens
t_PUNTOCOMA     = r';'
t_DOSPUNTOS     = r':'
t_DOBLEDOS      = r'::'
t_PARA          = r'\('
t_PARC          = r'\)'
t_LLAVEA        = r'{'
t_LLAVEC        = r'}'
t_CORA          = r'\['
t_CORC          = r'\]'
t_COMA          = r','
t_PTO           = r'\.'
t_MAS           = r'\+'
t_MENOS         = r'-'
t_POR           = r'\*'
t_DIV           = r'/'
t_POT           = r'\^'
t_MOD           = r'%'
t_MENORQUE      = r'<'
t_MENORIGUAL    = r'<='
t_MAYORQUE      = r'>'
t_MAYORIGUAL    = r'>='
t_IGUALIGUAL    = r'=='
t_DIFERENTE     = r'!='
t_IGUAL         = r'='
t_AND           = r'&&'
t_OR            = r'\|\|'
t_NOT           = r'!'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value,'ID')
     return t

def t_CADENA(t):
    r'(\".*?\")'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

def t_COMENTARIO_MULTILINEA(t):
    r'[/][*][^*]*[*]+([^/*][^*]*[*]+)*[/]*'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r"//.*"
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t\r"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    errores.append(Excepcion("Lexico","Error léxico: " + t.value[0] , t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()

# Asociación de operadores y precedencia
precedence = (
    ('left','OR'),
    ('left','AND'),
    ('left','IGUAL','NOT'),
    ('left','DIFERENTE','IGUALIGUAL'),
    ('left','MENORQUE','MAYORQUE','MAYORIGUAL','MENORIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR', 'DIV', 'MOD'),
    ('left','POT'),
    ('right','PARA','PARC'),
    ('right','UMENOS'),
    )

# Definición de la gramática

#Abstract
from Abstract.instruccion import Expresion
from Instrucciones.Imprimir import Imprimir
from Expresiones.Primitivo import Primitivo
from Expresiones.Aritmetica import Aritmetica, OperadorAritmetico
from Expresiones.Relacional import Relacional, OperadorRelacional
from Expresiones.Logica import Logica, OperadorLogico
from Expresiones.Identificador import Identificador
from Expresiones.Nativas import ENativas, ExpresionNativa
from Instrucciones.Asignacion import Asignacion
from Instrucciones.If import If
from Instrucciones.Nativas import FNativas, FuncionNativa
from Instrucciones.While import While
from Instrucciones.For import For
from Instrucciones.Break import Break
from Instrucciones.Funcion import Funcion
from Instrucciones.Llamada import Llamada
from Instrucciones.Return import ReturnI

def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_instrucciones_instruccion(t) :
    'instrucciones    : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]
    
#///////////////////////////////////////INSTRUCCIONES//////////////////////////////////////////////////

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion'
    if t[1] == "":
        t[0] = []
    else:    
        t[0] = [t[1]]

#///////////////////////////////////////INSTRUCCION//////////////////////////////////////////////////

def p_instruccion(t) :
    '''instruccion      : imprimir_instr PUNTOCOMA
                        | asignacion_instr PUNTOCOMA
                        | asignacion_instr_dos PUNTOCOMA
                        | if_instr 
                        | while_instr PUNTOCOMA
                        | for_instr PUNTOCOMA
                        | break_instr PUNTOCOMA
                        | continue_instr PUNTOCOMA
                        | funcion_instr PUNTOCOMA
                        | llamada_instr PUNTOCOMA
                        | return_instr 
                        | marreglo_instr PUNTOCOMA
                        | struct_instr PUNTOCOMA
                        | mstruct_instr PUNTOCOMA
    '''
    t[0] = t[1]

def p_instruccion_error(t):
    'instruccion        : error PUNTOCOMA'
    errores.append(Excepcion("Sintáctico","Error Sintáctico: " + str(t[1].value) , t.lineno(1), find_column(input, t.slice[1])))
    t[0] = ""
#///////////////////////////////////////IMPRIMIR//////////////////////////////////////////////////

def p_imprimir(t) :
    '''
    imprimir_instr      : RPRINT PARA varias_coma PARC
                    | RPRINTLN PARA varias_coma PARC
                    | RPRINT PARA PARC
                    | RPRINTLN PARA PARC
    '''
    if (t[1] == 'print')&(isinstance(t[3],list)):
        t[0] = Imprimir(t[3], t.lineno(1), find_column(input, t.slice[1]),2)
    elif (t[1] == 'println')&(isinstance(t[3],list)):
        t[0] = Imprimir(t[3], t.lineno(1), find_column(input, t.slice[1]),1)
    elif t[1] == 'print':
        t[0] = Imprimir(None, t.lineno(1), find_column(input, t.slice[1]),2)
    elif t[1] == 'println':
        t[0] = Imprimir(None, t.lineno(1), find_column(input, t.slice[1]),1)

def p_imprimir2(t):
    '''
    varias_coma         : varias_coma COMA expresion
    '''
    t[1].append(t[3])
    t[0] = t[1]

def p_imprimir3(t):
    '''
    varias_coma         : expresion
    '''
    t[0] = []
    t[0].append(t[1])

#///////////////////////////////////////DECLARACIÓN Y ASIGNACION//////////////////////////////////////////////////

def p_asignacion(t) :
    '''
    asignacion_instr     : ID IGUAL expresion
                        | RGLOBAL ID IGUAL expresion
                        | RGLOBAL ID
    '''
    if t[2]=="=":
        t[0] = Asignacion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))
    elif len(t)>3:
        t[0] = Asignacion(t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_asignacion2(t) :
    '''
    asignacion_instr_dos     : ID IGUAL expresion DOBLEDOS tipo
                            | ID IGUAL expresion DOBLEDOS ID
    '''
    if isinstance(t[5],str):
        t[0] = Asignacion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Asignacion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]),t[5])

def p_tipo(t):
    '''
    tipo                 : RINT
                        | RFLOAT
                        | RBOOL
                        | RCHAR
                        | RSTRING
                        | RARREGLO LLAVEA tlista LLAVEC
    '''
    if t[1]=='Int64':
        t[0] = TIPOS.ENTERO
    elif t[1]=='Float64':
        t[0] = TIPOS.DECIMAL
    elif t[1]=='Bool':
        t[0] = TIPOS.BOOLEANO
    elif t[1]=='Char':
        t[0] = TIPOS.CHARACTER
    elif t[1]=='String':
        t[0] = TIPOS.CADENA
    elif t[1]=='Vector':
        t[0] = t[3]

def p_tipo2(t):
    '''
    tlista              : RINT
                        | RFLOAT
                        | RBOOL
                        | RCHAR
                        | RSTRING
                        | RARREGLO LLAVEA tlista LLAVEC
    '''
    if t[1]=='Int64':
        t[0] = [TIPOS.ENTERO]
    elif t[1]=='Float64':
        t[0] = [TIPOS.DECIMAL]
    elif t[1]=='Bool':
        t[0] = [TIPOS.BOOLEANO]
    elif t[1]=='Char':
        t[0] = [TIPOS.CHARACTER]
    elif t[1]=='String':
        t[0] = [TIPOS.CADENA]
    elif t[1]=='Vector':
        t[0] = [TIPOS.ARREGLO]
        t[0] = t[0] + t[3]

#///////////////////////////////////////IF//////////////////////////////////////////////////

def p_if1(t) :
    'if_instr     : RIF expresion instrucciones REND PUNTOCOMA'
    t[0] = If(t[2], t[3], None, t.lineno(1), find_column(input, t.slice[1]))

def p_if2(t) :
    'if_instr     : RIF expresion instrucciones RELSE instrucciones REND PUNTOCOMA'
    t[0] = If(t[2], t[3], t[5], t.lineno(1), find_column(input, t.slice[1]))

def p_if3(t) :
    'if_instr     : RIF expresion instrucciones elseif_instr REND PUNTOCOMA'
    t[0] = If(t[2], t[3], t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_if4(t) :
    'elseif_instr     : RELSEIF expresion instrucciones RELSE instrucciones'
    t[0] = If(t[2], t[3], t[5], t.lineno(1), find_column(input, t.slice[1]))

def p_if5(t) :
    'elseif_instr     : RELSEIF expresion instrucciones elseif_instr'
    t[0] = If(t[2], t[3], t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_if6(t) :
    'elseif_instr     : RELSEIF expresion instrucciones'
    t[0] = If(t[2], t[3], None, t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////LOOP//////////////////////////////////////////////////

def p_while(t) :
    'while_instr     : RWHILE expresion instrucciones REND'
    t[0] = While(t[2], t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_for(t) :
    'for_instr     : RFOR ID RIN expresion DOSPUNTOS expresion instrucciones REND'
    t[0] = For(t[2], t[4], t[7], t.lineno(1), find_column(input, t.slice[1]), t[6])

def p_for2(t) :
    'for_instr     : RFOR ID RIN expresion instrucciones REND'
    t[0] = For(t[2], t[4], t[5], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////TRANSFERENCIA//////////////////////////////////////////////////

def p_break(t) :
    'break_instr     : RBREAK'
    t[0] = Break(t.lineno(1), find_column(input, t.slice[1]))

def p_continue(t) :
    'continue_instr     : RCONTINUE'
    t[0] = Continue(t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////FUNCION//////////////////////////////////////////////////

def p_funcion_1(t) :
    'funcion_instr     : RFUNC ID PARA parametros PARC DOBLEDOS tipo instrucciones REND'
    t[0] = Funcion(t[2], t[7], t[4], t[8], t.lineno(1), find_column(input, t.slice[1]))

def p_funcion_2(t) :
    'funcion_instr     : RFUNC ID PARA PARC DOBLEDOS tipo instrucciones REND'
    t[0] = Funcion(t[2], t[6], [], t[7], t.lineno(1), find_column(input, t.slice[1]))

def p_funcion_3(t) :
    'funcion_instr     : RFUNC ID PARA parametros PARC instrucciones REND'
    t[0] = Funcion(t[2], None, t[4], t[6], t.lineno(1), find_column(input, t.slice[1]))

def p_funcion_4(t) :
    'funcion_instr     : RFUNC ID PARA PARC instrucciones REND'
    t[0] = Funcion(t[2], None, [], t[5], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////PARAMETROS//////////////////////////////////////////////////

def p_parametros_1(t) :
    '''parametros     : parametros COMA ID
                    | parametros COMA ID DOBLEDOS ID  
                    | parametros COMA ID DOBLEDOS tipo  
    '''
    t[1].append(Parametro(t[3], t[5], t.lineno(1), find_column(input, t.slice[3])))
    t[0] = t[1]
    
def p_parametros_2(t) :
    '''parametros    : ID
                   | ID DOBLEDOS ID
                   | ID DOBLEDOS tipo
    '''
    t[0] = []
    t[0].append(Parametro(t[1], t[3], t.lineno(1), find_column(input, t.slice[1])))

#///////////////////////////////////////LLAMADA A FUNCION//////////////////////////////////////////////////

def p_llamada1(t) :
    '''llamada_instr     : ID PARA PARC
                        | ID PARA PARC DOBLEDOS ID
                        | ID PARA PARC DOBLEDOS tipo
    '''
    t[0] = Llamada(t[1], [], t.lineno(1), find_column(input, t.slice[1]))

def p_llamada2(t) :
    '''llamada_instr     : ID PARA parametros_llamada PARC
                        | ID PARA parametros_llamada PARC DOBLEDOS ID
                        | ID PARA parametros_llamada PARC DOBLEDOS tipo
    '''
    t[0] = Llamada(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////PARAMETROS LLAMADA A FUNCION//////////////////////////////////////////////////

def p_parametrosLL_1(t) :
    'parametros_llamada     : parametros_llamada COMA expresion'
    t[1].append(t[3])
    t[0] = t[1]

def p_parametrosLL_2(t) :
    'parametros_llamada    : expresion'
    t[0] = []
    t[0].append(t[1])

#///////////////////////////////////////LLAMADA A FUNCION//////////////////////////////////////////////////

def p_return(t) :
    '''return_instr     : RRETURN expresion PUNTOCOMA
                    | RRETURN PUNTOCOMA
    '''
    if t[2]==';':
        t[0] = ReturnI(None, t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = ReturnI(t[2], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////EXPRESION//////////////////////////////////////////////////

def p_expresion_binaria(t):
    '''
    expresion : expresion MAS expresion
            | expresion MENOS expresion
            | expresion POR expresion
            | expresion DIV expresion
            | expresion POT expresion
            | expresion MOD expresion
            | expresion MENORQUE expresion
            | expresion MAYORQUE expresion
            | expresion IGUALIGUAL expresion
            | expresion MENORIGUAL expresion
            | expresion MAYORIGUAL expresion
            | expresion DIFERENTE expresion
            | expresion AND expresion
            | expresion OR expresion
            | NOT expresion
            | MENOS expresion %prec UMENOS
    '''
    if t[2] == '+':
        t[0] = Aritmetica(OperadorAritmetico.MAS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        t[0] = Aritmetica(OperadorAritmetico.MENOS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*':
        t[0] = Aritmetica(OperadorAritmetico.POR, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '/':
        t[0] = Aritmetica(OperadorAritmetico.DIV, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '^':
        t[0] = Aritmetica(OperadorAritmetico.POT, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '%':
        t[0] = Aritmetica(OperadorAritmetico.MOD, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[1] == '-':
        t[0] = Aritmetica(OperadorAritmetico.UNMENOS, t[2],None, t.lineno(2), find_column(input, t.slice[1]))
    elif t[2] == '<':
        t[0] = Relacional(OperadorRelacional.MENORQUE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>':
        t[0] = Relacional(OperadorRelacional.MAYORQUE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '==':
        t[0] = Relacional(OperadorRelacional.IGUALIGUAL, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<=':
        t[0] = Relacional(OperadorRelacional.MENORIGUAL, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>=':
        t[0] = Relacional(OperadorRelacional.MAYORIGUAL, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '!=':
        t[0] = Relacional(OperadorRelacional.DIFERENTE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '&&':
        t[0] = Logica(OperadorLogico.AND, t[1], t.lineno(2), find_column(input, t.slice[2]),t[3])
    elif t[2] == '||':
        t[0] = Logica(OperadorLogico.OR, t[1], t.lineno(2), find_column(input, t.slice[2]),t[3])
    elif t[1] == '!':
        t[0] = Logica(OperadorLogico.NOT, t[2], t.lineno(2), find_column(input, t.slice[1]))

def p_expresion_nativa(t):
    '''
    expresion : RLOG PARA expresion COMA expresion PARC
            | RLOG10 PARA expresion PARC
            | RSEN PARA expresion PARC
            | RCOS PARA expresion PARC
            | RTAN PARA expresion PARC
            | RSQRT PARA expresion PARC
    '''
    if t[1] == 'log':
        t[0] = ENativas(ExpresionNativa.LOG, t[3], t.lineno(2), find_column(input, t.slice[2]), t[5])
    elif t[1] == 'log10':
        t[0] = ENativas(ExpresionNativa.LOG10, t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[1] == 'sin':
        t[0] = ENativas(ExpresionNativa.SIN, t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[1] == 'cos':
        t[0] = ENativas(ExpresionNativa.COS, t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[1] == 'tan':
        t[0] = ENativas(ExpresionNativa.TAN, t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[1] == 'sqrt':
        t[0] = ENativas(ExpresionNativa.SQRT, t[3], t.lineno(2), find_column(input, t.slice[2]))

def p_expresion_agrupacion(t):
    '''
    expresion :   PARA expresion PARC 
    '''
    t[0] = t[2]

def p_expresion_llamada(t):
    '''expresion : llamada_instr'''
    t[0] = t[1]

def p_expresion_identificador(t):
    '''expresion : ID'''
    t[0] = Identificador(t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_entero(t):
    '''expresion : ENTERO'''
    t[0] = Primitivo(TIPOS.ENTERO,t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_decimal(t):
    '''expresion : DECIMAL'''
    t[0] = Primitivo(TIPOS.DECIMAL,t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_cadena(t):
    '''expresion : CADENA'''
    t[0] = Primitivo(TIPOS.CADENA,str(t[1]).replace('\\n', '\n'), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_true(t):
    '''expresion : RTRUE'''
    t[0] = Primitivo(TIPOS.BOOLEANO, True, t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_false(t):
    '''expresion : RFALSE'''
    t[0] = Primitivo(TIPOS.BOOLEANO, False, t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_nothing(t):
    '''expresion : RNOTHING'''
    t[0] = Primitivo(TIPOS.NULO, None, t.lineno(1), find_column(input, t.slice[1]))

def p_funcion_nativa(t):
    '''
    expresion : RPARSE PARA tipo COMA expresion PARC
            | RTRUNC PARA tipo COMA expresion PARC
            | RFLOAT2 PARA expresion PARC
            | RSTRING2 PARA expresion PARC
            | RLENGTH PARA expresion PARC
    '''
    if t[1] == 'parse':
        t[0] = FNativas(FuncionNativa.PARSE, t[5], t.lineno(2), find_column(input, t.slice[2]), t[3])
    elif t[1] == 'trunc':
        t[0] = FNativas(FuncionNativa.TRUNC, t[5], t.lineno(2), find_column(input, t.slice[2]), t[3])
    elif t[1] == 'float':
        t[0] = FNativas(FuncionNativa.FLOAT, t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[1] == 'string':
        t[0] = FNativas(FuncionNativa.STRING, t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[1] == 'length':
        t[0] = FNativas(FuncionNativa.LENGTH, t[3], t.lineno(2), find_column(input, t.slice[2]))

#///////////////////////////////////////ARREGLOS//////////////////////////////////////////////////

def p_arreglos(t):
    '''
    expresion : CORA varias_coma CORC
    '''
    t[0] = Primitivo(TIPOS.ARREGLO,t[2], t.lineno(1), find_column(input, t.slice[1]))

def p_aArreglos(t):
    '''
    expresion : ID varios_cor
    '''
    t[0] = AArreglos(t[1], t[2], t.lineno(1), 1)

def p_aArreglos2(t):
    '''
    varios_cor         : varios_cor CORA expresion CORC
    '''
    t[1].append(t[3])
    t[0] = t[1]

def p_aArreglos3(t):
    '''
    varios_cor         : CORA expresion CORC
    '''
    t[0] = []
    t[0].append(t[2])

def p_mArreglos(t):
    '''
    marreglo_instr : ID varios_cor IGUAL expresion
    '''
    t[0] = MArreglos(t[1], t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))

#////////////////////////////////////////STRUCTS///////////////////////////////////////////////////

def p_dstructs(t):
    '''
    struct_instr : RMUTABLE RSTRUCT ID atributos REND
                | RSTRUCT ID atributos REND
    '''
    if t[1]=="mutable":
        t[0] = Struct(t[3],t[4], t.lineno(1), find_column(input, t.slice[1]),t[1])
    else:
        t[0] = Struct(t[2],t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_atr_structs(t):
    '''
    atributos         : atributos ID PUNTOCOMA
                    | atributos ID DOBLEDOS ID PUNTOCOMA
                    | atributos ID DOBLEDOS tipo PUNTOCOMA
    '''
    t[1].setdefault(t[2])
    t[0] = t[1]

def p_atr_structs2(t):
    '''
    atributos         : ID PUNTOCOMA
                    | ID DOBLEDOS ID PUNTOCOMA
                    | ID DOBLEDOS tipo PUNTOCOMA
    '''
    t[0] = {}
    t[0].setdefault(t[1])

def p_mstructs(t):
    '''
    mstruct_instr : ID varios_pt IGUAL expresion 
    '''
    t[0] = MStruct(t[1],t[2],t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_mstructs2(t):
    '''
    varios_pt         : varios_pt PTO ID
    '''
    t[1].append(t[3])
    t[0] = t[1]

def p_mstructs3(t):
    '''
    varios_pt         : PTO ID
    '''
    t[0] = []
    t[0].append(t[2])

def p_astructs(t):
    '''
    expresion : ID varios_pt
    '''
    t[0] = AStruct(t[1], t[2], t.lineno(1), find_column(input, t.slice[1]))

import ply.yacc as yacc
parser = yacc.yacc()

from TS.Arbol import Arbol
from TS.TablaSimbolos import TablaSimbolos

def getErrores():
    return errores

def parse(inp) :
    global errores
    global lexer
    global parser
    errores = []
    lexer = lex.lex(reflags= re.IGNORECASE)
    parser = yacc.yacc()
    global input
    input = inp
    instrucciones=parser.parse(inp)
    ast = Arbol(instrucciones)
    TSGlobal = TablaSimbolos()
    TSGlobal.setEntorno("Global")
    ast.setTSglobal(TSGlobal)
    ast.tablas.append(TSGlobal)
    #for error in errores:                   # CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
    #     ast.getExcepciones().append(error)
    #     ast.updateConsola(error.toString())
    ast.excepciones = errores
    for instruccion in ast.getInstrucciones():
        result = instruccion.interpretar(ast,TSGlobal)
        if isinstance(result, Excepcion):
            ast.excepciones.append(result)
            ast.updateConsola(result.toString())

    raiz = NodoAST("RAIZ")
    instruccioness = NodoAST("init")
    instruccioness2 = NodoAST("INSTRUCCIONES")
    for i in ast.getInstrucciones():
        if i == ast.getInstrucciones()[0]:
            instruccioness3 = NodoAST("INSTRUCCION")
            instruccioness3.agregarHijoNodo(i.getNodo())
            instruccioness2.agregarHijoNodo(instruccioness3)
        else:
            instrtmp = instruccioness2
            instruccioness3 = NodoAST("INSTRUCCION")
            instruccioness2 = NodoAST("INSTRUCCIONES")
            instruccioness2.agregarHijoNodo(instrtmp)
            instruccioness3.agregarHijoNodo(i.getNodo())
            instruccioness2.agregarHijoNodo(instruccioness3)
    instruccioness.agregarHijoNodo(instruccioness2)
    raiz.agregarHijoNodo(instruccioness)
    ast.raiz = raiz
    return ast
