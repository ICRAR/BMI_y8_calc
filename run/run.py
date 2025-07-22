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

import pandas as pd
from bmizscore.zscore import get_bmiz_singlevalue as get_y5_bmiz
from pygrowup import Observation as get_y1_bmifa
year = 8
params = {
    "simple": {
        'n_var': 10,
        'width': [10,10,1],
        'grid': 5,
        'step': 100,
        'opt': 'LBFGS',
        'lamb': 0.01,
        'lamb_l1': 5,
        'lamb_ent': 2,
        'variables': ['occupcode_m_0',
                      'hhincome_0',
                      'y5_a5',
                      'y5_a6',
                      'y5_a7',
                      'y5_a8',
                      'y5_a9',
                      'y5_a10',
                      'y5_bmiz',
                      'preg_gain'
                      ]
    },
    "comprehensive":{
        'n_var': 20,
        'width': [20,10,1],
        'grid': 5,
        'step': 100,
        'opt': 'LBFGS',
        'lamb': 0.01,
        'lamb_l1': 5,
        'lamb_ent': 2,
        'variables': ['occupcode_m_0',
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
                      'preg_gain']
    }
}

mode = 'simple'
# train the model first

def add_y1y5_bmiz(data, mode):
    # Check for required columns for y5_bmiz calculation
    required_y5_cols = ['y5_agemos', 'y5_a2', 'y5_a1', 'sex']
    missing_y5_cols = [col for col in required_y5_cols if col not in data.columns]
    if missing_y5_cols:
        raise ValueError(f"Missing required columns for y5_bmiz calculation: {', '.join(missing_y5_cols)}")
    
    try:
        y5_bmiz = []
        for ix, row in data.iterrows():
            try:
                y5_agemos = row['y5_agemos']
                y5_height = row['y5_a2']
                y5_weight = row['y5_a1']
                sex = row['sex']
                
                # Check for null values
                if pd.isna(y5_agemos) or pd.isna(y5_height) or pd.isna(y5_weight) or pd.isna(sex):
                    raise ValueError(f"Null values found in row {ix} for y5_bmiz calculation")
                
                bmiz = get_y5_bmiz(y5_agemos, sex, y5_height, y5_weight)
                y5_bmiz.append(bmiz)
            except Exception as e:
                raise ValueError(f"Error calculating y5_bmiz for row {ix}: {str(e)}")
        
        data['y5_bmiz'] = y5_bmiz

        if mode == 'comprehensive' or mode == 'simple':
            # Check for required columns for y1_bmifa calculation
            required_y1_cols = ['y1_agemos', 'y1_a2', 'y1_a1', 'sex']
            missing_y1_cols = [col for col in required_y1_cols if col not in data.columns]
            if missing_y1_cols:
                raise ValueError(f"Missing required columns for y1_bmifa calculation: {', '.join(missing_y1_cols)}")
            
            try:
                y1_bmifa = []
                for ix, row in data.iterrows():
                    try:
                        y1_agemos = row['y1_agemos']
                        y1_height = row['y1_a2']
                        y1_weight = row['y1_a1']
                        sex = row['sex']
                        sex_obs = get_y1_bmifa.MALE if sex==1 else get_y1_bmifa.FEMALE
                        zbirthy1 = get_y1_bmifa(sex=sex_obs, age_in_months=y1_agemos
                                                )

                        # Check for null values
                        if pd.isna(y1_agemos) or pd.isna(y1_height) or pd.isna(y1_weight) or pd.isna(sex):
                            raise ValueError(f"Null values found in row {ix} for y1_bmifa calculation")
                        
                        sex_str = 'M' if sex == 1 else 'F'
                        
                        # Check for division by zero
                        if y1_height == 0:
                            raise ValueError(f"Height cannot be zero in row {ix}")
                        
                        y1_bmifa_one = zbirthy1.bmi_for_age(y1_weight / (y1_height / 100) ** 2)
                        y1_bmifa.append(y1_bmifa_one)
                    except Exception as e:
                        raise ValueError(f"Error calculating y1_bmifa for row {ix}: {str(e)}")
                
                data['y1_bmifa'] = y1_bmifa
            except Exception as e:
                raise ValueError(f"Error in y1_bmifa calculation: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error in add_y1y5_bmiz: {str(e)}")
    
    return data


