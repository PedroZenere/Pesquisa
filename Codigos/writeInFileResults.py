def writeInFileResults(params, lista_metodos):    
    with open('../Input/Resultado_Metodos_' + params + '.json', 'w') as file:
        file.write(str(lista_metodos))