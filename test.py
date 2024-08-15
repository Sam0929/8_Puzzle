import random

def funcao_avaliadora(estado: list) -> bool:
    estado_final = [[1,2,3],[4,5,6],[7,8,"X"]]
    print(estado_final)
    if estado == estado_final:
        return True
    
    return False

def cria_estado():
    estado = [1,2,3,4,5,6,7,8,"X"]
    random.shuffle(estado)
    print(estado)

if __name__ == "__main__":
    # estado = [[1,2,5],[4,3,6],[7,8,"X"]]
    # print(funcao_avaliadora(estado))
    cria_estado()