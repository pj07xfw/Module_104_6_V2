"""
    Fichier : gestion_magasin_crud.py
    Auteur : OM 2021.03.16
    Gestions des "routes" FLASK et des données pour les fonctionalite.
"""
import sys

import pymysql
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from APP_FILMS import obj_mon_application
from APP_FILMS.database.connect_db_context_manager import MaBaseDeDonnee
from APP_FILMS.erreurs.exceptions import *
from APP_FILMS.erreurs.msg_erreurs import *
from APP_FILMS.fonctionalites.gestion_fonctionalite_wtf_forms import FormWTFAjouterFonctionalite
from APP_FILMS.fonctionalites.gestion_fonctionalite_wtf_forms import FormWTFDeleteFonctionalite
from APP_FILMS.fonctionalites.gestion_fonctionalite_wtf_forms import FormWTFUpdateFonctionalite

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /fonctionalite_afficher
    
    Test : ex : http://127.0.0.1:5005/fonctionalite_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_fonctionalite_sel = 0 >> tous les fonctionalites.
                id_fonctionalite_sel = "n" affiche la fonctionalite dont l'id est "n"

"""

@obj_mon_application.route("/fonctionalite_afficher/<string:order_by>/<int:id_fonctionalite_sel>", methods=['GET', 'POST'])
def fonctionalite_afficher(order_by, id_fonctionalite_sel):
    if request.method == "GET":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion fonctionalite ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur GestionFonctionalite {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                if order_by == "ASC" and id_fonctionalite_sel == 0:
                    strsql_fonctionalite_afficher = """SELECT id_fonctionalite, autonomie, portee_drone, poids, taille_diagonale FROM t_fonctionalite ORDER BY id_fonctionalite ASC"""
                    mc_afficher.execute(strsql_fonctionalite_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_fonctionalite"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id de la fonctionalite sélectionné avec un nom de variable
                    valeur_id_fonctionalite_selected_dictionnaire = {"value_id_fonctionalite_selected": id_fonctionalite_sel}
                    strsql_fonctionalite_afficher = """SELECT id_fonctionalite, autonomie, portee_drone, poids, taille_diagonale FROM t_fonctionalite WHERE id_fonctionalite = %(value_id_fonctionalite_selected)s"""

                    mc_afficher.execute(strsql_fonctionalite_afficher, valeur_id_fonctionalite_selected_dictionnaire)
                else:
                    strsql_fonctionalite_afficher = """SELECT id_fonctionalite, autonomie, portee_drone, poids, taille_diagonale FROM t_fonctionalite ORDER BY id_fonctionalite DESC"""

                    mc_afficher.execute(strsql_fonctionalite_afficher)

                data_fonctionalite = mc_afficher.fetchall()

                print("data_fonctionalite ", data_fonctionalite, " Type : ", type(data_fonctionalite))

                # Différencier les messages si la table est vide.
                if not data_fonctionalite and id_fonctionalite_sel == 0:
                    flash("""La table "t_fonctionalite" est vide. !!""", "warning")
                elif not data_fonctionalite and id_fonctionalite_sel > 0:
                    # Si l'utilisateur change l'id_fonctionalite dans l'URL et que le fonctionalite n'existe pas,
                    flash(f"La fonctionalite demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_fonctionalite" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données fonctionalite affichés !!", "success")

        except Exception as erreur:
            print(f"RGG Erreur générale. fonctionalite_afficher")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)"
            # fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            flash(f"RGG Exception {erreur} fonctionalite_afficher", "danger")
            raise Exception(f"RGG Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Envoie la page "HTML" au serveur.
    return render_template("fonctionalite/fonctionalite_afficher.html", data=data_fonctionalite)

"""

    Auteur : OM 2021.03.22
    Définition d'une "route" /fonctionalite_ajouter
    
    Test : ex : http://127.0.0.1:5005/fonctionalite_ajouter
    
    Paramètres : sans
    
    But : Ajouter un fonctionalite pour un film
    
    Remarque :  Dans le champ "name_fonctionalite_html" du formulaire "fonctionalite/fonctionalite_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/fonctionalite_ajouter", methods=['GET', 'POST'])
