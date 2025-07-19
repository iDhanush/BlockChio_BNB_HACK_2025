from langchain.agents import create_structured_chat_agent
from langchain.agents.agent import AgentExecutor
from langsmith import Client
from langchain_core.tools import StructuredTool
from langchain_core.runnables import chain
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

from agents.blockchain_agent.schemas import AgentState, TransferInput, NoInput
from agents.llm import get_llm

prompt = Client().pull_prompt("hwchase17/structured-chat-agent", include_model=True)



class BlockchainAgent:
    def __init__(self):
        self.llm = get_llm()
        self.tools = []
        self.wallet = 'xxx'
        self.agent = self.get_agent()
        self.struct_tools = self.StructTools(self)

    class StructTools:
        def __init__(self, other_self):
            self.get_balance = StructuredTool.from_function(
                name="get_balance",
                coroutine=other_self.get_balance,
                description="""Get the balance of a wallet""",
                args_schema=NoInput
            )
            self.transfer = StructuredTool.from_function(
                name="transfer",
                coroutine=other_self.transfer,
                description="""Transfer Crypto from one wallet to another""",
                args_schema=TransferInput
            )
            self.mint_nft = StructuredTool.from_function(
                name="mint_nft",
                coroutine=other_self.mint_nft,
                description="""Mint a NFT""",
                args_schema=NoInput
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


    async def get_balance(self):
        await asyncio.sleep(1)

    @staticmethod
    async def transfer (amount: int, to: str):
        await asyncio.sleep(1)
        return f"You have transfered {amount} rs to {to}"

    @staticmethod
    async def mint_nft():
        await asyncio.sleep(1)
        return "You have minted a nft"



    @staticmethod
    def create_workflow(agent_executor):
        # Define the nodes for our graph
        @chain
        async def agent_node(state: AgentState) -> AgentState:
            question = state["question"]
            result = await agent_executor.ainvoke({
                "input": question,})
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
# async def main():
#     agent = BlockchainAgent()
#     agent.tools.append(agent.struct_tools.get_balance)
#
#     # Sample query to test the agent with tool usage
#     query = "How much is left?"
#
#     print(f"User: {query}")
#     response = await agent.run(query)
#
#     print(f"Agent Response:\n{response}")
#
#
# if __name__ == "__main__":
#     asyncio.run(main())


