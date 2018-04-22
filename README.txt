Algorithme de Bentley-Ottmann

Notes préliminaires :

  - J'ai crée un dépot git pour pouvoir conserver les différentes versions de
    mon algorithme
  - A chaque commit j'ai détaillé les ajouts réalisés
  - Je n'ai modifié que le fichier bo.py ainsi qu'une ligne du fichier tycat.py
    afin d'afficher des points plus petits sur les images obtenues grace à tycat
  - Je me suis aidé de l'explication de l'algorithme de Bentley-Ottmann donné
    sur la page: http://geomalgorithms.com/a09-_intersect-3.html
  - Pour débuguer mon algorithme j'ai rajouté des variables locales à la
    fonction test qui permettent d'afficher chacune des informations
    différentes, j'ai aussi rajouté des méthodes permettant d'afficher le
    contenu de mes structures de données

Bilan:

L'algorithme réussit apparement à trouver les intersections de  chaque tests.
J'ai vérifié assez rapidement pour chaque fichier si il ne manquait pas
d'intersection, je n'en ai pas trouvé.

J'ai vérifié pour chaque tests si l'algorithme ne comptait pas deux fois
certaines intersections, ce n'est apparement pas le cas sauf pour les tests
triangle_0.1.bo et triangle_0.8.bo où on se rend compte facilement que certaines
intersections ont été comptés plusieurs fois. C est probablement du à une erreur
de précision.

Pour ces mêmes test on peut voir certaines intersections entre le triangle et
le quadrillage, qui sont des intersections du quadrillage. Ces intersections
sont probablement des intersections entre un segment du triangle et une des
extrémités d'un segment du quadrillage, elles ne devraient donc pas être trouvés
par l'algorithme. C est probablement du à une erreur de précision. Il est
également possible cependant que l'algorithme soit censé trouver ces points.

L'algorithme est assez rapide il s'éxécute en moins de 8 secondes pour tous
les tests, sauf pour le test random_200.bo qui s'éxécute en à peu près 30
secondes. J'effectue ces tests sur une virtual machine ayant une mémoire vive
de 2 Go, ces temps de calcul peuvent donc varier sur une autre machine.

L'algo pourrait être plus rapide si je rendais certaines structures de données
plus lourdes, que je leur rajoutais certains paramètres. Par exemple j'aurai pu
rajouter pour les cellules de la sweep_line un paramètre donnant la pente du
segment ce qui m'aurait éviter de la recalculer à chaque fois.
