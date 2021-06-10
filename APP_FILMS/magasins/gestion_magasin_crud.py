"""
    Fichier : gestion_magasin_crud.py
    Auteur : OM 2021.03.16
    Gestions des "routes" FLASK et des données pour les magasin.
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
from APP_FILMS.magasins.gestion_magasin_wtf_forms import FormWTFAjouterMagasin
from APP_FILMS.magasins.gestion_magasin_wtf_forms import FormWTFDeleteMagasin
from APP_FILMS.magasins.gestion_magasin_wtf_forms import FormWTFUpdateMagasin

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /magasin_afficher
    
    Test : ex : http://127.0.0.1:5005/magasin_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_magasin_sel = 0 >> tous les magasins.
                id_magasin_sel = "n" affiche le magasin dont l'id est "n"

"""

@obj_mon_application.route("/magasin_afficher/<string:order_by>/<int:id_magasin_sel>", methods=['GET', 'POST'])
def magasin_afficher(order_by, id_magasin_sel):
    if request.method == "GET":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion magasin ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur GestionMagasin {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                if order_by == "ASC" and id_magasin_sel == 0:
                    strsql_magasin_afficher = """SELECT id_magasin, nom_magasin, prix,reduction FROM t_magasin ORDER BY id_magasin ASC"""
                    mc_afficher.execute(strsql_magasin_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_magasin"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du magasin sélectionné avec un nom de variable
                    valeur_id_magasin_selected_dictionnaire = {"value_id_magasin_selected": id_magasin_sel}
                    strsql_magasin_afficher = """SELECT id_magasin, nom_magasin, prix,reduction FROM t_magasin WHERE id_magasin = %(value_id_magasin_selected)s"""

                    mc_afficher.execute(strsql_magasin_afficher, valeur_id_magasin_selected_dictionnaire)
                else:
                    strsql_magasin_afficher = """SELECT id_magasin, nom_magasin, prix,reduction FROM t_magasin ORDER BY id_magasin DESC"""

                    mc_afficher.execute(strsql_magasin_afficher)

                data_magasin = mc_afficher.fetchall()

                print("data_magasin ", data_magasin, " Type : ", type(data_magasin))

                # Différencier les messages si la table est vide.
                if not data_magasin and id_magasin_sel == 0:
                    flash("""La table "t_magasin" est vide. !!""", "warning")
                elif not data_magasin and id_magasin_sel > 0:
                    # Si l'utilisateur change l'id_magasin dans l'URL et que le magasin n'existe pas,
                    flash(f"Le magasin demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_magasin" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données magasin affichés !!", "success")

        except Exception as erreur:
            print(f"RGG Erreur générale. magasin_afficher")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)"
            # fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            flash(f"RGG Exception {erreur} magasin_afficher", "danger")
            raise Exception(f"RGG Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Envoie la page "HTML" au serveur.
    return render_template("magasin/magasin_afficher.html", data=data_magasin)

"""

    Auteur : OM 2021.03.22
    Définition d'une "route" /magasin_ajouter
    
    Test : ex : http://127.0.0.1:5005/magasin_ajouter
    
    Paramètres : sans
    
    But : Ajouter un magasin pour un magasin
    
    Remarque :  Dans le champ "name_magasin_html" du formulaire "magasin/magasin_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/magasin_ajouter", methods=['GET', 'POST'])
def magasin_ajouter_wtf():
    form = FormWTFAjouterMagasin()
    if request.method == "POST":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion magasin ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur GestionMagasin {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            if form.validate_on_submit():
                name_magasin_wtf = form.nom_magasin_wtf.data
                prix = form.nom_prix_drone_wtf.data
                reduction = form.nom_reduction_drone_wtf.data
                name_magasin = name_magasin_wtf.lower()
                valeurs_insertion_dictionnaire = {"value_intitule_magasin": name_magasin, "prix" : prix, "reduction" : reduction }
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_magasin = """INSERT INTO t_magasin (id_magasin, nom_magasin, prix,reduction) VALUES (NULL,%(value_intitule_magasin)s,%(prix)s,%(reduction)s)"""
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(strsql_insert_magasin, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('magasin_afficher', order_by='DESC', id_magasin_sel=0))

        # ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except pymysql.err.IntegrityError as erreur_magasin_doublon:
            # Dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs/exceptions.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            code, msg = erreur_magasin_doublon.args

            flash(f"{error_codes.get(code, msg)} ", "warning")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except (pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                TypeError) as erreur_gest_dron_crud:
            code, msg = erreur_gest_dron_crud.args

            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Erreur dans Gestion magasin CRUD : {sys.exc_info()[0]} "
                  f"{erreur_gest_dron_crud.args[0]} , "
                  f"{erreur_gest_dron_crud}", "danger")

    return render_template("magasin/magasin_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /magasin_update
    
    Test : ex cliquer sur le menu "magasin" puis cliquer sur le bouton "EDIT" d'un "magasin"
    
    Paramètres : sans
    
    But : Editer(update) un magasin qui a été sélectionné dans le formulaire "magasin_afficher.html"
    
    Remarque :  Dans le champ "nom_magasin_update_wtf" du formulaire "magasin/magasin_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/magasin_update", methods=['GET', 'POST'])
def magasin_update_wtf():

    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_magasin"
    id_magasin_update = request.values['id_magasin_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateMagasin()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "magasin_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_magasin_update = form_update.nom_magasin_update_wtf.data
            name_magasin_update = name_magasin_update.lower()
            name_prix_update = form_update.nom_prix_drone_update_wtf.data
            name_prix_update = name_prix_update.lower()
            name_reduction_update = form_update.nom_reduction_drone_update_wtf.data
            name_reduction_update = name_reduction_update.lower()

            valeur_update_dictionnaire = {"value_id_magasin": id_magasin_update, "value_name_magasin": name_magasin_update, "value_prix" : name_prix_update, "value_reduction" : name_reduction_update}
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulemagasin = """UPDATE t_magasin SET  nom_magasin = %(value_name_magasin)s, prix = %(value_prix)s, reduction = %(value_reduction)s WHERE id_magasin = %(value_id_magasin)s"""
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(str_sql_update_intitulemagasin, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_magasin_update"
            return redirect(url_for('magasin_afficher', order_by="ASC", id_magasin_sel=id_magasin_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_magasin" et "intitule_magasin" de la "t_magasin"
            str_sql_id_magasin = "SELECT id_magasin,  nom_magasin, prix,reduction FROM t_magasin WHERE id_magasin = %(value_id_magasin)s"
            valeur_select_dictionnaire = {"value_id_magasin": id_magasin_update}
            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()
            mybd_curseur.execute(str_sql_id_magasin, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom magasin" pour l'UPDATE
            data_nom_magasin = mybd_curseur.fetchone()
            print("data_nom_magasin ", data_nom_magasin, " type ", type(data_nom_magasin), " magasin ", "prix", "reduction",
                  data_nom_magasin["nom_magasin"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "magasin_update_wtf.html"
            form_update.nom_magasin_update_wtf.data = data_nom_magasin["nom_magasin"]
            form_update.nom_prix_drone_update_wtf.data = data_nom_magasin["prix"]
            form_update.nom_reduction_drone_update_wtf.data = data_nom_magasin["reduction"]

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans magasin_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans magasin_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_dron_crud:
        code, msg = erreur_gest_dron_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_dron_crud} ", "danger")
        flash(f"Erreur dans magasin_update_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_dron_crud.args[0]} , "
              f"{erreur_gest_dron_crud}", "danger")
        flash(f"__KeyError dans magasin_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("magasin/magasin_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /magasin_delete
    
    Test : ex. cliquer sur le menu "magasin" puis cliquer sur le bouton "DELETE" d'un "magasin"
    
    Paramètres : sans
    
    But : Effacer(delete) un magasin qui a été sélectionné dans le formulaire "magasin_afficher.html"
    
    Remarque :  Dans le champ "nom_magasin_delete_wtf" du formulaire "magasin/magasin_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@obj_mon_application.route("/magasin_delete", methods=['GET', 'POST'])
def magasin_delete_wtf():
    data_films_attribue_magasin_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_magasin"
    id_magasin_delete = request.values['id_magasin_btn_delete_html']

    # Objet formulaire pour effacer le magasin sélectionné.
    form_delete = FormWTFDeleteMagasin()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("magasin_afficher", order_by="ASC", id_magasin_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "magasin/magasin_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_magasin_delete = session['data_films_attribue_magasin_delete']
                print("data_films_attribue_magasin_delete ", data_films_attribue_magasin_delete)

                flash(f"Effacer le magasin de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer magasin" qui va irrémédiablement EFFACER le magasin
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_magasin": id_magasin_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_images_magasin = """DELETE FROM t_drone_images WHERE fk_drone = %(value_id_magasin)s"""
                str_sql_delete_idmagasin = """DELETE FROM t_magasin WHERE id_magasin = %(value_id_magasin)s"""
                # Manière brutale d'effacer d'abord la "fk_images", même si elle n'existe pas dans la "t_magasin_film"
                # Ensuite on peut effacer le magasin vu qu'il n'est plus "lié" (INNODB) dans la "t_magasin_film"
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(str_sql_delete_images_magasin, valeur_delete_dictionnaire)
                    mconn_bd.mabd_execute(str_sql_delete_idmagasin, valeur_delete_dictionnaire)

                flash(f"magasin définitivement effacé !!", "success")
                print(f"magasin définitivement effacé !!")

                # afficher les données
                return redirect(url_for('magasin_afficher', order_by="ASC", id_magasin_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_magasin": id_magasin_delete}
            print(id_magasin_delete, type(id_magasin_delete))

            # Requête qui affiche tous les films_magasin qui ont le magasin que l'utilisateur veut effacer
            str_sql_magasin_films_delete = """SELECT id_drone_images,  chemin_images, id_drone, nom_drone FROM t_drone_images
                                            INNER JOIN t_drone ON t_drone_images.fk_drone = t_drone.id_drone
                                            INNER JOIN t_images ON t_drone_images.fk_images = t_images.id_images
                                            WHERE fk_images = %(value_id_magasin)s"""

            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()

            mybd_curseur.execute(str_sql_magasin_films_delete, valeur_select_dictionnaire)
            data_films_attribue_magasin_delete = mybd_curseur.fetchall()
            print("data_films_attribue_magasin_delete...", data_films_attribue_magasin_delete)

            # Nécessaire pour mémoriser les données afin d'afficher à nouveau
            # le formulaire "magasin/magasin_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            session['data_films_attribue_magasin_delete'] = data_films_attribue_magasin_delete

            # Opération sur la BD pour récupérer "id_magasin" et "intitule_magasin" de la "t_magasin"
            str_sql_id_magasin = "SELECT id_magasin, nom_magasin FROM t_magasin WHERE id_magasin = %(value_id_magasin)s"

            mybd_curseur.execute(str_sql_id_magasin, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()",
            # vu qu'il n'y a qu'un seul champ "nom magasin" pour l'action DELETE
            data_nom_magasin = mybd_curseur.fetchone()
            print("data_nom_magasin ", data_nom_magasin, " type ", type(data_nom_magasin), " magasin ",
                  data_nom_magasin["nom_magasin"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "magasin_delete_wtf.html"
            form_delete.nom_magasin_delete_wtf.data = data_nom_magasin["nom_magasin"]

            # Le bouton pour l'action "DELETE" dans le form. "magasin_delete_wtf.html" est caché.
            btn_submit_del = False

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans magasin_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans magasin_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_dron_crud:
        code, msg = erreur_gest_dron_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_dron_crud} ", "danger")

        flash(f"Erreur dans magasin_delete_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_dron_crud.args[0]} , "
              f"{erreur_gest_dron_crud}", "danger")

        flash(f"__KeyError dans magasin_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("magasin/magasin_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_magasin_associes=data_films_attribue_magasin_delete)
