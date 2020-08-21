def imprimeResultados(li):
    with open('Resultado_Metodos_' + result + '.json', 'w') as file:
        file.write(str(li))
        
def print_res(params, lista_metodos):
    
    global result, ext
    result, ext = params.split('.')
    
    imprimeResultados(lista_metodos)