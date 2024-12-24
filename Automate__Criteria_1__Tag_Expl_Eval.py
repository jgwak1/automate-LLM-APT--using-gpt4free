''' Might need to worry about the "max_token" ? '''


from g4f.client import Client
from g4f.Provider import OpenaiChat

import os
import json
import time






# from prompt_templates_NO_file_upload.subtask_1 import get__subtask_1_prompts_list
def get__criteria_1_prompts_list( tagging_summary : dict , cited_source_content : dict ):

    # Modified the Criteria-1 prompt:
    # 
    #    > For the Criteria-1 prompt used with the ChatGPT browser, 
    #    > the ATT&CK technique domain-knowledge file was uploaded, and ChatGPT was tasked with locating the cited source content.
    #
    #    > Here, the "Cited Source Content" is explicitly provided (as gpt4free doesn't support file-uploading),
    #    > so some parts of the prompt have been adjusted accordingly.

    prompt_1 = (
         f"**Task**: Verify if the 'Relevant Excerpt' in the tagging summary accurately reflects the content of the 'Cited Source' specified in the tagging summary by cross-referencing it with the domain knowledge-base. The goal is to detect any LLM-generated inaccuracies."
         f"\n\n"
         f"**Relevant Excerpt**: "  # Changed 
         f"{tagging_summary['Relevant Excerpt']}"
         f"\n\n"
 
         f"**Cited Source Content**: "  # Changed 
         f"{ cited_source_content['Cited Source Content']}"
         f"\n\n"

         f"**Instructions**:"
         # f"\n1. Access the domain knowledge-base as outlined below. If any access attempts fail, please report the specific issue encountered."
         # f"\n   - First verify if the 'enterprise-attack-v16.0-techniques.xlsx' file is uploaded. If it is uploaded, open and review the content of the 'techniques' sheet."
         # f"\n\n"
         # f"2. Locate and Cross-Reference the 'Cited Source':"
         f"1. Cross-Reference the 'Relevant Excerpt' with 'Cited Source Content':"
         # f"\n   - Locate the actual content of the 'Cited Source' by examining both the online domain resource (https://attack.mitre.org/techniques/enterprise/) and the uploaded file (enterprise-attack-v16.0-techniques.xlsx)."
         # f"\n   - Retrieve and present the 'verbatim' full content of the cited source directly within your response, without just redirecting or referring me to an external link. Clearly indicate whether it was sourced from the online database, the provided file, or both."
         f"\n   - Identify and present the subset(s) of the cited source that corresponds to the 'Relevant Excerpt.' Ensure subset(s) is provided 'verbatim.'"
         f"\n   - Compare the 'Relevant Excerpt' to the located subset(s), noting any paraphrasing, omissions, additions, or discrepancies."
         f"\n\n"
         f"2. Rate the alignment between the 'Relevant Excerpt' and the located subset(s) of the cited source using the rubric below:"
         f"\n\n"
         f"**Rubric**:"
         f"\n5 (Excellent): The relevant excerpt is quoted verbatim and appears exactly in the cited source, without any alterations or discrepancies."
         f"\n4 (Good): The relevant excerpt is paraphrased but accurately reflects subset(s) of the cited source, without adding or omitting information that would alter the meaning or intent."
         f"\n3 (Satisfactory): The relevant excerpt is paraphrased and largely reflects subset(s) of the cited source, but with some minor differences or omissions that would slightly alter the meaning or intent."
         f"\n2 (Weak): The relevant excerpt is paraphrased and partially reflects subset(s) of the cited source, but with significant differences, omissions, or misrepresentations that noticeably alter the meaning or intent."
         f"\n1 (Unacceptable): The relevant excerpt fails to reflect any subset of the cited source, being fabricated, missing, or entirely misaligned."
         f"\n\n"
         f"**Ensure that the output follows this structure:**"
         # f"\n- **Access Domain Knowledge Base**: List all sources you successfully reviewed for this task."

         f"\n- **Alignment Rating**: Rate the alignment of the 'Relevant Excerpt' against the content of the 'Cited Source' using the rubric provided, along with a brief rationale."

         f"\n- **Locating 'verbatim' full content of 'Cited Source' and also the 'verbatim' subset(s) of the 'Cited Source' that corresponds to the 'Relevant Excerpt'**: Present the 'verbatim' full content of the cited source directly within your response, without just redirecting or referring me to an external link. Explicitly specify the source of the located content (online database, provided file, or both). Additionally, extract and present the verbatim subset(s) of the cited source that directly corresponds to the 'Relevant Excerpt.'"
         f"\n- **Relevant Excerpt**: Present the relevant excerpt from the tagging summary."
         f"\n- **Comparison**: Compare the 'Relevant Excerpt' and the located subset(s) of the cited source, providing detailed notes on any alignment, discrepancies, or paraphrasing."
         # f"\n- **Alignment Rating**: Rate the alignment of the 'Relevant Excerpt' against the content of the 'Cited Source' using the rubric provided, along with a brief rationale."
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

   sample_criteria_1_prompts_list = get__criteria_1_prompts_list( sample_tagging_summary , sample_cited_source_content )

   sample__prompt_and_response_dict_list = g4f_generate( sample_criteria_1_prompts_list )

   sample__prompt_and_response_dict_list

   # --------------------
   outputs_dir_path = "/home/jgwak1/gpt4free_JY/crtieria_1_outputs"

   output_fpath = os.path.join( outputs_dir_path , f"{sample_tagging_summary_dpath.split('/')[-2]}__{sample_tagging_summary_dpath.split('/')[-1]}.json")

   with open( output_fpath , "w") as json_fpath:
        json.dump( sample__prompt_and_response_dict_list , json_fpath, ensure_ascii=False, indent=4)




#    outputs_dir_path = "/home/jgwak1/gpt4free_JY/subtask_1_outputs__2024_12_18"
# #    apt29_collection_t1005_sample_path = "code_samples/externally_dependent_on_scripts/apt29/collection--T1005  Data from Local System--windows"

#    def get_sample_paths(starting_dir):
#         dirs_with_txt_files = []
#         for root, _, files in os.walk(starting_dir):
#             if any(file.endswith('.txt') for file in files):
#                 dirs_with_txt_files.append(root)
#         return dirs_with_txt_files


#    sample_paths_list = get_sample_paths( "/home/jgwak1/gpt4free_JY/code_samples" )

  
#    for sample_path in sample_paths_list:
       
#         code_snippet_file_path = os.path.join(sample_path, "code_snippet.txt")
#         background_info_file_path = os.path.join(sample_path, "background_info.txt")

#         if os.path.exists(code_snippet_file_path):
#             code_snippet_str = open(code_snippet_file_path, "r").read() 
#         else:
#             raise RuntimeError(f"Missing 'code_snippet.txt' at {sample_path}")

#         if os.path.exists(background_info_file_path):
#             background_info_str  = open(background_info_file_path, "r").read() 
#         else:
#             background_info_str = "N/A"


#         sample__subtask_1_prompt_list = get__subtask_1_prompts_list( code_snippet= code_snippet_str , background_info= background_info_str )

#         sample__prompt_and_response_dict_list = g4f_generate( sample__subtask_1_prompt_list )


#         output_fpath = os.path.join( outputs_dir_path , f"{sample_path.split('/')[-2]}__{sample_path.split('/')[-1]}.json")
#         with open( output_fpath , "w") as json_fpath:
#             json.dump( sample__prompt_and_response_dict_list , json_fpath, ensure_ascii=False, indent=4)




