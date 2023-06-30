from display.base_module import DisplayModule, DisplaySize

SIZE = (20, 4)

class Raspi_2004_lcd(DisplayModule):
    """
    A controller to control a 20x4 lcd using a raspberry pi
    """
    def __init__(self):
        super(Raspi_2004_lcd, self).__init__(DisplaySize(*SIZE))
        import display.modules.lcddriver as lcddriver
        self.lcd = lcddriver.LCDisplay()

    def display_line(self, line: int, content: str):
        """
        Display a line to the lcd display
        :param line: line number to display to
        :param content: content to display
        :return:
        """
        self.lcd.lcd_display_string(content, line)

