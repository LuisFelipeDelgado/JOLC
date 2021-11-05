class Return:
    def __init__(self, val, retType, isTemp, aux = None,tipoS=''):
        self.valor = val
        self.tipo = retType
        self.aux = aux
        self.isTemp = isTemp
        self.ev = ''
        self.ef = ''
        self.tipoS = tipoS