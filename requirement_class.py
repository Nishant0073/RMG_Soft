import pandas as pd

class Input_files:
    def __init__(self,profiles_file,requirements_file):
        self.profiles_file = profiles_file
        self.requirements_file = requirements_file
        self.profiles_data = pd.read_excel(profiles_file)
        self.requirements_data = pd.read_excel(requirements_file)
        

    

    
        