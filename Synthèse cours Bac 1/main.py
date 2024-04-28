import pygame
import time
import math
import os
import pygame.draw

pygame.init()

pygame.mixer.init()

# pygame.mixer.pre_init(frequency =44100,size=16,channels=1,buffer=512)
# Constantes qui sont les tailles de l'écran
LARGEUR, HAUTEUR = 800, 400
VITESSE_DEPLACEMENT = 5
VITESSE_DE_SAUT = 0.5
HAUTEUR_SAUT = 100
VITESSE_D_ANIMATION = 0.25
t_saut = -math.sqrt(HAUTEUR_SAUT)
collision_id = 0

# Configure la surface de dessin
surface = pygame.display.set_mode((LARGEUR, HAUTEUR))

# gestions sons
son_saut = pygame.mixer.Sound(os.path.join("assets", "saut.wav"))
son_piece = pygame.mixer.Sound(os.path.join("assets", "piece.wav"))

acteur_id_right = 0
acteur_id_left = 0
# création du rect personnage et attribution de l'image
acteur_left = [pygame.image.load(os.path.join("assets", f"acteur_L{i}.png")).convert_alpha() for i in range(1, 5)]
acteur_right = [pygame.image.load(os.path.join("assets", f"acteur_R{i}.png")).convert_alpha() for i in range(1, 5)]

acteur = acteur_right[0]

acteur_rect = acteur.get_rect()
acteur_rect = acteur_rect.inflate(-25, -5)
acteur_rect.midbottom = (LARGEUR // 2, HAUTEUR)

# création du rect pièce
pieces = [pygame.image.load(os.path.join("assets", f"piece_{i}.png")).convert_alpha() for i in range(1, 8)]
piece_id = 0
# pieces_rect
pieces_rect = []
for i in range(5):
    pieces_rect.append(pieces[0].get_rect(center=(20 + 180 * i, HAUTEUR - 150)))

# configurer FPS
FPS = 60
# couleur de fond
couleur = (255, 255, 255)
# variable pour le saut
en_saut = False
# variable pour la boucle principale
running = True
# horloge pour le FPS
clock = pygame.time.Clock()


# méthode pour le saut
def sauter(t, forme, vitesse, hauteur):
    y_initiale = HAUTEUR - forme.h
    t += vitesse
    fin_saut = False
    forme.y = y_initiale - (hauteur - t ** 2)
    if forme.y >= y_initiale:
        forme.y = y_initiale
        fin_saut = True
    return t, fin_saut


# méthode pour dessiner
def dessin(couleur):
    surface.fill(couleur)
    # on dessine le personnage avec l'allignement du rect sur l'image
    surface.blit(acteur, acteur.get_rect(center=acteur_rect.center))

    # on dessine les pièces
    for p in pieces_rect:
        surface.blit(pieces[int(piece_id)], p)


    pygame.display.update()


# Boucle principale / Game loop
while running:
    # on récupère les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                acteur = acteur_right[0]
                acteur_id_right = 1
            if event.key == pygame.K_q:
                acteur = acteur_left[0]
                acteur_id_left = 1
    # on récupère les touches
    touches = pygame.key.get_pressed()
    if touches[pygame.K_q]:
        acteur_rect.x -= VITESSE_DEPLACEMENT
        acteur_id_left += VITESSE_D_ANIMATION
        if acteur_id_left >= len(acteur_left):
            acteur_id_left = 1
        acteur = acteur_left[int(acteur_id_left)]
    if touches[pygame.K_d]:
        acteur_rect.x += VITESSE_DEPLACEMENT
        acteur_id_right += VITESSE_D_ANIMATION
        if acteur_id_right >= len(acteur_right):
            acteur_id_right = 1
        acteur = acteur_right[int(acteur_id_right)]
    if touches[pygame.K_SPACE]:
        if en_saut == False:
            son_saut.play()
        en_saut = True
    # gestion du saut
    if en_saut:
        # on récupère la nouvelle valeur de t_saut et si le saut est fini
        t_saut, fin_saut = sauter(t_saut, acteur_rect, VITESSE_DE_SAUT, HAUTEUR_SAUT)
        if fin_saut:
            en_saut = False
            t_saut = -math.sqrt(HAUTEUR_SAUT)
    for i, p in enumerate(pieces_rect):
        if acteur_rect.colliderect(pieces_rect[i]):
            if collision_id != i:
                son_piece.play()
            collision_id = i

    piece_id += 0.1
    if piece_id >= len(pieces):
        piece_id = 0

    # on dessine
    dessin(couleur)

    # on attend pour avoir un FPS constant
    clock.tick(FPS)

pygame.quit()