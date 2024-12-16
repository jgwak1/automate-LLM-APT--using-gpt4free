from g4f.client import Client

def g4f_generate( prompt ):
    
    client = Client()
    
    response = ''

    for llm in [
        'gpt-4o',
        'gpt-4o-mini',
        'gpt-4-turbo',
        'gpt-4',
        'o1-preview',
        'o1-mini',
        "gemini-pro", 
        "gemini-flash", 
        "gemini",
        "mixtral-8x7b",
        "llama-3.1-405b"
        ]:
    
        try:
            response = client.chat.completions.create(
                model=llm,
                messages=[
                    {"role": "user", "content":
                    prompt}],
                # Add any other necessary parameters
            ).choices[0].message.content.strip()
    
        except:
            continue
    
        if 'sorry' not in response and \
            'cannot' not in response  and \
            'rate limit' not in response and \
            "can't" not in response and \
            'not safe' not in response and \
            "don't know" not in response and \
            "403 Forbidden" not in response and \
            'invisible' not in response and \
            len(response) > 10  :
            return response
    
        else: 
            print('-'*100)
            print(response)
            print('-'*100)
            
    return None




if __name__ == "__main__":


    # TODO Explore file-upload 


   prmpt = "Hwi"

   resp = g4f_generate( prmpt )

   print( resp )

   pass
