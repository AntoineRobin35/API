import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException # attention à cet import c'est pour l'expect pour mettre les coefs même si la variable n'existe pas
from selenium.webdriver.common.keys import Keys
import re

# lancement d'école directe et time.sleep pour le checking browser(mais ne s'active pas tout le temps sur chrome)

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.ecoledirecte.com/login")
time.sleep(5)

# connexion au site de école directe (login)

try :
    id = driver.find_element(By.ID, "username")
    id.clear()
    id.send_keys("Marceau35580")
    password = driver.find_element(By.ID, "password")
    password.clear()
    password.send_keys("Soleil04*")
except Exception as ex :
    assert False

driver.find_element(By.ID, "connexion").click()

# time.sleep pour la question "capchat" et clique sur l'icone note

time.sleep(10)

driver.find_element(By.CLASS_NAME, "icon-ed_carnetnotes").click()

time.sleep(5)

variables_dynamiques = {}  # Un dictionnaire pour stocker les "variables dynamiques"

texte_final = []

def notes(changeur_de_note, changeur_de_matière):
    global texte_final
    texte_final = []
    for i in range(10):
        try:
            x_path = f'//*[@id="encart-notes"]/div[2]/table/tbody/tr[{changeur_de_matière}]/td[3]/button[{changeur_de_note}]/span[1]'
            Notes = driver.find_element(By.XPATH, x_path)
            texte_complet = Notes.text  # Récupérer tout le texte

            if texte_complet == "Abs ":
                changeur_de_note = changeur_de_note + 1
                continue # pour reprendre la boucle au début
            if "sur" in texte_complet:
                continue  # Ignore cette itération si le format est incorrect

            texte_filtré_01 = texte_complet.split()[0].replace(",", ".")  # Remplacez la virgule par un point
            texte_filtré_02 = float(texte_filtré_01)  # Convertir en float
        except NoSuchElementException :
            break
        try:
            x_path2 = f'//*[@id="encart-notes"]/div[2]/table/tbody/tr[{changeur_de_matière}]/td[3]/button[{changeur_de_note}]/span[1]/sub'
            Diviseur = driver.find_element(By.XPATH, x_path2)
            texte_complet_diviseur = Diviseur.text.replace("/", "")  # Remplacez la virgule par un point
            texte_filtré_diviseur = float(texte_complet_diviseur)  # Convertir en float
            note_sur_20 = 20 / texte_filtré_diviseur * texte_filtré_02
            texte_final.append(note_sur_20)
        except NoSuchElementException:
            texte_final.append(texte_filtré_02)  # Ajoutez une valeur par défaut (au cas où)
        finally:
            changeur_de_note += 1
    return texte_final  # Retourner la liste après la boucle

# Appeler la fonction
notes_français = notes(1,1)
notes_histoire = notes(1, 2)
notes_Matématiques = notes(1,3)
notes_SVT = notes(1,4)
notes_Physique_Chimie = notes(1,5)
notes_Technologie = notes(1,6)
notes_Anglais = notes(1,7)
notes_Espagnol = notes(1,8)
notes_Sport = notes(1,9)
notes_Art_Plastiques = notes(1,10)
notes_Musique = notes(1,11)
notes_Oral = notes(1,12)



liste_coef = []
def coef(changeur_de_coefs, changeur_de_matière, nom_des_listes):
    global liste_coef
    global notes_français
    global notes_Oral
    global notes_Musique
    global notes_Art_Plastiques
    global notes_Espagnol
    global notes_Technologie
    global notes_Physique_Chimie
    global notes_Sport
    global notes_SVT
    global notes_Matématiques
    global notes_histoire
    global notes_Anglais
    liste_coef = []
    for i in range(len(nom_des_listes)):
        try:
            X_path_coef = f"//*[@id='encart-notes']/div[2]/table/tbody/tr[{changeur_de_matière}]/td[3]/button[{changeur_de_coefs}]/span[1]/sup"
            coefs = driver.find_element(By.XPATH, X_path_coef)
            liste_coef.append(coefs.text)
            # Supprimer les caractères indésirables et convertir en nombre si possible
            liste_coef = [
                float(re.sub(r"[()]", "", element)) if isinstance(element, str) else element
                for element in liste_coef
            ]
        except NoSuchElementException:
            liste_coef.append(1)
        finally:
            changeur_de_coefs += 1
    return liste_coef

