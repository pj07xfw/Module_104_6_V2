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


class FormWTFAjouterGamme(FlaskForm):
    """
        Dans le formulaire "images_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_gamme_regexp = "[A-Za-z1-9]"
    nom_gamme_wtf = StringField("Clavioter la gamme ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(nom_gamme_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    submit = SubmitField("Enregistrer drone")


class FormWTFUpdateGamme(FlaskForm):
    """
        Dans le formulaire "images_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_gamme_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_gamme_update_wtf = StringField("Clavioter la gamme ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                  Regexp(nom_gamme_update_regexp,
                                                                          message="Pas de chiffres, de caractères  "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    submit = SubmitField("Update gamme")


class FormWTFDeleteGamme(FlaskForm):
    """
        Dans le formulaire "gamme_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "gamme".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_gamme".
    """
    nom_gamme_delete_wtf = StringField("Effacer cette gamme")
    submit_btn_del = SubmitField("Effacer gamme")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
