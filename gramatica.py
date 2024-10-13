from copy import copy

class Gramatica:

    def __init__(self):
        """
        TODO: Docstrings
        """
        self.EsLL1 = True
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
        
        # Detección y resolución de problemas detectados en la gramática
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
        generativos = set()

        algo_nuevo = True
        while algo_nuevo:
            algo_nuevo = False
            for nt in nuevas_reglas:
                for produccion in nuevas_reglas[nt]["producciones"]:
                    if nt not in generativos:
                        cc_gen = [c in generativos for c in produccion.split() if c.isupper()]
                        if all(cc_gen):
                            algo_nuevo = True
                            generativos.add(nt)
        
        no_generativos = set(nuevas_reglas.keys()) - generativos

        if self.debug:
            print(f"NT generativos: {generativos}")
            print(f"NT no generativos: {no_generativos}")
        
        for ng in no_generativos:
            nuevas_reglas.pop(ng)
        
        reglas_superfluas = []
        for nt in nuevas_reglas:
            for produccion in nuevas_reglas[nt]["producciones"]:
                simbolos = produccion.split()
                for simbolo in simbolos:
                    if simbolo in no_generativos:
                        reglas_superfluas.append((nt, produccion))
                        break

        for nt, produccion in reglas_superfluas:
            nuevas_reglas[nt]["producciones"].pop(produccion)

        # Seteo
        self.reglas = nuevas_reglas

        # Obtener First, Follow y Select
        # First
        for nt in self.reglas:
            self.obtener_first(nt)

        # TODO: Follow
        distinguido = None
        if self.reglas:
            distinguido = [nt for nt in self.reglas.keys()][0]
        if distinguido is not None:
            self.reglas[str(distinguido)]["follow"].append("$")



        # Select
        for nt in self.reglas:
            for produccion in self.reglas[nt]["producciones"]:
                first = copy(self.reglas[nt]["producciones"][produccion]["first"])
                select = []
                if "lambda" in first:
                    first.remove("lambda")
                    first.extend(self.reglas[nt]["follow"])
                select.extend(first)
                self.reglas[nt]["producciones"][produccion]["select"] = select

        # Es LL1 ?
        while self.EsLL1:
            for nt in self.reglas:
                selects = []
                for produccion in self.reglas[nt]["producciones"]:
                    selects.extend(self.reglas[nt]["producciones"][produccion]["select"])
                self.EsLL1 = len(selects) == len(set(selects))
            break
    

    def obtener_first(self, nt):
        firsts = []
        for produccion in self.reglas[nt]["producciones"]:
            if len(self.reglas[nt]["producciones"][produccion]["first"]) == 0:
                simbolos = produccion.split()
                for simbolo in simbolos:
                    if simbolo.islower():
                        self.reglas[nt]["producciones"][produccion]["first"].append(simbolo)
                        firsts.append(simbolo)
                    else:
                        firsts.extend(self.obtener_first(simbolo))
                        self.reglas[nt]["producciones"][produccion]["first"] = list(set(firsts))
                    if "lambda" not in firsts:
                        break
        
        return firsts

    

    def evaluar_cadena(self, cadena):

        pila = ["$", next(iter(self.reglas))]
        entrada = cadena + "$"
        indice_entrada = 0
        no_valido = False

        while pila:
            X = pila.pop()
            if indice_entrada < len(entrada):
                a = entrada[indice_entrada]
            else:
                print("Fin de la cadena inesperado")
                no_valido = True
        
            if X.islower() or X == "$":
                if X == a:
                    indice_entrada += 1
                else:
                    print(f"Se esperaba {X}, pero se encontró {a}")
                    no_valido = True
            else:
                producciones_posibles = [p for p in self.reglas[X]["producciones"] if a in self.reglas[X]["producciones"][p]["select"]]

                if not producciones_posibles:
                    print(f"No hay producción para {X} y {a}")
                    no_valido = True

                if len(producciones_posibles) > 1:
                    print("La gramática no es LL(1)")
                    self.EsLL1 = False
                    no_valido = True

                if producciones_posibles:
                    produccion = producciones_posibles[0]
                    nueva_produccion = produccion.split()[::-1]
                    pila.extend(nueva_produccion)

        if no_valido:
            return False
        else:
            return True
