from  django.db import connection
from .models import RegistroCordoes

def registro_cordao(ChS,cod_placa, id_placa,list_sensor):

    with connection.cursor() as cursor:
        s   =   list_sensor #10
        
        if ChS is not None:
            chs             =   ChS.cordao_fisico
            start_index     =   chs.find('Ch')
        
            # Se encontrar o prefixo 'Ch'
            if start_index != -1:
                # Inicializar uma lista para coletar os dígitos após 'Ch'
                number_str = ''

                # Iterar sobre os caracteres após 'Ch'
                for char in chs[start_index + 2:]:
                    # Se o caractere for um dígito, adicioná-lo à string number_str
                    if char.isdigit():
                        number_str += char
                    else:
                        break  # Parar o loop se encontrarmos algo que não é um dígito

                # Converter a string de dígitos em um número inteiro, se houver dígitos
                number = int(number_str) if number_str else 0
            else:
                number = 0  # Definir número como 0 se o prefixo 'Ch' não for encontrado

              # Imprimir o número extraído (pode ser removido se não for necessário)
            for _ in s:
                number += 1
                
                for s in _:
                    cordao_fisico = f"Ch{number}S{s}"
                    cursor.execute('INSERT INTO registro_cordoes (cod_placa,placa_id,cordao_fisico) \
                                    VALUES (%s,%s,%s)', [cod_placa,id_placa,cordao_fisico]) 
            

        else:
            number = 0
            for _ in s:
                number += 1
                #print(number)
                for s in _:
                    cordao_fisico = f"Ch{number}S{s}"
                    cursor.execute('INSERT INTO registro_cordoes (cod_placa,placa_id,cordao_fisico) \
                                    VALUES (%s,%s,%s)', [cod_placa,id_placa,cordao_fisico]) 
                


def update_canal_sensor(cordao_sensor, canal,sensor):

      with connection.cursor() as cursor:
        for indice , teste_um in enumerate(cordao_sensor):

            t2      =   canal[indice]
            t3      =   sensor[indice]

            sql     =   'UPDATE registro_cordoes SET canal_placa = %s, sensor_placa = %s ' \
                        'WHERE cordao_fisico = %s'
            params  =   [t2,t3,teste_um]
                     
            if t2 != '' and  t3 != '':  
                cursor.execute(sql, params)



def update_cod_placa(cod_placa, id_placa):
    with connection.cursor() as cursor:
        sql     =   'UPDATE registro_cordoes SET cod_placa = %s WHERE placa_id = %s'
        params  =   [cod_placa, id_placa]

        cursor.execute(sql, params)



def registrar_canal_sensor(ultimo_sensor, ultimo_canal, lista_sensor):
    max_sensor      =   16
    max_canal       =   16

    sensor_placa    =   ultimo_sensor
    canal_placa     =   ultimo_canal

  

    if sensor_placa     ==  0:
        sensor_placa    =   0
        canal_placa     =   1

    sensor_livre    =   max_sensor - sensor_placa

    

    with connection.cursor() as cursor:
        for sensores in lista_sensor:
            for sensor in sensores:
                sensor_placa += 1
                if sensor_placa == 17:
                    sensor_placa = 1
                    canal_placa += 1                

                if max_sensor >= sensor_placa:
                    sql = 'UPDATE registro_cordoes SET sensor_placa = %s, canal_placa = %s WHERE sensor_placa IS NULL LIMIT 1'
                    params = [sensor_placa, canal_placa]
                    cursor.execute(sql, params)

                

def cadastrar_cordao_manual(cod_placa,ip_placa,cordao_fisico,canal, sensor):

    with connection.cursor() as cursor:

        for index, cod in enumerate(cod_placa):

            ip = ip_placa[index]
            cordao = cordao_fisico[index]
            canais = canal[index]
            sensores = sensor[index]


            cursor.execute('INSERT INTO registro_cordoes (cod_placa, cordao_fisico, canal_placa, sensor_placa, placa_id)\
                           VALUES(%s,%s,%s,%s,%s)', [cod, cordao,canais, sensores, ip])
