from bs4 import BeautifulSoup
import bs4.element
import base64
import math
import random

import dukpy
import re
import bcrypt
import time
class Renderer:
    def __init__(self, util, return_function, filename=None, db_filename=None):
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
        self.sleeper = 0.00
        self.is_current_line_empty=True
        self.tags = ["div", "span", "p", "input", "button", "submit", "a", "img"]

        self.filename = filename
        self.db_filename = db_filename

        self.inheritable_properties = [
            'color',
            'top',
            'left',
            'background-color',
            'width',
            'display',
            'place-items',
            'margin-top'
        ]
        self.html_content = ""
        self.current_focus_index = 0
        self.input_values = {}  # Dictionary to store input values for each element
        
        self.update_js_code()
        self.render_page()


    def update_js_code(self):
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

            function ajax(url, callback_function) {
                // Simulate the AJAX call by sending data to Python
                var ajaxResult = {url: url, callback_function: callback_function};
                return {ajaxResult: ajaxResult};  // Return an object with a key 'ajaxResult'
            }

            function alert(message) {
                lastAlertMessage = message;
                return { alertMessage: message };
            }
        """
        # Read the HTML template
        if self.filename == None:
            db = self.util.mongo_client['bbs']
            upload_html_collection = db['uploads_html']
            html_data = upload_html_collection.find_one({"filename": self.db_filename, 'chosen_bbs' : self.util.sid_data.chosen_bbs })
            self.html_content = base64.b64decode(html_data['file_data']);
        else:
            with open(self.filename, "r") as file:
                self.html_content = file.read()
        
        if self.util.sid_data.user_document is not None:
            db = self.util.mongo_client['bbs']
            users_collection = db['users']
            user_data = users_collection.find_one({"_id": self.util.sid_data.user_document['_id']})

            if isinstance(self.html_content, bytes):
                html_content_str = self.html_content.decode('utf-8')
            else:
                html_content_str = self.html_content

            # Replace placeholders with actual user data or remove them if not present
            all_placeholders = re.findall(r'\{userdata\.\w+\}', html_content_str)
            for placeholder in all_placeholders:
                field = placeholder.strip('{}').split('.')[1]
                if field in user_data and user_data[field] is not None:
                    html_content_str = html_content_str.replace(placeholder, str(user_data[field]))
                else:
                    html_content_str = html_content_str.replace(placeholder, '')

            # If you need to use the modified content as bytes later on, encode it back
            self.html_content = html_content_str.encode('utf-8')

        # Use regex to extract JavaScript from <script> tags
        self.additional_js_code = ""
        if isinstance(self.html_content, bytes):
            html_content_str = self.html_content.decode('utf-8')
        else:
            html_content_str = self.html_content

        script_regex = r'<script[^>]*>(.*?)</script>'
        scripts = re.findall(script_regex, html_content_str, re.DOTALL | re.IGNORECASE)

        # Add the extracted scripts to self.js_code
        for script in scripts:
            self.additional_js_code += "\n" + script
        self.js_code += self.additional_js_code
        



    def emit_ajax(self, ajax_data):
        # Use socket.io to send ajax_data to the front-end
        self.util.emit_ajax(ajax_data['url'], self.filename, ajax_data['callback_function'])
        


    def has_display_grid_style(self, style):
        if style is None:
            return False
        return re.search(r'display\s*:\s*grid', style, re.IGNORECASE) is not None


    def render_page(self):
        # Fetch user data from the database
        # Assuming 'self.util.sid_data.user_document['_id']' contains the current user's ID
        self.util.emit_waiting_for_input(False, 14)

        self.soup = BeautifulSoup(self.html_content, "html.parser")
        unique_id = 0

        for element in self.soup.find_all():
            element['uniqueid'] = str(unique_id)
            unique_id += 1

        # self.soup = self.add_data_grid_row_attributes(self.soup)
        self.soup = self.add_data_grid_attributes(self.soup)

        self.redraw_elements(True)
        self.util.emit_waiting_for_input(True, 15)

    def get_total_rows_from_parent_style_with_repeat(self, grid_container_style):
        # Search for the 'grid-template-rows' property with a 'repeat()' value
        match = re.search(r'grid-template-rows\s*:\s*repeat\((\d+),', grid_container_style)
        if match:
            # Extract the number of rows from the first capturing group
            total_rows = int(match.group(1))
        else:
            # Fallback if no 'repeat()' is found
            total_rows = 1  # Default to 1 if the style doesn't use 'repeat()' or is not found
        return total_rows

    def add_data_grid_attributes(self, soup):
        for grid_container in soup.find_all(style=self.has_display_grid_style):
            # Assuming 4 columns and 2 rows
            total_columns = 4
            total_rows = 2

            column_number = 1
            row_number = 1

            for child in grid_container.find_all(recursive=False):
                child['data-grid-column'] = str(column_number)
                child['data-grid-row'] = str(row_number)

                # Increment column_number and reset if needed
                column_number += 1
                if column_number > total_columns:
                    column_number = 1
                    row_number += 1

                # Check if we've reached the end of the grid and reset row_number if needed
                if row_number > total_rows and column_number == 1:
                    row_number = 1

        return soup



    
    def get_total_columns_from_parent_style(self, grid_container):
        style = grid_container.get('style', '')
        # Extract the 'grid-template-columns' part of the style
        for part in style.split(';'):
            if 'grid-template-columns' in part:
                columns = part.split(':')[1].strip()
                # Count the number of columns defined
                return len(columns.split(' '))
        # Default to 1 column if 'grid-template-columns' is not defined
        return 1


    def get_total_rows_from_parent_style(self, grid_container):
        # Extract the total number of rows from the parent's style
        # This is a simplified version and needs to be adjusted based on your actual CSS
        style = grid_container.get('style', '')
        if 'grid-template-rows:' in style:
            rows = style.split('grid-template-rows:')[1].split(';')[0].strip()
            return len(rows.split())
        return 0  # Default value if rows are not defined

    

    def is_nested_grid(self, container):

        # Get the parent of the current container
        parent_container = container.parent

        # Check if the parent container exists and has a display: grid style
        if parent_container and self.has_display_grid_style(parent_container.get('style')):
            return True

        return False

    def extract_fr_units_and_fixed_sizes(self, grid_style):
        fr_units = []
        fixed_sizes = []
        # Match the 'repeat()' function and extract the number of repetitions and the size
        match = re.search(r'grid-template-columns\s*:\s*repeat\((\d+),\s*(\d+px)\)', grid_style)
        if match:
            repeats = int(match.group(1))
            size = float(match.group(2).strip('px'))
            # Add the size to fixed_sizes list 'repeats' number of times
            fixed_sizes = [size] * repeats
        else:
            # Fallback to split method if 'repeat()' is not used
            columns_part = grid_style.split('grid-template-columns:')[1].split(';')[0].strip()
            for unit in columns_part.split():
                if 'fr' in unit:
                    fr_units.append(float(unit.strip('fr')))
                elif 'px' in unit:
                    fixed_sizes.append(float(unit.strip('px')))
        return fr_units, fixed_sizes

    def extract_row_fr_units_and_fixed_sizes(self, grid_style):
        row_fr_units = []
        row_fixed_sizes = []
        # Match the 'repeat()' function and extract the number of repetitions and the size
        match = re.search(r'grid-template-rows\s*:\s*repeat\((\d+),\s*(\d+px)\)', grid_style)
        if match:
            repeats = int(match.group(1))
            size = float(match.group(2).strip('px'))
            # Add the size to row_fixed_sizes list 'repeats' number of times
            row_fixed_sizes = [size] * repeats
        elif 'grid-template-rows:' in grid_style:
            # Fallback to split method if 'repeat()' is not used
            rows_part = grid_style.split('grid-template-rows:')[1].split(';')[0].strip()
            for unit in rows_part.split():
                if 'fr' in unit:
                    row_fr_units.append(float(unit.strip('fr')))
                elif 'px' in unit:
                    row_fixed_sizes.append(float(unit.strip('px')))
        return row_fr_units, row_fixed_sizes

    def calculate_grid_width(self, total_width, fr_units, fixed_sizes):
        # Subtract fixed sizes from the total width to get the width available for fractional units
        width_for_fr = total_width - sum(fixed_sizes)
        # Calculate the width that each 'fr' unit represents
        fr_unit_width = width_for_fr / sum(fr_units) if fr_units else 0
        # Calculate the width of each column
        column_widths = [fr_unit * fr_unit_width for fr_unit in fr_units] + fixed_sizes
        # Sum the widths of all columns to get the total width
        total_width = sum(column_widths)
        return total_width
    
        

   

    
    def get_start_row_of_nested_grid(self, nested_container):
        # Find the parent grid container
        parent_grid = nested_container.parent
        # Get all child elements of the parent grid container that are grid items
        grid_items = parent_grid.find_all(recursive=False)  # direct children only

        # Initialize the row index
        start_row_index = 0
        # Go through each grid item until you find the nested container
        for grid_item in grid_items:
            if grid_item == nested_container:
                break  # Found the nested container, stop counting
            if 'grid' in grid_item.get('style', ''):  # Assuming grid items have 'grid' in their style
                start_row_index += 1  # Increment for each preceding grid item

        return start_row_index

    def get_rows_spanned_by_nested_grid(self, nested_container):
        # Get the 'data-grid-row' attribute of the nested grid container
        start_row = int(nested_container.get('data-grid-row', 0)) - 1  # Convert to 0-based index
        # Assuming each grid item occupies one row
        end_row = start_row  # If the nested grid spans more rows, adjust this accordingly

        return start_row, end_row


    def calculate_height_of_spanned_rows(self, start_row, end_row, parent_row_heights):
        return sum(parent_row_heights[start_row:end_row])
    
    def get_main_grid_total_height(self, container, viewport_height):
        start_row, end_row = self.get_rows_spanned_by_nested_grid(container)

        # Get the row heights of the parent grid
        parent_row_fr_units, parent_row_fixed_sizes = self.extract_row_fr_units_and_fixed_sizes(container.parent.get('style', ''))
        parent_row_heights = self.calculate_individual_row_heights(viewport_height, parent_row_fr_units, parent_row_fixed_sizes)

        # Check if the start_row is within the range of defined rows
        if start_row >= len(parent_row_heights):
            #print("Error: Nested grid's start row exceeds the number of rows in the parent grid.")
            return 0

        # Adjust end_row if it exceeds the number of defined rows
        end_row = min(end_row, len(parent_row_heights) - 1)

        # Calculate the height for the nested grid
        nested_height = sum(parent_row_heights[start_row:end_row + 1])  # +1 because end_row is inclusive
        return nested_height

    def calculate_top_position(self, container, default_height):
        inherited_styles = self.gather_inherited_styles(container)
        add_top = inherited_styles.get('margin-top', 0)
        # Find the parent grid container using a lambda function for style filtering
        parent_grid = container.find_parent(lambda tag: tag.name in self.tags and self.has_display_grid_style(tag.get('style', '')))

        # If there's no parent grid, return default height
        if not parent_grid:
            return default_height + add_top

        # Extract row heights from the parent grid
        parent_row_fr_units, parent_row_fixed_sizes = self.extract_row_fr_units_and_fixed_sizes(parent_grid.get('style', ''))
        parent_row_heights = self.calculate_individual_row_heights(self.util.sid_data.yHeight-1, parent_row_fr_units, parent_row_fixed_sizes)

        # Get the grid row of the current container
        grid_row = int(container.get('data-grid-row', 1)) - 1  # Default to 1 if not specified, adjust for 0-based indexing

        # Calculate the top position based on the row heights up to the grid row
        top_position = sum(parent_row_heights[:grid_row]) + add_top

        return top_position

    def calculate_nested_items_top(self, nested_container, nested_row_heights):
        # Assume each item's height is 5.0px, and there is no gap between rows
        item_height = 5.0

        for index, item in enumerate(nested_container.find_all(recursive=False)):
            # Calculate the 'top' position for this item
            # Assuming 'data-grid-row' starts at 1 for the first row
            item_grid_row = int(item.get('data-grid-row', '1')) - 1
            item_top = item_height * item_grid_row

            # Construct the new style attribute with the correct 'top' value
            item_style = item.get('style', '')
            new_styles = [s for s in item_style.split(';') if not s.startswith('top')]
            new_styles.append(f"top: {item_top}px") # Add the new 'top' value
            item['style'] = '; '.join(new_styles).strip(';') # Clean up and set the style attribute

            # Debug output



    

    def calculate_individual_row_heights(self, total_height, fr_units, fixed_sizes):
        # First, add the fixed sizes directly to the row heights list
        row_heights = fixed_sizes.copy()
        
        # If there are fractional units, distribute the remaining height among them
        if fr_units:
            # Subtract the sum of fixed sizes from the total height to get the height available for fractional units
            height_for_fr = total_height - sum(fixed_sizes)
            # Calculate the height that each 'fr' unit represents
            fr_unit_height = height_for_fr / sum(fr_units)
            # Add the calculated heights for the fractional units to the row heights list
            row_heights.extend(fr_unit * fr_unit_height for fr_unit in fr_units)

        row_heights = [fr_unit * fr_unit_height for fr_unit in fr_units] + fixed_sizes
        return row_heights

    def reset_nested_grid_top(self, parent_grid, total_height):
        # Find the parent grid container
      
        # parent_grid = nested_container.find(lambda tag: 'display:grid' in tag.get('style', ''))
        # Get the 'top' property of the parent grid
        parent_top_value_str = parent_grid.get('style', '').split('top:')[1].split('px')[0] if 'top:' in parent_grid.get('style', '') else '0'
        parent_top_value = int(float(parent_top_value_str.strip()))

        # Get the row index of the nested grid within the parent grid
        parent_grid_row_index = int(parent_grid.get('data-grid-row', '0')) - 1
        # Calculate the sum of the heights of all rows before the nested grid in the parent grid
        parent_row_heights = self.calculate_row_heights(parent_grid, total_height)
        accumulated_height_before_nested = sum(parent_row_heights[:parent_grid_row_index])
        # The top position of the nested grid container is the parent's top plus the accumulated height
        nested_grid_top = parent_top_value + accumulated_height_before_nested
        return nested_grid_top

    def calculate_row_heights(self, grid_container, total_height):
        # Extract the row heights from the grid's style
        # Assume a function to extract the fr units and fixed sizes from the style string
        fr_units, fixed_sizes = self.extract_fr_units_and_fixed_sizes(grid_container.get('style', ''))
        row_heights = self.calculate_individual_row_heights(total_height, fr_units, fixed_sizes)
        return row_heights

    def parse_grid_template(self, grid_template):
        # Regular expression to find repeat function
        repeat_regex = r'repeat\((\d+),\s*([\d.]+(px|fr))\)'

        # Expand repeat function
        while re.search(repeat_regex, grid_template):
            match = re.search(repeat_regex, grid_template)
            count, value = int(match.group(1)), match.group(2)
            expanded = ' '.join([value] * count)
            grid_template = re.sub(repeat_regex, expanded, grid_template, 1)

        return grid_template


    def redraw_elements(self, useHTMLValues):
        self.processed_ids = set()
        
        def process_grid_container(container, total_width, total_height, parent_top):
            
            if self.is_nested_grid(container):
                # Assuming 'self.main_grid_style' contains the 'style' attribute of the main grid container
                main_grid_style = container.parent.get('style')  # The parent should be the main grid
                
                # Calculate the total height available for the nested grid
                nested_height = self.get_main_grid_total_height(container, total_height)
                
                nested_grid_top = self.reset_nested_grid_top(container, total_height) # total_height = 10, nested_height = 10
                
                # Extract fr units and fixed sizes from the main grid's 'grid-template-columns' style
                fr_units, fixed_sizes = self.extract_fr_units_and_fixed_sizes(main_grid_style)
                main_grid_total_width = self.calculate_grid_width(total_width, fr_units, fixed_sizes)

                # Assuming the nested grid spans the width of the first column of the main grid
                nested_width = main_grid_total_width * (fr_units[0] / sum(fr_units))
                
                # Extract the nested grid's style and use it to determine the column and row fractions
                nested_grid_style = container.get('style', '')
                nested_columns_fr_units, nested_columns_fixed_sizes = self.extract_fr_units_and_fixed_sizes(nested_grid_style)
                nested_rows_fr_units, nested_rows_fixed_sizes = self.extract_row_fr_units_and_fixed_sizes(nested_grid_style)

                # Determine the starting row of the nested grid within the parent grid
                # and accumulate the heights of all rows up to that point
                # accumulated_height = nested_grid_top  # Start from the top position of the nested grid container

                # Now use these row heights to calculate the nested grid's row heights
                nested_row_heights = self.calculate_individual_row_heights(nested_height, nested_rows_fr_units, nested_rows_fixed_sizes)

                # Call the function to calculate the top position for nested items
                self.calculate_nested_items_top(container, nested_row_heights)
                self.calculate_left_positions(container, nested_width)
                # debug_elements = container.find_all(self.tags, recursive=False)
                # nested_items = container.find_all(recursive=False)  # Get the direct children (grid items)
                
                # Calculate the width and height each 'fr' unit represents in the nested grid
                # Calculate the width each 'fr' unit represents in the nested grid
                if nested_columns_fr_units:
                    # When 'fr' units are used, they are usually equal so dividing the total width by the number of 'fr' units.
                    nested_fr_width = nested_width / sum(nested_columns_fr_units)
                    item_width = nested_fr_width
                    items_per_row = len(nested_columns_fr_units)  # The number of 'fr' units is the number of items per row
                else:
                    # Assuming all fixed sizes are equal, the number of items per row would be the total width divided by the width of one item.
                    # This assumes that nested_columns_fixed_sizes contains the width for one column, repeated for how many columns there are.
                    item_width = nested_width / len(nested_columns_fixed_sizes)

                    items_per_row = int(nested_width / item_width)  # How many items of 'item_width' fit into 'nested_width'
                    nested_fr_width = item_width  # Use fixed sizes if no 'fr' units

                # Calculate the height each 'fr' unit represents in the nested grid
                if nested_rows_fr_units:
                    nested_fr_height = nested_height / sum(nested_rows_fr_units)
                else:
                    # Use the fixed size for height if no 'fr' units. This assumes all rows are equal height.
                    nested_fr_height = nested_height

                # total_rows = len(nested_items) // items_per_row
                # row_heights = [nested_fr_height for _ in range(total_rows)]
                item_width = math.ceil(nested_fr_width)
                item_height = nested_fr_height

                nested_grid_top = self.reset_nested_grid_top(container, parent_top)
                for index, item in enumerate(container.find_all(recursive=False)):
                    column_index = index % items_per_row
                    row_index = index // items_per_row

                    # Calculate the left and top positions
                    item_left = column_index * item_width
                    item_top = nested_grid_top + row_index * item_height

                    # Update the style for each nested item
                    item_style = item.get('style', '')

                    # Check if 'height' already exists
                    height_already_exists = 'height' in item_style
                    width_already_exists = 'width' in item_style

                    # Filter out 'left', 'top', 'width' and 'height' from existing styles if they already exist
                    new_styles = [s for s in item_style.split(';') if not any(x in s for x in ['left', 'top'] 
                                    or (x in s for x in ['height'] if not height_already_exists) 
                                    or (x in s for x in ['width'] if not width_already_exists))]

                    # Process the height
                    if height_already_exists:
                        item_height = self.extract_percentage_value('height', item_style, nested_fr_height, item_height)
                    else:
                        item_height = nested_fr_height

                    # Ensure that item_height is an integer
                    item_height = int(item_height)
                    item_top = int(item_top)  # Assuming item_top is defined earlier

                    # Add 'width' style only if it doesn't already exist
                    if not width_already_exists:
                        new_styles.append(f"width: {item_width}px;")  # Assuming item_width is defined

                    extracted_position = self.extract_style_value(style, 'position',None)
                    position = extracted_position if extracted_position is not None else None
                    
                    if position == 'relative':
                        extracted_margin_top = self.extract_style_value(style, 'top',None)
                        margin_top = extracted_margin_top if extracted_margin_top is not None else None
                        if margin_top == None:
                            margin_top = inherited_styles.get('top', 0)  # Inherits margin-top if not defined in own style
                        top = 0

                    new_styles += [f"left: {item_left}px;", f"top: {item_top}px;", f"relative_top: {margin_top}px;"]  # Assuming item_left is defined

                    # Add 'height' style only if it doesn't already exist
                    if not height_already_exists:
                        new_styles.append(f"height1: {item_height}px;")

                    item['style'] = '; '.join(new_styles)

            else:
                container_style = container.get('style', '')
                row_heights = []  # Initialize row_heights to an empty list
                # Extract column styles
                if 'grid-template-columns:' in container_style:
                    columns_style = container_style.split('grid-template-columns:')[1].split(';')[0].strip()
                    # Parse and expand the grid template
                    grid_columns = self.parse_grid_template(columns_style).split()
                    total_fr_columns = sum([float(c.split('fr')[0]) for c in grid_columns if 'fr' in c])
                    fixed_width_columns = sum([int(re.findall(r'\d+', c)[0]) for c in grid_columns if 'px' in c])
                    fr_width = (total_width - fixed_width_columns) / total_fr_columns if total_fr_columns else 0
                    column_widths = [fr_width * float(c.split('fr')[0]) if 'fr' in c else int(re.findall(r'\d+', c)[0]) for c in grid_columns]
                # Extract row styles
                grid_rows = []  # Initialize grid_rows to an empty list
                if 'grid-template-rows:' in container_style:
                    rows_style = container_style.split('grid-template-rows:')[1].split(';')[0].strip()
                    # Parse and expand the grid template
                    grid_rows = self.parse_grid_template(rows_style).split()

                    # Calculate the total fraction units and fixed heights
                    total_fr_units = sum(float(r.replace('fr', '')) for r in grid_rows if 'fr' in r)
                    fixed_height_rows = sum(int(re.findall(r'\d+', r)[0]) for r in grid_rows if 'px' in r)
                    fr_unit_height = (total_height - fixed_height_rows) / total_fr_units if total_fr_units else 0

                    # Extract margin-top from the container style
                    margin_top = self.extract_style_value(container_style, 'margin-top', 0)

                    # Adjust the total height by subtracting the margin-top
                    adjusted_height = total_height - margin_top

                    # Find all grid elements
                    elements = container.find_all(self.tags, recursive=False)
                    num_elements = len(elements)

                    # Calculate the height for each element based on grid-template-rows
                    row_heights = []
                    for r in grid_rows:
                        if 'fr' in r:
                            fr_value = float(r.replace('fr', ''))
                            row_height = (adjusted_height * fr_value) / total_fr_units
                        elif 'px' in r:
                            row_height = float(r.replace('px', ''))
                        else:
                            raise ValueError(f"Invalid row height unit: {r}")
                        row_heights.append(row_height)

                    # Initialize the cumulative height with margin_top
                    cumulative_height = margin_top
                    
                    # Calculate the top position
                    # Apply the styles to the elements
                    for index, element in enumerate(elements):

                        # Calculate the left position and width based on grid-template-columns
                        left = sum(column_widths[:index % len(column_widths)]) if grid_columns else 0
                        width = column_widths[index % len(column_widths)] if grid_columns else total_width
                        height_per_element = adjusted_height / num_elements
                        height = height_per_element
                        if margin_top == 0:
                            column = index % len(grid_columns) if grid_columns else 0
                            row = index // len(grid_columns) if grid_columns else 0
                            top = sum(row_heights[:row]) if row_heights else 0
                            height = row_heights[row] if grid_rows and row < len(row_heights) else total_height
                        else:
                            # Calculate the top position for the current element
                            if index == 0:
                                # For the first element, the top is just the margin_top
                                top = margin_top
                            else:
                                # For subsequent elements, add the height of the previous element
                                previous_element = elements[index - 1]
                                # previous_height = self.extract_style_value(previous_element.get('style', ''), 'height', 0)
                                inherited_previous_styles = self.gather_inherited_styles(previous_element)

                                previous_height = self.extract_percentage_value('height', previous_element.get('style', ''), height, height)
                                cumulative_height += previous_height
                                top = cumulative_height

                        # Update the element's style
                        existing_style = element.get('style', '')

                        if 'left:' not in existing_style and 'left :' not in existing_style:
                            existing_style += f" left: {left}px;"

                        if 'top:' not in existing_style and 'top :' not in existing_style:
                            existing_style += f" top: {top}px;"

                        if 'width:' not in existing_style and 'width :' not in existing_style:
                            existing_style += f" width: {width}px;"

                        if 'relative_top:' not in existing_style and 'relative_top :' not in existing_style:
                            existing_style += f" relative_top: {margin_top}px;"

                        # Check if 'background-size: contain' is in the style
                        is_contain = 'background-size: contain' in existing_style

                        # If 'height' is not in the style, add it based on whether 'contain' is present
                        if 'height:' not in existing_style:
                            if not is_contain:
                                existing_style += f" height: {height}px;"  # Convert height to pixels if 'contain' is not present
                            else:
                                existing_style += " height: 100%;"  # Keep as 100% if 'contain' is present
                        else:
                            if not is_contain:
                                # Extract the existing height percentage and convert it to pixels
                                height_value = self.extract_percentage_value('height', existing_style, 1, height)
                                # Update the existing style string with the new height in pixels
                                existing_style = existing_style.replace(f'height: {height_value}%', f'height: {height}px')

                        element['style'] = existing_style
                #nested_grids = element.find_all(["div"], style=self.has_grid_style, recursive=True)
                
                #print(nested_grids)
                #for nested_grid in nested_grids:
                #    unique_id = nested_grid.get('uniqueid')
                #    if unique_id not in processed_ids:
                #        print(f"Processing nested grid {unique_id}...")
                #        # Calculate the width and height for the nested grid
                #        nested_top = top
                #        process_grid_container(nested_grid, width, height, processed_ids, parent_top = nested_top)
                #        processed_ids.add(unique_id)

            return

        # Start processing with the outermost grid containers
        grid_containers = self.soup.find_all(self.tags, style=self.has_grid_style, recursive=True)
        
        for container in grid_containers:
            top_position =  self.calculate_top_position(container, 0)
            process_grid_container(container, self.util.sid_data.xWidth, self.util.sid_data.yHeight-1, top_position)

        new_block = True
        last_char = ' '
        elements = self.soup.find_all(self.tags)  # Add more tags as needed
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
            margin_top, top, left = self.extract_position(style)
            self.util.sid_data.startX = left if left is not None else 0
            self.util.sid_data.startY = top if top is not None else 0

            width = self.extract_percentage_value('width', style, self.util.sid_data.xWidth, self.util.sid_data.xWidth)
            height = self.extract_percentage_value('height', style, self.util.sid_data.yHeight-1, self.util.sid_data.yHeight-1)
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

            if element.name == 'div' or element.name =='span':
                self.util.sid_data.startX = 0
                mytop, myleft, last_char, new_block = self.render_element(element, self.util.sid_data.startX, self.util.sid_data.startY, width, height, margin_top, last_char=last_char)
                self.util.sid_data.startY = mytop
                self.util.sid_data.startX = myleft
            elif element.name == 'p':
                self.util.sid_data.startX = 0
                self.util.sid_data.startY += 1  # You might need to add logic to check if this increment is necessary
                mytop, myleft, last_char, new_block = self.render_element(element, self.util.sid_data.startX, self.util.sid_data.startY, width, height, margin_top, last_char=last_char)
                self.util.sid_data.startY = mytop
                self.util.sid_data.startX = myleft
            elif element.name == 'button' or element.name=='submit':
                self.util.sid_data.startX = left
                self.util.sid_data.startY = top
                width = self.extract_width(style, default_width=35 if element.name == 'input' else 35)
                centered_text = self.center_text(element.text, width)
                self.util.output(centered_text, 14, 6)

            elif element.name == 'img':
                pass
                #self.util.startX = left
                #self.util.startY = mytop
                # self.ound_image(element.get('src', ''), left, top, width, height)
                #
                #mytop, myleft, last_char, new_block = self.render_element(element, self.util.sid_data.startX, self.util.sid_data.startY, width, height, last_char=last_char)
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
            for inheritable_attribute in self.inheritable_properties:
                value = self.extract_style_value(parent_style, inheritable_attribute, None)
                if value != None:
                    pass
                if value is not None:
                    inherited_styles[inheritable_attribute] = value

            parent = parent.parent
        return inherited_styles
    
    def gather_inherited_tags(self, element):
        parent = element.parent

        while parent is not None:
            # Check if the parent is an <a> tag
            if isinstance(parent, bs4.element.Tag) and parent.name == "a":
                # Return the href attribute (link) of the <a> tag if it exists
                return parent.get('href', None)
            # Move to the next parent
            parent = parent.parent

        # Return None if no <a> tag is found
        return None
    
    def render_element(self, element, left, initial_top, default_width, default_height, new_block=True, last_char=' '):

        original_width = default_width
        original_height = default_height

        cumulative_height = initial_top
        top = self.util.sid_data.startY
        if 'display: block' in element.parent.get('style', '') or 'display:block' in element.parent.get('style', ''):
            tag_children = [child for child in element.parent.contents if isinstance(child, bs4.element.Tag)]
            if tag_children and element is tag_children[0]:
                top = self.calculate_top_position(element.parent, default_height)

        if isinstance(element, bs4.element.Tag):
            unique_id = element.get('uniqueid')
            if unique_id in self.processed_ids:
                return initial_top, left, last_char, new_block

            tag_name = element.name
            if tag_name == 'span' or tag_name=='img':
                pass
            elif tag_name in ['div', 'p']:
                new_block = True
                pass

            style = element.get('style', '')

            # Check for a 'padding' value that sets all sides to the same value
            padding_value = self.extract_style_value(style, 'padding', None)
            if padding_value is not None:
                padding_values = [padding_value] * 4
            else:
                # Individual padding properties
                padding_style = ['padding-top', 'padding-right', 'padding-bottom', 'padding-left']
                padding_defaults = [0, 0, 0, 0]  # Default padding values if individual padding properties are not set
                padding_values = [self.extract_style_value(style, prop, default) for prop, default in zip(padding_style, padding_defaults)]

            # Extracts values from own style, set them only if not None
            extracted_color = self.extract_style_value(style, 'color', None)
            color = extracted_color if extracted_color is not None else None
            extracted_backgroundColor = self.extract_style_value(style, 'background-color', None)
            backgroundColor = extracted_backgroundColor if extracted_backgroundColor is not None else None

            extracted_background_image = self.extract_style_value(style, 'background-image',None)
            background_image = extracted_background_image if extracted_background_image is not None else ''

             # Determine if 'element' is a nested grid container
            if self.is_nested_grid(element):
                # Calculate the total height of the nested grid container
                total_height = self.get_main_grid_total_height(element, default_height)
                current_height = total_height

            else:
                # Calculate the height of the current element based on its content
                current_height = self.calculate_element_height(element, default_width)

            # Set the top position for the current element
            # top = cumulative_height

            # Update the cumulative height for the next element
            cumulative_height += current_height
            height = cumulative_height
            

            inherited_styles = self.gather_inherited_styles(element)
            if tag_name == 'span':
                # Handle span tags as inline elements
                display = self.extract_style_value(element.get('style', ''), 'display', 'inline')
                # Continue rendering inline, no new block context
            else:
                # For other elements, extract and handle display property as before
                extracted_display = self.extract_style_value(style, 'display', None)
                display = extracted_display if extracted_display else self.get_default_display(tag_name)

            

            extracted_margin_top = self.extract_style_value(style, 'margin-top',None)
            margin_top = extracted_margin_top if extracted_margin_top is not None else None
            if margin_top == None:
                    margin_top = inherited_styles.get('margin-top', 0)  # Inherits margin-top if not defined in own style

            if display == 'grid' or element.name == 'img':
                
                extracted_position = self.extract_style_value(style,'position', None)
                position = extracted_position if extracted_position is not None else None


                if position == 'relative':
                    extracted_margin_top = self.extract_style_value(style,'top', None)
                    margin_top = extracted_margin_top if extracted_margin_top is not None else None
                    # margin_top = inherited_styles.get('relative_top', 0)  # Inherits top if not defined in own style
                    top = inherited_styles.get('top', 0)  # Inherits top if not defined in own style'''
            
            if display != 'inline':
                extracted_top = self.extract_style_value(style,'top', None)
                top = extracted_top if extracted_top is not None else None
                if top == None:
                    top = inherited_styles.get('top', 0)  # Inherits top if not defined in own style             

                extracted_left = self.extract_style_value(style,'left', None)
                left = extracted_left if extracted_left is not None else None
                if left == None:
                    left = inherited_styles.get('left', 0)  # Inherits left if not defined in own style

            
            if color == None:
                color = inherited_styles.get('color', color)  # Inherits color if not defined in own style
            if color == None:
                color = 6

            extracted_place_items = self.extract_style_value(style,'place-items', None)
            place_items = extracted_place_items if extracted_place_items is not None else None
            if place_items == None:
                place_items = inherited_styles.get('place-items', None)  # Inherits width if not defined in own style


            extracted_text_align = self.extract_style_value(style,'text-align', None)
            text_align = extracted_text_align if extracted_text_align is not None else None

            if backgroundColor == None:
                backgroundColor = inherited_styles.get('background-color', None)  # Inherits background-color if not defined in own style
            if backgroundColor == None:
                backgroundColor = 0

            extracted_width = self.extract_style_value(style,'width', None)
            default_width = extracted_width if extracted_width is not None else None
            if default_width == None:
                default_width = inherited_styles.get('width', self.util.sid_data.xWidth)  # Inherits width if not defined in own style

            extracted_height = self.extract_style_value(style,'height', None)
            height = extracted_height if extracted_height is not None else None
            if height == None:
                height = inherited_styles.get('height', default_height)  # Inherits height
            # Recursively process child elements (depth-first)
            tag_name = element.name

            if tag_name == 'img':
                imgwidth = self.extract_percentage_value('width', element.get('style', ''), default_width, original_width)
                imgheight = self.extract_percentage_value('height', element.get('style', ''), height, original_height)
                imgurl = element.get('src')

                if place_items == "center" and height is not None:
                    # Calculate center of the div
                    center_x = left + original_width / 2
                    center_y = top + original_height / 2

                    # Calculate the position to start the image to make it centered
                    # Assuming imgwidth and imgheight are the dimensions of the image
                    img_left = center_x - imgwidth / 2
                    img_top = center_y - imgheight / 2

                    # Ensure the image does not go out of the div's boundaries
                    img_left = max(left, img_left)
                    img_top = max(top, img_top)

                    self.util.emit_background_image(imgurl, img_left, img_top, imgwidth, imgheight, False)
                else:
                    self.util.emit_background_image(imgurl, left, top, imgwidth, imgheight, False)
                return initial_top, left, last_char, new_block
          

            if tag_name == 'p':
                top += 1
                left = 0
 
           # Assuming this function is part of a class with self.util already defined

            for child in element.children:
                if isinstance(child, bs4.element.Tag):
                    # Recursively call render_element for child tags
                    top, left, last_char, new_block = self.render_element(child, left, top, default_width, height, new_block=new_block, last_char=last_char)
                    
                elif isinstance(child, bs4.NavigableString):
                    child_text = child
                    if child_text:
                        child_text = child_text.strip()
                        inherited_link = self.gather_inherited_tags(child)

                        if inherited_link:
                            if len(inherited_link) > 1:
                                self.util.emit_href(default_width, inherited_link, left, top, height)
                            else:
                                self.util.emit_link(default_width, inherited_link, self.key_pressed, child.parent.get('uniqueid'), left, top, height)
                        
                        if background_image:
                            cleaned_url = self.clean_background_image_url(background_image)  # Assuming a method to clean the URL

                            print(child.parent.get('style', ''))
                            extracted_height = self.extract_style_value(child.parent.get('style', ''), 'height', None)
                            is_grid_full_height = 'display: grid' in child.parent.get('style', '') and extracted_height == '100%'
      
                            dynamicHeight = is_grid_full_height  # Set dynamicHeight based on the extracted style

                            self.util.emit_background_image(cleaned_url, left, top, default_width, height, False, False, dynamicHeight)

                        else:
                            if backgroundColor != 0 or len(child_text.strip())>0:
                                if unique_id not in self.processed_ids:
                                    self.processed_ids.add(unique_id)
                                    top, left, last_char, new_block = self.output_text(display, child_text, left, top, default_width, height, tag_name, color, backgroundColor, tuple(padding_values), place_items, text_align, margin_top, new_block=new_block, last_char=last_char)
                        
                        time.sleep(self.sleeper)
                        # After text, it's no longer the start of a new block

            # Mark this Tag element as processed
            self.processed_ids.add(unique_id)

        # If the element is a string (NavigableString), process it directly
        elif isinstance(element, bs4.NavigableString):
            child_text = element
            if child_text and backgroundColor != None and backgroundColor != 0:
                child_text = child_text.strip()
                # Output text with the color extracted from the parent Tag
                parent_tag_name = element.parent.name if element.parent else None
                inherited_link = self.gather_inherited_tags(element)
                if inherited_link:
                            if len(inherited_link)>1:
                                self.util.emit_href(default_width, inherited_link, left, top, height)
                            else:
                                self.util.emit_link(default_width, inherited_link, self.key_pressed, element.get('uniqueid'), left, top, height)
                
                if background_image != None and background_image != '':
                    cleaned_url = background_image.replace("url('", "").replace("')", "")
                    self.util.emit_background_image(cleaned_url, left, top, width, height, False)
                else:
                    if backgroundColor != 0 or len(child_text.strip())>0 :
                        if unique_id not in self.processed_ids:
                            self.processed_ids.add(unique_id)
                            top, left, last_char, new_block = self.output_text(display, child_text, left, top, default_width, height, parent_tag_name, backgroundColor, 4, tuple(padding_values), place_items, text_align, margin_top, last_char=last_char, new_block=new_block)
                
                time.sleep(self.sleeper)
                
            
        return top, left, last_char, new_block


    def clean_background_image_url(self, background_image):
        """
        Cleans the background image URL by stripping specific patterns and handling 'rand(x,y)'.
        """
        # Strip url('') pattern
        cleaned_url = background_image.replace("url('", "").replace("')", "")

        # Find the pattern 'rand(x,y)' in the string and replace it with a random number
        match = re.search(r'\{rand\((\d+),(\d+)\)\}', cleaned_url)
        if match:
            # Extract x and y values
            x, y = map(int, match.groups())
            # Generate a random number between x and y
            random_number = random.randint(x, y)
            # Replace the 'rand(x,y)' pattern with the random number
            cleaned_url = re.sub(r'\{rand\(\d+,\d+\)\}', str(random_number), cleaned_url)

        return cleaned_url
    def get_default_display(self, tag_name):
        # Define default display values for common tags
        default_display_values = {
            'div': 'block',
            'span': 'inline',
            'p': 'block',
        }
        return default_display_values.get(tag_name, 'block')  # Default to 'block' if tag not found

    def key_pressed(self, char):
        self.util.sid_data.menu.handle_key(char)
        pass


    def has_grid_style(self, style):
        if style is None:
            return False
        return 'grid-template-columns:' in style or 'grid-template-rows:' in style

    
    def get_horizontal_space(self, current_line, display, maximum, text_align):
        horizontal_space = 0
        if display == 'grid':
            if text_align == "center":
                line_length = len(current_line)
                horizontal_space = (maximum - line_length) // 2
        return horizontal_space

    def output_text(self, display, element, left, top, width, height, tag_name, foregroundColor, backgroundColor, padding, place_items, text_align, margin_top, new_block=False, last_char=None):
        text = element if isinstance(element, str) else element.get_text()
        words = text.split() or [" "]

         # Determine if a space is needed at the start of this element
        first_word_is_punctuation = words[0] in [",", ".", ":", ";", "!", "?"] if words else False

        need_space = True # last_char and last_char != ' ' # and not first_word_is_punctuation # and not new_block

        text = text + " " if need_space else text
        current_line = ""

        original_top = top  # Save the original top position
        original_left = left  # Save the original top position
        link_start_x = left  # Initialize the starting x position of the link

        padding_top, padding_right, padding_bottom, padding_left = padding
        
       
        if height:
            if display == 'grid':
                max_width = width
            else: 
                max_width = self.util.sid_data.xWidth
            
            if display == 'grid':
                total_lines = self.calculate_total_lines(words, width, padding_left, padding_right)
        
                # Adjust top for vertical centering
                if place_items == "center" and height is not None:
                    lines_to_center = min(total_lines, height)
                    vertical_space = height - lines_to_center
                    for _ in range(vertical_space // 2):
                        self.util.sid_data.startX = left
                        self.util.sid_data.startY = top
                        self.util.output(" " * width, foregroundColor, backgroundColor)
                        top += 1
                if margin_top > 0:
                    for _ in range(margin_top):
                        self.util.sid_data.startX = left
                        self.util.sid_data.startY = top
                        self.util.output(" " * width, foregroundColor, backgroundColor)
                        top += 1

                for _ in range(padding_top):
                    self.util.sid_data.startX = left
                    self.util.sid_data.startY = top
                    self.util.output(" " * width, foregroundColor, backgroundColor)
                    top += 1
                    time.sleep(self.sleeper)

            for i, word in enumerate(words):
    
                is_punctuation = word in [",", ".", ":", ";", "!", "?"]

                if display =='grid':
                    if max_width != None:
                        maximum = max_width - padding_left - padding_right
                    else:
                        maximum = 0
                else:
                    maximum = max_width - left
                if len(current_line) + len(word) + (0 if is_punctuation or new_block else 1) > maximum:
                    
                    if display  == "grid":                    
                        self.util.sid_data.startX = original_left
                    else:
                        self.util.sid_data.startX = left
                    
                    self.util.sid_data.startY = top

                    horizontal_space = self.get_horizontal_space( current_line, display, maximum, text_align)
                    self.util.output(" " * (padding_left + horizontal_space)  + current_line, foregroundColor, backgroundColor)
                    new_block = False
                

                    time.sleep(self.sleeper)
                    remaining_space = width - len(current_line) - horizontal_space if width is not None else self.util.sid_data.xWidth - len(current_line) - horizontal_space
                    # Output spaces until the specified width is reached
                    self.util.output(" " * remaining_space, foregroundColor, backgroundColor)
                    top += 1
                    if height != None and top - original_top >= height:
                        break  # Stop printing if height is exceeded
                    if display == 'grid':
                        left = original_left  # Reset left to original_left instead of 0
                    else:
                        left = 0
                    current_line = word
                    link_start_x = left  # Reset the starting x position of the link
                else:
                    current_line += ("" if is_punctuation or new_block else " ") + word
                    new_block = False

            if height == None or (current_line and top - original_top < height):
                horizontal_space = self.get_horizontal_space( current_line, display, maximum, text_align)
                self.util.sid_data.startX = left
                self.util.sid_data.startY = top
                self.util.output(" " * (padding_left + horizontal_space) , foregroundColor, backgroundColor)
                self.util.output(current_line, foregroundColor, backgroundColor)
                new_block = False
                last_char = current_line[-1] if current_line else None
                time.sleep(self.sleeper)
                if display == 'grid':
                    if width != None:
                        remaining_space = width - len(current_line) - horizontal_space
                        self.util.output(" " * remaining_space, foregroundColor, backgroundColor)

                    if height != None and original_top != None:
                        myheight = height + original_top - 1
                    else:
                        myheight = 0

                    if myheight > self.util.sid_data.yHeight:
                        myheight = self.util.sid_data.yHeight - original_top
                    while height != None and top < myheight:
                        self.util.sid_data.startX = left
                        self.util.sid_data.startY = top + 1
                    
                        self.util.output(" " * width, foregroundColor, backgroundColor)
                        top += 1
                        time.sleep(self.sleeper)
                    
                    # Update top and left for the next element
                    top = 0 # original_top + myheight-1 if height is not None else top + 0

                    if width != None:
                        left = original_left + width if original_left + width <= max_width else 0
                    else:
                        left = original_left
                else:
                    left = self.util.sid_data.startX

                if left == 0 and display == 'grid':
                        top += 1  # Move down a row if we've hit the max width
            else:
                left = self.util.sid_data.startX
            
        
        return top, left, last_char, new_block


   

    

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

        margin_top = 0
        top = self.extract_style_value(style, 'top', None)

        position = self.extract_style_value(style, 'position', None)
        if position == 'relative':
            relative_top = self.extract_style_value(style, 'relative_top', None)
            margin_top = relative_top

        left = self.extract_style_value(style, 'left', None)
        if top == None:
            top = self.util.sid_data.startY
        if left == None:
            left = self.util.sid_data.startX
        return margin_top, top, left 


    def extract_width(self, style, default_width=35):
        return self.extract_style_value(style, 'width', default_width)

    def extract_style_value(self, style, attribute, default_value):
        properties = style.split(';')
        last_value = default_value  # Initialize with the default value

        for prop in properties:
            prop = prop.strip()
            colon_index = prop.find(':')
            if colon_index != -1:
                key = prop[:colon_index].strip()
                value = prop[colon_index + 1:].strip()

                if key == attribute:
                    if 'calc' in value:
                        last_value = self.calculate_css_calc(value)
                    elif 'px' in value:
                        last_value = int(float(value.split('px')[0].strip()))
                    else:
                        last_value = value

        return last_value

    def extract_percentage_value(self, attribute, style, default_value, current_height):
        if current_height == None:
            current_height = self.util.sid_data.yHeight -1

        properties = style.split(';')
        #print("Properties after split:", properties)  # Debug: Print properties list

        for prop in properties:
            prop = prop.strip()
            #print("Current property:", prop)  # Debug: Print the current property

            colon_index = prop.find(':')
            if colon_index != -1:
                key = prop[:colon_index].strip()
                value = prop[colon_index + 1:].strip()

                #print(f"Key: '{key}', Value: '{value}'")  # Debug: Print the key and value

                if key == attribute:
                    if 'calc' in value:
                        return self.calculate_css_calc(value)
                    elif 'px' in value:
                        numeric_value = int(float(value.split('px')[0].strip()))
                        return numeric_value
                    elif '%' in value:
                        percentage_value = float(value.split('%')[0].strip()) / 100
                        calculated_height = int(current_height * percentage_value)
                        return calculated_height
                    else:
                        return default_value
        return default_value



    def handle_event_with_dukpy(self, js_code):
        full_js_code = self.js_code + ' ' + js_code
        js_result = dukpy.evaljs(full_js_code, input_values=self.input_values)
            
        return js_result
    
    
    def handle_click(self, x, y):
        print("Handle click")
        print(self.js_code)
        execute_submit = True
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
                    print(wrapped_js)
                    my_element = self.extract_element_for_id(element_id)
                    if my_element and my_element.name == 'button' and my_element.get('type') == 'submit':
                        self.update_previous_element()
                    js_result = self.handle_event_with_dukpy(wrapped_js)

                    execute_submit = self.evaluateJSResult(js_result)
        
                    # Other relevant code...
                my_element = self.extract_element_for_id(element_id)
                if my_element and my_element.name == 'button' and my_element.get('type') == 'submit' and execute_submit == True:
                    self.submit_function()

    def alert_callback(self):
        self.update_js_code()
        self.util.clear_screen()
        self.util.sid_data.startX = 0
        self.util.sid_data.startY = 0
        self.redraw_elements(True)
        self.util.emit_waiting_for_input(True, 15)

    def update_previous_element(self):
        if self.previous_element_id is not None:
            previous_element = self.extract_element_for_id(self.previous_element_id)
            if previous_element:
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
                    self.element_order = [e.get('id') for e in self.soup.find_all(self.tags) if e.get('id')]
                    for i, el_id in enumerate(self.element_order):
                        if el_id == element_id:
                            next_input_index = i

                    # If an input element is found, update the current focus index
                    if next_input_index is not None:
                        self.current_focus_index = next_input_index
                    else:
                        # If no next input is found, optionally reset focus to start
                        self.current_focus_index = 1

                if focused_element.name == 'input':
                    self.input_values[element_id] = input_data
                elif focused_element.name == 'button':
                    self.input_values[element_id] = input_data
                    style = focused_element.get('style', '')
                    margin_top, top, left = self.extract_position(style)
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
        margin_top, top, left = self.extract_position(style)
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
        margin_top, top, left = self.extract_position(style)
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
            self.element_order = [e.get('id') for e in self.soup.find_all(self.tags) if e.get('id')]
            
        # Move to the next element in the list
        self.current_focus_index += 1

        # Wrap around if the end of the list is reached
        if self.current_focus_index > len(self.element_order)-1:
            self.current_focus_index = 0

        # Get the ID of the next element to focus
        next_element_id = self.element_order[self.current_focus_index]
        # Call the existing focus function
        self.focus_on_element(next_element_id, False)
    
    def focus_previous_element(self):
    # Check if the elements list and current focus index are initialized
        if not hasattr(self, 'element_order'):
            self.element_order = [e.get('id') for e in self.soup.find_all(self.tags) if e.get('id')]
            
        # Move to the previous element in the list
        self.current_focus_index -= 1

        # Wrap around if the beginning of the list is reached
        if self.current_focus_index < 0:
            self.current_focus_index = len(self.element_order) - 1

        # Get the ID of the previous element to focus
        previous_element_id = self.element_order[self.current_focus_index]
        # Call the existing focus function
        self.focus_on_element(previous_element_id, False)

    def enter(self):
        if not hasattr(self, 'element_order'):
            self.element_order = [e.get('id') for e in self.soup.find_all(self.tags) if e.get('id')]
            
        element_id = self.element_order[self.current_focus_index]

        my_element = self.extract_element_for_id(element_id)
        if my_element:
            if my_element.name == 'button' and my_element.get('type') == 'submit':
                self.submit_function()
            elif my_element.name == 'input':
                self.focus_next_element()


    
    def calculate_left_positions(self, grid_container, total_width):
    # Extract the style attribute from the grid container
        grid_style = grid_container.get('style', '')

        # Use the extract function to get fr units and fixed sizes
        fr_units, fixed_sizes = self.extract_fr_units_and_fixed_sizes(grid_style)

        # Assume total width is known, and calculate column widths based on fr and fixed sizes
        # For simplicity, this example will distribute the remaining width evenly across fr units
        # You may need a more complex calculation based on the actual CSS specifications for fr units
        remaining_width = total_width - sum(fixed_sizes)
        fr_unit_width = remaining_width / sum(fr_units) if fr_units else 0

        column_widths = [size if size else fr_unit_width for size in fixed_sizes + [fr_unit_width] * len(fr_units)]

        for index, item in enumerate(grid_container.find_all(recursive=False)):
            column_index = int(item.get('data-grid-column', '1')) - 1
            item_left = sum(column_widths[:column_index])

            # Update the 'left' position
            item_style = item.get('style', '')
            new_styles = [s for s in item_style.split(';') if not s.startswith('left')]
            new_styles.append(f"left: {item_left}px")
            item['style'] = '; '.join(new_styles).strip(';')
            # Optionally, print debug information


            #existing_style = item.get('style', '')
            #new_left_style = f"left: {item_left}px;"
            #item['style'] = self.merge_styles(existing_style, new_left_style)
            #print(f"Debug: Updated Item Style: {item['style']}")

            

    def calculate_total_lines(self, words, width, padding_left, padding_right):
        total_lines = 0
        current_line_length = 0

        for word in words:
            is_punctuation = word in [",", ".", ":", ";", "!", "?"]
            word_length = len(word)

            if width == None:
                available_width = 0
            else:
                # Calculate the available width considering padding
                available_width = width - padding_left - padding_right

            # Check if the word fits in the current line
            if current_line_length + word_length + (0 if is_punctuation else 1) > available_width:
                # Increment line count and reset current line length
                total_lines += 1
                current_line_length = word_length
            else:
                # Update the current line length
                current_line_length += word_length + (0 if is_punctuation else 1)

        # Add the last line if there's any content in it
        if current_line_length > 0:
            total_lines += 1

        return total_lines


    def calculate_css_calc(self, calc_expression):
        # Remove 'calc' and unnecessary characters
        calc_expression = calc_expression.replace('calc', '').replace('(', '').replace(')', '').strip()

        # Split by '+' and '-' operators
        tokens = re.split('(\+|\-)', calc_expression)

        result = 0
        operator = '+'
        for token in tokens:
            token = token.strip()
            if token in ['+', '-']:
                operator = token
            else:
                # Handle different units
                if 'px' in token:
                    value = math.ceil(float(token.replace('px', '').strip()))
                elif 'vh' in token:
                    vh_value = float(token.replace('vh', '').strip())
                    value = math.ceil((vh_value / 100) * self.util.sid_data.yHeight)
                elif 'vw' in token:
                    vw_value = float(token.replace('vw', '').strip())
                    value = math.ceil((vw_value / 100) * self.util.sid_data.xWidth)
                else:
                    value = 0  # Or handle other units if necessary

                # Apply the operation
                if operator == '+':
                    result += value
                elif operator == '-':
                    result -= value

        return result

    
    def extract_text_content(self, element):
        # Extract and return the text content of the element
        # Handle any specific cases, like nested tags or special characters
        return element.get_text()

    def extract_padding_values(self, element):
        # Extract padding values from the element's style
        # Assuming you have a method for extracting specific style values
        style = element.get('style', '')
        padding_left = self.extract_style_value(style, 'padding-left', 0)
        padding_right = self.extract_style_value(style, 'padding-right', 0)
        return padding_left, padding_right

    def calculate_element_height(self, element, width):
            # Extract the text content of the element
            text_content = self.extract_text_content(element)
            words = text_content.split()

            # Initialize variables for line calculation
            total_lines = 0
            current_line_length = 0

            # Extract padding values (assuming a method to extract padding values)
            padding_left, padding_right = self.extract_padding_values(element)

            # Calculate the available width considering padding
            available_width = width - padding_left - padding_right

            for word in words:
                is_punctuation = word in [",", ".", ":", ";", "!", "?"]
                word_length = len(word)

                # Check if the word fits in the current line
                if current_line_length + word_length + (0 if is_punctuation else 1) > available_width:
                    total_lines += 1  # Increment line count
                    current_line_length = word_length  # Reset line length
                else:
                    current_line_length += word_length + (0 if is_punctuation else 1)

            # Add the last line if there's any content in it
            if current_line_length > 0:
                total_lines += 1

            return total_lines

    def on_ajax_response(self, response_data):
        # Extract the AJAX call result from the response_data
        print("ADDITIONAL CODE"+self.additional_js_code+"***")
        print(response_data)
        ajax_result = response_data['text']
        filename = response_data['filename']
        self.filename = filename
        callback_function = response_data['callback_function']

        # The JavaScript code with a placeholder for the AJAX result
        onclick_code = 'return '+callback_function+"('"+str(ajax_result)+"')"
        wrapped_js = f"""
            function evaluateOnClick() {{
                var result = {{}};
                result.onClickResult = (function() {{ {onclick_code} }})();
                result.onAlert = lastAlertMessage;  // Retrieve alert message from the global variable
                return result;
            }}
            evaluateOnClick();
        """
        
        self.update_js_code()
        print(self.js_code+wrapped_js)
        final_result = dukpy.evaljs(self.js_code+wrapped_js, input_values=self.input_values)
        evaluateResult = self.evaluateJSResult(final_result)
        print("evaluateResult")
        print(evaluateResult)
        if evaluateResult == True:
            self.submit_function()

    def evaluateJSResult(self, js_result):
        # Check onClickResult and onAlert
        print(js_result)
        onClickResult = js_result.get('onClickResult')
        print("onClickResult")
        print(onClickResult)
        onAlertMessage = js_result.get('onAlert')
        print("onAlertMessage")
        print(onAlertMessage)
        
        

        # Check if onClickResult is an object and handle it
        if isinstance(onClickResult, dict):
            # Handle focused element
            element_id_to_focus = onClickResult.get('focusElementId')
            if element_id_to_focus:
                print("element_id_to_focus")
                self.focus_on_element(element_id_to_focus[1:], True)
                return False
            
            # Handle ajax result
            ajax_data = onClickResult.get('ajaxResult')
            print("ajax_data")
            if ajax_data and 'url' in ajax_data:
                # You have the URL from the ajax call, handle it as needed
                # For example, you could initiate a request or handle it differently
                # based on the URL value
                self.emit_ajax(ajax_data)
                return False
            
        elif isinstance(onClickResult, bool):
            if onClickResult==False:
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
                return False # Stop if JavaScript returns false
            
        return True