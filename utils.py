import pygame
from pygame.locals import *
pygame.init()
font = pygame.font.SysFont(None, 28)

class Button:
    def __init__(self, x, y, w, h, text, font, color, hover_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.rect.collidepoint(mouse_pos) and mouse_pressed[0]
    
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255, 255, 255)
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active if clicked
            self.active = self.rect.collidepoint(event.pos)
            self.color = (0, 255, 0) if self.active else (255, 255, 255)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text  # return text on Enter
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font.render(self.text, True, self.color)
        return None

    def draw(self, screen):
        # Draw text and box
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)
    def get_text(self):
        return self.text

class Text:
    def __init__(self, text, x, y, font, color=(255, 255, 255), center=False):
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.color = color
        self.center = center
        self.update_surface()

    def update_surface(self):
        """Rerender the text surface after changes."""
        self.surface = self.font.render(str(self.text), True, self.color)
        self.rect = self.surface.get_rect()
        if self.center:
            self.rect.center = (self.x, self.y)
        else:
            self.rect.topleft = (self.x, self.y)

    def set_text(self, new_text):
        """Change the displayed text."""
        self.text = new_text
        self.update_surface()

    def set_color(self, new_color):
        """Change text color."""
        self.color = new_color
        self.update_surface()

    def draw(self, screen):
        """Draw text to the screen."""
        screen.blit(self.surface, self.rect)


"""
================================================================================
Pygame UI Elements: Button, InputBox, Text
================================================================================

This file contains three reusable classes that make it easier to create UI 
components (buttons, text input fields, and static/dynamic text) in a Pygame 
project.

You can use them to quickly add menus, forms, labels, or simple interactive 
interfaces to your Pygame application.

--------------------------------------------------------------------------------
1. Button
--------------------------------------------------------------------------------
Purpose:
    - Creates a clickable button with hover effects.
    - Displays text centered inside the button.

Constructor:
    Button(x, y, w, h, text, font, color, hover_color)
    
Parameters:
    x, y        -> Top-left position of the button
    w, h        -> Width and height of the button
    text        -> Text to display on the button
    font        -> Pygame font object (e.g., pygame.font.SysFont(None, 28))
    color       -> Button background color (tuple, e.g., (100, 100, 100))
    hover_color -> Button background color when mouse is hovering
    
Methods:
    draw(screen, mouse_pos)
        -> Draws the button to the screen. Changes color on hover.
    
    is_clicked(mouse_pos, mouse_pressed)
        -> Returns True if the button is clicked with the left mouse button.

Example:
    my_button = Button(100, 200, 150, 50, "Click Me", font, (0,0,255), (0,100,255))
    my_button.draw(screen, pygame.mouse.get_pos())
    if my_button.is_clicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
        print("Button was clicked!")

--------------------------------------------------------------------------------
2. InputBox
--------------------------------------------------------------------------------
Purpose:
    - Provides a simple text input field.
    - User can click inside to activate typing.
    - Supports typing letters, deleting with backspace, and submitting with Enter.

Constructor:
    InputBox(x, y, w, h, text="")
    
Parameters:
    x, y   -> Top-left position of the input box
    w, h   -> Width and height
    text   -> Initial text (optional)
    
Methods:
    handle_event(event)
        -> Call this inside your event loop.
        -> Updates input text when keys are pressed.
        -> Returns text string if Enter is pressed, otherwise None.
    
    draw(screen)
        -> Draws the input box and its current text.
    
    get_text()
        -> Returns the current string stored inside the input box.

Example:
    input_box = InputBox(100, 300, 200, 40)
    
    for event in pygame.event.get():
        result = input_box.handle_event(event)
        if result is not None:   # Enter pressed
            print("User typed:", result)
    
    input_box.draw(screen)

--------------------------------------------------------------------------------
3. Text
--------------------------------------------------------------------------------
Purpose:
    - Simple static or dynamic text display.
    - Can be used as a label, title, or score counter.
    - Supports changing text and color dynamically.

Constructor:
    Text(text, x, y, font, color=(255,255,255), center=False)
    
Parameters:
    text   -> The text string to display
    x, y   -> Position
    font   -> Pygame font object
    color  -> Text color (default: white)
    center -> If True, (x,y) will be the text center instead of top-left
    
Methods:
    set_text(new_text)
        -> Change the displayed text.
    
    set_color(new_color)
        -> Change text color.
    
    draw(screen)
        -> Draw the text to the screen.

Example:
    score_text = Text("Score: 0", 10, 10, font)
    score_text.draw(screen)
    score_text.set_text("Score: " + str(new_score))

--------------------------------------------------------------------------------
4. Example Usage
--------------------------------------------------------------------------------
Typical main loop usage:

    import pygame
    from pygame.locals import *
    pygame.init()
    font = pygame.font.SysFont(None, 28)

    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    button = Button(100, 100, 150, 50, "Play", font, (0,0,200), (0,0,255))
    input_box = InputBox(100, 200, 200, 40)
    label = Text("Enter Name:", 100, 170, font)

    running = True
    while running:
        screen.fill((30, 30, 30))
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            result = input_box.handle_event(event)
            if result is not None:
                print("User entered:", result)

        # Draw UI
        button.draw(screen, mouse_pos)
        input_box.draw(screen)
        label.draw(screen)

        if button.is_clicked(mouse_pos, mouse_pressed):
            print("Button clicked!")

        pygame.display.flip()
        clock.tick(60)

--------------------------------------------------------------------------------
Notes:
--------------------------------------------------------------------------------
- Always call `draw()` methods AFTER filling the screen (so they appear on top).
- Call `handle_event()` for input boxes inside your event loop.
- Use `is_clicked()` for buttons outside the event loop (in your main loop).
- Customize fonts and colors for styling.
================================================================================
"""