def fonctionalite_ajouter_wtf():
    form = FormWTFAjouterFonctionalite()
    if request.method == "POST":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion fonctionalite ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur Gestionfonctionalite {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            if form.validate_on_submit():
                name_fonctionalite_wtf = form.nom_fonctionalite_wtf.data
                portee_drone = form.nom_portee_drone_wtf.data
                poids_drone = form.nom_poids_drone_wtf.data
                taille_diagonale = form.nom_diagonale_drone_wtf.data
                name_fonctionalite = name_fonctionalite_wtf.lower()
                valeurs_insertion_dictionnaire = {"value_intitule_fonctionalite": name_fonctionalite, "portee_drone": portee_drone, "poids" : poids_drone, "taille_diagonale" : taille_diagonale}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_fonctionalite = """INSERT INTO t_fonctionalite ( autonomie, portee_drone, poids, taille_diagonale) VALUES (%(value_intitule_fonctionalite)s,%(portee_drone)s,%(poids)s,%(taille_diagonale)s)"""
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(strsql_insert_fonctionalite, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('fonctionalite_afficher', order_by='DESC', id_fonctionalite_sel=0))

        # ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except pymysql.err.IntegrityError as erreur_fonctionalite_doublon:
            # Dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs/exceptions.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            code, msg = erreur_fonctionalite_doublon.args

            flash(f"{error_codes.get(code, msg)} ", "warning")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except (pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                TypeError) as erreur_gest_dron_crud:
            code, msg = erreur_gest_dron_crud.args

            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Erreur dans Gestion fonctionalite CRUD : {sys.exc_info()[0]} "
                  f"{erreur_gest_dron_crud.args[0]} , "
                  f"{erreur_gest_dron_crud}", "danger")

    return render_template("fonctionalite/fonctionalite_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /fonctionalite_update
    
    Test : ex cliquer sur le menu "fonctionalite" puis cliquer sur le bouton "EDIT" d'un "fonctionalite"
    
    Paramètres : sans
    
    But : Editer(update) un fonctionalite qui a été sélectionné dans le formulaire "magasin_afficher.html"
    
    Remarque :  Dans le champ "nom_fonctionalite_update_wtf" du formulaire "fonctionalite/magasin_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/fonctionalite_update", methods=['GET', 'POST'])
