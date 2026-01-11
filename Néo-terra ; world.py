import random
import time
import sys
import json
import os

def rpg_futuriste():
    # --- Lore ---
    def afficher_lore():
        print("""
        ===== NÉO-TERRA 2187 =====
        En 2187, la Terre est déchirée entre les Humains Libres et les Synthétiques.
        Vous incarnez un aventurier dans ce monde post-apocalyptique.
        Votre mission : découvrir la vérité derrière la guerre et choisir votre destin.
        """)

    # --- Rôles ---
    def choisir_rôle():
        while True:
            print("\n===== CHOISISSEZ VOTRE RÔLE =====")
            print("1. Mercenaire (Équilibré, bon en combat)")
            print("2. Hacker (Faible en PV, mais peut désactiver les ennemis)")
            print("3. Scientifique (Peut soigner et fabriquer des implants)")
            print("4. Soldat Synthétique (PV élevés, mais vulnérable aux hackers)")
            rôle = input("Votre choix (1/2/3/4) : ").strip()
            rôles = {
                "1": {"nom": "Mercenaire", "pv": 120, "attaque": 20, "defense": 15, "compétences": ["Coup de poing énergétique", "Tir de précision"], "dialogue": "Je suis un loup solitaire. Payez-moi et je ferai le travail."},
                "2": {"nom": "Hacker", "pv": 80, "attaque": 10, "defense": 10, "compétences": ["Désactiver ennemi", "Piratage de défense"], "dialogue": "Les machines ont des failles. Moi aussi, mais je les exploite mieux."},
                "3": {"nom": "Scientifique", "pv": 90, "attaque": 12, "defense": 12, "compétences": ["Fabriquer implant", "Soin d'urgence"], "dialogue": "La science est la clé. Même dans ce monde de brutes."},
                "4": {"nom": "Soldat Synthétique", "pv": 150, "attaque": 18, "defense": 20, "compétences": ["Bouclier énergétique", "Surpuissance"], "dialogue": "Je suis une machine de guerre. Rien de plus, rien de moins."}
            }
            if rôle in rôles:
                return rôles[rôle]
            else:
                print("Choix invalide. Veuillez entrer 1, 2, 3 ou 4.")

    # --- Classes ---
    class Personnage:
        def __init__(self, rôle):
            self.nom = rôle["nom"]
            self.pv = rôle["pv"]
            self.attaque = rôle["attaque"]
            self.defense = rôle["defense"]
            self.compétences = rôle["compétences"]
            self.dialogue = rôle["dialogue"]
            self.inventaire = ["Potion de soin"]
            self.niveau = 1
            self.exp = 0
            self.fin_jeu = False

        def attaquer(self, ennemi):
            try:
                dégats = max(0, self.attaque - ennemi.defense // 2)
                ennemi.pv -= dégats
                print(f"{self.nom} inflige {dégats} dégâts à {ennemi.nom} !")
            except AttributeError:
                print("Erreur : L'ennemi n'a pas d'attribut 'defense' ou 'pv'.")

        def utiliser_compétence(self, compétence, ennemi=None):
            compétence = compétence.strip()
            try:
                if compétence == "Coup de poing énergétique" and ennemi:
                    dégats = self.attaque * 1.5
                    ennemi.pv -= dégats
                    print(f"{self.nom} utilise {compétence} et inflige {dégats} dégâts !")
                elif compétence == "Tir de précision" and ennemi:
                    dégats = self.attaque * 2
                    ennemi.pv -= dégats
                    print(f"{self.nom} utilise {compétence} et inflige {dégats} dégâts !")
                elif compétence == "Désactiver ennemi" and ennemi:
                    ennemi.pv = 0
                    print(f"{self.nom} désactive {ennemi.nom} !")
                elif compétence == "Piratage de défense" and ennemi:
                    ennemi.defense = max(0, ennemi.defense - 10)
                    print(f"{self.nom} pirate les défenses de {ennemi.nom} (-10 défense) !")
                elif compétence == "Fabriquer implant":
                    self.inventaire.append("Implant de soin")
                    print(f"{self.nom} fabrique un Implant de soin !")
                elif compétence == "Soin d'urgence":
                    self.pv = min(self.pv + 30, 150)
                    print(f"{self.nom} se soigne ! +30 PV.")
                elif compétence == "Bouclier énergétique":
                    self.defense += 15
                    print(f"{self.nom} active un Bouclier énergétique (+15 défense) !")
                elif compétence == "Surpuissance":
                    self.attaque += 20
                    print(f"{self.nom} active la Surpuissance (+20 attaque) !")
                else:
                    print(f"Compétence '{compétence}' inconnue ou ennemi manquant.")
            except Exception as e:
                print(f"Erreur lors de l'utilisation de la compétence : {e}")

        def ajouter_objet(self, objet):
            self.inventaire.append(objet)
            print(f"{objet} ajouté à l'inventaire.")

    class Ennemi:
        def __init__(self, nom, pv, attaque, defense):
            self.nom = nom
            self.pv = pv
            self.attaque = attaque
            self.defense = defense

        def attaquer(self, joueur):
            try:
                dégats = max(0, self.attaque - joueur.defense // 2)
                joueur.pv -= dégats
                print(f"{self.nom} inflige {dégats} dégâts à {joueur.nom} !")
            except AttributeError:
                print("Erreur : Le joueur n'a pas d'attribut 'defense' ou 'pv'.")

    class MédecinRebelle:
        def __init__(self):
            self.nom = "Dr. Lina Kova"
            self.pv = 60
            self.attaque = 12
            self.defense = 18
            self.dialogue_aide = [
                f"\n{self.nom} : 'Je suis là pour t'aider. Ce fou doit être arrêté.'",
                f"{self.nom} : 'Prends ça, ça pourrait te sauver la vie.' *vous donne une Potion de soin*"
            ]

        def soigner(self, joueur):
            try:
                joueur.pv = min(joueur.pv + 40, 150)
                print(f"\n{self.nom} vous soigne ! +40 PV.")
            except AttributeError:
                print("Erreur : Le joueur n'a pas d'attribut 'pv'.")

        def attaquer(self, ennemi):
            try:
                dégats = max(0, self.attaque - ennemi.defense // 2)
                ennemi.pv -= dégats
                print(f"{self.nom} inflige {dégats} dégâts à {ennemi.nom} !")
            except AttributeError:
                print("Erreur : L'ennemi n'a pas d'attribut 'defense' ou 'pv'.")

    class ChefSynthétique:
        def __init__(self):
            self.nom = "Commandant X-47"
            self.pv = 200
            self.attaque = 30
            self.defense = 25
            self.dialogue_intro = [
                f"\n{self.nom} : 'Je suis l'aboutissement de l'évolution synthétique. Vous n'avez aucune chance.'",
                f"{self.nom} : 'Votre résistance est inutile. La Terre appartient désormais aux machines.'"
            ]
            self.dialogue_mort = [
                f"\n{self.nom} : 'Ceci... n'était pas prévu...' *s'effondre*",
                f"Le corps du {self.nom} s'écroule, déclenchant une explosion de données."
            ]

        def attaquer(self, joueur):
            try:
                choix = random.choice(["Attaque laser", "Bouclier temporel", "Appel de renforts"])
                if choix == "Attaque laser":
                    dégats = 35
                    joueur.pv -= dégats
                    print(f"\n{self.nom} utilise {choix} ! {joueur.nom} subit {dégats} dégâts !")
                elif choix == "Bouclier temporel":
                    self.defense += 15
                    print(f"\n{self.nom} utilise {choix} ! (+15 défense)")
                else:  # Appel de renforts
                    dégats = 20
                    joueur.pv -= dégats
                    print(f"\n{self.nom} appelle des renforts ! {joueur.nom} subit {dégats} dégâts !")
            except Exception as e:
                print(f"Erreur lors de l'attaque du Commandant X-47 : {e}")

        def animation_mort(self):
            for ligne in self.dialogue_mort:
                for char in ligne:
                    sys.stdout.write(char)
                    sys.stdout.flush()
                    time.sleep(0.03)
                time.sleep(1)

    class Quête:
        def __init__(self, titre, description, récompense):
            self.titre = titre
            self.description = description
            self.récompense = récompense
            self.terminée = False

        def compléter(self):
            self.terminée = True
            print(f"Quête '{self.titre}' terminée ! Récompense : {self.récompense}")

    class QuêteClinique:
        def __init__(self):
            self.titre = "Infiltration de la Clinique du Chirurgien Fou"
            self.description = "Infiltrez la clinique abandonnée du Dr. Elias Voss pour récupérer des données sur ses expériences."
            self.récompense = "Données de recherche (déverrouille une compétence secrète)"
            self.étapes = [
                "Trouver l'entrée de la clinique (cachée dans les égouts de Neo-Paris).",
                "Éviter les pièges et les patients mutés.",
                "Affronter le Chirurgien Fou et récupérer ses notes."
            ]
            self.terminée = False
            self.en_cours = False

        def démarrer(self):
            self.en_cours = True
            print(f"\n===== QUÊTE : {self.titre} =====")
            print(f"Description : {self.description}")
            print("Étapes :")
            for i, étape in enumerate(self.étapes, 1):
                print(f"  {i}. {étape}")
            print(f"Récompense : {self.récompense}\n")

        def compléter_étape(self, numéro):
            if numéro <= len(self.étapes):
                print(f"\nÉtape '{self.étapes[numéro-1]}' terminée !")
                if numéro == len(self.étapes):
                    self.terminée = True
                    print(f"Quête '{self.titre}' terminée ! Récompense : {self.récompense}")
            else:
                print("Numéro d'étape invalide.")

    class QuêteFinale:
        def __init__(self):
            self.titre = "Affrontement Final"
            self.description = "Affrontez le Commandant X-47 pour décider du sort de l'humanité."
            self.récompense = "Fin du jeu"
            self.terminée = False

        def démarrer(self):
            print(f"\n===== QUÊTE FINALE : {self.titre} =====")
            print(f"Description : {self.description}")

        def compléter(self, choix_final):
            self.terminée = True
            if choix_final == "détruire":
                print("""
                Vous activez le virus informatique qui détruit le Commandant X-47 et désactive tous les Synthétiques.
                Les Humains Libres reprennent le contrôle de la Terre, mais au prix d'un retour en arrière technologique.
                === FIN : LA LIBERTÉ RETROUVÉE ===
                """)
            elif choix_final == "fusion":
                print("""
                Vous choisissez de fusionner les consciences humaines et synthétiques.
                Une nouvelle ère de paix et de collaboration commence, créant une civilisation hybride.
                === FIN : L'HARMONIE TROUVÉE ===
                """)
            else:
                print("""
                Vous vous alliez avec les Synthétiques pour dominer les Humains Libres.
                La Terre devient un monde froid et mécanique, où les émotions humaines sont réprimées.
                === FIN : L'ÈRE DES MACHINES ===
                """)

    # --- Carte ---
    carte = {
        "Neo-Paris": {
            "description": "Une ville contrôlée par les Synthétiques. Des drones patrouillent les rues.",
            "ennemis": [("Drones Sentinelles", 40, 15, 10), ("Gardiens Synthétiques", 60, 20, 15)]
        },
        "Base Rebelle": {
            "description": "Un repaire humain caché sous terre. On y trouve des alliés et des soins.",
            "ennemis": []
        },
        "Usine Prométhée": {
            "description": "Une usine abandonnée où un projet secret est en cours...",
            "ennemis": [("Robots Ouvriers", 50, 18, 12), ("IA de Sécurité", 80, 25, 20)]
        },
        "Tour de Contrôle": {
            "description": "Le cœur du réseau synthétique. Le Commandant X-47 y réside.",
            "ennemis": []
        }
    }

    # --- Animations ---
    def animation_combat(joueur, ennemi):
        try:
            print(f"\n⚔️  {joueur.nom} vs {ennemi.nom}  ⚔️")
            if hasattr(ennemi, 'dialogue_intro'):
                for ligne in ennemi.dialogue_intro:
                    for char in ligne:
                        sys.stdout.write(char)
                        sys.stdout.flush()
                        time.sleep(0.03)
                    time.sleep(1)
        except Exception as e:
            print(f"Erreur lors de l'animation de combat : {e}")

    def animation_attaque(attaquant, défenseur, compétence=None):
        try:
            if compétence:
                print(f"\n{attaquant.nom} prépare {compétence}...")
                time.sleep(1)
            else:
                print(f"\n{attaquant.nom} attaque !")
            for _ in range(3):
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(0.5)
            print(" BOOM !")
            time.sleep(0.5)
        except Exception as e:
            print(f"Erreur lors de l'animation d'attaque : {e}")

    # --- Combat ---
    def combat(joueur, ennemi):
        try:
            print(f"\nCombat contre {ennemi.nom} !")
            while joueur.pv > 0 and ennemi.pv > 0:
                print(f"\n{joueur.nom} : {joueur.pv} PV | {ennemi.nom} : {ennemi.pv} PV")
                print("1. Attaquer")
                print("2. Utiliser une compétence")
                print("3. Utiliser un objet")
                choix = input("Que faire ? ").strip()
                if not choix:
                    print("Veuillez entrer un choix valide.")
                    continue
                if choix == "1":
                    joueur.attaquer(ennemi)
                elif choix == "2":
                    print("Compétences disponibles :")
                    for i, compétence in enumerate(joueur.compétences, 1):
                        print(f"{i}. {compétence}")
                    choix_compétence = input("Quelle compétence utiliser ? (entrez le numéro) ").strip()
                    if choix_compétence.isdigit() and 1 <= int(choix_compétence) <= len(joueur.compétences):
                        compétence = joueur.compétences[int(choix_compétence) - 1]
                        joueur.utiliser_compétence(compétence, ennemi)
                    else:
                        print("Choix invalide. Veuillez entrer un numéro valide.")
                elif choix == "3":
                    if joueur.inventaire:
                        print("Inventaire :", ", ".join(joueur.inventaire))
                        objet = input("Quel objet utiliser ? ").strip()
                        if objet in joueur.inventaire:
                            if objet == "Potion de soin":
                                joueur.pv += 30
                                print(f"{joueur.nom} récupère 30 PV !")
                            joueur.inventaire.remove(objet)
                        else:
                            print("Objet introuvable.")
                    else:
                        print("Inventaire vide.")
                else:
                    print("Choix invalide.")
                if ennemi.pv <= 0:
                    print(f"{ennemi.nom} est vaincu !")
                    objet_trouvé = random.choice(["Potion de soin", "Crédits", "Données de recherche"])
                    joueur.ajouter_objet(objet_trouvé)
                    joueur.exp += 20
                    print(f"{joueur.nom} gagne 20 points d'expérience !")
                    break
                ennemi.attaquer(joueur)
                if joueur.pv <= 0:
                    print(f"{joueur.nom} est vaincu...")
                    return False
            return True
        except Exception as e:
            print(f"Erreur lors du combat : {e}")
            return False

    # --- Système de Craft ---
    def craft_implants(joueur):
        try:
            if "Données de recherche" in joueur.inventaire:
                print("\n===== CRAFT D'IMPLANT =====")
                print("1. Implant Offensif (+10 Attaque)")
                print("2. Implant Défensif (+10 Défense)")
                print("3. Implant de Soin (Récupère 20 PV/tour pendant 3 tours)")
                choix = input("Que voulez-vous fabriquer ? (1/2/3) ").strip()
                if choix in ["1", "2", "3"]:
                    if choix == "1":
                        joueur.attaque += 10
                        joueur.inventaire.remove("Données de recherche")
                        print("Implant Offensif installé ! +10 Attaque.")
                    elif choix == "2":
                        joueur.defense += 10
                        joueur.inventaire.remove("Données de recherche")
                        print("Implant Défensif installé ! +10 Défense.")
                    elif choix == "3":
                        joueur.inventaire.append("Implant de Soin")
                        joueur.inventaire.remove("Données de recherche")
                        print("Implant de Soin fabriqué ! Utilisez-le pendant le combat.")
                else:
                    print("Choix invalide.")
            else:
                print("Il vous faut des 'Données de recherche' pour crafter.")
        except Exception as e:
            print(f"Erreur lors du craft : {e}")

    # --- Quête de la Clinique ---
    def infiltrer_clinique(joueur):
        try:
            quête = QuêteClinique()
            quête.démarrer()
            input("\nAppuyez sur Entrée pour commencer l'infiltration...")
            print("\nVous explorez les égouts sombres de Neo-Paris...")
            time.sleep(2)
            print("Vous trouvez une porte rouillée menant à la clinique.")
            quête.compléter_étape(1)
            médecin = MédecinRebelle()
            for ligne in médecin.dialogue_aide:
                for char in ligne:
                    sys.stdout.write(char)
                    sys.stdout.flush()
                    time.sleep(0.03)
            médecin.soigner(joueur)
            joueur.ajouter_objet("Potion de soin")
            chirugien = ChirurgienFou()
            animation_combat(joueur, chirugien)
            effet_saignement = 0
            while joueur.pv > 0 and chirugien.pv > 0:
                print(f"\n{joueur.nom} : {joueur.pv} PV | {chirugien.nom} : {chirugien.pv} PV")
                print("1. Attaquer")
                print("2. Utiliser une compétence")
                print("3. Utiliser un objet")
                print("4. Demander de l'aide au Médecin Rebelle")
                choix = input("Que faire ? ").strip()
                if not choix:
                    print("Veuillez entrer un choix valide.")
                    continue
                if choix == "1":
                    animation_attaque(joueur, chirugien)
                    dégats = max(0, joueur.attaque - chirugien.defense // 2)
                    chirugien.pv -= dégats
                    print(f"{joueur.nom} inflige {dégats} dégâts à {chirugien.nom} !")
                elif choix == "2":
                    print("Compétences disponibles :")
                    for i, compétence in enumerate(joueur.compétences, 1):
                        print(f"{i}. {compétence}")
                    choix_compétence = input("Quelle compétence utiliser ? (entrez le numéro) ").strip()
                    if choix_compétence.isdigit() and 1 <= int(choix_compétence) <= len(joueur.compétences):
                        compétence = joueur.compétences[int(choix_compétence) - 1]
                        animation_attaque(joueur, chirugien, compétence)
                        joueur.utiliser_compétence(compétence, chirugien)
                    else:
                        print("Choix invalide. Veuillez entrer un numéro valide.")
                elif choix == "3":
                    if joueur.inventaire:
                        print("Inventaire :", ", ".join(joueur.inventaire))
                        objet = input("Quel objet utiliser ? ").strip()
                        if objet in joueur.inventaire:
                            if objet == "Potion de soin":
                                joueur.pv += 30
                                print(f"{joueur.nom} récupère 30 PV !")
                            joueur.inventaire.remove(objet)
                        else:
                            print("Objet introuvable.")
                    else:
                        print("Inventaire vide.")
                elif choix == "4":
                    médecin.attaquer(chirugien)
                    médecin.soigner(joueur)
                else:
                    print("Choix invalide.")
                if chirugien.pv <= 0:
                    print("\nLe Chirurgien Fou est à terre, agonisant.")
                    while True:
                        choix_moral = input("Voulez-vous l'achever ou l'épargner ? (achever/épargner) ").strip().lower()
                        if choix_moral in ["achever", "épargner"]:
                            break
                        print("Veuillez entrer 'achever' ou 'épargner'.")
                    if choix_moral == "achever":
                        print(f"\n{joueur.nom} achève le Chirurgien Fou sans pitié.")
                        joueur.ajouter_objet("Clé USB Cryptée")
                        print("Vous récupérez une Clé USB Cryptée (récompense sombre).")
                    else:
                        print(f"\n{joueur.nom} épargne le Chirurgien Fou.")
                        joueur.ajouter_objet("Données de recherche")
                        print("Le Chirurgien Fou vous donne ses données par gratitude.")
                    quête.compléter_étape(3)
                    break
                effet = chirugien.attaquer(joueur)
                if effet == "saignement":
                    joueur.pv -= 10
                    print(f"{joueur.nom} saigne et perd 10 PV !")
                if joueur.pv <= 0:
                    print(f"\n{joueur.nom} est vaincu...")
                    joueur.fin_jeu = True
                    return
            carte["Tour de Contrôle"] = {
                "description": "Le cœur du réseau synthétique. Le Commandant X-47 y réside.",
                "ennemis": []
            }
        except Exception as e:
            print(f"Erreur lors de l'infiltration de la clinique : {e}")

    # --- Quête Finale ---
    def quête_finale(joueur):
        quête = QuêteFinale()
        quête.démarrer()
        input("\nAppuyez sur Entrée pour affronter le Commandant X-47...")
        commandant = ChefSynthétique()
        animation_combat(joueur, commandant)
        while joueur.pv > 0 and commandant.pv > 0:
            print(f"\n{joueur.nom} : {joueur.pv} PV | {commandant.nom} : {commandant.pv} PV")
            print("1. Attaquer")
            print("2. Utiliser une compétence")
            print("3. Utiliser un objet")
            choix = input("Que faire ? ").strip()
            if not choix:
                print("Veuillez entrer un choix valide.")
                continue
            if choix == "1":
                joueur.attaquer(commandant)
            elif choix == "2":
                print("Compétences disponibles :")
                for i, compétence in enumerate(joueur.compétences, 1):
                    print(f"{i}. {compétence}")
                choix_compétence = input("Quelle compétence utiliser ? (entrez le numéro) ").strip()
                if choix_compétence.isdigit() and 1 <= int(choix_compétence) <= len(joueur.compétences):
                    compétence = joueur.compétences[int(choix_compétence) - 1]
                    joueur.utiliser_compétence(compétence, commandant)
                else:
                    print("Choix invalide. Veuillez entrer un numéro valide.")
            elif choix == "3":
                if joueur.inventaire:
                    print("Inventaire :", ", ".join(joueur.inventaire))
                    objet = input("Quel objet utiliser ? ").strip()
                    if objet in joueur.inventaire:
                        if objet == "Potion de soin":
                            joueur.pv += 30
                            print(f"{joueur.nom} récupère 30 PV !")
                        joueur.inventaire.remove(objet)
                    else:
                        print("Objet introuvable.")
                else:
                    print("Inventaire vide.")
            else:
                print("Choix invalide.")
            if commandant.pv <= 0:
                print(f"\n{commandant.nom} est vaincu !")
                print("\nVous avez vaincu le Commandant X-47. Le sort de l'humanité est entre vos mains.")
                while True:
                    choix_final = input("Que faire ? (détruire/fusion/dominer) ").strip().lower()
                    if choix_final in ["détruire", "fusion", "dominer"]:
                        break
                    print("Veuillez entrer 'détruire', 'fusion' ou 'dominer'.")
                quête.compléter(choix_final)
                joueur.fin_jeu = True
                return
            commandant.attaquer(joueur)
            if joueur.pv <= 0:
                print(f"\n{joueur.nom} est vaincu...")
                joueur.fin_jeu = True
                print("""
                === FIN : LA DÉFAITE ===
                Vous avez échoué à arrêter le Commandant X-47.
                Les Synthétiques prennent le contrôle total de la Terre.
                """)
                return

    # --- Sauvegarde ---
    def sauvegarder(joueur, quêtes):
        try:
            sauvegarde = {
                "joueur": {
                    "nom": joueur.nom,
                    "pv": joueur.pv,
                    "attaque": joueur.attaque,
                    "defense": joueur.defense,
                    "compétences": joueur.compétences,
                    "inventaire": joueur.inventaire,
                    "niveau": joueur.niveau,
                    "exp": joueur.exp,
                    "fin_jeu": joueur.fin_jeu
                },
                "quêtes": [{"titre": q.titre, "terminée": q.terminée} for q in quêtes]
            }
            with open("sauvegarde.txt", "w") as f:
                json.dump(sauvegarde, f)
            print("Progression sauvegardée !")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")

    def charger():
        try:
            if os.path.exists("sauvegarde.txt"):
                with open("sauvegarde.txt", "r") as f:
                    sauvegarde = json.load(f)
                rôle = {
                    "nom": sauvegarde["joueur"]["nom"],
                    "pv": sauvegarde["joueur"]["pv"],
                    "attaque": sauvegarde["joueur"]["attaque"],
                    "defense": sauvegarde["joueur"]["defense"],
                    "compétences": sauvegarde["joueur"]["compétences"],
                    "dialogue": "Rechargé et prêt à l'action."
                }
                joueur = Personnage(rôle)
                joueur.inventaire = sauvegarde["joueur"]["inventaire"]
                joueur.niveau = sauvegarde["joueur"]["niveau"]
                joueur.exp = sauvegarde["joueur"]["exp"]
                joueur.fin_jeu = sauvegarde["joueur"]["fin_jeu"]
                quêtes = [Quête(q["titre"], "", "") for q in sauvegarde["quêtes"]]
                for i, q in enumerate(quêtes):
                    q.terminée = sauvegarde["quêtes"][i]["terminée"]
                print("Progression chargée !")
                return joueur, quêtes
            else:
                print("Aucune sauvegarde trouvée.")
                return None, None
        except Exception as e:
            print(f"Erreur lors du chargement : {e}")
            return None, None

    # --- Gestion des Lieux et Quêtes ---
    def afficher_carte_et_missions(joueur, quêtes, carte):
        print("\n===== CARTE =====")
        for i, lieu in enumerate(carte.keys(), 1):
            print(f"{i}. {lieu} - {carte[lieu]['description']}")
        print("\n===== MISSIONS EN COURS =====")
        for i, quête in enumerate(quêtes, 1):
            statut = "✓" if quête.terminée else "✗"
            print(f"{i}. [{statut}] {quête.titre} : {quête.description}")

    def choisir_lieu(joueur, quêtes, carte):
        while True:
            afficher_carte_et_missions(joueur, quêtes, carte)
            choix = input("\nOù voulez-vous aller ? (Entrez le numéro) : ").strip()
            if not choix:
                print("Veuillez entrer un numéro valide.")
                continue
            try:
                choix = int(choix)
                lieu_nom = list(carte.keys())[choix - 1]
                return lieu_nom
            except (ValueError, IndexError):
                print("Choix invalide. Veuillez entrer un numéro valide.")

    def gérer_quêtes(joueur, quêtes, lieu_choisi):
        if lieu_choisi == "Base Rebelle":
            if not quêtes[1].terminée:
                print(f"\nVous arrivez à la {lieu_choisi}.")
                print("Un rebelle vous approche : 'Aidez-nous à reprendre l'usine, et nous vous récompenserons !'")
                while True:
                    choix = input("Accepter la mission ? (o/n) : ").strip().lower()
                    if choix in ["o", "n"]:
                        break
                    print("Veuillez entrer 'o' ou 'n'.")
                if choix == "o":
                    print("Mission acceptée ! Rendez-vous à l'Usine Prométhée.")
                    quêtes[1].description = "Rendez-vous à l'Usine Prométhée pour aider les rebelles."
                else:
                    print("Vous déclinez la mission.")
            else:
                print(f"\nVous êtes déjà venu à la {lieu_choisi}. Les rebelles vous saluent.")

        elif lieu_choisi == "Usine Prométhée":
            if not quêtes[1].terminée and "Rendez-vous à l'Usine Prométhée" in quêtes[1].description:
                print(f"\nVous arrivez à l'{lieu_choisi} avec les rebelles.")
                print("Un combat intense commence contre les robots gardiens !")
                ennemi = Ennemi("Robot Gardien", 70, 20, 15)
                if combat(joueur, ennemi):
                    quêtes[1].compléter()
                    joueur.ajouter_objet("Arme rare")
                    print("Mission accomplie ! Vous recevez une Arme rare.")
            else:
                print(f"\nVous explorez l'{lieu_choisi} mais ne trouvez rien d'intéressant.")

        elif lieu_choisi == "Neo-Paris":
            if not quêtes[0].terminée:
                print(f"\nVous entrez dans {lieu_choisi}, une ville sous contrôle synthétique.")
                print("Votre mission : Trouver des données dans la base centrale.")
                ennemi = Ennemi("Drone Sentinelle", 50, 15, 10)
                if combat(joueur, ennemi):
                    quêtes[0].compléter()
                    joueur.ajouter_objet("Données volées")
                    print("Mission accomplie ! Vous récupérez des Données volées.")
            else:
                print(f"\n{lieu_choisi} est déjà explorée.")

        elif lieu_choisi == "Clinique Abandonnée":
            infiltrer_clinique(joueur)

        elif lieu_choisi == "Tour de Contrôle":
            quête_finale(joueur)

    # --- Boucle principale ---
    afficher_lore()
    joueur, quêtes = charger()
    if joueur is None:
        rôle = choisir_rôle()
        joueur = Personnage(rôle)
        quêtes = [
            Quête("Infiltration à Neo-Paris", "Trouver des données dans la base synthétique.", "Données volées"),
            Quête("Alliance avec les Rebelles", "Aider les rebelles à reprendre l'usine.", "Arme rare"),
            Quête("Le Secret de Prométhée", "Découvrir le projet secret dans l'usine.", "Compétence secrète")
        ]

    while joueur.pv > 0 and not joueur.fin_jeu:
        lieu_choisi = choisir_lieu(joueur, quêtes, carte)
        gérer_quêtes(joueur, quêtes, lieu_choisi)

        if "Données de recherche" in joueur.inventaire:
            while True:
                craft = input("\nVoulez-vous fabriquer un implant ? (o/n) : ").strip().lower()
                if craft in ["o", "n"]:
                    break
                print("Veuillez entrer 'o' ou 'n'.")
            if craft == "o":
                craft_implants(joueur)

        sauvegarder(joueur, quêtes)

    print("\nMerci d'avoir joué à Néo-Terra 2187 !")

# --- Lancer le jeu ---
rpg_futuriste()

