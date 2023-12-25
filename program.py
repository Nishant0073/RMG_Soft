import pandas as pd
import re


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



# main program
employees_data = pd.read_excel('employee_data.xlsx')
requirement_data = pd.read_excel('requirements_data.xlsx')


j=0
requirement_skills_col = 0
requirement_loc_col = 0

for i in requirement_data.columns:
    if(i=="Main Skill Description"):
        requirement_skills_col = j
    if(i=="Location"):
        requirement_loc_col =j
    j = j+1

j=0

employee_skills_col = 0
employee_loc_col = 0

for i in employees_data.columns:
    if(i=="Skills"):
        employee_skills_col = j
    if(i=="Location"):
        employee_loc_col = j
    j = j+1


for req in requirement_data.values:
    requirement_location = get_parsed_location(req[requirement_loc_col])
    requirement_skills = get_parsed_skills(req[requirement_skills_col])

    # Existing Excel file path
    excel_file_path = req[0].strip() +req[1].strip() +'.xlsx'

    df = pd.DataFrame({})
    df.to_excel(excel_file_path, index=False)

    df = pd.read_excel(excel_file_path)


    for emp in employees_data.values:
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
            for col in employees_data.columns.values:
                new_row[col]=emp[indx]
                indx = indx + 1
            df = pd.concat([df, pd.DataFrame([new_row], columns=employees_data.columns.values)], ignore_index=True)

    df.to_excel(excel_file_path, index=False)