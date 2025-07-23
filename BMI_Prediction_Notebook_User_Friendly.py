#   Copyright (c) 2025. UWA (in the framework of the ICRAR)
#  #
#   Redistribution and use in source and binary forms, with or without modification, are permitted
#   provided that the following conditions are met:
#  #
#   1. Redistributions of source code must retain the above copyright notice, this list of conditions and
#   the following disclaimer.
#  #
#   2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions
#   and the following disclaimer in the documentation and/or other materials provided with the distribution.
#  #
#   3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or
#   promote products derived from this software without specific prior written permission.
#  #
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#   WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#   DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#   FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#   DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#   SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#   CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#   OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
#   THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#%% [markdown]
# # Year 8 BMI Prediction Calculator
#
# Welcome to the Year 8 BMI Prediction Calculator! This tool helps you predict a child's Body Mass Index (BMI) at Year 8 based on measurements and factors from earlier years.
#
# ## What is BMI?
#
# Body Mass Index (BMI) is a value calculated from a person's weight and height. It provides a simple numeric measure of a person's thickness or thinness, allowing health professionals to discuss weight problems more objectively with their patients.
#
# ## How to Use This Tool
#
# This calculator is designed to be simple to use, even if you have no experience with programming. Just follow these steps:
#
# 1. **Select a Prediction Mode**: Choose between Simple Mode (10 variables) or Comprehensive Mode (20 variables)
# 2. **Choose a Prediction Method**: Select either Single Sample (for one child) or Batch Processing (for multiple children)
# 3. **Enter the Required Information**: Fill in the requested measurements and information
# 4. **Get Your Prediction**: Click the "Predict BMI" button to see the results
#
# Let's get started!

#%% [markdown]
# ## Setup (Technical - You Can Skip This Section)
#
# The cell below loads the necessary components for the calculator to work. You don't need to understand this code - just run the cell by clicking the play button ▶️ or pressing Shift+Enter.

#%%
# This cell loads all the necessary components for the calculator
# You don't need to understand this code - just run the cell

import pandas as pd
import numpy as np
import os
import csv
import json
import io
from IPython.display import display, HTML, FileLink
import ipywidgets as widgets

# Import the BMI calculation functions
from run.run import add_y1y5_bmiz, calculate_y8_bmi
from bmizscore.zscore import get_bmiz_singlevalue as get_y5_bmiz
from pygrowup import Observation as get_y1_bmifa

