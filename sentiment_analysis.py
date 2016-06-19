#############################################################################################
# Univesidade Federal de Pernambuco -- UFPE (http://www.ufpe.br)                            #
# Centro de Informatica -- CIn (http://www.cin.ufpe.br)                                     #
# Bacharelado em Sistemas de Informacao                                                     #
# IF968 -- Programacao 1                                                                    #
#                                                                                           #
# Autores:    Renata Kelly da Silva Amorim                                                  #
#             Vinicius Giles Costa Paulino                                                  #
#                                                                                           #
# Email:      rksa@cin.ufpe.br                                                              #
#             vgcp@cin.ufpe.br                                                              #
#                                                                                           #
# Data:       2016-06-10                                                                    #
#                                                                                           #
# Descricao:  Este e' um modelo de arquivo para ser utilizado para a implementacao          #
#             do projeto pratico da disciplina de Programacao 1.                            #
#             A descricao do projeto encontra-se no site da disciplina e trata-se           #
#             de uma adaptacao do projeto disponivel em                                     #
#             http://nifty.stanford.edu/2016/manley-urness-movie-review-sentiment/          #
#             O objetivo deste projeto e' implementar um sistema de analise de              #
#             sentimentos de comentarios de filmes postados no site Rotten Tomatoes.        #
#                                                                                           #
# Licenca:    The MIT License (MIT)                                                         #
#             Copyright(c) 2016 Renata Kelly da Silva Amorim, Vinicius Giles Costa Paulino  #
#                                                                                           #
#############################################################################################

import sys
import re

def clean_up(s):
    ''' Retorna uma versao da string 's' na qual todas as letras sao
        convertidas para minusculas e caracteres de pontuacao sao removidos
        de ambos os extremos. A pontuacao presente no interior da string
        e' mantida intacta.
    '''    
    punctuation = ''''!"'`,;:.-?)([]<>*#\n\t\r\\'''''
    result = s.lower().strip(punctuation)
    return result

def split_on_separators(original, separators):
    ''' Retorna um vetor de strings nao vazias obtido a partir da quebra
        da string original em qualquer dos caracteres contidos em 'separators'.
        'separators' e' uma string formada com caracteres unicos a serem usados
        como separadores. Por exemplo, '^$' e' uma string valida, indicando que
        a string original sera quebrada em '^' e '$'.
    '''            
    return list(filter(lambda x: x != '',re.split('[{0}]'.format(separators),original)))

def checkTokens(listTokens, listStopWords):
    ''' Retorna um vetor com todos os tokens limpos (usando a clean_up())
        excluindo strings vazias e stop words. O vetor passado como 
        parametro deve ter sido ja' retornado pela funcao split_on_separators().
        listTokens e' um vetor de strings com todas as palavras de um comentario
        do conjunto de treino ou teste.
        listStopWords e' um vetor contendo todas as palavras que nao devem ser
        consideradas ao computar o sentimento de um comentario.
    '''
    listCleanTokens = list()
    for token in listTokens:
        token = clean_up(token)
        if token != '' and len(token) != 1 and token not in listStopWords and not token.isdigit():
            listCleanTokens.append(token)
    return listCleanTokens

def readStopWordsSet(fname):
    ''' Retorna um vetor com todas as stop words do arquivo passado
        no parametro.
    '''
    arquivo = open(fname, 'r')
    # Le todas as palavras
    stopWordsList = list()
    for word in arquivo.readlines():
        stopWordsList.append(clean_up(word))
    return stopWordsList

def readTrainingSet(fname, listStopWords):
    ''' Recebe o caminho do arquivo com o conjunto de treinamento como parametro
        e retorna um dicionario com triplas (palavra,freq,escore) com o escore
        medio das palavras no comentarios.
        listStopWords e' um vetor contendo todas as palavras que nao devem ser
        consideradas ao computar o sentimento de um comentario. Isso e' necessario
        aqui para ser passado como parametro para a funcao checkTokens(), a qual
        fara essa verificacao nas palavras do conjunto de treinamento.
    '''
    words = dict()
    arquivo = open(fname, "r")
    # Le todas as palavras
    for lineReview in arquivo.readlines():
        scoreReview = int(lineReview[0]) # Salva o primeiro char do review
        wordsReview = checkTokens(split_on_separators(lineReview[2:], " /-"), listStopWords)
        for word in wordsReview:
            if word not in words:
                words[word] = [1,scoreReview]
            else:
                words[word][0] += 1 # Soma um na frequencia
                words[word][1] += scoreReview # Acrescenta os scores
    arquivo.close()              
    # Organiza na tripla (palavra,freq,scoreMedio)
    for word in words:
        freq = words[word][0]
        scoreMedio = int(words[word][1]) // int(freq)
        words[word] = (word, freq, scoreMedio)
    return words