def fonctionalite_update_wtf():

    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_fonctionalite"
    id_fonctionalite_update = request.values['id_fonctionalite_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateFonctionalite()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "magasin_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_fonctionalite_update = form_update.nom_fonctionalite_update_wtf.data
            name_fonctionalite_update = name_fonctionalite_update.lower()
            name_portee_update = form_update.nom_portee_update_wtf.data
            name_portee_update = name_portee_update.lower()
            name_poids_update = form_update.nom_portee_update_wtf.data
            name_poids_update = name_poids_update.lower()
            name_diagonale_update = form_update.taille_diagonale_update_wtf.data
            name_diagonale_update = name_diagonale_update.lower()

            valeur_update_dictionnaire = {"value_id_fonctionalite": id_fonctionalite_update, "value_name_fonctionalite": name_fonctionalite_update, "value_portee_drone" : name_portee_update, "value_poids" : name_poids_update, "value_taille_diagonale" : name_diagonale_update}
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulefonctionalite = """UPDATE t_fonctionalite SET  autonomie = %(value_name_fonctionalite)s, portee_drone =  %(value_portee_drone)s , poids = %(value_poids)s, taille_diagonale = %(value_taille_diagonale)s WHERE id_fonctionalite = %(value_id_fonctionalite)s"""
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(str_sql_update_intitulefonctionalite, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_fonctionalite_update"
            return redirect(url_for('fonctionalite_afficher', order_by="ASC", id_fonctionalite_sel=id_fonctionalite_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_fonctionalite" et "intitule_fonctionalite" de la "t_fonctionalite"
            str_sql_id_fonctionalite = "SELECT id_fonctionalite,  autonomie, portee_drone, poids, taille_diagonale  FROM t_fonctionalite WHERE id_fonctionalite = %(value_id_fonctionalite)s"
            valeur_select_dictionnaire = {"value_id_fonctionalite": id_fonctionalite_update}
            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()
            mybd_curseur.execute(str_sql_id_fonctionalite, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom fonctionalite" pour l'UPDATE
            data_nom_fonctionalite = mybd_curseur.fetchone()
            print("data_nom_fonctionalite ", data_nom_fonctionalite, " type ", type(data_nom_fonctionalite), " fonctionalite ", "portee_drone", "poids", "taille_diagonale",
                data_nom_fonctionalite["autonomie"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "magasin_update_wtf.html"
            form_update.nom_fonctionalite_update_wtf.data = data_nom_fonctionalite["autonomie"]
            form_update.nom_portee_update_wtf.data = data_nom_fonctionalite["portee_drone"]
            form_update.nom_poids_update_wtf.data = data_nom_fonctionalite["poids"]
            form_update.taille_diagonale_update_wtf.data = data_nom_fonctionalite["taille_diagonale"]

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans fonctionalite_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans fonctionalite_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_dron_crud:
        code, msg = erreur_gest_dron_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_dron_crud} ", "danger")
        flash(f"Erreur dans fonctionalite_update_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_dron_crud.args[0]} , "
              f"{erreur_gest_dron_crud}", "danger")
        flash(f"__KeyError dans fonctionalite_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("fonctionalite/fonctionalite_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /fonctionalite_delete
    
    Test : ex. cliquer sur le menu "fonctionalite" puis cliquer sur le bouton "DELETE" d'un "fonctionalite"
    
    Paramètres : sans
    
    But : Effacer(delete) un fonctionalite qui a été sélectionné dans le formulaire "magasin_afficher.html"
    
    Remarque :  Dans le champ "nom_fonctionalite_delete_wtf" du formulaire "fonctionalite/magasin_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@obj_mon_application.route("/fonctionalite_delete", methods=['GET', 'POST'])
def fonctionalite_delete_wtf():
    data_films_attribue_fonctionalite_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_fonctionalite"
    id_fonctionalite_delete = request.values['id_fonctionalite_btn_delete_html']

    # Objet formulaire pour effacer le fonctionalite sélectionné.
    form_delete = FormWTFDeleteFonctionalite()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("fonctionalite_afficher", order_by="ASC", id_fonctionalite_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "fonctionalite/magasin_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_fonctionalite_delete = session['data_films_attribue_fonctionalite_delete']
                print("data_films_attribue_fonctionalite_delete ", data_films_attribue_fonctionalite_delete)

                flash(f"Effacer le fonctionalite de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer fonctionalite" qui va irrémédiablement EFFACER la fonctionalite
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_fonctionalite": id_fonctionalite_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_images_fonctionalite = """DELETE FROM t_drone_images WHERE fk_drone = %(value_id_fonctionalite)s"""
                str_sql_delete_idfonctionalite = """DELETE FROM t_fonctionalite WHERE id_fonctionalite = %(value_id_fonctionalite)s"""
                # Manière brutale d'effacer d'abord la "fk_images", même si elle n'existe pas dans la "t_dfonctionalite_film"
                # Ensuite on peut effacer le fonctionalite vu qu'il n'est plus "lié" (INNODB) dans la "t_fonctionalite_film"
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(str_sql_delete_images_fonctionalite, valeur_delete_dictionnaire)
                    mconn_bd.mabd_execute(str_sql_delete_idfonctionalite, valeur_delete_dictionnaire)

                flash(f"fonctionalite définitivement effacée !!", "success")
                print(f"fonctionalite définitivement effacée !!")

                # afficher les données
                return redirect(url_for('fonctionalite_afficher', order_by="ASC", id_fonctionalite_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_fonctionalite": id_fonctionalite_delete}
            print(id_fonctionalite_delete, type(id_fonctionalite_delete))

            # Requête qui affiche tous les films_fonctionalite qui ont le fonctionalite que l'utilisateur veut effacer
            str_sql_fonctionalite_films_delete = """SELECT id_drone_images,  chemin_images, id_drone, nom_drone FROM t_drone_images
                                            INNER JOIN t_drone ON t_drone_images.fk_drone = t_drone.id_drone
                                            INNER JOIN t_images ON t_drone_images.fk_images = t_images.id_images
                                            WHERE fk_images = %(value_id_fonctionalite)s"""

            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()

            mybd_curseur.execute(str_sql_fonctionalite_films_delete, valeur_select_dictionnaire)
            data_films_attribue_fonctionalite_delete = mybd_curseur.fetchall()
            print("data_films_attribue_fonctionalite_delete...", data_films_attribue_fonctionalite_delete)

            # Nécessaire pour mémoriser les données afin d'afficher à nouveau
            # le formulaire "fonctionalite/magasin_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            session['data_films_attribue_fonctionalite_delete'] = data_films_attribue_fonctionalite_delete

            # Opération sur la BD pour récupérer "id_fonctionalite" et "intitule_fonctionalite" de la "t_fonctionalite"
            str_sql_id_fonctionalite = "SELECT id_fonctionalite, autonomie FROM t_fonctionalite WHERE id_fonctionalite = %(value_id_fonctionalite)s"

            mybd_curseur.execute(str_sql_id_fonctionalite, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()",
            # vu qu'il n'y a qu'un seul champ "nom fonctionalite" pour l'action DELETE
            data_nom_fonctionalite = mybd_curseur.fetchone()
            print("data_nom_fonctionalite ", data_nom_fonctionalite, " type ", type(data_nom_fonctionalite), " fonctionalite ",
                  data_nom_fonctionalite["autonomie"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "magasin_delete_wtf.html"
            form_delete.nom_fonctionalite_delete_wtf.data = data_nom_fonctionalite["autonomie"]

            # Le bouton pour l'action "DELETE" dans le form. "magasin_delete_wtf.html" est caché.
            btn_submit_del = False

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans fonctionalite_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans fonctionalite_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_dron_crud:
        code, msg = erreur_gest_dron_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_dron_crud} ", "danger")

        flash(f"Erreur dans fonctionalite_delete_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_dron_crud.args[0]} , "
              f"{erreur_gest_dron_crud}", "danger")

        flash(f"__KeyError dans fonctionalite_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("fonctionalite/fonctionalite_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_fonctionalite_associes=data_films_attribue_fonctionalite_delete)
