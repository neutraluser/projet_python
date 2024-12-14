class Competence:
    def __init__(self, *, nom, puissance, defense, cout_chakra, image_path,affinite=None):
        """
        Initialise une compétence.

        Paramètres:
        ----------
        nom : str
            Nom de la compétence.
        puissance : int
            Puissance d'attaque.
        defense : int
            Puissance de défense.
        cout_chakra : int
            Coût en chakra.
        image_path : str
            Chemin de l'image associée.
        """
        self.nom = nom
        self.puissance = puissance
        self.defense = defense
        self.cout_chakra = cout_chakra
        self.image_path = image_path
        self.affinite=affinite