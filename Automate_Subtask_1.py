# https://github.com/xtekky/gpt4free/blob/8d8756f74500e7a74a73fab63bdd014fe4e3f1e7/g4f/Provider/ChatGpt.py#L108
# https://github.com/xtekky/gpt4free/blob/8d8756f74500e7a74a73fab63bdd014fe4e3f1e7/docs/client.md?plain=1#L109
# https://github.com/xtekky/gpt4free/blob/8d8756f74500e7a74a73fab63bdd014fe4e3f1e7/g4f/client/service.py#L24C5-L24C27


#    prmpt = "Which ChatGPT model are you? Be specific. Are you ChatGPT 4? 4.o? 3? or other? What platform are you?"


from g4f.client import Client
from g4f.Provider import OpenaiChat

import os
import json
import time






# from prompt_templates_NO_file_upload.subtask_1 import get__subtask_1_prompts_list
def get__subtask_1_prompts_list( code_snippet : str = "", background_info : str = "N/A" ):

    prompt_1 = (
            f"Given the code snippet and its background information (if available) below, "
            f"provide a concise behavioral description based on the following 4 steps. "
            f"I will provide you the 4 steps sequentially, so do not start yet:\n\n"
            f"Code snippet:\n{code_snippet}\n\n"
            f"Background information (if available):\n{background_info}\n\n"
            f"Please do not tag the final description with any MITRE ATT&CK Tactics, Techniques, or Procedures (TTPs)."
    )


    prompt_2 = "Step 1: Examine the code snippet and its background information (if available) to identify its core function, such as making API calls, performing file manipulations, interacting with system-level resources, or initiating network communications. Pay close attention to any options or flags that specify how the command operates."
    prompt_3 = "Step 2: Identify the inputs and outputs, including the data or parameters the commands accept (e.g., task name, file path, user or group name), and the resulting actions or outcomes they produce (e.g., creating a scheduled task, listing group members, or displaying output)."
    prompt_4 = "Step 3: Describe the actions performed by the commands in plain language, focusing on what it does and its potential impact on the system or environment."

    prompt_5 = "Step 4: Adjust the level of detail in the description from Step 3 to match the level typically found in a description of a MITRE ATT&CK technique. Please do not tag the final description with any MITRE ATT&CK Tactics, Techniques, or Procedures (TTPs)"

    # prompt_5_First_Modified = (
    #     f"Step 4: Adjust the description to focus more on the higher-level intention of the code (similar to a typical description of a MITRE ATT&CK technique) rather than being providing plain language explanations of each line of code."
    #     f"Please do not tag the final description with any MITRE ATT&CK Tactics, Techniques, or Procedures (TTPs)"
    # ) 

    # prompt_5_Second_Modified = (
    #     "Step 4: Refine the description from Step 3 to emphasize the higher-level intention "
    #     "or overarching purpose of the code, using language similar to a typical MITRE ATT&CK technique description. "
    #     "This should highlight the strategic objective rather than detailing individual lines of code or actions. "

    #     "Please do not tag the final description with any MITRE ATT&CK Tactics, Techniques, or Procedures (TTPs)."
    # )

    return [ prompt_1, prompt_2, prompt_3, prompt_4, prompt_5 ]




