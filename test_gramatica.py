import unittest
from gramatica import Gramatica

class TestGramaticaLL1(unittest.TestCase):
    def test_sin_recursividad_derecha(self):
        """a. Prueba una gramática sin recursión a derecha"""
        g = Gramatica()
        g.setear("S:Q a\nQ:b\nQ:c")
        self.assertTrue(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("ba"))
        self.assertTrue(g.evaluar_cadena("ca"))
        self.assertFalse(g.evaluar_cadena("aba"))

    def test_con_recursividad_derecha(self):
        """b. Prueba una gramática con recursión a derecha"""
        g = Gramatica()
        g.setear("S:P\nS:Q\nQ:b Q\nP:a P\nP:lambda")
        self.assertTrue(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("aaa"))
        self.assertFalse(g.evaluar_cadena("b"))

    def test_con_lambda(self):
        """c. Prueba una gramática con lambda"""
        g = Gramatica()
        g.setear("S:Q a\nQ:b\nQ:lambda")
        self.assertTrue(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("ba"))
        self.assertFalse(g.evaluar_cadena(""))

    def test_sin_lambda(self):
        """d. Prueba una gramática sin lambda"""
        g = Gramatica()
        g.setear("S:a Q\nQ:b R\nQ:c R\nR:d")
        self.assertTrue(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("abd"))
        self.assertTrue(g.evaluar_cadena("acd"))
        self.assertFalse(g.evaluar_cadena(""))

    def test_con_reglas_innecesarias(self):
        """e. Prueba una gramática con reglas innecesarias"""
        g = Gramatica()
        g.setear("S:P a\nP:P\nP:b")
        self.assertTrue(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("ba"))
        self.assertFalse(g.evaluar_cadena("c"))

    def test_con_simbolos_inaccesibles(self):
        """f. Prueba una gramática con símbolos inaccesibles desde el axioma"""
        g = Gramatica()
        g.setear("S:a Q\nQ:b Q\nQ:c\nP:d")
        self.assertTrue(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("abc"))
        self.assertFalse(g.evaluar_cadena("adc"))

    def test_con_no_terminales_no_generativos(self):
        """g. Prueba una gramática con no terminales no generativos"""
        g = Gramatica()
        g.setear("S:Q a\nS:P\nQ:c\nP:P x")
        self.assertTrue(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("ca"))
        self.assertFalse(g.evaluar_cadena("ac"))

    """ Tests no LL(1) """

    def test_no_ll1_sin_recursion_derecha(self):
        """h.a Gramática sin recursión a derecha"""
        g = Gramatica()
        g.setear("S:Q a\nS:P\nP:b\nQ:b")
        self.assertFalse(g.EsLL1)

    def test_no_ll1_con_recursion_derecha(self):
        """h.b Gramática con recursión a derecha"""
        g = Gramatica()
        g.setear("S:a S\nS:P\nS:b\nS:Q\nQ:Q b\nP:b")
        self.assertFalse(g.EsLL1)

    def test_no_ll1_con_lambda(self):
        """h.c Gramática con lambda"""
        g = Gramatica()
        g.setear("S:Q a\nS:P\nP:b\nQ:b\nQ:lambda")
        self.assertFalse(g.EsLL1)

    def test_no_ll1_sin_lambda(self):
        """h.d Gramática sin lambda"""
        g = Gramatica()
        g.setear("S:a Q\nQ:b R\nQ:b\nR:x")
        self.assertFalse(g.EsLL1)

    def test_no_ll1_con_reglas_innecesarias(self):
        """h.e Gramática con una regla innecesaria"""
        g = Gramatica()
        g.setear("S:P a\nS:Q\nQ:b\nP:P\nP:b")
        self.assertFalse(g.EsLL1)

    def test_no_ll1_con_simbolos_inaccesibles(self):
        """h.f Gramática con un símbolo inaccesible desde el axioma"""
        g = Gramatica()
        g.setear("S:a Q\nS:a R\nQ:b\nR:b\nP:d")
        self.assertFalse(g.EsLL1)

    def test_no_ll1_con_no_terminales_no_generativos(self):
        """h.g Gramática con un no terminal no generativo"""
        g = Gramatica()
        g.setear("S:Q a\nS:P\nS:R\nQ:c\nP:c\nR:R a")
        self.assertFalse(g.EsLL1)
    
    def test_recursion_izquierda(self):
        """i. Gramática con recursión a la izquierda"""
        g = Gramatica()
        g.setear("S:Q a\nQ:A\nQ:B\nA:b\nB:b")

