# Year 8 BMI Prediction Tool

A web application for predicting Year 8 BMI using different prediction models.

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

### Prerequisites

- Python 3.7+
- pip

### Dependencies

The application requires the following Python packages:

- fastapi
- uvicorn
- pandas
- jinja2
- python-multipart
- pygrowup (from GitHub)

### Installation Steps

1. Clone the repository:
   ```
   git clone <repository-url>
   cd BMI_y8_calc
   ```

2. Install the required packages:
   ```
   pip install fastapi uvicorn pandas jinja2 python-multipart
   pip install git+https://github.com/jbaldivieso/pygrowup2.git
   ```

   Note: Do not install pygrowup directly from PyPI. Use the GitHub repository as specified.

3. Create the necessary directories:
   ```
   mkdir -p static templates
   ```

## Usage

### Starting the Application

Run the following command from the project root directory:

```
uvicorn main:app --reload
```

The application will be available at http://0.0.0.0:8000 by default.

#### Configuring the Port

If port 8000 is already in use, you can:

1. Run the application directly using Python, which will use port 8080 by default:
   ```
   python main.py
   ```

2. Set a custom port using the PORT environment variable:
   ```
   # On Linux/macOS
   PORT=8888 python main.py
   
   # On Windows (Command Prompt)
   set PORT=8888
   python main.py
   
   # On Windows (PowerShell)
   $env:PORT=8888
   python main.py
   ```

3. Specify a port directly with uvicorn:
   ```
   uvicorn main:app --reload --port 8888
   ```

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

## Deployment to Render

This application can be easily deployed to [Render](https://render.com/), a cloud platform that offers free hosting for web services.

### Prerequisites for Render Deployment

- A GitHub account with this repository pushed to it
- A Render account (you can sign up for free at [render.com](https://render.com/))

### Configuration Files

The repository includes two important files for Render deployment:

1. **Procfile**: Tells Render how to start the application
2. **render.yaml**: Defines the service configuration for Render's Blueprint feature

### Deployment Steps

1. **Push your code to GitHub**:
   Make sure your code, including the Procfile and render.yaml, is pushed to a GitHub repository.

2. **Connect to Render**:
   - Log in to your Render account
   - Click "New" and select "Blueprint" from the dropdown menu
   - Connect your GitHub account if you haven't already
   - Select the repository containing this application

3. **Deploy the Blueprint**:
   - Render will automatically detect the render.yaml file
   - Review the settings and click "Apply"
   - Render will create and deploy the service as defined in the render.yaml file

4. **Manual Deployment (Alternative)**:
   If you prefer not to use Blueprints:
   - Click "New" and select "Web Service"
   - Connect your GitHub repository
   - Select "Python" as the environment
   - Set the build command to: `pip install -r requirements.txt`
   - Set the start command to: `uvicorn main:app --host=0.0.0.0 --port=$PORT`
   - Click "Create Web Service"

5. **Access Your Application**:
   - Once deployment is complete, Render will provide a URL for your application
   - The application will be available at this URL
   - You can also set up a custom domain in the Render dashboard

### Environment Variables

No additional environment variables are required for basic functionality. Render automatically provides the `PORT` environment variable, which the application uses.

### Troubleshooting

- **Build Failures**: Check the build logs in the Render dashboard. Common issues include missing dependencies or Python version incompatibilities.
- **Runtime Errors**: Check the logs in the Render dashboard for any runtime errors.
- **Slow First Request**: Render may put free services to sleep after periods of inactivity. The first request after inactivity may be slow as the service wakes up.

## API Endpoints

The application provides the following API endpoints:

- `GET /`: Main web interface
- `GET /api/variables/{mode}`: Get the variables required for a specific mode
- `GET /api/template/{mode}`: Download a template CSV file for a specific mode
- `POST /api/predict/single`: Predict BMI for a single sample
- `POST /api/predict/batch`: Process a batch of samples from a CSV file

### API Documentation

FastAPI automatically generates interactive API documentation. You can access it at:

- Swagger UI: http://localhost:{port}/docs (replace {port} with the port you're using)
- ReDoc: http://localhost:{port}/redoc (replace {port} with the port you're using)

For example, if you're running on the default port with uvicorn:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Or if you're running with Python directly (default port 8080):
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

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