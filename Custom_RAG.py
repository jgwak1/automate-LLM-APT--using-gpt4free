

# TODO @ 2024-12-16: Impelment an External RAG (Look for Open sourced RAG) here 
#     > https://github.com/xtekky/gpt4free/discussions/1769
#     > https://github.com/xtekky/gpt4free/issues/1100
# from langchain_openai import OpenAIEmbeddings



import pandas as pd

# https://huggingface.co/sentence-transformers
# https://github.com/UKPLab/sentence-transformers/issues/3135
from sentence_transformers import SentenceTransformer
# https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.faiss.FAISS.html
from langchain_community.vectorstores import FAISS , Chroma
from langchain_core.vectorstores import InMemoryVectorStore

# from langchain.embeddings import SentenceTransformerEmbeddings 
# from langchain_community.chains import VectorSearch


from langchain.embeddings.base import Embeddings
from typing import List

if __name__ == "__main__":

   mitre_attack_technique_dataset_fpath = "/home/jgwak1/gpt4free_JY/enterprise-attack-v16.0-techniques.xlsx"

   mitre_attack_technique_dataset = pd.read_excel(mitre_attack_technique_dataset_fpath, engine='openpyxl')
   mitre_attack_technique_dataset

   technique_texts = [
      f"{row['ID']} - {row['name']}: {row['description']}"
      for _, row in mitre_attack_technique_dataset.iterrows()
   ]

   # embedding_model = SentenceTransformer("all-MiniLM-L6-v2", device='cpu') # JY: do it with cpu for now. as there are some dependency-issues with gpu  
   # technique_embeddings = embedding_model.encode(technique_texts, show_progress_bar=True)


   class CustomEmbeddings(Embeddings):
      def __init__(self, model_name: str = "all-MiniLM-L6-v2", device = "cpu"): # or 'cuda'
         self.model = SentenceTransformer(model_name, device= device) # JY: Do it with cpu for now instead of cuda.
                                                                    #     As don't need to deal with dependency-issues with gpu  
                                                                    #     Also "all-MiniLM-L6-v2" appears to be lightweight enough with cpu

      def embed_documents(self, documents: List[str]) -> List[List[float]]:
         return [self.model.encode(sentences= d, show_progress_bar=True).tolist() for d in documents]

      def embed_query(self, query: str) -> List[float]:
         return self.model.encode(sentences= [query], show_progress_bar=True)[0].tolist()

   # Create the custom embedding function
   embedding_model = CustomEmbeddings(model_name="all-MiniLM-L6-v2")



   # JY: Doesn't work yet. Probably need to set a persistent database -- need to study this more.
   # vectorStore = Chroma.from_texts(
   #    texts=technique_texts,
   #    embedding=embedding_model,
   # )

   # JY: Works after "pip install faiss-cpu" & "pip install faiss-gpu"
   # https://faiss.ai/ -- seems to use "L2 Norm (Euclidean Distance)"
   vectorStore__FAISS = FAISS.from_texts(
      texts=technique_texts,
      embedding=embedding_model,
   )

   # JY: Works . Seems to retrieve based on just 'cosine-similarity'
   # https://api.python.langchain.com/en/latest/vectorstores/langchain_core.vectorstores.in_memory.InMemoryVectorStore.html
   # > "Uses a dictionary, and computes cosine similarity for search using numpy."
   vectorStore__InMemoryVectorStore = InMemoryVectorStore.from_texts(
         texts=technique_texts,
         embedding=embedding_model,
   )


   # # 4. Define a retrieval function
   def retrieve_top_techniques(query, 
                               vectorstore, 
                               top_k= 10 ):
      # Retrieve top-k most relevant techniques
      docs_and_scores = vectorstore.similarity_search_with_score(query, k=top_k) # Generates embedding for the query inside of it
      return docs_and_scores


   # INTERESTING!! T1047 이 위에 나오긴함 Top 2 로 !! 이걸로도 Top10 할수는 있을듯?? -- 가능은 할듯 대신 explanation은 produce하기 힘들겠지만
   #               아니면 그냥 provide the whole techqniue knwoledge-file ?

   # 5. Test with an input query

   behavior_description__menu_pass__execution__T1047__Windows_Management_Instrumentation = \
   "The code snippet establishes a remote connection with the target host and executes commands through WMI using the `wmiexec.vbs` script. In the half-interactive shell mode utilized in this instance, the script can send and receive output, but does not grant a full command-line interface. This setup poses a risk for unauthorized access and control of the target host, enabling attackers to execute arbitrary commands, exploit the system for further operations like data exfiltration, or make unauthorized changes in the host's configuration. Proper permissions for WMI access on the target are required for the script's execution, highlighting the need for strong restrictions and monitoring to mitigate potential abuse." 
   query = behavior_description__menu_pass__execution__T1047__Windows_Management_Instrumentation
   top_techniques__InMemoryVectorStore = retrieve_top_techniques(query, vectorStore__InMemoryVectorStore)
   top_techniques__FAISS = retrieve_top_techniques(query, vectorStore__FAISS)

   # Display results
   print("Query:", query)
   print("\nTop Relevant Techniques (top_techniques__InMemoryVectorStore")
   for i, (technique, score) in enumerate(top_techniques__InMemoryVectorStore, 1):
      print(f"{i}. {technique} (Score: {score})")
   print("-"*20)
   print("\nTop Relevant Techniques (top_techniques__FAISS")
   for i, (technique, score) in enumerate(top_techniques__InMemoryVectorStore, 1):
      print(f"{i}. {technique} (Score: {score})")

   print()

   # TODO @ 2024-12-16 : NEED TO DEBUG THIS 
   # TODO: Problem with the following
   # https://github.com/langchain-ai/langchain/discussions/16222
   # https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.faiss.FAISS.html#langchain_community.vectorstores.faiss.FAISS.from_texts
   # 3. Create FAISS vector store
   # langchain vector store with sentence_transformer
   # https://medium.com/@garysvenson09/how-to-use-sentence-transformers-in-langchain-projects-c279bb535e0f (X)
   # https://betterprogramming.pub/building-a-question-answer-bot-with-langchain-vicuna-and-sentence-transformers-b7f80428eadc
   # vector_store = InMemoryVectorStore( technique_embeddings )
   # for text, embedding in zip(technique_texts, technique_embeddings):
   #    vector_store.add_texts([text], [embedding])
   # vector_store = FAISS.from_texts(technique_texts, technique_embeddings)


   # =============================================================================================
   # 2024-12-17
   # https://github.com/langchain-ai/langchain/discussions/7818#discussioncomment-9847810
   #   
   #   To integrate the SentenceTransformer model with LangChain's Chroma, 
   #   you need to ensure that the embedding function is correctly implemented and used. 
   #   
   #   Here is a step-by-step guide based on the provided information and the correct approach:


   # # 4. Define a retrieval function
   # def retrieve_top_techniques(query, 
   #                             vectorstore, 
   #                             top_k= 10 ):
   #    # Retrieve top-k most relevant techniques
   #    docs_and_scores = vectorstore.similarity_search_with_score(query, k=top_k) # Generates embedding for the query inside of it
   #    return docs_and_scores

   # # 5. Test with an input query
   # query = "How can an attacker gain higher-level permissions?"
   # top_techniques = retrieve_top_techniques(query, vectorStore__InMemoryVectorStore)

   # # Display results
   # print("Query:", query)
   # print("\nTop Relevant Techniques:")
   # for i, (technique, score) in enumerate(top_techniques, 1):
   #    print(f"{i}. {technique} (Score: {score})")