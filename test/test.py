import pandas as pd
from bmizscore.zscore import get_bmiz_singlevalue as get_y5_bmiz
from pygrowup import Calculator as get_y1_bmifa
year = 8
params = {
    "good": {
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
    "better":{
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

mode = 'good'
# train the model first

def add_y1y5_bmiz(data,mode):
    y5_bmiz = []
    for ix, row in data.iterrows():
        y5_agemos = row['y5_agemos']
        y5_height = row['y5_a2']
        y5_weight = row['y5_a1']
        sex = row['sex']
        y5_bmiz.append(get_y5_bmiz(y5_agemos,sex,y5_height,y5_weight))
    data['y5_bmiz'] = y5_bmiz

    if mode == 'better':
        zbirthy1 = get_y1_bmifa(
            adjust_height_data=False,
            adjust_weight_scores=False,
            include_cdc=False,
            logger_name="pygrowup",
            log_level="INFO",
        )
        y1_bmifa = []
        for ix, row in data.iterrows():
            y1_agemos = row['y1_agemos']
            y1_height = row['y1_a2']
            y1_weight = row['y1_a1']
            sex = row['sex']
            sex_str = 'M' if sex == 1 else 'F'
            y1_bmifa_one = zbirthy1.bmifa(
                measurement=y1_weight / (y1_height / 100) ** 2,
                age_in_months=y1_agemos,
                sex=sex_str,
                height=y1_height,
            )
            y1_bmifa.append(y1_bmifa_one)
        data['y1_bmifa'] = y1_bmifa
    return data


def calculate_y8_bmi(data, mode):
    """
    Calculate y8 BMI using the formula saved in the formula file.

    Parameters:
    data (pandas.DataFrame): The input data containing the required variables
    mode (str): The mode to use ('good' or 'better')

    Returns:
    pandas.DataFrame: The input data with y8_bmi column added
    """
    # Read the formula from the appropriate file
    formula_path = f'../calculator/formula_{mode}.txt'
    with open(formula_path, 'r') as file:
        formula_str = file.read().strip()

    # Extract the actual formula from the string (remove brackets)
    formula_str = formula_str.strip('[]')

    # Calculate y8 BMI for each row in the data
    y8_bmi = []
    for _, row in data.iterrows():
        # Create a dictionary of variable values from the row
        variables = {}
        for col in data.columns:
            variables[col] = row[col]

        # Replace variable names in the formula with their values
        formula_eval = formula_str
        for var_name, var_value in variables.items():
            if var_name in formula_str:
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
            y8_bmi.append(bmi_value)
        except Exception as e:
            print(f"Error evaluating formula: {e}")
            y8_bmi.append(None)

    # Add the calculated y8 BMI to the data
    data['y8_bmi'] = y8_bmi
    return data

# test
dummy = pd.read_csv('../calculator/dummy.csv')
data = add_y1y5_bmiz(dummy,mode)
data = calculate_y8_bmi(data, mode)
