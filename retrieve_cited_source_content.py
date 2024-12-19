
import pandas as pd
import json
import os

if __name__ == "__main__":



   mitre_attack_technique_dataset_fpath = "/home/jgwak1/gpt4free_JY/enterprise-attack-v16.0-techniques.xlsx"
   mitre_attack_technique_dataset = pd.read_excel(mitre_attack_technique_dataset_fpath, engine='openpyxl')
   mitre_attack_technique_dataset

   mitre_attack_techniqueIdName_descriptions_map = {
      f"{row['ID']} : {row['name']}": f"{row['description']}"
      for _, row in mitre_attack_technique_dataset.iterrows()
   }


   with open( file = os.path.join( os.getcwd() , "mitre_attack_techniqueIdName_descriptions_map.json") ,mode= "w" ) as fp:
      json.dump( mitre_attack_techniqueIdName_descriptions_map , fp )


   mitre_attack_technique_dataset