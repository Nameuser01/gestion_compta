#!/usr/bin/env python3

from datetime import date
from os.path import exists
import codecs
import time
import os

# Vérifie l'existence du fichier csv du mois courant. Si le fichier n'existe pas, il sera créé
def file_verification(path):
	# Récupération de la date actuelle
	tmp_filename = str(date.today())
	filename = f"{tmp_filename[0:4]}_{tmp_filename[5:7]}.csv"

	# Vérification de l'existence et création du fichier si nécessaire
	file_exists = exists(f"{path}/{filename}")
	if (file_exists == False):
		os.system(f'echo "Date;Opérations;Objet" > {path}/{filename}')
	else:
		pass

# Afficher le menu de selection des fichiers de travail
def menu():
	print("0 - Quitter le programme")
	print("1 - Travailler sur le CSV du mois courant")
	print("2 - Travailler sur un fichier CSV")


# Afficher le menu d'actions possibles sur les fichiers csv
def menu_actions_csv(nom_fichier):
	print("0 - Revenir au menu principal")
	print(f"1 - Lire le fichier courant ({nom_fichier})")
	print(f"2 - Ajouter un événement au fichier courant ({nom_fichier})")
	print(f"3 - Supprimer un événement du fichier courant ({nom_fichier})")
	print(f"4 - Modifier un événement du fichier courant ({nom_fichier})")


# Demander une action de l'utilisateur pour continuer et clear le terminal
def clear():
	time.sleep(0.2)
	foo = input("\n\n[*] Appuyez sur entrée pour continuer...")
	os.system("clear")


# Récupération et vérification du nom de fichier entré par l'utilisateur
def choix_nom_fichier(path):
	retry = True
	loop_cutter = 0
	while (retry == True):
		nom_fichier = input("Quel est le nom de votre fichier ?\n> ")
		nom_fichier = "".join(nom_fichier.split())
		file_exists = exists(f"{path}/{nom_fichier}")
		if (file_exists == False):
			retry = True
			print("\n\n[!] Erreur: Le fichier indiqué n'existe pas !")
		elif (file_exists == True):
			retry = False
			return nom_fichier
		else:
			loop_cutter += 1
			if (loop_cutter >= 3):
				retry = False
				print("[!] Erreur: Boucle infinie !")
			else:
				pass
			print("Erreur liée à la librairie 'exists' !")

# Parsing des données récupérées depuis les fichiers CSV séléctionnés
def extract_data(path, nom_fichier):
	f = codecs.open(f"{path}/{nom_fichier}", "r", "utf8")
	data_global = f.read()
	f.close()
	data_global = data_global.replace("\n", ";")
	data_global = data_global.split(";")
	date = data_global[0:len(data_global):3]
	operation = data_global[1:len(data_global):3]
	objet = data_global[2:len(data_global):3]
	return data_global, date, operation, objet


# Fonction de débeug pour le control des tailles des listes <dates>, <operations> et <objets>
def length_control(x, y, z):
	print(f"X :\n{x}\nlen(x) = {len(x)}\n\n===\nY :\n{y}\nlen(y) = {len(y)}\n\n===\nZ :\n{z}\nlen(z) = {len(z)}")

# Disposer clairement les données du fichier travaillé dans le terminal pour l'utilisateur
def reading_file(x, y, z, nom_fichier):
	print(nom_fichier)
	title_1 = " Date \t\t|"
	title_2 = " Operation \t|"
	title_3 = " Objet"
	separator_1 = "-" * (len(title_1) * 2 - 2)
	separator_2 = "-" * (len(title_2) + 2)
	separator_3 = "-" * (len(title_3) * 5)
	print(f"\n{title_1}{title_2}{title_3}\n{separator_1}+{separator_2}+{separator_3}")
	for i in range(1, len(x) - 1):
		print(f"{x[i]} \t| {y[i]} \t| {z[i]}")

# Test booléen pour déterminer si une variable est un float
def isFloat(x):
		try:
			float(x)
			return True
		except ValueError:
			return False

# Test booléen pour déterminer si une variable est un integer
def isInt(x):
		try:
			int(x)
			return True
		except ValueError:
			return False

