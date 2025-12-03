import json
import random as ran
import time

def credits(fitxer):
    with open(fitxer, 'r', encoding='utf-8') as fitxer:
        for linia in fitxer:
            print(linia.strip().center(80)) 
            time.sleep(0.3) 

MITHRIL = f'\033[38;2;136;154;204m'
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

#mirar vida
def check_life(hp):
    if hp <= 0:
        return False
    else:
        return True 
    
#mirar si se pot comprar algo  
def can_buy(m,p):
    r = m-p
    return r

def copiar(fitxer):
    with open(fitxer, 'r', encoding='utf-8') as json_file:
        dades = json.load(json_file)
    return dades

def pegar(dades, fitxer):
    with open(fitxer, 'w', encoding='utf-8') as json_file:
        json.dump(dades, json_file, indent=4)

#Emprar objectes
def emprar(item):
    stats = copiar('stats_player.json')
    inventari = copiar('inventari.json')
    objectes = copiar('objectes.json') 

    if item not in inventari or item not in objectes:
        print("Error: Ítem no vàlid o inexistent.")
        return

    quantitat_actual = inventari[item][0]
    estat_inventari = inventari[item][1]
    propietats = objectes[item]

    estatistica = propietats[2]
    valor = propietats[3]

    if quantitat_actual < 1:
        print(f"No et queden {item} per emprar.")
        return
    
    if estat_inventari != "noEquipable":
        print(f"L'objecte '{item}' és equipable, no consumible. Utilitza la funció 'equipar'.")
        return

    if estatistica in stats:
        stats[estatistica] += valor
        
        inventari[item][0] -= 1

        color = VERD_C if estatistica == 'vida' else BLAU_C
        print(f"{color}Has emprat {item}. {estatistica} ha pujat en {valor}. Ara tens {stats[estatistica]} de {estatistica} max.{RESET}")
        if inventari[item][0] == 0:
            del inventari[item]
            if len(inventari) == 1 and "inventari_buit" in inventari:
                 inventari["inventari_buit"] = True 
    else:
        print(f"Error: L'estadística '{estatistica}' no existeix.")
        return
    print("")
    pegar(inventari, 'inventari.json')
    pegar(stats, 'stats_player.json')

#veure inventari
def see_inventary():
    print("")
    while True: 
        inventari = copiar('inventari.json')
        
        if inventari.get('inventari_buit', True) == True:
            print("El teu inventari està buit.")
            return

        print_inventari = ""
        items_consumibles = {}

        for item, data in inventari.items(): 
            if item != 'inventari_buit' and data[1] == "noEquipable" and data[0] > 0:
                quantitat = data[0]
                print_inventari += f"{item}({quantitat}), " 
                items_consumibles[item] = quantitat

        if not print_inventari:
            print("No tens objectes consumibles a l'inventari.") 
            return

        print("Objectes consumibles:")
        print(f"{CIAN}{print_inventari.rstrip(', ')}{RESET}") 
        print("")
        
        while True:
            op = input("Quin objecte vols emprar? ('s' per sortir) ").strip() 
            print("")
            
            if op == "s":
                print("Has sortit de l'inventari.")
                return 
            
            # Comprovem la cadena de text directament
            if op in items_consumibles: 
                emprar(op) 
                break 
            else:
                print("Objecte no vàlid, equipable o sense unitats. Torna a intentar.")
                print("")

#Equipar armadures i armes
def equipar(op):
    inventari = copiar("inventari.json")
    stats = copiar("stats_player.json")
    objectes = copiar("objectes.json") 

    if op not in inventari or op not in objectes or objectes[op][0] != "Equipable":
        print("Error: Aquest ítem no és equipable o no el tens.")
        return
    nou_slot = objectes[op][1] 
    nova_stat = objectes[op][2] 
    nou_valor = objectes[op][3] 
    
    item_desequipat = None
    for item in list(inventari.keys()):
        if item != "inventari_buit" and inventari.get(item) and inventari[item][1] == "Equipat":
            if item in objectes and objectes[item][1] == nou_slot: 
                item_desequipat = item

                stat_vella = objectes[item][2] 
                valor_vell = objectes[item][3] 
                stats[stat_vella] -= valor_vell
                inventari[item][1] = "Equipable"
                print(f"({item}) S'ha des-equipat correctament (Slot {nou_slot}): -{valor_vell} de {stat_vella}")
                break 
    if nova_stat in stats:
        stats[nova_stat] += nou_valor
        inventari[op][1] = "Equipat"
        print(f"({op}) S'ha equipat correctament (Slot {nou_slot}): +{nou_valor} de {nova_stat}")
    else:
        print(f"Error: L'estadística {nova_stat} no existeix en el jugador.")
    pegar(inventari, 'inventari.json')
    pegar(stats, 'stats_player.json')

