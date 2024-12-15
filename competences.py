class Competence:
    competences = {
        "Feu": {
            "attaque_1": {
                "nom": "Boule de Feu",
                "puissance": 30,
                "defense": 10,
                "cout_chakra": 80,
                "image_path": "image_tech/Katon-Goukakyuu-no-Jutsu.jpg",
                "zone": 3,  # portée
                "aoe": 1    # rayon AoE autour de la case ciblée
            },
            "attaque_2": {
                "nom": "Nuées Ardentes",
                "puissance": 80,
                "defense": 20,
                "cout_chakra": 25,
                "image_path": "image_tech/Katon_-_Balsamine_Pourpre.png",
                "zone": 5,
                "aoe": 2
            },
            "vitesse": 3
        },
        "Eau": {
            "attaque_1": {
                "nom": "Dragon Aqueu",
                "puissance": 100,
                "defense": 30,
                "cout_chakra": 40,
                "image_path": "image_tech/dragon_aqueu.png",
                "zone": 4,
                "aoe": 2
            },
            "attaque_2": {
                "nom": "Grande Cataracte",
                "puissance": 70,
                "defense": 20,
                "cout_chakra": 15,
                "image_path": "image_tech/Grande_Cataracte.png",
                "zone": 6,
                "aoe": 1
            },
            "vitesse": 5
        },
        "Foudre": {
            "attaque_1": {
                "nom": "Éclair",
                "puissance": 85,
                "defense": 15,
                "cout_chakra": 20,
                "image_path": "image_tech/Foudre-Eclair.png",
                "zone": 2,
                "aoe": 1
            },
            "attaque_2": {
                "nom": "Tempête",
                "puissance": 95,
                "defense": 25,
                "cout_chakra": 30,
                "image_path": "image_tech/Foudre-Tempete.png",
                "zone": 4,
                "aoe": 2
            },
            "vitesse": 10
        }
    }

    def __init__(self, affinite):
        if affinite not in Competence.competences:
            raise ValueError(f"L'affinité '{affinite}' n'existe pas.")
        config = Competence.competences[affinite]
        attaque_1 = config["attaque_1"]
        attaque_2 = config["attaque_2"]
        vitesse = config["vitesse"]

        self.affinite = affinite
        self.nom_attaque1 = attaque_1["nom"]
        self.puissance_attaque1 = attaque_1["puissance"]
        self.defense_attaque1 = attaque_1["defense"]
        self.cout_chakra_attaque1 = attaque_1["cout_chakra"]
        self.image_path_attaque1 = attaque_1["image_path"]
        self.zone_attaque1 = attaque_1["zone"] # portée
        self.aoe_attaque1 = attaque_1["aoe"]   # AoE radius

        self.nom_attaque2 = attaque_2["nom"]
        self.puissance_attaque2 = attaque_2["puissance"]
        self.defense_attaque2 = attaque_2["defense"]
        self.cout_chakra_attaque2 = attaque_2["cout_chakra"]
        self.image_path_attaque2 = attaque_2["image_path"]
        self.zone_attaque2 = attaque_2["zone"]
        self.aoe_attaque2 = attaque_2["aoe"]

        self.vitesse = vitesse

        # Compétence de soin commune
        self.nom_sort_soin = "Sort de Soin"
        self.puissance_sort_soin = 0
        self.cout_chakra_sort_soin = 30
        self.image_path_sort_soin = "sort_soin.png"
