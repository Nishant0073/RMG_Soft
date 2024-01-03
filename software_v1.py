import tkinter as tk
from tkinter import filedialog
import pandas as pd
from openpyxl import load_workbook
import datetime
import re

# generated_files = []
excel_file_path = ""
generated_excel_data = {}

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


def process_files(employees_file,requirement_file):
    # try:
        # main program
        employees_data = pd.read_excel(employees_file)
        requirement_data = pd.read_excel(requirement_file)


        j=0
        requirement_skills_col = 0
        requirement_loc_col = 0
        requirement_tech_familly_col = 0;

        for i in requirement_data.columns:
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
        

        for i in employees_data.columns:
            if(i=="Skills"):
                employee_skills_col = j
            if(i=="Location"):
                employee_loc_col = j
            j = j+1

        # Existing Excel file path
        global excel_file_path
        excel_file_path = "Matched_data_"+ str(datetime.date.today()) +'.xlsx'
        df = pd.DataFrame({})
        df.to_excel(excel_file_path, index=False)
        df = pd.read_excel(excel_file_path)

        requirement_no = 0
        rows = []

        for req in requirement_data.values:
            requirement_location = get_parsed_location(req[requirement_loc_col])
            requirement_skills = get_parsed_skills(req[requirement_skills_col])
            requirement_tech_familly = req[requirement_tech_familly_col]
            requirement_no = requirement_no+1

             
            sheet_name_ = "Sheet"+ str(requirement_no)
            cnt = 0
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
                    df = pd.DataFrame(pd.DataFrame([new_row], columns=employees_data.columns.values))
                    global generated_excel_data
                    if requirement_tech_familly in generated_excel_data:
                        generated_excel_data[requirement_tech_familly].append(df)
                    else:
                        generated_excel_data.update({requirement_tech_familly : [df]})
                    rows.append(df)
        
            # if(len(rows)!=0): 
            #     merged_df = pd.concat(rows,ignore_index=1)
            #     with pd.ExcelWriter(excel_file_path,mode='a',if_sheet_exists="overlay" ) as writer:
            #             merged_df.to_excel(
            #                 writer,
            #                 sheet_name= sheet_name_,
            #                 index=False
            #             )
            #     rows = []
            # generated_files.append(excel_file_path)
            # df.to_excel(excel_file_path, index=False)
        # global generated_excel_data
        for tech_familly, empl in generated_excel_data.items():
            merged_df = pd.concat(empl,ignore_index=1)
            with pd.ExcelWriter(excel_file_path,mode='a',if_sheet_exists="overlay") as writer:
                merged_df.to_excel(
                    writer,
                    sheet_name = tech_familly,
                    index = False
                )
                     
        # print(generated_excel_data)

        return True
    # except Exception as e:
    #     print(e)
    #     return False

def select_file(entry_widget):
    file_path = filedialog.askopenfilename()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)

def process_and_display():
    employee_file = employee_filepath.get()
    requirement_file = requirement_filepath.get()

    if employee_file and requirement_file:
        new_file_path = process_files(employee_file ,requirement_file)
        if(new_file_path==True):
            if excel_file_path:
            #     generated_files_list = ""
            #     for name in generated_files:
            #         generated_files_list = generated_files_list + '\n' + name
                result_label.config(text=f"New file generated:\n{excel_file_path}"+"\n")
            else:
                result_label.config(text=f"No Match Found!"+"\n")
        else:
            result_label.config(text="Something went wrong!\n")
    else:
        result_label.config(text="Please select both files.")

# Create the main Tkinter window
root = tk.Tk()
root.title("Resource Locator App")

# File 1 selection
file1_label = tk.Label(root, text="Select Profiles File:")
file1_label.grid(row=0, column=0, padx=10, pady=10)

employee_filepath = tk.Entry(root, width=40)
employee_filepath.grid(row=0, column=1, padx=10, pady=10)

file1_button = tk.Button(root, text="Browse", command=lambda: select_file(employee_filepath))
file1_button.grid(row=0, column=2, padx=10, pady=10)

# File 2 selection
file2_label = tk.Label(root, text="Select Open Requirements File:")
file2_label.grid(row=1, column=0, padx=10, pady=10)

requirement_filepath = tk.Entry(root, width=40)
requirement_filepath.grid(row=1, column=1, padx=10, pady=10)

file2_button = tk.Button(root, text="Browse", command=lambda: select_file(requirement_filepath))
file2_button.grid(row=1, column=2, padx=10, pady=10)

# Process button
process_button = tk.Button(root, text="Process Files", command=process_and_display)
process_button.grid(row=2, column=1, pady=20)

# Result label
result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=3)

# Start the Tkinter event loop
root.mainloop()




#  if i in dict:
#             dict[i].append(j);
#         else:
#             dict.update({i:[]})
