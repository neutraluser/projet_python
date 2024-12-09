class Personnage:
    """
    Représente un personnage avec ses attributs et compétences.
    """
    def __init__(self, name, health, chakra, competences, affinite,sprite_path):
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
        """
        self.name = name
        self.health = health
        self.chakra = chakra
        self.competences = competences
        self.affinite = affinite
        self.sprite_path = sprite_path

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

