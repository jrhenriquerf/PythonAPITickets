# -*- coding: utf-8 -*-
import nltk
import sys
import csv
reload(sys)
sys.setdefaultencoding("utf-8")

def retornaPrioridade(mensagem):
    #tipo='CORPO'
    baseTreino = []
    baseTeste = []

    #if tipo == 'ASSUNTO':
    #    fileTreino = 'dadosTreinoAssuntos.csv'
    #    fileTeste = 'dadosTesteAssuntos.csv'
    #else:
    fileTreino = 'dadosTreino.csv'
    fileTeste = 'dadosTeste.csv'

    #Base de treinamento para treinar a IA, com menos dados que a base de testes para que ela não trabalhe decoradamente.
    def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
        csv_reader = csv.reader(utf8_data, dialect, **kwargs)
        for row in csv_reader:
            yield [unicode(cell, 'utf-8') for cell in row]

    readerTreino = unicode_csv_reader(open(fileTreino))
    for field1, field2 in readerTreino:
        baseTreino.append((field1, field2))

    readerTeste = unicode_csv_reader(open(fileTeste))
    for field1, field2 in readerTeste:
        baseTeste.append((field1, field2))

    stopwordsNltk = nltk.corpus.stopwords.words('portuguese')

    # Técnica para retirar as partes inúteis das palavras, deixando apenas seus radicais.
    # Ex.: para Amor, Amado e Amável o radical é Am. Para o algoritmo as 3 palavras seriam tratadas como uma só,
    # fazendo com que o algoritmo seja mais dinâmico e menos carregado.
    def aplicaStemmer(texto):
     stemmer = nltk.stem.RSLPStemmer()
     frasesStemming = []
     for (palavras, prioridade) in texto:
        #aplica o stemmer as palavres que não estão dentre as stopwords
        comStemming = [str(stemmer.stem(p.decode('utf-8'))) for p in palavras.split() if p not in stopwordsNltk]
        frasesStemming.append((comStemming, prioridade))
     return frasesStemming

    #Aplica o stemmer nas frases de treinamento
    frasesStemmingTreino = aplicaStemmer(baseTreino)
    #Aplica o stemmer nas frases de teste
    frasesStemmingTeste = aplicaStemmer(baseTeste)

    # junta todas as palavras em uma lista de palavras
    def buscaPalavras(frases):
        todasPalavras = []
        for (palavras, prioridade) in frases:
            todasPalavras.extend(palavras)
        return todasPalavras

    #busca todas as palavras de treinamento
    palavrasTreino = buscaPalavras(frasesStemmingTreino)

    #Extrai palavras não dublicadas (a ver)
    def extratorPalavras(documento):
        #utilização do set para remover as palavras dublicadas na lista
        doc = set(documento)
        caracteristicas = {}
        for palavras in palavrasTreino:
            caracteristicas['%s' % palavras] = (palavras in doc)
        return caracteristicas

    baseCompletaTreino = nltk.classify.apply_features(extratorPalavras, frasesStemmingTreino)
    baseCompletaTeste = nltk.classify.apply_features(extratorPalavras, frasesStemmingTeste)

    classificador = nltk.NaiveBayesClassifier.train(baseCompletaTreino)

    erros = []
    for (frase, classe) in baseCompletaTeste:
        resultado = classificador.classify(frase)
        if resultado != classe:
            erros.append((classe, resultado, frase))

    testeStemming = []
    stemmer = nltk.stem.RSLPStemmer()
    for (palavrasTreino) in mensagem.split():
        comStemmer = [p for p in palavrasTreino.split()]
        testeStemming.append(str(stemmer.stem(comStemmer[0].decode('utf-8'))))

    novo = extratorPalavras(testeStemming)

    return classificador.classify(novo)
