import pandas as pd

#Colunas que não interessam
notinteresting = ['hora', 'dia', 'ano', 'mes']

#Definindo Dicionario para armazenar a classificação das colunas com seu respectivo tipo: Radiação, TemperaturaUmidade, Outros
colunas = {}
colunas['Rad'] = []
colunas['TempUmi'] = []
colunas['Outros'] = []

#Classificando as colunas
def identColunas():

    sinonimosTemperaturaUmidade = ['temperatura', 'temperature', 'umidade', 'humidity']
    sinonimosRadiacao = ['radiacao', 'radiation']

    for collumn in dataset:
        if collumn.lower() not in notinteresting:
            if(collumn.lower() in sinonimosTemperaturaUmidade):
                colunas['TempUmi'].append(collumn)
            
            elif(collumn.lower() in sinonimosRadiacao):
                colunas['Rad'].append(collumn)
                
            else:
                colunas['Outros'].append(collumn)


def validarFaixa(inicio, fim, col):
    faixa = fim-inicio
    end = (len(dataset.loc[:,col])-1)

    #Se fim da faixa for maior que o tamanho do dataset
    if(fim > end):
        fim = end
    
    countLines = 0
    soma = 0
    cont = 0
    global media
    #Conta quantos valores null tem na coluna inteira
    for i in range(inicio, fim, 1):
        if(pd.isnull(dataset.loc[i,col])):
            countLines += 1

    #Calcula média
    if countLines != faixa:
        for i in range(inicio, fim, 1):
            if(not pd.isnull(dataset.loc[i,col])):
                soma += dataset.loc[i,col]
                cont += 1
        media = soma / cont

    #Se igual, então a faixa inteira é nula
    #Atribui o valor da média para a primeira linha da faixa
    elif countLines == faixa:
        dataset.loc[inicio, col] = media
          
def carrega_faixa():
    identColunas()
    #Definindo valores das faixas de análise
    #Foi definido: 50
    #Passível de alteração no futuro
    for collumn in dataset:
        start = 0
        faixa = 50
        if collumn.lower() not in notinteresting:
            while(start <= len(dataset.loc[:,collumn])-1):
                validarFaixa(start, (faixa-1), collumn)
                start += 50
                faixa += 50

def imprimeResultCSV(params):
    dataset.to_csv((params), sep=',', index=False, na_rep='NaN')

def correct_dateset(params):
    global dataset
    global media

    dataset = pd.read_csv(str(params), sep=',')

    carrega_faixa()
    imprimeResultCSV(str(params))