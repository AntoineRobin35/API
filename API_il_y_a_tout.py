import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import re


# lancement d'école directe et time.sleep pour le checking browser(mais ne s'active pas tout le temps sur chrome)

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
#chrome_options.add_argument("--headless")  # Activer le mode headless
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.ecoledirecte.com/login")

# Attente jusqu'à ce que le champ "username" soit visible
try:
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
except TimeoutException:
    print("Le champ 'username' n'est pas apparu à temps.")
    driver.quit()

# connexion au site de école directe (login)

try :
    id = driver.find_element(By.ID, "username")
    id.clear()
    id.send_keys("exemple")
    password = driver.find_element(By.ID, "password")
    password.clear()
    password.send_keys("exemple")
except Exception as ex:
    print(f"Erreur lors de la saisie des identifiants : {ex}")
    driver.quit()

driver.find_element(By.ID, "connexion").click()


# Attente jusqu'à ce que la page des notes soit accessible
try:
    WebDriverWait(driver, 3600).until(
        EC.presence_of_element_located((By.CLASS_NAME, "icon-ed_carnetnotes"))
    )
    driver.find_element(By.CLASS_NAME, "icon-ed_carnetnotes").click()
except TimeoutException:
    print("Vous avez mis trop de temps à répondre à la question.")
    driver.quit()

# attente de la page des notes
time.sleep(10)

#création des dictionnaires qui stocke tout
dictionnaire_notes = {}
dictionnaire_moyennes = {}


# Ce code récupère toutes les matières et les classes dans le dictionnaire pour qu'elles deviennent des clés
changeur_de_matière = 1

while True:
    try :
        Xpath_nom_matière = f'//*[@id="encart-notes"]/div[2]/table/tbody/tr[{changeur_de_matière}]/td[1]/span[1]/span'
        chercheur_de_nom = driver.find_element(By.XPATH, Xpath_nom_matière)
        chercheur_de_nom = chercheur_de_nom.text
        dictionnaire_moyennes[chercheur_de_nom] = {}
        dictionnaire_notes[chercheur_de_nom] = {}
        changeur_de_matière = changeur_de_matière + 1
    except NoSuchElementException :
        break


# Code qui récupère les notes de chaques matières et les range dans un dictionnaire
changeur_de_matière = 1
changeur_de_clé = 0
changeur_de_note = 1
changeur_de_note_dictionnaire = 1

while True:
    try:
        x_path = f'//*[@id="encart-notes"]/div[2]/table/tbody/tr[{changeur_de_matière}]/td[3]/button[{changeur_de_note}]/span[1]'
        Notes = driver.find_element(By.XPATH, x_path)
        texte_complet = Notes.text  # Récupérer tout le texte

        if "sur" in texte_complet:
            changeur_de_note = changeur_de_note + 1
            continue  # Ignore cette itération si le format est incorrect

        texte_filtré_01 = texte_complet.split()[0].replace(",", ".")  # Remplacez la virgule par un point

        try:
            texte_filtré_02 = float(texte_filtré_01)  # Convertir en float
        except ValueError:
            dictionnaire_notes[list(dictionnaire_notes.keys())[changeur_de_clé]][f"note{changeur_de_note_dictionnaire}"] = {}
            dictionnaire_notes[list(dictionnaire_notes.keys())[changeur_de_clé]][f"note{changeur_de_note_dictionnaire}"]["valeur"] = texte_filtré_01
            changeur_de_note = changeur_de_note + 1
            changeur_de_note_dictionnaire = changeur_de_note_dictionnaire + 1
            continue

    except NoSuchElementException :
        if changeur_de_clé < len(dictionnaire_notes):
            changeur_de_note = 1
            changeur_de_note_dictionnaire = 1
            changeur_de_matière = changeur_de_matière + 1
            changeur_de_clé = changeur_de_clé + 1
            continue
        else:
            break
    try:
        x_path2 = f'//*[@id="encart-notes"]/div[2]/table/tbody/tr[{changeur_de_matière}]/td[3]/button[{changeur_de_note}]/span[1]/sub'
        Diviseur = driver.find_element(By.XPATH, x_path2)
        texte_complet_diviseur = Diviseur.text.replace("/", "")  # Remplacez la virgule par un point
        texte_filtré_diviseur = float(texte_complet_diviseur)  # Convertir en float
        note_sur_20 = 20 / texte_filtré_diviseur * texte_filtré_02
        dictionnaire_notes[list(dictionnaire_notes.keys())[changeur_de_clé]][f"note{changeur_de_note_dictionnaire}"] = {}
        dictionnaire_notes[list(dictionnaire_notes.keys())[changeur_de_clé]][f"note{changeur_de_note_dictionnaire}"]["valeur"] = note_sur_20
    except NoSuchElementException:
        dictionnaire_notes[list(dictionnaire_notes.keys())[changeur_de_clé]][f"note{changeur_de_note_dictionnaire}"] = {}
        dictionnaire_notes[list(dictionnaire_notes.keys())[changeur_de_clé]][f"note{changeur_de_note_dictionnaire}"]["valeur"] = texte_filtré_02
    finally:
        changeur_de_note += 1
        changeur_de_note_dictionnaire += 1

