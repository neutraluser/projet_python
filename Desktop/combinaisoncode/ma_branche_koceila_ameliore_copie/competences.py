class Competence:
    #dictionnaire competences = nom de l'attaque, puissance de l'attaque , defense de l'attaque , cout_chakra ,image
    competences= {
                "Feu":{
                    "attaque_1":{
                            "nom":"Boule de Feu",
                            "puissance":30,
                            "defense":10,
                            "cout_chakra":80,
                            "image_path":"image_tech/Katon-Goukakyuu-no-Jutsu.jpg"
                                },
                    "attaque_2": {
                        "nom": "Nuées Ardentes",
                        "puissance": 80,
                        "defense": 20,
                        "cout_chakra": 25,
                        "image_path": "image_tech/Katon_-_Balsamine_Pourpre.png"
                    }
                },
                "Eau":{
                            "attaque_1":{
                                    "nom":"dragon_aqueu",
                                    "puissance":100,
                                    "defense":30,
                                    "cout_chakra":40,
                                    "image_path":"image_tech/dragon_aqueu.png"
                                        },
                            "attaque_2": {
                                "nom": "Grande_Cataracte",
                                "puissance": 70,
                                "defense": 20,
                                "cout_chakra": 15,
                                "image_path": "image_tech/image_tech/Grande_Cataracte.png"
                            }
                        },

                "Foudre" :{
                    "attaque_1": {
                        "nom": "Éclair",
                        "puissance": 85,
                        "defense": 15,
                        "cout_chakra": 20,
                        "image_path": "image_tech/Foudre-Eclair.png"
                    },
                    "attaque_2": {
                        "nom": "Tempête",
                        "puissance": 95,
                        "defense": 25,
                        "cout_chakra": 30,
                        "image_path": "image_tech/Foudre-Tempete.png"
                    }

                }
    }


    def __init__(self,affinite):
        if affinite not in Competence.competences:
            raise ValueError(f"Le titre '{affinite }' n'existe pas dans les configurations.")
        config = Competence.competences[affinite]
        attaque_1=config["attaque_1"]
        attaque_2=config["attaque_2"]

        self.affinite=affinite
        self.nom_attaque1=attaque_1["nom"]
        self.puissance_attaque1 =attaque_1["puissance"]
        self.defense_attaque1 =attaque_1["defense"]
        self.cout_chakra_attaque1 =attaque_1["cout_chakra"]
        self.image_path_attaque1 =attaque_1["image_path"]

        self.nom_attaque2 = attaque_2["nom"]
        self.puissance_attaque2= attaque_2["puissance"]
        self.defense_attaque2 = attaque_2["defense"]
        self.cout_chakra_attaque2= attaque_2["cout_chakra"]
        self.image_path_attaque2= attaque_2["image_path"]
#perso1=Competence("Foudre")
#print(perso1.nom_attaque2)