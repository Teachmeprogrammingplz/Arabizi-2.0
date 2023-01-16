# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:05:06 2022

@author: echchihab
"""

#importation des librairies utilisees


#import nltk
#nltk.download("stopwords")
#nltk.download('wordnet')

import pickle
from pyarabic import araby
from  pyarabic.araby import normalize_ligature
import qalsadi.lemmatizer
from collections import Counter
import pandas as pd
import numpy as np
from lxml import etree
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import requests
import string

def init_Hashmap2() :
    #nouns also
    tree = etree.parse("ArDict.xml")
    hashmap = {}
    for verb in tqdm(tree.xpath("/words/verbs/verb")):
        rot = verb.get("ro")
        if (len(rot) == 3) :
            df = ''
            for i in range(len(verb)) :
                df = df + verb[i].get("desc") + ' '
            if df != '' :
                for i in range(len(rot)) :
                    try :
                        hashmap[rot[i] , i] = hashmap[rot[i] , i] + " " + df
                    except :
                        hashmap[rot[i] , i] = df 
    for noun in tqdm(tree.xpath("/words/nouns/noun")):
         rot = noun[0].get("ro")
         if (len(rot) == 3) :
             df = ''
             for i in range(1, len(noun)) :
                 try :
                     df = df +' ' +noun[i].get("desc") 
                 except :
                     next
             if df != '' :
                for i in range(len(rot)) :
                     try :
                         hashmap[rot[i] , i] = hashmap[rot[i] , i] + " " + df
                     except :
                         hashmap[rot[i] , i] = df              
    return hashmap


def init_Hashmap() :
    #nouns also
    tree = etree.parse("ArDict.xml")
    hashmap = []
    for verb in tqdm(tree.xpath("/words/verbs/verb")):
        rot = verb.get("ro")
        if (len(rot) == 3) :
            df = ''
            for i in range(len(verb)) :
                df = df + ' ' + verb[i].get("desc") 
            if df != '' :
                for i in range(len(rot)) :
                    hashmap.append((rot[i] , i , df))
    
    for noun in tqdm(tree.xpath("/words/nouns/noun")):
         rot = noun[0].get("ro")
         if (len(rot) == 3) :
             df = ''
             for i in range(1, len(noun)) :
                 try :
                     df = df +' ' + noun[i].get("desc") 
                 except :
                     next
             if df != '' :
                 for i in range(len(rot)) :
                     hashmap.append((rot[i] , i , df))              
    return hashmap


def StopWords() :
    tree = etree.parse("sw.xml")
    res = []
    for form in tree.xpath("/stopWords/stopWord/vowForm"):
        res.append(form.text)
    for form in tree.xpath("/stopWords/stopWord/simpleStopWord"):
        res.append(form.text)
    tree = etree.parse("particles.xml")
    for form in tree.xpath("/arabic_particles/particle/Form/voweledform"):
        res.append(form.text)
    for form in tree.xpath("/arabic_particles/particle/Form/unvoweledform"):
        res.append(form.text)
    lst = ['له', 'هاهنا', 'إياه', 'عنده','إياها', 'بعده','ذا','مما','ذلك','ممن','عندها','أيها', 'لئلا','حينئذ','و' 'الذي','أيضا', 'أنا','بخ','عندهم','بعدما','بأن','التي','وذات','هذه','معها','ذاك','بأنه', 'وإياه','هكذا','بأنها', 'معه', 'وهاهنا','لنا', 'لدى','عندك','بأيها','ماذا', 'هؤلاء','وعند','معي','هاك','بعدها','إنا','معهم','لكيلا']
    for el in lst :
        res.append(el)
    filehandler = open('Stop Words.pickle', 'wb')
    pickle.dump(res, filehandler)
    filehandler.close()

def getStopWords() :
    file_to_read = open('Stop Words.pickle', 'rb')
    loaded_dictionary = pickle.load(file_to_read)
    file_to_read.close()  
    return loaded_dictionary


def lemmatize(text) :
    url = 'https://farasa.qcri.org/webapi/lemmatization/'
    api_key = "rWvaBZbFwnfvOVllAI"
    payload = {'text': text, 'api_key': api_key}
    data = requests.post(url, data=payload)
    result = json.loads(data.text)
    print(result)
    return result['text']

def remove_punctuation(text):
    #custom function to remove the punctuation
    return text.translate(str.maketrans('', '', string.punctuation))


#Segmanter et enlever les SW plus les lemmatiser
def textProcess2(text, stop_words) :
  
    tokens = lemmatize(text)
    res = ""
    for dic in tokens :
        if dic not in stop_words:
            res = res + " " + dic
    res = remove_punctuation(res)
    return res


def textProcess(text, stop_words) :
    lemmer = qalsadi.lemmatizer.Lemmatizer()
    #Normalize Lam Alef ligatures into two letters (LAM and ALEF)
    text = normalize_ligature(text)
    tokens = araby.tokenize_with_location(text)
    res = ""
    for dic in tokens :
        txt = lemmer.lemmatize(dic['token'])
        if txt not in stop_words :
            res = res + " " + txt
    return res


def Occur(res) :
    res = res.split()
    counter = Counter(res)
    counter = counter.most_common(20)
    return dict(counter)
    
    
def update_Hashmap2(label) :
    file1 = open(label, 'r', encoding="utf-8")
    lines = file1.readlines()
    Hashmap = {}
    for line in lines :
        line = line.strip()
        item = line.split(":", 1)
        value = item[1].replace('#', '')
        value = value.replace('unk', '')
        key = item[0].split()
        key = (key[0], int(key[1]))
        Hashmap[key] = value
    return Hashmap

def update_Hashmap(dic) :
    
    sw = getStopWords()
    Hashmap = []
    for line in tqdm(dic) :
        Hashmap.append((line[0], line[1], textProcess(line[2], sw)))
        
    return Hashmap


def generate_DF2(title) :
    dct = update_Hashmap("Letters.txt")
    lettres = [key[0] for key in dct.keys()]
    positions = [key[1] for key in dct.keys()]
    values = [key for key in dct.values()]
    BOW = []
    for key in tqdm(dct.keys()) :
        lst = Occur(dct[key])
        BOW.append(' '.join([str(item) for item in lst]))
    data = {'Lettre': lettres,
            'Position': positions,
            'Values' : values,
            'BOW' : BOW}
    
    '''
    nouns = []
    values = dct.values()
    for value in values :
        v = value.keys()
        nouns.extend(v)
    nouns = [*set(nouns)]
    
    filehandler = open('Vocabulary.pickle', 'wb')
    pickle.dump(nouns, filehandler)
    filehandler.close()
    '''
    
    filehandler = open('BOW.pickle', 'wb')
    pickle.dump(dct, filehandler)
    filehandler.close()
    
    df = pd.DataFrame(data)
    df.to_csv(title)

def generate_DF(title) :
    dct = update_Hashmap(init_Hashmap())
    lettres = [key[0] for key in dct]
    positions = [key[1] for key in dct]
    values = [key[2] for key in dct]
    BOW = []
    for key in tqdm(dct) :
        lst = Occur(key[2])
        BOW.append(' '.join([str(item) for item in lst]))
    data = {'Lettre': lettres,
            'Position': positions,
            'Values' : values,
            'BOW' : BOW}
    
    '''
    nouns = []
    values = dct.values()
    for value in values :
        v = value.keys()
        nouns.extend(v)
    nouns = [*set(nouns)]
    
    filehandler = open('Vocabulary.pickle', 'wb')
    pickle.dump(nouns, filehandler)
    filehandler.close()
    '''
    
    filehandler = open('BOW.pickle', 'wb')
    pickle.dump(dct, filehandler)
    filehandler.close()
    
    df = pd.DataFrame(data)
    df.to_csv(title)


def getHashmap() :
    file_to_read = open('BOW.pickle', "rb")
    loaded_dictionary = pickle.load(file_to_read)
    file_to_read.close()
    return loaded_dictionary

def DictHashmap() :
    tree = etree.parse("ArDict.xml")
    hashmap = {}
    stop_words = getStopWords()
    for noun in  tqdm(tree.xpath("/words/nouns/noun")):
        rot = noun[0].get("ro")
        if (len(rot) == 3) :
            deff = ''
            for i in range(1, len(noun)):
                try :
                    deff = deff + ' ' + noun[i].get("desc")
                except :
                    next
            if deff != '' :
                deff = textProcess(deff, stop_words)
                hashmap[noun.get("vow"), rot] = deff
            #hashmap[noun.get("unv"), rot] = deff
    filehandler = open('Dict Nouns BOW.pickle', 'wb')
    pickle.dump(hashmap, filehandler)
    filehandler.close()

def DictHashmapV() :
    tree = etree.parse("ArDict.xml")
    hashmap = {}
    stop_words = getStopWords()
    for verb in  tqdm(tree.xpath("/words/verbs/verb")):
        rot = verb.get("ro")
        if (len(rot) == 3) :
            deff = ''
            for i in range(1, len(verb)):
                try :
                    deff = deff + ' ' + verb[i].get("desc")
                except :
                    next
            if deff != '' :
                deff = textProcess(deff, stop_words)
                hashmap[verb.get("vow"), rot] = deff
            #hashmap[verb.get("unv"), rot] = deff
    filehandler = open('Dict Verbs BOW.pickle', 'wb')
    pickle.dump(hashmap, filehandler)
    filehandler.close()
    
def getDictHashmap() :
    file_to_read = open('Dict Nouns BOW.pickle', "rb")
    file_to_read1 = open('Dict Verbs BOW.pickle', "rb")
    loaded_dictionary = pickle.load(file_to_read)
    loaded_dictionary1 = pickle.load(file_to_read1)
    file_to_read.close()
    file_to_read1.close()
    
    loaded_dictionary = {**loaded_dictionary,**loaded_dictionary1}
    return loaded_dictionary




def getLettrePos(value) :
    
    df = pd.read_csv("BOW.csv")
    df = pd.DataFrame(df)
    df = df.dropna()
    df = df.query("Position == @value")
    
    return df


def getVocabulary() :
 
    file_to_read = open('Vocabulary.pickle', 'rb')
    loaded_dictionary = pickle.load(file_to_read)
    file_to_read.close()  
    return loaded_dictionary




def Predict_Roots_CountV2() :

    Hashmap = getWords() 
    df = pd.read_csv("BOW.csv")
    df = pd.DataFrame(df)
    df = df.dropna()
    
    vectorizer1 = CountVectorizer(max_features = 3000) 
    
    #max_features = 3000   si on a  besoin
    
    dtm = vectorizer1.fit_transform(df["Values"])
    print(dtm.shape)
    
    res = {}
    precision1 = 0
    precision2 = 0
    precision3 = 0
    
    df_Pos0 = getLettrePos(0)
    dtm_Pos0 = vectorizer1.transform(df_Pos0["Values"])
    df_Pos1 = getLettrePos(1)
    dtm_Pos1 = vectorizer1.transform(df_Pos1["Values"])
    df_Pos2 = getLettrePos(2)
    dtm_Pos2 = vectorizer1.transform(df_Pos2["Values"])
    
    for key in Hashmap.keys() :
        deff = Hashmap[key]
        deff = vectorizer1.transform([deff])
        
        cosine_sim_dtm0 = cosine_similarity(dtm_Pos0, deff)
        cosine_sim_dtm1 = cosine_similarity(dtm_Pos1, deff)
        cosine_sim_dtm2 = cosine_similarity(dtm_Pos2, deff)
        
        max_index0 = np.argmax(cosine_sim_dtm0, axis=0)
        max_index1 = np.argmax(cosine_sim_dtm1, axis=0)
        max_index2 = np.argmax(cosine_sim_dtm2, axis=0)
        
        L0 = df_Pos0["Lettre"].values[max_index0][0]
        L1 = df_Pos1["Lettre"].values[max_index1][0]
        L2 = df_Pos2["Lettre"].values[max_index2][0]
    
        root = key[1]
        word = L0+L1+L2
                          
        res[key] = word
        
        print('Name : '+ key[0])
        print('Original root : '+ key[1])
        print('Predicted root : '+ word)
        
        pre = 0
        if L0 in root : 
            pre+=1
        if L1 in root : 
            pre+=1
        if L2 in root : 
            pre+=1
        if pre == 3 :
            precision3 += 1
        if pre == 2 :
            precision2 += 1
        if pre == 1 :
            precision1 += 1
    
    precision3 = precision3 * 100 / len(Hashmap.items())
    precision2 = precision2 * 100 / len(Hashmap.items())
    precision1 = precision1 * 100 / len(Hashmap.items())
    
    words = [key[0] for key in res.keys()]
    roots = [key[1] for key in res.keys()]
    predicted = [value for value in res.values()]
    BOW = [Occur(value) for value in Hashmap.values()]
    data = {'Word': words,
            'Root' : roots,
            'Predicted root': predicted,
            'BOW' : BOW}
    df = pd.DataFrame(data)
    df.to_csv("Predicted BOW.csv")
    
    
    
    return precision1,precision2,precision3
        
        
        
def Predict_Root(text) :
    
    df = pd.read_csv("BOW.csv")
    df = pd.DataFrame(df)
    df = df.dropna()
    stop_words = getStopWords()
    text = textProcess(text, stop_words)
    vectorizer1 = CountVectorizer() 
    
    #max_features = 3000   si on a  besoin
    
    dtm = vectorizer1.fit_transform(df["Values"])
    
    deff = vectorizer1.transform([text])
    
    df_Pos0 = getLettrePos(0)
    dtm_Pos0 = vectorizer1.transform(df_Pos0["Values"])
    df_Pos1 = getLettrePos(1)
    dtm_Pos1 = vectorizer1.transform(df_Pos1["Values"])
    df_Pos2 = getLettrePos(2)
    dtm_Pos2 = vectorizer1.transform(df_Pos2["Values"])
    
    
    cosine_sim_dtm0 = cosine_similarity(dtm_Pos0, deff)
    cosine_sim_dtm1 = cosine_similarity(dtm_Pos1, deff)
    cosine_sim_dtm2 = cosine_similarity(dtm_Pos2, deff)
    
    max_index0 = np.argmax(cosine_sim_dtm0, axis=0)
    max_index1 = np.argmax(cosine_sim_dtm1, axis=0)
    max_index2 = np.argmax(cosine_sim_dtm2, axis=0)
    
    L0 = df_Pos0["Lettre"].values[max_index0][0]
    L1 = df_Pos1["Lettre"].values[max_index1][0]
    L2 = df_Pos2["Lettre"].values[max_index2][0]
        
  
    word = L0+L1+L2
                      
    
    return word



def Predict_Roots_CountV() :

    Hashmap = getDictHashmap() 
    df = pd.read_csv("BOW.csv")
    df = pd.DataFrame(df)
    df = df.dropna()
    
    vectorizer1 = CountVectorizer() 
    
    #max_features = 3000   si on a  besoin
    
    dtm = vectorizer1.fit_transform(df["Values"])
    print(dtm.shape)
    
    res = {}
    precision1 = 0
    precision2 = 0
    precision3 = 0
    df_Pos0 = getLettrePos(0)
    dtm_Pos0 = vectorizer1.transform(df_Pos0["Values"])
    df_Pos1 = getLettrePos(1)
    dtm_Pos1 = vectorizer1.transform(df_Pos1["Values"])
    df_Pos2 = getLettrePos(2)
    dtm_Pos2 = vectorizer1.transform(df_Pos2["Values"])
    
    for key in tqdm(Hashmap.keys()) :
        deff = Hashmap[key]
        deff = vectorizer1.transform([deff])
        
        cosine_sim_dtm0 = cosine_similarity(dtm_Pos0, deff)
        cosine_sim_dtm1 = cosine_similarity(dtm_Pos1, deff)
        cosine_sim_dtm2 = cosine_similarity(dtm_Pos2, deff)
        
        max_index0 = np.argmax(cosine_sim_dtm0, axis=0)
        max_index1 = np.argmax(cosine_sim_dtm1, axis=0)
        max_index2 = np.argmax(cosine_sim_dtm2, axis=0)
        
        L0 = df_Pos0["Lettre"].values[max_index0][0]
        L1 = df_Pos1["Lettre"].values[max_index1][0]
        L2 = df_Pos2["Lettre"].values[max_index2][0]
    
        root = key[1]
        word = L0+L1+L2
                          
        res[key] = word
        '''
        print('Word : '+ key[0])
        print('Original root : '+ key[1])
        print('Predicted root : '+ word)
        '''
        pre = 0
        if L0 == root[0] : 
            pre+=1
        if L1 == root[1] : 
            pre+=1
        if L2 == root[2] : 
            pre+=1
        if pre == 3 :
            precision3 += 1
        if pre == 2 :
            precision2 += 1
        if pre == 1 :
            precision1 += 1
    
    precision3 = precision3 * 100 / len(Hashmap.items())
    precision2 = precision2 * 100 / len(Hashmap.items())
    precision1 = precision1 * 100 / len(Hashmap.items())
    
    words = [key[0] for key in res.keys()]
    roots = [key[1] for key in res.keys()]
    predicted = [value for value in res.values()]
    BOW = [Occur(value) for value in Hashmap.values()]
    data = {'Word': words,
            'Root' : roots,
            'Predicted root': predicted,
            'BOW' : BOW}
    df = pd.DataFrame(data)
    df.to_csv("Predicted BOW.csv")
    
    
    
    return precision1,precision2,precision3
    

def getWords() :
    file1 = open('Words.txt', 'r', encoding="utf-8")
    lines = file1.readlines()
    Hashmap = {}
    for line in lines :
        line = line.strip()
        item = line.split(":", 1)
        value = item[1].replace('#', '').strip()
        value = value.replace('unk', '')
        key = item[0].split()
        key = (key[0], key[1])
        Hashmap[key] = value
    
    return Hashmap




def verification() :
    
    tree = etree.parse("Cont.xml")
    hashmap = {}
    for word in tqdm(tree.xpath("/Lexicon/LE")):
        rot = word.get("ro").replace(" ", "")
        if (len(rot) == 3 and word.get("ty") != 'كلمة وظيفيَّة') :
            df = ''
            for i in range(len(word)) :
                try :
                    df = df + word[i].get("des") + ' '
                except: 
                    df = df + word[i].get("dom") + ' '
            if df != '' :
                predicted = Predict_Root(df)
                hashmap[rot] = predicted
                print("\n")
                print("The Word is : "+ word.get("le"))
                print("original Root : "+ rot)
                print("predicted Root : "+ predicted)
                print("\n")




def verification2() :
    
    tree = etree.parse("Cont.xml")
    hashmap = {}
    stop_words = getStopWords()
    for word in tqdm(tree.xpath("/Lexicon/LE")):
        rot = word.get("ro").replace(" ", "")
        if (len(rot) == 3 and word.get("ty") != 'كلمة وظيفيَّة') :
            df = ''
            for i in range(len(word)) :
                try :
                    df = df + word[i].get("des") + ' '
                except: 
                    next
            if df != '' :
                df = textProcess(df, stop_words)
                hashmap[word.get("le"), rot] = df
                
    filehandler = open('Dict words BOW.pickle', 'wb')
    pickle.dump(hashmap, filehandler)
    filehandler.close()
    

'''
#Pour les noms
DictHashmap()
DictHashmapV()
Hashmap2 = getDictHashmap()

Hashmap = {}
for key in Hashmap2 :
    if Hashmap2[key].replace(" ", "") != "" :
        Hashmap[key] = Hashmap2[key]
    
print(len(Hashmap.keys()))
file1 = open("Hashmap.txt", "w", encoding="utf-8") 
L = []
for key in Hashmap.keys() :
    file1.write(str(key[0])+" "+str(key[1])+" :"+" "+Hashmap[key] + "\n")


#file1.writelines(L)

file1.close()
'''


'''
#Pour les letters

Hashmap2 = init_Hashmap()

Hashmap = {}
for key in Hashmap2 :
    if Hashmap2[key].replace(" ", "") != "" :
        Hashmap[key] = Hashmap2[key]
    
print(len(Hashmap.keys()))
file1 = open("Hashmap.txt", "w", encoding="utf-8") 
L = []
for key in Hashmap.keys() :
    file1.write(str(key[0])+" "+str(key[1])+" :"+" "+Hashmap[key] + "\n")


#file1.writelines(L)

file1.close()

'''


'''
precision = Predict_Roots_CountV()
print('Pourcetage de 3/3 precision est :' +  str(precision[2]) + "%")
print('Pourcetage de 2/3 precision est :' +  str(precision[1])+ "%")
print('Pourcetage de 1/3 precision est :' +  str(precision[0])+ "%")
print('Pourcetage de 0/3 precision est :' +  str(100 - (precision[0]+ precision[1]+precision[2]))+ "%")
'''


'''
vocab1 = getVocabulary()
vocab2 = vectorizer1.get_feature_names()
vocab_difference = set(vocab1).symmetric_difference(set(vocab2))
print(vocab_difference)


#df_bow_sklearn = pd.DataFrame(dtm.toarray(),columns=vectorizer1.get_feature_names())
#print(df_bow_sklearn.head())
'''





      
