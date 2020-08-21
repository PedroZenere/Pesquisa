import pandas as pd
import sys
import os
from os.path import isfile, join, basename

#Importando funções..
from select_method import charge_data
from correct_dataset import correct_dateset
from fault_identification import fault_identification
from writeInFileResults import writeInFileResults
    
def gap_identification(zone, percent):
    data_list = fault_identification(name, zone, percent)
    return data_list

def createParams(data_list):
    methods_list = charge_data(name, data_list)
    return methods_list

def get_file(ext):
    for nome_arquivo in os.listdir(path):
        nome, extensao = os.path.splitext(nome_arquivo)
        if(nome == 'Resultado_Metodos_'+filename[0] and extensao == ext ):
            return nome+extensao

def execFramework(methods):
    os.system('java -jar Fficsed/Fficsed.jar ' + param[0] + ' ' + methods)

def main():

    global path, param, name, filename
    path = '../Input'
    param = sys.argv[1:]
    name = param[0]
    filename = name.split('/')[2]
    resultName = filename.split('.')[0]
    
    #Parametro para identificacao das falhas: Tamanho da faixa, porcentagem de erro desejada
    zone, percent = param[1], param[2]

    correct_dateset(name)
    data_list = gap_identification(zone, percent)
    methods_list = createParams(data_list)
    writeInFileResults(resultName, methods_list)

    methods = get_file('.json')

    # execFramework(methods)

if __name__ == "__main__":
    main()

