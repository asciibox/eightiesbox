from bs4 import BeautifulSoup
import bs4.element

import dukpy
import re
import bcrypt

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
        elements = self.soup.find_all(["div", "p", "input", "button", "submit"])  # Add more tags as needed
        self.element_order = [e.get('id') for e in self.soup.find_all(["div", "p", "input", "button", "submit"]) if e.get('id')]

        for element in elements:
            if self.first_input_element == None and element.name == 'input':
                self.first_input_element = element
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
            if left != None:
                self.util.sid_data.startX = left
            if top != None:
                self.util.sid_data.startY = top


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
                    print("Setting "+element_id)
                    self.input_values[element_id] = element_value
            elif element_id != None:
                element_value = self.input_values[element_id]

            if element.name == 'div':
                
                mytop, myleft = self.render_element(element, self.util.sid_data.startX, self.util.sid_data.startY)
                self.util.sid_data.startY = mytop
                self.util.sid_data.startX = myleft
            elif element.name == 'p':
                self.util.sid_data.startY += 2  # You might need to add logic to check if this increment is necessary
                mytop, myleft = self.render_element(element, self.util.sid_data.startX, self.util.sid_data.startY)
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

    
    def render_element(self, element, left, top, color = 6, new_block=True):
        
        # Check if the element is a Tag and process it
        if isinstance(element, bs4.element.Tag):
            unique_id = element.get('uniqueid')

            # Check if this Tag's unique_id has already been processed
            if unique_id in self.processed_ids:
                return top, left

            # Apply specific styles and processing for this Tag element
            style = element.get('style', '')
            color = self.extract_color(style)

            # Recursively process child elements (depth-first)
            for child in element.children:
                if isinstance(child, bs4.element.Tag):
                    # If the child is a Tag, recursively call render_element
                    top, left = self.render_element(child, left, top, color, new_block=new_block)
                    # After a tag, it's no longer the start of a new block
                    new_block = False
                elif isinstance(child, bs4.NavigableString):
                    child_text = child.strip()
                    if child_text:
                        top, left = self.output_text(child_text, left, top, color, new_block=new_block)
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
                top, left = self.output_text(child_text, left, top, color)

        return top, left














    def output_text(self, element, left, top, foregroundColor=6, new_block=False,):
        # Initialize left with the current startX value.
        left = self.util.sid_data.startX

        # Determine if the element is a string or needs text extraction
        text = element if isinstance(element, str) else element.get_text()

        # Split the text into words
        words = text.split()

        current_line = ""
        max_width = self.util.sid_data.xWidth

        for i, word in enumerate(words):
            is_punctuation = word in [",", ".", ":", ";", "!", "?"]

            if len(current_line) + len(word) + (0 if is_punctuation or new_block else 1) > max_width - left:
                # Output the current line and reset it
                self.util.sid_data.startX = left
                self.util.sid_data.startY = top
                self.util.output(current_line, foregroundColor, 0)
                top += 1
                left = 0
                current_line = word
            else:
                current_line += ("" if is_punctuation or new_block else " ") + word

            new_block = False  # After the first word, it's no longer a new block

        if current_line:
            self.util.sid_data.startX = left
            self.util.sid_data.startY = top
            self.util.output(current_line, foregroundColor, 0)

        left = self.util.sid_data.startX
        top = self.util.sid_data.startY

        return top, left



    

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
            left = 0
        return top, left 

    def extract_color(self, style):
        return self.extract_style_value(style, 'color', 6)

    def extract_width(self, style, default_width=35):
        return self.extract_style_value(style, 'width', default_width)

    def extract_style_value(self, style, attribute, default_value):
        if attribute + ':' in style:
            return int(style.split(attribute + ':')[1].split('px')[0].strip())
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


                if using_mouse:
        # Find the index of the next input element
                    next_input_index = None
                    self.element_order = [e.get('id') for e in self.soup.find_all(["div", "p", "input", "button", "submit"]) if e.get('id')]
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
            self.element_order = [e.get('id') for e in self.soup.find_all(["div", "p", "input", "button", "submit"]) if e.get('id')]
            
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
            self.element_order = [e.get('id') for e in self.soup.find_all(["div", "p", "input", "button", "submit"]) if e.get('id')]
            
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
            self.element_order = [e.get('id') for e in self.soup.find_all(["div", "p", "input", "button", "submit"]) if e.get('id')]
            
        element_id = self.element_order[self.current_focus_index]

        my_element = self.extract_element_for_id(element_id)
        if my_element:
            if my_element.name == 'button' and my_element.get('type') == 'submit':
                self.submit_function()
            elif my_element.name == 'input':
                self.focus_next_element()