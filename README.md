
# RMG Software 
A program to filter profiles based on open requirements.

## How to install

-  Install python3 from Microsoft Store.
-  Download the project from:
     - <img src="https://github.com/Nishant0073/RMG_Soft/blob/main/download_project_img.png" width="400" height="350" />
    
-  Extract RMG_Soft-main folder from the RMG_Soft-main.zip file.
-  After extraction, open RMG_Soft-main(extracted) folder in powershell(recommended) or cmd.
-  Run the following command to install required python libraries:
            ``` pip install -r requirements.txt ```
-  After successfull execution of command, run the main program file "rmg_software.py" using following command:
        ``` python .\rmg_software.py ```
- And your Done!  

## How to use this software
- It takes two input files:
     1. Open_Requirement.xlsx -> This file contains list of open requirements
     2. Profiles.xlsx  -> This file contains list of profiles. 
- Select file using browse buttons:
- Then hit process button
     - <img src="https://github.com/Nishant0073/RMG_Soft/blob/main/Software.png" width="400" height="150" />
## How does it works?
- It takes two files input Open_Requirement.xlsx and Profiles.xlsx
- First it iterate over the each row in Open_Requirement.xlsx
    - For each requirement it extract following values:
       1. **Requirement Location** (Should be seprated by forword slash ('/'))
       2. **Requirement Skills** (Should be in follwing format  ** skill1 / skill1_aleternative + skill2 / skill2_alternative **  eg. Java / .Net + AWS / Azure
       3. **Requirement Tech Familly** 
    - All **three fields** must be **not empty otherwise this software will skip that  requirement**
    - Then it iterate over each row in Profiles.xlsx
        - For each profile it extract following values:
            1. **Profile Skill**  (Should be seperated by comma ',')
            2. **Profile Location**  (Should be seperated by comma ',')
         - All **two fields** must be **not empty otherwise this software will skip that  profile**
    - Then it matches profile with requirement and stores result in excel sheet.
    - The profiles are stored in different sheets.Each techfamilly will have diffrent sheet and the a excel file will contains all those sheets.
- The findal result is stored into excel file.The name of file is in following formate: **Matched_data_year-month-day.xlsx** eg. Matched_data_2024-01-08.xlsx

  
