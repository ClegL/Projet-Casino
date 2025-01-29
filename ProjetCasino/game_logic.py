#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Ce fichier contient comme son nom l'indique la logique du jeu, c'est ici que le plus gros se fait 
# Il gère également les intéractions utilisateur, les niveaux, les essais, les mises et les gains via les modules importés 

from level_manager import LevelManager  # Gère les niveaux et les essais
from user_manager import UserManager  # Charge et sauvegarde les données utilisateur
from stats_manager import StatsManager  # Affiche et met à jour les stats
from countdown import is_timeout
import time  

class CasinoGame:
    def __init__(self):
        self.user_manager = UserManager()
        self.level_manager = LevelManager()
        self.stats_manager = StatsManager()
        self.name_user = ""
        self.solde = 1000  # Dotation initiale de l'utilisateur
        self.mise = 0
        self.gain = 0

    def start_game(self):
        print("Bienvenue au Casino !")
        self.name_user = input("Entrez votre nom : ").strip()

        # Pour charger/créer un utilisateur
        user_data = self.user_manager.load_user(self.name_user)
        if user_data:
            print(f"Bon retour, {self.name_user} !")
            self.solde = user_data.get("solde", self.solde)
            self.level_manager.level = user_data.get("level", 1)
            self.level_manager.last_level_reached = user_data.get("last_level_reached", 1)
            self.stats_manager.stats = user_data.get("stats", self.stats_manager.stats)
        else:
            print(f"Bonjour, {self.name_user} ! C'est votre première fois ici.")
            self.user_manager.create_user(self.name_user, self.solde, self.level_manager.level, self.level_manager.last_level_reached, self.stats_manager.stats)

        print(f"\nVous avez une dotation initiale de {self.solde} €.")
        print("Les règles du niveau 1 sont les suivantes :")
        print("- Si vous devinez le nombre du premier coup, vous doublez votre mise.")
        print("- Si vous devinez au deuxième coup, vous gagnez votre mise exacte.")
        print("- Si vous ne devinez pas après 3 essais, vous perdez votre mise.")
        print("Ces règles ne s'appliquent qu'au niveau 1. Aux niveaux suivants, vous pouvez miser, mais les gains ne sont pas multipliés.")

        while True:
            self.play_level()
            if not self.ask_to_continue():
                break

        self.stats_manager.show_stats(self.name_user, self.solde)
        self.user_manager.save_user(self.name_user, self.solde, self.level_manager.level, self.level_manager.last_level_reached, self.stats_manager.stats)

    def play_level(self):
        target, essais_restants = self.level_manager.setup_level()
        self.mise = int(input(f"\nNiveau {self.level_manager.level} : Combien souhaitez-vous miser ? (Solde actuel : {self.solde} €) : "))
        while self.mise > self.solde or self.mise <= 0:
            print("Mise invalide. Veuillez entrer une mise valide.")
            self.mise = int(input(f"Combien souhaitez-vous miser ? (Solde actuel : {self.solde} €) : "))

        self.solde -= self.mise
        print(f"\nNiveau {self.level_manager.level} : Devinez le nombre entre 1 et {self.level_manager.range[self.level_manager.level]}.")
        print(f"Il vous reste {essais_restants} essais.")

        nb_coup = 0
        while essais_restants > 0:
            try:
                start_time = time.time()  # Utilisez time.time()
                guess = int(input("Votre proposition : "))
                end_time = time.time()  # Utilisez time.time()

                if is_timeout(start_time, timeout=10):
                    print("Temps écoulé ! Vous perdez un essai.")
                    essais_restants -= 1
                    continue

                nb_coup += 1
                if guess == target:
                    print("Félicitations ! Vous avez deviné le nombre.")
                    self.stats_manager.update_stats(win=True)
                    self.gain = self.calculate_gain(nb_coup)
                    self.solde += self.gain
                    print(f"Vous avez gagné {self.gain} €. Votre solde est maintenant de {self.solde} €.")

                    if self.level_manager.level < self.level_manager.max_level:
                        self.level_manager.level += 1
                        self.level_manager.last_level_reached = self.level_manager.level
                    break
                else:
                    if guess < target:
                        print("Le nombre mystère est plus grand.")
                    else:
                        print("Le nombre mystère est plus petit.")
                    essais_restants -= 1

            except ValueError:
                print("Veuillez entrer un nombre valide.")

        if essais_restants == 0:
            print(f"Vous avez perdu ce niveau. Le nombre était {target}.")
            self.stats_manager.update_stats(win=False)
            if self.level_manager.level > 1:
                self.level_manager.level -= 1

        self.stats_manager.stats['essais_tentés'] += 1

    def calculate_gain(self, nb_coup):
        if self.level_manager.level == 1:
            if nb_coup == 1:
                return self.mise * 2
            elif nb_coup == 2:
                return self.mise
            else:
                return 0
        else:
            return self.mise

    def ask_to_continue(self):
        print("\nVoulez-vous continuer à jouer ?")
        print("Vous avez 10 secondes pour décider. Appuyez sur Entrée pour continuer ou 'q' pour quitter.")
        start_time = time.time()  # Utilisez time.time()
        choix = input()
        end_time = time.time()  # Utilisez time.time()

        if is_timeout(start_time, timeout=10):
            print("Le temps est écoulé, partie terminée !")
            return False

        if choix.lower() == 'q':
            return False
        return True

