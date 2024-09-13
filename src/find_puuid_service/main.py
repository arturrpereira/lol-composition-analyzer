''''
    consumer.py
        - captura os summuner ids de uma fila
    
    send.py
        - Envia os PUUIDs encontrados para uma fila

    * callback function do consumer.py
        - acessa o endpoint -> /lol/match/v5/matches/by-puuid/{puuid}/ids
        - retorna o PUUID

'''
