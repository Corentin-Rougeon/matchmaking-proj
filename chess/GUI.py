import pygame
import pygame_gui
import board
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton

pygame.init()

resolution = (800,800)

pygame.display.set_caption('chess')
window_surface = pygame.display.set_mode(resolution)
manager = pygame_gui.UIManager(resolution,pygame_gui.PackageResource('assets','theme.json'))
manager.set_visual_debug_mode(True)
clock = pygame.time.Clock()

background = pygame.Surface(resolution)
#background.fill(manager.get_theme().get_colour('dark_bg'))

load_time_1 = clock.tick()

button_row_width = resolution[0]/8
button_row_height = resolution[0]/8
spacing = 0

ChessBoardSquares = [ [0]*9 for i in range(9)]

print(ChessBoardSquares)



unicode_pieces = {
    "R": "♖", "r": "♜",
    "N": "♘", "n": "♞",
    "B": "♗", "b": "♝",
    "Q": "♕", "q": "♛",
    "K": "♔", "k": "♚",
    "P": "♙", "p": "♟",' ': ' '
}







isWhite = True
Squareid = 0
for j in range(0,8):
    isWhite = isWhite == False
    for i in range(0,8):
        position = (i * spacing + ((i - 0) * button_row_width),
                    (j * spacing + ((j - 0) * button_row_height)))
        isWhite = isWhite == False
        if isWhite:
            Class = "whiteSquare"
        else:
            Class = "blackSquare"



        Class += ",whitePiece"


        '''text_box = pygame_gui.elements.UITextBox(
            html_text="My "
                      "<shadow size=1 color=#553520>"
                      "<font face=PermanentMarker color=#A06545>"
                      "<effect id=test>EARTHQUAKE</effect> "
                      "</font>"
                      "</shadow>"
                      "will <font face=PermanentMarker>"
                      "<effect id=shatter>SHATTER</effect>"
                      "</font>"
                      " your bones. Puny Mortals.",
            relative_rect=pygame.Rect(100, 100, 200, 90),
            manager=manager)
        '''


        button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position,
                                                               (button_row_width,
                                                                button_row_height)),
                                     text= f"{Squareid}",
                                     manager=manager,
                                     object_id=ObjectID(object_id=f"{Squareid}",
                                                        class_id="@"+Class))

        button.hide()
        pygame.draw.rect(window_surface, (255, 255, 255),
                         [position[0], position[1], button_row_width, button_row_height])

        pygame.display.flip()
        Squareid += 1



load_time_2 = clock.tick()
print('Button creation time taken:', load_time_2/1000.0, 'seconds.')

is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0


    for j in range(0, 8):
        for i in range(0, 8):
            position = (i * spacing + ((i - 0) * button_row_width),
                        (j * spacing + ((j - 0) * button_row_height)))

            #pygame.draw.rect(window_surface, (255, 255, 255),
            #                 [position[0], position[1], button_row_width, button_row_height])


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            print(event.ui_object_id)

            #print(event.ui_object_id)


        manager.process_events(event)

    manager.update(time_delta)

    #window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    pygame.display.update()