def get__subtask_1_prompts_list__POST_background( code_snippet : str = "", background_info : str = "N/A" ):

    prompt_1 = (
            # f"Given the code snippet and its background information (if available) below, "
            f"Given the code snippet below, "
            f"provide a concise behavioral description based on the following 4 steps. "
            f"I will provide you the 4 steps sequentially, so do not start yet:\n\n"
            f"Code snippet:\n{code_snippet}\n\n"
            # f"Background information (if available):\n{background_info}\n\n"
            # f"Please do not tag the final description with any MITRE ATT&CK Tactics, Techniques, or Procedures (TTPs)."
    )

    # prompt_2 = "Step 1: Examine the code snippet and its background information (if available) to identify its core function, such as making API calls, performing file manipulations, interacting with system-level resources, or initiating network communications. Pay close attention to any options or flags that specify how the command operates."

    prompt_2 = "Step 1: Examine the code snippet to identify its core function, such as making API calls, performing file manipulations, interacting with system-level resources, or initiating network communications. Pay close attention to any options or flags that specify how the command operates."
    prompt_3 = "Step 2: Identify the inputs and outputs, including the data or parameters the commands accept (e.g., task name, file path, user or group name), and the resulting actions or outcomes they produce (e.g., creating a scheduled task, listing group members, or displaying output)."
    prompt_4 = "Step 3: Describe the actions performed by the commands in plain language, focusing on what it does and its potential impact on the system or environment."

    prompt_btwn_4n5 = (
            f"Step 4: Following is the background information for the code snippet, which includes information relevant to the code snippet's behavior but not directly available from the code snippet itself "
            f"(e.g., the code snippet shows only the function usage, while the background information provides the implementation of that function). "
            f"Adjust the description from Step 3 to reflect the complete behavior of the code snippet, supplemented by the provided background information.\n\n"
            f"Background information:\n{background_info}\n\n"
    )

    # prompt_5 = (
    #     "Step 5: Produce a final plain-language description by refining the description from Step 4 to capture not only the key actions, key features and potential impact of the code snippet but also its higher-level objective, similar to a typical MITRE ATT&CK technique description. "
    #     "Please do not tag the final description with any MITRE ATT&CK Tactics, Techniques, or Procedures (TTPs)."
    # )

    prompt_5_v2 = (
        "Step 5: Produce a final plain-language description by refining the description from Step 4 to focus on the key actions, key features, potential impact, and higher-level objective of the code snippet in a clear and concise manner, avoiding excessive details. "
        "Do not include any tags for MITRE ATT&CK Tactics, Techniques, or Procedures (TTPs)."
    )


    return [ prompt_1, prompt_2, prompt_3, prompt_4, prompt_btwn_4n5, prompt_5_v2 ]


def get__subtask_1_prompts_list__PRE_background( code_snippet : str = "", background_info : str = "N/A" ):

    prompt_1 = (
            # f"Given the code snippet and its background information (if available) below, "
            f"Given the code snippet below, "
            f"provide a concise behavioral description based on the following 4 steps. "
            f"I will provide you the 4 steps sequentially, so do not start yet:\n\n"
            f"Code snippet:\n{code_snippet}\n\n"
            # f"Background information (if available):\n{background_info}\n\n"
            f"Please do not tag the final description with any MITRE ATT&CK Tactics, Techniques, or Procedures (TTPs)."
    )

    prompt_2 = "Step 1: Examine the code snippet and its background information (if available) to identify its core function, such as making API calls, performing file manipulations, interacting with system-level resources, or initiating network communications. Pay close attention to any options or flags that specify how the command operates."
    prompt_3 = "Step 2: Identify the inputs and outputs, including the data or parameters the commands accept (e.g., task name, file path, user or group name), and the resulting actions or outcomes they produce (e.g., creating a scheduled task, listing group members, or displaying output)."
    prompt_4 = "Step 3: Describe the actions performed by the commands in plain language, focusing on what it does and its potential impact on the system or environment."

    prompt_5 = (
        "Step 5: Adjust the description from Step 4 using language similar to a typical MITRE ATT&CK technique description. "
        "Please do not tag the final description with any MITRE ATT&CK Tactics, Techniques, or Procedures (TTPs)."
    )




    return [ prompt_1, prompt_2, prompt_3, prompt_4, prompt_5 ]







def g4f_generate( prompt_list : list ):


    # client = Client(provider=OpenaiChat)   
    client = Client()  

    # JY: To interact with same client with multiple prompts (i.e., Command line Chat Program)
    #     > https://github.com/xtekky/gpt4free/blob/8d8756f74500e7a74a73fab63bdd014fe4e3f1e7/docs/client.md?plain=1#L256
    #     > https://github.com/xtekky/gpt4free/blob/8d8756f74500e7a74a73fab63bdd014fe4e3f1e7/g4f/Provider/ChatGpt.py#L80
    #     > https://community.openai.com/t/how-can-i-maintain-conversation-continuity-with-chat-gpt-api/574819
    #       -- "Is there any other way than to save past conversation history in a DB and use it? (Dec 2023)"
    #           > "LLM models today are stateless, meaning that every single bit of context you want it to consider, 
    #              should be passed with every interaction with it through the messages.
    #              So no, there is no way to maintain a conversation rather than passing it (or its summary) every time to the model."

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


