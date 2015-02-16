
# L'application par ses onglets

## <a name="onglet-personnages"/>Onglet 'Personnages'

## <a name="sommaire"/>Sommaire

* [Aperçu](#screenshot)
* [Présentation](#introduction)
* [Utilisation](#utilisation)
    * [Liste de noms de personnages](#name_list)
        * [Ajouter un nom](#list_add)
        * [Renommer un nom](#list_rename)
        * [Supprimer un nom](#list_del)
        * [Purger la liste](#list_purge)
    * [Historique personnage](#historique-personnage)
    * [Visuel relations](#visuel-relations)
        * [Ajouter un nom](#canvas_add)
        * [Renommer un nom](#canvas_rename)
        * [Supprimer un nom](#canvas_del)
        * [Ajouter une relation](#canvas_add_rel)
        * [Renommer une relation](#canvas_rename_rel)
        * [Supprimer une relation](#canvas_del_rel)
* [Pour finir](#pour-finir)
* [Navigation rapide](#navigation-rapide)


## <a name="screenshot"/>Aperçu

![image](../../images/screenshots/fr/screenshot-005.png)

Retourner au [sommaire](#sommaire).


## <a name="introduction"/>Présentation

Cet onglet permet de gérer les protagonistes du film, notamment les
noms des personnages, leur histoire personnelle, ainsi que les liens
qui les unissent.

Cet onglet se subdivise en **trois zones**&nbsp;:

1. en haut, à gauche&nbsp;: c'est la **liste des noms de personnages**
à proprement parler&nbsp;;
1. en bas, à gauche&nbsp;: c'est la zone de texte permettant de
renseigner l'**histoire personnelle** de chaque personnage
sélectionné&nbsp;;
1. à droite, la grande zone grise&nbsp;: il s'agit du canevas graphique
du **gestionnaire visuel de relations** entre personnages.

Toutes les zones sont **redimensionnables**&nbsp;: il suffit de placer
la flèche de la souris entre les zones, l'icône du pointeur doit alors
changer d'aspect (e.g. deux flèches qui s'opposent), de maintenir le
clic enfoncé puis de déplacer dans le sens indiqué par le pointeur de
souris pour obtenir le redimensionnement escompté.

Retourner au [sommaire](#sommaire).

## <a name="utilisation"/>Utilisation

### <a name="name_list"/>Liste de noms de personnages

#### <a name="list_add"/>Ajouter un nom de personnage

Pour ajouter un nouveau nom de personnage, cliquez sur le bouton `+`
(signe plus) situé en bas à gauche de la liste des noms de personnages.

Une fenêtre de dialogue s'ouvre alors pour vous permettre d'entrer un
nom.

Ne vous étonnez pas si le nom apparaît systématiquement en majuscules
dans la liste, une fois que vous l'avez validé&nbsp;: il s'agit d'une
règle de rédaction de scénario qui veut que les noms de personnages
soient toujours cités en toutes majuscules dans le texte.

La liste est donc gérée conformément à cette exigence technique, en vue
de faire figurer tous les noms de personnages en toutes majuscules lors
de leur saisie dans le texte du scénario (voir
[onglet&nbsp;'Scénario'](fr_tab_scenario.html) pour plus de détail).

Notez aussi que chaque nom de personnage doit être **unique**
(exemple&nbsp;: vous ne pouvez pas créer deux 'JACQUES' sans préciser
une différence entre les deux, par exemple avec le nom de famille,
'JACQUES DUMOULIN' et 'JACQUES DUFOUR').

Quoi qu'il en soit, le logiciel ne manquera pas de vous le signaler, le
cas échéant.

Retourner au [sommaire](#sommaire).

#### <a name="list_rename"/>Renommer un nom de personnage

Changer le nom d'un personnage implique plusieurs règles&nbsp;:

1. le nom à changer doit déjà exister dans la liste&nbsp;;
1. le nom à changer ne doit pas être cité dans le texte du scénario au
moment de le renommer&nbsp;;
1. le nouveau nom doit être unique et ne pas figurer d'ores et déjà par
ailleurs dans la liste des noms de personnages existants
(exemple&nbsp;: changer 'TOTO' en 'TUTU', alors que 'TUTU' existe déjà
dans la liste).

Pour renommer un personnage, sélectionnez son nom dans la liste, puis
cliquez sur le bouton `Renommer` situé en bas de la liste.

Une fenêtre de dialogue s'ouvre alors pour vous permettre de modifier
le nom sélectionné.

Si le nouveau nom entré figure déjà dans la liste, le logiciel ne
manquera pas de vous le signaler et l'ancien nom du personnage **ne
sera pas modifié**.

Retourner au [sommaire](#sommaire).

#### <a name="list_del"/>Supprimer un nom de personnage

Vous ne pouvez supprimer le nom d'un personnage que si ce nom existe
effectivement dans la liste et qu'il *N'EST PAS* cité au moins une fois
dans le texte du scénario (voir
[onglet&nbsp;'Scénario'](fr_tab_scenario.html) pour plus de détail).

Pour supprimer un nom de personnage, sélectionnez-le tout d'abord dans
la liste, puis cliquez sur le bouton `-` (signe moins) situé en bas à
gauche de la liste des noms de personnages.

Une fenêtre de dialogue vous demandera de confirmer votre choix avant
de procéder à la suppression définitive du nom du personnage.

Retourner au [sommaire](#sommaire).

#### <a name="list_purge"/>Purger la liste

Il peut arriver parfois que l'on ait besoin de faire place nette dans
la liste des noms de personnages.

Purger la liste des noms de personnages revient à supprimer
automatiquement tous les noms qui ne sont pas cités au moins une fois
dans le texte du scénario.

Pour purger la liste des noms de personnages, cliquez sur le bouton
`Purger` situé en bas de la liste.

Une fenêtre de dialogue s'ouvre alors et vous demande confirmation de
l'opération de nettoyage automatique.

Cliquez sur `Oui` si vous souhaitez ne conserver que les noms figurant
déjà dans le texte du scénario et supprimer tous les autres.

Retourner au [sommaire](#sommaire).


### <a name="historique-personnage"/>Historique personnage

Pour renseigner l'histoire personnelle d'un personnage, il faut tout
d'abord sélectionner un nom de personnage dans la liste.

Cliquez sur le nom de personnage que vous souhaitez renseigner puis
cliquez sur la zone de texte blanche en bas, à gauche, qui vous
permettra de rédiger l'histoire du personnage.

Ne cherchez pas de bouton `Sauvegarder`, il n'y en a pas&nbsp;: toutes
les saisies dans ces petites zones de texte sont **automatiquement
sauvegardées** entre chaque personnage.

Il vous suffit donc de sélectionner un nom, d'entrer ensuite son
histoire personnelle, puis de cliquer sur un autre nom, d'entrer son
histoire personnelle aussi, etc, etc.

En revanche, ce petit confort ne vous dispense pas de sauvegarder
régulièrement **le projet en entier** (voir [ci-dessous](#save)).

La zone de texte blanche s'appelle un **éditeur de texte brut**.

L'éditeur de texte brut permet des sauts à la ligne lorsque vous
pressez la touche de clavier `<Entrée>` (retour chariot).

Chaque saut à la ligne crée un nouveau paragraphe.

En revanche, contrairement au **traitement de textes**, cet objet ne
permet pas la mise en forme du texte entré (diverses polices de
caractères, gras, italique, souligné, couleurs d'encre et de fond,
centrage / justification de paragraphes, etc).

Il s'agit d'une zone de texte **neutre**.

Un double-clic sur un mot permet de sélectionner **ce mot uniquement**.

Un triple-clic sur un mot permet de sélectionner **le paragraphe** dans
lequel ce mot se trouve.

Le menu `Edition > Tout sélectionner` ou la combinaison de touches de
clavier `<Ctrl-A>` permettent de **tout sélectionner** dans l'éditeur
de texte brut.

Tout ruban de sélection est susceptible d'être remplacé par la
prochaine frappe d'une touche au clavier.

Contrairement aux champs de formulaire (voir
[onglet&nbsp;'Titre/Données'](fr_tab_title_data.html)), un éditeur de texte
brut prend en charge l'annulation des mots entrés.

Pour annuler la saisie du dernier mot entré, utilisez soit le menu
`Edition > Annuler`, soit le raccourci clavier `<Ctrl-Z>` correspondant
au couplage successif des touches `Ctrl` (en bas à gauche ou à droite
de votre clavier) et `Z` du clavier alphanumérique.

Pour répéter la saisie du dernier mot annulé, utilisez soit le menu
`Edition > Refaire`, soit le raccourci clavier `<Ctrl-Shift-Z>`
correspondant au couplage successif des touches `Ctrl`, `Shift`
(chariot majuscules) et `Z` du clavier alphanumérique.

Retourner au [sommaire](#sommaire).


### <a name="visuel-relations"/>Visuel relations

#### <a name="canvas_add"/>Ajouter un nom de personnage

Vous pouvez ajouter un nom de personnage directement dans le
gestionnaire visuel de relations, sans passer par la liste des noms de
personnages située à gauche.

Pour ce faire, double-cliquez simplement sur une zone neutre du canevas
graphique.

Une zone neutre se caractérise par le fond du canevas graphique (fond
gris), à l'exclusion de tout autre objet qui pourrait se trouver sous
la flèche de la souris, comme par exemple, une étiquette de nom de
personnage déjà existant, un lien de relation ou encore une étiquette
de relation entre personnages.

Une fenêtre de dialogue s'ouvre alors pour vous permettre d'entrer un
nom.

Ne vous étonnez pas si le nom apparaît systématiquement en majuscules
dans la liste des noms de personnages ou sur l'étiquette du canevas
graphique, une fois que vous l'avez validé&nbsp;: il s'agit d'une règle
de rédaction de scénario qui veut que les noms de personnages soient
toujours cités en toutes majuscules dans le texte.

La liste des noms est donc gérée conformément à cette exigence
technique, en vue de faire figurer tous les noms de personnages en
toutes majuscules lors de leur saisie dans le texte du scénario (voir
[onglet&nbsp;'Scénario'](fr_tab_scenario.html) pour plus de détail).

Notez aussi que chaque nom de personnage doit être **unique**
(exemple&nbsp;: vous ne pouvez pas créer deux 'JACQUES' sans préciser
une différence entre les deux, par exemple avec le nom de famille,
'JACQUES DUMOULIN' et 'JACQUES DUFOUR').

Quoi qu'il en soit, le logiciel ne manquera pas de vous le signaler, le
cas échéant.

Retourner au [sommaire](#sommaire).

#### <a name="canvas_rename"/>Renommer un nom de personnage

Vous pouvez renommer un personnage directement dans le gestionnaire
visuel de relations, sans passer par la liste des noms de personnages
située à gauche.

Pour ce faire, double-cliquez simplement sur l'étiquette du canevas
graphique qui contient le nom que vous souhaitez changer.

Une fenêtre de dialogue s'ouvre alors pour vous permettre de modifier
le nom sélectionné.

Changer le nom d'un personnage implique toutefois quelques règles
simples&nbsp;:

1. le nom à changer doit déjà exister dans la liste&nbsp;;
1. le nom à changer ne doit pas être cité dans le texte du scénario au
moment de le renommer&nbsp;;
1. le nouveau nom doit être unique et ne pas figurer d'ores et déjà par
ailleurs dans la liste des noms de personnages existants
(exemple&nbsp;: changer 'TOTO' en 'TUTU', alors que 'TUTU' existe déjà
dans la liste).

Si le nouveau nom entré figure déjà dans la liste, le logiciel ne
manquera pas de vous le signaler et l'ancien nom du personnage **ne
sera pas modifié**.

Retourner au [sommaire](#sommaire).

#### <a name="canvas_del"/>Supprimer un nom de personnage

Vous pouvez supprimer le nom d'un personnage directement dans le
gestionnaire visuel de relations, sans passer par la liste des noms de
personnages située à gauche.

Pour ce faire, maintenez enfoncée la touche `Ctrl` (en bas à gauche ou
à droite de votre clavier), puis cliquez sur l'étiquette du canevas
graphique qui contient le nom que vous souhaitez supprimer.

Vous ne pouvez supprimer le nom d'un personnage que si ce nom existe
effectivement dans la liste et qu'il *N'EST PAS* cité au moins une fois
dans le texte du scénario (voir
[onglet&nbsp;'Scénario'](fr_tab_scenario.html) pour plus de détail).

Une fenêtre de dialogue vous demandera alors de confirmer votre choix
avant de procéder à la suppression définitive du nom du personnage.

Retourner au [sommaire](#sommaire).

#### <a name="canvas_add_rel"/>Ajouter une relation

Ajouter une relation ne peut se faire qu'en respectant les règles
suivantes&nbsp;:

1. on ne peut créer de relation qu'entre deux noms de personnages
**distincts** (le logiciel ne manquera pas de vous le signaler, le cas
échéant)&nbsp;;
1. on ne peut créer qu'**une seule relation** entre deux mêmes
personnages (n'essayez donc pas de créer une relation `TOTO père de
TUTU` *ET* `TUTU fils de TOTO`, cela ne marchera pas)&nbsp;;
1. un lien de relation tiré à partir d'un personnage mais qui
n'aboutirait nulle part ne crée aucune relation, évidemment.

Pour créer une relation entre deux noms de personnages distincts,
maintenez enfoncée la touche `Shift` (chariot majuscules, symbole
&uArr;, en bas à gauche ou à droite du clavier), enfoncez le bouton
clic de la souris sur l'étiquette du nom de départ, puis glissez la
souris jusqu'à atteindre l'étiquette du nom de personnage d'arrivée et
enfin relâchez le bouton clic de la souris une fois sur place, ainsi
que la touche `Shift` du clavier.

Un lien visuel devrait apparaître sous la forme d'un trait noir sortant
de l'étiquette de départ et aboutissant à l'étiquette d'arrivée,
flanqué d'une étiquette noire mentionnant 'Relation' à mi-chemin.

Retourner au [sommaire](#sommaire).

#### <a name="canvas_rename_rel"/>Renommer une relation

Pour changer le contenu texte d'une relation, double-cliquez simplement
sur l'étiquette noire contenant le texte à modifier.

Une fenêtre de dialogue s'ouvre alors pour vous permettre de modifier
le contenu texte de la relation.

Retourner au [sommaire](#sommaire).

#### <a name="canvas_del_rel"/>Supprimer une relation

Pour supprimer une relation entre deux noms de personnages, maintenez
enfoncée la touche `Ctrl` (en bas à gauche ou à droite de votre
clavier), puis cliquez sur l'étiquette noire du canevas graphique qui
contient le texte de la relation que vous souhaitez supprimer.

Une fenêtre de dialogue vous demandera alors de confirmer votre choix
avant de procéder à la suppression définitive de la relation.

Retourner au [sommaire](#sommaire).


## <a name="pour-finir"/>Pour finir

Si vous cliquez simplement sur l'étiquette de nom d'un personnage dans
le canevas graphique du gestionnaire visuel de relations, vous
sélectionnez par la même occasion le nom du personnage dans la liste
des noms de personnages située en haut à gauche et vous obtenez aussi
dans la foulée des informations dans l'historique personnage situé en
bas à gauche.

Vous pouvez déplacer les étiquettes de noms de personnages qui se
trouvent dans le canevas graphique du gestionnaire de relations en
maintenant simplement le bouton clic de la souris enfoncé sur
l'étiquette de nom que vous souhaitez déplacer, en bougeant la souris
dans la direction souhaitée, puis en relâchant le bouton clic de la
souris une fois sur place (glisser-déposer, drag'n'drop).

Il existe aussi une fonctionnalité de navigation secrète.

Pour naviguer rapidement dans le canevas graphique, maintenez le bouton
clic de la souris enfoncé sur une zone neutre, puis déplacez la souris
dans la direction où vous souhaitez aller.

Relâchez enfin le bouton clic de la souris une fois arrivé(e) à
destination.

Une zone neutre se caractérise par le fond du canevas graphique (fond
gris), à l'exclusion de tout autre objet qui pourrait se trouver sous
la flèche de la souris, comme par exemple, une étiquette de nom de
personnage déjà existant, un lien de relation ou encore une étiquette
de relation entre personnages.

<a name="save"/>

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
