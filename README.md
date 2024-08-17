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
#### Language and Literacy Development
##### EC6: Can identify or name at least ten letters of the alphabet
<!--_Task2_result_EC6_start-->
The ability shows a fluctuating pattern, the percentage starts at 3.2% at 3 years increasing at 14.7% at 4 years and 11 months. The trend suggests variability in early literacy development, posibily influenced by environmental factors or structured learning activities.  
However, there is an overall upward trend, especially as the children approach 4 years of age, indicating growing familiarity with letters.
<!--_Task2_result_EC6_end-->

##### EC7: Can read at least four simple, popular words
<!--_Task2_result_EC7_start-->
The ability to read at least four simple words also shows an irregular pattern, starting at 4.2% at 3 years and 0 months, and ending at 16.4% by 4 years 11 months.  
This inconsistency may be attributed to the level of practice or instruction each child receives. However, similar to letter identification, there is a gradual improvement, particularly in the latter half of the year.
<!--_Task2_result_EC7_end-->

#### Math Development
##### EC8: Does know the name and recognize the symbol of all numbers from 1 to 10
<!--_Task2_result_EC8_start-->
The ability to recognize and name numbers from 1 to 10 shows a more stable and progressive increase starting at 8.4% and ending at about 30%.  
This steady improvement suggests that numeracy skills are being consistently developed during this period, possibly due to repetitive counting activities or formal education.
<!--_Task2_result_EC8_end-->

### Motor skills
##### EC9: Can pick up a small object with two fingers, like a stick or a rock from the ground
<!--_Task2_result_EC9_start-->
Fine motor skills, as measured by the ability to pick up small objects, show a high level of competency across all ages, with percentages consistently above 85%. The skill progresses from 92.6% at 3 years and 0 months to 98.2% by 3 years and 11 months.  
The consistently high percentages indicate that fine motor skills are well developed in this age group, likely due to frequent opportunities to practice these movements in daily activities.
<!--_Task2_result_EC9_end-->

##### EC10: Is sometimes too sick to play
<!--_Task2_result_EC10_start-->
The percentage of children too sick to play fluctuates significantly, ranging from 30.2% to 46.9%. There is no clear trend over the months, indicating that this could be influenced individual health conditions. The impact seems to be slightly less at 4 years and above.
<!--_Task2_result_EC10_end-->

#### Social and Development
##### EC11: Does follow simple directions on how to do something correctly
<!--_Task2_result_EC11_start-->
The ability to follow simple directions and complete tasks independently shows improvement. For following directions, percentages rise from 80.0% at 3 years and 0 months to 90.5% by 3 years and 11 months.  
This steady improvement suggests that as children age, their ability to understand and execute instructions, as well as their autonomy in completing tasks, strengthens.
<!--_Task2_result_EC11_end-->

##### EC12: When given something to do, is able to do it independently
<!--_Task2_result_EC12_start-->
For task independence, the percentages also show growth, from 62.1% at 3 years and 0 months around 75% by 4 years and 11 months.
As for the previuous analysis the ability and autonomy strengthens.
<!--_Task2_result_EC12_end-->

##### EC13: Does get along well with other children
<!--_Task2_result_EC13_start-->
The data for this indicator shows relatively high and stable percentages of positive responses, fluctuating between 93.1% and 98.9% across the year. This suggests that most children in this age group generally exhibit strong social skills and are able to interact well with other young children. There is a slight variation in the percentages, but no clear trend of improvement or decline. The one missing data point at 3 years and 2 months counld be interpolated as it doesn't seem to change the trend.
<!--_Task2_result_EC13_end-->

##### EC14: Does kick, bite, or hit other children or adults
<!--_Task2_result_EC14_start-->
For this indicator, the data shows more fluctuation. This indicator generally represents undesirable behavior, so lower percentages are preferable. However, the data does not show a clear trend of improvement or worsening behavior. There are some noticeable peaks, indicating variability in the prevalence of aggressive behaviors among children in this age group. Despite the fluctuations, the overall range suggests that a significant portion of children occasionally exhibit such behaviors.
<!--_Task2_result_EC14_end-->

##### EC15: Does get distracted easily
<!--_Task2_result_EC15_start-->
The positive response percentages for this indicator range from 29.5% to 44.0%, indicating a moderate level of distractibility among children aged 3 to 4 years. There is no consistent trend over time; instead, the data oscillates. The overall variability suggests that distractibility is a common, but not overwhelming, characteristic in this age group.
<!--_Task2_result_EC15_end-->
