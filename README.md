# UNICEF-P3-202408
UNICEF assessment for P3 position in Florence - August 2024  

Both parts of the assessment are stored in the same project to make it faster for the person that will grade the test to clone the repository and run the software, I would use two separate repositories otherwise.  


## Installation and running instructions
### Installation steps
1. Download the project from Git
2. Create a Python Virtual Environment: **python -m venv .venv**
3. Activate the virtual environment: **.venv\scripts\activate**
3. Install the required packages: **pip install -r requirements.txt**

## Task 1: Population-weighted coverage of health services
### Running the code
Execute the following command: **python main_mnch.py**

### How does it work?
Running the main_mnch.py file starts the data extraction, data cleaning, merginig and analysis process. The results are shown in a windows that opens automatically.
The results shown in the window are the same contents that can be found in the "Results" section of this README.md file. The application is connected to the readme and pulls the text automatically to avoid discrepancies.

### Results
<!--_Task1_result_start-->
Countries have been divided into two groups: "on track" to meet their under-5 mortality rate reduction targets and "off track". 

The analysis indicates that antenatal care visits have a relatively minor impact on reducing the under-5 mortality rate, with on-track countries showing a 56.5% coverage of antenatal care compared to 54.4% in off-track countries. However, a more significant impact is observed in the coverage of skilled birth attendance. On-track countries demonstrate an 85.7% coverage of skilled birth attendance, while off-track countries have only 63.8% coverage.  

This suggests that increasing the coverage of skilled birth attendance may be a more effective intervention for reducing the under-5 mortality rate.  
While antenatal care visits are important, their impact might be less pronounced in comparison to the presence of skilled birth attendants during delivery, which directly influences birth outcomes. Therefore, to make substantial progress in reducing under-5 mortality, efforts should focus on enhancing the availability and accessibility of skilled birth attendance. 

Antenatal care, even if having less impact on the targets may still be important for other health outcomes not related to the analysis but still important.
Other factors could contribute to the differences and further investigation is required.
<!--_Task1_result_end-->

## Task 2: Data Perspective
### Running the code
Execute the following command: **python main_edu.py**
Or open the **Edu.html** to see the Data Perspective

### How does it work?
Running the main_edu.py file extracts the data and performs the calculations, it outputs the results in a .js file that will be used by the Interface to show the analysis results. Ideally the results should be pushed to a server and the data pulled by the Web Application, in this case everything can be run locally.
The Web Application is very basic and can be improved introducing frameworks like React.js.



### Results