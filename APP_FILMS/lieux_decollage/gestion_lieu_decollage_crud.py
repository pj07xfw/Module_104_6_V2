"""
    Fichier : gestion_lieu_decollage_crud.py
    Auteur : OM 2021.03.16
    Gestions des "routes" FLASK et des données pour les lieux.
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
from APP_FILMS.lieux_decollage.gestion_lieu_decollage_wtf_forms import FormWTFAjouterLieu
from APP_FILMS.lieux_decollage.gestion_lieu_decollage_wtf_forms import FormWTFDeleteLieu
from APP_FILMS.lieux_decollage.gestion_lieu_decollage_wtf_forms import FormWTFUpdateLieu

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /lieu_afficher
    
    Test : ex : http://127.0.0.1:5005/lieu_decollage_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_lieu_sel = 0 >> tous les lieux.
                id_lieu_sel = "n" affiche le lieu dont l'id est "n"

"""

@obj_mon_application.route("/lieu_decollage_afficher/<string:order_by>/<int:id_lieu_sel>", methods=['GET', 'POST'])
def lieu_decollage_afficher(order_by, id_lieu_sel):
    if request.method == "GET":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion lieu_decollage ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur Gestion Lieu_decollage {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                if order_by == "ASC" and id_lieu_sel == 0:
                    strsql_lieu_afficher = """SELECT id_lieu_decollage, lieu FROM t_lieu_decollage ORDER BY id_lieu_decollage ASC"""
                    mc_afficher.execute(strsql_lieu_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_lieu_decollage"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du lieu sélectionné avec un nom de variable
                    valeur_id_lieu_selected_dictionnaire = {"value_id_lieu_selected": id_lieu_sel}
                    strsql_lieu_afficher = """SELECT id_lieu_decollage, lieu FROM t_lieu_decollage WHERE id_lieu_decollage = %(value_id_lieu_selected)s"""

                    mc_afficher.execute(strsql_lieu_afficher, valeur_id_lieu_selected_dictionnaire)
                else:
                    strsql_lieu_afficher = """SELECT id_lieu_decollage, lieu FROM t_lieu_decollage ORDER BY id_lieu_decollage DESC"""

                    mc_afficher.execute(strsql_lieu_afficher)

                data_lieu = mc_afficher.fetchall()

                print("data_lieu ", data_lieu, " Type : ", type(data_lieu))

                # Différencier les messages si la table est vide.
                if not data_lieu and id_lieu_sel == 0:
                    flash("""La table "t_lieu_decollage" est vide. !!""", "warning")
                elif not data_lieu and id_lieu_sel > 0:
                    # Si l'utilisateur change l'id_lieu_decollage dans l'URL et que le lieu n'existe pas,
                    flash(f"Le lieu demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_lieu_decollage" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données lieu affichés !!", "success")

        except Exception as erreur:
            print(f"RGG Erreur générale. lieu_decollage_afficher")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)"
            # fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            flash(f"RGG Exception {erreur} lieu_decollage_afficher", "danger")
            raise Exception(f"RGG Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Envoie la page "HTML" au serveur.
    return render_template("lieu_decollage/lieu_decollage_afficher.html", data=data_lieu)

"""

    Auteur : OM 2021.03.22
    Définition d'une "route" /lieu_decollage_ajouter
    
    Test : ex : http://127.0.0.1:5005/lieu_decollage_ajouter
    
    Paramètres : sans
    
    But : Ajouter un lieu pour un film
    
    Remarque :  Dans le champ "name_lieu_html" du formulaire "lieu_decollage/lieu_decollage_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/lieu_decollage_ajouter", methods=['GET', 'POST'])
def lieu_decollage_ajouter_wtf():
    form = FormWTFAjouterLieu()
    if request.method == "POST":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion lieu_decollage ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur Gestion lieu_decollage {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            if form.validate_on_submit():
                name_lieu_wtf = form.nom_lieu_wtf.data

                name_lieu = name_lieu_wtf.lower()
                valeurs_insertion_dictionnaire = {"value_lieu": name_lieu}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_lieu = """INSERT INTO t_lieu_decollage (id_lieu_decollage, lieu) VALUES (NULL,%(value_lieu)s)"""
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(strsql_insert_lieu, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('lieu_decollage_afficher', order_by='DESC', id_lieu_sel=0))

        # ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except pymysql.err.IntegrityError as erreur_lieu_doublon:
            # Dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs/exceptions.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            code, msg = erreur_lieu_doublon.args

            flash(f"{error_codes.get(code, msg)} ", "warning")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except (pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                TypeError) as erreur_gest_dron_crud:
            code, msg = erreur_gest_dron_crud.args

            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Erreur dans Gestion lieu_decollage CRUD : {sys.exc_info()[0]} "
                  f"{erreur_gest_dron_crud.args[0]} , "
                  f"{erreur_gest_dron_crud}", "danger")

    return render_template("lieu_decollage/lieu_decollage_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /lieu_decollage_update
    
    Test : ex cliquer sur le menu "lieu" puis cliquer sur le bouton "EDIT" d'un "lieu"
    
    Paramètres : sans
    
    But : Editer(update) un lieu qui a été sélectionné dans le formulaire "magasin_afficher.html"
    
    Remarque :  Dans le champ "nom_lieu_update_wtf" du formulaire "lieu_decollage/lieu_decollage_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/lieu_decollage_update", methods=['GET', 'POST'])
def lieu_decollage_update_wtf():

    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_lieu_decollage"
    id_lieu_update = request.values['id_lieu_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateLieu()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "magasin_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_lieu_update = form_update.nom_lieu_update_wtf.data
            name_lieu_update = name_lieu_update.lower()

            valeur_update_dictionnaire = {"value_id_lieu_decollage": id_lieu_update, "value_name_lieu": name_lieu_update}
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulelieu = """UPDATE t_lieu_decollage SET  lieu = %(value_name_lieu)s WHERE id_lieu_decollage = %(value_id_lieu_decollage)s"""
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(str_sql_update_intitulelieu, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_lieu_update"
            return redirect(url_for('lieu_decollage_afficher', order_by="ASC", id_lieu_sel=id_lieu_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_lieu" et "intitule_lieu" de la "t_lieu"
            str_sql_id_lieu_decollage = "SELECT id_lieu_decollage,  lieu FROM t_lieu_decollage WHERE id_lieu_decollage = %(value_id_lieu_decollage)s"
            valeur_select_dictionnaire = {"value_id_lieu_decollage": id_lieu_update}
            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()
            mybd_curseur.execute(str_sql_id_lieu_decollage, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom lieu" pour l'UPDATE
            data_nom_lieu = mybd_curseur.fetchone()
            print("data_lieu ", data_nom_lieu, " type ", type(data_nom_lieu), " lieu ",
                  data_nom_lieu["lieu"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "magasin_update_wtf.html"
            form_update.nom_lieu_update_wtf.data = data_nom_lieu["lieu"]

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans lieu_decollage_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans lieu_decollage_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_dron_crud:
        code, msg = erreur_gest_dron_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_dron_crud} ", "danger")
        flash(f"Erreur dans lieu_update_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_dron_crud.args[0]} , "
              f"{erreur_gest_dron_crud}", "danger")
        flash(f"__KeyError dans lieu_decollage_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("lieu_decollage/lieu_decollage_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /lieu_decollage_delete
    
    Test : ex. cliquer sur le menu "lieu" puis cliquer sur le bouton "DELETE" d'un "lieu"
    
    Paramètres : sans
    
    But : Effacer(delete) un lieu qui a été sélectionné dans le formulaire "lieu_decollage_afficher.html"
    
    Remarque :  Dans le champ "nom_lieu_delete_wtf" du formulaire "lieu_decollage/lieu_decollage_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@obj_mon_application.route("/lieu_decollage_delete", methods=['GET', 'POST'])
def lieu_decollage_delete_wtf():
    data_films_attribue_lieu_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_lieu"
    id_lieu_delete = request.values['id_lieu_btn_delete_html']

    # Objet formulaire pour effacer le lieu sélectionné.
    form_delete = FormWTFDeleteLieu()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("lieu_decollage_afficher", order_by="ASC", id_lieu_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "lieu_decollage/lieu_decollage_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_lieu_delete = session['data_films_attribue_lieu_delete']
                print("data_films_attribue_lieu_delete ", data_films_attribue_lieu_delete)

                flash(f"Effacer le lieu de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer lieu" qui va irrémédiablement EFFACER le lieu
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_lieu_decollage": id_lieu_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_images_lieu = """DELETE FROM t_drone_lieu_decollage WHERE fk_lieu = %(value_id_lieu_decollage)s"""
                str_sql_delete_idlieu = """DELETE FROM t_lieu_decollage WHERE id_lieu_decollage = %(value_id_lieu_decollage)s"""
                # Manière brutale d'effacer d'abord la "fk_lieu", même si elle n'existe pas dans la "t_drone_lieu"
                # Ensuite on peut effacer le lieu vu qu'il n'est plus "lié" (INNODB) dans la "t_drone_lieu"
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(str_sql_delete_images_lieu, valeur_delete_dictionnaire)
                    mconn_bd.mabd_execute(str_sql_delete_idlieu, valeur_delete_dictionnaire)

                flash(f"lieu définitivement effacé !!", "success")
                print(f"lieu définitivement effacé !!")

                # afficher les données
                return redirect(url_for('lieu_decollage_afficher', order_by="ASC", id_lieu_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_lieu_decollage": id_lieu_delete}
            print(id_lieu_delete, type(id_lieu_delete))

            # Requête qui affiche tous les films_drones qui ont le lieu que l'utilisateur veut effacer
            str_sql_lieu_films_delete = """SELECT id_drone_lieu_decollage, nom_drone, id_lieu_decollage, lieu FROM t_drone_lieu_decollage
                                            INNER JOIN t_lieu_decollage ON t_drone_lieu_decollage.fk_lieu = t_lieu_decollage.id_lieu_decollage
                                            INNER JOIN t_drone ON t_drone_lieu_decollage.fk_drone = t_drone.id_drone
                                            WHERE fk_drone = %(value_id_lieu_decollage)s"""

            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()

            mybd_curseur.execute(str_sql_lieu_films_delete, valeur_select_dictionnaire)
            data_films_attribue_lieu_delete = mybd_curseur.fetchall()
            print("data_films_attribue_lieu_delete...", data_films_attribue_lieu_delete)

            # Nécessaire pour mémoriser les données afin d'afficher à nouveau
            # le formulaire "lieu/lieu_decollage_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            session['data_films_attribue_lieu_delete'] = data_films_attribue_lieu_delete

            # Opération sur la BD pour récupérer "id_lieu_decollage" et "intitule_lieu" de la "t_lieu"
            str_sql_id_lieu_decollage = "SELECT id_lieu_decollage, lieu FROM t_lieu_decollage WHERE id_lieu_decollage = %(value_id_lieu_decollage)s"

            mybd_curseur.execute(str_sql_id_lieu_decollage, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()",
            # vu qu'il n'y a qu'un seul champ "nom lieu" pour l'action DELETE
            data_nom_lieu = mybd_curseur.fetchone()
            print("data_nom_lieu ", data_nom_lieu, " type ", type(data_nom_lieu), " lieu ",
                  data_nom_lieu["lieu"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "magasin_delete_wtf.html"
            form_delete.nom_lieu_delete_wtf.data = data_nom_lieu["lieu"]

            # Le bouton pour l'action "DELETE" dans le form. "magasin_delete_wtf.html" est caché.
            btn_submit_del = False

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans lieu_decollage_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans lieu_decollage_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_dron_crud:
        code, msg = erreur_gest_dron_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_dron_crud} ", "danger")

        flash(f"Erreur dans lieu_decollage_delete_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_dron_crud.args[0]} , "
              f"{erreur_gest_dron_crud}", "danger")

        flash(f"__KeyError dans lieu_decollage_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("lieu_decollage/lieu_decollage_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_lieu_associes=data_films_attribue_lieu_delete)
