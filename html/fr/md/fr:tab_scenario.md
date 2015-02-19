
# L'application par ses onglets

## <a name="onglet-scenario"/>Onglet 'Scénario'

## <a name="sommaire"/>Sommaire

* [Aperçu](#screenshot)
* [Présentation](#introduction)
* [Utilisation](#utilisation)
    * [Le navigateur de scènes](#navigation)
    * [L'éditeur texte de scénario](#editor)
        * [Composition](#composition)
        * [Éléments de scénario](#elements)
        * [Enchaînements d'éléments](#switch_create)
        * [Détection de noms de personnages](#characters)
        * [Fonctionnalités d'édition](#features)
    * [La zone d'information](#information)
* [Pour finir](#pour-finir)
* [Navigation rapide](#navigation-rapide)


## <a name="screenshot"/>Aperçu

![image](../../images/screenshots/fr/screenshot-008.png)

Retourner au [sommaire](#sommaire).


## <a name="introduction"/>Présentation

Cet onglet permet de rédiger le scénario du projet de film à proprement
parler.

Il se compose de **trois zones** principales&nbsp;:

1. à gauche, le **navigateur de scènes**, qui permet d'accéder aux
lignes où se trouvent les scènes d'un clic de souris&nbsp;;
1. au centre, l'**éditeur texte de scénario**, qui est un peu plus
qu'un simple éditeur de texte brut&nbsp;;
1. à droite, la **zone d'information**, qui affiche des conseils, des
historiques de personnages en fonction de ce qui est détecté dans le
texte du scénario, ainsi que quelques statistiques estimatives.

Toutes les zones sont **redimensionnables**&nbsp;: il suffit de placer
la flèche de la souris entre les zones, l'icône du pointeur doit alors
changer d'aspect (e.g. deux flèches qui s'opposent), de maintenir le
clic enfoncé puis de déplacer dans le sens indiqué par le pointeur de
souris pour obtenir le redimensionnement escompté.

Retourner au [sommaire](#sommaire).


## <a name="utilisation"/>Utilisation

### <a name="navigation"/>Le navigateur de scènes

Le navigateur de scènes se remplit automatiquement au fur et à mesure
que vous rédigez des nouvelles scènes dans votre texte de scénario.

Pour accéder à une scène donnée, cliquez simplement sur la scène en
question dans la liste déroulante du navigateur de scènes, le curseur
d'insertion de l'éditeur texte de scénario se rendra alors à l'endroit
désiré.

Retourner au [sommaire](#sommaire).

### <a name="editor"/>L'éditeur texte de scénario

#### <a name="composition"/>Composition

L'éditeur texte de scénario se compose de trois parties&nbsp;:

1. un **sélecteur d'éléments** de scénario, qui permet de changer le
type d'élément de scénario affecté à la ligne où se trouve actuellement
le curseur d'insertion (voir [Éléments de scénario](#elements) un peu
plus bas)&nbsp;;
1. un **indicateur d'enchaînements**, qui permet de connaître toutes les
alternatives d'enchaînement à tout moment (voir
[Enchaînements&nbsp;d'éléments](#switch_create) un peu plus
bas)&nbsp;;
1. l'**éditeur texte** de scénario à proprement parler, qui est
l'organe principal de la rédaction du texte de scénario.

Sauf indication contraire, toute mention 'éditeur', 'éditeur texte' ou
'éditeur texte de scénario' dans cette page de documentation se réfère
systématiquement à l'objet éditeur de texte de l'onglet 'Scénario'.

Le sélecteur d'éléments de scénario et l'indicateur d'enchaînements
seront mentionnés explicitement.

Retourner au [sommaire](#sommaire).

#### <a name="elements"/>Éléments de scénario

L'écriture d'un scénario suit des règles de métier qui permettent
d'identifier les différents paragraphes sous la forme d'**éléments de
scénario**.

Il en existe beaucoup, mais le logiciel `tkScenarist` a fait le choix
de ne garder que l'essentiel&nbsp;:

1. élément 'Scène'&nbsp;: ce paragraphe permet d'identifier sans
ambiguïté le début d'une scène&nbsp;;
1. élément 'Action'&nbsp;: ce paragraphe décrit une action au sein
d'une scène&nbsp;;
1. élément 'Personnage'&nbsp;: ce paragraphe indique qu'un personnage
prend la parole, c'est donc théoriquement le début d'un dialogue&nbsp;;
1. élément 'Parenthèses'&nbsp;: ce paragraphe sert de complément
d'information sur l'état du personnage au moment où il prend la parole
e.g. en souriant, en triturant nerveusement ses mèches de cheveux, en
compulsant le dossier, etc&nbsp;;
1. élément 'Dialogue'&nbsp;: c'est le texte du dialogue à proprement
parler, ce que dit le personnage signalé dans l'élément 'Personnage',
qui doit obligatoirement précéder l'élément 'Dialogue'&nbsp;;
1. élément 'Transition'&nbsp;: ce paragraphe permet de donner des
indications techniques sur la transition attendue par le scénariste
entre deux scènes e.g. CUT, FADE IN, FADE OUT, etc. On place
généralement un élément 'Transition' juste avant ou juste après un
élément 'Scène'.

Seuls les cinq premiers éléments sont vraiment indispensables à la
rédaction correcte d'un scénario.

Le sixième élément, 'Transition', est un petit plus dont on se gardera
d'abuser, surtout si l'on veut approcher une qualité optimale de
rédaction d'un scénario à vocation professionnelle.

Pour changer le type d'élément de scénario à un endroit donné de votre
texte, placez le curseur d'insertion sur le paragraphe à modifier,
cliquez sur le bouton (montrant une petite flèche vers le bas) situé à
droite du **sélecteur d'éléments** de scénario pour dérouler une liste
de choix, puis sélectionnez l'élément qui vous intéresse dans cette
liste de choix.

L'aspect du paragraphe s'adapte alors automatiquement à votre demande.

La plupart du temps, vous pouvez aussi recourir aux
[Enchaînements&nbsp;d'éléments](#switch_create) pour obtenir des
résultats analogues.

Notez toutefois qu'il est fortement recommandé&nbsp;:

* de débuter le texte d'un scénario par un élément 'Scène', ce que vous
propose par défaut le logiciel `tkScenarist`&nbsp;;
* de *NE PAS* abuser des éléments 'Transition', surtout si votre
scénario est à vocation professionnelle (c'est en effet le boulot du
storyboarder de s'occuper de l'aspect découpage technique de
l'histoire, pas celui du scénariste)&nbsp;;
* de toujours commencer un dialogue par l'élément 'Personnage', suivi
de l'élément 'Parenthèses' (facultatif), puis de l'élément 'Dialogue'
(obligatoire)&nbsp;;
* de prendre l'habitude de rédiger une action en conjuguant les verbes
à l'indicatif présent.

Retourner au [sommaire](#sommaire).

#### <a name="switch_create"/>Enchaînements d'éléments

L'**indicateur d'enchaînements** affiche les différents types
d'éléments de scénario que vous pouvez obtenir en pressant sur les
touches d'enchaînement citées&nbsp;:

* la touche `<Tab>` ou tabulation, qui se trouve à gauche de votre
clavier alphanumérique (souvent représentée par deux longues flèches
qui s'opposent et qui viennent buter sur des taquets)&nbsp;;
* la touche `<Entrée>` ou retour chariot, qui se trouve à droite de
votre clavier alphanumérique (souvent représentée par une flèche coudée
imitant le mouvement du retour de chariot d'une machine à
écrire)&nbsp;;
* la combinaison de touches `<Ctrl-Entrée>` qui correspond au couplage
successif de la touche `Ctrl` (en bas à gauche ou à droite du clavier)
et de la touche `Entrée`.

**Attention**&nbsp;: ne confondez pas la touche `<Entrée>` du clavier
**alphanumérique** avec la touche du même nom du clavier **numérique**,
le logiciel `tkScenarist` ne reconnaît que la première en ce qui
concerne les fonctionnalités d'enchaînement, la seconde étant
neutralisée afin d'éviter d'éventuelles erreurs de saisie.

L'indicateur d'enchaînements fonctionne selon deux modes&nbsp;:

1. le mode 'Switch' (basculement)&nbsp;: lorsqu'une ligne de paragraphe
sélectionnée est encore vide, l'appui d'une touche d'enchaînement
provoquera le **basculement** de la ligne sélectionnée vers le type
d'élément de scénario affiché dans l'indicateur d'enchaînements e.g. si
vous êtes sur une ligne 'Action' vierge et que vous pressez la touche
`<Tab>` de votre clavier, la ligne basculera en type
'Personnage'&nbsp;;
1. le mode 'Create' (nouvelle ligne)&nbsp;: dès qu'une ligne de
paragraphe sélectionnée n'est plus vide i.e. qu'elle contient au moins
une lettre ou un signe, l'appui d'une touche d'enchaînement provoquera
la **création** d'une nouvelle ligne de paragraphe à la suite, avec le
type d'élément spécifié par l'indicateur d'enchaînements e.g. si vous
êtes sur une ligne 'Scène' non vide et que vous pressez la touche
`<Entrée>` de votre clavier, une nouvelle ligne de type 'Action'
viendra se créer à la suite.

L'indicateur d'enchaînements étant à **affichage dynamique permanent**,
n'hésitez pas à le consulter avant de presser une touche d'enchaînement
sur votre clavier, afin de vous assurer de bien obtenir l'élément de
scénario souhaité.

**Note**&nbsp;: vous pouvez redéfinir les enchaînements grâce à l'outil
[Éléments de scénario](fr_tools_scenario_elements_editor.html).

Retourner au [sommaire](#sommaire).

#### <a name="characters"/>Détection de noms de personnages

Le logiciel `tkScenarist` est doté d'un algorithme de détection de noms
de personnages suffisamment fin pour reconnaître y compris des **noms
longs composés** e.g. 'PIERRE-HENRI DE MORTE-FONTAINE CHÂTEAUROUX'.

Lorsque vous commencez à saisir dans l'éditeur texte de scénario le nom
d'un personnage **déjà déclaré** dans la liste des noms de personnages
de [l'onglet 'Personnages'](fr_tab_characters.html), l'algorithme ouvre une
petite fenêtre jaune sous le curseur d'insertion et vous propose tous
les noms susceptibles de correspondre à ce que vous avez commencé de
taper au clavier.

Avec les flèches `<Haut>` (&nbsp;&uarr;&nbsp;) et `<Bas>`
(&nbsp;&darr;&nbsp;) du clavier, vous pouvez vous déplacer dans cette
liste de choix pour sélectionner le nom qui vous intéresse.

Pressez ensuite la touche `<Entrée>` de votre clavier (ou `<Tab>`, au
choix) pour insérer le nom choisi dans le texte du scénario.

Vous pouvez aussi double-cliquer avec la souris sur le nom choisi dans
la liste pour l'insérer dans le texte du scénario.

Les noms de personnages sont toujours insérés en *MAJUSCULES*&nbsp;:
cela correspond à une règle du métier, qui veut que les noms des
personnages soient toujours cités en toutes majuscules dans un script
de scénario.

Notez par la même occasion que si vous avez renseigné l'historique du
personnage au préalable, ce texte s'affichera automatiquement dans la
**zone d'information** située à droite, au moment de l'insertion du nom
choisi.

Il en va de même si vous placez le curseur d'insertion n'importe où
dans le texte où se trouve un nom de personnage reconnaissable par
l'algorithme de détection de noms de personnages&nbsp;: son historique,
s'il est renseigné, s'affichera pour vous apporter un complément
d'information sur le personnage désigné par le curseur d'insertion.

Il existe aussi une autre fonctionnalité de détection de noms de
personnages.

Si, par exemple, vous n'avez pas souhaité déclarer vos noms de
personnages dans [l'onglet 'Personnages'](fr_tab_characters.html), vous
pouvez malgré tout citer un nom de personnage **lors d'un dialogue**
(avec l'élément de scénario 'Personnage'), celui-ci sera alors
automatiquement ajouté à la liste des noms de personnages de l'onglet
'Personnages', accompagné d'un historique vide, que vous aurez tout le
loisir de renseigner par la suite.

Il va de soi que si vous avez utilisé dans le texte du scénario un nom
de personnage non reconnu par l'algorithme, par exemple parce que non
déclaré au préalable dans la liste des noms de personnages ou non
déclaré au cours d'un dialogue, ce nom *NE SERA PAS* automatiquement
formaté en toutes majuscules comme l'exigerait la règle métier,
l'algorithme de détection ne pouvant savoir par avance si vous citez un
mot quelconque, un nom commun ou autre chose (pas d'analyse sémantique
du texte saisi).

En revanche, une fois que le nom de personnage est déclaré et reconnu
par l'algorithme de détection de noms de personnages, il vous suffit de
placer le curseur d'insertion sur le nom de personnage non formaté dans
le texte pour que celui-ci soit immédiatement reconnu et reformaté,
conformément aux règles du métier.

Retourner au [sommaire](#sommaire).

#### <a name="features"/>Fonctionnalités d'édition

L'éditeur texte de scénario propose &ndash; entre autres &ndash; les
fonctionnalités d'édition suivantes&nbsp;:

* vous pouvez déplacer le curseur d'insertion avec les flèches `<Haut>`
(&nbsp;&uarr;&nbsp;), `<Bas>` (&nbsp;&darr;&nbsp;), `<Gauche>`
(&nbsp;&larr;&nbsp;) et `<Droite>` (&nbsp;&rarr;&nbsp;) de votre
clavier&nbsp;;
* vous pouvez placer le curseur d'insertion n'importe où dans le texte
en cliquant simplement avec la souris à l'endroit désiré&nbsp;;
* un double-clic sur un mot permet de sélectionner **ce mot
uniquement**&nbsp;;
* un triple-clic sur un mot permet de sélectionner **le paragraphe** où
se trouve ce mot&nbsp;;
* le menu `Edition > tout sélectionner` ou la combinaison de touches de
clavier `<Ctrl-A>` ont le même effet qu'un triple-clic sur un
mot&nbsp;;
* vous pouvez aussi sélectionner une portion de texte à la
souris&nbsp;;
* tout ruban de sélection est susceptible d'être remplacé par la
prochaine frappe d'une touche au clavier&nbsp;;
* la combinaison de touches de clavier `<Ctrl-Effacer>` supprime **un
mot entier** en arrière&nbsp;;
* la combinaison de touches de clavier `<Ctrl-Suppr>` supprime **un mot
entier** en avant&nbsp;;
* la combinaison de touches de clavier `<Ctrl-Z>` permet d'annuler la
dernière opération en date. Attention&nbsp;: cette fonctionnalité est
encore **expérimentale**, elle n'est pas garantie de fonctionner à
100% dans tous les cas de figure&nbsp;;
* la combinaison de touches de clavier `<Ctrl-Shitf-Z>` permet de
répéter la dernière opération annulée. Attention&nbsp;: cette
fonctionnalité est encore **expérimentale**, elle n'est pas garantie de
fonctionner à 100% dans tous les cas de figure&nbsp;;

Il existe d'autres fonctionnalités moins habituelles, qu'il serait sans
doute trop long (et bien inutile) de lister ici.

Retourner au [sommaire](#sommaire).

### <a name="information"/>La zone d'information

La zone d'information affiche des conseils automatiques, des
informations historiques sur le personnage reconnu par le curseur
d'insertion de l'éditeur texte de scénario, si ce curseur est placé sur
un nom de personnage, ainsi que quelques statistiques estimatives pour
avoir un ordre d'idée de l'état d'avancement du projet.

Attention, les données statistiques affichées ici ne sont vraiment que
des **estimations**&nbsp;: elles ne doivent pas être prises pour
référence.

Seules les données récapitulatives du document PDF&reg; du scénario
sont vraiment fiables.

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