#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Ce fichier est là pour afficher et mettre à jour les statistiques à la fin de la partie

class StatsManager:
    def __init__(self):
        self.stats = {
            'essais_tentés': 0,
            'Réussis': 0,
            'échecs': 0,
            'essai_actuel': 0,
            'essais_max': 0,
        }

    def update_stats(self, win):
        """Met à jour les statistiques en fonction d'une victoire ou d'une défaite."""
        if win:
            self.stats['Réussis'] += 1
            self.stats['essai_actuel'] += 1
            if self.stats['essai_actuel'] > self.stats['essais_max']:
                self.stats['essais_max'] = self.stats['essai_actuel']
        else:
            self.stats['échecs'] += 1
            self.stats['essai_actuel'] = 0

    def show_stats(self, name_user, solde):
        """Affiche les statistiques du joueur."""
        print("\nStatistiques du Jeu :")
        print(f"Nom de l'utilisateur : {name_user}")
        print(f"Parties jouées : {self.stats['essais_tentés']}")
        print(f"Réussites : {self.stats['Réussis']}")
        print(f"Échecs : {self.stats['échecs']}")
        print(f"Suite de victoires actuelle : {self.stats['essai_actuel']}")
        print(f"Suite de victoires maximale : {self.stats['essais_max']}")
        print(f"Solde actuel : {solde} €")

