
class RadioGroup:
    def __init__(self, buttons):
        self.buttons = buttons  # List of buttons

    def handle_click(self, mouse_pos):
        """Handle button click logic."""
        for button in self.buttons:
            if button.check_click(mouse_pos):  # If the button is clicked
                self.set_active(button)
                break

    def set_active(self, active_button):
        """Set the clicked button as active and deactivate others."""
        for button in self.buttons:
            button.set_active(button == active_button)

    def get_active(self):
        for btn in self.buttons:
            if btn.active: return btn

    def draw(self, screen):
        """Draw all buttons in the group."""
        for button in self.buttons:
            button.draw(screen)