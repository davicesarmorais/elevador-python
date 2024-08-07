""" Implementação original do elevador 
sem usar bibliotecas para terminal """

import random
import threading
import keyboard
import os, time

# Variáveis -------------------------------------

desligar_elevador = False
fila_subir = []
fila_descer = []
direcao_elevador = 'parado'
andar_selecionado = ''
andar_atual = 0

# -----------------------------------------------

def parar_nos_andares():
    global fila_subir, fila_descer

    if direcao_elevador == "subindo":
        # Pega no caminho
        if int(andar_atual) in fila_subir:
            fila_subir.remove(int(andar_atual))
        
        # Muda de direção
        elif fila_descer and (int(andar_atual) == fila_descer[0]):
            if ((not fila_subir) 
            or (fila_subir and (fila_descer[0] > fila_subir[-1]))):  
                fila_descer.remove(int(andar_atual))

    elif direcao_elevador == "descendo":
        # Pega no caminho
        if int(andar_atual) in fila_descer:
            fila_descer.remove(int(andar_atual))
        
        # Muda de direção
        elif fila_subir and (int(andar_atual) == fila_subir[0]):
            if ((not fila_descer) 
            or (fila_descer and (fila_descer[-1] > fila_subir[0]))):  
                fila_subir.remove(int(andar_atual))


def movimentar_elevador():
    global andar_atual, direcao_elevador

    valor_maximo = max(max(fila_subir, default=float('-inf')), 
                       max(fila_descer, default=float('-inf')))

    valor_minimo = min(min(fila_subir, default=float('+inf')), 
                       min(fila_descer, default=float('+inf')))

    if ((fila_subir or fila_descer)
    and (int(andar_atual) < valor_maximo)
    and (direcao_elevador != "descendo")):
        direcao_elevador = "subindo"
        andar_atual += 0.1

    elif ((andar_atual > valor_minimo)  
    or (andar_atual > 0)
    and (not fila_descer and not fila_subir)):  
        direcao_elevador = "descendo"
        andar_atual -= 0.1
    
    else:
        direcao_elevador = "parado"


def adicionar_a_fila(evento):
    global andar_selecionado
    global fila_descer, fila_subir
    
    andar_selecionado = int(andar_selecionado)
    if evento == 'up' and andar_selecionado not in fila_subir:
        fila_subir.append(andar_selecionado)
    elif evento == 'down' and andar_selecionado not in fila_descer:
        fila_descer.append(andar_selecionado)

    fila_descer.sort(reverse=True)
    fila_subir.sort(reverse=False)
    andar_selecionado = ''


def on_key_event(event):
    global andar_selecionado, desligar_elevador
    
    if event.name == 'esc':
        desligar_elevador = True
        return
    
    andar_selecionado = random.randrange(0, 29)
    evento = random.choice(['up', 'down'])
    adicionar_a_fila(evento)
           
    
def start_key_listener():
    keyboard.on_press(on_key_event)
        
# Programa -------------------------------------

def elevador():   
    while True:
        os.system('cls')
        print(f"Andares: 0 - 28")
        print(f"Fila subindo: [{', '.join(map(str, fila_subir))}]")
        print(f"Fila descendo: [{', '.join(map(str, fila_descer))}]")
        print(f"Elevador {direcao_elevador}")
        print(f"Andar atual: {int(andar_atual)}")
        print(f"\nAndar selecionado: {andar_selecionado}")

        print(f"Isso é uma demonstração (aperte qualquer tecla para selecionar um andar).")
        print("Aperte 'esc' para encerrar o programa.")
        
        if desligar_elevador:
            break
        
        movimentar_elevador()
        parar_nos_andares()
        time.sleep(0.1)
        
            
listener_thread = threading.Thread(target=start_key_listener)
task_thread = threading.Thread(target=elevador)

listener_thread.start()
task_thread.start()

listener_thread.join()
task_thread.join()