def veure_equipables():
    print("")
    while True: 
        inventari = copiar('inventari.json')
        objectes = copiar('objectes.json')
        
        items_equipables = {}
        print_inventari = ""

        for item, data in inventari.items():
            if item != 'inventari_buit' and data[1] in ["Equipable", "Equipat"]:
                if item in objectes:
                    propietats = objectes[item]
                    stat = propietats[2]
                    valor = propietats[3]
                else:
                    continue
                display_estat = "(Equipat)" if data[1] == "Equipat" else "(Desequipat)"
                print_inventari += f"{item} {display_estat} (+{valor} {stat}), "
                items_equipables[item] = True
        if not print_inventari:
            print("No tens objectes equipables a l'inventari.") 
            return None
        print("Objectes equipables:")
        print(print_inventari.rstrip(', ')) 
        print("")
        while True:
            try:
                op = input("Quin objecte vols equipar? ('s' per sortir) ").strip() 
                print("")
                if op == "s":
                    print("Has sortit de l'inventari.")
                    return None 
                if op in items_equipables:
                    equipar(op)
                    break 
                else:
                    print("Objecte no vàlid. Torna a intentar.")
            except:
                print("Error d'entrada. Torna a intentar.")

def restablir_stats(race):
    if race == None:
        stats_base = {
            "vida": 35,
            "atac": 20,
            "armadura": 0,
            "agilitat": 75,
            "monedes": 0,
            "raça": "humà"
        }
    elif race == 1:
        stats_base = {
            "vida": 30,
            "atac": 20,
            "armadura": 0,
            "agilitat": 100,
            "monedes": 0,
            "raça": "elf"
        }
    elif race == 2:
        stats_base = {
            "vida": 35,
            "atac": 20,
            "armadura": 0,
            "agilitat": 75,
            "monedes": 0,
            "raça": "humà"
        }
    elif race == 3:
        stats_base = {
            "vida": 30,
            "atac": 15,
            "armadura": 20,
            "agilitat": 20,
            "monedes": 0,
            "raça": "nan"
        }
    pegar(stats_base, 'stats_player.json')
    rutas_base = {
        "km": 0,
        "ruta": 1,
        "evento": False
    }   
    pegar(rutas_base, 'rutas.json')

def menu_inici(op):
    inventari = copiar("inventari.json")
    partida = copiar("partida.json")
    print("")

    if op == 0:
        print("S'ha carregat la partida correctament.")
    elif op == 1:
        partida["nueva_partida"] = True 
        partida["nom"] = "" 
        partida["event_anell"] = False
        partida["event_plaça"] = False
        partida["event_castell"] = False
        partida["derrota_rei"] = False
        partida["missatge"] = False
        partida["events_ciutat"] = False
        inventari_net = {"inventari_buit": True}
        pegar(inventari_net, "inventari.json")
        pegar(partida, "partida.json")
        
        print("S'ha inicialitzat l'estat del joc. A punt per crear el nou personatge.")
    elif op == 2:
        print("Adéu.")
        exit()

#Veure stats
def veure_stats():
    stats = copiar("stats_player.json")
    print_stats = ""
    for item in stats:
        print_stats += f"{item}: {stats[item]}, "
    print("")
    return f"{GROC}{print_stats}{RESET}"

#Events aleatoris al caminar
def caminar():
    rutas = copiar('rutas.json')
    print(f"Has caminat 1km")
    n = ran.randint(1,11)
    if rutas['ruta'] != 3:
        if n in range(1,9):
            return "batalla"
        elif n in range(9,11):
            return "objecte"
    else:
        print("")
        if rutas['km'] == 10:
            return "drac"
        else:
            time.sleep(1)
            return "res"


#Calcular dany
import random as ran

def calc_dany(stats_p, stats_e, atacant):
    if atacant == "player":
        dany_base = stats_p["atac"] * 0.5
        armadura_objectiu = stats_e["armadura"]
        
        precisio_exit = True
        missatge_error = "L'Enemic esquiva l'atac!" 

    elif atacant == "enemic":        
        probabilitat_encert = stats_e["precisió"] / 100.0 # Ex: 45 (goblin) -> 0.45
        if ran.random() >= probabilitat_encert:
            print(f"{GRIS}L'enemic ha fallat!{RESET}")
            return 0 
        dany_base = stats_e["atac"] * 0.5 
        armadura_objectiu = stats_p["armadura"] 
    rng = ran.uniform(0.9, 1.1)
    dany_ajustat = dany_base * rng
    
    factor_resistencia = 1 - (armadura_objectiu / 200) 
    dany_despres_armadura = dany_ajustat * factor_resistencia
    es_critic = ran.random() < 0.1  # 10% de probabilitat
    if es_critic:
        dany_final = dany_despres_armadura * 2
        print(f"{MAGENTA}Cop Crític!{RESET}")
    else:
        dany_final = dany_despres_armadura
    return max(1, round(dany_final))
