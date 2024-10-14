from gramatica import Gramatica

prueba = Gramatica()
prueba.setear("S:a Q\nQ:b R\nQ:c R\nR:d\nU:U b")
print(prueba)
print("-----------------------------------------------------------------------------")
prueba.setear("S:X Y Z\nX:a\nX:b\nX:lambda\nY:a\nY:d\nY:lambda\nZ:e\nZ:f\nZ:lambda")
print(prueba)
print("-----------------------------------------------------------------------------")
prueba.setear("S:a Q\nS:a R\nQ:b\nR:b\nP:d")
print(prueba)
print("-----------------------------------------------------------------------------")
prueba.setear("S:a S\nS:Q\nQ:b")
print(prueba)
print("-----------------------------------------------------------------------------")


