from bs4 import BeautifulSoup
import dukpy


class ProfileRenderer:
    def __init__(self, util):
        self.util = util
        self.element_positions = {}  # Store element positions
        self.js_code = """
            function manipulateDOM() {
                // Define the JavaScript DOM manipulation logic here.
                // For example, changing the display property of an element
                return {elementId: 'newDisplayValue'};
            }
            manipulateDOM();
            """

    def render_profile(self):
        with open("html/profile.html", "r") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")
        elements = soup.find_all(["div", "input", "button"])  # Add more tags as needed

        for element in elements:

            
            # Extract event handlers
            #onclick = element.get('onclick')
            #onkeydown = element.get('onkeydown')

            # Process events if they exist
            #if onclick:
            #    self.handle_event_with_dukpy(onclick)
            #if onkeydown:
            #    self.handle_event_with_dukpy(onkeydown)

            style = element.get('style', '')
            top, left = self.extract_position(style)
            color = self.extract_color(style)

            width = self.extract_width(style)
            height = self.extract_style_value(style, 'height', 1)  # Assuming a default height
            end_x = left + width
            end_y = top + height
            self.element_positions[element] = [(left, top), (end_x, end_y)]

            if element.name == 'div':
                self.util.emit_current_string(element.text, color, 4, False, left, top)
            elif element.name in ['input', 'button']:
                width = self.extract_width(style, default_width=35 if element.name == 'input' else 75)
                width_spaces = ' ' * width
                self.util.emit_current_string(width_spaces, color, 4, False, left, top)

    def is_inside_box(self, x, y, element):
        start, end = self.element_positions.get(element, [(0, 0), (0, 0)])
        return start[0] <= x <= end[0] and start[1] <= y <= end[1]

    def extract_position(self, style):
        top = self.extract_style_value(style, 'top', 0)
        left = self.extract_style_value(style, 'left', 0)
        return top, left

    def extract_color(self, style):
        return self.extract_style_value(style, 'color', 0)

    def extract_width(self, style, default_width=35):
        return self.extract_style_value(style, 'width', default_width)

    def extract_style_value(self, style, attribute, default_value):
        if attribute + ':' in style:
            return int(style.split(attribute + ':')[1].split('px')[0].strip())
        return default_value

    def handle_event_with_dukpy(self, js_code, additional_js):
        js_result = dukpy.evaljs(js_code + ' ' + additional_js)
        for element_id, new_display in js_result.items():
            element = soup.find(id=element_id)
            if element:
                element['style'] = f'display: {new_display};'  # Example: Updating the display style