#Intentar fugir
def fugir(stats_p,stats_e):
    prob_base = stats_p["agilitat"] / 100
    penalitzacio_atac = stats_e["atac"] * 0.005
    prob_final = prob_base - penalitzacio_atac
    prob_final = max(0.01, min(1.0, prob_final))
    rng = ran.random() 
    if rng < prob_final:
        return True
    else:
        return False

#Batalles aleatories
def batalla(ruta):
    partida = copiar("partida.json")
    enemics = copiar("enemies.json")
    stats = copiar("stats_player.json")
    inventari = copiar("inventari.json")
    rng = ran.randint(1,101)
    if ruta == 1:
        if rng in range(1,11):  
            enemic = "troll"
        elif rng in range(11,56):
            enemic = "goblin"
        else:   
            enemic = "esquelet"
    elif ruta == 2:
        if rng in range(1,51):
            enemic = "fangus mutant"
        elif rng in range(51,86):
            enemic = "llop"
        else:
            enemic = "drac jove"
    elif ruta == 3:
        enemic = "Glaurung"
    if partida["event_castell"] == True and partida['events_ciutat'] == False:
        enemic = "Rei de la Muntanya"
        print(f"El {MAGENTA}{enemic}{RESET} et desafia! ")
    elif enemic == "Glaurung":
        print(f"El Drac {VERMELL}{enemic}{RESET} et desafia! ")
        print("")
        with open('ascii.txt', 'r', encoding='utf-8') as fitxer:
            linies = fitxer.readlines()
            for i in range(107,134):
                print(linies[i], end='')
                time.sleep(0.2)
        print("")
        if "escata" in inventari:
            print(f"{VERD}Glaurung ha perdut 50 de vida per la batalla anterior! {RESET}")
            enemics['Glaurung']['vida'] -= 50
    else:
        print(f"Te trobes contra un {enemic}!")
    enemic_actual = enemics[enemic].copy()

    intentar_fugir = False    
    while True:
        if intentar_fugir == True:
            return "fugit"
        print_stats_e = ""
        while True:
            try:
                print_stats_e = ""
                for stat in enemic_actual:
                    if stat != "experiència":
                        print_stats_e += f"{stat}: {enemic_actual[stat]}, "
                print(f"{VERMELL}{print_stats_e}{RESET}")
                print("")
                print(f"{BLAU}{partida['nom']} --- vida: {stats['vida']}{RESET}")
                if enemic == "Rei de la Muntanya" and partida['derrota_rei'] == True:
                    print(f"Atacar --- Inventari --- {MAGENTA}Python{RESET}")
                else:
                    print("Atacar --- Inventari --- Fugir")
                op = int(input("Que vols fer? (1,2,3) ")) 
                print("")
                inventari = copiar('inventari.json')
                if enemic == "drac jove" and "anell" in inventari and partida["event_anell"] == False:
                    time.sleep(1)
                    print("")
                    print("...")                    
                    time.sleep(2)
                    print("")
                    print("El drac està reaccionant al resplandor del teu anell!")
                    time.sleep(2)
                    print("")
                    print("...")
                    time.sleep(2)
                    print("")
                    print("Sembla que li has caigut bé al drac")
                    time.sleep(2)
                    print("")
                    print("El drac s'ha anat volant.")
                    time.sleep(2)
                    print("")
                    print(f"Has trobat una {MAGENTA}escata de drac{RESET} al terra!")
                    time.sleep(2)
                    obtenir_objecte("escata")
                    partida['event_anell'] = True
                    pegar(partida,'partida.json')
                    return "drac"
                if op == 1:
                    dany_jugador = calc_dany(stats, enemic_actual, 'player')

                    print(f"Ataques al {enemic}.")
                    print(f"{BLAU}L'has ferit i li has llevat {dany_jugador} de vida. {RESET}")

                    nova_vida_enemic = enemic_actual["vida"] - dany_jugador
                    enemic_actual["vida"] = max(0, nova_vida_enemic)

                    if check_life(enemic_actual["vida"]) == False:
                        if enemic == "Glaurung":
                            print("")
                            print("")
                            print(f"{VERMELL}Glaurung: {RESET}Vaja, realment ets més fort del que esperava.")
                            time.sleep(3)
                        return "guanya"
                    dany_enemic = calc_dany(stats, enemic_actual, 'enemic')
                    if dany_enemic > 0:
                        print(f"{VERMELL}El {enemic} t'ha ferit i t'ha llevat {dany_enemic} de vida {RESET}")
                        nova_vida_jugador = stats["vida"] - dany_enemic
                        stats["vida"] = max(0, nova_vida_jugador) 

                    if check_life(stats["vida"]) == False:
                        return "perd"
                    break
                elif op == 2:
                    see_inventary()
                elif op == 3:
                    if enemic == "Glaurung":
                        print("No pots fugir del drac.")
                        break
                    elif partida['derrota_rei'] == True:
                        time.sleep(1)
                        print(f"{MAGENTA}Rei: {RESET}...")
                        print("")
                        time.sleep(1)
                        print(f"{MAGENTA}Rei: {RESET}A què estàs esperant? ")
                        print("")
                        time.sleep(2)
                        with open('ascii.txt', 'r', encoding='utf-8') as fitxer:
                            linies = fitxer.readlines()
                            for i in range(22,29):
                                print(linies[i], end='')
                                time.sleep(1)
                        print("")
                        time.sleep(1)
                        print(f"{MAGENTA}Rei: {RESET}Que està passant?")
                        print("")
                        time.sleep(2)
                        print(f"{MAGENTA}Rei: {RESET}No és possible...")
                        print("")
                        time.sleep(5)
                        print(f"{VERMELL}vida: 0, atac: 0, armadura: 0, precisió: 0,{RESET}")
                        print("")
                        time.sleep(3)
                        print("Has derrotat al Rei de la Muntanya. ")
                        print("")
                        rutas = copiar('rutas.json')
                        rutas['km'] = 0
                        rutas['ruta'] = 3 
                        pegar(rutas, 'rutas.json')
                        return "guanya"
                    else:
                        if enemic == "Rei de la Muntanya":
                            print("No pots fugir del Rei.")
                            break
                        else:
                            intentar_fugir = fugir(stats,enemic_actual)
                            if intentar_fugir == True:
                                print("Has fugit exitosament. ")
                                pegar(stats,'stats_player.json')
                                return "fugit" 
                            elif intentar_fugir == False:
                                print("No has aconseguit fugir. ")
                else:
                    print("")
            except:
                print("")

