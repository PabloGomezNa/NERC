#! /usr/bin/python3

import sys
import re
from os import listdir

from xml.dom.minidom import parse
from nltk.tokenize import word_tokenize

#On the feature extractor, to lematize and stemmis
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk import pos_tag

#nltk.download('wordnet')
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')


   
## --------- tokenize sentence ----------- 
## -- Tokenize sentence, returning tokens and span offsets

def tokenize(txt):
    offset = 0
    tks = []
    ## word_tokenize splits words, taking into account punctuations, numbers, etc.
    for t in word_tokenize(txt):
        ## keep track of the position where each token should appear, and
        ## store that information with the token
        offset = txt.find(t, offset)
        tks.append((t, offset, offset+len(t)-1))
        offset += len(t)
    ## tks is a list of triples (word,start,end)
    return tks


## --------- get tag ----------- 
##  Find out whether given token is marked as part of an entity in the XML
def get_tag(token, spans) :
   (form,start,end) = token
   for (spanS,spanE,spanT) in spans :
      if start==spanS and end<=spanE : return "B-"+spanT
      elif start>=spanS and end<=spanE : return "I-"+spanT
   return "O"
 
 
 
 


   



## --------- Feature extractor ----------- 
## -- Extract features for each token in given sentence

def initial_extract_features(tokens) :

   # for each token, generate list of features and add it to the result
   result = []
   for k in range(0,len(tokens)):
      tokenFeatures = [];
      t = tokens[k][0]

      tokenFeatures.append("form="+t)
      tokenFeatures.append("suf3="+t[-3:])

      if k>0 :
         tPrev = tokens[k-1][0]
         tokenFeatures.append("formPrev="+tPrev)
         tokenFeatures.append("suf3Prev="+tPrev[-3:])
      else :
         tokenFeatures.append("BoS")

      if k<len(tokens)-1 :
         tNext = tokens[k+1][0]
         tokenFeatures.append("formNext="+tNext)
         tokenFeatures.append("suf3Next="+tNext[-3:])
      else:
         tokenFeatures.append("EoS")
    
      result.append(tokenFeatures)
    
   return result




def extract_features_without_Resources(tokens) :

   # for each token, generate list of features and add it to the result
   result = []

   #initialize lemmatizer and stemmer
   lemmatizer = WordNetLemmatizer()
   stemmer = PorterStemmer()
   

   for k in range(0,len(tokens)):
      tokenFeatures = [];
      t = tokens[k][0]
      
  
      #Actual word
      tokenFeatures.append("form="+t)
      
      if k == 0:
         tokenFeatures.append("BoS")
      elif k == len(tokens)-1:
         tokenFeatures.append("EoS")


      #OUR ADDITION
      #LOWERCASED WORD
      lowercased=t.lower()
      tokenFeatures.append("lowercased="+lowercased)

  

      #WORD LENGHT
      tokenFeatures.append("word_length=" + str(len(t)))
      

      
      #PART OF SPEECH
      pos = pos_tag([t])[0][1]
      tokenFeatures.append("pos=" + pos)

      #LEMATISSER
      lemma = lemmatizer.lemmatize(t)
      tokenFeatures.append("lemma=" + lemma)
      
      #STEMMING
      stem = stemmer.stem(t)
      tokenFeatures.append("stem=" + stem)


      tokenFeatures.append("suf3="+t[-3:]) #sufix

      tokenFeatures.append("pre3="+t[+3:]) #prefix

      # add the string "OC" if there is one capital letter in the word
      # or add the string "MTOC" if there are more than one capital letters in the word
      if sum(1 for c in t if c.isupper()) == 1:
         tokenFeatures.append("OC")
      elif sum(1 for c in t if c.isupper()) > 1:
         tokenFeatures.append("MTOC")

      #We define a set of special characters and we will add a tag if the word has one of them, tag = SC
      punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
      if any(c in punctuation for c in t):
         tokenFeatures.append("SC")
         
      #INTENTAR CON MULTIPLE SPECIAL CHARACTERS, PARA MEJORAR DRUG_N
     #We will add a tag for the presence of Digits
      if any(c.isdigit() for c in t):
         tokenFeatures.append("DIG")


      # tokenFeatures.append("suf3="+t[-3:])
      # tokenFeatures.append("pre3="+t[:3])
      # tokenFeatures.append("suf4="+t[-4:])
      # tokenFeatures.append("pre4="+t[:4])
      # tokenFeatures.append("suf5="+t[-5:])
      # tokenFeatures.append("pre5="+t[:5])
      # tokenFeatures.append("suf6="+t[-6:])
      # tokenFeatures.append("pre6="+t[:6])




      if k>0 :
         tPrev = tokens[k-1][0]
         tokenFeatures.append("formPrev="+tPrev)
         tokenFeatures.append("suf3Prev="+tPrev[-3:])
      else :
         tokenFeatures.append("BoS")


      if k<len(tokens)-1 :
         tNext = tokens[k+1][0]
         tokenFeatures.append("formNext="+tNext)
         tokenFeatures.append("suf3Next="+tNext[-3:])
      else:
         tokenFeatures.append("EoS")
    
      result.append(tokenFeatures)
    
   return result




