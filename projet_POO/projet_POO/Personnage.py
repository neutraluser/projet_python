from competences import *
class Personnage:
    """
    Représente un personnage avec ses attributs et compétences.
    """
    def __init__(self, name, health, chakra, competences, affinite, sprite_path):
        """
        Initialise un personnage.

        Paramètres:
        ----------
        name : str
            Nom du personnage.
        health : int
            Points de vie du personnage.
        chakra : int
            Points de chakra disponibles.
        competences : list[Competence]
            Liste des compétences du personnage.
        affinite : str
            Affinité du personnage (Feu, Eau, Foudre, etc.).
        sprite_path : str
            Chemin de l'image associée pour le personnage.
        """
        self.name = name
        self.health = health
        self.chakra = chakra
        self.competences = competences
        self.affinite = affinite
        self.sprite_path = sprite_path

    def ajuster_degats(self, competence):
        """
        Ajuste les dégâts reçus en fonction de l'affinité de la compétence.
        """
        modifiers = {
            "Feu": {"Eau": 0.8, "Foudre": 1.2},
            "Eau": {"Feu": 2, "Foudre": 0.8},
            "Foudre": {"Eau": 1.1, "Feu": 0.9},
        }

        if competence.affinite in modifiers and self.affinite in modifiers[competence.affinite]:
            return competence.puissance * modifiers[competence.affinite][self.affinite]
        return competence.puissance

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
            print(f"  - {competence.nom} (Puissance : {competence.puissance}, Coût : {competence.cout_chakra})")
