from gramatica import Gramatica

prueba = Gramatica()

gramaticas = []

gramaticas.append("S:a Q\nQ:b R\nQ:c R\nR:d\nU:U b")
gramaticas.append("S:X Y Z\nX:a\nX:b\nX:lambda\nY:a\nY:d\nY:lambda\nZ:e\nZ:f\nZ:lambda")
gramaticas.append("S:a Q\nS:a R\nQ:b\nR:b\nP:d")
gramaticas.append("S:a S\nS:Q\nQ:b")
gramaticas.append("S:P\nS:Q\nQ:b Q\nP:a P\nP:lambda")

for reglas in gramaticas:
    prueba.setear(reglas)
    print(prueba)
    print("-----------------------------------------------------------------------------")
    print()