# code qui récupère les différents coefs et qui les range dans le dictionnaire
changeur_de_matière = 1
changeur_de_clé = 0
changeur_de_coefs = 1
changeur_de_clé_coefs = 0
while True :
    coefs = None
    try:
        X_path_coef = f"//*[@id='encart-notes']/div[2]/table/tbody/tr[{changeur_de_matière}]/td[3]/button[{changeur_de_coefs}]/span[1]/sup"
        coefs = driver.find_element(By.XPATH, X_path_coef)
        coefs = coefs.text
        coefs = coefs.strip("()")
        coefs = float(coefs)  # conversion string(chaine de caractère) vers float(nombre décimal)
        if coefs.is_integer():  # is_integer vérifie si la valeur float est un entier déguisé (comme 2.0)
            coefs = int(coefs)  # Convertit en entier
        dictionnaire_notes[list(dictionnaire_notes.keys())[changeur_de_clé]][f"note{changeur_de_coefs}"]["coef"] = coefs
        changeur_de_coefs = changeur_de_coefs + 1
        changeur_de_clé_coefs = changeur_de_clé_coefs + 1
    except NoSuchElementException:
        if changeur_de_clé_coefs < len(dictionnaire_notes[list(dictionnaire_notes.keys())[changeur_de_clé]]):
            dictionnaire_notes[list(dictionnaire_notes.keys())[changeur_de_clé]][f"note{changeur_de_coefs}"]["coef"] = 1
            coefs = 1
            changeur_de_coefs = changeur_de_coefs + 1
            changeur_de_clé_coefs = changeur_de_clé_coefs + 1
            continue
        else:
            if changeur_de_matière < len(dictionnaire_notes):
                changeur_de_matière = changeur_de_matière + 1
                changeur_de_coefs = 1
                changeur_de_clé = changeur_de_clé + 1
                changeur_de_clé_coefs = 0
                continue
            else:
                break



# code pour récupérer les compétences et rangement dans dictionnaire
liste_compétences = []
changeur_de_compétences = 3
changeur_de_note = 1
changeur_de_matière = 1
changeur_de_clé = 0
while True:
    try:
        Xpath_compétences = f'//*[@id="encart-notes"]/div[2]/table/tbody/tr[{changeur_de_matière}]/td[3]/button[{changeur_de_note}]/span[{changeur_de_compétences}]/span'
        compétences = driver.find_element(By.XPATH, Xpath_compétences)
        compétences = compétences.text
        liste_compétences.append(compétences)
        changeur_de_compétences = changeur_de_compétences + 1
    except:
        if changeur_de_note < len(dictionnaire_notes[list(dictionnaire_notes.keys())[changeur_de_clé]]):
            dictionnaire_notes[list(dictionnaire_notes.keys())[changeur_de_clé]][f"note{changeur_de_note}"]["compétences"] = liste_compétences
            #print("matière {} ".format(changeur_de_matière),"note {} ".format(changeur_de_note),liste_compétences)
            liste_compétences = []
            changeur_de_note = changeur_de_note + 1
            changeur_de_compétences = 3
            continue
        else:
            if changeur_de_matière < len(dictionnaire_notes):
                dictionnaire_notes[list(dictionnaire_notes.keys())[changeur_de_clé]][f"note{changeur_de_note}"]["compétences"] = liste_compétences
                #print("matière {} ".format(changeur_de_matière), "note {} ".format(changeur_de_note), liste_compétences)
                liste_compétences = []
                changeur_de_matière += 1
                changeur_de_clé += 1
                changeur_de_note = 1
                changeur_de_compétences = 3
                continue
            else:
                break

# on quitte Ecole Directe
driver.quit()

# Calcul de la moyenne pondérée pour chaque matière
changeur_de_clé = 0  # Index pour parcourir les matières
total_moyenne = 0
for i in range(len(dictionnaire_notes)):
    total_notes = 0
    total_coefs = 0
    matière = list(dictionnaire_notes.keys())[changeur_de_clé]  # Obtenir la clé de la matière
    notes_valides = False  # Indicateur de présence de valeurs numériques

    for note in dictionnaire_notes[matière].values():
        try:
            valeur = float(note["valeur"])  # Tente de convertir en float
            coef = note["coef"]
            total_notes += valeur * coef
            total_coefs += coef
            notes_valides = True  # Une valeur valide a été trouvée
        except ValueError:  # Ignore les valeurs non numériques comme "Abs"
            pass  # Simplement passer à la prochaine note

    # Gérer le cas où il n'y a pas de valeurs numériques
    if not notes_valides:
        moyenne = None  # Pas de moyenne calculable
    else:
        moyenne = total_notes / total_coefs  # Calcul normal
        moyenne = round(moyenne, 2)
        total_moyenne += moyenne

    # Ajouter la moyenne dans le dictionnaire même si elle est None et calcul de la moyenne générale
    dictionnaire_moyennes[matière]["moyenne"] = moyenne
    changeur_de_clé += 1

# Calcul de la moyenne générale
moyenne_générale = 0
moyenne_générale = total_moyenne / len(dictionnaire_moyennes)
moyenne_générale = round(moyenne_générale, 2)
dictionnaire_moyennes["moyenne_générale"] = moyenne_générale


print(dictionnaire_notes)
print(dictionnaire_moyennes)
