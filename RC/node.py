#!usr/bin/python3.4
# -*-coding:utf-8 -*

from numpy import log
import matplotlib.pyplot as plt


class Node:
    """Le noeud du réseau de concepts"""

    # activation entre 0 et 100
    # poids des liens entre 0 et 100

    def __init__(self, newname, impcon, activation=None):
        self.linksIn = {}
        # les liens ARRIVANT SUR LE NOEUD
        # (pour que ce soit simple à programmer)
        self.linksOut = {}
        # les liens PARTANT DU NOEUD (parce qu'il y en a besoin aussi)
        self.name = newname
        self.isObserved = False
        if activation:
            self.a = activation
        else:
            self.a = 0
            self.ic = impcon

    def existsLink(self, de):
        """existe-t-il un lien de self au noeud passé en argument ?"""
        if(de in self.linksOut):
            return(True)
        else:
            return(False)

    def addLink(self, lien, de):
        """ajouter un lien de self vers le noeud passé en argument"""
        if(de in self.linksOut):
            del self.linksOut[de]
            # il faut écraser le précédent : à tout instant,
            # il n'y a qu'un seul lien venant d'un noeud donné
        self.linksOut.update({de: lien})
        if(self in de.linksIn):
            del de.linksIn[self]
        de.linksIn.update({self: lien})

    def computeActivation(self):
        """Calcule la nouvelle activation du noeud  en fonction des autres"""
        divlog = log(3+len(self.linksIn))/log(3)
        # diviseur logarithmique qui aide à rendre compte de la connexité
        divlog = 1  # pour le moment je désactive cette possibilité...
        i = 0
        for n, l in self.linksIn.items():
            i = i+l.p*n.a
            # ne tient pas compte pour l'instant de l'activation des noeuds
            # qui sont sur les liens
        i = i/(100*divlog)  # influence des autres noeuds
        d = self.a/(100*self.ic)  # désactivation du noeud
        self.a = self.a+i-d
        self.a = min(self.a, 100)  # on ne dépasse pas la valeur 100

    def __str__(self):
        """surcharge de la méthode __str__"""
        return("{0}".format(self.name, self.ic))

    def describeLinks(self):
        """décrit tous les liens vers d'autres noeuds du RC"""
        print("Liens venant d autres noeuds : ")
        for l, n in self.linksOut.items():
            print("{0} ----> {1}".format(l, n))

    def addObserver(self, obs):
        self.isObserved = True
        self.observer = obs


class Link:
    """Lien dans le réseau de concepts"""

    def __init__(self, proximite, node=None):
        self.label = node
        self.p = proximite

    def __str__(self):
        if(self.label):
            return("Etiquette : {0}, proximite : {1}").format(self.label.name,
                                                              self.p)
        else:
            return("proximite : {0}").format(self.p)


class NodeObserver:

    def __init__(self):
        self.times = []  # liste d'instants où le noeud est modifié
        self.activations = []
        # liste d'activations successives (c'est ça qu'on observe)

    def update(self, time, activation):
        self.times.append(time)
        self.activations.append(activation)

    def draw(self):
        # trace un graphe mignon de l'activation en fonction du temps
        print(self.times)
        print(self.activations)
        plt.figure()
        plt.plot(self.times, self.activations)
        plt.show()


# test des classes
if __name__ == "__main__":
    elephant = Node("elephant", 5, 0)

    print(elephant)

    nd = NodeObserver()
    nd.update(1, 2)
    nd.update(2, 4)
    nd.update(3, 6)
    # nd.draw()
