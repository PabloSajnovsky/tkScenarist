
# Outil 'Éléments de scénario'

## <a name="sommaire"/>Sommaire

* [Aperçu](#screenshot)
* [Présentation](#introduction)
* [Utilisation](#utilisation)
    * [Barre d'onglets](#pref_tabs)
        * [Onglet 'Préférences générales'](#global_prefs)
        * [Onglet 'Préférences projet'](#project_prefs)
    * [Section 'Enchaînements'](#tab_switch)
        * [Encadré 'Élément'](#element_frame)
        * [Encadré 'Actions'](#actions_frame)
    * [Section 'Styles'](#looknfeel)
        * [Encadré 'Style'](#lnf_frame)
        * [Encadré 'Aperçu'](#preview_frame)
    * [Boutons tout en bas](#dialog_buttons)
        * [Bouton 'OK'](#ok_button)
        * [Bouton 'Réinitialiser'](#reset_button)
        * [Bouton 'Annuler'](#cancel_button)
* [Pour finir](#pour-finir)
* [Navigation rapide](#navigation-rapide)


## <a name="screenshot"/>Aperçu

![image](../../images/screenshots/fr/screenshot-009.png)

Retourner au [sommaire](#sommaire).


## <a name="introduction"/>Présentation

Cet outil permet de régler plus finement le comportement de l'éditeur
de texte spécifique de l'onglet `Scénario` de l'application.

Il se compose de **trois sections** principales&nbsp;:

1. tout en haut, la **barre d'onglets**, composée d'un onglet
`Préférences générales` et d'un onglet `Préférences projet`, qui vous
permettent de choisir où vous voulez appliquer vos réglages&nbsp;;
1. ensuite, vous avez la **section 'Enchaînements'**, composée d'un
encadré intitulé 'Élément' et d'un encadré intitulé 'Actions', qui vous
permettent de régler les enchaînements d'éléments de scénario en mode
'Switch' et en mode 'Create'&nbsp;;
1. pour finir, vous avez la **section 'Styles'**, composée d'un encadré
intitulé 'Style' et d'un encadré intitulé 'Aperçu', qui vous permettent
de régler l'aspect visuel de chaque élément de scénario.

Dans cet outil, les zones **ne sont pas** redimensionnables.

**ATTENTION**&nbsp;: il est fortement recommandé de bien prendre
connaissance de la documentation concernant
[l'onglet 'Scénario'](fr_tab_scenario.html) avant de vous lancer dans des
réglages hasardeux.

**Notre équipe ne prend pas en charge** de support concernant les
résultats inattendus qui pourraient survenir suite à une mauvaise
utilisation de cet outil. La lecture attentive de la page ici présente
devrait résoudre la plupart de vos problèmes.

Retourner au [sommaire](#sommaire).


## <a name="utilisation"/>Utilisation

### <a name="pref_tabs"/>Barre d'onglets

La barre d'onglet vous permet de choisir où vous voulez appliquer vos
réglages.

Retourner au [sommaire](#sommaire).

#### <a name="global_prefs"/>Onglet 'Préférences générales'

Cliquez sur l'onglet `Préférences générales` pour appliquer vos
réglages à l'ensemble des projets futurs que vous produirez à partir de
là.

En effet, si vous validez vos réglages grâce au [Bouton 'OK'](#ok_button) situé tout en bas de l'outil, vos nouveaux choix seront
conservés dans la mémoire du logiciel d'une session sur l'autre, ce qui
signifie que vous n'aurez pas besoin d'effectuer ces réglages à nouveau
à chaque fois que vous lancerez `tkScenarist`.

**ATTENTION**&nbsp;: si vous avez un projet ouvert ou déjà en cours, ce
sont les réglages des `Préférences projet` qui ont la **priorité** sur
les réglages généraux. Vous risquez donc de ne pas voir immédiatement
le résultat de vos changements.

Pour voir vos nouveaux réglages généraux, sauvegardez le projet en
cours, puis utilisez soit le menu `Projet > Nouveau`, soit le raccourci
clavier `<Ctrl-N>` correspondant au couplage successif des touches
`Ctrl` (en bas à gauche ou à droite de votre clavier) et `N` du clavier
alphanumérique.

**Pour revenir aux réglages d'usine** (par défaut), cliquez sur le
[Bouton 'Réinitialiser'](#reset_button) situé tout en bas de l'outil,
puis cliquez sur le [Bouton 'OK'](#ok_button), sauvegardez le projet
en cours, puis utilisez soit le menu `Projet > Nouveau`, soit le
raccourci clavier `<Ctrl-N>` correspondant au couplage successif des
touches `Ctrl` (en bas à gauche ou à droite de votre clavier) et `N` du
clavier alphanumérique.

Retourner au [sommaire](#sommaire).

#### <a name="project_prefs"/>Onglet 'Préférences projet'

Cliquez sur l'onglet `Préférences projet` pour appliquer vos réglages
**uniquement au projet en cours** de production.

Ces réglages seront **conservés dans le fichier du projet lui-même** la
prochaine fois que vous sauvegarderez le projet (voir [plus bas](#pour-finir)) et ils seront restaurés la prochaine fois que vous
ouvrirez de nouveau ce même fichier de projet (menu `Projet > Ouvrir`
ou raccourci clavier `<Ctrl-O>`).

Les préférences projet ont toujours la **priorité** sur les préférences
générales. Chaque fois que vous ouvrez un fichier projet, ce sont les
réglages que ce fichier contient qui prennent le dessus sur les
réglages généraux en cours. *Ne vous laissez donc pas surprendre*.

**Pour revenir aux préférences générales actuelles**, cliquez sur le
[Bouton 'Réinitialiser'](#reset_button) situé tout en bas de l'outil,
puis cliquez sur le [Bouton 'OK'](#ok_button) et enfin sauvegardez le
projet en cours (voir [plus bas](#pour-finir)).

Retourner au [sommaire](#sommaire).

### <a name="tab_switch"/>Section 'Enchaînements'

La section 'Enchaînements' vous permet de régler les enchaînements
d'éléments de scénario en mode 'Switch' et en mode 'Create' (voir
[Onglet 'Scénario'](fr_tab_scenario.html) pour plus de détail).

Retourner au [sommaire](#sommaire).

#### <a name="element_frame"/>Encadré 'Élément'

L'encadré 'Élément' affiche en premier lieu l'élément de scénario
actuellement sélectionné.

Vous pouvez sélectionner un élément de scénario soit en cliquant sur le
bouton situé à droite de la liste déroulante et en choisissant un
élément dans la liste qui s'affiche, soit en cliquant directement sur
un élément de scénario se trouvant dans la zone de texte de
[l'encadré 'Aperçu'](#preview_frame).

Retourner au [sommaire](#sommaire).

#### <a name="actions_frame"/>Encadré 'Actions'

L'encadré 'Actions' affiche tous les enchaînements correspondant à
l'élément de scénario actuellement sélectionné dans
[l'encadré 'Élément'](#element_frame).

Pour bien comprendre le fonctionnement de cet outil, prenons un
exemple.

Supposons que l'élément de scénario `Personnage` soit actuellement
sélectionné (voir [illustration](#screenshot) ci-dessus).

Dans l'encadré 'Actions', nous voyons qu'il est indiqué (par
exemple)&nbsp;:

*« Avec la touche&nbsp;: `<Tab>`, Créer une nouvelle ligne de&nbsp;:
`Parenthèses` et Basculer ligne en&nbsp;: `Action`. »*

Qu'est-ce que cela signifie concrètement&nbsp;?

Lorsque le curseur d'insertion de l'éditeur de texte spécifique de
l'onglet `Scénario` de l'application se trouve sur une ligne
correspondant à l'élément `Personnage`, le fait d'appuyer sur la touche
`<Tab>` de tabulation du clavier provoque les enchaînements
suivants&nbsp;:

* si la ligne `Personnage` *N'EST PAS* vide, ajouter une nouvelle ligne
en-dessous, qui correspondra à l'élément `Parenthèses` (mode
'Create')&nbsp;;
* si la ligne `Personnage` *EST* vide, changer cette ligne `Personnage`
actuelle de sorte qu'elle devienne une ligne qui corresponde à
l'élément `Action` (mode 'Switch')&nbsp;;

Cela revient à adopter le comportement intuitif suivant&nbsp;: lorsque
je tape du texte dans mon onglet `Scénario`, si j'arrive sur une ligne
`Personnage`, je peux avoir comme alternative de transformer cette
ligne en une ligne `Action`, en pressant la touche `<Tab>` (et si la
ligne est vide) ou alors je peux immédiatement passer à la ligne
suivante, qui sera une ligne `Parenthèses`, toujours en pressant la
touche `<Tab>` et si ma ligne `Personnage` contient déjà un nom de
personnage.

Ce fonctionnement est similaire pour la touche `<Entrée>` (retour
chariot) du clavier, ainsi que pour la combinaison de touches
`<Ctrl-Entrée>` du clavier.

Dans [l'illustration](#screenshot) ci-dessus, nous pouvons lire à peu
près ceci&nbsp;: lorsque je tape du texte dans mon onglet `Scénario`,
si j'arrive sur une ligne `Personnage` et que je presse la touche
`<Entrée>`, alors que ma ligne est vide, **il ne se passera rien**
(« Basculer ligne vers : rien ») ou alors, si je presse la touche
`<Entrée>` et que ma ligne `Personnage` contient déjà un nom de
personnage, je peux immédiatement passer à la ligne suivante, qui sera
alors une ligne `Dialogue`.

De même, dans [l'illustration](#screenshot) ci-dessus, nous pouvons
lire à peu près cela&nbsp;: lorsque je tape du texte dans mon onglet
`Scénario`, si j'arrive sur une ligne `Personnage` et que je presse la
combinaison de touches `<Ctrl-Entrée>`, alors que ma ligne est vide,
**il ne se passera rien** (« Basculer ligne vers : rien ») ou alors, si
je presse `<Ctrl-Entrée>` et que ma ligne `Personnage` contient déjà un
nom de personnage, je peux immédiatement passer à la ligne suivante,
qui sera alors une ligne `Action`.

Pour modifier un enchaînement ou un autre, cliquez sur la liste
déroulante de l'action que vous souhaitez modifier, puis sélectionnez
un élément de scénario dans cette liste.

Si vous sélectionnez la ligne blanche qui se trouve en tout premier
choix dans ces listes déroulantes, cela correspond à l'action *« ne
rien faire »* (si je presse sur la touche concernée, ne rien faire).

Prenez bien soin de vérifier vos nouveaux enchaînements&nbsp;: certains
cas peuvent conduire à des impasses, qui risquent par la suite de
carrément bloquer le bon déroulement de la rédaction de votre texte de
scénario.

En cas de gros souci, vous pouvez toujours débloquer la situation en
réinitialisant tout d'abord les [préférences générales](#global_prefs)
et ensuite les [préférences projet](#project_prefs), dans cet ordre-là
et cet ordre-là seulement.

Retourner au [sommaire](#sommaire).

### <a name="looknfeel"/>Section 'Styles'

La section 'Styles' vous permet de régler l'aspect visuel de chaque
élément de scénario (voir [Onglet 'Scénario'](fr_tab_scenario.html) pour
plus de détail).

Retourner au [sommaire](#sommaire).

#### <a name="lnf_frame"/>Encadré 'Style'

L'encadré 'Style' permet de choisir la police de caractères ainsi que
diverses mises en forme à appliquer à l'élément de scénario
actuellement sélectionné dans [l'encadré 'Élément'](#element_frame).

Un élément de scénario étant avant tout un **paragraphe**, toutes les
mises en forme que vous choisirez ne pourront s'appliquer qu'à
*l'ensemble du paragraphe*, indistinctement, et non pas à certains mots
du paragraphe.

À l'heure actuelle, l'encadré 'Style' permet d'appliquer les mises en
forme suivantes&nbsp;:

* **la police** de caractères&nbsp;: choisissez la police de caractères
qui vous convient le mieux, pour l'élément de scénario actuellement
sélectionné, en cliquant sur la liste déroulante puis en cliquant sur
l'élément de liste approprié&nbsp;;

* **la taille** de la police de caractères appliquée&nbsp;: choisissez
la taille (en points d'imprimerie, pt) de la police de caractères qui
vous convient le mieux, pour l'élément de scénario actuellement
sélectionné, en cliquant sur la liste déroulante puis en cliquant sur
la taille appropriée&nbsp;;

* **le style** de la police de caractères appliquée&nbsp;: choisissez
le style (normal, gras, italique, gras italique) de la police de
caractères qui vous convient le mieux, pour l'élément de scénario
actuellement sélectionné, en cliquant sur la liste déroulante puis en
cliquant sur le style approprié&nbsp;;

* **les couleurs** de fond et d'encre du paragraphe&nbsp;: cliquez sur
le bouton approprié, puis sélectionnez une couleur dans la boîte de
dialogue qui apparaît&nbsp;;

* **l'alignement** du texte (à gauche, au centre, à droite) pour
l'élément de scénario actuellement sélectionné, en cliquant sur le
bouton approprié&nbsp;;

* **les marges** gauche et droite du paragraphe&nbsp;: choisissez la
taille de marge gauche/droite qui vous convient le mieux, pour
l'élément de scénario actuellement sélectionné, en cliquant sur la
liste déroulante idoine, puis en cliquant sur l'élément de liste
approprié.

Les nouveaux choix sont immédiatement répercutés dans
[l'encadré 'Aperçu'](#preview_frame).

Retourner au [sommaire](#sommaire).

#### <a name="preview_frame"/>Encadré 'Aperçu'

L'encadré 'Aperçu' permet non seulement de visualiser les modifications
que vous apportez dans [l'encadré 'Style'](#lnf_frame), mais aussi de
sélectionner un élément de scénario en particulier, pour lui apporter
de nouvelles modifications.

Pour sélectionner un élément de scénario, cliquez simplement sur la
ligne qui décrit l'élément dans la zone de texte de l'encadré 'Aperçu'.

L'élément est alors immédiatement sélectionné dans
[l'encadré 'Élément'](#element_frame).

Retourner au [sommaire](#sommaire).

### <a name="dialog_buttons"/>Boutons tout en bas

L'outil 'Éléments de scénario' dispose de trois boutons de dialogue
situés tout en bas, qui permettent d'accomplir les actions les plus
importantes de cet outil.

Retourner au [sommaire](#sommaire).

#### <a name="ok_button"/>Bouton 'OK'

Le bouton `OK` situé tout en bas de l'outil permet de **valider** tous
les changements que vous venez d'apporter, aussi bien du côté des
[préférences générales](#global_prefs) que du côté des
[préférences projet](#project_prefs).

Notez toutefois que&nbsp;:

* les **préférences générales** ne seront réellement sauvegardées qu'au
moment de *quitter sereinement* le logiciel `tkScenarist`&nbsp;; si
d'aventure, le logiciel venait à rencontrer une erreur (appelée aussi
'exception' dans le jargon des développeurs informaticiens), il reste
possible sinon probable que la sauvegarde ne se fasse pas
correctement&nbsp;;

* les **préférences projet** ne seront réellement sauvegardées qu'au
moment où vous déciderez de *sauvegarder vous-même* le fichier de votre
projet actuel, puisque ces préférences sont enregistrées *dans* le
fichier de votre projet.

Retourner au [sommaire](#sommaire).

#### <a name="reset_button"/>Bouton 'Réinitialiser'

L'action du bouton `Réinitialiser` situé tout en bas de l'outil dépend
entièrement de [l'onglet de préférences](#pref_tabs) dans lequel vous
vous trouvez au moment où vous cliquez dessus&nbsp;:

* si vous êtes avec [l'onglet 'Préférences générales'](#global_prefs)
sélectionné, le bouton `Réinitialiser` rétablira les **réglages par
défaut du logiciel** dans les préférences générales et les appliquera
globalement dès le prochain lancement du logiciel ou si vous utilisez
le menu `Projet > Nouveau` (raccourci clavier `<Ctrl-N>`)&nbsp;;

* si vous êtes avec [l'onglet 'Préférences projet'](#project_prefs)
sélectionné, le bouton `Réinitialiser` appliquera les préférences
générales actuelles aux préférences du projet, même si ces préférences
générales ne sont pas forcément correctes.

**Note**&nbsp;: pour se sortir d'un mauvais pas, il faut donc **tout
d'abord** réinitialiser les préférences générales et **ensuite
seulement** réinitialiser les préférences projet, dans cet ordre-là et
cet ordre-là uniquement.

Retourner au [sommaire](#sommaire).

#### <a name="cancel_button"/>Bouton 'Annuler'

Le bouton `Annuler` situé tout en bas permet de **quitter** l'outil
**sans valider** les changements que vous venez d'effectuer.

Ces changements seront par conséquent **irrévocablement perdus**.

Vous pouvez obtenir un résultat analogue en pressant la touche
`<Échap>` (ou `<Esc>`, `<Escape>`) de votre clavier.

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