def readTestSet(fname):
    ''' Esta funcao le o arquivo contendo o conjunto de teste
        retorna um vetor/lista de pares (escore,texto) dos
        comentarios presentes no arquivo.
    '''    
    reviews = []
    arquivo = open(fname, "r")
    for line in arquivo.readlines():
        reviews.append((int(line[0]), line[2:]))
    arquivo.close()
    return reviews

def computeSentiment(review,words,listStopWords):
    ''' Retorna o sentimento do comentario recebido como parametro.
        O sentimento de um comentario e' a media dos escores de suas
        palavras. Se uma palavra nao estiver no conjunto de palavras do
        conjunto de treinamento, entao seu escore e' 2.
        Review e' a parte textual de um comentario.
        Words e' o dicionario com as palavras e seus escores medios no conjunto
        de treinamento.
        listStopWords e' um vetor contendo todas as palavras que nao devem ser
        consideradas ao computar o sentimento de um comentario. Isso e' necessario
        aqui para ser passado como parametro para a funcao checkTokens(), a qual
        fara essa verificacao nas palavras do conjunto de teste.
    '''
    score = 0.0
    count = 0
    palavrasReview = checkTokens(split_on_separators(review, " /-"), listStopWords)
    if len(palavrasReview) == 0: # Caso o comentario nao tenha nenhuma palavra
        return 0
    else:
        for palavra in palavrasReview:
            if palavra not in words:
                score += 2.0
                count += 1
            else:
                score += words[palavra][2]
                count+=1
        return score/count

def computeSumSquaredErrors(reviews,words,listStopWords):
    '''    Computa a soma dos quadrados dos erros dos comentarios recebidos
        como parametro. O sentimento de um comentario e' obtido com a
        funcao computeSentiment. 
        Reviews e' um vetor de pares (escore,texto)
        Words e' um dicionario com as palavras e seus escores medios no conjunto
        de treinamento.    
    '''    
    sse = 0
    for review in reviews:
        # review e' um par. review[0] = escore, review[1] = texto
        sentiment = computeSentiment(review[1], words, listStopWords)
        sse += (sentiment - review[0])**2 # Sentiment - Score
    return sse / len(reviews)

def main():
    # Os arquivos sao passados como argumentos da linha de comando para o programa
    # Voce deve buscar mais informacoes sobre o funcionamento disso (e' parte do
    # projeto).
    
    # A ordem dos parametros e' a seguinte: o primeiro e' o nome do arquivo
    # com o conjunto de treinamento, o arquivo do conjunto de teste, em seguida
    # o arquivo do conjunto de stop words.
    
    if len(sys.argv) < 3:
        print('Numero invalido de argumentos')
        print('O programa deve ser executado como python sentiment_analysis.py <arq-treino> <arq-teste> <arq-stopwords>')
        sys.exit(0)
    elif len(sys.argv) > 3:
        # Le o conjunto de stop words caso seja dado um quarto argumento na chamada
        stopwords = readStopWordsSet(sys.argv[3])
    else:
        # Se nao houver o quarto argumento, le o arquivo padrao
        stopwords = readStopWordsSet('stopWordsSet.txt')
    
    # Lendo conjunto de treinamento e computando escore das palavras
    words = readTrainingSet(sys.argv[1], stopwords)
    
    # Lendo conjunto de teste
    reviews = readTestSet(sys.argv[2])
    
    # Inferindo sentimento e computando soma dos quadrados dos erros
    sse = computeSumSquaredErrors(reviews,words,stopwords)
    
    print('A soma do quadrado dos erros e\': {0}'.format(sse))            

if __name__ == '__main__':
    main()
