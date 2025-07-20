import asyncio
from aiogram import Bot
from agents.llm import get_llm
from langchain.agents.agent import AgentExecutor
from langchain.agents import create_structured_chat_agent
from langsmith import Client
from langchain_core.tools import StructuredTool
from langchain_core.runnables import chain
from langgraph.graph import StateGraph, END
from agents.telegram_agent.schemas import TelegramImageInput, TelegramTextInput, AgentState

# Pull the prompt template from LangSmith Hub
# You can replace this with your own prompt if you prefer
try:
    prompt = Client().pull_prompt("hwchase17/structured-chat-agent", include_model=True)
except Exception as e:
    print(f"Could not pull prompt from LangSmith. Using a default. Error: {e}")
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )


class TelegramAgent:
    def __init__(self, creds: dict):
        """
        Initializes the agent, tools, and the aiogram Bot instance.

        Args:
            creds (dict): A dictionary containing credentials.
                          Expected key: 'bot_token'.
        """
        if "bot_token" not in creds:
            raise ValueError("`creds` dictionary must contain a 'bot_token' key.")

        # Initialize Aiogram Bot
        self.bot = Bot(token=creds["bot_token"])

        self.llm = get_llm()
        self.struct_tools = self.StructTools(self)

        # Add tools to the agent's tool list
        self.tools = [
            self.struct_tools.send_message,
            self.struct_tools.send_image,
        ]

        self.agent = self.get_agent()

    class StructTools:
        def __init__(self, agent_instance):
            self.send_message = StructuredTool.from_function(
                name="send_telegram_message",
                coroutine=agent_instance.send_message,
                description="Sends a text message to a specified user through Telegram.",
                args_schema=TelegramTextInput
            )
            self.send_image = StructuredTool.from_function(
                name="send_telegram_image",
                coroutine=agent_instance.send_image,
                description="Sends an image from a URL to a specified user through Telegram.",
                args_schema=TelegramImageInput
            )

    def get_agent(self):
        """Creates the LangChain agent and wraps it in a LangGraph workflow."""
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

        return self.create_workflow(agent_executor)

    async def send_message(self, user_id: int, text: str) -> str:
        """
        Sends a text message to a user via Telegram using aiogram.
        """
        try:
            await self.bot.send_message(chat_id=user_id, text=text)
            print(f"Message sent to user {user_id}")
            return f"Successfully sent message to user_id {user_id}."
        except Exception as e:
            error_message = f"Failed to send message to user_id {user_id}. Error: {e}"
            print(error_message)
            return error_message

    async def send_image(self, user_id: int, image_url: str) -> str:
        """
        Sends an image to a user via Telegram using aiogram.
        """
        try:
            await self.bot.send_photo(chat_id=user_id, photo=image_url)
            print(f"Image sent to user {user_id}")
            return f"Successfully sent image to user_id {user_id}."
        except Exception as e:
            error_message = f"Failed to send image to user_id {user_id}. Error: {e}"
            print(error_message)
            return error_message

    @staticmethod
    def create_workflow(agent_executor):
        """Defines and compiles the LangGraph workflow."""

        @chain
        async def agent_node(state: AgentState) -> AgentState:
            result = await agent_executor.ainvoke({
                "input": state["question"],
                "chat_history": state.get("chat_history", [])
            })
            state["response"] = result.get("output", "Error: Could not get output from agent")
            return state

        workflow = StateGraph(AgentState)
        workflow.add_node("agent", agent_node)
        workflow.set_entry_point("agent")
        workflow.add_edge("agent", END)
        return workflow.compile()

    async def run(self, query: str):
        """
        Runs the agent with a given query, with a retry mechanism.
        """
        result = None
        last_exception = None
        for i in range(3):
            try:
                # No need to re-create the agent here, it's done in __init__
                result = await self.agent.ainvoke({
                    "question": query,
                })
                break
            except Exception as e:
                print(f'Exception happened in agent (attempt {i + 1}/3): {e}')
                last_exception = e
                await asyncio.sleep(1)  # Wait before retrying

        if not result:
            return f"Error: Could not get output from agent after 3 attempts. Last error: {last_exception}"

        return result


async def main():
    agent = TelegramAgent(creds={'bot_token': bot_token})
    await agent.bot.session.close()
