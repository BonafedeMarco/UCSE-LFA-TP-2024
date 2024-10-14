from copy import copy

class Gramatica:

    def __init__(self):
        self.EsLL1 = True
        self.reglas = {}
        self.debug = False



    def __str__(self):
        max_len_consecuente = 0
        max_len_fi = 0
        max_len_fo = 0
        max_len_se = 0
        padding_spaces = 1
        has_lambda = False

        for nt in self.reglas:
            if max_len_fo < len(self.reglas[nt]["follow"]):
                max_len_fo = len(self.reglas[nt]["follow"])
            
            for produccion in self.reglas[nt]["producciones"]:
                if max_len_consecuente < len(produccion):
                    max_len_consecuente = len(produccion)

                if "lambda" in self.reglas[nt]["producciones"][produccion]["first"]:
                    has_lambda = True

                if max_len_fi < len(self.reglas[nt]["producciones"][produccion]["first"]):
                    max_len_fi = len(self.reglas[nt]["producciones"][produccion]["first"])

                
                if max_len_se < len(self.reglas[nt]["producciones"][produccion]["select"]):
                    max_len_se = len(self.reglas[nt]["producciones"][produccion]["select"])
        
        max_len_fi = (max_len_fi * 3) + (max_len_fi - 1) * 2 + 2
        max_len_fo = (max_len_fo * 3) + (max_len_fo - 1) * 2 + 2
        max_len_se = (max_len_se * 3) + (max_len_se - 1) * 2 + 2

        if has_lambda:
            max_len_fi += 5

        line_length = 3 + max_len_consecuente + max_len_fi + max_len_fo + max_len_se + padding_spaces * 5 + 9

        print("-" * line_length)
        print("|" + " " * padding_spaces, end = "")
        print("A", end = "")
        print(" " * padding_spaces + "|", end = "")
        print(" " * padding_spaces + "C" + " " * (max_len_consecuente - len("C")), end = "")
        print(" " * padding_spaces + "|", end = "")
        print(" " * padding_spaces + "Fi" + " " * (max_len_fi - len("Fi")) , end = "")
        print(" " * padding_spaces + "|", end = "")
        print(" " * padding_spaces + "Fo" + " " * (max_len_fo - len("Fo")), end = "")
        print(" " * padding_spaces + "|", end = "")
        print(" " * padding_spaces + "Se" + " " * (max_len_se - len("Se")), end = "")
        print(" " * padding_spaces + "|")
        print("-" * line_length)
        for nt in self.reglas:
            first_line = True
            fo = str(self.reglas[nt]["follow"])
            for produccion in self.reglas[nt]["producciones"]:
                fi = str(self.reglas[nt]["producciones"][produccion]["first"])
                se = str(self.reglas[nt]["producciones"][produccion]["select"])
                print("|" + " " * padding_spaces, end = "")
                if first_line:
                    print(nt, end = "")
                else:
                    print(" " * padding_spaces, end = "")
                print(" " * padding_spaces + "|", end = "")
                print(" " * padding_spaces + produccion + " " * (max_len_consecuente - len(produccion)), end = "")
                print(" " * padding_spaces + "|", end = "")
                print(" " * padding_spaces + fi + " " * (max_len_fi - len(fi)) , end = "")
                print(" " * padding_spaces + "|", end = "")
                if first_line:
                    print(" " * padding_spaces + fo + " " * (max_len_fo - len(fo)), end = "")
                else:
                    print(" " * padding_spaces + " " * max_len_fo, end = "")
                print(" " * padding_spaces + "|", end = "")
                print(" " * padding_spaces + se + " " * (max_len_se - len(se)), end = "")
                print(" " * padding_spaces + "|")
                first_line = False
            print("-" * line_length)

        return f"\nEsLL(1)? => {self.EsLL1}"



    def setear(self, gramatica):
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
                    if simbolo[0].isupper() and simbolo != nt:
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
                        cc_gen = [c in generativos for c in produccion.split() if c[0].isupper()]
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
            self.obtener_firsts(nt)

        # Follow
        distinguido = [nt for nt in self.reglas.keys()][0]
        self.reglas[distinguido]["follow"].append("$")

        for nt_fol in self.reglas:
            self.obtener_follows(nt_fol)

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
        for nt in self.reglas:
            selects = []
            for produccion in self.reglas[nt]["producciones"]:
                selects.extend(self.reglas[nt]["producciones"][produccion]["select"])
            self.EsLL1 = len(selects) == len(set(selects))
            if not self.EsLL1:
                break
    


    def obtener_firsts(self, nt):
        firsts = []
        for produccion in self.reglas[nt]["producciones"]:
            if len(self.reglas[nt]["producciones"][produccion]["first"]) == 0:
                simbolos = produccion.split()
                for simbolo in simbolos:
                    if simbolo[0].isupper():
                        firsts = []
                        firsts.extend(self.obtener_firsts(simbolo))
                        self.reglas[nt]["producciones"][produccion]["first"] = list(set(firsts))
                    else:
                        self.reglas[nt]["producciones"][produccion]["first"].append(simbolo)
                        firsts.append(simbolo)
                    if "lambda" not in firsts:
                        break
        
        return firsts


    
    def obtener_follows(self, nt_fol):
        follows = []
        for nt in self.reglas:
            for produccion in self.reglas[nt]["producciones"]:
                simbolos = produccion.split()
                if nt_fol in simbolos and nt != nt_fol:
                    for s_index, simbolo in enumerate(simbolos):
                        if simbolo == nt_fol:
                            ext = []

                            #################################

                            pos = s_index + 1

                            while True:

                                if pos < len(simbolos):
                                    lookup = simbolos[pos]
                                    conjunto = "first"
                                else:
                                    lookup = nt
                                    conjunto = "follow"

                                if lookup[0].isupper(): # Le sigue un NO Terminal
                                    if conjunto == "first":
                                        for subprod in self.reglas[lookup]["producciones"]:
                                            ext.extend(self.reglas[lookup]["producciones"][subprod]["first"])
                                        
                                    else:
                                        self.obtener_follows(lookup)
                                        ext.extend(self.reglas[lookup]["follow"])
                                
                                else: # Le sigue un Terminal
                                    ext.append(lookup) 

                                if "lambda" not in ext:
                                    break

                                ext.remove("lambda")
                                pos += 1

                            #################################
                            
                            follows.extend(ext)
        
        # Para remover duplicados
        new_follows = list(set(follows))
        new_follows.extend(self.reglas[nt_fol]["follow"])

        self.reglas[nt_fol]["follow"] = list(set(new_follows))

        return follows



    def evaluar_cadena(self, cadena):
        if self.EsLL1:
            pila = ["$", next(iter(self.reglas))]
            entrada = cadena + "$"
            indice_entrada = 0
            cadena_valida = True

            while pila:
                X = pila.pop()
        
                if X == 'lambda':
                    continue

                if indice_entrada < len(entrada):
                    a = entrada[indice_entrada]
                else:
                    print("Fin de la cadena inesperado")
                    cadena_valida = False
            
                if X[0].islower() or X == "$":
                    if X == a:
                        indice_entrada += 1
                    else:
                        print(f"Se esperaba {X}, pero se encontró {a}")
                        cadena_valida = False
                else:
                    producciones_posibles = [p for p in self.reglas[X]["producciones"] if a in self.reglas[X]["producciones"][p]["select"]]

                    if not producciones_posibles:
                        print(f"No hay producción para {X} y {a}")
                        cadena_valida = False

                    if producciones_posibles:
                        produccion = producciones_posibles[0]
                        nueva_produccion = produccion.split()[::-1]
                        pila.extend(nueva_produccion)
        else:
            print("La gramática no es LL(1)")
            cadena_valida = False

        return cadena_valida
