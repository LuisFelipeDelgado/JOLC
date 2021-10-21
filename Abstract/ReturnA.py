class Return:
    def __init__(self, val, retType, isTemp, aux = None):
        self.valor = val
        self.tipo = retType
        self.aux = aux
        self.isTemp = isTemp
        self.trueLbl = ''
        self.falseLbl = ''