"""
    Fichier : gestion_magasin_crud.py
    Auteur : OM 2021.03.16
    Gestions des "routes" FLASK et des données pour les marque.
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
from APP_FILMS.marques.gestion_marque_wtf_forms import FormWTFAjouterMarque
from APP_FILMS.marques.gestion_marque_wtf_forms import FormWTFDeleteMarque
from APP_FILMS.marques.gestion_marque_wtf_forms import FormWTFUpdateMarque

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /marque_afficher
    
    Test : ex : http://127.0.0.1:5005/marque_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_marque_sel = 0 >> tous les marques.
                id_marque_sel = "n" affiche le marque dont l'id est "n"

"""

@obj_mon_application.route("/marque_afficher/<string:order_by>/<int:id_marque_sel>", methods=['GET', 'POST'])
def marque_afficher(order_by, id_marque_sel):
    if request.method == "GET":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion marque ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur GestionMarque {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                if order_by == "ASC" and id_marque_sel == 0:
                    strsql_marque_afficher = """SELECT id_marque, marque FROM t_marque ORDER BY id_marque ASC"""
                    mc_afficher.execute(strsql_marque_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_marque"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du marque sélectionné avec un nom de variable
                    valeur_id_marque_selected_dictionnaire = {"value_id_marque_selected": id_marque_sel}
                    strsql_marque_afficher = """SELECT id_marque, marque FROM t_marque WHERE id_marque = %(value_id_marque_selected)s"""

                    mc_afficher.execute(strsql_marque_afficher, valeur_id_marque_selected_dictionnaire)
                else:
                    strsql_marque_afficher = """SELECT id_marque, marque FROM t_marque ORDER BY id_marque DESC"""

                    mc_afficher.execute(strsql_marque_afficher)

                data_marque = mc_afficher.fetchall()

                print("data_marque ", data_marque, " Type : ", type(data_marque))

                # Différencier les messages si la table est vide.
                if not data_marque and id_marque_sel == 0:
                    flash("""La table "t_marque" est vide. !!""", "warning")
                elif not data_marque and id_marque_sel > 0:
                    # Si l'utilisateur change l'id_marque dans l'URL et que le marque n'existe pas,
                    flash(f"La marque demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_marque" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données marque affichés !!", "success")

        except Exception as erreur:
            print(f"RGG Erreur générale. marque_afficher")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)"
            # fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            flash(f"RGG Exception {erreur} marque_afficher", "danger")
            raise Exception(f"RGG Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Envoie la page "HTML" au serveur.
    return render_template("marque/marque_afficher.html", data=data_marque)

"""

    Auteur : OM 2021.03.22
    Définition d'une "route" /marque_ajouter
    
    Test : ex : http://127.0.0.1:5005/marque_ajouter
    
    Paramètres : sans
    
    But : Ajouter une marque pour un film
    
    Remarque :  Dans le champ "name_marque_html" du formulaire "marque/marque_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/marque_ajouter", methods=['GET', 'POST'])
def marque_ajouter_wtf():
    form = FormWTFAjouterMarque()
    if request.method == "POST":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion marque ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur Gestionmarque {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            if form.validate_on_submit():
                name_marque_wtf = form.nom_marque_wtf.data
                name_marque = name_marque_wtf.lower()
                valeurs_insertion_dictionnaire = {"value_intitule_marque": name_marque}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_marque = """INSERT INTO t_marque (id_marque, marque) VALUES (NULL,%(value_intitule_marque)s)"""
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(strsql_insert_marque, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('marque_afficher', order_by='DESC', id_marque_sel=0))

        # ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except pymysql.err.IntegrityError as erreur_marque_doublon:
            # Dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs/exceptions.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            code, msg = erreur_marque_doublon.args

            flash(f"{error_codes.get(code, msg)} ", "warning")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except (pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                TypeError) as erreur_gest_dron_crud:
            code, msg = erreur_gest_dron_crud.args

            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Erreur dans Gestion marque CRUD : {sys.exc_info()[0]} "
                  f"{erreur_gest_dron_crud.args[0]} , "
                  f"{erreur_gest_dron_crud}", "danger")

    return render_template("marque/marque_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /marque_update
    
    Test : ex cliquer sur le menu "marque" puis cliquer sur le bouton "EDIT" d'un "marque"
    
    Paramètres : sans
    
    But : Editer(update) un marque qui a été sélectionné dans le formulaire "magasin_afficher.html"
    
    Remarque :  Dans le champ "nom_marque_update_wtf" du formulaire "marque/magasin_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/marque_update", methods=['GET', 'POST'])
def marque_update_wtf():

    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_marque"
    id_marque_update = request.values['id_marque_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateMarque()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "magasin_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_marque_update = form_update.nom_marque_update_wtf.data
            name_marque_update = name_marque_update.lower()


            valeur_update_dictionnaire = {"value_id_marque": id_marque_update, "value_name_marque": name_marque_update}
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulemarque = """UPDATE t_marque SET  marque = %(value_name_marque)s WHERE id_marque = %(value_id_marque)s"""
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(str_sql_update_intitulemarque, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_marque_update"
            return redirect(url_for('marque_afficher', order_by="ASC", id_marque_sel=id_marque_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_marque" et "intitule_marque" de la "t_marque"
            str_sql_id_marque = "SELECT id_marque, marque FROM t_marque WHERE id_marque = %(value_id_marque)s"
            valeur_select_dictionnaire = {"value_id_marque": id_marque_update}
            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()
            mybd_curseur.execute(str_sql_id_marque, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom marque" pour l'UPDATE
            data_nom_marque = mybd_curseur.fetchone()
            print("data_nom_marque ", data_nom_marque, " type ", type(data_nom_marque), " marque ",
                  data_nom_marque["marque"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "magasin_update_wtf.html"
            form_update.nom_marque_update_wtf.data = data_nom_marque["marque"]
    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans marque_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans marque_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_dron_crud:
        code, msg = erreur_gest_dron_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_dron_crud} ", "danger")
        flash(f"Erreur dans marque_update_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_dron_crud.args[0]} , "
              f"{erreur_gest_dron_crud}", "danger")
        flash(f"__KeyError dans marque_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("marque/marque_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /marque_delete
    
    Test : ex. cliquer sur le menu "marque" puis cliquer sur le bouton "DELETE" d'un "marque"
    
    Paramètres : sans
    
    But : Effacer(delete) un marque qui a été sélectionné dans le formulaire "magasin_afficher.html"
    
    Remarque :  Dans le champ "nom_marque_delete_wtf" du formulaire "marque/magasin_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@obj_mon_application.route("/marque_delete", methods=['GET', 'POST'])
def marque_delete_wtf():
    data_films_attribue_marque_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_marque"
    id_marque_delete = request.values['id_marque_btn_delete_html']

    # Objet formulaire pour effacer le marque sélectionné.
    form_delete = FormWTFDeleteMarque()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("marque_afficher", order_by="ASC", id_marque_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "marque/magasin_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_marque_delete = session['data_films_attribue_marque_delete']
                print("data_films_attribue_marque_delete ", data_films_attribue_marque_delete)

                flash(f"Effacer le marque de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer marque" qui va irrémédiablement EFFACER le marque
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_marque": id_marque_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_images_marque = """DELETE FROM t_drone_images WHERE fk_drone = %(value_id_marque)s"""
                str_sql_delete_idmarque = """DELETE FROM t_marque WHERE id_marque = %(value_id_marque)s"""
                # Manière brutale d'effacer d'abord la "fk_images", même si elle n'existe pas dans la "t_marque_film"
                # Ensuite on peut effacer le marque vu qu'il n'est plus "lié" (INNODB) dans la "t_marque_film"
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(str_sql_delete_images_marque, valeur_delete_dictionnaire)
                    mconn_bd.mabd_execute(str_sql_delete_idmarque, valeur_delete_dictionnaire)

                flash(f"marque définitivement effacée !!", "success")
                print(f"marque définitivement effacée !!")

                # afficher les données
                return redirect(url_for('marque_afficher', order_by="ASC", id_marque_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_marque": id_marque_delete}
            print(id_marque_delete, type(id_marque_delete))

            # Requête qui affiche tous les films_marque qui ont le marque que l'utilisateur veut effacer
            str_sql_marque_films_delete = """SELECT id_drone_images,  chemin_images, id_drone, nom_drone FROM t_drone_images
                                            INNER JOIN t_drone ON t_drone_images.fk_drone = t_drone.id_drone
                                            INNER JOIN t_images ON t_drone_images.fk_images = t_images.id_images
                                            WHERE fk_images  = %(value_id_marque)s"""

            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()

            mybd_curseur.execute(str_sql_marque_films_delete, valeur_select_dictionnaire)
            data_films_attribue_marque_delete = mybd_curseur.fetchall()
            print("data_films_attribue_marque_delete...", data_films_attribue_marque_delete)

            # Nécessaire pour mémoriser les données afin d'afficher à nouveau
            # le formulaire "marque/magasin_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            session['data_films_attribue_marque_delete'] = data_films_attribue_marque_delete

            # Opération sur la BD pour récupérer "id_marque" et "intitule_marque" de la "t_marque"
            str_sql_id_marque = "SELECT id_marque, marque FROM t_marque WHERE id_marque = %(value_id_marque)s"

            mybd_curseur.execute(str_sql_id_marque, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()",
            # vu qu'il n'y a qu'un seul champ "nom marque" pour l'action DELETE
            data_nom_marque = mybd_curseur.fetchone()
            print("data_nom_marque ", data_nom_marque, " type ", type(data_nom_marque), " marque ",
                  data_nom_marque["marque"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "magasin_delete_wtf.html"
            form_delete.nom_marque_delete_wtf.data = data_nom_marque["marque"]

            # Le bouton pour l'action "DELETE" dans le form. "magasin_delete_wtf.html" est caché.
            btn_submit_del = False

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans marque_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans marque_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_dron_crud:
        code, msg = erreur_gest_dron_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_dron_crud} ", "danger")

        flash(f"Erreur dans marque_delete_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_dron_crud.args[0]} , "
              f"{erreur_gest_dron_crud}", "danger")

        flash(f"__KeyError dans marque_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("marque/marque_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_marque_associes=data_films_attribue_marque_delete)
