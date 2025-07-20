import base64
import time
from pathlib import Path

from langchain.agents import create_structured_chat_agent
from langchain.agents.agent import AgentExecutor
from langsmith import Client
from langchain_core.tools import StructuredTool
from langchain_core.runnables import chain
from langgraph.graph import StateGraph, END
from agents.blockchain_agent.schemas import AgentState
from agents.image_agent.schemas import ImagePrompt
from agents.llm import get_llm
from responses import StandardException
import requests

prompt = Client().pull_prompt("hwchase17/structured-chat-agent", include_model=True)


import base64
import json
import requests
from pathlib import Path
def generate_gemini_image(api_key: str, prompt: str, output_file: str = "gemini_image.png"):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-preview-image-generation:generateContent"
    headers = {
        "x-goog-api-key": api_key,  # <-- Must be a string!
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{
            "parts": [
                {"text": prompt}
            ]
        }],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code}, {response.text}")

    try:
        base64_data = response.json()["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
        print(base64_data)
        with open(output_file, "wb") as f:
            f.write(base64.b64decode(base64_data))
        print(f"Image saved to {output_file}")
    except Exception as e:
        raise Exception(f"Failed to decode image: {e}")
# Example usage:
generate_gemini_image(get_llm(), "A cyberpunk astronaut dog on Mars playing chess with a robot.")


class ImageAgent:
    def __init__(self):
        self.llm = get_llm()
        self.tools = []
        self.struct_tools = self.StructTools(self)
        self.agent = self.get_agent()

    class StructTools:
        def __init__(self, other_self):
            self.generate_image = StructuredTool.from_function(
                name="generate_image",
                coroutine=other_self.generate_image,
                description="""Create image according to the prompt""",
                args_schema=ImagePrompt
            )

    def get_agent(self):
        agent = create_structured_chat_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt,
        )

        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )

        # Create LangGraph workflow
        workflow = self.create_workflow(agent_executor)
        self.agent = workflow
        return workflow

    @staticmethod
    async def google_search(search_list: list[str]):
        print(type(search_list), search_list)
        return "yoyoyo"

    @staticmethod
    async def generate_image(prompt: str):
        await asyncio.sleep(1)
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        return f"I have created an image for the prompt: {prompt}\nurl: https://jjssr.com/image.jpg\n note that the final output should contain all this information including the comment and url"

    @staticmethod
    def create_workflow(agent_executor):
        # Define the nodes for our graph
        @chain
        async def agent_node(state: AgentState) -> AgentState:
            question = state["question"]
            result = await agent_executor.ainvoke({
                "input": question, })
            state["response"] = result.get("output", "Error: Could not get output from agent")
            if type(state["response"]) is not dict:
                raise StandardException(status_code=402, details='invalid')
            return state

        # Define the graph
        workflow = StateGraph(AgentState)

        # Add the agent node
        workflow.add_node("agent", agent_node)

        # Set the entry point
        workflow.set_entry_point("agent")

        # Set the exit point
        workflow.add_edge("agent", END)

        # Compile the graph
        return workflow.compile()

    # noinspection PyTypeChecker
    async def run(self, query: str):
        result = None
        query = "Create an image from prompt" + query
        for i in range(3):
            try:
                self.agent = self.get_agent()
                result = await self.agent.ainvoke({
                    "question": query,
                    "response": None
                })
                break
            except Exception as e:
                print('exception happened in agent 1:', str(e))
                last_exception = e
                continue
        if not result:
            return "Error: Could not get output from agent"

        return result


import asyncio
generate_and_save_image('a cute cat')
# async def main():
#     agent = ImageAgent()
#     agent.tools.append(agent.struct_tools.create_img)
#
#     # Sample query to test the agent with tool usage
#     query = "Create an image of a cat"
#
#     print(f"User: {query}")
#     response = await agent.run(query)
#
#     print(f"Agent Response:\n{response}")
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
