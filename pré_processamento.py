"""
    29.07.2018 || UNIVERSIDADE DO ESTADO DO RIO DE JANEIRO (UERJ)
    Autores:  Fernanda Milagres
              Gabriel de Miranda Pontes da Silva
              Leonídia Barreto
    Mentora: Karla Figueiredo
    Projeto: Desenvolvimento de Bibliotecas em Python para Data Science.
    Biblioteca desenvolvida para auxiliar na Normalização dos dados, descoberta de Outliers e reenchimento dos Missing values da base de dados.    
"""

import pandas as pd
import numpy as np

def initialize(link, name):
    file = pd.read_excel(link, name)
    df = pd.DataFrame(file)
    #df = df.replace('?', 'NaN')
    return df

def taxa_missing(df, coluna_planilha):
    num = denom = 0

    for k in df[coluna_planilha]:
        if k == '?':
            num += 1
        denom += 1

    print('Numero de missings: {0}'.format(num))
    print('Numero total: {0}'.format(denom))
    
               


        

def normalizacao_min_max(df, coluna_planilha):        
    col = []
    for k in df[coluna_planilha]:
        if k != 'NaN':
            col.append(lambda k: [(k - min(df[coluna_planilha]))/(max(df[coluna_planilha]) - min(df[coluna_planilha]))])
        
        """
        col = []
        col =  [ col.apply(lambda k: [(k - min(self._df[coluna_planilha]))/(max(self._df[coluna_planilha]) - min(self._df[coluna_planilha]))]) for k in self._df[coluna_planilha] if k != 'NaN']
        """
    return col
 
def normalizacao_min_max_supervisionado(df, coluna_planilha, coluna_planilha_class, index): #index é a categoria numérica da classe
    col = coluna_planilha[coluna_planilha_class == index]
    coluna_planilha['norm'] = col.apply(lambda x: [(x - min(col))/(max(col)-min(col))])
    return coluna_planilha['norm']
    
    

    


def media(df, coluna_planilha):
    """
        Determina a média dos registros numéricos de um atributo (coluna)
        do DataFrame passado como parâmetro.
    """

    soma = 0
    num = 0

    for i in df[coluna_planilha]:
        if i != 'NaN':
            soma += i
            num += 1

    return soma / num

def desvio_padrao(df, coluna_planilha):
    """
        Determina o desvio-padrão dos registros (linhas) numéricos
        de um atributo (coluna) do DataFrame passado como parâmetro.
    """

    Ma = media(df, coluna_planilha)
    n = 0
    soma = 0
    
    for k in df[coluna_planilha]:
        if k != 'NaN':
            teste = (k - Ma) ** 2
            soma += teste
            n  += 1

    return (soma/n) ** 0.5

def outlier_desvio_padrao(df, coluna_planilha, desvio, media, entrada):
    """
        Identifica outliers nos registros de um atributo
        utilizando-se do desvio e média desta coluna.
    """         
    
    j = entrada
    
    for k in df[coluna_planilha]:
        if isinstance(k, int):
            if abs(k - media) > desvio:
                outlier.append(j)
            j += 1        

def media_supervisionada(df, coluna_planilha, coluna_planilha_class, output_class):
    """
        Determina a média de um atributo de acordo com
        a classe de saída especificada no parâmetro.
    """

    soma = 0
    num = 0
    k = 0

    for j in df[coluna_planilha_class]:
        if j == output_class:
            if isinstance(df.loc[k, coluna_planilha], (float, int)):
                soma += df.loc[k, coluna_planilha]
                num += 1
        k += 1
                
    return soma / num

def desvio_padrao_supervisionado(df, coluna_planilha, atributo_saida, classe_saida):
    """
        Determina o desvio-padrão de um atributo de acordo
        com a classe de saída especificada no parâmetro.

        Parametros
        ----------
                classe_saida : Especifica a classe de saída que será trabalhada.
                               costuma ser uma classe categórica (quando se trata de classificação),
                               mas também é possível valores numéricos (para inferências).                 
    """
    
    media_super = media_supervisionada(df, coluna_planilha, coluna_planilha_class, output_class)
    n = 0
    soma = 0
    z = 0
    
    for k  in df[coluna_planilha_class]:
        if k == output_class:
            if isinstance(df.loc[z, coluna_planilha], (float, int)):
                teste = (df.loc[z, coluna_planilha] - media_super) ** 2
                soma += teste
                n  += 1
        z += 1

    return (soma / n) ** 0.5    

def outlier_desvio_padrao_supervisionado(df, coluna_planilha, coluna_planilha_class, output_class):
    """
        Identifica outliers nos registros de um atributo utilizando-se do
        desvio-padrão supervisionado e a média supervisionada desta coluna.
    """

    j = 0
    media_ = media_supervisionada(df, coluna_planilha, coluna_planilha_class, output_class)
    desvio_ = desvio_padrao_supervisionado(df, coluna_planilha, coluna_planilha_class, output_class)
    
    for k in df[coluna_planilha_class]:
        if k == output_class:
            if abs(df.loc[j, coluna_planilha] - media_) > desvio_:
                    outlier.append(j)
        j += 1

def outlier_categorico(df, coluna_planilha, frequencia):
    """
        Função para informar outliers em dados categóricos (dados não-numéricos)
        de determinado atributo.
    """


    tool = []
    outlier = []
    
    for k in df[coluna_planilha]:
        if k not in tool:
            if isinstance(k, int):
                tool.append(k)
    
    x  = 0
    for k in tool:
        y = 0
        valor = k
        cont = 0
             
        for j in df[coluna_planilha]:
            if j == k:
                cont += 1
            y += 1
                 
        freq = cont / y
             
        if freq < frequencia:
            outlier.append(k)
                 
def outlier_desvio_padrao_supervisionado(df, coluna_planilha, coluna_planilha_classe, frequencia):
    pass







def missing_media_moda(df, coluna_planilha, classe_saida):
    for k in df[coluna_planilha]:
        if k != np.nan:
            if isinstance(k, (int, float)):
                df.loc[k , coluna_planilha] = media_supervisionada(df, coluna_planilha, coluna_planilha_classe, classe_saida)
            else:
                df.loc[k, coluna_planilha] = moda_supervisionada(df, coluna_planilha, coluna_planilha_classe, classe_saida)
                
        
        
            

def troca_missing_value(coluna_testada, coluna_tipo):         
        """
            no_numeric = [] -> Vetor que guarda as posições dos valores não numéricos de cada coluna.
            tipo = []       -> Vetor que guarda o tipo relativo ao missing value.
        """

        for i,j in coluna_testada, coluna_tipo:
            if i == '?':             # not(isinstance(i, (int)))
                '''
                    no_numeric.append(i)
                    tipo.append(j)
                '''
                i = missing_media(coluna_testada, coluna_tipo, j)
                
                 
                 