#    outputs_dir_path = "/home/jgwak1/gpt4free_JY/subtask_1_outputs__With_Modified_Prompt_5__2024_12_24"
#    outputs_dir_path = "subtask_1_outputs__With_Second_Modified_Prompt_5__2024_12_24"

#    outputs_dir_path = "subtask_1_outputs__POST_background__2024_12_24"

   outputs_dir_path = "subtask_1_outputs__POST_background__2024_12_25__Produce_More_Clear_and_Concise_Final_Description__trial_3"

#    apt29_collection_t1005_sample_path = "code_samples/externally_dependent_on_scripts/apt29/collection--T1005  Data from Local System--windows"

   def get_sample_paths(starting_dir):
        dirs_with_txt_files = []
        for root, _, files in os.walk(starting_dir):
            if any(file.endswith('.txt') for file in files):
                dirs_with_txt_files.append(root)
        return dirs_with_txt_files


   sample_paths_list = get_sample_paths( "/home/jgwak1/gpt4free_JY/code_samples" )

#    samples_to_reexamine = \
#    [ 
#     # [ Not in Top-10 list ]
#    "apt29/collection--T1005  Data from Local System--windows", 

#    "apt29/defensive-evasion--T1134.002  Access Token Manipulation  Create Process with Token--windows", 
#    "apt29/discovery--T1033  System Owner,User Discovery--windows",

#    # "apt29/execution--T1204.002  User Execution  Malicious File--windows", # Discard as background info is too long
#    "apt29/privilege-escalation--T1134.001  Access Token Manipulation  Token Impersonation,Theft--windows",
#    "carbanak/defense-evasion--T1140  Deobfuscate,Decode Files or Information--windows",
#    # "fin6/credential-access--T1003.001  OS Credential Dumping  LSASS Memory - Invoke-Mimikatz--windows"  # Discard as background info is too long
#    "menu_pass/execution--T1047  Windows Management Instrumentation--windows",

#    # [ Top 6 or 7 ]

#    "carbanak/collection--T1005  Data from Local System--linux",
#    "fin6/privilege-escalation--T1134: Access Token Manipulation--windows",
#    "oilrig/Ingress Tool Transfer--T1105  Ingress Tool Transfer--Windows"
# #    ] 

#    previously_poor_sample_paths_list = [ sample_path for sample_path in sample_paths_list if any( [ sample_path.endswith(s) for s in samples_to_reexamine ] ) ] 

#    sample_paths_list = [ sample_path for sample_path in sample_paths_list if sample_path not in previously_poor_sample_paths_list ] 


   for sample_path in sample_paths_list:
        
       
        code_snippet_file_path = os.path.join(sample_path, "code_snippet.txt")
        background_info_file_path = os.path.join(sample_path, "background_info.txt")

        if os.path.exists(code_snippet_file_path):
            code_snippet_str = open(code_snippet_file_path, "r").read() 
        else:
            raise RuntimeError(f"Missing 'code_snippet.txt' at {sample_path}")

        if os.path.exists(background_info_file_path):
            background_info_str  = open(background_info_file_path, "r").read() 
        else:
            background_info_str = "N/A"


        # sample__subtask_1_prompt_list = get__subtask_1_prompts_list( code_snippet= code_snippet_str , background_info= background_info_str )


        sample__subtask_1_prompt_list = get__subtask_1_prompts_list__POST_background( code_snippet= code_snippet_str , background_info= background_info_str )

        # get__subtask_1_prompts_list__POST_background


        sample__prompt_and_response_dict_list = g4f_generate( sample__subtask_1_prompt_list )


        output_fpath = os.path.join( outputs_dir_path , f"{sample_path.split('/')[-2]}__{sample_path.split('/')[-1]}.json")
        with open( output_fpath , "w") as json_fpath:
            json.dump( sample__prompt_and_response_dict_list , json_fpath, ensure_ascii=False, indent=4)





