import pandas as pd
import json
from collections import OrderedDict

def jsonDefault(OrderedDict):
    return OrderedDict.__dict__

class Item:
    def __init__(self, indice, tipo_var, begin_faixa, end_faixa, porcentagem, tipo_falha, falha_dados_relacionados):
        self.indice = indice
        self.tipo_var = tipo_var
        self.begin_faixa = begin_faixa
        self.end_faixa = end_faixa
        self.porcentagem = porcentagem
        self.tipo_falha = tipo_falha
        self.falha_dados_relacionados = falha_dados_relacionados

    def __repr__(self):
        return json.dumps(self, default=jsonDefault, indent=4, sort_keys=True)

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

#Identificando variáveis relacionadas
def identRelacao(linha, coluna):

    if(coluna in colunas['Rad']):
        key = 'Rad'
    elif(coluna in colunas['TempUmi']):
        key = 'TempUmi'
    else:
        key = 'Outros'

    for value in colunas[key]:
        if value != coluna:
            if(not pd.isnull(dataset.loc[linha,value])):
                return True

    return False
            
#Identificando as falhas em cada faixa de registros
def identFalhas(start, collumn, faixa, porcentage):
    cont = 0
    var_relacionada = True
    for i in range(start, len(dataset.loc[:,collumn]), 1):
        if(pd.isnull(dataset.loc[i,collumn])):
            cont = cont + 1
            if(var_relacionada == True):
                var_relacionada = identRelacao(i, collumn)

        if(i > 0 and (i+1) % faixa == 0):
            x = (cont*100)/(faixa)
            startFaixa = (i+1) - (faixa)
            endFaixa = i
            if(x >= porcentage):
                return True, startFaixa, endFaixa, x, var_relacionada
            else:
                return False, startFaixa, endFaixa, x, var_relacionada
        
        elif(i == len(dataset.loc[:,collumn])-1):
            x = (cont*100)/(faixa)
            startFaixa = start
            endFaixa = i+1
            if(x >= porcentage):
                return True, startFaixa, endFaixa, x, var_relacionada
            else:
                return False, startFaixa, endFaixa, x, var_relacionada

def carregaResultadosFalhas(zone, percent):
    #Iniciando a lista
    lista = []
    #pre-setando parametros
    faixa = zone
    porcentage = percent

    indice = -1

    identColunas()

    for collumn in dataset:
        indice = indice + 1
       
        if collumn.lower() not in notinteresting:
            tipo_var = collumn
        
            start = 0
            while(start <= len(dataset.loc[:,collumn])-1):
                bol, inicio, fim, porcent, var_relacionada = identFalhas(start, collumn, faixa, porcentage)

                if(var_relacionada == True):
                    var_relacionada = 'Relacionada'
                else:
                    var_relacionada = 'Nao Relacionada'

                if(bol == True):
                    
                    tipo_falha = 'Sequencial'
                    lista.append(Item(indice, tipo_var, inicio, fim, porcent, tipo_falha, var_relacionada))
                else:
                    tipo_falha = 'Aleatorio'
                    lista.append(Item(indice, tipo_var, inicio, fim, porcent, tipo_falha, var_relacionada))

                start = start + faixa
    
    return lista

def fault_ident(params, zone, percent):

    global dataset
    
    dataset = pd.read_csv(str(params), sep=',')
    lista_dados = carregaResultadosFalhas(int(zone), int(percent))
    
    return lista_dados