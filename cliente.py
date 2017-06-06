# -*- coding: utf-8 -*-
import funciones
import Pyro4
import servidor

login  = ''

def main():

    global login, conexion
    sub_band=0
    #conexion = servidor.Run_super('127.0.0.1', 'root', '', 'paginas')
    uri = "paginas.com"
    conexion = Pyro4.Proxy("PYRONAME:"+uri)

    conectar = servidor.Run_super('127.0.0.1', 'root', '', 'paginas')

    while True:

        if login == '':

            verificar = conectar.Validar()

            #verificar = funciones.validar(usuario,password)
            #login = 'true'
            print verificar

            if verificar != 0:
                login = 'true'

        else:

            if verificar == 1: # Si el usuario es administrador

                login = 'true'
                funciones.menuAdmin()

                opcion = int(raw_input("Ingrese una Opción: "))

                if opcion == 1:
                    #print conexion.Sumar(a, b)
                    conectar.Registrar()

                    #if result:
                     #   print "Página Registrada"

                if opcion == 2:

                    conectar.PClaves()
                    #print result

                if opcion == 3:

                    result = conectar.Listar()

                    for resp in result:
                        print "ID = %d, Pagina = %s, Palabras Clave = %s" % (resp[0], resp[1], resp[2])

                if opcion == 4:

                    funciones.salir()
                    login = ''

            elif verificar == 2: # Si el usuario es cliente

                login = 'true'
                if(sub_band==0):
                    funciones.menuCliente()
                    opcion = int(raw_input("Ingrese una Opción: "))
                else:
                    option = 4

                if opcion == 1: #Listar Páginas
                    sub_band = 0
                    result = conectar.Listar()

                    for resp in result:
                        print "ID = %d, Pagina = %s, Palabras Clave = %s" % (resp[0], resp[1], resp[2])

                if opcion == 2: #Eliminar Páginas
                    sub_band = 0
                    conectar.Eliminar()

                if opcion == 3:
                    sub_band = 0
                    #print conexion.Sumar(a, b)
                    conectar.Registrar()

                if opcion == 4:
                    sub_band=1
                    funciones.SubmenuCliente()
                    opt = raw_input("Ingrese una Opción: ")

                    if opt == 'a' or opt == 'A':

                        conectar.Palabras()

                    if opt == 'b' or opt == 'B':

                        result = conectar.Diccionario()

                        for resp in result:
                            print "Palabras Clave = %s" % (resp[0])

                    if opt == 'c' or opt == 'C':

                        conectar.Count_Img()

                    if opt == 'd' or opt == 'D':

                        conectar.PrintLinks()

                    if opt == 'e' or opt == 'E':

                        conectar.AnalizeUrl()

                    if opt == 'f' or opt == 'F':

                        conectar.PrintMetaKeywords()

                    if opt == 'h' or opt == 'H':

                        conectar.Estructura()

                    if opt == 'i' or opt == 'I':

                        conectar.Penalizar()

                    if opt == 'j' or opt == 'J':
                        conectar.Pdudoso()

                    if opt == 'l' or opt == 'L':

                        conectar.Librerias()

                    if opt == 'm' or opt == 'M':

                        conectar.Externos()

                    if opt == 'o' or opt == 'O':

                        funciones.menuCliente()
                        sub_band = 0

                if opcion == 5:
                    #print conexion.Sumar(a, b)
                    conectar.Ranking()
                    sub_band = 0

                if opcion == 6:
                    sub_band = 0
                    result = conectar.Listar_penalizadas()
                    for resp in result:
                        print "ID = %d, Pagina = %s" % (resp[0], resp[1])

                if opcion == 7:
                    sub_band = 0
                    funciones.salir()
                    login = ''

            else: # Si el usuario o pass es erróneo

                login = ''
                print "Error de Usuario"


if __name__ == '__main__':
    main()