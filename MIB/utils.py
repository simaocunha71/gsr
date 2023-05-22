#Valores dos objetos vão ser dados estaticamente através de variaveis globais. 
#Na versão definitiva, o agente vai passar estes argumentos para a classe MIB, que por sua vez vai passar para o grupo system/config/keys

#TODO: Fazer funçoes auxiliares de povoaçao dos objetos da MIB

import datetime

def get_timestamp ():
    """Função que vai devolver dois resultados: nº de dias em que o agente começou (Anos + Meses + Dias) 
    e o nº de segundos em que o agente começou (Horas + Minutos + Segundos)"""
    now = datetime.datetime.now()

    year = now.year
    month = now.month
    day = now.day

    date = year*104 + month*102 + day
    #print(str(year) + '/' + str(month) + '/' + str(day))

    hour = now.hour
    minute = now.minute
    second = now.second

    time = hour*104 + minute*102 + second
    #print(str(hour) + ':' + str(minute) + ':' + str(second))

    return date, time

#print (get_timestamp())