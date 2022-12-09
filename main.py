#!/usr/bin/env python3

import datetime
from datetime import date
from os.path import exists
import codecs
import time
import os

# Traduction mois numérique en format humain
def get_human_month(x):
	list_months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
	return list_months[x - 1]


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
	current_date = datetime.date.today()
	current_month = current_date.month
	print("0 - Quitter le programme")
	print(f"1 - Travailler sur le CSV du mois courant ({get_human_month(current_month)})")
	print("2 - Choisir un fichier CSV")


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
		if (len(y[i]) <= 4):
			print(f"{x[i]} \t| {y[i]} \t\t| {z[i]}")
		else:
			print(f"{x[i]} \t| {y[i]} \t| {z[i]}")


# Test booléen pour déterminer si un fichier existe
def test_file_existence(path, filename):
	file_full = f"{path}/{filename}"
	result = exists(file_full)
	return result


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


# Module d'écriture dynamique d'événements dans des fichiers
def writing_events(path, filename, x, y, z):
	# Détection du fichier de destination
	today = date.today()
	current_year = today.year
	result = test_file_existence(path, filename)
	if (result == True):
		# Enregistrement des données dans le fichier adéquat
		fichier_destination = f"{str(current_year)[0:2]}{x[-2:]}_{x[3:5]}.csv"
		global_data, dates, opérations, objets = extract_data(path, fichier_destination)
		del global_data[0]
		del dates[0]
		del dates[len(dates) - 1]
		del opérations[0]
		del objets[0]

		compteur = 1
		position = 0
		for i in dates:
			if (int(x[0:2]) < int(i[0:2])):
				if ((compteur - 1) >= 1):
					if (int(x[0:2]) <= int(dates[-2][0:2])):
						position = compteur
						break
					else:
						position = compteur
				else:
					pass
			elif (int(x[0:2]) < int(i[0:2]) and compteur == 1):
				position = 1
				break
			elif (compteur == (len(dates) - 1) and position == 0):
				position = len(dates) + 1
			else:
				pass
			compteur += 1

		# Ecriture dans un buffer
		position -= 1
		dates.insert(position, x)
		opérations.insert(position, y)
		objets.insert(position, f"{z}\n")
		print(f"DEBEUG : {dates} !!! {opérations} !!! {objets}")

		# Ecriture du buffer vers le fichier
		f = open(f"{path}/{fichier_destination}", "w")
		f.write("Date;Opérations;Objet\n")
		for i in range(0, len(dates) - 1):
			f.write(f"{dates[i]};{opérations[i]};{objets[i]}")
		f.close()
		print(f"[+] Données correctement écrites dans le fichier '{fichier_destination}'")
	else:
		print(f"[!] Erreur : le fichier {filename} n'existe pas, voulez vous le créer pour y ajouter les données que vous venez de renseigner ? [Y/n]")
		choix_création_fichier = str(input("> "))
		if (choix_création_fichier.lower() == "y" or choix_création_fichier.lower() == "o"):
			# création du fichier et écriture des données
			nouveau_fichier = f"{str(current_year)[0:2]}{x[-2:]}_{x[3:5]}.csv"
			os.system(f'echo "Date;Opérations;Objet" > {path}/{nouveau_fichier}')
			f = open(f"{path}/{nouveau_fichier}", "a")
			f.write(f"{x};{y};{z}")
			f.close()
			print(f"[+] Données correctement écrites dans le fichier '{nouveau_fichier}' !")
		else:
			print("[*] Ok, abandon de l'écriture, aucun fichier ne sera mis à jour.")

	time.sleep(1.5)	


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
		print("Choix possibles pour la selection de la date")
		print("0 - Quitter")
		tmp_today_date = date.today()
		print(f"1 - Date courante ({tmp_today_date.day}-{tmp_today_date.month}-{tmp_today_date.year})")
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
			print("\n\nVeuillez compléter les informations suivantes :\n")
			time.sleep(0.25)

			# Récupération de l'année utilisateur
			récup_année = False
			bit_validation_dates = [0, 0, 0]
			loop_cutter_récup_dates = 0
			while (récup_année == False):
				asked_year = str(input("Année = "))
				isInteger = isInt(asked_year)
				if (isInteger == False):
					print(f"[!] Erreur : l'année {asked_year} n'est pas correcte !")
				else:
					asked_year = int(asked_year)
					current_date = datetime.date.today()
					current_year = current_date.year
					if (len(str(asked_year)) == 2):
						asked_year = str(current_year)[0:2] + str(asked_year)
						asked_year = int(asked_year)
						if (asked_year > 0 and asked_year <= current_year):
							bit_validation_dates[0] = 1
							récup_année = True
						else:
							pass
					elif (len(str(asked_year)) == 1):
						asked_year = str(current_year)[0:3] + str(asked_year)
						asked_year = int(asked_year)
						if (asked_year > 0 and asked_year <= current_year):
							bit_validation_dates[0] = 1
							récup_année = True
						else:
							pass
					elif (len(str(asked_year)) == 4):
						if (asked_year > 0 and asked_year <= current_year):
							bit_validation_dates[0] = 1
							récup_année = True
						else:
							pass
					else:
						print("[!] Erreur : La date entrée est de taille incorrecte !")

			# Récupération du mois utilisateur
			if (bit_validation_dates == [1, 0, 0]):
				récup_mois = False
			else:
				récup_mois = True

			loop_cutter_recup_mois = 0
			while (récup_mois == False):
				asked_month = str(input("Mois = "))
				isInteger = isInt(asked_month)
				if (isInteger == False):
					print(f"[!] Erreur : le mois {asked_month} n'est pas correct !")
				else:
					asked_month = int(asked_month)
					if (asked_month > 0 and asked_month <= 12):
						bit_validation_dates[1] = 1
						récup_mois = True
					else:
						if (loop_cutter_recup_mois >= 3):
							print("[!] Erreur : Nombre de tentatives infructueuses trop important, fermerture de l'instance !")
						else:
							print(f"[!] Erreur : le mois {asked_month} n'est pas correct !")

				loop_cutter_recup_mois += 1

			# Récupération du jour utilisateur
			if(bit_validation_dates == [1, 1, 0]):
				récup_jour = False
			else:
				récup_jour = True

			loop_cutter_recup_jour = 0
			while (récup_jour == False):
				asked_day = str(input("Jour = "))
				isInteger = isInt(asked_day)
				if (isInteger == False):
					print(f"[!] Erreur : {asked_day} n'est pas correct !")
				else:
					asked_day = int(asked_day)
					if (asked_day > 0 and asked_day <= 31):
						bit_validation_dates[2] = 1
						récup_jour = True
					else:
						print(f"[!] Erreur: Le jour {asked_day} n'est pas correct !")
				loop_cutter_recup_jour += 1
				if (loop_cutter_recup_jour >= 3):
					print(f"[!] Erreur : Nombre de tentatives infructueuses trop important, fermeture de l'instance !")
					récup_mois = True
				else:
					pass

			loop_cutter_récup_dates += 1
			# validation et composition de la sortie
			if (bit_validation_dates == [1, 1, 1]):
				if (len(str(asked_day)) == 1):
					asked_day = f"0{asked_day}"
				else:
					pass
				if (len(str(asked_month)) == 1):
					asked_month = f"0{asked_month}"
				else:
					pass
				today = f"{asked_day}/{asked_month}/{str(asked_year)[2:4]}"
				bit_validation[0] = 1
				quitter = True
			else:
				if (loop_cutter_récup_dates >= 3):
					print(f"[!] Erreur : Nombre de tentatives trop important, fermeture de l'instance !")
					quitter = True
				else:
					print("[!] Erreur lors de la tentative de récupération de la date !")
				

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
				opération_insert = f"{opération_insert[0:compteur]}.{opération_insert[compteur + 1:compteur + 3]}"
				retour = isFloat(opération_insert)
			else:
				pass

			compteur += 1

		if (retour == False):
			retour = isFloat(opération_insert)
		else:
			pass
		if (retour == True):
			opération_valide = opération_insert
			quitter_1 = True
			bit_validation[1] = 1

		else:
			print("[!] Somme entrée invalide, veuillez réessayer !")
			loopCutter_1 += 1
			if (loopCutter_1 >= 3):
				print("[!] Trop d'erreurs, fermeture de l'instance !")
				quitter_1 = True
				quitter_2 = True
			else:
				pass

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
	if (bit_validation == [1, 1, 1]):
		writing_events(path, nom_fichier, today, opération_valide, objet_insert)
	else:
		total = 0
		for a in bit_validation:
			total += a
		if (total <= 2):
			print(f"[!] Ecriture non effectuée, {3 - total} champs sont manquants !")
		else:
			print(f"[!] Ecriture non effectuée, {3 - total} champ est manquant !")


# Fonction de suppression de ligne(s) dans un fichier CSV
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

