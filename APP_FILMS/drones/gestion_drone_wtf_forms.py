"""
    Fichier : gestion_images_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import Length
from wtforms.validators import Regexp


class FormWTFAjouterDrone(FlaskForm):
    """
        Dans le formulaire "images_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_drone_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_drone_wtf = StringField("Clavioter le drone ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(nom_drone_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    affiche_drone_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    affiche_drone_wtf = StringField("Clavioter l'affiche", validators=[Length(min=2, max=900, message="min 2 max 20"),
                                                                       Regexp(affiche_drone_regexp,
                                                                              message="Pas de chiffres, de caractères "
                                                                                      "spéciaux, "
                                                                                      "d'espace à double, de double "
                                                                                      "apostrophe, de double trait union")
                                                                       ])
    submit = SubmitField("Enregistrer drone")


class FormWTFUpdateDrone(FlaskForm):
    """
        Dans le formulaire "images_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_drone_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_drone_update_wtf = StringField("Clavioter le drone ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                  Regexp(nom_drone_update_regexp,
                                                                          message="Pas de chiffres, de caractères  "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    affiche_drone_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    affiche_drone_update_wtf = StringField("Clavioter l'affiche", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(affiche_drone_update_regexp,
                                                                                 message="Pas de chiffres, de caractères  "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    submit = SubmitField("Update drone")


class FormWTFDeleteDrone(FlaskForm):
    """
        Dans le formulaire "images_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_drone_delete_wtf = StringField("Effacer ce drone")
    submit_btn_del = SubmitField("Effacer drone")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
