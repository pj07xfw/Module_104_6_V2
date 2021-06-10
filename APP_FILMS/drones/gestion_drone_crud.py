"""
    Fichier : gestion_magasin_crud.py
    Auteur : OM 2021.03.16
    Gestions des "routes" FLASK et des données pour les drone.
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
from APP_FILMS.drones.gestion_drone_wtf_forms import FormWTFAjouterDrone
from APP_FILMS.drones.gestion_drone_wtf_forms import FormWTFDeleteDrone
from APP_FILMS.drones.gestion_drone_wtf_forms import FormWTFUpdateDrone

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /drone_afficher
    
    Test : ex : http://127.0.0.1:5005/drone_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_drone_sel = 0 >> tous les drones.
                id_drone_sel = "n" affiche le drone dont l'id est "n"

"""

@obj_mon_application.route("/drone_afficher/<string:order_by>/<int:id_drone_sel>", methods=['GET', 'POST'])
def drone_afficher(order_by, id_drone_sel):
    if request.method == "GET":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion drone ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur GestionDrone {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                if order_by == "ASC" and id_drone_sel == 0:
                    strsql_drones_afficher = """SELECT id_drone, nom_drone, affiche_drone FROM t_drone ORDER BY id_drone ASC"""
                    mc_afficher.execute(strsql_drones_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_drone"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du drone sélectionné avec un nom de variable
                    valeur_id_drone_selected_dictionnaire = {"value_id_drone_selected": id_drone_sel}
                    strsql_drones_afficher = """SELECT id_drone, nom_drone, affiche_drone FROM t_drone WHERE id_drone = %(value_id_drone_selected)s"""

                    mc_afficher.execute(strsql_drones_afficher, valeur_id_drone_selected_dictionnaire)
                else:
                    strsql_drones_afficher = """SELECT id_drone, nom_drone, affiche_drone FROM t_drone ORDER BY id_drone DESC"""

                    mc_afficher.execute(strsql_drones_afficher)

                data_drones = mc_afficher.fetchall()

                print("data_drones ", data_drones, " Type : ", type(data_drones))

                # Différencier les messages si la table est vide.
                if not data_drones and id_drone_sel == 0:
                    flash("""La table "t_drone" est vide. !!""", "warning")
                elif not data_drones and id_drone_sel > 0:
                    # Si l'utilisateur change l'id_drone dans l'URL et que le drone n'existe pas,
                    flash(f"Le drone demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_drone" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données drone affichés !!", "success")

        except Exception as erreur:
            print(f"RGG Erreur générale. drone_afficher")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)"
            # fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            flash(f"RGG Exception {erreur} drone_afficher", "danger")
            raise Exception(f"RGG Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Envoie la page "HTML" au serveur.
    return render_template("drones/drone_afficher.html", data=data_drones)

"""

    Auteur : OM 2021.03.22
    Définition d'une "route" /drone_ajouter
    
    Test : ex : http://127.0.0.1:5005/drone_ajouter
    
    Paramètres : sans
    
    But : Ajouter un drone pour un film
    
    Remarque :  Dans le champ "name_drone_html" du formulaire "drone/drone_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/drone_ajouter", methods=['GET', 'POST'])
def drone_ajouter_wtf():
    form = FormWTFAjouterDrone()
    if request.method == "POST":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion drone ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur Gestiondrones {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            if form.validate_on_submit():
                name_drone_wtf = form.nom_drone_wtf.data
                affiche_drone = form.affiche_drone_wtf.data
                name_drone = name_drone_wtf.lower()
                valeurs_insertion_dictionnaire = {"value_intitule_drone": name_drone, "value_affiche_drone" : affiche_drone}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_drone = """INSERT INTO t_drone (id_drone, nom_drone, affiche_drone) VALUES (NULL,%(value_intitule_drone)s,%(value_affiche_drone)s)"""
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(strsql_insert_drone, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('drone_afficher', order_by='DESC', id_drone_sel=0))

        # ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except pymysql.err.IntegrityError as erreur_drone_doublon:
            # Dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs/exceptions.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            code, msg = erreur_drone_doublon.args

            flash(f"{error_codes.get(code, msg)} ", "warning")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except (pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                TypeError) as erreur_gest_dron_crud:
            code, msg = erreur_gest_dron_crud.args

            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Erreur dans Gestion drone CRUD : {sys.exc_info()[0]} "
                  f"{erreur_gest_dron_crud.args[0]} , "
                  f"{erreur_gest_dron_crud}", "danger")

    return render_template("drones/drone_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /drone_update
    
    Test : ex cliquer sur le menu "drone" puis cliquer sur le bouton "EDIT" d'un "drone"
    
    Paramètres : sans
    
    But : Editer(update) un drone qui a été sélectionné dans le formulaire "magasin_afficher.html"
    
    Remarque :  Dans le champ "nom_drone_update_wtf" du formulaire "drone/magasin_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/drone_update", methods=['GET', 'POST'])
def drone_update_wtf():

    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_drone"
    id_drone_update = request.values['id_drone_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateDrone()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "magasin_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_drone_update = form_update.nom_drone_update_wtf.data
            name_drone_update = name_drone_update.lower()
            name_affiche_drone_update = form_update.affiche_drone_update_wtf.data
            name_affiche_drone_update = name_affiche_drone_update.lower()

            valeur_update_dictionnaire = {"value_id_drone": id_drone_update, "value_name_drone": name_drone_update, "value_affiche_drone" : name_affiche_drone_update }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intituledrone = """UPDATE t_drone SET  nom_drone = %(value_name_drone)s, affiche_drone = %(value_affiche_drone)s WHERE id_drone = %(value_id_drone)s"""
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(str_sql_update_intituledrone, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_drone_update"
            return redirect(url_for('drone_afficher', order_by="ASC", id_drone_sel=id_drone_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_drone" et "intitule_drone" de la "t_drone"
            str_sql_id_drone = "SELECT id_drone,  nom_drone, affiche_drone FROM t_drone WHERE id_drone = %(value_id_drone)s"
            valeur_select_dictionnaire = {"value_id_drone": id_drone_update}
            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()
            mybd_curseur.execute(str_sql_id_drone, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom drone" pour l'UPDATE
            data_nom_drone = mybd_curseur.fetchone()
            print("data_nom_drone ", data_nom_drone, " type ", type(data_nom_drone), " drone ",
                  data_nom_drone["nom_drone"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "magasin_update_wtf.html"
            form_update.nom_drone_update_wtf.data = data_nom_drone["nom_drone"]
            form_update.affiche_drone_update_wtf.data = data_nom_drone["affiche_drone"]
    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans drone_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans drone_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_dron_crud:
        code, msg = erreur_gest_dron_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_dron_crud} ", "danger")
        flash(f"Erreur dans drone_update_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_dron_crud.args[0]} , "
              f"{erreur_gest_dron_crud}", "danger")
        flash(f"__KeyError dans drone_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("drones/drone_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /drone_delete
    
    Test : ex. cliquer sur le menu "drone" puis cliquer sur le bouton "DELETE" d'un "drone"
    
    Paramètres : sans
    
    But : Effacer(delete) un drone qui a été sélectionné dans le formulaire "magasin_afficher.html"
    
    Remarque :  Dans le champ "nom_drone_delete_wtf" du formulaire "drone/magasin_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@obj_mon_application.route("/drone_delete", methods=['GET', 'POST'])
def drone_delete_wtf():
    data_films_attribue_drone_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_drone"
    id_drone_delete = request.values['id_drone_btn_delete_html']

    # Objet formulaire pour effacer le drone sélectionné.
    form_delete = FormWTFDeleteDrone()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("drone_afficher", order_by="ASC", id_drone_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "drone/magasin_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_drone_delete = session['data_films_attribue_drone_delete']
                print("data_films_attribue_drone_delete ", data_films_attribue_drone_delete)

                flash(f"Effacer le drone de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer drone" qui va irrémédiablement EFFACER le drone
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_drone": id_drone_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_images_drone = """DELETE FROM t_drone_images WHERE fk_drone = %(value_id_drone)s"""
                str_sql_delete_iddrone = """DELETE FROM t_drone WHERE id_drone = %(value_id_drone)s"""
                # Manière brutale d'effacer d'abord la "fk_images", même si elle n'existe pas dans la "t_drone_film"
                # Ensuite on peut effacer le drone vu qu'il n'est plus "lié" (INNODB) dans la "t_drone_film"
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(str_sql_delete_images_drone, valeur_delete_dictionnaire)
                    mconn_bd.mabd_execute(str_sql_delete_iddrone, valeur_delete_dictionnaire)

                flash(f"drone définitivement effacé !!", "success")
                print(f"drone définitivement effacé !!")

                # afficher les données
                return redirect(url_for('drone_afficher', order_by="ASC", id_drone_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_drone": id_drone_delete}
            print(id_drone_delete, type(id_drone_delete))

            # Requête qui affiche tous les films_drones qui ont le drone que l'utilisateur veut effacer
            str_sql_drones_films_delete = """SELECT id_drone_images,  chemin_images, id_drone, nom_drone FROM t_drone_images
                                            INNER JOIN t_drone ON t_drone_images.fk_drone = t_drone.id_drone
                                            INNER JOIN t_images ON t_drone_images.fk_images = t_images.id_images
                                            WHERE fk_drone = %(value_id_drone)s"""

            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()

            mybd_curseur.execute(str_sql_drones_films_delete, valeur_select_dictionnaire)
            data_films_attribue_drone_delete = mybd_curseur.fetchall()
            print("data_films_attribue_drone_delete...", data_films_attribue_drone_delete)

            # Nécessaire pour mémoriser les données afin d'afficher à nouveau
            # le formulaire "drone/magasin_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            session['data_films_attribue_drone_delete'] = data_films_attribue_drone_delete

            # Opération sur la BD pour récupérer "id_drone" et "intitule_drone" de la "t_drone"
            str_sql_id_drone = "SELECT id_drone, nom_drone FROM t_drone WHERE id_drone = %(value_id_drone)s"

            mybd_curseur.execute(str_sql_id_drone, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()",
            # vu qu'il n'y a qu'un seul champ "nom drone" pour l'action DELETE
            data_nom_drone = mybd_curseur.fetchone()
            print("data_nom_drone ", data_nom_drone, " type ", type(data_nom_drone), " drone ",
                  data_nom_drone["nom_drone"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "magasin_delete_wtf.html"
            form_delete.nom_drone_delete_wtf.data = data_nom_drone["nom_drone"]

            # Le bouton pour l'action "DELETE" dans le form. "magasin_delete_wtf.html" est caché.
            btn_submit_del = False

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans drone_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans drone_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_dron_crud:
        code, msg = erreur_gest_dron_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_dron_crud} ", "danger")

        flash(f"Erreur dans drone_delete_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_dron_crud.args[0]} , "
              f"{erreur_gest_dron_crud}", "danger")

        flash(f"__KeyError dans drone_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("drones/drone_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_drone_associes=data_films_attribue_drone_delete)