# add events to a csv file
def adding_file(path, nom_fichier):
	# Récupération des informations à insérer dans le CSV
	loopCutter = 0
	quitter = False
	loopCutter_1 = 0
	quitter_1 = False
	loopCutter_2 = 0
	quitter_2 = False
	bit_validation = [0, 0, 0]

	# Récupération de la date
	while (quitter == False):
		os.system("clear")
		print("= = Choix possibles pour la selection de la date = =")
		print("0 - Quitter")
		print("1 - Date courante")
		print("2 - Date pesonnalisée")
		selec_date_entry = input("\n\nChoix d'une option\n> ")
		selec_date_entry = "".join(selec_date_entry.split())
		
		if (selec_date_entry == "0"):
			quitter = True
			quitter_1 = True
			quitter_2 = True
			print("[*] Fermeture de l'interface d'édition.")

		elif (selec_date_entry == "1"):
			tmp_today = str(date.today())
			today = f"{tmp_today[-2:]}/{tmp_today[5:7]}/{tmp_today[2:4]}"
			print("[+] Date correctement enregistrée")
			time.sleep(1.5)
			quitter = True
			bit_validation[0] = 1

		elif (selec_date_entry == "2"):
			print("Veuillez compléter les informations suivantes :\n\n")
			time.sleep(1.5)

			# Récupération de l'année utilisateur
			recup_année = False
			while (récup_année == False):
				asked_year = str(input("Année = "))
				isInteger = isInt(asked_year)
				if (isInteger == False):
					print(f"[!] Erreur : l'année {asked_year} n'est pas correcte !")
				else:
					current_date = datetime.date.today()
					current_year = today.year
					if (len(asked_year) == 2):
						asked_year = str(current_year)[0:2] + str(asked_year)
						asked_year = int(asked_year)
						if (asked_year > 0 and asked_year <= current_year):
							récup_année = True
						else:
							pass
					elif (len(asked_year) == 1):
						asked_year = str(current_year)[0:3] + str(asked_year)
						asked_year = int(asked_year)
						if (asked_year > 0 and asked_year <= current_year):
							récup_année = True
						else:
							pass
					elif (len(asked_year) == 4):
						if (asked_year > 0 and asked_year <= current_year):
							récup_année = True
						else:
							pass
					else:
						print("[!] Erreur : La date entrée possède une taille incorrecte !")

			# validation et composition de la sortie
			today = 

			quitter = True
			bit_validation[0] = 1  # Bit validation récupération correcte de la date

		else:
			loopCutter += 1
			print("[!] Erreur: Entrée incorrecte")
			if (loopCutter >= 6):
				print("[!] Trop d'erreurs, fermeture de l'instance !")
				quitter = True
				quitter_1 = True
				quitter_2 = True
			else:
				pass

	# Récupération de l'opération
	while(quitter_1 == False):
		os.system("clear")
		opération_insert = input("Opération à ajouter\n> ")
		compteur = 0
		retour = False
		for i in opération_insert:
			if (i == "."):
				retour = isFloat(opération_insert)
			elif (i == ","):
				print(f"DEBEUG: somme à ajouter |{opération_insert[0:compteur]}|.|{opération_insert[compteur + 1:compteur + 3]}|")
				tmp_injection = f"{opération_insert[0:compteur]}.{opération_insert[compteur + 1:compteur + 3]}"
				print(f"tmp_injection vaut {tmp_injection}")
				retour = isFloat(tmp_injection)
				print(f"retour = {retour}")
				time.sleep(5)

			else:
				pass

			compteur += 1

		if (compteur == len(opération_insert) and retour == False):
			retour = isFloat(opération_insert)
		else:
			pass

		if (retour == True):
			opération_valide = opération_insert
			quitter_1 = True
			bit_validation[1] = 1

		else:
			print("[!] Somme entrée invalide, veuillez réessayer!")
			loopCutter_1 += 1
			if (loopCutter_1 >= 3):
				print("[!] Trop d'erreurs, fermeture de l'instance !")
				quitter_1 = True
				quitter_2 = True
			else:
				pass

		print(f"Somme à injecter dans le fichier csv : {opération_insert} €")  # DEBEUG
		time.sleep(3)  # DEBEUG

	# Récupération de l'objet lié à l'ajout de l'opération actuelle
	while (quitter_2 == False):
		os.system("clear")
		objet_insert = input("Objet de l'opération\n> ")
		if (len(objet_insert) > 0):
			quitter_2 = True
			bit_validation[2] = 1

		else:
			loopCutter_2 += 1
			if (loopCutter_2 >= 3):
				quitter_2 = True
			else:
				pass

	# Ajout des événements au fichier CSV
	print(f"bit validation vaut {bit_validation}")
	if (bit_validation == [1, 1, 1]):
		f = open(f"{path}/{nom_fichier}", "a")
		f.write(f"{today};{opération_valide} €;{objet_insert}\n")
		f.close()
		print(f"[+] Données écrites dans le fichier !")
	else:
		total = 0
		for a in bit_validation:
			total += a
		print(f"[!] Ecriture non effectuée, {3 - total} champs est manquant !")

	time.sleep(2)

