from bs4 import BeautifulSoup
import bs4.element

import dukpy
import re
import bcrypt
import time
class Renderer:
    def __init__(self, util, return_function):
        # Initialize common rendering properties
        self.util = util
        self.first_input_element = None
        self.element_positions = {}  # Store element positions
        self.onclick_events = {}
        self.soup = None
        self.return_function = return_function
        self.active_callback = None
        self.previous_element_id = None
        self.processed_ids = set()
        self.sleeper = 0.1

        self.inheritable_properties = [
            'color',
            'top',
            'left',
            'background-color',
            'width'
        ]

        self.current_focus_index = 0
        self.input_values = {}  # Dictionary to store input values for each element
        self.js_code = """
            var lastAlertMessage = ''; // Global variable to store the last alert message

            function $(elementId) {
                // Simulate jQuery-like behavior
                return {
                    focus: function() {
                        // This function prepares the data to be sent back to Python
                        return { focusElementId: elementId };
                    },
                    val: function(newValue) {
                        if (newValue !== undefined) {
                            dukpy.input_values[elementId] = newValue;
                        }
                        if (elementId.substring(0,1)=='#') {
                            elementId=elementId.substring(1);
                        }
                        return dukpy.input_values[elementId] || '';
                    }
                };
            }

            function alert(message) {
                lastAlertMessage = message; // Update the global variable with the new message
                return { alertMessage: message };
            }
        """


    def render_page(self, filename):
        # Fetch user data from the database
        # Assuming 'self.util.sid_data.user_document['_id']' contains the current user's ID

        # Read the HTML template
        with open(filename, "r") as file:
            html_content = file.read()

        if self.util.sid_data.user_document != None:
            db = self.util.mongo_client['bbs']
            users_collection = db['users']
            user_data = users_collection.find_one({"_id": self.util.sid_data.user_document['_id']})
            # Replace placeholders with actual user data or remove them if not present
            all_placeholders = re.findall(r'\{userdata\.\w+\}', html_content)
            for placeholder in all_placeholders:
                field = placeholder.strip('{}').split('.')[1]
                if field in user_data and user_data[field] is not None:
                    html_content = html_content.replace(placeholder, str(user_data[field]))
                else:
                    html_content = html_content.replace(placeholder, '')

        self.soup = BeautifulSoup(html_content, "html.parser")
        unique_id = 0

        for element in self.soup.find_all():
            element['uniqueid'] = str(unique_id)
            unique_id += 1
        self.redraw_elements(True)

        

    def redraw_elements(self, useHTMLValues):
        grid_containers = self.soup.find_all(["div", "p", "input", "button", "submit", "a"], style=lambda s: 'grid-template-columns:' in s or 'grid-template-rows:' in s if s else False)

        for container in grid_containers:
            container_style = container.get('style', '')
            grid_columns = []
            grid_rows = []
            total_width = self.util.sid_data.xWidth
            total_height = self.util.sid_data.yHeight

            # Extract column and row styles
            if 'grid-template-columns:' in container_style:
                columns_style = container_style.split('grid-template-columns:')[1].split(';')[0].strip()
                grid_columns = columns_style.split()
                total_fr_columns = sum([float(c.split('fr')[0]) for c in grid_columns if 'fr' in c])
                fixed_width_columns = sum([int(c.strip('px')) for c in grid_columns if 'px' in c])
                fr_width = (total_width - fixed_width_columns) / total_fr_columns if total_fr_columns else 0
                column_widths = [fr_width * float(c.split('fr')[0]) if 'fr' in c else int(c.strip('px')) for c in grid_columns]

            if 'grid-template-rows:' in container_style:
                rows_style = container_style.split('grid-template-rows:')[1].split(';')[0].strip()
                grid_rows = rows_style.split()
                total_fr_rows = sum([float(r.split('fr')[0]) for r in grid_rows if 'fr' in r])
                fixed_height_rows = sum([int(r.strip('px')) for r in grid_rows if 'px' in r])
                fr_height = (total_height - fixed_height_rows) / total_fr_rows if total_fr_rows else 0
                row_heights = [fr_height * float(r.split('fr')[0]) if 'fr' in r else int(r.strip('px')) for r in grid_rows]

            elements = container.find_all(["div", "p", "input", "button", "submit", "a"])
            for index, element in enumerate(elements):
                existing_style = element.get('style', '')
                column = index % len(grid_columns) if grid_columns else 0
                row = index // len(grid_columns) if grid_columns else 0

                left = sum(column_widths[:column]) if grid_columns else 0
                top = sum(row_heights[:row]) if grid_rows else 0

                width = column_widths[column] if grid_columns else total_width
                height = row_heights[row] if grid_rows else total_height

                # Only update left, top, width, and height if they don't already exist
                if 'left:' not in existing_style:
                    existing_style += f" left: {left}px;"
                if 'top:' not in existing_style:
                    existing_style += f" top: {top}px;"
                if 'width:' not in existing_style:
                    existing_style += f" width: {width}px;"
                if 'height:' not in existing_style:
                    existing_style += f" height: {height}px;"

                element['style'] = existing_style


        elements = self.soup.find_all(["div", "p", "input", "button", "submit", "a"])  # Add more tags as needed
        self.element_order = [e.get('id') for e in elements if e.get('id')]

        for element in elements:
            if self.first_input_element == None and element.name == 'input':
                self.first_input_element = element
            onclick = element.get('onclick')
            if onclick:
                element_id = element.get('id', None)
                if element_id:
                    self.onclick_events[element_id] = onclick

            style = element.get('style', '')
            
            # Non-grid element positioning logic
            top, left = self.extract_position(style)
            self.util.sid_data.startX = left if left is not None else 0
            self.util.sid_data.startY = top if top is not None else 0

            width = self.extract_width(style)
            height = self.extract_style_value(style, 'height', 1)
            end_x = left + width
            end_y = top + height

            # Store positions using the element's ID
            element_id = element.get('id')
            if element_id:
                self.element_positions[element_id] = [(left, top), (end_x, end_y)]

            element_value = ""
            if useHTMLValues == True:
                element_value = element.get('value')
                if element_value:
                    self.input_values[element_id] = element_value
            elif element_id != None:
                element_value = self.input_values[element_id]

            if element.name == 'div':
                self.util.sid_data.startX = 0
                mytop, myleft = self.render_element(element, self.util.sid_data.startX, self.util.sid_data.startY, None, None)
                self.util.sid_data.startY = mytop
                self.util.sid_data.startX = myleft
            elif element.name == 'p':
                self.util.sid_data.startX = 0
                self.util.sid_data.startY += 1  # You might need to add logic to check if this increment is necessary
                mytop, myleft = self.render_element(element, self.util.sid_data.startX, self.util.sid_data.startY, None, None)
                self.util.sid_data.startY = mytop
                self.util.sid_data.startX = myleft
            elif element.name == 'button' or element.name=='submit':
                self.util.sid_data.startX = left
                self.util.sid_data.startY = top
                width = self.extract_width(style, default_width=35 if element.name == 'input' else 35)
                centered_text = self.center_text(element.text, width)
                self.util.output(centered_text, 14, 6)

            elif element.name == 'input':
                width = self.extract_width(style, default_width=35 if element.name == 'input' else 35)
                # Pad the element_value to match the width
                padded_element_value = element_value.ljust(width)
                
                self.util.sid_data.startX = left
                self.util.sid_data.startY = top
                self.util.output(padded_element_value, 6, 4)

        if self.first_input_element != None:
            ele_id = self.first_input_element.get('id', None)
            self.focus_on_element(ele_id, False)
            self.util.sid_data.setCurrentAction("wait_for_profile_renderer")

    def gather_inherited_styles(self, element):
        inherited_styles = {}
        parent = element.parent
        while parent is not None:
            parent_style = parent.get('style', '')
            for inheritable_attribute in self.inheritable_properties:  # inheritable_properties is a list of CSS properties that are inheritable
                value = self.extract_style_value(parent_style, inheritable_attribute, None)
                if value is not None:
                    inherited_styles[inheritable_attribute] = value
            parent = parent.parent
        return inherited_styles
    
    def render_element(self, element, left, top, default_width, default_height, new_block=True):
        if isinstance(element, bs4.element.Tag):
            unique_id = element.get('uniqueid')
            if unique_id in self.processed_ids:
                return top, left

            style = element.get('style', '')
            # Extracts values from own style, set them only if not None
            extracted_color = self.extract_style_value(style, 'color', None)
            color = extracted_color if extracted_color is not None else None
            extracted_backgroundColor = self.extract_style_value(style, 'background-color', None)
            backgroundColor = extracted_backgroundColor if extracted_backgroundColor is not None else None

            extracted_width = self.extract_style_value(style, 'width',None)
            width = extracted_width if extracted_width is not None else default_width

            extracted_height = self.extract_style_value(style,'height', None)
            height = extracted_height if extracted_height is not None else default_height

            inherited_styles = self.gather_inherited_styles(element)

            extracted_display = self.extract_style_value(style,'display', None)
            display = extracted_display if extracted_display is not None else None

            if color == None:
                color = inherited_styles.get('color', color)  # Inherits color if not defined in own style
            if color == None:
                color = 6

            if display == None:
                display = inherited_styles.get('display', color)  # Inherits color if not defined in own style
            if display == None:
                display = 'block'



            if backgroundColor == None:
                backgroundColor = inherited_styles.get('background-color', 0)  # Inherits background-color if not defined in own style
            if backgroundColor == None:
                backgroundColor = 0

            if 'width' not in style:
                width = inherited_styles.get('width', width)  # Inherits width if not defined in own style

            if 'height' not in style:
                height = inherited_styles.get('height', height)  # Inherits height

            # Recursively process child elements (depth-first)
            tag_name = element.name
            link = element.get('href')
            for child in element.children:
                if isinstance(child, bs4.element.Tag):
                    # If the child is a Tag, recursively call render_element
                    top, left = self.render_element(child, left, top, width, height, new_block=new_block)
                    # After a tag, it's no longer the start of a new block
                    new_block = False
                elif isinstance(child, bs4.NavigableString):
                    child_text = child.strip()
                    if child_text:
                        print("LEFT:"+str(left))
                        top, left = self.output_text(display, child_text, left, top, width, height, tag_name, color, backgroundColor, link=link, new_block=new_block)
                        time.sleep(self.sleeper)
                        # After text, it's no longer the start of a new block
                        new_block = False

            # Mark this Tag element as processed
            self.processed_ids.add(unique_id)

        # If the element is a string (NavigableString), process it directly
        elif isinstance(element, bs4.NavigableString):
            child_text = element.strip()
            if child_text:
                print("NavigableString:", child_text)  # For debugging
                # Output text with the color extracted from the parent Tag
                parent_tag_name = element.parent.name if element.parent else None
                top, left = self.output_text(display, child_text, left, top, width, height, parent_tag_name, color, backgroundColor, link=link)
                time.sleep(self.sleeper)
                
            
        return top, left














    def output_text(self, display, element, left, top, width, height, tag_name, foregroundColor=6, backgroundColor=0, new_block=False, link=""):
    # Initialize left with the current startX value.
        #left = self.util.sid_data.startX
        
        # Determine if the element is a string or needs text extraction
        text = element if isinstance(element, str) else element.get_text()

        # Split the text into words
        words = text.split()

        current_line = ""
        max_width = self.util.sid_data.xWidth
        original_top = top  # Save the original top position
        original_left = left  # Save the original top position
        link_start_x = left  # Initialize the starting x position of the link

        for i, word in enumerate(words):
 
            is_punctuation = word in [",", ".", ":", ";", "!", "?"]

            if len(current_line) + len(word) + (0 if is_punctuation or new_block else 1) > max_width - left:
                # Check if we're in a link and need to emit before wrapping
                if tag_name == 'a' and current_line:
                    self.emit_href(len(text), link, link_start_x, top)

                # Output the current line and reset it
                self.util.sid_data.startX = left
                self.util.sid_data.startY = top
                
                if height == None or top - original_top < height:

                    self.util.output(current_line, foregroundColor, backgroundColor)
                    time.sleep(self.sleeper)
                    if display == 'grid':
                        if width != None:
                            remaining_space = width - len(current_line)
                        else:
                            remaining_space = self.util.sid_data.xWidth - len(current_line)
                        # Output spaces until the specified width is reached
                        self.util.output(" " * remaining_space, foregroundColor, backgroundColor)

                top += 1
                if height != None and top - original_top >= height:
                    print("break")
                    break  # Stop printing if height is exceeded
                left = 0
                current_line = word
                link_start_x = left  # Reset the starting x position of the link
            else:
                current_line += ("" if is_punctuation or new_block else " ") + word

            new_block = False  # After the first word, it's no longer a new block

        if height == None or current_line and top - original_top < height:
            self.util.sid_data.startX = left
            self.util.sid_data.startY = top
            self.util.output(current_line, foregroundColor, 0)

            time.sleep(self.sleeper)
            if width != None:
                remaining_space = width - len(current_line)
                self.util.output(" " * remaining_space, 6, 0)
            
            if tag_name == 'a':
                self.emit_href(len(text), link, link_start_x, top)

        if display == 'grid':
            # Fill the remaining vertical space with empty spaces
            while height != None and top < height :
                # self.util.sid_data.startX = original_left
                self.util.sid_data.startY = top + 1
                self.util.output(" " * width, foregroundColor, backgroundColor)
                top += 1

        # left = original_left # self.util.sid_data.startX
        
        # top = original_top  # Reset startY to the original position
        
        #self.util.startY = original_top
            
        left = self.util.sid_data.startX

        return top, left


    def emit_href(self, length, link, x, y):
        """ Emit a socket event for an href link. """
        self.util.socketio.emit('a', {
            'href': link,
            'length': length,
            'x': x,
            'y': y
        }, room=self.util.request_id)



    

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
        top = self.extract_style_value(style, 'top', None)
        left = self.extract_style_value(style, 'left', None)
        if top == None:
            top = self.util.sid_data.startY
        if left == None:
            left = self.util.sid_data.startX
        return top, left 


    def extract_width(self, style, default_width=35):
        return self.extract_style_value(style, 'width', default_width)

    def extract_style_value(self, style, attribute, default_value):
        print("Input style:", style)  # Debug: Print input style
        print("Searching for attribute:", attribute)  # Debug: Print the attribute to be searched

        properties = style.split(';')
        print("Properties after split:", properties)  # Debug: Print properties list

        for prop in properties:
            prop = prop.strip()
            print("Current property:", prop)  # Debug: Print the current property

            key_value = prop.split(':')
            if len(key_value) == 2:
                key, value = key_value[0].strip(), key_value[1].strip()
                print(f"Key: '{key}', Value: '{value}'")  # Debug: Print the key and value

                if key == attribute:
                    print("Attribute found")  # Debug: Print when attribute is found
                    if 'px' in value:
                        numeric_value = int(float(value.split('px')[0].strip()))
                        print(f"Returning numeric value: {numeric_value}")  # Debug: Print the numeric value
                        return numeric_value
                    else:
                        print(f"Returning value: {value}")  # Debug: Print the non-numeric value
                        return value
            
        print(f"Attribute not found, returning default value: {default_value}")  # Debug: Print when returning default
        return default_value




    def handle_event_with_dukpy(self, js_code):
        full_js_code = self.js_code + ' ' + js_code
        print("FULL_JS_CODE")
        print(full_js_code)
        print("SELF.INPUT_VALUES")
        print(self.input_values)
        js_result = dukpy.evaljs(full_js_code, input_values=self.input_values)
        return js_result
    
    
    def handle_click(self, x, y):
        for element_id, (start, end) in self.element_positions.items():
            if start[0] <= x <= end[0] and start[1] <= y <= end[1]:
                if element_id in self.onclick_events:
                    onclick_code = self.onclick_events[element_id]
                    wrapped_js = f"""
                        function evaluateOnClick() {{
                            var result = {{}};
                            result.onClickResult = (function() {{ {onclick_code} }})();
                            result.onAlert = lastAlertMessage;  // Retrieve alert message from the global variable
                            return result;
                        }}
                        evaluateOnClick();
                    """
                    my_element = self.extract_element_for_id(element_id)
                    if my_element and my_element.name == 'button' and my_element.get('type') == 'submit':
                        self.update_previous_element()
                    js_result = self.handle_event_with_dukpy(wrapped_js)
                    print("Debug Information:", js_result.get('debugInfo'))

                    # Check onClickResult and onAlert
                    onClickResult = js_result.get('onClickResult')
                    onAlertMessage = js_result.get('onAlert')
                    
                    if isinstance(onClickResult, bool) and not onClickResult:
                        # Calculate box width
                        boxWidth = len(onAlertMessage) + 2
                        some_y_coordinate = 0
                        # Top border
                        self.util.sid_data.setStartX(0)
                        self.util.sid_data.setStartY(some_y_coordinate)  # Replace with the appropriate Y coordinate
                        self.util.output("+", 11, 4)
                        for i in range(1, boxWidth - 1):
                            self.util.output("-", 11, 4)
                        self.util.output("+", 11, 4)

                        # Output message
                        self.util.sid_data.setStartX(0)
                        self.util.sid_data.setStartY(some_y_coordinate + 1)  # Adjust Y coordinate as needed
                        self.util.output("|" + onAlertMessage + "|", 11, 4)

                        # Bottom border
                        self.util.sid_data.setStartX(0)
                        self.util.sid_data.setStartY(some_y_coordinate + 2)  # Adjust Y coordinate as needed
                        self.util.output("+", 11, 4)
                        for i in range(1, boxWidth - 1):
                            self.util.output("-", 11, 4)
                        self.util.output("+", 11, 4)
                        self.util.wait(self.alert_callback)
                        return  # Stop if JavaScript returns false

                    # Check if onClickResult is an object and handle it
                    elif isinstance(onClickResult, dict):
                        print("onClickResult2")
                        print(onClickResult)
                        # Handle focused element
                        element_id_to_focus = onClickResult.get('focusElementId')
                        if element_id_to_focus:
                            self.focus_on_element(element_id_to_focus[1:], True)
                        
                        # Handle alert message
                        alert_message = onClickResult.get('alertMessage')
                        if alert_message:
                            print("Alert:", alert_message)

                    print("onClickResult3")
                    print(onClickResult)
        
                    # Other relevant code...
                my_element = self.extract_element_for_id(element_id)
                if my_element and my_element.name == 'button' and my_element.get('type') == 'submit':
                    self.submit_function()

    def alert_callback(self):
        self.util.clear_screen()
        self.util.sid_data.startX = 0
        self.util.sid_data.startY = 0
        self.redraw_elements(False)

    def update_previous_element(self):
        print("Updating previous element:", self.previous_element_id)
        if self.previous_element_id is not None:
            previous_element = self.extract_element_for_id(self.previous_element_id)
            if previous_element:
                print(previous_element.name)
                if previous_element.name == 'input':
                    self.input_values[self.previous_element_id] = self.util.sid_data.localinput
                elif previous_element.name == 'button':
                    # Code to reset the button style
                    self.reset_button_style(previous_element)



    def focus_on_element(self, element_id, using_mouse):
        self.update_previous_element()
        matched_element_position = self.element_positions.get(element_id)
        if matched_element_position:
            start, _ = matched_element_position
            width = self.extract_width_for_id(element_id)
            self.util.sid_data.startX = start[0]
            self.util.sid_data.startY = start[1]
            self.util.sid_data.setInputType("text")

            # If there was a previously focused element, save its current input value
            if self.previous_element_id is not None:
                self.input_values[self.previous_element_id] = self.util.sid_data.localinput

            # Set the default value for the new element
            default_value = self.input_values.get(element_id, "")

            # Nested function for callback
            def callback_with_element_id(input_data):
                # Re-fetch the currently focused element
                focused_element = self.extract_element_for_id(self.previous_element_id)

                # When clicking on an element, the current_focus_index must get set according to
                # the order of elements. What is known is the id of the clicked element, but not that
                # of of current_focus_index
                if using_mouse:
                    # Find the index of the next input element
                    next_input_index = None
                    self.element_order = [e.get('id') for e in self.soup.find_all(["div", "p", "input", "button", "submit", "a"]) if e.get('id')]
                    for i, el_id in enumerate(self.element_order):
                        print(el_id+"=="+element_id)
                        if el_id == element_id:
                            next_input_index = i

                    # If an input element is found, update the current focus index
                    if next_input_index is not None:
                        self.current_focus_index = next_input_index
                        print("found "+str(next_input_index))
                    else:
                        # If no next input is found, optionally reset focus to start
                        self.current_focus_index = 1

                if focused_element.name == 'input':
                    self.input_values[element_id] = input_data
                elif focused_element.name == 'button':
                    self.input_values[element_id] = input_data
                    style = focused_element.get('style', '')
                    top, left = self.extract_position(style)
                    width = self.extract_width(style, 35)
                    element_value = focused_element.get('value')
                    
                    centered_text = self.center_text(focused_element.text, width)

                    self.util.sid_data.startX = left
                    self.util.sid_data.startY = top
                    self.util.output(centered_text, 14, 1)

            # Update the active callback
            self.active_callback = callback_with_element_id

            # Update the previous element ID
            self.previous_element_id = element_id

            focused_element = self.extract_element_for_id(element_id)
            if (focused_element.name == 'input'):
                # Ask for input with the default value for the current element
                self.handle_input_element(element_id, width, default_value)
            else:
                self.handle_button_element(element_id)

    def handle_input_element(self, element_id, width, default_value):
        # Code to handle input element
        focused_element = self.extract_element_for_id(element_id)
        if focused_element.get('type') == 'text':
            self.util.sid_data.setInputType("text")
        else:
            self.util.sid_data.setInputType("password")
        self.util.askinput(width, self.active_callback, [], default_value)

    def reset_button_style(self, button_element):
        # Reset the style of the button to its non-focused state
        # You might change the color, text style, etc.
        # Example:
        style = button_element.get('style', '')
        top, left = self.extract_position(style)
        width = self.extract_width(style, 35)
        # Pad the element_value to match the width
        element_value = button_element.get('value')
        
        centered_text = self.center_text(button_element.text, width)

        self.util.sid_data.startX = left
        self.util.sid_data.startY = top
        self.util.output(centered_text, 14, 6)

    def handle_button_element(self, element_id):
        # Code to handle button element
        button_element = self.extract_element_for_id(element_id)
        style = button_element.get('style', '')
        top, left = self.extract_position(style)
        width = self.extract_width(style, 35)
        # Pad the element_value to match the width
        element_value = button_element.get('value')
        
        centered_text = self.center_text(button_element.text, width)

        self.util.sid_data.startX = left
        self.util.sid_data.startY = top
        self.util.output(centered_text, 14, 1)

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
    
    def focus_next_element(self):
        # Check if the elements list and current focus index are initialized
        if not hasattr(self, 'element_order'):
            self.element_order = [e.get('id') for e in self.soup.find_all(["div", "p", "input", "button", "submit", "a"]) if e.get('id')]
            
        # Move to the next element in the list
        self.current_focus_index += 1

        # Wrap around if the end of the list is reached
        if self.current_focus_index > len(self.element_order)-1:
            self.current_focus_index = 0

        print("going down to "+str(self.current_focus_index))

        # Get the ID of the next element to focus
        next_element_id = self.element_order[self.current_focus_index]
        print("focus_on_element")
        # Call the existing focus function
        self.focus_on_element(next_element_id, False)
    
    def focus_previous_element(self):
    # Check if the elements list and current focus index are initialized
        if not hasattr(self, 'element_order'):
            self.element_order = [e.get('id') for e in self.soup.find_all(["div", "p", "input", "button", "submit", "a"]) if e.get('id')]
            
        # Move to the previous element in the list
        self.current_focus_index -= 1

        # Wrap around if the beginning of the list is reached
        if self.current_focus_index < 0:
            self.current_focus_index = len(self.element_order) - 1

        print("going up to "+str(self.current_focus_index))
        # Get the ID of the previous element to focus
        previous_element_id = self.element_order[self.current_focus_index]
        print("focus_on_element")
        # Call the existing focus function
        self.focus_on_element(previous_element_id, False)

    def enter(self):
        if not hasattr(self, 'element_order'):
            self.element_order = [e.get('id') for e in self.soup.find_all(["div", "p", "input", "button", "submit", "a"]) if e.get('id')]
            
        element_id = self.element_order[self.current_focus_index]

        my_element = self.extract_element_for_id(element_id)
        if my_element:
            if my_element.name == 'button' and my_element.get('type') == 'submit':
                self.submit_function()
            elif my_element.name == 'input':
                self.focus_next_element()