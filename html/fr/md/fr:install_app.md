
# Installation du logiciel

## <a name="sommaire"/>Sommaire

* [Télécharger tkScenarist](#download)
    * [Versions officielles](#versions-officielles)
    * [Daily build](#daily-build)
    * [Fork et pull requests](#fork-et-pull-requests)
* [Installer tkScenarist](#install)
    * [En général](#general)
    * [Pré-requis](#pre-requisites)
    * [UNIX/Linux](#unixlinux)
    * [MS-Windows&trade;](#ms-windows)
    * [Signaler un problème](#bug-report)
* [Premiers pas avec tkScenarist](#getting_started)
    * [Lancer l'application](#launching_app)
        * [Dans MS-Windows&trade;](#dans-ms-windows)
        * [Dans UNIX/Linux](#dans-unixlinux)
    * [Comment s'organise tkScenarist](#organisation)
    * [Aller plus loin](#aller-plus-loin)
* [Navigation rapide](#navigation-rapide)


## <a name="download"/>Télécharger tkScenarist

### Versions officielles

Il est fortement recommandé aux utilisateurs de `tkScenarist` de ne
télécharger que les **versions officielles** du logiciel.

Ces versions ont généralement été testées et validées autant que faire
se peut. Elles devraient donc être opérationnelles, au moins dans les
limites des options qu'elles proposent au moment où elles les proposent
(en fonction du numéro de version, justement).

Il est clair que plus le numéro de version choisi sera élevé et plus le
logiciel vous offrira de possibilités ou de corrections de bogues.

Vous trouverez dans **GitHub** une page nommée [Releases](https://github.com/tarball69/tkScenarist/releases) dans laquelle vous
aurez toutes les versions officielles listées et classées de la version
**la plus récente** (plus grand numéro de version) à la version **la
plus ancienne** (plus petit numéro de version).

À chaque numéro de version, vous trouverez un lien hypertexte nommé
`zip` et un autre lien hypertexte (à côté) nommé `tar.gz`, qui
correspondent tous deux au type d'archive compressée que vous pouvez
télécharger pour cette version officielle.

Cliquez sur le format d'archive que vous souhaitez télécharger,
attendez que le téléchargement se termine.

> Dans le doute, cliquez toujours sur le lien nommé `zip`, qui
correspond à une archive ZIP standard (format très répandu) de la
version officielle.

Dézippez ensuite l'archive téléchargée en local sur votre disque dur à
l'aide du gestionnaire d'archives de votre système ou à l'aide d'un
logiciel approprié e.g. 7-zip, PKZip, etc.

Retourner au [sommaire](#sommaire).

### Daily build

Si vous vous sentez l'âme d'un explorateur, vous pouvez toujours tester
les versions `daily build` du logiciel en cliquant sur le bouton
**Download ZIP** situé [à droite de la page projet GitHub](https://github.com/tarball69/tkScenarist).

**ATTENTION** : les versions `daily build` ne sont *PAS* des versions
officielles ! Vous les utilisez en connaissance de cause et à vos
risques et périls.

Retourner au [sommaire](#sommaire).

### Fork et pull requests

Les développeurs de logiciels souhaitant contribuer au projet pourront
faire un **[fork](https://help.github.com/articles/fork-a-repo)**,
puis des **[pull requests](https://help.github.com/articles/using-pull-requests/)** selon la
(les) contribution(s) qu'ils souhaiteront apporter.

Retourner au [sommaire](#sommaire).


## <a name="install"/>Installer tkScenarist

### <a name="general"/>En général

Ce logiciel n'a *PAS* besoin d'être installé, de quelque manière que ce
soit.

Il vous suffit de le [télécharger](#download) à la page
[Releases](https://github.com/tarball69/tkScenarist/releases) du projet
GitHub, de dézipper l'archive téléchargée et de l'utiliser
immédiatement.

Bien sûr, dans l'idéal, vous prendrez la précaution de copier le
dossier obtenu dans l'un de vos dossiers préférés &ndash; par exemple
dans un répertoire nommé `apps` &ndash; sachant qu'un logiciel qui
traîne dans le dossier des téléchargements a toutes les chances de se
faire supprimer accidentellement.

Retourner au [sommaire](#sommaire).

### <a name="pre-requisites"/>Pré-requis

Ce logiciel ne peut fonctionner que si **Python3** et **Tkinter** sont
correctement installés sur votre machine.

En revanche, il n'y a **pas d'autres dépendances** que ces deux
pré-requis.

Python3 est le langage de programmation utilisé par le logiciel
`tkScenarist` et Tkinter sa bibliothèque graphique, généralement
installée **par défaut** avec le langage Python3.

Si jamais vous obtenez un message d'erreur du type **ImportError** dans
la fenêtre noire (console) qui apparaît lors du lancement du logiciel,
c'est qu'il y a de fortes chances pour que vous essayiez de lancer le
programme avec **Python2** et non pas son grand frère **Python3**. Il
peut arriver parfois aussi que la bibliothèque Tkinter soit mal
installée, bien que ce soit rare.

Quoi qu'il en soit, n'hésitez pas à vous faire aider sur les forums
d'entraide appropriés (par exemple : [developpez.com](http://www.developpez.net/forums/f96/autres-langages/python-zope/)).

Notez que l'installation de Python3 à côté de Python2 ne pose
généralement aucun problème particulier.

Vous pouvez télécharger et installer Python3 à partir de cette
adresse&nbsp;:

https://www.python.org/downloads/ (Ctrl+clic: nouvel onglet)

Retourner au [sommaire](#sommaire).

### UNIX/Linux

La plupart des distributions Linux populaires e.g. Ubuntu, Debian,
SuSE, etc. ont déjà une **pré-installation** de Python3/Tkinter.

Si vous êtes dans ce cas, **n'essayez pas** d'installer Python3/Tkinter
manuellement, non seulement c'est totalement inutile, mais de plus,
cela pourrait mettre une sacrée grouille dans votre système.

Dans un tel cas, il vous suffit de [télécharger](#download) une
version officielle de `tkScenarist`, de la dézipper et de l'utiliser
immédiatement.

Retourner au [sommaire](#sommaire).

### MS-Windows&trade;

Plusieurs usagers de MS-Windows&trade; ont fait remarquer qu'ils ont
une console MS-DOS noire qui apparaît au lancement du logiciel.

Cette fenêtre particulièrement disgracieuse peut même parfois être
carrément gênante.

Il s'agit cependant d'un comportement propre au langage Python sous
MS-Windows&trade; et **cela n'a rien d'anormal**.

Toutefois, si vous souhaitez vous débarrasser de cette console noire,
il vous suffit de changer l'extension du fichier `.py` en `.pyw` puis
de lancer à nouveau votre logiciel favori pour ne plus être embêté(e).

Dans le cas ici présent, cela revient à renommer le fichier
`tkscenarist.py` en `tkscenarist.pyw`, puis de relancer le programme
pour que cela fonctionne sans console.

Retourner au [sommaire](#sommaire).

### <a name="bug-report"/>Signaler un problème

Quoi qu'il en soit, si vous rencontrez des problèmes à l'installation
ou durant l'utilisation de `tkScenarist`, merci de le signaler en
postant un message sur le **[bugtracker](https://github.com/tarball69/tkScenarist/issues)** du projet GitHub.

Retourner au [sommaire](#sommaire).


## <a name="getting_started"/>Premiers pas avec tkScenarist

### <a name="launching_app"/>Lancer l'application

#### Dans MS-Windows&trade;

Une fois le dossier `tkScenarist-...` dézippé et copié en lieu sûr,
double-cliquez simplement sur le fichier `tkscenarist.py` qui se trouve
dedans pour lancer l'application.

**Nota Bene** : si vous avez suivi les instructions concernant la
[console noire](#ms-windows) qui apparaît au lancement du programme,
vous devrez dès lors double-cliquer sur le fichier renommé
`tkscenarist.pyw` et non plus sur le fichier `tkscenarist.py`
d'origine.

Retourner au [sommaire](#sommaire).

#### Dans UNIX/Linux

Une fois le dossier `tkScenarist-...` dézippé et copié en lieu sûr,
cliquez simplement sur le fichier `tkscenarist.py` qui se trouve dedans
(si le sticky bit 'executable' autorise l'exécution du fichier tel
quel) pour lancer l'application.

Si cela ne donne rien, ouvrez une console shell et tapez :

```sh
    $ cd /emplacement/du/fichier # à remplacer, évidemment.
    $ python3 tkscenarist.py
```

**Exemple concret&nbsp;:** en supposant que vous avez copié le dossier
`tkScenarist/` dans votre répertoire favori `~/apps/`, cela
donne&nbsp;:

```sh
    $ cd ~/apps/tkScenarist
    $ python3 tkscenarist.py
```
Retourner au [sommaire](#sommaire).

##### Sticky bit 'executable'

Si vous souhaitez rendre `tkScenarist` automatiquement exécutable, il
vous suffit de faire un `chmod +x` sur le fichier concerné.

**Exemple concret&nbsp;:** en supposant que vous avez copié le dossier
`tkScenarist/` dans votre répertoire favori `~/apps/`, cela
donne&nbsp;:

```sh
    $ cd ~/apps/tkScenarist
    $ chmod +x tkscenarist.py
```

À partir de là, vous pourrez lancer `tkScenarist` directement en
(double) cliquant sur le fichier `tkscenarist.py` dans votre
gestionnaire de fichiers habituel.

Retourner au [sommaire](#sommaire).

### <a name="organisation"/>Comment s'organise tkScenarist ?

Le logiciel `tkScenarist` utilise un système d'onglets vous permettant
d'avoir accès à tous les éléments essentiels d'un projet de film dès le
premier coup d'oeil.

L'ordre des onglets est basé sur l'attitude intuitive et naturelle du
scénariste, qui consiste à&nbsp;:

1. trouver un titre pour le projet de film&nbsp;;
1. trouver un sous-titre, voire un sous-sous-titre pour l'épisode, s'il
s'agit d'une série (facultatif)&nbsp;;
1. mettre sur un brouillon toutes les idées qui pourraient aider à
formaliser le projet&nbsp;;
1. écrire un pitch ou au moins un concept sur ce que l'on veut
faire&nbsp;;
1. gérer les personnages du film, notamment leur histoire personnelle
et les relations qu'ils entretiennent les uns avec les autres;
1. écrire le scénario lui-même, une fois que l'on sait un peu mieux où
l'on va&nbsp;;
1. écrire le découpage technique (storyboard), une fois que le scénario
est finalisé&nbsp;;
1. gérer les disponibilités des ressources qui participeront
éventuellement à la réalisation du projet cinématographique final.

En plus de ces onglets viennent s'ajouter quelques outils destinés à
vous faciliter la tâche&nbsp;:

* une base de données de noms provenant de toutes origines, avec
possibilité d'effectuer des recherches multiples&nbsp;;
* un gestionnaire de modèles d'histoires ou de pitchs, qui vous permet
de récupérer des modèles écrits par des tiers, voire de rédiger vos
propres modèles, soit pour les exploiter personnellement, soit pour les
partager avec d'autres&nbsp;;
* un éditeur de styles (look'n'feel) pour agrémenter votre éditeur de
scénario de réglages plus fins que ceux livrés en standard.

Notez toutefois que les réglages que vous apporterez à votre éditeur de
scénario n'impacteront **en aucune manière** la production de votre
scénario au format PDF. En effet, la mise en forme du scénario, en vue
d'une impression pour présentation à un éventuel producteur
professionnel, obéit à des règles de métier assez strictes. Ne vous
étonnez donc pas de voir le document PDF se construire toujours de la
même façon.

Retourner au [sommaire](#sommaire).

### Aller plus loin

Si vous souhaitez en savoir plus sur l'utilisation du logiciel
`tkScenarist`, n'hésitez pas à compulser la **[documentation wiki](https://github.com/tarball69/tkScenarist/wiki/Accueil)** disponible en
ligne.

Elle contient en théorie tout ce dont vous auriez besoin de savoir pour
bien utiliser ce logiciel.

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
