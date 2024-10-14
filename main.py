from gramatica import Gramatica

prueba = Gramatica()
prueba.setear("S:a Q\nQ:b R\nQ:c R\nR:d\nU:U b")
#prueba.setear("S:X Y Z\nX:a\nX:b\nX:lambda\nY:a\nY:d\nY:lambda\nZ:e\nZ:f\nZ:lambda")
#prueba.setear("S:a Q\nS:a R\nQ:b\nR:b\nP:d")
print(prueba)


