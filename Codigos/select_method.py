import pandas as pd
import json
import sys
import os
from collections import OrderedDict

def jsonDefault(OrderedDict):
    return OrderedDict.__dict__

class Tipo_Metodo:
    def __init__(self, indice, begin_faixa, end_faixa, metodo):
        self.indice = indice
        self.begin_faixa = begin_faixa
        self.end_faixa = end_faixa
        self.metodo = metodo

    def __repr__(self):
        return json.dumps(self, default=jsonDefault, indent=4, sort_keys=True)
    
#Colunas que não interessam
notinteresting = ['hora', 'dia', 'ano', 'mes']

#Definindo Dicionario para armazenar a classificação das colunas com seu respectivo tipo: Radiação, TemperaturaUmidade, Outros
colunas = {}
colunas['Rad'] = []
colunas['TempUmi'] = []
colunas['Outros'] = []

#---------------------------------------------- SELECIONA METODO --------------------------

def tipoColuna(variavel):
    if(variavel in colunas['Rad']):
        return 'Radiacao'
    elif(variavel in colunas['TempUmi']):
        return 'TemperaturaUmidade'
    else:
        return 'Outros'

def selecionaMetodo(value):
    
        variavel = tipoColuna(value.tipo_var)
        if value.tipo_falha == 'Aleatorio':
            if value.falha_dados_relacionados == 'Relacionada':
                return 'Media'
            else:
                if(variavel == 'Radiacao'):
                    return 'RLM'
                else:
                    return 'Media'
        else:
            if value.falha_dados_relacionados == 'Relacionada':
                if(variavel == 'Radiacao' or variavel == 'TemperaturaUmidade'):
                    return 'SVM'
                else:
                    if(value.porcentagem < 33):
                        return 'Media'
                    else:
                        return 'SVM'
            else:
                if(variavel == 'Radiacao'):
                    return 'RLM'
                elif(variavel == 'TemperaturaUmidade'):
                    return 'SVM'
                else:
                    return 'Media'

def carregaListaMetodos(lista_dados):

    lista_metodos = []

    for value in lista_dados:
        metodo = selecionaMetodo(value)
    
        lista_metodos.append(Tipo_Metodo(value.indice, value.begin_faixa, value.end_faixa, metodo))

    return lista_metodos

def charge_data(params, lista_dados):

    lista_metodos = carregaListaMetodos(lista_dados)
    return lista_metodos
    
