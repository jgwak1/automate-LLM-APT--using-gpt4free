''' Might need to worry about the "max_token" ? '''




from g4f.client import Client
from g4f.Provider import OpenaiChat

import os
import json
import time


# from prompt_templates_NO_file_upload.subtask_1 import get__subtask_1_prompts_list
def get__criteria_2_prompts_list( tagging_summary : dict , behavior_description : dict ):

    prompt_1 = (
         f"## Task"
         f"\nEvaluate the 'behavior alignment' between the provided 'Behavior Description' and the 'Relevant Excerpt'."
         f"\n\n"
         f"**Behavior Description**:"
         f"\n{ behavior_description['Behavior Description'] }"
         f"\n\n"
         f"**Relevant Excerpt**:"
         f"\n{ tagging_summary['Relevant Excerpt'] }"
         f"\n\n"
         f"### Instruction"
         f"\n\n"
         f"Rate the behavior alignment between the 'Behavior Description' and the 'Relevant Excerpt'."
         f"\n\n"
         f"Use the criteria provided in the rubric to assign the rating, and offer a clear rationale for the rating."
         f"\n\n"
         f"### Rubric"
         f"\n\n"
         f"**Behavior Alignment**"
         f"\n\n"
         f"5 (Perfect Behavior Alignment): The 'behavior description' and the 'relevant excerpt' demonstrate a precise and exact alignment in behavior. The 'relevant excerpt' directly and accurately addresses the core behavior outlined in the 'behavior description' with no ambiguity or gaps."
         f"\n\n"
         f"4 (Strong Behavior Alignment): The 'behavior description' and the 'relevant excerpt' demonstrate a substantial alignment in behavior. The 'relevant excerpt' effectively addresses the core behavior outlined in the 'behavior description', accommodating minor variations that do not significantly affect relevance or clarity."
         f"\n\n"
         f"3 (Satisfactory Behavior Alignment): The 'behavior description' and the 'relevant excerpt' demonstrate a sufficient alignment in behavior, though some differences reduce the overall alignment. The 'relevant excerpt' adequately addresses the core behavior outlined in the 'behavior description', though some aspects are unclear, missing, or loosely connected."
         f"\n\n"
         f"2 (Weak Behavior Alignment): The 'behavior description' and the 'relevant excerpt' demonstrate limited alignment in behavior, with significant differences that weaken the connection. The 'relevant excerpt' only partially addresses the core behavior outlined in the 'behavior description', offering minimal relevance or clarity."
         f"\n\n"
         f"1 (No Behavior Alignment): The 'behavior description' and the 'relevant excerpt' demonstrate no alignment in behavior. The 'relevant excerpt' fails to address or relate to the core behavior outlined in the 'behavior description' in any meaningful way."
         f"\n\n"
         f"---"
         f"\n\n"
         f"### Ensure that the output follows this structure:"
         f"\n\n"
         f"- **Alignment Rating (Behavior):**"
         f"\n  (Provide the behavior alignment rating along with a very concise rationale focused exclusively on alignment of the behavior.)"
         f"\n\n"
         f"- **Details: Behavior Description, Relevant Excerpt, and Their Connection**"
         f"\n\n"
         f"  - **Original Behavior Description**:"
         f"\n    (Provide the original behavior description.)"
         f"\n\n"
         f"  - **Original Relevant Excerpt**:"
         f"\n    (Provide the original relevant excerpt.)"
         f"\n\n"
         f"  - **Behavior Connection in Behavior Description**:"
         f"\n    (Identify the 'verbatim' segment of the Behavior Description that connects semantically to the Relevant Excerpt.)"
         f"\n\n"
         f"  - **Behavior Connection in Relevant Excerpt**:"
         f"\n    (Identify the 'verbatim' segment of the Relevant Excerpt that connects semantically to the Behavior Description.)"
      )

    return [ prompt_1 ]



def g4f_generate( prompt_list : list ):


    # client = Client(provider=OpenaiChat)   
    client = Client()  


    message_history = [] # conversation history for 'Command line Chat Program' - alike interaction
    prompt_and_response_dict_list = []

    for i, prompt in enumerate( prompt_list ) :
        print(f"prompt-{i+1} start")
        start_time = time.time()
        
        message_history.append( {"role": "user",  "content": prompt} )

        try:
            response = client.chat.completions.create(
                # Add any other necessary parameters
                model= 'gpt-4o',
                
                messages= message_history,  # Pass the message history (conversation history) to every prompt for a 'command-line chat program' like interaction

            ).choices[0].message.content.strip()

            # Update the conversation history with GPT's response
            message_history.append({"role": "assistant", "content": response})

        except Exception as error_msg:
            print(f"Exception: {error_msg}", flush=True)
            response = f"Could not get response, DUE TO Exception: '{error_msg}'"

        elapsed_time = time.time() - start_time
        print(f"prompt-{i+1} done -- took {elapsed_time} seconds")

        prompt_and_response_dict_list.append( {f"prompt_{i+1}": prompt, "response": response })


    return prompt_and_response_dict_list




if __name__ == "__main__":

   sample_tagging_summary_dpath = "/home/jgwak1/gpt4free_JY/tagging_explanations/externally_dependent_on_scripts/apt29/collection--T1056.001  Input Capture  Keylogging--windows"

   sample_tagging_summary_fpath  = os.path.join( sample_tagging_summary_dpath , "tagging_summary.json" )
   sample_behavior_description_fpath  = os.path.join( sample_tagging_summary_dpath , "behavior_description.json" )
   sample_cited_source_content_fpath  = os.path.join( sample_tagging_summary_dpath , "cited_source_content.json" )

   sample_tagging_summary = json.load( fp = open( sample_tagging_summary_fpath, "r" ) )
   sample_behavior_description = json.load( fp = open( sample_behavior_description_fpath, "r" ) )
   sample_cited_source_content = json.load( fp = open( sample_cited_source_content_fpath, "r" ) )

   sample_criteria_2_prompts_list = get__criteria_2_prompts_list( sample_tagging_summary , sample_behavior_description )

   sample__prompt_and_response_dict_list = g4f_generate( sample_criteria_2_prompts_list )

   sample__prompt_and_response_dict_list

   # --------------------
   outputs_dir_path = "/home/jgwak1/gpt4free_JY/crtieria_2_outputs"

   output_fpath = os.path.join( outputs_dir_path , f"{sample_tagging_summary_dpath.split('/')[-2]}__{sample_tagging_summary_dpath.split('/')[-1]}.json")

   with open( output_fpath , "w") as json_fpath:
        json.dump( sample__prompt_and_response_dict_list , json_fpath, ensure_ascii=False, indent=4)

