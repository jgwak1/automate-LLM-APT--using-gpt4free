
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
   prompt_5 = "Step 4: Adjust the level of detail in the description from Step 3 to match the level typically found in a description of a MITRE ATT&CK technique."

   return [ prompt_1, prompt_2, prompt_3, prompt_4, prompt_5]