# Estructura de gramática utilizada internamente

* las reglas son almacenadas en diccionarios anidados
* las claves del primer nivel son los no terminales
* el valor es un diccionario que contiene:
    * un diccionario con todas las reglas que tengan ese NT como antecedente
    * un array con los follow
* el sub diccionario de clave "producciones" tiene una entrada por consecuente
* cada consecuente es un diccionario con arrays para:
    * el conjunto de los first
    * el conjunto de los select


```
reglas = {
  NT_0 : {
    "producciones" : {
      consecuente_0 : {
        "first" : [],
        "select" : []
      },
      consecuente_1 : {
        "first" : [],
        "select" : []
      },
      ...
    },
    "follow" : []
  },
  ...
}
```
