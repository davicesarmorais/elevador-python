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
    
    if direcao_elevador == 'subindo':
        if int(andar_atual) in fila_subir:
            fila_subir.remove(int(andar_atual))
        elif fila_descer and (int(andar_atual) == fila_descer[0]):
            if (fila_subir) and (fila_descer[0] > fila_subir[0]):
                fila_descer.remove(int(andar_atual))
            elif (not fila_subir):
                fila_descer.remove(int(andar_atual))   
        
    elif direcao_elevador == 'descendo':
        if int(andar_atual) in fila_descer:
            fila_descer.remove(int(andar_atual))
        elif fila_subir and int(andar_atual) == fila_subir[0]:
            if (fila_descer) and (fila_descer[0] > fila_subir[0]):
                fila_subir.remove(int(andar_atual))
            elif (not fila_descer):
                fila_subir.remove(int(andar_atual))
        

def movimentar_elevador():
    global andar_atual, direcao_elevador
    
    max_subindo = max(fila_subir) if fila_subir else float('-inf')
    max_descendo = max(fila_descer) if fila_descer else float('-inf')
    valor_maximo = max(max_subindo, max_descendo)
    
    if ((fila_subir or fila_descer) 
        and (int(andar_atual) < valor_maximo) 
        and (direcao_elevador != 'descendo')
        ):
        direcao_elevador = 'subindo'
        andar_atual += 0.1
    
    elif andar_atual > 0:
        direcao_elevador = 'descendo'
        andar_atual -= 0.1
    else:
        direcao_elevador = 'parado'
        
        
def adicionar_a_fila(evento):
    global andar_selecionado
    global fila_descer, fila_subir
    
    andar_selecionado = int(andar_selecionado)
    if evento == 'up' and andar_selecionado not in fila_subir:
        fila_subir.append(andar_selecionado)
    elif evento == 'down' and andar_selecionado not in fila_descer:
        fila_descer.append(andar_selecionado)

    fila_descer.sort(reverse=True)
    fila_subir.sort(reverse=True)
    andar_selecionado = ''


def on_key_event(event):
    global andar_selecionado, desligar_elevador
    
    if event.name == 'esc':
        desligar_elevador = True
        return
    
    andar_selecionado = random.randrange(0, 29)
    evento = random.choice(['up', 'down'])
    adicionar_a_fila(evento)
    
    #caracteres_permitidos = [ '1', '2', '3', '4', '5','6', '7', 
    #                         '8', '9', '0', 'up', 'down', 'backspace' ]
    #
    #if event.name not in caracteres_permitidos:
    #    return
    #
    #if event.name not in ['up', 'down', 'backspace']:
    #    andar_selecionado += event.name
    #
    #if not andar_selecionado:
    #    return
    #
    #elif event.name == 'backspace':
    #    andar_selecionado = andar_selecionado[:-1]
    #   
    #elif (event.name in ['up', 'down']) and int(andar_selecionado) in range(0, 29):
    #    adicionar_a_fila(event.name)
           
    
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
        #if andar_selecionado and int(andar_selecionado) in range(0, 29):
        #    print("Andar válido")
        #else:
        #    print("Andar inválido")
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
