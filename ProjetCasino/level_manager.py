#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Ici on gère les niveaux et les essais : on définit les paramètres et la fonction setup_level nous génère ensuite 
# le nombre mystère

import random

class LevelManager:
    def __init__(self):
        self.level = 1
        self.max_level = 3
        self.attempts = {1: 3, 2: 5, 3: 7}
        self.range = {1: 10, 2: 20, 3: 30}
        self.last_level_reached = 1

    def setup_level(self):
        target = random.randint(1, self.range[self.level])
        essais_restants = self.attempts[self.level]
        return target, essais_restants

