"""
    Fichier : gestion_magasin_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import Length
from wtforms.validators import Regexp


class FormWTFAjouterMagasin(FlaskForm):
    """
        Dans le formulaire "images_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_magasin_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_magasin_wtf = StringField("Clavioter le magasin ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(nom_magasin_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    nom_prix_drone_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_prix_drone_wtf = StringField("Clavioter le prix", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                       Regexp(nom_prix_drone_regexp,
                                                                              message="Pas de chiffres, de caractères "
                                                                                      "spéciaux, "
                                                                                      "d'espace à double, de double "
                                                                                      "apostrophe, de double trait union")
                                                                       ])
    nom_reduction_drone_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_reduction_drone_wtf = StringField("Clavioter la réduction", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                      Regexp(nom_reduction_drone_regexp,
                                                                             message="Pas de chiffres, de caractères "
                                                                                     "spéciaux, "
                                                                                     "d'espace à double, de double "
                                                                                     "apostrophe, de double trait union")
                                                                      ])
    submit = SubmitField("Enregistrer magasin")


class FormWTFUpdateMagasin(FlaskForm):
    """
        Dans le formulaire "images_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_magasin_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_magasin_update_wtf = StringField("Clavioter le magasin", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                  Regexp(nom_magasin_update_regexp,
                                                                          message="Pas de chiffres, de caractères  "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    nom_prix_drone_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_prix_drone_update_wtf = StringField("Clavioter le prix",
                                         validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                     Regexp(nom_prix_drone_update_regexp,
                                                            message="Pas de chiffres, de caractères  "
                                                                    "spéciaux, "
                                                                    "d'espace à double, de double "
                                                                    "apostrophe, de double trait "
                                                                    "union")
                                                     ])
    nom_reduction_drone_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_reduction_drone_update_wtf = StringField("Clavioter la réduction",
                                         validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                     Regexp(nom_reduction_drone_update_regexp,
                                                            message="Pas de chiffres, de caractères  "
                                                                    "spéciaux, "
                                                                    "d'espace à double, de double "
                                                                    "apostrophe, de double trait "
                                                                    "union")
                                                     ])
    submit = SubmitField("Update magasin")


class FormWTFDeleteMagasin(FlaskForm):
    """
        Dans le formulaire "images_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "magasin".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_magasin".
    """
    nom_magasin_delete_wtf = StringField("Effacer ce magasin")
    submit_btn_del = SubmitField("Effacer magasin")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