# Load variable descriptions
def load_variable_descriptions():
    descriptions = {}
    values = {}
    with open("calculator/codes.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            descriptions[row["name"]] = row["description"]
            if row["values"]:
                values[row["name"]] = [v.strip() for v in row["values"].split("\n")]
    return descriptions, values

variable_descriptions, variable_values = load_variable_descriptions()

# Define the variables for each mode
mode_variables = {
    "simple": [
        'occupcode_m_0',
        'hhincome_0',
        'y1_bmifa',
        'y5_a5',
        'y5_a6',
        'y5_a7',
        'y5_a8',
        'y5_a9',
        'y5_a10',
        'y5_bmiz',
        'preg_gain'
    ],
    "comprehensive": [
        'occupcode_m_0',
        'agebirth_m_y',
        'height_m',
        'mode_delivery',
        'height_f1',
        'hhincome_0',
        'solid_food',
        'ga_wt2',
        'y1_a10',
        'y5_a5',
        'y5_a6',
        'y5_a7',
        'y5_a8',
        'y5_a9',
        'y5_a10',
        'y5_bmiz',
        'y1_bmifa',
        'ga_us',
        'prepreg_cig',
        'preg_gain'
    ]
}

# Define the required variables for calculating derived variables
derived_variables = {
    "y5_bmiz": ["y5_agemos", "sex", "y5_a2", "y5_a1"],
    "y1_bmifa": ["y1_agemos", "sex", "y1_a2", "y1_a1"]
}

# Get all required variables for a mode
def get_required_variables(mode):
    # Get the variables for the mode
    required = set(mode_variables[mode])
    
    # Add variables needed for derived variables
    for var in mode_variables[mode]:
        if var in derived_variables:
            required.update(derived_variables[var])
    
    # Remove y1_bmifa and y5_bmiz as they will be generated by the code
    required.discard('y1_bmifa')
    required.discard('y5_bmiz')
    
    # Group variables by category
    other_vars = []
    y1_vars = []
    y5_vars = []
    
    for var in required:
        if var.startswith('y1_'):
            y1_vars.append(var)
        elif var.startswith('y5_'):
            y5_vars.append(var)
        else:
            other_vars.append(var)
    
    # Sort each group alphabetically for consistency
    other_vars.sort()
    y1_vars.sort()
    y5_vars.sort()
    
    # Combine the groups in the specified order
    return other_vars + y1_vars + y5_vars

# Functions for prediction
def process_single_sample(data, mode):
    # Convert to DataFrame with a single row
    df = pd.DataFrame([data])
    
    # Calculate derived variables
    df = add_y1y5_bmiz(df, mode)
    
    # Calculate Year 8 BMI
    df = calculate_y8_bmi(df, mode)
    
    return df['y8_bmi'].iloc[0]

def process_batch(file_path, mode):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Calculate derived variables
    df = add_y1y5_bmiz(df, mode)
    
    # Calculate Year 8 BMI
    df = calculate_y8_bmi(df, mode)
    
    return df

def create_template_csv(mode):
    required_vars = get_required_variables(mode)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(required_vars)
    return output.getvalue()

def save_template_csv(mode, filename=None):
    if filename is None:
        filename = f"template_{mode}.csv"
    
    content = create_template_csv(mode)
    with open(filename, "w") as f:
        f.write(content)
    
    print(f"Template CSV saved as {filename}")
    return FileLink(filename)

# Create the interactive form for single sample prediction
def create_single_sample_form(mode):
    required_vars = get_required_variables(mode)
    widgets_dict = {}
    
    # Create a widget for each variable
    for var in required_vars:
        description = variable_descriptions.get(var, var)
        
        if var in variable_values:
            # Create a dropdown for categorical variables
            options = [(value, value.split(' - ')[0].strip()) for value in variable_values[var]]
            widgets_dict[var] = widgets.Dropdown(
                options=options,
                description=description,
                style={'description_width': 'initial'},
                layout=widgets.Layout(width='100%')
            )
        else:
            # Create a float input for continuous variables
            widgets_dict[var] = widgets.FloatText(
                description=description,
                style={'description_width': 'initial'},
                layout=widgets.Layout(width='100%')
            )
    
    # Create a button to submit the form
    submit_button = widgets.Button(
        description='Predict BMI',
        button_style='primary',
        icon='calculator'
    )
    
    # Create an output widget to display the result
    output = widgets.Output()
    
    # Define the submit button callback
    def on_submit_button_clicked(b):
        # Clear the output
        output.clear_output()
        
        # Get the values from the widgets
        data = {}
        for var, widget in widgets_dict.items():
            if isinstance(widget, widgets.Dropdown):
                # Extract the value from the dropdown
                data[var] = widget.value
            else:
                data[var] = widget.value
        
        # Check if all required fields are filled
        missing_vars = [var for var, value in data.items() if value is None]
        
        with output:
            if missing_vars:
                print(f"Error: Missing required variables: {', '.join(missing_vars)}")
                return
            
            try:
                # Process the data
                result = process_single_sample(data, mode)
                
                # Display the result
                display(HTML(f"<h3>Prediction Result</h3><p>Predicted Year 8 BMI: <strong>{result:.2f}</strong></p>"))
            except Exception as e:
                print(f"Error: {str(e)}")
    
    # Attach the callback to the button
    submit_button.on_click(on_submit_button_clicked)
    
    # Group the widgets by category
    general_widgets = [widgets_dict[var] for var in required_vars if not var.startswith('y1_') and not var.startswith('y5_')]
    y1_widgets = [widgets_dict[var] for var in required_vars if var.startswith('y1_')]
    y5_widgets = [widgets_dict[var] for var in required_vars if var.startswith('y5_')]
    
    # Create accordion sections for each category
    accordion = widgets.Accordion()
    accordion.children = [
        widgets.VBox(general_widgets),
        widgets.VBox(y1_widgets),
        widgets.VBox(y5_widgets)
    ]
    accordion.set_title(0, 'General Information')
    accordion.set_title(1, 'Year 1 Measurements')
    accordion.set_title(2, 'Year 5 Measurements')
    
    # Return the form
    return widgets.VBox([accordion, submit_button, output])

# Create the interactive form for batch processing
def create_batch_processing_form(mode):
    # Create a file upload widget
    file_upload = widgets.FileUpload(
        accept='.csv',
        multiple=False,
        description='Upload CSV:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='100%')
    )
    
    # Create a button to download the template
    template_button = widgets.Button(
        description='Download Template',
        button_style='info',
        icon='download'
    )
    
    # Create a button to process the batch
    process_button = widgets.Button(
        description='Process Batch',
        button_style='primary',
        icon='cogs',
        disabled=True
    )
    
    # Create an output widget to display the result
    output = widgets.Output()
    
    # Define the template button callback
    def on_template_button_clicked(b):
        # Clear the output
        output.clear_output()
        
        with output:
            # Create and save the template
            link = save_template_csv(mode)
            display(HTML("<p>Template CSV file created. Click the link below to download:</p>"))
            display(link)
    
    # Define the file upload callback
    def on_file_upload_change(change):
        if file_upload.value:
            process_button.disabled = False
        else:
            process_button.disabled = True
    
    # Define the process button callback
    def on_process_button_clicked(b):
        # Clear the output
        output.clear_output()
        
        if not file_upload.value:
            with output:
                print("Error: No file uploaded.")
            return
        
        # Get the uploaded file
        uploaded_file = next(iter(file_upload.value.values()))
        file_name = next(iter(file_upload.value.keys()))
        
        with output:
            try:
                # Save the uploaded file temporarily
                temp_file = f"temp_{file_name}"
                with open(temp_file, "wb") as f:
                    f.write(uploaded_file["content"])
                
                # Process the batch
                result_df = process_batch(temp_file, mode)
                
                # Save the result
                result_file = f"result_{file_name}"
                result_df.to_csv(result_file, index=False)
                
                # Display the result
                display(HTML(f"<h3>Batch Processing Complete</h3><p>Processed {len(result_df)} samples.</p>"))
                display(HTML("<p>Here's a preview of the results:</p>"))
                display(result_df.head())
                display(HTML("<p>Click the link below to download the complete results:</p>"))
                display(FileLink(result_file))
                
                # Clean up the temporary file
                os.remove(temp_file)
            except Exception as e:
                print(f"Error: {str(e)}")
    
    # Attach the callbacks
    template_button.on_click(on_template_button_clicked)
    file_upload.observe(on_file_upload_change, names='value')
    process_button.on_click(on_process_button_clicked)
    
    # Return the form
    return widgets.VBox([
        widgets.HBox([template_button]),
        widgets.HTML("<br><p>Upload a CSV file with the required variables:</p>"),
        file_upload,
        process_button,
        output
    ])

# Create the mode selection widget
def create_mode_selection():
    # Create a radio button widget for mode selection
    mode_selection = widgets.RadioButtons(
        options=[('Simple Mode (10 variables)', 'simple'), ('Comprehensive Mode (20 variables)', 'comprehensive')],
        description='Select Mode:',
        style={'description_width': 'initial'}
    )
    
    # Create a tab widget for the prediction methods
    tabs = widgets.Tab()
    
    # Create an output widget to display the forms
    output = widgets.Output()
    
    # Define the mode selection callback
    def on_mode_selection_change(change):
        # Clear the output
        output.clear_output()
        
        with output:
            # Create the forms for the selected mode
            single_form = create_single_sample_form(mode_selection.value)
            batch_form = create_batch_processing_form(mode_selection.value)
            
            # Update the tabs
            tabs.children = [single_form, batch_form]
    
    # Set the tab titles
    tabs.set_title(0, 'Single Sample')
    tabs.set_title(1, 'Batch Processing')
    
    # Attach the callback
    mode_selection.observe(on_mode_selection_change, names='value')
    
    # Initialize the forms
    on_mode_selection_change({'new': mode_selection.value})
    
    # Return the mode selection and tabs
    return widgets.VBox([mode_selection, tabs])

# Print a message to indicate the setup is complete
print("✅ Setup complete! You can now use the BMI prediction tool below.")

#%% [markdown]
# ## BMI Prediction Tool
#
# Now that everything is set up, you can use the interactive tool below to predict Year 8 BMI.
#
# ### Prediction Modes
#
# * **Simple Mode**: Uses 10 key variables for prediction. This mode is quicker and requires less data.
# * **Comprehensive Mode**: Uses 20 variables for a more detailed prediction. This mode may provide more accurate results but requires more data.
#
# ### Prediction Methods
#
# * **Single Sample**: Use this tab when you want to predict BMI for a single child. You'll enter all the required information directly in the form.
# * **Batch Processing**: Use this tab when you want to predict BMI for multiple children at once. You'll upload a CSV file with the required information for each child.
#
# ### Instructions for Single Sample Prediction
#
# 1. Select either "Simple Mode" or "Comprehensive Mode"
# 2. Make sure the "Single Sample" tab is selected
# 3. Click on each section (General Information, Year 1 Measurements, Year 5 Measurements) to expand it
# 4. Fill in all the required fields
# 5. Click the "Predict BMI" button to see the results
#
# ### Instructions for Batch Processing
#
# 1. Select either "Simple Mode" or "Comprehensive Mode"
# 2. Click on the "Batch Processing" tab
# 3. Click the "Download Template" button to get a CSV template
# 4. Open the template in a spreadsheet program (like Excel) and fill in the data for multiple children
# 5. Save the file as a CSV
# 6. Click the "Upload CSV" button and select your filled-in CSV file
# 7. Click the "Process Batch" button to see and download the results

#%%
# Create and display the interactive BMI prediction tool
mode_selection = create_mode_selection()

# Display the tool
display(HTML("<h3>Year 8 BMI Prediction Calculator</h3>"))
display(HTML("<p>Select your preferred mode and enter the required information below:</p>"))
display(mode_selection)

#%% [markdown]
# ## Understanding the Variables
#
# Here's a brief explanation of the key variables used in the prediction models:
#
# ### General Information
# - **Mother's Occupation Code**: The occupation category of the mother
# - **Household Income**: The income level of the household
# - **Mother's Age at Birth**: The age of the mother when the child was born (in years)
# - **Mother's Height**: The height of the mother (in cm)
# - **Mode of Delivery**: How the child was delivered (e.g., vaginal, cesarean)
# - **Father's Height**: The height of the father (in cm)
# - **Solid Food Introduction**: Age when solid food was introduced (in months)
# - **Birth Weight**: The weight of the child at birth (in grams)
# - **Gestational Age**: The duration of pregnancy (in weeks)
# - **Pre-pregnancy Cigarettes**: Number of cigarettes smoked before pregnancy
# - **Pregnancy Weight Gain**: Weight gained during pregnancy (in kg)
#
# ### Year 1 Measurements
# - **Age in Months**: The child's age in months at the time of measurement
# - **Weight**: The child's weight (in kg)
# - **Height**: The child's height (in cm)
# - **Sex**: The child's biological sex (1 for male, 2 for female)
# - **Triceps Skinfold**: Thickness of the triceps skinfold (in mm)
#
# ### Year 5 Measurements
# - **Age in Months**: The child's age in months at the time of measurement
# - **Weight**: The child's weight (in kg)
# - **Height**: The child's height (in cm)
# - **Sex**: The child's biological sex (1 for male, 2 for female)
# - **Triceps Skinfold**: Thickness of the triceps skinfold (in mm)
# - **Subscapular Skinfold**: Thickness of the subscapular skinfold (in mm)
# - **Biceps Skinfold**: Thickness of the biceps skinfold (in mm)
# - **Suprailiac Skinfold**: Thickness of the suprailiac skinfold (in mm)
# - **Thigh Skinfold**: Thickness of the thigh skinfold (in mm)
# - **Calf Skinfold**: Thickness of the calf skinfold (in mm)
#
# ## Need Help?
#
# If you encounter any issues or have questions about using this tool, please refer to the documentation or contact the support team.