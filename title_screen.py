import pygame

def show_title_screen(screen):
    font = pygame.font.Font(None, 74)
    button_font = pygame.font.Font(None, 36)
    input_font = pygame.font.Font(None, 32)
    running = True
    started = False

    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)

    # Title text
    title_text = font.render("Piano Physics Simulation", True, WHITE)
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))

    # Button text
    start_button = button_font.render("Start", True, WHITE)
    start_button_rect = start_button.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 180))

    # Input field for ball elasticity
    elasticity_label = input_font.render("Ball Elasticity (0.0 to 1.0):", True, WHITE)
    elasticity_rect = elasticity_label.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 30))
    elasticity_input = ""
    
    # Input field for ball friction
    friction_label = input_font.render("Ball Friction (0.0 to 1.0):", True, WHITE)
    friction_rect = friction_label.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 70))
    friction_input = ""

    # Variable to track the active input box
    active_input = None

    # Function to draw input fields
    def draw_input_box(input_text, rect):
        pygame.draw.rect(screen, WHITE, rect, 2)
        text_surface = input_font.render(input_text, True, WHITE)
        screen.blit(text_surface, (rect.x + 5, rect.y + 5))

    # Cursor properties
    cursor_color = WHITE
    cursor_width = 2
    cursor_blink_rate = 500
    last_blink_time = 0
    cursor_visible = True

    # Main loop for the title screen
    while running:
        screen.fill(BLACK)
        
        # Draw title and start button
        screen.blit(title_text, title_rect)
        pygame.draw.rect(screen, BLUE, start_button_rect.inflate(20, 20))
        screen.blit(start_button, start_button_rect)

        # Draw input labels and fields
        screen.blit(elasticity_label, elasticity_rect)
        screen.blit(friction_label, friction_rect)
        draw_input_box(elasticity_input, pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 - 10, 200, 40))
        draw_input_box(friction_input, pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 + 90, 200, 40))

        # Draw cursor if input fields are active and cursor is visible
        if active_input == "elasticity" and elasticity_input != "" and cursor_visible:
            cursor_x = screen.get_width() // 2 - 100 + input_font.size(elasticity_input)[0] + 5
            cursor_rect = pygame.Rect(cursor_x, screen.get_height() // 2 - 10 + 5, cursor_width, 30)
            pygame.draw.rect(screen, cursor_color, cursor_rect)

        if active_input == "friction" and friction_input != "" and cursor_visible:
            cursor_x = screen.get_width() // 2 - 100 + input_font.size(friction_input)[0] + 5
            cursor_rect = pygame.Rect(cursor_x, screen.get_height() // 2 + 90 + 5, cursor_width, 30)
            pygame.draw.rect(screen, cursor_color, cursor_rect)

        pygame.display.flip()

        # Cursor blinking logic
        current_time = pygame.time.get_ticks()
        if current_time - last_blink_time > cursor_blink_rate:
            cursor_visible = not cursor_visible  # Toggle cursor visibility
            last_blink_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    started = True
                    running = False  # exit the title screen
                # Check if the mouse click is inside one of the input boxes
                if pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 - 10, 200, 40).collidepoint(event.pos):
                    active_input = "elasticity"
                elif pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 + 90, 200, 40).collidepoint(event.pos):
                    active_input = "friction"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if active_input == "elasticity" and elasticity_input:
                        elasticity_input = elasticity_input[:-1]
                    elif active_input == "friction" and friction_input:
                        friction_input = friction_input[:-1]
                else:
                    # Add typed character to the active input field
                    if active_input == "elasticity" and (elasticity_input == "" or len(elasticity_input) < 4):
                        if event.unicode.isnumeric() or event.unicode == '.':
                            elasticity_input += event.unicode
                    if active_input == "friction" and (friction_input == "" or len(friction_input) < 4):
                        if event.unicode.isnumeric() or event.unicode == '.':
                            friction_input += event.unicode

        pygame.time.Clock().tick(60)

    # Convert the inputs to float and return them
    try:
        elasticity = float(elasticity_input) if 0.0 <= float(elasticity_input) <= 1.0 else 0.99
        friction = float(friction_input) if 0.0 <= float(friction_input) <= 1.0 else 0.0
    except ValueError:
        elasticity = 0.99
        friction = 0.0

    return started, elasticity, friction
