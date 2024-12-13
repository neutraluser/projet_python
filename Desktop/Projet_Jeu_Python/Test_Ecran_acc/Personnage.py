from competences import *
from unit import *

class Personnage:
    """
    Représente un personnage avec ses attributs et compétences.
    """
    def __init__(self, name, health, chakra, affinite,image):
        self.name = name
        self.health = health
        self.chakra = chakra
        self.competences = Competence(affinite)
        self.affinite = affinite
        self.image =image

    def afficher_statistiques(self):
        """
        Affiche les statistiques du personnage.
        """
        print(f"Nom : {self.name}")
        print(f"PV : {self.health}")
        print(f"Chakra : {self.chakra}")
        print(f"Affinité : {self.affinite}")
        print("Compétences :")
        for competence in self.competences:
            print(f"  - {competence.nom_attaque1} (Puissance : {competence.puissance_attaque1}, Coût : {competence.cout_chakra_attaque1})")
            print(
                f"  - {competence.nom_attaque2} (Puissance : {competence.puissance_attaque2}, Coût : {competence.cout_chakra_attaque2})")

