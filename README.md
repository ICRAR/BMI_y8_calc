# Year 8 BMI Prediction Tool

A web application for predicting Year 8 BMI using different prediction models.

## Usage Options

You have two options to use this application:

### 1. Online Application

Access our online application at: **[https://bmi-y8-calc.onrender.com/](https://bmi-y8-calc.onrender.com/)**

**Note:** The website may delay requests by 50 seconds or more as it is hosted on a free plan. The application will become active after this initial delay.

### 2. Local Deployment

You can download this repository and run the application on your own computer. This option provides:
- No waiting time for predictions
- Complete privacy of your data
- Ability to modify the application if needed

Follow the installation and usage instructions below to set up and run the application locally.

## Overview

This application provides a web interface for predicting Year 8 BMI using two different prediction models:

- **Simple Mode**: Uses 10 variables for prediction
- **Comprehensive Mode**: Uses 20 variables for more accurate prediction

Users can make predictions for a single sample by filling out a form or process multiple samples by uploading a CSV file.

## Features

- Choose between "Simple" and "Comprehensive" prediction modes
- Single sample prediction with form validation
- Batch processing with CSV file upload/download
- Automatic calculation of derived variables (y5_bmiz and y1_bmifa)
- Dropdown menus for categorical variables
- Responsive web interface

## Installation

The following instructions will guide you through setting up the application on your local machine. This is only necessary if you choose the local deployment option.

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Installation Steps

1. Clone the repository:
   ```
   git clone https://github.com/ICRAR/BMI_y8_calc
   cd BMI_y8_calc
   ```

2. Install the required packages in a local environment:
   ```
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

3. Create the necessary directories:
   ```
   mkdir -p static templates
   ```

## Usage

Once you have installed the application and its dependencies, you can run it locally on your machine. The following instructions will guide you through starting and using the application.

### Starting the Application

Run the following command from the project root directory:

```
uvicorn main:app --host=0.0.0.0 --port=${PORT:-8000}
```

The application will be available at http://0.0.0.0:8000 by default.


### Using the Web Interface

1. Select a prediction mode ("Simple" or "Comprehensive")
2. Choose between single sample prediction or batch processing

#### Single Sample Prediction

1. Fill in all the required fields in the form
2. Click the "Predict BMI" button
3. View the predicted Year 8 BMI result

#### Batch Processing

1. Download the template CSV file for your selected mode
2. Fill in the CSV file with your data
3. Upload the completed CSV file
4. Click the "Process Batch" button
5. Download the results CSV file, which includes the predicted Year 8 BMI values

## Variables

### Simple Mode Variables

The "Simple" mode uses the following 10 variables:

- occupcode_m_0: Occupation of mother
- hhincome_0: Household weekly income
- y5_a5: Year 5 Chest circumference (cm)
- y5_a6: Year 5 Mid arm circumference (cm)
- y5_a7: Year 5 Triceps skinfold (cm)
- y5_a8: Year 5 Subscapular skinfold (cm)
- y5_a9: Year 5 Suprailiac skinfold (cm)
- y5_a10: Year 5 Abdominal skinfold (cm)
- y5_bmiz: Year 5 BMI z-score (calculated)
- preg_gain: Pregnancy weight gain (kg)

### Comprehensive Mode Variables

The "Comprehensive" mode uses the following 20 variables:

- occupcode_m_0: Occupation of mother
- agebirth_m_y: The mother's age in years
- height_m: Height of the mother (cm)
- mode_delivery: Mode of delivery
- height_f1: Height of the father (cm)
- hhincome_0: Household weekly income
- solid_food: Age of the child when solid food was introduced, in month
- ga_wt2: Gestational age at time WT2 was recorded (weeks)
- y1_a10: Year 1 Abdominal skinfold (cm)
- y5_a5: Year 5 Chest circumference (cm)
- y5_a6: Year 5 Mid arm circumference (cm)
- y5_a7: Year 5 Triceps skinfold (cm)
- y5_a8: Year 5 Subscapular skinfold (cm)
- y5_a9: Year 5 Suprailiac skinfold (cm)
- y5_a10: Year 5 Abdominal skinfold (cm)
- y5_bmiz: Year 5 BMI z-score (calculated)
- y1_bmifa: Year 1 BMI-for-age (calculated)
- ga_us: Gestational age determined by ultrasound in days
- prepreg_cig: Cigarettes per day before pregnancy, at any time pre-partum
- preg_gain: Pregnancy weight gain (kg)

### Derived Variables

The application automatically calculates the following derived variables:

- y5_bmiz: Calculated using y5_agemos, sex, y5_a2 (height), and y5_a1 (weight)
- y1_bmifa: Calculated using y1_agemos, sex, y1_a2 (height), and y1_a1 (weight)

## License

Copyright (c) 2025. UWA (in the framework of the ICRAR)

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



## Acknowledgements
We gratefully acknowledge all Raine Study participants and their families for their continued participation in the study, as well as the Raine Study team for study co-ordination and data collection. We also thank the NHMRC and the Raine Medical Research Foundation for their support. The core management of the Raine Study is funded by The University of Western Australia, Curtin University, The Kids Research Institute Australia, Women and Infants Research Foundation, Edith Cowan University, Murdoch University, The University of Notre Dame Australia and the Western Australian Future Health Research and Innovation Fund (2023-2024; Grant ID WACSOSP2023-2024). The Pawsey Supercomputing Centre provided computation resources to carry out analyses required with funding from the Australian Government and the Government of Western Australia. The data collection of the Raine Study Gen1- and Gen2-1, 2, 5, 8 year follow-ups was funded by NHMRC Grant and The Raine Medical Research Foundation.

This project uses the following open-source libraries:

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Pandas](https://pandas.pydata.org/)
- [Bootstrap](https://getbootstrap.com/)
- [pygrowup](https://github.com/jbaldivieso/pygrowup2)