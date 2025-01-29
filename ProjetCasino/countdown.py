#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Comme son nom l'indique c'est pour contenir le countdown (sa fonction)

import time

def is_timeout(start_time, timeout=10):
    """Vérifie si le temps imparti est écoulé."""
    return time.time() - start_time > timeout

