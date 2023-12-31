from bs4 import BeautifulSoup
import dukpy


class ProfileRenderer:
    def __init__(self, util, return_function):
        self.util = util
        self.element_positions = {}  # Store element positions
        self.onclick_events = {}
        self.soup = None
        self.return_function = return_function
        self.input_values = {}  # Dictionary to store input values for each element
        self.active_callback = None
        self.previous_element_id = None
        self.js_code = """
            function $(elementId) {
                // Simulate jQuery-like behavior
                return {
                    focus: function() {
                        // This function prepares the data to be sent back to Python
                        return { focusElementId: elementId };
                    }
                };
            }
            """

    def render_profile(self):
        with open("html/profile.html", "r") as file:
            html_content = file.read()

        self.util.clear_screen()
        self.soup = BeautifulSoup(html_content, "html.parser")
        elements = self.soup.find_all(["div", "input", "button", "submit"])  # Add more tags as needed

        for element in elements:

            onclick = element.get('onclick')
            if onclick:
                element_id = element.get('id', None)
                if element_id:
                    self.onclick_events[element_id] = onclick
            
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
            height = self.extract_style_value(style, 'height', 1)
            end_x = left + width
            end_y = top + height

            # Store positions using the element's ID
            element_id = element.get('id')
            if element_id:
                self.element_positions[element_id] = [(left, top), (end_x, end_y)]


            if element.name == 'div':
                self.util.sid_data.startX = left
                self.util.sid_data.startY = top
                self.util.output(element.text, 6, 0)
            elif element.name == 'button' or element.name=='submit':
                self.util.sid_data.startX = left
                self.util.sid_data.startY = top
                width = self.extract_width(style, default_width=35 if element.name == 'input' else 35)
                centered_text = self.center_text(element.text, width)
                self.util.output(centered_text, 14, 6)

            elif element.name == 'input':
                width = self.extract_width(style, default_width=35 if element.name == 'input' else 35)
                width_spaces = ' ' * width
                self.util.sid_data.startX = left
                self.util.sid_data.startY = top
                self.util.output(width_spaces, 6, 4)

        self.util.sid_data.setCurrentAction("wait_for_profile_renderer")

    def extract_element_for_id(self, element_id):
        # Assuming self.soup is already a BeautifulSoup object of your HTML content
        element = self.soup.find(id=element_id)
        if element:
            # Process the element as needed, e.g., extract text or attributes
            return element
        else:
            return None

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

    def handle_event_with_dukpy(self, js_code):
        # Here, you need to modify the JavaScript logic to identify which element needs focus
        print(self.js_code + ' ' + js_code)
        js_result = dukpy.evaljs(self.js_code + ' ' + js_code)
        # Assuming js_result contains the element ID that needs focus
        element_id_to_focus = js_result.get('focusElementId')[1:]
        if element_id_to_focus:
            self.focus_on_element(element_id_to_focus)

    def handle_click(self, x, y):
        for element_id, (start, end) in self.element_positions.items():
            
            if start[0] <= x <= end[0] and start[1] <= y <= end[1]:
                if element_id in self.onclick_events:
                    self.handle_event_with_dukpy(self.onclick_events[element_id])

                my_element = self.extract_element_for_id(element_id)
                if my_element and my_element.name == 'button' and my_element.get('type') == 'submit':
                    self.submit_function()

    def focus_on_element(self, element_id):
        matched_element_position = self.element_positions.get(element_id)
        if matched_element_position:
            start, _ = matched_element_position
            width = self.extract_width_for_id(element_id)
            self.util.sid_data.startX = start[0]
            self.util.sid_data.startY = start[1]
            self.util.sid_data.setInputType("text")
            print("element_id:" + element_id)

            # If there was a previously focused element, save its current input value
            if self.previous_element_id is not None:
                self.input_values[self.previous_element_id] = self.util.sid_data.localinput

            # Set the default value for the new element
            default_value = self.input_values.get(element_id, "")

            # Nested function for callback
            def callback_with_element_id(input_data):
                # Update the value for the element that was active when the input was provided
                self.input_values[element_id] = input_data

            # Update the active callback
            self.active_callback = callback_with_element_id

            # Update the previous element ID
            self.previous_element_id = element_id

            # Ask for input with the default value for the current element
            self.util.askinput(width, self.active_callback, [], default_value)

    def callback_function(self, input_data, element_id):
        # Store the input value for this element ID
        self.input_values[element_id] = input_data

    def submit_function(self):
        self.return_function()
        pass
    
    def extract_width_for_id(self, element_id):
        # Retrieve the position data for the specified element
        position_data = self.element_positions.get(element_id)

        if position_data:
            # Position data is in the format [(left, top), (end_x, end_y)]
            start, end = position_data
            # Calculate width as the difference between end_x and left
            width = end[0] - start[0]
            return width
        else:
            # Return a default width if the element or its position data is not found
            return 35  # Or any other appropriate default value
        
        
    def center_text(self, text, width):
        # Truncate the text if it's longer than the width
        if len(text) > width:
            return text[:width]
        
        # Calculate the padding needed on each side
        padding = (width - len(text)) // 2
        return ' ' * padding + text + ' ' * (width - len(text) - padding)