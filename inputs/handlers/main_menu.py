import ui.screens as Screens

def handle_select_mode(pinId, menu_items, current_selection):
    new_selection = current_selection
    new_screen = Screens.Screen.SELECT_MODE
    
    if pinId == 19:  # Left button
        new_selection = (current_selection - 1) % len(menu_items)
    elif pinId == 5:  # Right button
        new_selection = (current_selection + 1) % len(menu_items)
    elif pinId == 18:  # Middle button
        new_screen = menu_items[current_selection]
        
    return new_screen, new_selection