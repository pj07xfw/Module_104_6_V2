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


class FormWTFAjouterLieu(FlaskForm):
    """
        Dans le formulaire "images_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_lieu_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_lieu_wtf = StringField("Clavioter le lieu ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(nom_lieu_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    submit = SubmitField("Enregistrer drone")


class FormWTFUpdateLieu(FlaskForm):
    """
        Dans le formulaire "images_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_lieu_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_lieu_update_wtf = StringField("Clavioter le lieu ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                  Regexp(nom_lieu_update_regexp,
                                                                          message="Pas de chiffres, de caractères  "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    submit = SubmitField("Update drone")


class FormWTFDeleteLieu(FlaskForm):
    """
        Dans le formulaire "images_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "lieu".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_lieu_delete_wtf = StringField("Effacer ce lieu")
    submit_btn_del = SubmitField("Effacer lieu")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
