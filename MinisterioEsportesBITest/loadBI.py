import pandas as pd
import numpy as np
import cgi, cgitb
import os
import json
from pprint import pprint as pp
#cgitb.enable()  # debug

def stringToCurrency(dataframe):
    dataframe = dataframe.str.replace('R\$', '').replace(' ', '')
    dataframe = dataframe.str.replace('.', '')
    dataframe = dataframe.str.replace(',','.')
    dataframe = dataframe.convert_objects(convert_numeric=True)
    
    return dataframe

def to_JSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
            
script_dir = os.path.dirname(__file__)
'''
projeto_path = "relatorio/SLIE_200{}.csv".format(i)
abs_file_path = os.path.join(script_dir, projeto_path)
projeto = pd.read_csv(abs_file_path, sep="\t", index_col=0)
'''
#pp(projeto['nome do proponente'])
year = ''
patrocinado_path = ''
normalizationFactor = 100

for i in range(8,17):#2008 a 2016
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
        pp("Nao foi encontrado o arquivo {}".format(patrocinado_path))
    
    #Quantas vezes um projeto recebeu doacoes
    #projDonationHist = patrocinado.ix[:, 5].value_counts()
    
    try:
        patrocinado.ix[:,4] = stringToCurrency(patrocinado.ix[:,4])
        
        #Quantidade doada pelas empresas 
        pathCorpDonation = "patrocinado/empresasJSON/corpDonationAmount_{}.json".format(year)        
        corpDonationAmount = patrocinado.groupby(patrocinado.ix[:,0]).agg({"Valor Captador":np.sum})
        abs_file_path = os.path.join(script_dir, pathCorpDonation)
        corpDonationAmount = corpDonationAmount.sort_index(by="Valor Captador", ascending=False)
        corpDonationAmountSize = len(corpDonationAmount) + 1
        corpDonationAmount["id"] = range(1, corpDonationAmountSize)
        #corpDonationAmount.to_json(path_or_buf=abs_file_path)
        
        #Quantidade de doação recebida pelos projetos
        pathProjDonation = "patrocinado/projetosJSON/projDonationAmount_{}.json".format(year)
        projDonationAmount = patrocinado.groupby(patrocinado.ix[:,5]).agg({"Valor Captador":np.sum})
        abs_file_path = os.path.join(script_dir, pathProjDonation)
        projDonationAmount = projDonationAmount.sort_index(by="Valor Captador", ascending=False)
        projDonationAmount["id"] = range(1, len(projDonationAmount) + 1)
        #projDonationAmount.to_json(path_or_buf=abs_file_path)

        #Relacionamento entre empresa e projetos
        pathNetworkDonation = "patrocinado/grafosJSON/pathNetworkDonation_{}.json".format(year)
        abs_file_path = os.path.join(script_dir, pathNetworkDonation)
        
        nodes = []
        edges = []
        mapNet = {}

        for e, p, d in zip(patrocinado.ix[:,0], patrocinado.ix[:,5], patrocinado.ix[:,4]):
            relation = "{}$$${}".format(e, p)      
            try:
                mapNet[relation] += d
            except KeyError:
                mapNet[relation] = d
                
        for c in corpDonationAmount.iterrows():
            corpName = str(c[0])
            amount = c[1]["Valor Captador"]
            idCorp = int(c[1]["id"])
            node = dict({"id":idCorp, "title":corpName, "value":amount, "group":"empresa"})
            nodes.append(node)
        for p in projDonationAmount.iterrows():
            projName = str(p[0])
            amount = p[1]["Valor Captador"]
            idProj = int(p[1]["id"])+corpDonationAmountSize
            node = dict({"id":idProj, "title":projName, "value":amount, "group":"projeto"})
            nodes.append(node)
            
        for k in mapNet.keys():
            s = k.split("$$$")
            corpName = str(s[0])
            projName = str(s[1])
            
            if corpName!="nan" and projName!="nan":
                idCorp = int(corpDonationAmount["id"][corpName])
                idProj = int(projDonationAmount["id"][projName]+corpDonationAmountSize)
                title = str(mapNet[k]).replace(".", ",")
                title = "R$ {}".format(title)
                edges.append({"from":idCorp, "to":idProj, "value":title})
                

        listJSON = []
        listJSON.append({"nodes": nodes})
        listJSON.append({"edges": edges})
        
        with open(abs_file_path, 'w') as f:
            json.dump(listJSON, f)
    except:
        #pp(e)
        pp("Dataframe não preenchido")
        
print("FIM!")