def delete_lines(path, nom_fichier, num_line):
	f = open(f"{path}/{nom_fichier}", "r")
	f_content = f.readlines()
	f.close()
	os.system(f"echo '' > {path}/{nom_fichier}")
	f = open(f"{path}/{nom_fichier}", "a")
	print(f"f_content = {f_content}")
	compteur = 0
	for i in f_content:
		for a in num_line:
			erase = False
			if (compteur == a):
				erase = True
				break
			else:
				pass
		if (erase == False):
			f.write(i)
		else:
			pass

		compteur += 1
	f.close()
	time.sleep(10)

# Vérification de l'existence du fichier du mois courant 
path = "/home/elliot/py/comptabilité/DB"
file_verification(path)

quitter = False
loopCutter = 0

while (quitter == False):
	os.system("clear")
	menu()
	choix = input("Que voulez vous faire ?\n> ")
	if (choix == "0"):
		time.sleep(0.2)
		print("[*] Fermeture du programme...")
		quitter = True

	elif (choix == "1"):  # Selectionner le CSV du mois courant
		os.system("clear")
		# Récupération de la date courante pour composition du nom de fichier à traiter
		today = str(date.today())
		nom_fichier = f"{today[0:4]}_{today[5:7]}.csv"

		data_global, dates, operations, objets = extract_data(path, nom_fichier)
		#length_control(dates, operations, objets)  # Etape de control / debeug
		min_list = []
		min_list.append(len(dates))
		min_list.append(len(operations))
		min_list.append(len(objets))
		min_list = [int(i) for i in min_list]
		min_list.sort()
		for i in (dates, operations, objets):
			if (len(i) > min_list[0]):
				diff = len(i) - min_list[0]
				del i[-diff:]
			else:
				pass

		quitter_action_fichier = False
		loopCutter_action_fichier = 0

		# === Boucle des actions a effectuer sur le fichier courant ===
		while (quitter_action_fichier == False):
			os.system("clear")
			menu_actions_csv(nom_fichier)
			action_fichier = input("Que voulez vous faire ?\n> ")

			if (action_fichier == "0"):
				quitter_action_fichier = True
				time.sleep(0.2)
				print("[*] Retour...")

			elif (action_fichier == "1"):
				data_global, dates, operations, objets = extract_data(path, nom_fichier)
				reading_file(dates, operations, objets, nom_fichier)

			elif (action_fichier == "2"):
				adding_file(path, nom_fichier)

			elif (action_fichier == "3"):
				delete_lines(path, nom_fichier, 2)	

			else:
				loopCutter_action_fichier += 1
				print("[!] Erreur: Entrée incorrecte")
				if (loopCutter_action_fichier >= 3):
					print("[!] Trop d'erreurs, fermeture de l'instance !")
					quitter_action_fichier = True
				else:
					pass

			clear()


	elif (choix == "2"): # Selectionner un fichier CSV
		os.system('clear')
		nom_fichier = choix_nom_fichier(path)
		data_global, dates, operations, objets = extract_data(path, nom_fichier)
		# length_control(dates, operations, objets)  # Etape de control / debeug
		# Length normalization
		min_list = []
		min_list.append(len(dates))
		min_list.append(len(operations))
		min_list.append(len(objets))
		min_list = [int(i) for i in min_list]
		min_list.sort()
		for i in (dates, operations, objets):
			if (len(i) > min_list[0]):
				diff = len(i) - min_list[0]
				del i[-diff:]
			else:
				pass

		quitter_action_fichier = False
		loopCutter_action_fichier = 0
		# === Boucle des actions a effectuer sur le fichier courant ===
		while (quitter_action_fichier == False):
			os.system("clear")
			menu_actions_csv(nom_fichier)
			action_fichier = input("Que voulez vous faire ?\n> ")

			if (action_fichier == "0"):
				quitter_action_fichier = True
				time.sleep(0.2)
				print("[*] Retour...")

			elif (action_fichier == "1"):
				reading_file(dates, operations, objets, nom_fichier)

			elif (action_fichier == "2"):
				adding_file(path, nom_fichier)

			elif (action_fichier == "3"):
				to_delete = [2, 4]
				delete_lines(path, nom_fichier, to_delete)

			else:
				loopCutter_action_fichier += 1
				print("[!] Erreur: Entrée incorrecte")
				if (loopCutter_action_fichier >= 3):
					print("[!] Trop d'erreurs, fermeture de l'instance !")
					quitter_action_fichier = True
				else:
					pass

			clear()

	else:
		loopCutter += 1
		print("[-] Erreur: Entrée incorrecte")
		if (loopCutter >= 3):
			print("[!] Trop d'erreurs, fermeture de l'instance !")
			quitter = True
		else:
			pass