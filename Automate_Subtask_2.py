# https://github.com/xtekky/gpt4free/blob/8d8756f74500e7a74a73fab63bdd014fe4e3f1e7/g4f/Provider/ChatGpt.py#L108
# https://github.com/xtekky/gpt4free/blob/8d8756f74500e7a74a73fab63bdd014fe4e3f1e7/docs/client.md?plain=1#L109
# https://github.com/xtekky/gpt4free/blob/8d8756f74500e7a74a73fab63bdd014fe4e3f1e7/g4f/client/service.py#L24C5-L24C27


#    prmpt = "Which ChatGPT model are you? Be specific. Are you ChatGPT 4? 4.o? 3? or other? What platform are you?"


from g4f.client import Client
from g4f.Provider import OpenaiChat

import os
import json
import time
from typing import List

import pandas as pd



# TODO @ 2024-12-16: Impelment an External RAG (Look for Open sourced RAG) here 
#     > https://github.com/xtekky/gpt4free/discussions/1769
#     > https://github.com/xtekky/gpt4free/issues/1100
from langchain_openai import OpenAIEmbeddings



# from prompt_templates_NO_file_upload.subtask_1 import get__subtask_1_prompts_list
def get__subtask_2_prompts_list( behavior_description : str,
                                 MITRE_ATTACK_Technique_Descriptions : List[str] ):


    
    ''' 
     [ "prompt_1" used for ChatGPT browser with File-Upload functionality ]
        You are tasked with analyzing the behavioral description of a code snippet to identify potential cyber threats. 

        Please begin by reviewing the MITRE ATT&CK framework by:
        Review “technique” sheet of the uploaded file. 
        ### Uploaded File
        **enterprise-attack-v16.0-techniques.xlsx**

        This will prepare you to use them as references for analyzing the behavioral description I will provide for the task in the next prompt.
    '''
    prompt_1 = (

            #f"DON'T OUTPUT ANYTHING TO THIS PROMPT. JUST ANSWER 'I HAVE REVIEWED'"   # <-- Despite this, 
                                                                                     #      it returned 'and for API requests replace  https://www.blackbox.ai with https://api.blackbox.ai'
                                                                                     #       indicated of issue in interaction with GPT which is highly likely of the
                                                                                     #       huge input prompt size due to 'MITRE_ATTACK_Technique_Descriptions' 

            f"You are tasked with analyzing the behavioral description of a code snippet to identify potential cyber threats. "
            f"\n"
            f"Please begin by reviewing the following technique descriptions in the MITRE ATT&CK framwork."
            f"This will prepare you to use them as references for analyzing the behavioral description I will provide for the task in the next prompt."       
            
            
            f"---"
            f"\n\n"
            f"### MITRE ATT&CK technique descriptions:"
            f"\n"
            f"{ MITRE_ATTACK_Technique_Descriptions }"

            #f"DON'T OUTPUT ANYTHING TO THIS PROMPT. JUST ANSWER 'I HAVE REVIEWED'"   # <-- Despite this, 
                                                                                     #      it returned 'and for API requests replace  https://www.blackbox.ai with https://api.blackbox.ai'
                                                                                     #       indicated of issue in interaction with GPT which is highly likely of the
                                                                                     #       huge input prompt size due to 'MITRE_ATTACK_Technique_Descriptions' 

    )



    prompt_2 = (
            f"### Task Instructions:"
            f"\n"
            f"Using the MITRE ATT&CK framework, determine if any ATT&CK technique(s) correspond to the behavioral description."
            f"\n"
            f"Report the top 10 ATT&CK techniques you consider most relevant, explain your reasoning for each, and assign a confidence level based on the following rubric:"
            f"\n\n"
            f"#### Confidence Level 1 (Low Confidence)"
            f"The selected ATT&CK technique is a potential match but there is limited evidence or contextual relevance. The match may be inferred based on general similarities or weak connections to the behavioral description. Uncertainty remains high, and further validation or contextual information is needed to strengthen the claim."
            f"\n"
            f"#### Confidence Level 2 (Moderately Low Confidence)"
            f"The ATT&CK technique is somewhat relevant to the behavioral description but lacks robust evidence or there may be ambiguity in its applicability. There are noticeable gaps or uncertainties in the match, requiring additional cross-referencing or supportive data."
            f"\n"
            f"#### Confidence Level 3 (Moderate Confidence)"
            f"The ATT&CK technique shows a reasonable degree of relevance and there is a satisfactory level of supporting evidence to justify its inclusion. While there may be some minor gaps or areas that require further review, the correspondence is generally credible based on available data."
            f"\n"
            f"#### Confidence Level 4 (High Confidence)"
            f"The selected ATT&CK technique aligns well with the behavioral description and is supported by significant evidence or correlation. The connection is clear and well-justified with relevant excerpts and data points, leaving minimal uncertainty or need for additional validation."
            f"\n"
            f"#### Confidence Level 5 (Very High Confidence)"
            f"The identified ATT&CK technique directly corresponds to the behavioral description, supported by strong evidence and contextually robust data. There is high confidence in the match, with a thorough, well-documented rationale leaving little room for doubt or ambiguity."
            f"\n\n"
            f"#### For each tagged technique, ensure that the output follows this structure:"
            f"\n\n"
            f"- **Explanation for Tag**: Provide a clear and well-reasoned explanation of the tag's relevance to the behavioral description."
            f"- **Confidence Level**: Specify the confidence level for the tag."
            f"- **Cited Source**: Provide a **precise reference** to the source supporting the match (e.g., from the **MITRE ATT&CK technique database**). Avoid plain-text citations."
            f"- **Relevant Excerpt**: Include **verbatim excerpt** from the **Cited Source** that substantiates the tag’s relevance. **Ensure the Relevant Excerpt is presented as verbatim, exactly as it appears in the Cited Source, without any summarizations, modifications, omissions, additions, or paraphrasing.**"            
            f"- **Speculations/Predictions**: If the ‘Explanation for Tag’ includes any speculative or predictive elements, clearly identify them. If there are no speculative or predictive elements, explicitly state that the ‘Explanation for Tag’ does not contain any speculative or predictive elements."            
            f"\n\n"
            f"### Task Breakdown"
            f"\n"
            f"When performing the task, specifically:"
            f"1. Look for an existing “description of technique” in the MITRE ATT&CK framework that best aligns with the provided behavioral description."
            f"2. If a match is found, tag the behavioral description based on it."
            f"\n"

            f"Make sure that the top 10 techniques are reported in descending order of confidence level."  # -- response is weird
            # f"Make sure that the top 1 technique are reported in descending order of confidence level."  # -- response is OK
            #                                                                                              #    This indicates "prompt_2" length is fine,
            #                                                                                              #    but returns outputs for all top 10 techniques
            #                                                                                              #    exceeds their output token limit, 
            #                                                                                              #    while returning top-1 does not.

            f"If multiple techniques share the same confidence level, assess their relative confidence to determine the order."
            f"Additionally, please provide the cited source as a link or reference, not as plain text."
            f"Lastly, please make sure the relevant excerpts are “verbatim” excerpts from the reviewed MITRE ATT&CK technique database."
            f"---"
            f"\n\n"
            f"### Behavioral Description of a Code Snippet:"
            f"\n"
            f"{behavior_description}"
    )


    return [ prompt_1, prompt_2 ]


