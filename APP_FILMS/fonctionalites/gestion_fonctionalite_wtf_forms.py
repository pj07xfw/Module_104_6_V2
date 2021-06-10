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


class FormWTFAjouterFonctionalite(FlaskForm):
    """
        Dans le formulaire "images_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_fonctionalite_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_fonctionalite_wtf = StringField("Clavioter l'autonomie ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(nom_fonctionalite_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])

    nom_portee_drone_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_portee_drone_wtf = StringField("Clavioter la  portée",
                                        validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                    Regexp(nom_portee_drone_regexp,
                                                           message="Pas de chiffres, de caractères "
                                                                   "spéciaux, "
                                                                   "d'espace à double, de double "
                                                                   "apostrophe, de double trait union")
                                                    ])
    nom_poids_drone_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_poids_drone_wtf = StringField("Clavioter le poids",
                                       validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                   Regexp(nom_poids_drone_regexp,
                                                          message="Pas de chiffres, de caractères "
                                                                  "spéciaux, "
                                                                  "d'espace à double, de double "
                                                                  "apostrophe, de double trait union")
                                                   ])
    nom_diagonale_drone_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_diagonale_drone_wtf = StringField("Clavioter la diagonale",
                                      validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                  Regexp(nom_diagonale_drone_regexp,
                                                         message="Pas de chiffres, de caractères "
                                                                 "spéciaux, "
                                                                 "d'espace à double, de double "
                                                                 "apostrophe, de double trait union")
                                                  ])

    submit = SubmitField("Enregistrer fonctionalité")

class FormWTFUpdateFonctionalite(FlaskForm):
    """
        Dans le formulaire "images_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_fonctionalite_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_fonctionalite_update_wtf = StringField("Clavioter l'autonomie", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                  Regexp(nom_fonctionalite_update_regexp,
                                                                          message="Pas de chiffres, de caractères  "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    nom_portee_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_portee_update_wtf = StringField("Clavioter la portée",
                                               validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                           Regexp(nom_portee_update_regexp,
                                                                  message="Pas de chiffres, de caractères  "
                                                                          "spéciaux, "
                                                                          "d'espace à double, de double "
                                                                          "apostrophe, de double trait "
                                                                          "union")
                                                           ])
    nom_poids_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_poids_update_wtf = StringField("Clavioter le poids",
                                        validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                    Regexp(nom_poids_update_regexp,
                                                           message="Pas de chiffres, de caractères  "
                                                                   "spéciaux, "
                                                                   "d'espace à double, de double "
                                                                   "apostrophe, de double trait "
                                                                   "union")
                                                    ])
    taille_diagonale_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    taille_diagonale_update_wtf = StringField("Clavioter la diagonale",
                                       validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                   Regexp(taille_diagonale_update_regexp,
                                                          message="Pas de chiffres, de caractères  "
                                                                  "spéciaux, "
                                                                  "d'espace à double, de double "
                                                                  "apostrophe, de double trait "
                                                                  "union")
                                                   ])
    submit = SubmitField("Update fonctionalité")


class FormWTFDeleteFonctionalite(FlaskForm):
    """
        Dans le formulaire "images_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_fonctionalite_delete_wtf = StringField("Effacer cette fonctionalité")
    submit_btn_del = SubmitField("Effacer fonctionalité")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
