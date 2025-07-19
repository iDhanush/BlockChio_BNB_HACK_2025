from globar_vars import Var
from langchain_google_genai import ChatGoogleGenerativeAI
import random

llm_list = []
for api_key in Var.GOOGLE_API_KEYS:
    llm = ChatGoogleGenerativeAI(
        google_api_key=api_key,
        model='gemini-2.0-flash-lite',
        temperature=0.3)
    # print(llm.get_num_tokens())
    llm_list.append(llm)


def get_llm():
    return random.choice(llm_list)