def DrugBank(path_file):
   DrugBank_Drug = []
   DrugBank_Brand = []
   DrugBank_Group = []
   
   # Abrir el archivo y procesar cada línea
   with open(path_file, 'r',encoding='utf8') as file:
      for line in file:
         line = line.strip()  # Eliminar espacios y saltos de línea adicionales
         if '|' in line:  # Asegurar que la línea contiene el delimitador
               name, category = line.split('|')  # Separar el nombre y la categoría
               # Clasificar el nombre en la lista correspondiente
               if category.strip() == 'drug':
                  DrugBank_Drug.append(name.strip())
               elif category.strip() == 'brand':
                  DrugBank_Brand.append(name.strip())
               elif category.strip() == 'group':
                  DrugBank_Group.append(name.strip())

   # Mostrar las listas (opcional, para verificar los resultados)
   return DrugBank_Drug, DrugBank_Brand, DrugBank_Group
   
   
def HSDB(path_file):

   with open(path_file, 'r',encoding='utf8') as file:
      text = file.read()
      HSDB_List= text.split('\n')
      
   return HSDB_List

def load_resources():
    drugbank_drug, drugbank_brand, drugbank_group = DrugBank('C:\\Users\\pgome\\Desktop\\Master\\2nd Semester\\MUD-Mining Unstructured Data\\Lab\\Project2\\DDI\\resources\\DrugBank.txt')
    hsdb_list = HSDB('C:\\Users\\pgome\\Desktop\\Master\\2nd Semester\\MUD-Mining Unstructured Data\\Lab\\Project2\\DDI\\resources\\HSDB.txt')
    return drugbank_drug, drugbank_brand, drugbank_group, hsdb_list


