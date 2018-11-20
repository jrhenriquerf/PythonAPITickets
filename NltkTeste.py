# -*- coding: utf-8 -*-
import nltk
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

basetreinamento = [
    ('eu gosto disso', 'alegria'),
    ('este trabalho e agradável','alegria'),
    ('gosto de ficar no seu aconchego','alegria'),
    ('fiz a adesão ao curso hoje','alegria'),
    ('eu sou admirada por muitos','alegria'),
    ('adoro como você e','alegria'),
    ('adoro seu cabelo macio','alegria'),
    ('adoro a cor dos seus olhos','alegria'),
    ('somo tão amáveis um com o outro','alegria'),
    ('sinto uma grande afeição por ele','alegria'),
    ('quero agradar meus filhos','alegria'),
    ('me sinto completamente amado','alegria'),
    ('eu amo você','alegria'),
    ('por favor não me abandone','tristeza'),
    ('não quero ficar sozinha','tristeza'),
    ('não me deixe sozinha','tristeza'),
    ('estou abatida','tristeza'),
    ('ele esta todo abatido','tristeza'),
    ('tão triste suas palavras','tristeza'),
    ('seu amor não e mais meu','tristeza'),
    ('estou aborrecida','tristeza'),
    ('isso vai me aborrecer','tristeza'),
    ('estou com muita aflição','tristeza'),
    ('me aflige o modo como fala','tristeza'),
    ('estou em agonia com meu intimo','tristeza')
]

baseteste = [
    ('não precisei pagar o ingresso','alegria'),
    ('se eu ajeitar tudo fica bem','alegria'),
    ('minha fortuna ultrapassa a sua','alegria'),
    ('sou muito afortunado','alegria'),
    ('e benefico para todos esta nova medida','alegria'),
    ('ficou lindo','alegria'),
    ('achei esse sapato muito simpático','alegria'),
    ('estou ansiosa pela sua chegada','alegria'),
    ('congratulações pelo seu aniversário','alegria'),
    ('delicadamente ele a colocou para dormir','alegria'),
    ('a musica e linda','alegria'),
    ('sem musica eu não vivo','alegria'),
    ('conclui uma tarefa muito difícil','alegria'),
    ('isso tudo e um erro','tristeza'),
    ('eu sou errada eu sou errante','tristeza'),
    ('tenho muito dó do cachorro','tristeza'),
    ('e dolorida a perda de um filho','tristeza'),
    ('essa tragedia vai nos abalar para sempre','tristeza'),
    ('perdi meus filhos','tristeza'),
    ('perdi meu curso','tristeza'),
    ('sou só uma chorona','tristeza'),
    ('você e um chorão','tristeza'),
    ('se arrependimento matasse','tristeza'),
    ('me sinto deslocado em sala de aula','tristeza'),
    ('foi uma passagem fúnebre','tristeza'),
    ('nossa condolências e tristeza a sua perda','tristeza')
]

stopwordsnltk = nltk.corpus.stopwords.words('portuguese')

# Técnica de retirar as partes inúteis das palavras, deixando apenas seus radicais.
# Ex.: para Amor, Amado e Amável o radical é Am. Para o algoritmo as 3 palavras seriam tratadas como uma só,
# fazendo com que o algoritmo seja mais dinâmico e menos carregado.
def aplicastemmer(texto):
 stemmer = nltk.stem.RSLPStemmer()
 frasessstemming = []
 for (palavras, emocao) in texto:
    comstemming = [str(stemmer.stem(p.decode('utf-8'))) for p in palavras.split() if p not in stopwordsnltk]
    frasessstemming.append((comstemming, emocao))
 return frasessstemming

frasescomstemmingtreinamento = aplicastemmer(basetreinamento)
frasescomstemmingteste = aplicastemmer(baseteste)

def buscapalavras(frases):
 todaspalavras = []
 for (palavras, emocao) in frases:
    todaspalavras.extend(palavras)
 return todaspalavras

palavrastreinamento = buscapalavras(frasescomstemmingtreinamento)
palavrasteste = buscapalavras(frasescomstemmingteste)

def buscafrequencia(palavras):
 palavras = nltk.FreqDist(palavras)
 return palavras

frequenciatreinamento = buscafrequencia(palavrastreinamento)
frequenciateste = buscafrequencia(palavrasteste)

def extratorpalavras(documento):
 doc = set(documento)
 caracteristicas = {}
 for palavras in palavrastreinamento:
    caracteristicas['%s' % palavras] = (palavras in doc)
 return caracteristicas

caracteristicasfrase = extratorpalavras(['am', 'nov', 'dia'])
basecompletatreinamento = nltk.classify.apply_features(extratorpalavras, frasescomstemmingtreinamento)
basecompletateste = nltk.classify.apply_features(extratorpalavras, frasescomstemmingteste)

classificador = nltk.NaiveBayesClassifier.train(basecompletatreinamento)
print(classificador.labels())

print(nltk.classify.accuracy(classificador, basecompletateste))

erros = []
for (frase, classe) in basecompletateste:

    resultado = classificador.classify(frase)
    if resultado != classe:
        erros.append((classe, resultado, frase))
from nltk.metrics import ConfusionMatrix

esperado = []
previsto = []
for (frase, classe) in basecompletateste:
    resultado = classificador.classify(frase)
    previsto.append(resultado)
    esperado.append(classe)
matriz = ConfusionMatrix(esperado, previsto)
print(matriz)

teste = 'eu amo salada'
testestemming = []
stemmer = nltk.stem.RSLPStemmer()
for (palavrastreinamento) in teste.split():
 comstem = [p for p in palavrastreinamento.split()]
 testestemming.append(str(stemmer.stem(comstem[0])))

novo = extratorpalavras(testestemming)
distribuicao = classificador.prob_classify(novo)
print("RESULTADO:")
print(classificador.classify(novo))


