import pygame
class Map:
    # Dictionnaire des configurations prédéfinies
    configurations = {
        "Map1": {
            "track": "track/Sonic 1 Music Marble Zone.mp3",
            "fond": "maps/lengendary.png",
            "Liste_obstacles":[[1, 5], [1, 4], [1, 3], [1, 2], [1, 1], [1, 0], [4, 0], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [1, 13], [0, 13], [7, 13], [3, 22], [4, 22], [20, 19], [21, 19], [22, 19], [23, 18], [20, 18], [20, 17], [21, 17], [22, 17], [16, 1], [16, 2], [16, 3], [16, 4], [16, 5], [18, 5], [18, 4], [18, 3], [18, 2], [18, 1], [38, 12], [38, 11], [38, 10], [37, 10], [37, 11], [37, 16], [36, 16], [36, 15],[35, 16], [34, 16], [33, 16], [34, 15], [34, 14], [34, 13], [35, 13], [35, 14], [36, 14],  [51, 12], [51, 11], [51, 10], [51, 9], [51, 8], [51, 7], [51, 6], [51, 5], [51, 4], [52, 4], [53, 4], [54, 4], [54, 3], [55, 3], [56, 3], [57, 3], [58, 3], [59, 3], [59, 4], [60, 4], [61, 4], [62, 4], [63, 4], [63, 5], [63, 6], [63, 7], [63, 8], [63, 9], [63, 10], [63, 11], [63, 12], [62, 12], [61, 12], [60, 12], [59, 12], [58, 12], [57, 12], [56, 12], [55, 12], [54, 12], [53, 12], [52, 12], [53, 29], [53, 28], [52, 28], [52, 27], [52, 26], [53, 26], [54, 26], [54, 27], [54, 28], [48, 34], [47, 34], [47, 33], [48, 33], [49, 33], [49, 32], [48, 32], [47, 32], [49, 38], [49, 37], [50, 37], [50, 36], [50, 35], [49, 35], [48, 35], [48, 36], [48, 37], [52, 37], [52, 36], [53, 36], [53, 35], [53, 34], [52, 34], [51, 34], [51, 35], [36, 36], [37, 36], [38, 36], [38, 37], [38, 38], [38, 39], [38, 40], [37, 40], [36, 40], [35, 40], [35, 39], [35, 38], [35, 37], [36, 37], [37, 37], [37, 38], [36, 38], [31, 40], [31, 39], [31, 38], [31, 37], [31, 36], [30, 36], [29, 36], [28, 36], [28, 37], [28, 38], [28, 39], [28, 40], [29, 40], [30, 40], [30, 39], [29, 39], [29, 38], [29, 37], [65, 11], [65, 12], [65, 13], [65, 14], [65, 15], [65, 16], [65, 17], [65, 18], [66, 18], [67, 18], [68, 18], [69, 18], [70, 18], [70, 17], [70, 16], [70, 15], [70, 14], [70, 13], [70, 12], [70, 11], [69, 11], [68, 11], [67, 11], [66, 11], [50, 7], [45, 7], [45, 6], [45, 5], [45, 4], [46, 4], [46, 3], [47, 3], [48, 3], [48, 4], [48, 5], [48, 6], [48, 7], [47, 7], [47, 6], [47, 5], [46, 5], [38, 5], [37, 5]]
,
            "Liste_vide":[[9, 6], [13, 22], [41, 26], [0, 39], [1, 39], [2, 39], [3, 39], [4, 39], [5, 39], [6, 39], [7, 39], [6, 40], [5, 40], [4, 40], [3, 40], [2, 40], [1, 40], [0, 40], [0, 41], [1, 41], [2, 41], [3, 41], [4, 41], [5, 41], [43, 7], [43, 6], [42, 6], [42, 7], [34, 4], [33, 4], [32, 4], [31, 4], [30, 4], [29, 4], [28, 4], [27, 4], [26, 4], [25, 4], [24, 4], [23, 4], [23, 5], [24, 5], [25, 5], [26, 5], [27, 5], [28, 5], [29, 5], [30, 5], [31, 5], [32, 5], [33, 5], [33, 6], [32, 6], [31, 6], [30, 6], [29, 6], [28, 6], [27, 6], [26, 6], [25, 6], [24, 6], [25, 7], [26, 7], [27, 7], [28, 7], [29, 7], [30, 7], [31, 7], [32, 7], [31, 8], [30, 8], [29, 8], [28, 8], [27, 8], [26, 8], [25, 8], [26, 9], [27, 9], [28, 9], [29, 9], [30, 9], [31, 9], [30, 10], [29, 10], [26, 10], [26, 11], [27, 11], [28, 11], [29, 11], [30, 11], [30, 12], [29, 12], [28, 12], [27, 12], [26, 12], [25, 13], [26, 13], [27, 13], [28, 13], [29, 13], [30, 13], [30, 14], [29, 14], [28, 14], [26, 14], [25, 14], [25, 15], [26, 15], [28, 15], [29, 15], [30, 15], [30, 16], [29, 16], [28, 16], [27, 16], [26, 16], [25, 16], [25, 17], [26, 17], [27, 17], [28, 17], [29, 17], [30, 17], [31, 18], [30, 18], [29, 18], [28, 18], [28, 19], [29, 19], [30, 19], [31, 19], [32, 20], [31, 20], [30, 20], [29, 20], [29, 21], [30, 21], [31, 21], [32, 21], [32, 22], [31, 22], [30, 22], [29, 22], [28, 23], [29, 23], [30, 23], [31, 23], [32, 23], [32, 24], [31, 24], [30, 24], [29, 24], [28, 24], [27, 24], [25, 25], [26, 25], [27, 25], [28, 25], [29, 25], [30, 25], [31, 25], [32, 25], [31, 26], [30, 26], [29, 26], [28, 26], [27, 26], [26, 26], [25, 26], [24, 26], [23, 27], [25, 27], [26, 27], [27, 27], [28, 27], [30, 27], [31, 27], [30, 28], [29, 28], [28, 28], [27, 28], [26, 28], [23, 28], [22, 28], [20, 29], [21, 29], [22, 29], [23, 29], [24, 29], [25, 29], [26, 29], [27, 29], [28, 29], [26, 30], [25, 30], [24, 30], [23, 30], [22, 30], [21, 30], [20, 30], [19, 30], [19, 31], [20, 31], [21, 31], [22, 31], [23, 31], [24, 31], [25, 31], [23, 33], [22, 33], [21, 33], [20, 33], [19, 33], [18, 33], [17, 33], [17, 34], [18, 34], [19, 34], [20, 34], [21, 34], [22, 34], [23, 34], [22, 35], [21, 35], [20, 35], [19, 35], [18, 35], [17, 35], [16, 35], [16, 36], [17, 36], [18, 36], [19, 36], [20, 36], [19, 37], [18, 37], [17, 37], [16, 37], [15, 37], [14, 37], [13, 37], [12, 37], [11, 37], [11, 38], [12, 38], [13, 38], [14, 38], [15, 38], [16, 38], [17, 38], [18, 38], [17, 39], [16, 39], [15, 39], [14, 39], [13, 39], [12, 39], [11, 39], [10, 39], [9, 39], [8, 39], [7, 40], [8, 40], [9, 40], [10, 40], [11, 40], [12, 40], [13, 40], [14, 40], [15, 40], [16, 40], [16, 41], [15, 41], [14, 41], [13, 41], [12, 41], [11, 41], [10, 41], [9, 41], [8, 41], [7, 41], [6, 41]]
,
            "Liste_cache": [[2, 4], [2, 3], [2, 2], [2, 1], [3, 1], [3, 2], [3, 3], [3, 4], [20, 10], [20, 9], [17, 4], [17, 3], [17, 2], [17, 1], [27, 20], [26, 21], [27, 21], [24, 35], [24, 36], [23, 36], [23, 35], [35, 21], [35, 20], [36, 20], [36, 21], [49, 18], [49, 17], [49, 16], [50, 16], [51, 16], [51, 17], [51, 18], [50, 18], [50, 17], [59, 17], [60, 17], [60, 18], [59, 18], [59, 18], [50, 32], [50, 31]]

        },
        "Map2": {
            "track": "track2.png",
            "fond": "fond2.png",
            "Liste_obstacles": [(0, 0), (3, 3)],
            "Liste_vide": [(9, 9)],
        },
        "Map3": {
            "track": "track3.png",
            "fond": "fond3.png",
            "Liste_obstacles": [(5, 5), (10, 10)],
            "Liste_vide": [],
        }
    }

    def __init__(self, titre,WIDTH, HEIGHT,screen):
        """
        Initialise les attributs de la carte en fonction des configurations prédéfinies.

        Args:
            titre (str): Le titre de la carte.
        """
        # Vérifier si le titre existe dans les configurations
        if titre not in Map.configurations:
            raise ValueError(f"Le titre '{titre}' n'existe pas dans les configurations.")
        # Charger les arguments depuis les configurations
        config = Map.configurations[titre]
        self.titre = titre
        self.track = config["track"]
        self.fond = config["fond"]
        self.Liste_obstacles = config["Liste_obstacles"]
        self.Liste_vide = config["Liste_vide"]
        self.Liste_cache=config["Liste_cache"]
        pygame.mixer.music.load(self.track)
        #pygame.mixer.music.play()
        image = pygame.image.load(self.fond)  # Remplacez "image.png" par le nom de votre fichier
        image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        screen.blit(image, (0, 0))


