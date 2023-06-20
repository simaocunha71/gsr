import datetime

def get_timestamp ():
    """Função que vai devolver dois resultados: nº de dias em que o agente começou (Anos + Meses + Dias) 
    e o nº de segundos em que o agente começou (Horas + Minutos + Segundos) - função apenas usada no grupo System"""
    now = datetime.datetime.now()

    year = now.year
    month = now.month
    day = now.day

    date = year*104 + month*102 + day

    hour = now.hour
    minute = now.minute
    second = now.second

    time = hour*104 + minute*102 + second

    return date, time