def obtenir_objecte(ob):
    objectes = copiar('objectes.json')
    inventari = copiar('inventari.json')
    estat_inicial = objectes[ob][0] # Ex: "Equipable"
    if ob in inventari:
        inventari[ob][0] += 1
    else:
        inventari[ob] = [1, estat_inicial]
    inventari["inventari_buit"] = False
    pegar(inventari, 'inventari.json')
    return ob

def objecte_random(ruta):
    objectes = copiar('objectes.json')
    inventari = copiar('inventari.json')
    probabilitat_total = 0
    items_disponibles = {} 

    for item, propietats in objectes.items():
        if propietats[5] == ruta or item == "res": 
            probabilitat = propietats[4]
            probabilitat_total += probabilitat
            items_disponibles[item] = propietats
    
    tirada = ran.randint(1, probabilitat_total)
    
    probabilitat_acumulada = 0
    objecte_obtingut = None

    for item, propietats in items_disponibles.items():
        probabilitat_item = propietats[4]
        probabilitat_acumulada += probabilitat_item
        
        if tirada <= probabilitat_acumulada:
            objecte_obtingut = item
            break
            
    if objecte_obtingut == "res":
        return objecte_obtingut 
    if objecte_obtingut:
        estat_inicial = objectes[objecte_obtingut][0] 
        if objecte_obtingut in inventari:
            inventari[objecte_obtingut][0] += 1
        else:
            inventari[objecte_obtingut] = [1, estat_inicial]
            
        inventari["inventari_buit"] = False
        pegar(inventari, 'inventari.json')
        return objecte_obtingut
    else:
        return ""
def gamble(m):
    rng = ran.randint(1,101)
    if rng in range(1,46):
        return True
    else:
        return False
    
