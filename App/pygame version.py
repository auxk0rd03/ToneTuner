import pygame
import time

# Initialize Pygame
pygame.init()

# List of songs (Replaced with song titles)
songs = [
    "Song 1 - Artist A",
    "Song 2 - Artist B",
    "Song 3 - Artist C",
    "Song 4 - Artist D",
    "Song 5 - Artist E"
]

# List of colors for each song (match the length with the number of songs)
colors = [
    (255, 99, 71),     # Red for Song 1
    (70, 130, 180),    # Blue for Song 2
    (144, 238, 144),   # Green for Song 3
    (255, 215, 0),     # Gold for Song 4
    (255, 69, 0)       # Orange for Song 5
]

song_durations = [10, 10, 10, 10, 10]  # Song duration in seconds
current_index = 0

# Screen settings
win_width = 700
win_height = 500
screen = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Playlist")


def get_font_size():
    return int(win_width // 20)
# Function to draw the current song label
def draw_song_label():
    screen.fill(colors[current_index])  # Set background color based on the current song
    font = pygame.font.Font(None, get_font_size())
    song_text = font.render(f"Now Playing: {songs[current_index]}", True, (0, 0, 0))
    screen.blit(song_text, (win_width / 2 - song_text.get_width() / 2, win_height / 4))

# Function to draw buttons
def draw_buttons():
    
    button_width = win_width // 5
    button_height = win_height // 10
    
    back_button = pygame.Rect(win_width * 0.25 - button_width / 2, win_height * 0.75 - button_height / 2, button_width, button_height)
    forward_button = pygame.Rect(win_width * 0.75 - button_width / 2, win_height * 0.75 - button_height / 2, button_width, button_height)
    resize_up_button = pygame.Rect(win_width - button_width - 20, 20, button_width // 2, button_height // 2)
    resize_down_button = pygame.Rect(win_width - button_width - 20, 80, button_width // 2, button_height // 2)

    pygame.draw.rect(screen, (200, 200, 200), back_button)
    pygame.draw.rect(screen, (200, 200, 200), forward_button)
    pygame.draw.rect(screen, (200, 200, 200), resize_up_button)
    pygame.draw.rect(screen, (200, 200, 200), resize_down_button)
    
    font = pygame.font.Font(None, get_font_size())

    back_button_text = font.render("Backward", True, (0, 0, 0))
    forward_button_text = font.render("Forward", True, (0, 0, 0))
    resize_up_button_text = font.render("^", True, (0, 0, 0))
    resize_down_button_text = font.render("↓", True, (0, 0, 0))

    screen.blit(back_button_text, (back_button.centerx - back_button_text.get_width() / 2, back_button.centery - back_button_text.get_height() / 2))
    screen.blit(forward_button_text, (forward_button.centerx - forward_button_text.get_width() / 2, forward_button.centery - forward_button_text.get_height() / 2))
    screen.blit(resize_up_button_text, (resize_up_button.centerx - resize_up_button_text.get_width() / 2, resize_up_button.centery - resize_up_button_text.get_height() / 2))
    screen.blit(resize_down_button_text, (resize_down_button.centerx - resize_down_button_text.get_width() / 2, resize_down_button.centery - resize_down_button_text.get_height() / 2))

    return back_button, forward_button, resize_up_button, resize_down_button

# Function to handle button clicks
def handle_click(mouse_pos, back_button, forward_button, resize_up_button, resize_down_button):
    global current_index, win_width, win_height
    if back_button.collidepoint(mouse_pos):
        if current_index > 0:
            current_index -= 1
        return True
    elif forward_button.collidepoint(mouse_pos):
        if current_index < len(songs) - 1:
            current_index += 1
        return True
    elif resize_up_button.collidepoint(mouse_pos):
        win_width *= 1.2
        win_height *= 1.2
        screen = pygame.display.set_mode((win_width, win_height))
        return True
    elif resize_down_button.collidepoint(mouse_pos):
        win_width *= 0.8
        win_height *= 0.8
        screen = pygame.display.set_mode((win_width, win_height))
        return True
    return False

# Track the time 
start_time = time.time()

# Main game loop
running = True
while running:
    elapsed_time = time.time() - start_time

    # Automatically move to the next song if the duration has passed
    if elapsed_time >= song_durations[current_index]:
        current_index = (current_index + 1) % len(songs)
        start_time = time.time()

    # Draw the song label and buttons
    draw_song_label()
    back_button, forward_button, resize_up_button, resize_down_button = draw_buttons()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if handle_click(event.pos, back_button, forward_button, resize_up_button, resize_down_button):
                draw_song_label()
                draw_buttons()

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
