import pandas as pd
import numpy as np
import cgi, cgitb
import os
from pprint import pprint as pp
#cgitb.enable()  # debug

def stringToCurrency(dataframe):
    dataframe = dataframe.str.replace('R\$', '').replace(' ', '')
    dataframe = dataframe.str.replace('.', '')
    dataframe = dataframe.str.replace(',','.')
    dataframe = dataframe.convert_objects(convert_numeric=True)
    
    return dataframe

script_dir = os.path.dirname(__file__)
'''
projeto_path = "relatorio/SLIE_200{}.csv".format(i)
abs_file_path = os.path.join(script_dir, projeto_path)
projeto = pd.read_csv(abs_file_path, sep="\t", index_col=0)
'''
#pp(projeto['nome do proponente'])
year = ''
patrocinado_path = ''

for i in range(8,17):
    patrocinado = pd
    if i < 10:
        year = "200{}".format(i)
        patrocinado_path = "patrocinado/SLIE_{}.csv".format(year)
    else:
        year = "20{}".format(i)
        patrocinado_path = "patrocinado/SLIE_{}.csv".format(year)
        
    abs_file_path = os.path.join(script_dir, patrocinado_path)
    try:
        patrocinado = pd.read_csv(abs_file_path, sep="\t", index_col=0)
    except:
        pp("Nao foi encontrado o arquivo.{}".format(patrocinado_path))
    
    #Quantas vezes um projeto recebeu doacoes
    #projDonationHist = patrocinado.ix[:, 5].value_counts()
    
    try:
        #Quantidade doada pelas empresas 
        pathCorpDonation = "patrocinado/empresasJSON/corpDonationAmount_{}.json".format(year)
        patrocinado.ix[:,4] = stringToCurrency(patrocinado.ix[:,4])
        corpDonationAmount = patrocinado.groupby(patrocinado.ix[:,0]).agg({"Valor Captador":np.sum})
        abs_file_path = os.path.join(script_dir, pathCorpDonation)
        corpDonationAmount = corpDonationAmount.sort_index(by="Valor Captador", ascending=False)
        corpDonationAmount.to_json(path_or_buf=abs_file_path)
        
        #Quantidade de doação recebida pelos projetos
        pathProjDonation = "patrocinado/projetosJSON/projDonationAmount_{}.json".format(year)
        projDonationAmount = patrocinado.groupby(patrocinado.ix[:,5]).agg({"Valor Captador":np.sum})
        abs_file_path = os.path.join(script_dir, pathProjDonation)
        projDonationAmount = projDonationAmount.sort_index(by="Valor Captador", ascending=False)
        projDonationAmount.to_json(path_or_buf=abs_file_path)
    except:
        pp("Dataframe nao preenchido")
        
print("FIM!")