def extract_features_with_Resources(tokens,DrugBank_Drug,DrugBank_Brand,DrugBank_Group,HSDB_List) :

   # for each token, generate list of features and add it to the result
   result = []

   #initialize lemmatizer and stemmer
   lemmatizer = WordNetLemmatizer()
   stemmer = PorterStemmer()
   

   for k in range(0,len(tokens)):
      tokenFeatures = [];
      t = tokens[k][0]
      
  
      #Actual word
      tokenFeatures.append("form="+t)
      
      if k == 0:
         tokenFeatures.append("BoS")
      elif k == len(tokens)-1:
         tokenFeatures.append("EoS")


      #OUR ADDITION
      #LOWERCASED WORD
      lowercased=t.lower()
      tokenFeatures.append("lowercased="+lowercased)

      #IF ITS INSIDE THE LIST OF AVAILABLE RESOURCES
      if t in DrugBank_Drug:
         tokenFeatures.append("DrugBank_Drug")
      if t in DrugBank_Brand:
         tokenFeatures.append("DrugBank_Brand")
      if t in DrugBank_Group:
         tokenFeatures.append("DrugBank_Group")
      if t in HSDB_List:
         tokenFeatures.append("HSDB")      

      #WORD LENGHT
      tokenFeatures.append("word_length=" + str(len(t)))
      

      
      #PART OF SPEECH
      pos = pos_tag([t])[0][1]
      tokenFeatures.append("pos=" + pos)

      #LEMATISSER
      lemma = lemmatizer.lemmatize(t)
      tokenFeatures.append("lemma=" + lemma)
      
      #STEMMING
      stem = stemmer.stem(t)
      tokenFeatures.append("stem=" + stem)


      tokenFeatures.append("suf3="+t[-3:]) #sufix

      tokenFeatures.append("pre3="+t[+3:]) #prefix

      # add the string "OC" if there is one capital letter in the word
      # or add the string "MTOC" if there are more than one capital letters in the word
      if sum(1 for c in t if c.isupper()) == 1:
         tokenFeatures.append("OC")
      elif sum(1 for c in t if c.isupper()) > 1:
         tokenFeatures.append("MTOC")

      #We define a set of special characters and we will add a tag if the word has one of them, tag = SC
      punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
      if any(c in punctuation for c in t):
         tokenFeatures.append("SC")
         
      #INTENTAR CON MULTIPLE SPECIAL CHARACTERS, PARA MEJORAR DRUG_N
     #We will add a tag for the presence of Digits
      if any(c.isdigit() for c in t):
         tokenFeatures.append("DIG")


      # tokenFeatures.append("suf3="+t[-3:])
      # tokenFeatures.append("pre3="+t[:3])
      # tokenFeatures.append("suf4="+t[-4:])
      # tokenFeatures.append("pre4="+t[:4])
      # tokenFeatures.append("suf5="+t[-5:])
      # tokenFeatures.append("pre5="+t[:5])
      # tokenFeatures.append("suf6="+t[-6:])
      # tokenFeatures.append("pre6="+t[:6])




      if k>0 :
         tPrev = tokens[k-1][0]
         tokenFeatures.append("formPrev="+tPrev)
         tokenFeatures.append("suf3Prev="+tPrev[-3:])
      else :
         tokenFeatures.append("BoS")


      if k<len(tokens)-1 :
         tNext = tokens[k+1][0]
         tokenFeatures.append("formNext="+tNext)
         tokenFeatures.append("suf3Next="+tNext[-3:])
      else:
         tokenFeatures.append("EoS")
    
      result.append(tokenFeatures)
    
   return result


## --------- MAIN PROGRAM ----------- 
## --
## -- Usage:  baseline-NER.py target-dir
## --
## -- Extracts Drug NE from all XML files in target-dir, and writes
## -- them in the output format requested by the evalution programs.
## --


# directory with files to process
datadir = sys.argv[1]

#EXTRACT INFO ABOUT THE RESOUTCES
DrugBank_Drug, DrugBank_Brand, DrugBank_Group, HSDB_List = load_resources() #Load this here so we dont execute it each time


# process each file in directory
for f in listdir(datadir) :
   # parse XML file, obtaining a DOM tree
   tree = parse(datadir+"/"+f)
   # process each sentence in the file
   sentences = tree.getElementsByTagName("sentence")
   for s in sentences :
      sid = s.attributes["id"].value   # get sentence id
      spans = []
      stext = s.attributes["text"].value   # get sentence text
      entities = s.getElementsByTagName("entity")
      for e in entities :
         # for discontinuous entities, we only get the first span
         # (will not work, but there are few of them)
         (start,end) = e.attributes["charOffset"].value.split(";")[0].split("-")
         typ =  e.attributes["type"].value
         spans.append((int(start),int(end),typ))
         


      # convert the sentence to a list of tokens
      tokens = tokenize(stext)
      
      # Initial extract features function
      features = initial_extract_features(tokens)

      #Extrcact features modified bu without external resources
      #features = extract_features_without_Resources(tokens,DrugBank_Drug,DrugBank_Brand,DrugBank_Group,HSDB_List)

      # extract sentence features with rexternal resources
      #features = extract_features_with_Resources(tokens,DrugBank_Drug,DrugBank_Brand,DrugBank_Group,HSDB_List)

      # print features in format expected by crfsuite trainer
      for i in range (0,len(tokens)) :
         # see if the token is part of an entity
         tag = get_tag(tokens[i], spans) 
         print (sid, tokens[i][0], tokens[i][1], tokens[i][2], tag, "\t".join(features[i]), sep='\t')

      # blank line to separate sentences
      print()
