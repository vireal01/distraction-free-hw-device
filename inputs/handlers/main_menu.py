import ui.screens as Screens
import config

def handle_select_mode(pinId, menu_items, current_selection):
    new_selection = current_selection
    new_screen = Screens.Screen.SELECT_MODE
    
    if pinId == config.left_button:  # Left button
        new_selection = (current_selection - 1) % len(menu_items)
    elif pinId == config.right_button:  # Right button
        new_selection = (current_selection + 1) % len(menu_items)
    elif pinId == config.middle_button:  # Middle button
        new_screen = menu_items[current_selection]
        
    return new_screen, new_selection