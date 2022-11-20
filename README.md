# Balance Metrics Streamlit!

Collection of raw data of a person using a force platform with sensors!

Measure the center of pressure of that person!

This app created for the purpose of research to meausure the balance of a person depending of the forces collected by the platform to display calculations and chats in a clean and friendly dashboard.

It has been used python code and many libraries such as pandas, numpy, streamlit and charts libraries.


# Main Functions:

- Prepare File: First the user is able to view the raw data into chart and edit it depending on their needs!

- Insert New Entry : The user may insert new user in the database..Also if the user exists, there is the posibility to import the fields automtically.

- Center of Pressure : Calculate the ballance results for each entry of the dataframe table.

Streamlit Cloud Url : https://balance.streamlit.app


Prepare File: Cleaning & Preprocessing raw data. After import the txt raw data file, varius functionalities run in the background.

Behind the scene:

Jump attempt execution procedures:
At this point, we should mention that we check various jumps, specifically:


The plux dyno platform is square in shape, it has four sensors, one in each corner. The test is done as follows:

- At first we activate the platform.
- Then we find the weight of the platform and mark it down (for the next step).
- Next we tell the athlete/tester to get on the platform and then we are ready to press start the measurement.
- The athlete then begins the jump test procedure.
- As soon as they complete their effort in a few seconds, we press end of recording the values ​​and we are ready to receive the exported file with the raw data.


File Preparations:
To use this data to our advantage we first need some kind of pre-processing and cleaning.

In this section we will do that. So far all we have are current data type values.
The processing we need at this stage concerns the following actions:
- To convert these values ​​into weight,
- To remove the weight of the platform
- Calculate the total mass
- To display the total mass in a graph, so that we have the option to keep the interval we want as a final file.


-After we insert the file through a form, a new datframe is created.
- We check how many columns our datframe contains and define the names of the columns.

-Calculations are made to convert the raw data into a processed form. Specifically, we want to convert the values ​​of each row into a weight, so according to the plux guide we use the equation and some constants (see table).

- We create a new column in the dataframe, the sum of the total weights by subtracting the weight of the platform.

- We display the graph of the total mass and give the possibility to the user through a slider to get as many interval values ​​as he wishes.

In the front part of the application in the file preparation section, the user sees a form where he enters the file, because he is asked to fill in the weight, and then the mass graph is generated. A slider above that gives him the ability to take all the values ​​or to choose the ones he wants along the x-axis. After completing these steps, it is ready to export the final file to sysvi, which we will use later for further processing.