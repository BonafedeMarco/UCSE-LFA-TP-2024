class Gramatica:

    def __init__(self):
        """
        TODO: Docstrings
        """
        self.EsLL1 = False
        self.reglas = {}
        self.debug = True



    def __str__(self):
        """
        TODO: Docstrings
        """
        for nt in self.reglas:
            print(f"{nt}:")
            for prod in (self.reglas[nt]['producciones']):
                print(f"  {prod}:{self.reglas[nt]['producciones'][prod]}")
            print(f"  Follows:{self.reglas[nt]['follow']}")
            
        return f"EsLL(1)? => {self.EsLL1}"




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
            nuevas_reglas[antecedente]["producciones"].update({consecuente: {"first":[],"select":[]}}) 
        
        # TODO: Detección y resolución de problemas detectados en la gramática
        # Símbolos inaccesibles desde el axioma
        nt_antecedente = []
        nt_consecuente = []
        for nt in nuevas_reglas:
            nt_antecedente.append(nt)
            for produccion in nuevas_reglas[nt]["producciones"]:
                simbolos = produccion.split()
                for simbolo in simbolos:
                    if simbolo.isupper() and simbolo != nt:
                        nt_consecuente.append(simbolo)

        inaccesibles = set(nt_antecedente[1:]) - set(nt_consecuente)
        
        if self.debug:
            print(f"Inaccesibles: {inaccesibles}") 

        for simbolo in inaccesibles:
            nuevas_reglas.pop(simbolo)

        # Reglas de producción innecesarias
        producciones_innecesarias = []
        for nt in nuevas_reglas:
            for produccion in nuevas_reglas[nt]["producciones"]:
                if nt == produccion:
                    producciones_innecesarias.append(nt)
        
        if self.debug:
            print(f"Innecesarias: {producciones_innecesarias}")
        
        for nt in producciones_innecesarias:
            nuevas_reglas[nt]["producciones"].pop(nt)
        
        # No terminales no generativos

        # TODO: Obtener First, Follow y Select
        # evaluar si es o no LL1 para self.EsLL1

        # Seteo
        self.reglas = nuevas_reglas



    def evaluar_cadena(self, cadena):
        """
        TODO: Docstrings
        """