def g4f_generate( prompt_list : list ):


    # client = Client(provider=OpenaiChat)   
    client = Client()  

    message_history = [] # conversation history for 'Command line Chat Program' - alike interaction
    prompt_and_response_dict_list = []

    for i, prompt in enumerate( prompt_list ) :
        print(f"prompt-{i+1} start")
        start_time = time.time()
        

        # With shorter prompt, it's just fine
        # prompt_1_without_long_technique_descriptions = (
        #         f"You are tasked with analyzing the behavioral description of a code snippet to identify potential cyber threats. "
        #         f"\n"
        #         f"Please begin by reviewing the following technique descriptions in the MITRE ATT&CK framwork."
        #         f"This will prepare you to use them as references for analyzing the behavioral description I will provide for the task in the next prompt."       
        #         f"---"
        #         f"\n\n"
        #         f"### MITRE ATT&CK technique descriptions:"
        #         f"\n"

        #         )

        prompt = prompt_list[0]

        message_history.append( {"role": "user",  "content": prompt} )

        try:

            # JY @ 2024-12-17: Weird output seems to be related to long prompt, as with shorter prompts the it returns reasonably ,
            # 
            #                  I've tried with "max_tokens = None" and confirmed it was None by default, but doesn't solve the issue. 
            #                  as 
            # https://github.com/xtekky/gpt4free/blob/821e78d9e631158b136ec46e0ce744ed0bc77425/g4f/Provider/deprecated/GetGpt.py#L39

            # https://github.com/xtekky/gpt4free/issues/1077
            # https://community.openai.com/t/max-tokens-chat-completion-gpt4o/758066

            response = client.chat.completions.create(
                # Add any other necessary parameters
                model= 'gpt-4o',
                # model= 'gemini',

                # "gemini-pro", 
                # "gemini-flash", 
                # "gemini",
                # model = "mixtral-8x7b",
                # "llama-3.1-405b"

                messages= message_history,  # Pass the message history (conversation history) to every prompt for a 'command-line chat program' like interaction

                # max_tokens= None

                # max_tokens= 32000, # https://community.openai.com/t/max-tokens-chat-completion-gpt4o/758066
                max_tokens= 16384, # https://community.openai.com/t/max-tokens-chat-completion-gpt4o/758066

                                    # > The total number of tokens for gpt-4o including prompt and completion tokens is 128,000. 
                                    # > But the maximum number of completion tokens is 4,096. 
                                    # > Unfortunate, as that seriously limits our use case.

                                    # Regardless of "max_tokens", have tried {None, 3, 4096, 16384, 32000}
                                    # Sometimes,
                                        # Returned response:
                                            # Exception: RetryProvider failed:
                                            # PollinationsAI: TypeError: argument of type 'NoneType' is not iterable
                                            # Liaobots: RateLimitError: Response 402: Rate limit reached
                                            # DarkAI: RateLimitError: Response 429: Rate limit reached
                                            # Blackbox: ClientResponseError: 502, message='Bad Gateway', url='https://www.blackbox.ai/api/chat'
                                            # ChatGptEs: ClientConnectorError: Cannot connect to host chatgpt.es:443 ssl:default [Connect call failed ('212.53.165.225', 443)]
                                            # ChatGpt: HTTPError: 429 Client Error: Too Many Requests for url: https://chatgpt.com/backend-anon/conversation
                                            # OpenaiChat: RateLimitError: Response 429: Rate limit reached                                    
                                    
                                        # Returned response:
                                            # "and for API requests replace  https://www.blackbox.ai with https://api.blackbox.ai"


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


   outputs_dir_path = "/home/jgwak1/gpt4free_JY/subtask_2_outputs__2024_12_16"

   # menu_pass__execution--T1047  Windows Management Instrumentation--windows
   sample__behavior_description = "The code snippet establishes a remote connection with the target host and executes commands through WMI using the `wmiexec.vbs` script. In the half-interactive shell mode utilized in this instance, the script can send and receive output, but does not grant a full command-line interface. This setup poses a risk for unauthorized access and control of the target host, enabling attackers to execute arbitrary commands, exploit the system for further operations like data exfiltration, or make unauthorized changes in the host's configuration. Proper permissions for WMI access on the target are required for the script's execution, highlighting the need for strong restrictions and monitoring to mitigate potential abuse."


   mitre_attack_technique_dataset_fpath = "/home/jgwak1/gpt4free_JY/enterprise-attack-v16.0-techniques.xlsx"
   mitre_attack_technique_dataset = pd.read_excel(mitre_attack_technique_dataset_fpath, engine='openpyxl')
   mitre_attack_technique_dataset

   mitre_attack_technique_descriptions = [
      f"{row['ID']} - {row['name']}: {row['description']}"
      for _, row in mitre_attack_technique_dataset.iterrows()
   ]



   sample__subtask_2_prompt_list = get__subtask_2_prompts_list( sample__behavior_description, 
                                                                mitre_attack_technique_descriptions )

   sample__prompt_and_response_dict_list = g4f_generate( sample__subtask_2_prompt_list )

   sample__prompt_and_response_dict_list

   output_fpath = os.path.join( outputs_dir_path , f"interaction.json")
   with open( output_fpath , "w") as json_fpath:
        json.dump( sample__prompt_and_response_dict_list , json_fpath, ensure_ascii=False, indent=4)





