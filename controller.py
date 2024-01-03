
import pandas as pd
from openpyxl import load_workbook
import datetime
import re
 

#local import 
from requirement_class import *
from rmg_software import *

# Global Files
excel_file_path = ""
generated_excel_data = {}
input_files = Input_files()


# utility functions
def get_parsed_location(locations):
    values0 = locations.split('/')
    values = [v.strip().lower() for v in values0]
    return values

def get_parsed_skills(skills):
    # Split the string based on '+'
    main_parts = re.split(r'\s*\+\s*', skills)
    
    # Remove the word 'Associate' from each part
    main_parts = [part.replace('Associate', '') for part in main_parts]

    # Split each part based on '/' and remove spaces
    parsed_list = [[value.strip().lower() for value in part.split('/')] for part in main_parts]

    return parsed_list


def savaDataToExcel():
        # Existing Excel file path -> file to store the filtered data
        global excel_file_path
        #creating file
        excel_file_path = "Matched_data_"+ str(datetime.date.today()) +'.xlsx'
        df = pd.DataFrame({})
        df.to_excel(excel_file_path, index=False)
        df = pd.read_excel(excel_file_path)

        # global generated_excel_data
        for tech_familly, empl in generated_excel_data.items():
            merged_df = pd.concat(empl,ignore_index=1)
            with pd.ExcelWriter(excel_file_path,mode='a',if_sheet_exists="overlay") as writer:
                merged_df.to_excel(
                    writer,
                    sheet_name = tech_familly,
                    index = False
                )
        

def process_files():
    try:

        j=0
        requirement_skills_col = 0
        requirement_loc_col = 0
        requirement_tech_familly_col = 0

        for i in input_files.requirements_file.columns:
            if(i=="Main Skill Description"):
                requirement_skills_col = j
            if(i=="Location"):
                requirement_loc_col =j
            if(i=="Tech Family"):
                requirement_tech_familly_col = j
            j = j+1
        
        j=0
        employee_skills_col = 0
        employee_loc_col = 0
        

        for i in input_files.profiles_file.columns:
            if(i=="Skills"):
                employee_skills_col = j
            if(i=="Location"):
                employee_loc_col = j
            j = j+1


        for req in input_files.requirements_data.values:
            requirement_location = get_parsed_location(req[requirement_loc_col])
            requirement_skills = get_parsed_skills(req[requirement_skills_col])
            requirement_tech_familly = req[requirement_tech_familly_col]
             
            for emp in input_files.profiles_data.values:
                employee_skills = emp[employee_skills_col].split(',')
                employee_skills = [v.strip().lower() for v in employee_skills]

                employee_location = emp[employee_loc_col].split(',')
                employee_location = [v.strip().lower() for v in employee_location]

                location_satisfied = 0
                skills_satisfied = []

                for i in employee_location:
                    for j in requirement_location:
                        if(i==j):
                            location_satisfied = 1
                            break
                    if location_satisfied == 1:
                        break
            
                for req_skills in requirement_skills:
                    for skill in req_skills:
                        for eskill in  employee_skills:
                            if(skill==eskill):
                                skills_satisfied.append(skill)
                                break
            
                if(location_satisfied and len(skills_satisfied)==len(requirement_skills)):
                    new_row = {}
                    indx = 0
                    for col in input_files.profiles_data.columns.values:
                        new_row[col]=emp[indx]
                        indx = indx + 1
                    df = pd.DataFrame(pd.DataFrame([new_row], columns=input_files.profiles_data.columns.values))
                    global generated_excel_data
                    if requirement_tech_familly in generated_excel_data:
                        generated_excel_data[requirement_tech_familly].append(df)
                    else:
                        generated_excel_data.update({requirement_tech_familly : [df]})

        savaDataToExcel() 
        # print(generated_excel_data)
        return True
    except Exception as e:
        print(e)
        return False

def select_file(entry_widget):
    file_path = filedialog.askopenfilename()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)

def process_and_display():
    global input_files
    input_files = Input_files(employee_filepath.get(),requirement_filepath.get())
    if input_files.profile_file and input_files.requirement_file:
        new_file_path = process_files()
        if(new_file_path==True):
            if excel_file_path:
                result_label.config(text=f"New file generated:\n{excel_file_path}"+"\n")
            else:
                result_label.config(text=f"No Match Found!"+"\n")
        else:
            result_label.config(text="Something went wrong!\n")
    else:
        result_label.config(text="Please select both files.")
