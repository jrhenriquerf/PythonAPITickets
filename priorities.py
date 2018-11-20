# -*- coding: utf-8 -*-
import nltk
import sys
import csv
reload(sys)
sys.setdefaultencoding("utf-8")

def retornaPrioridade(mensagem):
    baseTreino = []
    baseTeste = []
    #Base de treinamento para treinar a IA, com menos dados que a base de testes para que ela não trabalhe decoradamente.
    def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
        csv_reader = csv.reader(utf8_data, dialect, **kwargs)
        for row in csv_reader:
            yield [unicode(cell, 'utf-8') for cell in row]

    readerTreino = unicode_csv_reader(open('dadosTreino.csv'))
    for field1, field2 in readerTreino:
        baseTreino.append((field1, field2))

    readerTeste = unicode_csv_reader(open('dadosTeste.csv'))
    for field1, field2 in readerTeste:
        baseTeste.append((field1, field2))

    #for (palavras, prioridade) in baseTeste:
    #    print(palavras)

    stopwordsnltk = nltk.corpus.stopwords.words('portuguese')

    # Técnica para retirar as partes inúteis das palavras, deixando apenas seus radicais.
    # Ex.: para Amor, Amado e Amável o radical é Am. Para o algoritmo as 3 palavras seriam tratadas como uma só,
    # fazendo com que o algoritmo seja mais dinâmico e menos carregado.
    def aplicastemmer(texto):
     stemmer = nltk.stem.RSLPStemmer()
     frasessstemming = []
     for (palavras, prioridade) in texto:
        #aplica o stemmer as palavres que não estão dentre as stopwords
        comstemming = [str(stemmer.stem(p.decode('utf-8'))) for p in palavras.split() if p not in stopwordsnltk]
        frasessstemming.append((comstemming, prioridade))
     return frasessstemming

    #Aplica o stemmer nas frases de treinamento
    frasescomstemmingtreinamento = aplicastemmer(baseTreino)
    #Aplica o stemmer nas frases de teste
    frasescomstemmingteste = aplicastemmer(baseTeste)

    #junta todas as palavras em uma lista de palavras
    def buscapalavras(frases):
     todaspalavras = []
     for (palavras, prioridade) in frases:
        todaspalavras.extend(palavras)
     return todaspalavras

    #busca todas as palavras de treinamento
    palavrastreinamento = buscapalavras(frasescomstemmingtreinamento)
    #busca todas as palavras de teste
    palavrasteste = buscapalavras(frasescomstemmingteste)

    #Busca a frequencia de cada palavra na lista de palavras passada por parâmetro
    def buscafrequencia(palavras):
     palavras = nltk.FreqDist(palavras)
     return palavras

    #Busca a frequencia das palavras de treinamento
    frequenciatreinamento = buscafrequencia(palavrastreinamento)
    #Busca a frequencia das palavras de testes
    frequenciateste = buscafrequencia(palavrasteste)

    #Extrai palavras não dublicadas (a ver)
    def extratorpalavras(documento):
     #utilização do set para remover as palavras dublicadas na lista
     doc = set(documento)
     caracteristicas = {}
     for palavras in palavrastreinamento:
        caracteristicas['%s' % palavras] = (palavras in doc)
     return caracteristicas

    caracteristicasfrase = extratorpalavras(['am', 'nov', 'dia'])
    basecompletatreinamento = nltk.classify.apply_features(extratorpalavras, frasescomstemmingtreinamento)
    basecompletateste = nltk.classify.apply_features(extratorpalavras, frasescomstemmingteste)

    classificador = nltk.NaiveBayesClassifier.train(basecompletatreinamento)
    #print(classificador.labels())

    #print(nltk.classify.accuracy(classificador, basecompletateste))

    erros = []
    for (frase, classe) in basecompletateste:

        resultado = classificador.classify(frase)
        if resultado != classe:
            erros.append((classe, resultado, frase))
    from nltk.metrics import ConfusionMatrix

    #esperado = []
    #previsto = []
    #for (frase, classe) in basecompletateste:
    #    resultado = classificador.classify(frase)
    #    previsto.append(resultado)
    #    esperado.append(classe)
    #matriz = ConfusionMatrix(esperado, previsto)
    #print(matriz)

    teste = mensagem
    testestemming = []
    stemmer = nltk.stem.RSLPStemmer()
    for (palavrastreinamento) in teste.split():
     comstem = [p for p in palavrastreinamento.split()]
     testestemming.append(str(stemmer.stem(comstem[0].decode('utf-8'))))

    novo = extratorpalavras(testestemming)
    distribuicao = classificador.prob_classify(novo)
    #print("RESULTADO:")
    #print(classificador.classify(novo))
    return classificador.classify(novo)