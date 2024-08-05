""" Usa a biblioteca curses para interface 
com o terminal. """


import curses
import threading
import keyboard
import time

# Variáveis -------------------------------------

desligar_elevador = False
fila_subindo = []
fila_descendo = []
direcao_elevador = 'parado'
andar_selecionado = ''
andar_atual = 0

# -----------------------------------------------

def parar_nos_andares():
    global fila_subindo, fila_descendo
    
    #TODO: MARK: Arrumar problema: 
    # elevador subindo, pressiona para baixo, 
    # andar selecionado maior que andar atual,
    # acaba pegando esse andar, não deveria acontecer.
    # ============================================
    # Exemplo: 
    # andar selecionado = 6 
    # andar atual = 4
    # lista_subindo = [8]
    # lista_descendo = [6]
    # ordem que deveria ser: [8, 6]
    # ordem que está saindo agora: [6, 8]
    
    if direcao_elevador == 'subindo':
        if int(andar_atual) in fila_subindo:
            fila_subindo.remove(int(andar_atual))
        elif fila_descendo and int(andar_atual) == fila_descendo[0]:
            fila_descendo.remove(int(andar_atual))
        
    elif direcao_elevador == 'descendo':
        if int(andar_atual) in fila_descendo:
            fila_descendo.remove(int(andar_atual))
        elif fila_subindo and int(andar_atual) == fila_subindo[0]:
            fila_subindo.remove(int(andar_atual))


def movimentar_elevador():
    global andar_atual, direcao_elevador
    
    max_subindo = max(fila_subindo) if fila_subindo else float('-inf')
    max_descendo = max(fila_descendo) if fila_descendo else float('-inf')
    
    if (fila_subindo or fila_descendo) and (int(andar_atual) < max(max_subindo, max_descendo)):
        direcao_elevador = 'subindo'
        andar_atual += 0.1
    
    elif andar_atual > 0:
        direcao_elevador = 'descendo'
        andar_atual -= 0.1
    else:
        direcao_elevador = 'parado'


def adicionar_a_fila(evento):
    global andar_selecionado
    global fila_descendo, fila_subindo
    
    andar_selecionado = int(andar_selecionado)
    if evento == 'up' and andar_selecionado not in fila_subindo:
        fila_subindo.append(andar_selecionado)
    elif evento == 'down' and andar_selecionado not in fila_descendo:
        fila_descendo.append(andar_selecionado)

    fila_descendo.sort(reverse=True)
    fila_subindo.sort(reverse=True)
    andar_selecionado = ''


def on_key_event(event):
    global andar_selecionado, desligar_elevador
    
    if event.name == 'esc':
        desligar_elevador = True
        return
    
    caracteres_permitidos = [ '1', '2', '3', '4', '5','6', '7', 
                             '8', '9', '0', 'up', 'down', 'backspace' ]
    
    if event.name not in caracteres_permitidos:
        return
    
    if event.name not in ['up', 'down', 'backspace']:
        andar_selecionado += event.name
    
    if not andar_selecionado:
        return
    
    elif event.name == 'backspace':
        andar_selecionado = andar_selecionado[:-1]
       
    elif (event.name in ['up', 'down']) and int(andar_selecionado) in range(0, 29):
        adicionar_a_fila(event.name)


def start_key_listener():
    keyboard.on_press(on_key_event)


# Programa -------------------------------------

def elevador(stdscr):    
    curses.curs_set(0)  
    stdscr.nodelay(True)  
    
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Andares: 0 - 28")
        stdscr.addstr(1, 0, f"Andar atual: {int(andar_atual)}")
        stdscr.addstr(2, 0, f"Elevador {direcao_elevador}")
        stdscr.addstr(3, 0, f"Fila subindo: [{', '.join(map(str, fila_subindo))}]")
        stdscr.addstr(4, 0, f"Fila descendo: [{', '.join(map(str, fila_descendo))}]")
        stdscr.addstr(5, 0, f"Andar selecionado: {andar_selecionado}")
        stdscr.addstr(6, 0, "Aperte seta para cima ou seta para baixo para confirmar o andar e a direcao.")
        stdscr.addstr(7, 0, "Aperte 'esc' para encerrar o programa.")
        stdscr.refresh()
        
        if desligar_elevador:
            break
        
        movimentar_elevador()
        parar_nos_andares()
        time.sleep(0.1)

# Inicia o programa

if __name__ == "__main__":
    listener_thread = threading.Thread(target=start_key_listener)
    listener_thread.start()
    
    curses.wrapper(elevador)  # Inicia a interface curses
    
    listener_thread.join()
