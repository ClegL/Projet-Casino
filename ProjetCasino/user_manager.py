#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Ce fichier vérifie puis charge et sauvegarde les utilisateurs dans un fichier JSON
#Créé également de nouveaux si ça ne fonctionne pas 

import json
import os

class UserManager:
    def __init__(self):
        self.users_file = "users.json"
        self.users = self.load_users()

    def load_users(self):
        """Charge les utilisateurs depuis le fichier JSON."""
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as file:
                return json.load(file)
        return {}

    def save_users(self):
        """Sauvegarde les utilisateurs dans le fichier JSON."""
        with open(self.users_file, "w") as file:
            json.dump(self.users, file, indent=4)

    def load_user(self, name_user):
        """Charge les données d'un utilisateur spécifique."""
        return self.users.get(name_user)

    def create_user(self, name_user, solde, level, last_level_reached, stats):
        """Crée un nouvel utilisateur."""
        self.users[name_user] = {
            "solde": solde,
            "level": level,
            "last_level_reached": last_level_reached,
            "stats": stats,
        }
        self.save_users()

    def save_user(self, name_user, solde, level, last_level_reached, stats):
        """Sauvegarde les données d'un utilisateur."""
        self.users[name_user] = {
            "solde": solde,
            "level": level,
            "last_level_reached": last_level_reached,
            "stats": stats,
        }
        self.save_users()

