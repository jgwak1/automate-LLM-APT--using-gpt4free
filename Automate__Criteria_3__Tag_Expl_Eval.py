''' Might need to worry about the "max_token" ? '''





from g4f.client import Client
from g4f.Provider import OpenaiChat

import os
import json
import time






# from prompt_templates_NO_file_upload.subtask_1 import get__subtask_1_prompts_list
def get__criteria_3_prompts_list( tagging_summary : dict , behavior_description : dict ):


    # Slightly modified the Criteria-3 prompt:
    # 
    #    > For the Criteria-3 prompt used with the ChatGPT browser, 
    #    > just provided the Tagging Summary, and asked ChatGPT to refer to the 'Explanation for Tag' and 'Relevant Excerpt' included in it,
    #    > to avoid manual labor 
    #
    #    > Here, explicitly provided 'Explanation for Tag' and 'Relevant Excerpt'
    #    > as can easily extract those two programmatically without manual labor.

    prompt_1 = (
         f"### Task"
         f"\nAssess whether the 'Explanation for Tag' effectively clarifies why the 'Behavior Description' is assigned a tag (i.e., an ATT&CK technique), using support from the 'Relevant Excerpt'."
         f"\n\n"
         f"---"
         f"\n\n"

         f"**Behavior Description**:"
         f"\n{ behavior_description['Behavior Description'] }"
         f"\n\n"
         f"**Relevant Excerpt**:"
         f"\n{ tagging_summary['Relevant Excerpt'] }"
         f"\n\n"
         f"**Explanation for Tag**:"
         f"\n{ tagging_summary['Explanation for Tag'] }"
         f"\n\n"

         # f"#### Behavior Description"
         # f"\n{ behavior_description['Behavior Description'] }"
         # f"\n\n"
         # f"#### Tagging Summary"
         # f"\n*<replace with tagging summary>*"
         # f"\n\n"
         f"---"
         f"\n\n"
         f"### Instructions"
         f"\n\n"
         f"1. Review the provided 'Behavior Description,' 'Relevant Excerpt,' and 'Explanation for Tag' from the tagging summary. Note that the 'Tag' refers to the 'ATT&CK technique' mentioned at the beginning of the tagging summary."
         f"\n2. Rate how well the 'Explanation for Tag' justifies the tag assignment by connecting the 'Behavior Description' and the 'Relevant Excerpt' using the rubric below."
         f"\n3. Provide a rationale for your rating, followed by a sentence-level analysis explaining how each sentence of the 'Explanation for Tag' derives from or corresponds to the 'Behavior Description' and/or 'Relevant Excerpt' for verification purposes."
         f"\n\n"
         f"---"
         f"\n\n"
         f"### Rubric"
         f"\n\n"
         f"- **5 (Excellent)**: The 'Explanation for Tag' comprehensively clarifies why the 'Behavior Description' is assigned the tag, using strong and detailed evidence from the 'Relevant Excerpt.'"
         f"The 'Explanation for Tag' is entirely relevant and fully addresses both the 'Behavior Description' and the 'Relevant Excerpt,' offering a complete and well-justified rationale for the tag."
         f"\n\n"
         f"- **4 (Good)**: The 'Explanation for Tag' clearly clarifies why the 'Behavior Description' is assigned the tag, using substantial and appropriate evidence from the 'Relevant Excerpt.'"
         f"The 'Explanation for Tag' is consistently relevant and meaningfully addresses both the 'Behavior Description' and the 'Relevant Excerpt,' though it may have minor omissions or slightly less depth than a comprehensive justification."
         f"\n\n"
         f"- **3 (Satisfactory)**: The 'Explanation for Tag' sufficiently clarifies why the 'Behavior Description' is assigned the tag, using reasonable evidence from the 'Relevant Excerpt.'"
         f"The 'Explanation for Tag' is generally relevant and adequately addresses both the 'Behavior Description' and the 'Relevant Excerpt,' but it may not explore key aspects in depth or rely on less specific evidence."
         f"\n\n"
         f"- **2 (Weak)**: The 'Explanation for Tag' partially clarifies why the 'Behavior Description' is assigned the tag, using limited evidence from the 'Relevant Excerpt.'"
         f"The 'Explanation for Tag' is loosely relevant and only weakly addresses either the 'Behavior Description' or the 'Relevant Excerpt,' providing an unclear or insufficient rationale."
         f"\n\n"
         f"- **1 (Unacceptable)**: The 'Explanation for Tag' fails to clarify why the 'Behavior Description' is assigned the tag, using no meaningful evidence from the 'Relevant Excerpt.'"
         f"The 'Explanation for Tag' is irrelevant and does not address either the 'Behavior Description' or the 'Relevant Excerpt.'"
         f"\n\n"
         f"---"
         f"\n\n"
         f"### Ensure that the output follows this structure:"
         f"\n\n"
         f"- **Rating**:"
         f"\n  Provide a rating for how well the 'Explanation for Tag' justifies the tag assignment by connecting the 'Behavior Description' and the 'Relevant Excerpt' according to the rubric provided."
         f"\n\n"
         f"- **Rationale for Rating**:"
         f"\n  Provide a concise, higher-level summary of how the 'Behavior Description' and 'Relevant Excerpt' semantically and substantively contribute to the 'Explanation for Tag.' The rationale should reflect the extent to which the 'Explanation for Tag' integrates key ideas or concepts from the 'Behavior Description' and 'Relevant Excerpt' to justify the assigned tag, and highlight any notable strengths, gaps, or omissions in the semantic connection."
         f"\n\n"
         f"- **Details:**"
         f"\n  - **Original Explanation for Tag:**"
         f"\n    *(Provide the original explanation for the tag.)*"
         f"\n\n"
         f"  - **Original Behavior Description:**"
         f"\n    *(Provide the original behavior description.)*"
         f"\n\n"
         f"  - **Original Relevant Excerpt:**"
         f"\n    *(Provide the original relevant excerpt.)*"
         f"\n\n"
         f"  - **How 'Behavior Description' and 'Relevant Excerpt' Contribute to 'Explanation for Tag' at the Sentence Level:**"
         f"\n    For each sentence in the 'Explanation for Tag,' identify and explain how the exact sentences or phrases from the 'Behavior Description' and 'Relevant Excerpt' contribute, as applicable."
         f"\n    Use the following format for reporting:"
         f"\n\n"
         f"    - **Sentence <n> of 'Explanation for Tag':** *<sentence n>*"
         f"\n      - **Contribution of 'Behavior Description':** Identify the exact sentence or phrase from the 'Behavior Description' and explain its contribution. (if there is)"
         f"\n      - **Contribution of 'Relevant Excerpt':** Identify the exact sentence or phrase from the 'Relevant Excerpt' and explain its contribution. (if there is)"
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

   sample_criteria_3_prompts_list = get__criteria_3_prompts_list( sample_tagging_summary , sample_behavior_description )

   sample__prompt_and_response_dict_list = g4f_generate( sample_criteria_3_prompts_list )

   sample__prompt_and_response_dict_list

   # --------------------
   outputs_dir_path = "/home/jgwak1/gpt4free_JY/crtieria_3_outputs"

   output_fpath = os.path.join( outputs_dir_path , f"{sample_tagging_summary_dpath.split('/')[-2]}__{sample_tagging_summary_dpath.split('/')[-1]}.json")

   with open( output_fpath , "w") as json_fpath:
        json.dump( sample__prompt_and_response_dict_list , json_fpath, ensure_ascii=False, indent=4)

