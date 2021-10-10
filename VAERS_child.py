!pip install -U -q PyDrive
from google.colab import drive
drive.mount('/content/drive')
!mkdir /content/drive/MyDrive/Analyse_Myocardites/

YB = 1990
YE = 2011
import pandas as pd
datas = []
for year in range (YB, YE):
  ssYear = str(year)
  nameFiles = [ssYear+"VAERSDATA.csv",ssYear+"VAERSSYMPTOMS.csv",ssYear+"VAERSVAX.csv"]
  datasYear = []
  print(year)
  for nameFile in nameFiles :
    df = pd.read_csv('https://raw.githubusercontent.com/emmanuelleDarles/Datas_Myocardites/main/'+nameFile, encoding='cp1252')
    datasYear.append(df)
  datas.append(datasYear)
print("Finish")

import math

def extractChild(df, age_limit):
  return df[df["AGE_YRS"]<=age_limit]

def computeNbSearchSymptom(dfChild, dfSymptoms, symptom):
  nb = 0
  int_df = pd.merge(dfChild, dfSymptoms, how ='inner', on =['VAERS_ID', 'VAERS_ID'])
  ID = []
  listColumns = ["SYMPTOM"+str(i) for i in range(1,6)]
  for c in listColumns :
    int_dfS = int_df[int_df[c]==symptom]
    for i in range(0,len(int_dfS)):
      if int_dfS.iloc[i]["VAERS_ID"] not in ID :
        nb+=1
        ID.append(int_dfS.iloc[i]["VAERS_ID"])
  print(ID)
  return nb

def searchSymptomEvolution(age_limit, symptom):
  datasChild = []
  sy = dict()
  year = YB
  for i in range(0,len(datas)) :
    dfChild = extractChild(datas[i][0],age_limit)
    datasChild.append(dfChild)
    nbSyYear = computeNbSearchSymptom(dfChild, datas[i][1], symptom)
    sy.update({year:[len(dfChild["VAERS_ID"]),nbSyYear]})
    year+=1
  return sy

myo = searchSymptomEvolution(18,"Myocarditis")
print(myo)


import matplotlib.pyplot as plt
import seaborn as sns

def plotEvolution(df, title, yb, ye, nameFile):
  plt.figure(figsize=(10,5))
  sns.set_style('darkgrid')
  years = [i for i in range(yb,ye)]
  nb = [df[i][1] for i in range(yb,ye)]
  plt.bar(years,nb)
  plt.title(title)
  plt.xlabel("Année")
  plt.ylabel("Nombre de myocardites susceptibles")
  plt.xticks([i for i in range(yb,ye,2)])
  plt.savefig("/content/drive/MyDrive/Analyse_Myocardites/"+nameFile)
  plt.show()

plotEvolution(myo,"Evolution temporelle des myocardites dans la VAERS chez les moins de 18 ans", YB, YE, "EvolutionMyocarditesVAERS.png")

def computeVariation(df,yb,ye):
  variation = []
  for y in range(yb,ye-1):
    a = df[y][1]/float(df[y][0])
    b = df[y+1][1]/float(df[y+1][0])
    if a!=0 :
      variation.append((b/a)*100)
    else : variation.append(0)
  return variation

def plotVariation(df, title, yb, ye, nameFile):
  plt.figure(figsize=(10,5))
  sns.set_style('darkgrid')
  variation = computeVariation(df,yb,ye)
  years = [i for i in range(yb+1,ye)]
  plt.bar(years,variation)
  plt.title(title)
  plt.xlabel("Année")
  plt.ylabel("Variation (%)")
  plt.xticks([i for i in range(yb,ye,2)])
  plt.savefig("/content/drive/MyDrive/Analyse_Myocardites/"+nameFile)
  plt.show()

plotVariation(myo,"Variation du nombre de myocardites (en %) déclarées dans la VAERS \n(normalisée sur le nombre de déclarants)\n chez les moins de 18 ans par rapport à l'année précédente", YB, YE, "VariationMyocarditesVAERS.png")

def computeNbSearchSymptom(dfChild, dfSymptoms, symptom):
  nb = 0
  int_df = pd.merge(dfChild, dfSymptoms, how ='inner', on =['VAERS_ID', 'VAERS_ID'])
  ID = []
  listColumns = ["SYMPTOM"+str(i) for i in range(1,6)]
  for c in listColumns :
    int_dfS = int_df[int_df[c]==symptom]
    for i in range(0,len(int_dfS)):
      if int_dfS.iloc[i]["VAERS_ID"] not in ID :
        nb+=1
        ID.append(int_dfS.iloc[i]["VAERS_ID"])
  return nb

def searchSymptomEvolutionVax(age_limit, symptom):
  datasChild = []
  syVax = dict()
  year = YB
  for i in range(0,len(datas)) :
    dfChild = extractChild(datas[i][0],age_limit)
    int_dfChild = pd.merge(dfChild, datas[i][2], how ='inner', on =['VAERS_ID', 'VAERS_ID'])
    datasChild.append(int_dfChild)
    nbSyYear = computeNbSearchSymptom(int_dfChild, datas[i][1], symptom)
    syVax.update({year : [len(int_dfChild["VAERS_ID"]),nbSyYear]})
    year+=1
  return syVax

myoVax = searchSymptomEvolutionVax(18,"Myocardites")
print(myoVax)

plotEvolution(myoVax,"Evolution temporelle des myocardites dans la VAERS \nsusceptibles d'être dûes aux vaccins chez les moins de 18 ans", YB, YE, "EvolutionMyocarditesVAERSVAX.png")

plotVariation(myoVax,"Variation du nombre de myocardites (en %) déclarées dans la VAERS suscpetibles d'être dûes aux vaccins \n(normalisée sur le nombre de déclarants)\n chez les moins de 18 ans par rapport à l'année précédente", YB, YE, "VariationMyocarditesVAERSVAX.png")
