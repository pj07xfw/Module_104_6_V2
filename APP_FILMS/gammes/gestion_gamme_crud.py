"""
    Fichier : gestion_magasin_crud.py
    Auteur : OM 2021.03.16
    Gestions des "routes" FLASK et des données pour les gamme.
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
from APP_FILMS.gammes.gestion_gamme_wtf_forms import FormWTFAjouterGamme
from APP_FILMS.gammes.gestion_gamme_wtf_forms import FormWTFDeleteGamme
from APP_FILMS.gammes.gestion_gamme_wtf_forms import FormWTFUpdateGamme

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /gamme_afficher
    
    Test : ex : http://127.0.0.1:5005/gamme_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_gamme_sel = 0 >> tous les gammes.
                id_gamme_sel = "n" affiche le gamme dont l'id est "n"

"""

@obj_mon_application.route("/gamme_afficher/<string:order_by>/<int:id_gamme_sel>", methods=['GET', 'POST'])
def gamme_afficher(order_by, id_gamme_sel):
    if request.method == "GET":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion gamme ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur GestionGamme {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                if order_by == "ASC" and id_gamme_sel == 0:
                    strsql_gamme_afficher = """SELECT id_gamme, nom_gamme FROM t_gamme ORDER BY id_gamme ASC"""
                    mc_afficher.execute(strsql_gamme_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_gamme"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du gamme sélectionné avec un nom de variable
                    valeur_id_gamme_selected_dictionnaire = {"value_id_gamme_selected": id_gamme_sel}
                    strsql_gamme_afficher = """SELECT id_gamme, nom_gamme FROM t_gamme WHERE id_gamme = %(value_id_gamme_selected)s"""

                    mc_afficher.execute(strsql_gamme_afficher, valeur_id_gamme_selected_dictionnaire)
                else:
                    strsql_gamme_afficher = """SELECT id_gamme, nom_gamme FROM t_gamme ORDER BY id_gamme DESC"""

                    mc_afficher.execute(strsql_gamme_afficher)

                data_gamme = mc_afficher.fetchall()

                print("data_gamme ", data_gamme, " Type : ", type(data_gamme))

                # Différencier les messages si la table est vide.
                if not data_gamme and id_gamme_sel == 0:
                    flash("""La table "t_gamme" est vide. !!""", "warning")
                elif not data_gamme and id_gamme_sel > 0:
                    # Si l'utilisateur change l'id_gamme dans l'URL et que la gamme n'existe pas,
                    flash(f"La gamme demandée n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_gamme" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données gamme affichés !!", "success")

        except Exception as erreur:
            print(f"RGG Erreur générale. gamme_afficher")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)"
            # fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            flash(f"RGG Exception {erreur} gamme_afficher", "danger")
            raise Exception(f"RGG Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Envoie la page "HTML" au serveur.
    return render_template("gamme/gamme_afficher.html", data=data_gamme)

"""

    Auteur : OM 2021.03.22
    Définition d'une "route" /gamme_ajouter
    
    Test : ex : http://127.0.0.1:5005/gamme_ajouter
    
    Paramètres : sans
    
    But : Ajouter une gamme pour un film
    
    Remarque :  Dans le champ "name_gamme_html" du formulaire "gamme/gamme_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/gamme_ajouter", methods=['GET', 'POST'])
def gamme_ajouter_wtf():
    form = FormWTFAjouterGamme()
    if request.method == "POST":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion gamme ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur Gestiongamme {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            if form.validate_on_submit():
                name_gamme_wtf = form.nom_gamme_wtf.data

                name_gamme = name_gamme_wtf.lower()
                valeurs_insertion_dictionnaire = {"value_intitule_gamme": name_gamme}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_gamme = """INSERT INTO t_gamme (id_gamme, nom_gamme) VALUES (NULL,%(value_intitule_gamme)s)"""
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(strsql_insert_gamme, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('gamme_afficher', order_by='DESC', id_gamme_sel=0))

        # ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except pymysql.err.IntegrityError as erreur_gamme_doublon:
            # Dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs/exceptions.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            code, msg = erreur_gamme_doublon.args

            flash(f"{error_codes.get(code, msg)} ", "warning")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except (pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                TypeError) as erreur_gest_dron_crud:
            code, msg = erreur_gest_dron_crud.args

            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Erreur dans Gestion gamme CRUD : {sys.exc_info()[0]} "
                  f"{erreur_gest_dron_crud.args[0]} , "
                  f"{erreur_gest_dron_crud}", "danger")

    return render_template("gamme/gamme_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /gamme_update
    
    Test : ex cliquer sur le menu "gamme" puis cliquer sur le bouton "EDIT" d'une "gamme"
    
    Paramètres : sans
    
    But : Editer(update) une gamme qui a été sélectionné dans le formulaire "magasin_afficher.html"
    
    Remarque :  Dans le champ "nom_gamme_update_wtf" du formulaire "gamme/magasin_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/gamme update", methods=['GET', 'POST'])
def gamme_update_wtf():

    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_gamme"
    id_gamme_update = request.values['id_gamme_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateGamme()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "magasin_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_gamme_update = form_update.nom_gamme_update_wtf.data
            name_gamme_update = name_gamme_update.lower()

            valeur_update_dictionnaire = {"value_id_gamme": id_gamme_update, "value_name_gamme": name_gamme_update}
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegamme = """UPDATE t_gamme SET  nom_gamme = %(value_name_gamme)s WHERE id_gamme = %(value_id_gamme)s"""
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(str_sql_update_intitulegamme, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_gamme_update"
            return redirect(url_for('gamme_afficher', order_by="ASC", id_gamme_sel=id_gamme_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_gamme" et "intitule_gamme" de la "t_gamme"
            str_sql_id_gamme = "SELECT id_gamme,  nom_gamme FROM t_gamme WHERE id_gamme = %(value_id_gamme)s"
            valeur_select_dictionnaire = {"value_id_gamme": id_gamme_update}
            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()
            mybd_curseur.execute(str_sql_id_gamme, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom gamme" pour l'UPDATE
            data_nom_gamme = mybd_curseur.fetchone()
            print("data_nom_gamme ", data_nom_gamme, " type ", type(data_nom_gamme), " gamme ",
                  data_nom_gamme["nom_gamme"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "magasin_update_wtf.html"
            form_update.nom_gamme_update_wtf.data = data_nom_gamme["nom_gamme"]

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans gamme_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans gamme_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_dron_crud:
        code, msg = erreur_gest_dron_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_dron_crud} ", "danger")
        flash(f"Erreur dans gamme_update_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_dron_crud.args[0]} , "
              f"{erreur_gest_dron_crud}", "danger")
        flash(f"__KeyError dans gamme_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("gamme/gamme_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /gamme_delete
    
    Test : ex. cliquer sur le menu "gamme" puis cliquer sur le bouton "DELETE" d'un "gamme"
    
    Paramètres : sans
    
    But : Effacer(delete) un gamme qui a été sélectionné dans le formulaire "magasin_afficher.html"
    
    Remarque :  Dans le champ "nom_gamme_delete_wtf" du formulaire "gamme/magasin_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@obj_mon_application.route("/gamme_delete", methods=['GET', 'POST'])
def gamme_delete_wtf():
    data_films_attribue_gamme_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_gamme"
    id_gamme_delete = request.values['id_gamme_btn_delete_html']

    # Objet formulaire pour effacer le gamme sélectionné.
    form_delete = FormWTFDeleteGamme()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("gamme_afficher", order_by="ASC", id_gamme_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "gamme/magasin_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_gamme_delete = session['data_films_attribue_gamme_delete']
                print("data_films_attribue_gamme_delete ", data_films_attribue_gamme_delete)

                flash(f"Effacer le gamme de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer gamme" qui va irrémédiablement EFFACER le gamme
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_gamme": id_gamme_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_images_gamme = """DELETE FROM t_drone_images WHERE fk_drone = %(value_id_gamme)s"""
                str_sql_delete_idgamme = """DELETE FROM t_gamme WHERE id_gamme = %(value_id_gamme)s"""
                # Manière brutale d'effacer d'abord la "fk_images", même si elle n'existe pas dans la "t_gamme_film"
                # Ensuite on peut effacer la gamme vu qu'il n'est plus "lié" (INNODB) dans la "t_gamme_film"
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(str_sql_delete_images_gamme, valeur_delete_dictionnaire)
                    mconn_bd.mabd_execute(str_sql_delete_idgamme, valeur_delete_dictionnaire)

                flash(f"gamme définitivement effacée !!", "success")
                print(f"gamme définitivement effacée !!")

                # afficher les données
                return redirect(url_for('gamme_afficher', order_by="ASC", id_gamme_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_gamme": id_gamme_delete}
            print(id_gamme_delete, type(id_gamme_delete))

            # Requête qui affiche tous les films_gamme qui ont la gamme que l'utilisateur veut effacer
            str_sql_gamme_films_delete = """SELECT id_drone_images,  chemin_images, id_drone, nom_drone FROM t_drone_images
                                            INNER JOIN t_drone ON t_drone_images.fk_drone = t_drone.id_drone
                                            INNER JOIN t_images ON t_drone_images.fk_images = t_images.id_images
                                            WHERE fk_images = %(value_id_gamme)s"""

            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()

            mybd_curseur.execute(str_sql_gamme_films_delete, valeur_select_dictionnaire)
            data_films_attribue_gamme_delete = mybd_curseur.fetchall()
            print("data_films_attribue_gamme_delete...", data_films_attribue_gamme_delete)

            # Nécessaire pour mémoriser les données afin d'afficher à nouveau
            # le formulaire "gamme/magasin_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            session['data_films_attribue_gamme_delete'] = data_films_attribue_gamme_delete

            # Opération sur la BD pour récupérer "id_gamme" et "intitule_gamme" de la "t_gamme"
            str_sql_id_gamme = "SELECT id_gamme, nom_gamme FROM t_gamme WHERE id_gamme = %(value_id_gamme)s"

            mybd_curseur.execute(str_sql_id_gamme, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()",
            # vu qu'il n'y a qu'un seul champ "nom gamme" pour l'action DELETE
            data_nom_gamme = mybd_curseur.fetchone()
            print("data_nom_gamme ", data_nom_gamme, " type ", type(data_nom_gamme), " gamme ",
                  data_nom_gamme["nom_gamme"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "magasin_delete_wtf.html"
            form_delete.nom_gamme_delete_wtf.data = data_nom_gamme["nom_gamme"]

            # Le bouton pour l'action "DELETE" dans le form. "magasin_delete_wtf.html" est caché.
            btn_submit_del = False

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans gamme_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans gamme_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_dron_crud:
        code, msg = erreur_gest_dron_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_dron_crud} ", "danger")

        flash(f"Erreur dans gamme_delete_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_dron_crud.args[0]} , "
              f"{erreur_gest_dron_crud}", "danger")

        flash(f"__KeyError dans gamme_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("gamme/gamme_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_gamme_associes=data_films_attribue_gamme_delete)