def evento(ruta,km):
    rutas = copiar('rutas.json')
    pegar(rutas, 'rutas.json')
    stats = copiar('stats_player.json')
    mercat = {"anell":[1,10],"capa":[1,10],"sopa":[3,5]}
    if ruta == 1 and km == 10:
        rutas['dins_event'] = True  
        print("¡Has trobat un poble!")
        print("")
        while True:
            while True:
                try:
                    print(f"Al poble hi ha un {MAGENTA}mercat{RESET} i una {MAGENTA}taberna{RESET} / (sortir del poble)")
                    print("                     1            2               3        ")   
                    print("")                 
                    op = int(input(f"On vols anar? (1,2,3): "))
                    print("")
                    if op in range(1,4):
                        break
                except:
                    print("")
            if op == 3:
                rutas['km'] = 0
                rutas['ruta'] = 2
                rutas['dins_event'] = False
                pegar(rutas, 'rutas.json')
                break
            elif op == 2:
                m = stats['monedes']
                while True:
                    print(f"En aquesta taberna pots apostar les teves {GROC}monedes!{RESET} ")
                    print(f"{GROC}Monedes:{RESET} {m}")
                    print("")
                    op = str(input("Vols apostar? (s,n): "))
                    print("")
                    op = op.lower()
                    op = op.replace(" ","") 
                    if op == "s":
                        if m <= 0:
                            print("No tens cap moneda! ")
                        else:
                            aposta = int(input("Quantes monedes vols apostar jugant a les cartes? "))
                            print("")
                            if aposta not in range(1,m+1):
                                print(f"L'aposta ha d'estar entre 1 i {m}")
                            else:
                                resultat = gamble(aposta)
                                if resultat == True:
                                    print(f"¡Has guanyat, {GROC}+{aposta} Monedes{RESET}!")
                                    m += aposta
                                else:
                                    print(f"Has perdut... {VERMELL}-{aposta} Monedes.{RESET}")
                                    m -= aposta
                                stats['monedes'] = m
                    elif op == "n":
                        stats['monedes'] = m
                        pegar(stats,'stats_player.json')
                        break
            elif op == 1:
                m = stats['monedes']
                while True:
                    if len(mercat) <= 0:
                        print("")
                        print(f"{CIAN}No hi ha res més per comprar{RESET}")
                        print("")
                        break
                    print_mercat = ""
                    c_mercat = mercat.copy() #copia de mercat
                    for item in c_mercat:
                        if mercat[item][0] <= 0:
                            mercat.pop(item)
                        else:
                            print_mercat += f"--- {BLANC}{item}({mercat[item][0]}){RESET}, {GROC}preu:{RESET} {mercat[item][1]} "                    
                    print(print_mercat)
                    print("")
                    print(f"{GROC}Monedes: {m}{RESET}")
                    if len(mercat) <= 0:
                        print("")
                        print(f"{CIAN}No hi ha res més per comprar{RESET}")
                        print("")
                        break
                    try:
                        op = str(input(f"Que vols comprar? ('s' per sortir): "))
                        print("")
                        if op == "s":
                            pegar(stats,'stats_player.json')
                            pegar(rutas,'rutas.json')
                            break                        
                        if op in mercat:
                            p = mercat[op][1]
                            r = can_buy(m,p)
                            if r >= 0:
                                print(f"Has comprat ({op}) per ({p}) monedes. ")
                                obtenir_objecte(op)
                                mercat[op][0] -= 1
                                m = r                            
                            else:
                                print(f"{VERMELL}No tens monedes suficients.{RESET}")
                            print("")
                    except:
                        print("")
    elif ruta == 2 and km == 10:
        rutas = copiar('rutas.json')
        rutas['dins_event'] = True  
        pegar(rutas, 'rutas.json')
        armeria = {"arc":[1,15],"puñal":[1,10]}
        password = "drac"
        partida = copiar('partida.json')
        print("")
        time.sleep(1)
        print("Has arribat a una gran ciutat a vora d'una montanya!")
        print("")
        with open('ascii.txt', 'r', encoding='utf-8') as fitxer:
            linies = fitxer.readlines()
            for i in range(30,58):
                print(linies[i], end='')
        while True:
            if partida['events_ciutat'] == True:
                while True:
                    try:
                        print("(sortir de la ciutat)")
                        print("          1          ")
                        print("")
                        op = int(input("Què vols fer? (1): "))
                        if op == 1:
                            rutas['ruta'] = 3
                            rutas['km'] = 1
                            rutas['dins_event'] = False
                            rutas['evento'] = False
                            pegar(rutas,'rutas.json')
                            print("")
                            break
                    except:
                        print("")
                if op == 1:
                    break
            if partida['missatge'] == True:
                print(f"{VERMELL}Has mort.{RESET}")
                print("")
                time.sleep(1)
                print("...")
                print("")
                time.sleep(3)
                print("Encara no has complert la teva missió. ")
                print("")
                time.sleep(3)
                print(f"{CIAN}{partida['nom']}{RESET}: ??? ")
                print("")
                time.sleep(2)
                print("Has arribat a una gran ciutat a vora d'una montanya!")
                print("")
                partida['missatge'] = False
                pegar(partida,'partida.json')
            while True:
                try:
                    print(f"A la ciutat hi ha una {MAGENTA}armeria{RESET}, una {MAGENTA}plaça{RESET} i un gran {MAGENTA}castell{RESET} / (sortir de la ciutat)")
                    print("                         1           2                3               4")
                    print("")
                    op = int(input("On vols anar? (1,2,3): "))
                    if op in range(1,5):
                        print("")
                        break
                except:
                    print("")
            if op == 2:
                print("Hi ha molta gent a la plaça.")
                time.sleep(1)
                if partida['derrota_rei'] == True:
                    print(f"{BLAU_C}Un home vell amb barba et mira i s'acosta a tu...{RESET}")
                    time.sleep(2)
                    print(f"{BLAU_C}Vell:{RESET} Això no és coincidencia, has de seguir endavant.")
                    print("")
                    time.sleep(1)
                    print(f"{GRIS}La gent parla dels seus negocis, però no hi ha res més d'interès aquí.{RESET}")
                if partida['event_plaça'] == False:
                    print(f"{BLAU_C}Un home vell amb barba et mira mentre canta una cançó molt antiga...{RESET}")
                    time.sleep(2)
                    print(f"{VERD_C}'La muntanya ens dóna fred, i el castell un gran poder.")
                    time.sleep(2)
                    print(f"Però la bèstia més temuda, la que escup el foc i mai perduda,")
                    time.sleep(2)
                    print(f"És la resposta al que vols sentir. Per poder seguir...'{RESET}")
                    time.sleep(3)
                    partida['event_plaça'] = True
                    pegar(partida,'partida.json')
                    print(f"{GRIS}La gent parla dels seus negocis, però no hi ha res més d'interès aquí.{RESET}")
                    print("")                
                else:
                    print(f"{GRIS}La gent parla dels seus negocis, però no hi ha res més d'interès aquí.{RESET}")
                print("")
            if op == 1:
                m = stats['monedes']
                while True:
                    if len(armeria) <= 0:
                        print("")
                        print(f"{CIAN}No hi ha res més per comprar{RESET}")
                        print("")
                        break
                    print_mercat = ""
                    c_armeria = armeria.copy() #copia de armeria
                    for item in c_armeria:
                        if armeria[item][0] <= 0:
                            armeria.pop(item)
                        else:
                            print_mercat += f"--- {BLANC}{item}({armeria[item][0]}){RESET}, {GROC}preu:{RESET} {armeria[item][1]} "                    
                    print(print_mercat)
                    print("")
                    print(f"{GROC}Monedes: {m}{RESET}")
                    if len(armeria) <= 0:
                        print("")
                        print(f"{CIAN}No hi ha res més per comprar{RESET}")
                        print("")
                        break
                    try:
                        op = str(input(f"Que vols comprar? ('s' per sortir): "))
                        print("")
                        if op == "s":
                            pegar(stats,'stats_player.json')
                            pegar(rutas,'rutas.json')
                            break                        
                        if op in armeria:
                            p = armeria[op][1]
                            r = can_buy(m,p)
                            if r >= 0:
                                print(f"Has comprat ({op}) per ({p}) monedes. ")
                                obtenir_objecte(op)
                                armeria[op][0] -= 1
                                m = r                            
                            else:
                                print(f"{VERMELL}No tens monedes suficients.{RESET}")
                            print("")
                    except:
                        print("") 
            if op == 4:
                if partida['events_ciutat'] == True:
                    rutas['km'] = 0
                    rutas['ruta'] = 3
                    rutas['dins_event'] = False
                    pegar(rutas, 'rutas.json')
                    break
                else:
                    print("...")
                    print("")
                    time.sleep(1)
                    print("Sent que encara no hauría d'abandonar la ciutat.")
                    print("")
            if op == 3:
                time.sleep(1)
                print("Un guarda s'acosta a tu.")
                time.sleep(1)
                word = str(input("Contrasenya? "))
                word = word.lower()
                word = word.replace(" ","")
                time.sleep(2)
                if word == password:
                    print("")
                    print("...")
                    print("")
                    time.sleep(2)
                    print("Pots passar.")
                    print("")
                    time.sleep(3)
                    print("Avançes pels passadísos del palau mentres observes les pintures i escultures")
                    print("")
                    time.sleep(4)
                    print("Arribes a la sala del tró.")
                    print("")
                    time.sleep(4)
                    print("Et trobes davant del rei, la seva presencia fa que et costi respirar")
                    print("")
                    time.sleep(3)
                    print("...")
                    print("")
                    time.sleep(3)
                    print(f"{MAGENTA}Rei:{RESET} Qui ets tu? No sembles d'aquestes terres.")
                    print("")
                    time.sleep(3)
                    print(f"{MAGENTA}Rei:{RESET} {CIAN}{partida['nom']}{RESET}?")
                    print("")
                    time.sleep(2)
                    print(f"{MAGENTA}Rei:{RESET} Si...")
                    print("")
                    time.sleep(3)
                    print(f"{MAGENTA}Rei:{RESET} Ja he escoltat aquest nom abans...")
                    print("")
                    time.sleep(3)
                    op = str(input(f"{MAGENTA}Rei:{RESET} Digue'm, {CIAN}{partida['nom']}{RESET}, quines són les teves intencions presentant-te al meu palau?: "))
                    print("")
                    print(f"{MAGENTA}Rei:{RESET} En realitat no m'importa.")
                    print("")
                    time.sleep(3)
                    print(f"{VERMELL}Sents com la mirada del rei et gela la sang.{RESET}")
                    print("")
                    time.sleep(2)
                    with open('ascii.txt', 'r', encoding='utf-8') as fitxer:
                        linies = fitxer.readlines()
                        for i in range(1,22):
                            print(linies[i], end='')
                            time.sleep(0.20) 
                    print("")
                    partida['event_castell'] = True
                    pegar(partida,'partida.json')
                    resultat = batalla(2)
                    if resultat == "perd":
                        time.sleep(1)
                        print("")
                        partida['derrota_rei'] = True
                        partida['missatge'] = True
                        pegar(partida,'partida.json')        
                    elif resultat == "guanya":
                        time.sleep(5)
                        print("Tothom t'està mirant")
                        print("")
                        time.sleep(4)
                        print("El silenci és tan gran que pots sentir el teu propi batec")
                        print("")
                        time.sleep(5)
                        print("El consejer del rei s'acosta a tu lentament.")
                        print("")
                        time.sleep(5)
                        print(f"{MAGENTA}Consejer:{RESET} Has aconseguit el què tots creiem impossible")
                        print("")
                        time.sleep(5)
                        print(f"{MAGENTA}Consejer:{RESET} Ens has alliberat de la tirania del Rei")
                        print("")
                        time.sleep(5)
                        print(f"{MAGENTA}Consejer:{RESET} Segons la llei, ara tu has de gobernar la ciutat sota la muntanya.")
                        print("")
                        time.sleep(5)
                        with open('ascii.txt', 'r', encoding='utf-8') as fitxer:
                            linies = fitxer.readlines()
                            for i in range(135,143):
                                print(linies[i], end='')
                                time.sleep(0.20)
                        print(f"{VERD}+100 vida, +100 atac, +30 armadura{RESET}")
                        stats['vida'] += 100
                        stats['atac'] += 100
                        stats['armadura'] += 30
                        print("")
                        time.sleep(2)
                        print(f"{MAGENTA}Consejer:{RESET} Ara, endinsa't a la muntanya per complir la profecia, confiam en tu.")
                        print("")
                        time.sleep(5)
                        rutas = copiar('rutas.json') 
                        rutas['km'] = 0
                        rutas['ruta'] = 3
                        rutas['dins_event'] = False
                        partida['events_ciutat'] = True
                        pegar(rutas, 'rutas.json')
                        pegar(partida,'partida.json')
                        pegar(stats,'stats.json')
                else:
                    print("...")
                    print("")
                    time.sleep(2)
                    print("Fora d'aqui. ")
                    print("")
                    time.sleep(1)
    elif ruta == 3:
        rutas['dins_event'] = True  
        print("Has entrat a la muntanya")
        print("")
        time.sleep(2)
        while True:
            partida = copiar('partida.json')    
            stats = copiar('stats_player.json')
            rutas = copiar('rutas.json')
            inventari = copiar('inventari.json')
            while True:
                try:
                    print("")
                    print(f"{CIAN}{partida['nom']}{RESET} --- vida: {stats['vida']}, Muntanya, km: {rutas['km']}")
                    print("")
                    print("Caminar --- Stats --- Sortir del Joc")
                    op = int(input(f"{partida['nom']}, ets a la ruta {rutas['ruta']}, que vols fer? (1,2,3) "))
                    print("")
                    if op in range(1,4):
                        break
                except:
                    print("")
            if op == 1:
                rutas["km"] += 1
                pegar(rutas, 'rutas.json')
                print(f"Has caminat 1km")
                print("")
                time.sleep(0.5)
                if rutas['km'] == 2:
                    print("Començes a veure antigues escriptures a les parets, no entens res del que expliquen.")
                    print("")
                    time.sleep(3)
                if rutas['km'] == 4:
                    print("L'atmosfera de la muntanya fa que et costi respirar.")
                    print("")
                    time.sleep(3)
                if rutas['km'] == 6:
                    print("Avançes per una sortida i coemençes a escalar la muntanya per fora.")
                    print("")
                    time.sleep(3)
                if rutas['km'] == 8:
                    print("Veus unes escales que semblen infinites, les segueixes.")
                    print("")
                    time.sleep(3)
                if rutas['km'] == 10:
                    time.sleep(3)
                    print("...")
                    print("")
                    time.sleep(3)
                    print("Has arribat al punt més àlgid de la muntanya")
                    print("")
                    time.sleep(3)
                    print("Veus una pila amb un mineral brillant adalt de tot.")
                    print("")
                    time.sleep(3)
                    print("Et sents observat")
                    print("")
                    time.sleep(3)
                    print("Un gran drac es fa veure davant teu.")
                    print("")
                    time.sleep(3)
                    print(f"{VERMELL}???{RESET}: Quin {stats['raça']} s'atreveix a perturbar el meu somni?")
                    print("")
                    time.sleep(3)
                    print(f"{VERMELL}???{RESET}: Mmm")
                    print("")
                    time.sleep(3)
                    print(f"{VERMELL}???{RESET}: Portes la corona del rei, tot i així, no ets el rei que jo conec")
                    print("")
                    time.sleep(3)
                    print(f"{VERMELL}???{RESET}: Sembla que ha arribat el moment que estava esperant")
                    print("")
                    time.sleep(3)
                    print(f"{VERMELL}???{RESET}: Si vols obtenir el {MITHRIL}Mithril{RESET}, hauràs de derrotar-me en batalla")
                    print("")
                    time.sleep(3)
                    if "escata" in inventari:
                        print("Sembla que el vent se remou darrera teu.")
                        print("")
                        time.sleep(3)
                        print("És el jove drac que et va obsequiar amb la seva escata!")
                        print("")
                        time.sleep(3)
                        print("Les dues bèsties començen a lluitar violentament.")
                        print("")
                        time.sleep(3)
                        print("El drac jove ha mort, però ha ferit de gravetat a l'altre.")
                        print("")
                        time.sleep(3)
                    resultat = batalla(3)
                    if resultat == "guanya":
                        print("")
                        print("Avançes al costat del drac caigut.")
                        print("")
                        time.sleep(3)
                        print(f"T'acostes al {MITHRIL}Mithril{RESET}.")
                        print("")
                        time.sleep(3)
                        with open('ascii.txt', 'r', encoding='utf-8') as fitxer:
                            linies = fitxer.readlines()
                            for i in range(145,159):
                                print(linies[i], end='')
                                time.sleep(0.2)
                        print("")
                        time.sleep(3)
                        print("Hi ha una escriptura gravada al mineral.")
                        print("")
                        time.sleep(3)
                        print(f"{BLAU}{partida['nom']}:{RESET} final.json?")
                        final = f"Ho has aconseguit, {partida['nom']}, has alliberat aquest mon de la corrupcio, ara pots descansar."
                        pegar(final,'final.json')
                        time.sleep(3)
                        credits('credits.txt')
                        partida["nueva_partida"] = True 
                        pegar(partida,'partida.json')
                    elif resultat == "perd":
                        partida = False
                        print(f"{VERMELL}Has mort.{RESET}")
                        print("")
                        time.sleep(1)
                        print(f"{VERMELL}Tal vegada en un altre vida serà.{RESET}")
                        print("")
                        time.sleep(5)
                        print(f"{datos['nom']} --- Ruta {rutas['ruta']}, km: {rutas['km']}")
                        datos = {
                            "nueva_partida": True,
                            "nom": "",
                            "lvl": 1,
                            "exp": 0
                        }
                        pegar(datos,'partida.json')
                        break
                else:
                    print("No has trobat res. ")
            elif op == 2:
                print(veure_stats())
            elif op == 3:
                pegar(inventari,'inventari.json')
                pegar(stats,'stats_player.json')
                pegar(rutas,'rutas.json')
                pegar(partida,'partida.json')
                menu_inici(2)