

L'intérêt principal, pour le moment, est de regarder des propagations d'activation.

Manipulation : 
-modifiez à votre guise le fichier RC.dot. Attention, la forme est importante. Le fontsize doit être défini à chaque noeud car il représente l'activation (c'est très parlant sur les images). Idem dans les edges, le weight représente la proximité et le label... le label.
-dans le fichier __init__.py, rajoutez ce que vous voulez au moment où on met des tâches dans la liste de tâches. Les seules tâches qui marchent bien consistent à activer des noeuds. Ensuite, de nouvelles tâches propagent l'activation (éxécutées dans un ordre random) et on regarde ce qui se passe
-choisissez le nombre d'étapes (temps) passé en argument à la fonction work
-dans le dossier figures, vous trouvez en png l'état du réseau à chaque étape. De toutes ces figures, ON PEUT FAIRE UNE ANIMATION SOUS BEAMER POUR LA REUNION SURMYHTISSIME EN BARRES DE L'ESPACE IL FAUT QUE JE DORME UN PEU
du coup, la notion de propagation d'activation est parlante sur cet exemple

-n'hésitez pas à bidouiller le réseau pour que ça fasse un résultat joli, et dont on puisse faire une anim' pas trop mal.
