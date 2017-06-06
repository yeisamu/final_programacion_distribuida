# -*- coding: utf-8 -*-
def menuAdmin():

    print "******** Administrador ********"
    print "------------------------------------------"
    print "1. Registro de Empresas (Páginas Web)"
    print "2. Agregar Palabras Clave"
    print "3. Consultar Empresas Registradas (Páginas)"
    print "4. Cerrar Sesión"
    print "------------------------------------------"

def menuCliente():

    print "******** Cliente ********"
    print "------------------------------------"
    print "1. Listado de Páginas"
    print "2. Eliminar Páginas Web"
    print "3. Agregar Nueva Página"
    print "4. Información SEO de un sitio Web"
    print "5. Ranking de Todos los Sitios Agregados"
    print "6. Listado de Páginas Penalizadas"
    print "7. Cerrar Sesión"
    print "------------------------------------"

def SubmenuCliente():

    print "******** Información Sitio Web ********"
    print "------------------------------------"
    print "a. Contar Palabras (MapReduce)"
    print "b. Diccionario de Palabras Clave"
    print "c. Contar Imágenes"
    print "d. Contar Enlaces Internos y Externos"
    print "e. Analizar URL"
    print "f. Analizar Palabras Clave (Keywords)"
    print "h. Estructura del Sitio Web"
    print "i. Penalizar Contenido No Apto"
    print "j. Penalizar Contenido de Dudosa Reputación"
    print "k. Penalizar Malas Prácticas de Desarrollo Web"
    print "l. Información de Librerias Usadas en el Sitio"
    print "m. Comprobar Enlaces Externos"
    print "n. Si se enlaza a una página web almacenada en el servidor debe dar más puntuación????"
    print "o. Regresar a Menú Principal"
    print "------------------------------------"

def RevisarLog():
    log = bd.listar_Log()
    return log

def salir():
    print "Sesión cerrada con Éxito"
    #exit(0)