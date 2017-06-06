# -*- coding: utf-8 -*-
import hashlib
import MySQLdb
import Tkinter, tkSimpleDialog
import requests
from bs4 import BeautifulSoup
from urlparse import urlparse
import urllib
import funciones

import urllib2,unicodedata

import multiprocessing
import string

from multiprocess_mapreduce import SimpleMapReduce

import operator
import glob

import Pyro4

HOST = '127.0.0.1'
USER = 'root'
PASSWORD = ''
DATABASE = 'paginas'

@Pyro4.expose

class Run_super:

    def __init__(self, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME):
        self.host = DB_HOST
        self.name = DB_NAME
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.conn = None
        self.conn = MySQLdb.connect(host=self.host,
                                        user=self.user,
                                        passwd=self.password,
                                        db=self.name)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def run_query(self,query=''):

        cursor = self.conn.cursor()  # Crear un cursor
        cursor.execute(query)  # Ejecutar una consulta

        if query.upper().startswith('SELECT'):
            data = cursor.fetchall()  # Traer los resultados de un select
        else:
            self.conn.commit()  # Hacer efectiva la escritura de datos
            # data = None
            data = cursor.fetchall()  # Traer los resultados de un select
        #cursor.close()  # Cerrar el cursor
        #self.conn.close()  # Cerrar la conexión
        return data

    def Validar(self):

        usuario = raw_input("Ingrese Nombre de Usuario: ")
        #clave = raw_input("Digite Clave: ")
        root = Tkinter.Tk()  # dialog needs a root window, or will create an "ugly" one for you
        root.withdraw()  # hide the root window
        clave = tkSimpleDialog.askstring("Clave de Usuario", "Digite su Clave:", show='*', parent=root)
        # tkSimpleDialog.focus()
        if clave == None:
            clave = ''

        p = hashlib.new('md5', clave)
        passw = p.hexdigest()

        sql = "SELECT * FROM (usuarios AS U INNER JOIN tipo_usuario AS TU ON U.tipo_user = TU.id) WHERE email = '" + usuario + "' AND pass='" + passw + "'"
        #print sql
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        #print result
        if result:
            #print "Entro"
            for registro in result:
                datos = registro[4]
        else:
            datos = 0

        return datos

    def Listar(self):

        result = None
        query = "SELECT * from paginas"

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            if result:
                datos = result
            else:
                datos = 'No Hay Datos'
        except:
            print "Error en Datos"

        # print datos
        return datos

    def Registrar(self):

        pagina = raw_input("Digite Nombre de la Página sin http:// : ")

        sql = 'INSERT INTO paginas (url, pclave) VALUES ("%s","%s")' % ('http://'+pagina,'')
        self.cursor.execute(sql)
        self.conn.commit()

    def Eliminar(self):

        result = self.Listar()

        print "_____________________________________"
        print "Páginas Registradas"

        for resp in result:

            print "ID = %d, Pagina = %s, Palabras Clave = %s" % (resp[0], resp[1], resp[2])

        print "_____________________________________"

        id = int(raw_input("Digite id de la Página a Eliminar: "))

        sql = "DELETE FROM paginas WHERE id = %i" % (int(id))
        #print sql
        self.cursor.execute(sql)
        self.conn.commit()

    def PClaves(self):

        result = self.Listar()

        print "_____________________________________"
        print "Páginas Registradas"

        for resp in result:

            print "ID = %d, Pagina = %s, Palabras Clave = %s" % (resp[0], resp[1], resp[2])

        print "_____________________________________"
        id = int(raw_input("Digite id de la Página: "))
        pclave = raw_input("Ingrese Palabras Claves: ")

        sql = "UPDATE paginas SET pclave='%s' WHERE id = %i" % (pclave, int(id))
        #print sql
        self.cursor.execute(sql)
        self.conn.commit()

    def Listar_penalizadas(self):

        result = None
        query = "SELECT * from paginas where penalizado='si'"
        print "_____________________________________"
        print "Páginas Penalizadas"
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            if result:

                datos = result
            else:
                datos = 'No Hay Datos'
        except:
            print "Error en Datos"

        # print datos
        return datos

    def Penalizar(self):

        result = self.Listar()
        betado=0
        palabraspenaliza = set([
            'porno', 'xxx', 'sexo', 'pene', 'vagina', 'apuestas', 'sexualidad', 'pornográficos', 'consolador', 'dildo',
            'viagra','james','espn',
        ])

        print "_____________________________________"
        print "Páginas Registradas"

        for resp in result:
            print "ID = %d, Pagina = %s, Palabras Clave = %s" % (resp[0], resp[1], resp[2])

        print "_____________________________________"

        id = int(raw_input("Digite id de la Página: "))

        query = "SELECT * from paginas WHERE id = %i" % (int(id))

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            if result:

                for resp in result:
                    datos = resp[1]
                    print datos

                request = requests.get(datos)
                content = request.content
                soup = BeautifulSoup(content, "html.parser")
                for text in soup.find_all('p'):
                    texto = text.text
                    for word in texto.split(' '):
                        word = word.lower()
                        if word  in palabraspenaliza:
                            betado=betado+1

                if betado > 2:
                    sql = "UPDATE paginas SET penalizado='si' WHERE id = %i" % (int(id))
                    # print sql
                    self.cursor.execute(sql)
                    self.conn.commit()
                    print "Página penalizada por tener contenido no Apto"
                else:
                    print "Página NO tiene contenido no Apto"

        except:
            print "Error en Datos"


    def Palabras(self):

        result = self.Listar()

        print "_____________________________________"
        print "Páginas Registradas"

        for resp in result:
            print "ID = %d, Pagina = %s, Palabras Clave = %s" % (resp[0], resp[1], resp[2])

        print "_____________________________________"

        id = int(raw_input("Digite id de la Página: "))

        query = "SELECT * from paginas WHERE id = %i" % (int(id))

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            if result:

                for resp in result:
                    datos = resp[1]
                    print datos

                request = requests.get(datos)
                content = request.content
                soup = BeautifulSoup(content, "html.parser")

                f = open("archivo.txt", "w")

                for text in soup.find_all('p'):
                    texto = text.text
                    linea = texto.strip();
                    normalizado = unicodedata.normalize('NFKD', linea).encode('ascii', 'ignore')
                    # texto = text.text
                    f.write(normalizado + '\n')
                    #texto = text.text
                    #recorre = recorre + texto
                    #print texto

                #f.write(recorre)
                f.close()
                self.contadorp('archivo.txt')

        except:
            print "Error en Datos"

    def Count_Img(self):

        result = self.Listar()

        print "_____________________________________"
        print "Páginas Registradas"

        for resp in result:
            print "ID = %d, Pagina = %s" % (resp[0], resp[1])

        print "_____________________________________"

        id = int(raw_input("Digite id de la Página: "))

        query = "SELECT * from paginas WHERE id = %i" % (int(id))

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            if result:

                for resp in result:
                    datos = resp[1]
                    puntos = resp[3]
                    print datos

                request = requests.get(datos)
                content = request.content
                soup = BeautifulSoup(content, "html.parser")

                l = soup.findAll("img", attrs={"src": True})

                if len(l):

                    print "Total Imágenes = " + str(len(l))

                    # si la página contiene imágenes suma puntos

                    puntos = puntos + 1
                    sql = "UPDATE paginas SET puntos='%i' WHERE id = %i" % (puntos, int(id))
                    # print sql
                    self.cursor.execute(sql)
                    self.conn.commit()

                else:

                    print "No hay imágenes"

                    puntos = puntos - 1
                    sql = "UPDATE paginas SET puntos='%i' WHERE id = %i" % (puntos, int(id))
                    # print sql
                    self.cursor.execute(sql)
                    self.conn.commit()

            else:
                print "El sitio No tiene Imágenes"
        except:
            print "Error en Datos"

    def Diccionario(self):

        result = None
        query = "SELECT pclave from paginas"

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            if result:
                datos = result
            else:
                datos = 'No Hay Datos'
        except:
            print "Error en Datos"

        # print datos
        return datos

    def PrintMetaKeywords(self):

        mk = ''

        result = self.Listar()

        print "_____________________________________"
        print "Páginas Registradas"

        for resp in result:
            print "ID = %d, Pagina = %s" % (resp[0], resp[1])

        print "_____________________________________"

        id = int(raw_input("Digite id de la Página: "))

        query = "SELECT * from paginas WHERE id = %i" % (int(id))

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            if result:

                for resp in result:
                    datos = resp[1]
                    puntos = resp[3]
                    print datos

                request = requests.get(datos)
                content = request.content
                soup = BeautifulSoup(content, "html.parser")

                l = soup.findAll("meta", attrs={"name": "keywords"})
                if l == []:

                    mk = "No hay Meta Keywords"
                    #Si la página no contiene Meta Keywords se restan puntos
                    puntos = puntos -1
                    sql = "UPDATE paginas SET puntos='%i' WHERE id = %i" % (puntos, int(id))
                    # print sql
                    self.cursor.execute(sql)
                    self.conn.commit()

                else:

                    mk = l[0]['content'].encode('utf-8')

                    puntos = puntos + 1

                    sql = "UPDATE paginas SET puntos='%i' WHERE id = %i" % (puntos, int(id))
                    # print sql
                    self.cursor.execute(sql)
                    self.conn.commit()

                print '' + mk + ''

        except:
            print "Error en Datos"

    def PrintLinks(self):

        result = self.Listar()

        print "_____________________________________"
        print "Páginas Registradas"

        for resp in result:
            print "ID = %d, Pagina = %s" % (resp[0], resp[1])

        print "_____________________________________"

        id = int(raw_input("Digite id de la Página: "))

        query = "SELECT * from paginas WHERE id = %i" % (int(id))

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            if result:

                for resp in result:
                    datos = resp[1]
                    puntos = resp[3]
                    print datos

                localurl = datos
                request = requests.get(localurl)
                content = request.content
                soup = BeautifulSoup(content, "html.parser")

                parse = urlparse(localurl)
                localurl = parse[0] + "://" + parse[1]
                print "Enlaces de Página"

                l = soup.findAll("a", attrs={"href": True})
                print "Total Enlaces = " + str(len(l)) + ''

                if len(l) >= 50: #si el número de enlaces es mayor a 50 se resta puntos a la página

                    puntos = puntos - 1

                    sql = "UPDATE paginas SET puntos='%i' WHERE id = %i" % (puntos, int(id))
                    # print sql
                    self.cursor.execute(sql)
                    self.conn.commit()

                else:

                    puntos = puntos + 1

                    sql = "UPDATE paginas SET puntos='%i' WHERE id = %i" % (puntos, int(id))
                    # print sql
                    self.cursor.execute(sql)
                    self.conn.commit()

                externallinks = []  # external links list

                for link in l:
                    # if it's external link
                    if link['href'].find("http://") == 0 and link['href'].find(localurl) == -1:
                        externallinks = externallinks + [link]

                print "Conteo de Enlaces Externos = " + str(len(externallinks)) + ''

                #internos = l - externallinks

                #print "Conteo de Enlaces Internos = " + internos + ''

                #if len(externallinks) > 0:

                #    print "Lista de Enlaces Externos:"

                #    for link in externallinks:
                #        if link.text != '':
                #            print '' + link.text.encode('utf-8')
                #            print ' => [' + '' + link['href'] + '' + ']' + ''
                #        else:
                #            print '' + '[image]',
                #            print ' => [' + '' + link['href'] + '' + ']' + ''

        except:
            print "Error en Datos"


    def Estructura(self):

        result = self.Listar()

        print "_____________________________________"
        print "Páginas Registradas"

        for resp in result:
            print "ID = %d, Pagina = %s" % (resp[0], resp[1])

        print "_____________________________________"

        id = int(raw_input("Digite id de la Página: "))

        query = "SELECT * from paginas WHERE id = %i" % (int(id))

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            if result:

                for resp in result:
                    datos = resp[1]
                    print datos

                l = urllib.urlopen(datos).read()
                soup = BeautifulSoup(l, "html.parser")
                print soup

        except:
            print "Error en Datos"

    def Librerias(self):

        result = self.Listar()

        print "_____________________________________"
        print "Páginas Registradas"

        for resp in result:
            print "ID = %d, Pagina = %s" % (resp[0], resp[1])

        print "_____________________________________"

        id = int(raw_input("Digite id de la Página: "))

        query = "SELECT * from paginas WHERE id = %i" % (int(id))

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            if result:

                for resp in result:
                    datos = resp[1]
                    print datos

                l = requests.get(datos)
                data = l.text
                soup = BeautifulSoup(data, "html.parser")

                for link in soup.find_all('script'):
                    print(link.get('src'))

        except:
            print "Error en Datos"

    def AnalizeUrl(self):

        title = ''

        result = self.Listar()

        print "_____________________________________"
        print "Páginas Registradas"

        for resp in result:
            print "ID = %d, Pagina = %s" % (resp[0], resp[1])

        print "_____________________________________"

        id = int(raw_input("Digite id de la Página: "))

        query = "SELECT * from paginas WHERE id = %i" % (int(id))

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            if result:

                for resp in result:
                    datos = resp[1]
                    puntos = resp[3]

                request = requests.get(datos)
                estado = request.status_code
                content = request.content

                soup = BeautifulSoup(content, "html.parser")

                if soup.find('title'):

                    title = soup.find('title').string
                    # si la página tiene título se le da puntos
                    puntos = puntos + 1
                    sql = "UPDATE paginas SET puntos='%i' WHERE id = %i" % (puntos, int(id))
                    # print sql
                    self.cursor.execute(sql)
                    self.conn.commit()

                else:

                    title = 'N/A'
                    #Se le resta puntos por no tener título
                    puntos = puntos - 1
                    sql = "UPDATE paginas SET puntos='%i' WHERE id = %i" % (puntos, int(id))
                    # print sql
                    self.cursor.execute(sql)
                    self.conn.commit()

                l = soup.findAll("meta", attrs={"name": "description"})

                if l == []:
                    md = "N/A"
                else:
                    md = l[0]['content'].encode('utf-8')

                print "Pagina = %s, Estado = %s, Titulo = %s, Meta = %s" % (datos, estado, title, md)

        except:

            print "Error en Datos"

    def Externos(self):

        result = self.Listar()

        print "_____________________________________"
        print "Páginas Registradas"

        for resp in result:
            print "ID = %d, Pagina = %s" % (resp[0], resp[1])

        print "_____________________________________"

        id = int(raw_input("Digite id de la Página: "))

        query = "SELECT * from paginas WHERE id = %i" % (int(id))

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            if result:

                for resp in result:
                    datos = resp[1]
                    puntos = resp[3]
                    print datos

                localurl = datos
                request = requests.get(localurl)
                content = request.content
                soup = BeautifulSoup(content, "html.parser")

                parse = urlparse(localurl)
                localurl = parse[0] + "://" + parse[1]
                #print "Enlaces de Página"

                l = soup.findAll("a", attrs={"href": True})
                #print "Total Enlaces = " + str(len(l)) + ''
                externallinks = []  # external links list

                for link in l:
                    # if it's external link
                    if link['href'].find("http://") == 0 and link['href'].find(localurl) == -1:
                        externallinks = externallinks + [link]

                print "Conteo de Enlaces Externos = " + str(len(externallinks)) + ''

                if len(externallinks) > 0:
                    # si la página contiene enlaces externos resta puntos
                    puntos = puntos - 1
                    sql = "UPDATE paginas SET puntos='%i' WHERE id = %i" % (puntos, int(id))
                    # print sql
                    self.cursor.execute(sql)
                    self.conn.commit()

                    print "Lista de Enlaces Externos:"

                    for link in externallinks:
                        if link.text != '':
                            print '' + link.text.encode('utf-8')
                            print ' => [' + '' + link['href'] + '' + ']' + ''
                        else:
                            print '' + '[image]',
                            print ' => [' + '' + link['href'] + '' + ']' + ''
                else:
                    # si la página no contiene enlaces externos suma puntos
                    puntos = puntos + 1
                    sql = "UPDATE paginas SET puntos='%i' WHERE id = %i" % (puntos, int(id))
                    # print sql
                    self.cursor.execute(sql)
                    self.conn.commit()

        except:
            print "Error en Datos"

    def Pdudoso(self):

        result = self.Listar()
        betado = 0
        palabraspenaliza = set([
            'porno', 'xxx', 'sexo', 'pene', 'vagina', 'apuestas', 'sexualidad', 'pornográficos', 'consolador', 'dildo',
            'viagra', 'james', 'espn',
        ])
        print "_____________________________________"
        print "Páginas Registradas"

        for resp in result:
            print "ID = %d, Pagina = %s, Palabras Clave = %s" % (resp[0], resp[1], resp[2])

        print "_____________________________________"

        id = int(raw_input("Digite id de la Página: "))

        query = "SELECT * from paginas WHERE id = %i" % (int(id))

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            if result:

                for resp in result:
                    datos = resp[1]
                    print datos

                request = requests.get(datos)
                content = request.content
                soup = BeautifulSoup(content, "html.parser")
                for text in soup.findAll("a", attrs={"href": True}):
                    texto = text.text
                    for word in texto.split(' '):
                        word = word.lower()
                        if word in palabraspenaliza:
                            betado = betado + 1

                if betado > 2:
                    sql = "UPDATE paginas SET dudoso='si' WHERE id = %i" % (int(id))
                    # print sql
                    self.cursor.execute(sql)
                    self.conn.commit()
                    print "Página penalizada por tener contenido de dudosa reputacion"
                else:
                    print "Página NO tiene contenido dudoso"


        except:
            print "Error en Datos"
    def Ranking(self):

        result = None
        query = "SELECT * from paginas ORDER BY puntos DESC"

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            if result:

                for resp in result:
                    print "ID = %d, Pagina = %s, Puntos = %s" % (resp[0], resp[1], resp[3])

            else:
                print 'No Hay Datos'

        except:
            print "Error en Datos"

    def __del__(self):
        print '\n Terminando Operaciones...'
        #self.cursor.close()
        #self.conn.close()
        print 'Finalizado.\n'

    def contadorp(self,archivo):
        import operator
        import glob

        input_files = glob.glob(archivo)

        mapper = SimpleMapReduce(file_to_words, count_words)
        word_counts = mapper(input_files)
        word_counts.sort(key=operator.itemgetter(1))
        word_counts.reverse()

        print '\nTOP 20 principales palabras\n'
        top20 = word_counts[:20]
        longest = max(len(word) for word, count in top20)
        for word, count in top20:
            print '%-*s: %5s' % (longest + 1, word, count)

def file_to_words(filename):
    STOP_WORDS = set([
        'la', 'las', 'y', 'de', 'en', 'del', 'los', 'que', 'si', 'a',
        'se', 'su', 'al', 'por', 'o', 'con', 'para', 'el', 'desde', 'hasta',
        'un', 'no', 'ante', 'como', 'lo', 'cual', 'una', 'mas', 'entre', 'sobre',
    ])
    TR = string.maketrans(string.punctuation, ' ' * len(string.punctuation))

    print multiprocessing.current_process().name, 'reading', filename
    output = []

    with open(filename, 'rt') as f:
        for line in f:
            if line.lstrip().startswith('..'):  # Skip rst comment lines
                continue
            line = line.translate(TR)  # Strip punctuation
            for word in line.split():
                word = word.lower()
                if word.isalpha() and word not in STOP_WORDS:
                    output.append((word, 1))
    return output

def count_words(item):
    word, occurances = item
    return (word, sum(occurances))

def main():

    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(Run_super) # Dirección de ejecucion
    ns.register("paginas.com", uri)
    daemon.requestLoop() # Cerrar la conexión

if __name__ == '__main__':
    main()