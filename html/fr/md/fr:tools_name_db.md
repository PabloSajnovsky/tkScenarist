
# Outil 'BDD noms de personnages'

## <a name="sommaire"/>Sommaire

* [Aperçu](#screenshot)
* [Présentation](#introduction)
* [Utilisation](#utilisation)
    * [Zone 'Rechercher'](#search)
    * [Zone 'Outils'](#tools)
        * [Naviguer dans les résultats](#browse_results)
        * [Importer un fichier CSV](#file_import)
* [Pour finir](#pour-finir)
* [Navigation rapide](#navigation-rapide)


## <a name="screenshot"/>Aperçu

![image](../../images/screenshots/fr/screenshot-006.png)

Retourner au [sommaire](#sommaire).


## <a name="introduction"/>Présentation

Cet outil permet de rechercher dans la base de données (BDD) centrale
du logiciel `tkScenarist` des milliers de noms de personnages provenant
de toutes origines à travers la planète.

Il se compose de **trois zones** principales&nbsp;:

1. à gauche, la zone **Affichage**, qui permet de visualiser le
résultat des différentes recherches effectuées dans la base de données
centrale&nbsp;;
1. en haut, à droite, la zone **Rechercher**, qui permet de composer
une requête de base de données, pour rechercher un nom ou un groupe de
noms particuliers&nbsp;;
1. en bas, à droite, la zone **Outils**, qui permet de naviguer dans
les résultats de recherche, ainsi que d'importer des noms
supplémentaires à partir d'un fichier au format CSV (Comma-Separated
Values, valeurs séparées par des virgules).

Dans cet outil, les zones **ne sont pas** redimensionnables.

Retourner au [sommaire](#sommaire).


## <a name="utilisation"/>Utilisation

### <a name="search"/>Zone 'Rechercher'

Par défaut, cet outil affiche tout le contenu de la base de données
centrale du logiciel `tkScenarist`, sans critère de sélection
particulier.

Si vous souhaitez rechercher plus précisément un nom, un type de noms
ou un groupe de noms, sélectionnez parmi les choix proposés ceux qui
correspondent au mieux à votre recherche.

Une **Mention**, c'est ce que vous recherchez e.g. un nom, une origine,
un genre (masculin, féminin, les deux, aucun des deux) ou une
description.

Cette mention peut correspondre à quatre situations bien
distinctes&nbsp;:

1. la mention **contient** les lettres que vous avez tapées dans la
petite zone de texte blanche située juste en-dessous&nbsp;;
1. la mention **commence par** les lettres que vous avez tapées dans la
petite zone de texte blanche située juste en-dessous&nbsp;;
1. la mention **se termine par** les lettres que vous avez tapées dans
la petite zone de texte blanche située juste en-dessous&nbsp;;
1. la mention **correspond exactement** aux lettres que vous avez
tapées dans la petite zone de texte blanche située juste
en-dessous&nbsp;;

La zone de choix 'Dans :' permet de sélectionner le ou les endroits où
il faut chercher les critères définis ci-dessus.

Il s'agit de cases à cocher qui autorisent des choix en logique 'et/ou'
e.g. rechercher dans les noms et/ou dans les origines et/ou dans les
descriptions, selon les combinaisons cochées que vous effectuerez.

La zone de choix 'Afficher :' est un peu plus spéciale&nbsp;: si vous
cochez le choix 'Tous les noms' la requête composée n'effectuera aucun
filtrage.

Vous aurez donc des noms masculins, féminins, [épicènes](http://fr.wikipedia.org/wiki/%C3%89pic%C3%A8ne) (mixtes) ou sans genre
particulier (ni masculins ni féminins).

En revanche, si vous cochez 'Noms masculins' et/ou 'Noms féminins',
vous n'obtiendrez &ndash; selon la combinaison cochée &ndash; que des
noms masculins, que des noms féminins ou que des noms épicènes
(mixtes).

Pour afficher que des noms sans genre particulier (ni masculins ni
féminins), décochez **tous les choix** offerts ici.

Une requête de recherche dans la base de données (BDD) est lancée
automatiquement une demi-seconde après que vous ayez cessé de taper des
lettres au clavier dans la zone de texte blanche ou une demi-seconde
après que vous ayez cessé de cliquer sur des options et des choix.

Chaque changement dans vos choix provoquera une nouvelle requête
automatique de recherche.

Retourner au [sommaire](#sommaire).

### <a name="tools"/>Zone 'Outils'

#### <a name="browse_results"/>Naviguer dans les résultats

Une fois que vous avez composé votre requête de recherche dans la base
de données, il se peut que les résultats à afficher soient largement
plus nombreux que ceux réellement affichés à un moment donné.

Pour se déplacer d'un bloc de résultats à un autre, cliquez sur le
bouton `Suivant` si vous voulez passer au bloc suivant, sur le bouton
`Précédent` si vous voulez retourner au bloc précédent ou sur le bouton
`Début` si vous souhaitez retourner au début de vos résultats de
recherche.

Chaque nouvelle requête automatique de recherche vous replacera
systématiquement au début des résultats de cette nouvelle recherche.

En général, si vous avez vraiment beaucoup de résultats, c'est que très
probablement votre requête de recherche n'est pas assez précise.

N'hésitez donc pas à affiner encore et encore ce que vous recherchez,
non seulement vous gagnerez du temps (plutôt que de naviguer
interminablement parmi des milliers de résultats), mais de plus vous
découvrirez des techniques intéressantes pour extraire efficacement des
informations au sein d'une base de données.

Retourner au [sommaire](#sommaire).

#### <a name="file_import"/>Importer un fichier CSV

Pour importer des noms supplémentaires dans la base de données (BDD)
centrale du logiciel `tkScenarist`, cliquez sur le bouton
`Importer fichier (CSV)`.

Un outil d'importation s'affiche alors pour vous permettre d'effectuer
un ajout de données à la base.

![image](../../images/screenshots/fr/screenshot-007.png)

Cliquez sur le bouton `Parcourir` de cet outil d'importation pour
désigner le fichier à importer dans la base de données.

Attention&nbsp;: cet outil n'accepte que le format de fichier CSV
standard (voir [CSV sur wikipedia](http://fr.wikipedia.org/wiki/Comma-separated_values) pour plus
d'information).

Une fois le fichier d'importation désigné, le logiciel devrait vous
proposer une première réaffectation des données en fonction de ce qu'il
aura pu détecter dans la première ligne (en-têtes) du fichier à
importer.

Chaque donnée séparée par une virgule dans le fichier devrait
correspondre (en théorie) à une colonne de la base de données e.g. Nom,
Genre, Origine, Description.

Vérifiez bien que le numéro de colonne (du fichier à importer) affecté
à chacune des colonnes de la base de données correspond bien à la
réalité.

En d'autres termes, est-ce que les valeurs affichées dans l'aperçu du
contenu du fichier à importer sont bien dans le même ordre
d'affectation que celui affiché dans les listes déroulantes de 'Nom',
'Genre', 'Origine' et 'Description' situées juste en-dessous ?

Si ce n'est pas le cas, déroulez la liste de choix correspondant à la
colonne erronée et sélectionnez le bon numéro de colonne en fonction de
la position de la donnée dans le fichier d'importation.

**Exemple concret**&nbsp;: supposons que vous vouliez importer un
fichier `asian-names.csv` dans la base de données du logiciel.

Cliquez sur le bouton `Parcourir`, rendez-vous à l'emplacement où se
trouve ce fichier puis double-cliquez sur ce fichier pour le
sélectionner.

Le logiciel procède alors à une reconnaissance de format et
d'organisation des données dans ce fichier.

Si tout va bien, un aperçu des quelques premières lignes du fichier
s'affichera dans la zone 'Aperçu', pour vous permettre de vérifier que
l'affectation des données s'est bien faite dans le bon ordre.

Supposons à présent que ce fichier n'ait pas de première ligne
d'en-têtes&nbsp;: le fichier commence immédiatement avec des données.

Le logiciel ne trouve donc aucune correspondance valable et affiche
dans toutes les listes déroulantes la mention `--- pas trouvé ---`.

Charge à vous dès lors de lui indiquer qui va où.

Dans le champ 'Nom', sélectionnez le numéro de colonne correspondant à
l'emplacement des noms dans le fichier à importer.

Si les noms sont cités en première position dans le fichier, c'est la
colonne 1, s'ils sont en deuxième position, c'est la colonne 2, etc.

Faites de même pour les champs 'Genre', 'Origine' et 'Description'.

Si, par exemple, des données ne figurent pas dans le fichier à importer
e.g. pas de description de nom nulle part, laissez simplement la
mention `--- pas trouvé ---`, le logiciel comprendra et en tiendra
compte.

Une fois que vous avez bien tout vérifié et/ou corrigé, cliquez sur le
bouton `Importer` situé à côté de la barre de progression, en bas de
l'outil d'importation de données.

La procédure d'importation se lance et gère le rapatriement des données
du fichier CSV dans la base de données centrale du logiciel.

Les noms importés en double (doublons) seront automatiquement filtrés
et éliminés, vous n'avez donc pas à vous en soucier.

Retourner au [sommaire](#sommaire).


## <a name="pour-finir"/>Pour finir

**IMPORTANT**&nbsp;: afin de vous préserver de toute mauvaise surprise,
pensez à **sauvegarder régulièrement votre projet**, soit en utilisant
le menu `Projet > Enregistrer`, soit en utilisant le raccourci clavier
`<Ctrl-S>` correspondant au couplage successif des touches `Ctrl` (en
bas à gauche ou à droite de votre clavier) et `S` du clavier
alphanumérique.

Retourner au [sommaire](#sommaire).

---

#### <a name="navigation-rapide"/>Navigation rapide

* **L'application par ses onglets**
    * [Onglet 'Titre/Données'](fr_tab_title_data.html)
    * [Onglet 'Brouillon/Notes'](fr_tab_draft_notes.html)
    * [Onglet 'Pitch/Concept'](fr_tab_pitch_concept.html)
    * [Onglet 'Personnages'](fr_tab_characters.html)
    * [Onglet 'Scénario'](fr_tab_scenario.html)
    * [Onglet 'Storyboard'](fr_tab_storyboard.html)
    * [Onglet 'Ressources'](fr_tab_resources.html)
* **Les outils**
    * [BDD noms de personnages](fr_tools_name_db.html)
    * [Modèles d'histoires/pitchs](fr_tools_pitch_templates.html)
    * [Éléments de scénario](fr_tools_scenario_elements_editor.html)

Retourner à [l'accueil](index.html).
