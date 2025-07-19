import asyncio
from agents.llm import get_llm
from langchain.agents.agent import AgentExecutor
from langchain.agents import create_structured_chat_agent
from langsmith import Client
from langchain_core.tools import StructuredTool
from langchain_core.runnables import chain
from langgraph.graph import StateGraph, END
from agents.telegram_agent.schemas import TelegramImageInput, TelegramTextInput, AgentState

prompt = Client().pull_prompt("hwchase17/structured-chat-agent", include_model=True)


class TelegramAgent:
    def __init__(self):
        self.llm = get_llm()
        self.tools = []
        self.struct_tools = self.StructTools(self)
        self.agent = self.get_agent()

    class StructTools:
        def __init__(self, other_self):
            self.send_message = StructuredTool.from_function(
                name="send_message",
                coroutine=other_self.send_message,
                description="""send message through telegram_agent""",
                args_schema=TelegramTextInput
            )
            self.send_image = StructuredTool.from_function(
                name="send_image",
                coroutine=other_self.send_image,
                description="""Send image through telegram_agent""",
                args_schema=TelegramImageInput
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
    async def send_message(user_id: int, text: str):
        await asyncio.sleep(1)
        return (f"I send the message: '{text}' "
                f"to userid: {user_id}")

    @staticmethod
    async def send_image(user_id: int, image_url: str):
        await asyncio.sleep(1)
        return f"I have snd image"

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

# import asyncio
# async def main():
#     agent = TelegramAgent()
#     agent.tools.append(agent.struct_tools.send_message)
#
#     # Sample query to test the agent with tool usage
#     query = "Send message hello"
#
#     print(f"User: {query}")
#     response = await agent.run(query)
#
#     print(f"Agent Response:\n{response}")
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
