import random

# affection nombre aléatoire, arguments: un entier et un entier booléen (entre 1 et 5), return: nombre aléatoire convenu
def affection(nombre:int,difficulté:int):
    if difficulté == 1:
        nombre = random.randint(1,101)
        return nombre
    if difficulté == 2:
        nombre = random.randint(1,201)
        return nombre
    if difficulté == 3:
        nombre = random.randint(1,301)
        return nombre
    if difficulté == 4:
        nombre = random.randint(1,401)
        return nombre
    if difficulté == 5:
        nombre = random.randint(1,501)
        return nombre