def calculate_y8_bmi(data, mode):
    """
    Calculate y8 BMI using the formula saved in the formula file.

    Parameters:
    data (pandas.DataFrame): The input data containing the required variables
    mode (str): The mode to use ('simple' or 'comprehensive')

    Returns:
    pandas.DataFrame: The input data with y8_bmi column added
    
    Raises:
    ValueError: If there are issues with the formula file or data
    """
    try:
        # Check if mode is valid
        if mode not in ['simple', 'comprehensive']:
            raise ValueError(f"Invalid mode: {mode}. Must be 'simple' or 'comprehensive'.")
        
        # Read the formula from the appropriate file
        formula_path = f'./calculator/formula_{mode}.txt'
        try:
            with open(formula_path, 'r') as file:
                formula_str = file.read().strip()
                
            if not formula_str:
                raise ValueError(f"Formula file is empty: {formula_path}")
        except FileNotFoundError:
            raise ValueError(f"Formula file not found: {formula_path}")
        except Exception as e:
            raise ValueError(f"Error reading formula file: {str(e)}")

        # Extract the actual formula from the string (remove brackets)
        formula_str = formula_str.strip('[]')
        
        # Check if the formula contains any variables
        if not any(var in formula_str for var in params[mode]['variables']):
            raise ValueError(f"Formula does not contain any valid variables: {formula_str}")

        # Calculate y8 BMI for each row in the data
        y8_bmi = []
        for ix, row in data.iterrows():
            try:
                # Create a dictionary of variable values from the row
                variables = {}
                for col in data.columns:
                    variables[col] = row[col]

                # Check if all variables in the formula are present in the data
                missing_vars = []
                for var in params[mode]['variables']:
                    if var in formula_str and var not in variables:
                        missing_vars.append(var)
                
                if missing_vars:
                    raise ValueError(f"Missing variables in row {ix}: {', '.join(missing_vars)}")

                # Replace variable names in the formula with their values
                formula_eval = formula_str
                for var_name, var_value in variables.items():
                    if var_name in formula_str:
                        # Check for null values
                        if pd.isna(var_value):
                            raise ValueError(f"Null value found for {var_name} in row {ix}")
                        
                        formula_eval = formula_eval.replace(var_name, str(var_value))

                # Evaluate the formula
                try:
                    import math
                    # Define math functions that might be used in the formula
                    sin = math.sin
                    cos = math.cos
                    tan = math.tan
                    tanh = math.tanh
                    atan = math.atan
                    exp = math.exp

                    # Evaluate the formula
                    bmi_value = eval(formula_eval)
                    
                    # Check if the result is valid
                    if pd.isna(bmi_value) or not isinstance(bmi_value, (int, float)):
                        raise ValueError(f"Invalid BMI value calculated: {bmi_value}")
                    
                    y8_bmi.append(bmi_value)
                except Exception as e:
                    raise ValueError(f"Error evaluating formula for row {ix}: {str(e)}\nFormula: {formula_eval}")
            except Exception as e:
                raise ValueError(f"Error processing row {ix}: {str(e)}")

        # Add the calculated y8 BMI to the data
        data['y8_bmi'] = y8_bmi
        return data
    except Exception as e:
        raise ValueError(f"Error in calculate_y8_bmi: {str(e)}")

# test
if __name__ == '__main__':
    dummy = pd.read_csv('./calculator/dummy.csv')
    data = add_y1y5_bmiz(dummy,mode)
    data = calculate_y8_bmi(data, mode)
