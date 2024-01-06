
from decimal import Decimal
import pandas as pd
from openpyxl import load_workbook
import datetime
import re
import openpyxl
from constants import *

#local import 
from requirement_class import *



class Controller:

    def __init__(self):
        self.generated_excel_data = {}

    # utility functions
    def get_parsed_location(self,locations):
        values0 = locations.split('/') if locations else []
        values = [v.strip().lower() for v in values0]
        return values

    def get_parsed_skills(self,skills):
        # Split the string based on '+'
        main_parts = re.split(r'\s*\+\s*', skills) if skills else []
        
        # Remove the word 'Associate' from each part
        main_parts = [part.replace('Associate', '') for part in main_parts]

        # Split each part based on '/' and remove spaces
        parsed_list = [[value.strip().lower() for value in part.split('/')] for part in main_parts]

        return parsed_list


    def delete_empty_sheets(self,excel_file_path):
        workbook=openpyxl.load_workbook(excel_file_path)
        workbook.get_sheet_names()
        sheet_names = workbook.get_sheet_names()
        for name in sheet_names:
            sheet = workbook[name]
            if(sheet.calculate_dimension() =="A1:A1"):
                workbook.remove_sheet(sheet)
        
        workbook.save(excel_file_path)

    def savaDataToExcel(self):
            # Existing Excel file path -> file to store the filtered data

            #creating file
            excel_file_path = output_file_name
            df = pd.DataFrame({})
            df.to_excel(excel_file_path, index=False)
            df = pd.read_excel(excel_file_path)

            # global generated_excel_data
            for tech_familly, empl in self.generated_excel_data.items():
                merged_df = pd.concat(empl,ignore_index=1)
                with pd.ExcelWriter(excel_file_path,mode='a',if_sheet_exists="overlay") as writer:
                    merged_df.to_excel(
                        writer,
                        sheet_name = tech_familly,
                        index = False
                    )
            self.delete_empty_sheets(excel_file_path)
            return excel_file_path
            

    def process_files(self,input_files_tmp):
        # try:
            input_files = input_files_tmp
            j=0
            requirement_skills_col = 0
            requirement_loc_col = 0
            requirement_tech_familly_col = 0

            for i in input_files.requirements_data.columns:
                if(i== requirements_skill_col_name ):
                    requirement_skills_col = j
                if(i== requirements_location_col_name):
                    requirement_loc_col =j
                if(i== requirements_tech_familly_col_name):
                    requirement_tech_familly_col = j
                j = j+1
            
            j=0
            employee_skills_col = 0
            employee_loc_col = 0
            

            for i in input_files.profiles_data.columns:
                if(i==profiles_skiLL_col_name):
                    employee_skills_col = j
                if(i==profiles_location_col_name):
                    employee_loc_col = j
                j = j+1

        
            
            for req in input_files.requirements_data.values:
                try:
                    requirement_location = self.get_parsed_location(req[requirement_loc_col])
                    requirement_skills = self.get_parsed_skills(req[requirement_skills_col])
                    requirement_tech_familly = req[requirement_tech_familly_col]
                except Exception as e:
                    print("Unable to requirement: "+ str(req))
                    continue;

                for emp in input_files.profiles_data.values:
                    try:
                        employee_skills =  emp[employee_skills_col].split(',') if (emp[employee_skills_col] or emp[employee_skills_col]!='') else "NA"
                        employee_skills = [v.strip().lower() for v in employee_skills]

                        employee_location = emp[employee_loc_col].split(',') if (emp[employee_loc_col] or emp[employee_loc_col]!='')else "Global"
                        employee_location = [v.strip().lower() for v in employee_location]
                    except Exception as e:
                        print("Unable to process profile: "+ str(emp))
                 
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
                            if(type(emp[indx])==int):
                                new_row[col]=Decimal(emp[indx])
                            elif(type(emp[indx])==pd._libs.tslibs.timestamps.Timestamp):
                                new_row[col]=str(emp[indx].date())
                            else:
                                new_row[col]=emp[indx]
                                

                            indx = indx + 1
                        df = pd.DataFrame(pd.DataFrame([new_row], columns=input_files.profiles_data.columns.values))
                        # generated_excel_data
                        if requirement_tech_familly in self.generated_excel_data:
                            self.generated_excel_data[requirement_tech_familly].append(df)
                        else:
                            self.generated_excel_data.update({requirement_tech_familly : [df]})

            return self.savaDataToExcel() 
        # except Exception as e:
        #     print(e)
        #     return "-1"
