# Project Flow
## Intro
1. Create project template by executing `template.py` file
2. Write the code on setup.py and pyproject.toml file to import local packages
3. Create a virtual env, activate it and install the requirements from requirements.txt
#### Commands(For Windows)
   ```bash
   python -m venv venv
   venv\Scripts\activate
   //add required modules to requirements.txt
   "pip install -r requirements.txt"
   ```
4. Do a "pip list" on terminal to make sure you have local packages installed.

---

## MongoDB Setup
5. Sign up to MongoDB Atlas and create a new project by just providing it a name then next next create.
6. From "Create a cluster" screen, hit "create", Select M0 service keeping other services as default, hit "create deployment"
7. Setup the username and password and then create DB user.
8. Go to "network access" and add ip address - "0.0.0.0/0" so that we can access it from anywhere
9. Go back to project >> "Get Connection String" >> "Drivers" >> {Driver:Python, Version:3.6 or later} 
   >> copy and save the connection string with you(replace password). >> Done.
10. Create folder "notebook" >> do step 11 >>  create file "mongoDB_demo.ipynb" >> select kernal>python kernal>vehicle>>
11. Dataset added to notebook folder
12. Push your data to mongoDB database from your python notebook.
13. Go to mongoDB Atlas >> Database >> browse collection >> see your data in key value format

---

## logging, exception and notebooks
14. Write the logger file and test it on demo.py
15. Write the exception file and test it on demo.py
16. EDA and Feature Engg notebook added.

---

## Data Ingestion
17. Before we work on "Data Ingestion" component >> Declare variables within constants.__init__.py file >> 
    add code to configuration.mongo_db_connections.py file and define the func for mondodb connection >> 
    Inside "data_access" folder, add code to vehicle_data.py that will use mongo_db_connections.py
    to connect with DB, fetch data in key-val format and transform that to df >>
    add code to entity.config_entity.py file for DataIngestionConfig class >>
    add code to entity.artifact_entity.py file for DataIngestionArtifact class >>
    add code to components.data_ingestion.py file >> add code to training pipeline >> 
    run demo.py (set mongodb connection url first, see next step)
18. To setup the connection url on mac(also work for windows):
	- create a `.env` file in root directory
	- set `MONGO_USER`,`MONGO_PASSWORD`,`MONGO_URI` where
		- `MONGO_USER` : Username
		- `MONGO_PASSWORD` : Database password
		- `MONGO_URI` : Connection string from mongoDB
		
---

## Data Validation, Data Transformation & Model Trainer
19. Complete the work on utils.main_utils.py and config.schema.yaml file (add entire info about dataset for data validation step)
20. Now work on the "Data Validation" component the way we did in step 17 for Data Ingestion. (Workflow mentioned below)
21. Now work on the "Data Transformation" component the way we did in above step. (add estimator.py to entity folder)
22. Now work on the "Model Trainer" component the way we did in above step. (add class to estimator.py in entity folder)

---

## Model Pusher
23. Set necessary parameters in constants
24. Create a google service account and a folder in gdrive
25. Copy the folder code and save as `GOOGLE_FOLDER_ID` in 'src/constants/__init__.py'
26. Use the `GGLEstimator` in `src/entity/estimator.py` to push or retrieve the model from the cloud

## Prediction pipeline and Web interface
27. Create the code structure of "Prediction Pipeline" and setup your app.py
28. Add "static" and "template" dir to the project.

	
	