class Gramatica:

    def __init__(self):
        """
        TODO: Docstrings
        """
        self.EsLL1 = False
        self.reglas = {}



    def __str__(self):
        """
        TODO: Docstrings
        """
        return f"{self.reglas}"



    def setear(self, gramatica):
        """
        TODO: Docstrings
        """
        nuevas_reglas = {}
        
        # Parsing inicial
        reglas = gramatica.split("\n")
        for regla in reglas:
            antecedente, consecuente = regla.split(":")
            nuevas_reglas.setdefault(antecedente, {"producciones":{},"follow":[]})
            nuevas_reglas[antecedente]["producciones"].update({consecuente: [[],[]]}) 
        
        # TODO: Detección y resolución de problemas detectados en la gramática

        # TODO: Obtener First, Follow y Select

        # Seteo
        self.reglas = nuevas_reglas



    def evaluar_cadena(self, cadena):
        """
        TODO: Docstrings
        """
