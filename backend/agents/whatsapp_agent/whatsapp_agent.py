import asyncio
from http.client import responses

from langsmith import Client
from agents.llm import get_llm
from langchain_core.runnables import chain
from langgraph.graph import StateGraph, END
from langchain_core.tools import StructuredTool
from langchain.agents.agent import AgentExecutor
from langchain.agents import create_structured_chat_agent
from agents.whatsapp_agent.schemas import WhatsappTextInput, WhatsappImageInput, AgentState
from agents.whatsapp_agent.whatsapp import snd_image, snd_message
from twilio.rest import Client as Whatsapp

from globar_vars import Var

prompt = Client().pull_prompt("hwchase17/structured-chat-agent", include_model=True)


class WhatsappAgent:
    def __init__(self, creds:list):
        self.llm = get_llm()
        self.tools = []
        creds2 = {}
        for cred in creds:
            for key, val in cred.items():
                creds2[key] = val
        self.creds = creds2
        self.creds["whatsapp_client"] = Whatsapp(self.creds.get('account_sid'), self.creds.get('auth_token'))
        self.struct_tools = self.StructTools(self)
        self.agent = self.get_agent()

    class StructTools:
        def __init__(self, other_self):
            self.send_message = StructuredTool.from_function(
                name="send_message",
                coroutine=other_self.send_message,
                description="""send message through Whatsapp""",
                args_schema=WhatsappTextInput
            )
            self.send_image = StructuredTool.from_function(
                name="send_image",
                coroutine=other_self.send_image,
                description="""Send image through Whatsapp""",
                args_schema=WhatsappImageInput
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

    async def send_message(self, number: str, text: str):
        response = await snd_message(self.creds, number, text)
        return response

    async def send_image(self, number: str, image_url: str, body:str):
        response = await snd_image(self.creds, number, image_url, body)
        return response

    @staticmethod
    def create_workflow(agent_executor):
        # Define the nodes for our graph
        @chain
        async def agent_node(state: AgentState) -> AgentState:
            question = state["question"]
            result = await agent_executor.ainvoke({
                "input": question, })
            state["response"] = result.get("output", "Error: Could not get output from agent")
            # if type(state["response"]) is not dict:
            # state["response"] = "Error: Could not get output from agent"
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
async def main():
    account_sid = Var.ACCOUNT_SID
    auth_token = Var.AUTH_TOKEN
    whatsapp_number = Var.WHATSAPP_NUMBER
    cred = [{"account_sid":account_sid, "auth_token":auth_token, "whatsapp_number":whatsapp_number}]
    agent = WhatsappAgent(cred)
    agent.tools.append(agent.struct_tools.send_message)
    agent.tools.append(agent.struct_tools.send_image)
    # Sample query to test the agent with tool usage
    query = "Send image https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTtzQxCr9uIe4TS2m6Hg5IvNqQATg-wpo3KdQ&s +918891636432"

    print(f"User: {query}")
    response = await agent.run(query)

    print(f"Agent Response:\n{response}")


if __name__ == "__main__":
    asyncio.run(main())
