import funciones_py as fp

partida = True

#Arxius json
datos = fp.copiar('partida.json')
    #with open(fitxer, 'r') as json_file:
        #dades = json.load(json_file)
    #return dades
rutas = fp.copiar('rutas.json')
inventari = fp.copiar('inventari.json')
stats = fp.copiar('stats_player.json')

NEGRETA = '\033[1m'
RESET = '\033[0m'
VERD_C = '\033[92m'
BLAU_C = '\033[94m'
VERMELL = '\033[31m'
BLAU = '\033[34m'
MAGENTA = '\033[35m'
NEGRE = '\033[30m'
GROC = '\033[33m'
CIAN = '\033[36m'
BLANC = '\033[37m'
VERD = '\033[32m' 
GRIS = '\033[90m' 


while True:
    print("")
    print("")
    print("          ▄▄▄▄███▄▄▄▄    ▄█      ███        ▄█    █▄       ▄████████  ▄█   ▄█       ")
    print("        ▄██▀▀▀███▀▀▀██▄ ███  ▀█████████▄   ███    ███     ███    ███ ███  ███       ")
    print("        ███   ███   ███ ███▌    ▀███▀▀██   ███    ███     ███    ███ ███▌ ███       ")
    print("        ███   ███   ███ ███▌     ███   ▀  ▄███▄▄▄▄███▄▄  ▄███▄▄▄▄██▀ ███▌ ███       ")
    print("        ███   ███   ███ ███▌     ███     ▀▀███▀▀▀▀███▀  ▀▀███▀▀▀▀▀   ███▌ ███       ")
    print("        ███   ███   ███ ███      ███       ███    ███   ▀███████████ ███  ███       ")
    print("        ███   ███   ███ ███      ███       ███    ███     ███    ███ ███  ███▌    ▄ ")
    print("         ▀█   ███   █▀  █▀      ▄████▀     ███    █▀      ███    ███ █▀   █████▄▄██ ")
    print("                                                          ███    ███      ▀         ")
    print("")
    print("                                        ® Manel Roca                               ")
    print("")
    if datos["nueva_partida"] == True:
        print("Nova partida --- Sortir")
        print("     1              2  ")
    else:
        print("Continuar --- Nova partida --- Sortir")
        print("    0              1              2  ")
    print("")
    while True:
        try:
            op = int(input(": "))
            if datos["nueva_partida"] == True:
                if op in [1,2]:
                    break
            elif op in [0,1,2]:
                break
        except:
            print("")
    if op == 0:
        fp.menu_inici(op)
        break 
    elif op == 1:
        fp.menu_inici(op)
        datos = fp.copiar('partida.json') 
        break 
    elif op == 2:
        fp.menu_inici(op)

if datos['nueva_partida'] == True:
    while True:
        nom = str(input("Quin és el teu nom? ")).strip()
        print("")
        if nom:
            break
        print("El nom no pot estar buit.")
    print("--- Selecció de Raça ---")
    print("")
    print("1. Elf (Àgil, menys vida)")
    print("2. Humà (Estàndard, equilibrat)")
    print("3. Nan (Resistent, menys atac i agilitat)")
    print("")
    while True:
        try:
            op_raca = int(input("Tria la teva raça (1, 2, 3): "))
            if op_raca in [1, 2, 3]:
                break
            else:
                print("Opció no vàlida. Tria 1, 2 o 3.")
        except:
            print("Entrada no vàlida. Introdueix un número.")
            
    fp.restablir_stats(op_raca) 
    
    datos['nueva_partida'] = False
    datos['nom'] = nom
    datos['lvl'] = 1
    datos['exp'] = 0
    datos['event_anell'] = False

    fp.pegar(datos, 'partida.json')
    
    stats = fp.copiar('stats_player.json') 
    print(f"Personatge creat: {datos['nom']} ({stats['raça']}), nivell: {datos['lvl']}, vida: {stats['vida']}")

#Continuar partida

while partida == True:
    datos = fp.copiar('partida.json')
    inventari = fp.copiar('inventari.json')
    stats = fp.copiar('stats_player.json')
    rutas = fp.copiar('rutas.json')
    if rutas['ruta'] == 3:
        while True:
            try:
                print("")
                print(f"{CIAN}{datos['nom']}{RESET} --- vida: {stats['vida']}, Muntanya, km: {rutas['km']}")
                print("")
                print("Caminar --- Stats --- Sortir del Joc")
                op = int(input(f"{datos['nom']}, ets a la ruta {rutas['ruta']}, que vols fer? (1,2,3) "))
                print("")
                if op in range(1,4):
                    break
            except:
                print("")
        if op == 1:
            fp.evento(3,0)   
        elif op == 2:
            print(fp.veure_stats())
        elif op == 3:
            fp.pegar(inventari,'inventari.json')
            fp.pegar(stats,'stats_player.json')
            fp.pegar(rutas,'rutas.json')
            fp.pegar(datos,'partida.json')
            fp.menu_inici(2)
    else:
        while True:
            try:
                print("")
                print(f"{CIAN}{datos['nom']}{RESET} --- vida: {stats['vida']}, ruta: {rutas['ruta']}, km: {rutas['km']}")
                print("")
                print("Caminar --- inventari --- Equipar --- Stats --- Sortir del Joc")
                op = int(input(f"{datos['nom']}, ets a la ruta {rutas['ruta']}, que vols fer? (1,2,3,4,5) "))
                print("")
                if op in range(1,6):
                    break
            except:
                print("")
        if op == 1:
            fp.evento(rutas['ruta'],rutas['km'])
            event = fp.caminar()
            rutas = fp.copiar('rutas.json')
            if event == "batalla":
                resultat = fp.batalla(rutas['ruta'])
                print("")
                if resultat == "perd":
                    partida = False
                    print(f"{VERMELL}Has mort.{RESET}")
                    print("")
                    print(f"{datos['nom']} --- Ruta {rutas['ruta']}, km: {rutas['km']}")
                    datos = {
                        "nueva_partida": True,
                        "nom": "",
                        "lvl": 1,
                        "exp": 0
                    }
                    fp.pegar(datos,'partida.json')
                    break
                elif resultat == "fugit":
                    if stats['monedes'] >= 3:
                        print(f"Se t'han caigut 3 {GROC}monedes{RESET} mentres fugies...")
                        stats['monedes'] -= 3
                        fp.pegar(stats,'stats_player.json')
                        rutas['km'] += 1
                        fp.pegar(rutas,'rutas.json')
                    continue 
                elif resultat == "guanya":
                    objecte_rng = fp.objecte_random(rutas['ruta'])
                    if objecte_rng != "res":
                        print(f"Has trobat un {MAGENTA}objecte!{RESET}")
                        print(f"+1 {MAGENTA}{objecte_rng}{RESET}")
                    else:
                        print(f"Has trobat 5 {GROC}monedes!{RESET}")
                        stats['monedes'] += 5
                        fp.pegar(stats, 'stats_player.json')
                    rutas['km'] += 1
                    fp.pegar(rutas,'rutas.json')
                    continue
                elif resultat == "drac":
                    continue
            elif event == "batalla" and rutas['ruta'] == 3:
                resultat = fp.batalla(rutas['ruta'])
                print("")
        elif op == 2:
            fp.see_inventary()
        elif op == 3:
            fp.veure_equipables()
        elif op == 4:
            print(fp.veure_stats())
        elif op == 5:
            fp.pegar(inventari,'inventari.json')
            fp.pegar(stats,'stats_player.json')
            fp.pegar(rutas,'rutas.json')
            fp.pegar(datos,'partida.json')
            fp.menu_inici(2)