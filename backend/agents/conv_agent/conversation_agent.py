import random
from langchain.agents import create_structured_chat_agent
from langchain.agents.agent import AgentExecutor
from langsmith import Client
from langchain_core.tools import StructuredTool
from langchain_core.runnables import chain
from langgraph.graph import StateGraph, END
from agents.conv_agent.schemas import AgentState
from agents.conv_agent.schemas import RagInput
from agents.llm import get_llm
from membase.memory.buffered_memory import BufferedMemory
from agents.conv_agent.rag import TextRAG
from membase.memory.message import Message
from pydantic import BaseModel
from langchain.schema.messages import HumanMessage, AIMessage


prompt = Client().pull_prompt("hwchase17/structured-chat-agent", include_model=True)

class ConvAgent:
    def __init__(self, cred: dict):
        self.llm = get_llm()
        self.tools = []
        self.rag_input = cred.get('rag_input', " ")
        self.rag = TextRAG(membase_account="sarathc", rag_input = self.rag_input)
        self.wallet = cred.get("wallet")
        self.private_key = cred.get("private_key")
        self.agent = self.get_agent()
        self.struct_tools = self.StructTools(self)
        self.memory = BufferedMemory(membase_account="0x6BF61cc9cC3F71eF7aBA7A82d132E4584EEe81A1",
                        auto_upload_to_hub=False)

    class StructTools:
        def __init__(self, other_self):
            self.get_rag_response = StructuredTool.from_function(
                name="get_rag_response",
                func=other_self.get_rag_response,
                description="Retrives response from rag",
                args_schema=RagInput
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


    def get_rag_response(self, query: str):
        results = self.rag.query(query)
        return results


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
        self.memory.add(Message(name='user', content=query, role="user"))
        chat_history = []
        for msg in self.memory._messages:
            if msg.role == "user":
                chat_history.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                chat_history.append(AIMessage(content=msg.content))
        for i in range(3):
            try:
                self.agent = self.get_agent()
                result = await self.agent.ainvoke({
                    "question": query,
                    "response": None,
                    "messages": chat_history
                })
                self.memory.add(Message(name='assistant', content=result.get("response", "Error: Could not get output from agent"), role="assistant"))
                break
            except Exception as e:
                print('exception happened in agent 1:', str(e))
                last_exception = e
                continue
        if not result:
            return "Error: Could not get output from agent"

        return result.get("response", "Error: Could not get output from agent")


import asyncio
async def main():
    agent = ConvAgent({
        "wallet": "0x6BF61cc9cC3F71eF7aBA7A82d132E4584EEe81A1",
        "private_key": "0x6BF61cc9cC3F71eF7aBA7A82d132E4584EEe81A1",
        "rag_input": "Floks is a very great company based on building agentic ai "
    })
    agent.tools.append(agent.struct_tools.get_rag_response)
    # Sample query to test the agent with tool usage
    query = "What is the purpose of Floks?"

    print(f"User: {query}")
    response = await agent.run(query)

    print(f"Agent Response:\n{response}")


if __name__ == "__main__":
    asyncio.run(main())