coef_français = coef(1,1,notes_français)
coef_histoire = coef(1,2, notes_histoire)
coef_Mathématiques = coef(1,3, notes_Matématiques)
coef_SVT = coef(1,4, notes_SVT)
coef_Physique_Chimie = coef(1,5, notes_Physique_Chimie)
coef_Technologie = coef(1,6,notes_Technologie)
coef_Anglais = coef(1,7,notes_Anglais)
coef_Espagnol = coef(1,8,notes_Espagnol)
coef_sport = coef(1,9,notes_Sport)
coef_Art_Plastiques = coef(1,10, notes_Art_Plastiques)
coef_Musique = coef(1,11, notes_Art_Plastiques)
coef_Oral = coef(1,12,notes_Oral)


somme = 0
somme_des_coefs = 0
def calcul_moyenne(coef, notes):
    global somme
    global somme_des_coefs
    somme_des_coefs = 0
    somme = 0
    global notes_français
    global notes_Oral
    global notes_Musique
    global notes_Art_Plastiques
    global notes_Espagnol
    global notes_Technologie
    global notes_Physique_Chimie
    global notes_Sport
    global notes_SVT
    global notes_Matématiques
    global notes_histoire
    global notes_Anglais
    global coef_français
    global coef_histoire
    global coef_Mathématiques
    global coef_SVT
    global coef_Physique_Chimie
    global coef_Technologie
    global coef_Anglais
    global coef_Espagnol
    global coef_sport
    global coef_Art_Plastiques
    global coef_Musique
    global coef_Oral

    if not coef or not notes:  # Si l'une des listes est vide
        return "Vous n'avez pas de moyenne pour cette matière"
        pass

    for i in range(0, len(coef)):
        somme = somme + float(notes[i]) * float(coef[i])
        somme_des_coefs = somme_des_coefs + coef[i]
        moyenne = round(somme / somme_des_coefs, 2)
    return moyenne

moyenne_français = calcul_moyenne(coef_français, notes_français)
print("Ta moyennes de français est de : ", moyenne_français)

moyenne_histoire = calcul_moyenne(coef_histoire, notes_histoire)
print("Ta moyennes d'Histoire est de : ", moyenne_histoire)

moyenne_Mathématiques = calcul_moyenne(coef_Mathématiques, notes_Matématiques)
print("Ta moyennes de Mathématiques est de : ", moyenne_Mathématiques)

moyenne_SVT = calcul_moyenne(coef_SVT, notes_SVT)
print("Ta moyennes de SVT est de : ", moyenne_SVT)

moyenne_Physique = calcul_moyenne(coef_Physique_Chimie, notes_Physique_Chimie)
print("Ta moyennes de Physique-Chimie est de : ", moyenne_Physique)

moyenne_Technologie = calcul_moyenne(coef_Technologie, notes_Technologie)
print("Ta moyennes de Technologie est de : ", moyenne_Technologie)

moyenne_Anglais = calcul_moyenne(coef_Anglais, notes_Anglais)
print("Ta moyennes d' Anglais est de : ", moyenne_Anglais)

moyenne_Espagnol = calcul_moyenne(coef_Espagnol, notes_Espagnol)
print("Ta moyennes d'Espagnol est de : ", moyenne_Espagnol)

moyenne_Sport = calcul_moyenne(coef_sport, notes_Sport)
print("Ta moyennes de Sport est de : ", moyenne_Sport)

moyenne_Art_Plastiques = calcul_moyenne(coef_Art_Plastiques, notes_Art_Plastiques)
print("Ta moyennes d'Art Plastiques est de : ", moyenne_Art_Plastiques)

moyenne_Musique = calcul_moyenne(coef_Musique, notes_Musique)
print("Ta moyennes de Musique est de : ", moyenne_Musique)

moyenne_Oral = calcul_moyenne(coef_Oral, notes_Oral)
print("Ta moyennes d'Oral est de : ", moyenne_Oral)


# Liste des moyennes
moyennes = [
    moyenne_français, moyenne_histoire, moyenne_Mathématiques, moyenne_SVT,
    moyenne_Physique, moyenne_Technologie, moyenne_Anglais, moyenne_Espagnol,
    moyenne_Sport, moyenne_Art_Plastiques, moyenne_Musique, moyenne_Oral
]

# Initialisation
somme_des_moyennes = 0
nombre_de_moyennes_valides = 0

# Vérification et calcul
for moyenne in moyennes:
    try:
        # Tente de convertir la moyenne en float
        somme_des_moyennes += float(moyenne)
        nombre_de_moyennes_valides += 1
    except ValueError:
        # Ignore les moyennes invalides (par exemple, avec des lettres)
        pass
# Calcul de la moyenne générale si au moins une moyenne valide
if nombre_de_moyennes_valides > 0:
    moyenne_générale = somme_des_moyennes / nombre_de_moyennes_valides
    print("Ta moyenne générale est de :", round(moyenne_générale, 2))
else:
    print("Aucune moyenne valide n'a été trouvée.")