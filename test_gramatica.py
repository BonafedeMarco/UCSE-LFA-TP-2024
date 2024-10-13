import unittest
from gramatica import Gramatica

class TestGramaticaLL1(unittest.TestCase):
    def test_sin_recursividad_derecha(self):
        """Prueba una gramática sin recursión a derecha"""
        g = Gramatica()
        g.setear("S:Q a\nQ:b\nQ:c")
        self.assertTrue(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("ba"))
        self.assertTrue(g.evaluar_cadena("ca"))
        self.assertFalse(g.evaluar_cadena("aba"))

    def test_con_recursividad_derecha(self):
        """Prueba una gramática con recursión a derecha"""
        g = Gramatica()
        g.setear("S:a S\nS:Q\nQ:b")
        self.assertTrue(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("ab"))
        self.assertTrue(g.evaluar_cadena("b"))

    def test_con_lambda(self):
        """Prueba una gramática con lambda"""
        g = Gramatica()
        g.setear("S:Q a\nQ:b\nQ:lambda")
        self.assertTrue(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("ba"))
        self.assertFalse(g.evaluar_cadena(""))

    def test_sin_lambda(self):
        """Prueba una gramática sin lambda"""
        g = Gramatica()
        g.setear("S:a Q\nQ:b R\nQ:c R\nR:d")
        self.assertTrue(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("abd"))
        self.assertTrue(g.evaluar_cadena("acd"))
        self.assertFalse(g.evaluar_cadena(""))

    def test_con_reglas_innecesarias(self):
        """Prueba una gramática con reglas innecesarias"""
        g = Gramatica()
        g.setear("S:P a\nP:P\nP:b")
        self.assertTrue(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("ba"))
        self.assertFalse(g.evaluar_cadena("c"))

    def test_con_simbolos_inaccesibles(self):
        """Prueba una gramática con símbolos inaccesibles"""
        g = Gramatica()
        g.setear("S:a Q\nQ:b Q\nQ:c\nP:d")
        self.assertTrue(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("abc"))
        self.assertFalse(g.evaluar_cadena("adc"))

    def test_con_no_terminales_no_generativos(self):
        """Prueba una gramática con no terminales no generativos"""
        g = Gramatica()
        g.setear("S:Q a\nS:P\nQ:c\nP:P x")
        self.assertTrue(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("ca"))
        self.assertFalse(g.evaluar_cadena("ac"))

    """ Test no ll(1) """

    def test_recursion_izquierda(self):
        """Prueba una gramática con recursión a la izquierda"""
        g = Gramatica()
        g.setear("S:Q a\nQ:A\nQ:B\nA:b\nB:b")
        self.assertFalse(g.EsLL1)
        self.assertFalse(g.evaluar_cadena("ba"))

    def test_no_ll1_sin_recursion_derecha(self):
        """Gramática sin recursión a derecha"""
        g = Gramatica()
        g.setear("S:Q a\nQ:Q b")
        self.assertFalse(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("ab"))
        self.assertFalse(g.evaluar_cadena("ba"), "Cadena inválida debido a los conjuntos FIRST")

    def test_no_ll1_con_recursion_derecha(self):
        """Gramática con recursión a la izquierda"""
        g = Gramatica()
        g.setear("S:a S\nS:Q\nQ:Q b")
        self.assertFalse(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("ab"))
        self.assertTrue(g.evaluar_cadena("b"))
        self.assertFalse(g.evaluar_cadena("ba"))

    def test_no_ll1_con_lambda(self):
        """Gramática con lambda"""
        g = Gramatica()
        g.setear("S:Q a\nS:P\nP:b\nQ:b\nQ:lambda")
        self.assertFalse(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("ab"))
        self.assertTrue(g.evaluar_cadena("a"))
        self.assertTrue(g.evaluar_cadena(""))

    def test_no_ll1_sin_lambda(self):
        """Gramática sin lambda"""
        g = Gramatica()
        g.setear("S:a Q\nQ:b R\nQ:c R\nR:R d")
        self.assertFalse(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("abd"))
        self.assertFalse(g.evaluar_cadena("bc"))

    def test_no_ll1_con_reglas_innecesarias(self):
        """Gramática con una regla inaccesible"""
        g = Gramatica()
        g.setear("S:P a\nS:Q\nQ:b\nP:P\nP:b")
        self.assertFalse(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("ba"))
        self.assertFalse(g.evaluar_cadena("ab"))

    def test_no_ll1_con_simbolos_inaccesibles(self):
        """Gramática con un símbolo terminal inaccesible"""
        g = Gramatica()
        g.setear("S:a Q\nQ:Q b\nP:d")
        self.assertFalse(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("ab"))
        self.assertFalse(g.evaluar_cadena("d"))

    def test_no_ll1_con_no_terminales_no_generativos(self):
        """Gramática con un no terminal no generativo"""
        g = Gramatica()
        g.setear("S:Q a\nS:P\nQ:c\nP:P c")
        self.assertFalse(g.EsLL1)
        self.assertTrue(g.evaluar_cadena("ca"))
        self.assertFalse(g.evaluar_cadena("b"))
