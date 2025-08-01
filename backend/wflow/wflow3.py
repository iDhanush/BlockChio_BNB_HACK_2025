import asyncio

from agents.image_agent.image_agent import ImageAgent
from agents.whatsapp_agent.whatsapp_agent import WhatsappAgent
from agents.telegram_agent.telegram_agent import TelegramAgent
from triggers.telegram_trigger import TelegramTrigger, BaseTrigger
from wflow.schemas import Node, Tool, WFlow, Conn

# ----------------------- Mapping -----------------------

AGENT_CLASS_MAP = {
    "ImageAgent": ImageAgent,
    "WhatsappAgent": WhatsappAgent,
    "TelegramAgent": TelegramAgent,
    # 'BlockchainAgent': BlockchainAgent
}
TRIGGER_CLASS_MAP = {
    "TelegramTrigger": TelegramTrigger,
    # "WhatsappTrigger": WhatsappTrigger (implement similar if needed)
}

# ----------------------- Runnable Classes -----------------------

class RunnableNode:
    def __init__(self, node: Node):
        self.node_id = node.node_id
        self.node = node
        agent_class = AGENT_CLASS_MAP[node.node_class]
        self.agent = agent_class(creds=node.creds)
        self.purpose = node.purpose
        for tool in node.tools:
            tool_func = tool.tool_func
            is_enabled = tool.active
            if is_enabled:
                if hasattr(self.agent.struct_tools, tool_func):
                    self.agent.tools.append(getattr(self.agent.struct_tools, tool_func))
                else:
                    print(f"Warning: Tool '{tool_func}' not found on agent '{node.node_class}'")
        print('initialized', node.node_class)

    async def run(self, input_text: str):
        return await self.agent.run(f"previously done: {input_text}\n\n\nYour Task: {self.purpose}")


class RunnableWorkflow:
    def __init__(self, wflow: WFlow):
        self.wflow_id = wflow.wflow_id
        self.nodes: dict[str, RunnableNode] = {
            node.node_id: RunnableNode(node)
            for node in wflow.nodes if node.type == "agent"
        }
        self.triggers: dict[str, BaseTrigger] = {
            node.node_id: TRIGGER_CLASS_MAP[node.node_class](node, wflow, workflow_registry)
            for node in wflow.nodes if node.type == "trigger"
        }
        self.conn_map = self._build_conn_map(wflow.connections)

    def _build_conn_map(self, connections: list[Conn]) -> dict[str, list[str]]:
        conn_map = {}
        for conn in connections:
            conn_map.setdefault(conn.from_node, []).append(conn.to_node)
        return conn_map

    async def run(self, trigger_node_id: str, query: str):
        next_nodes = self.conn_map.get(trigger_node_id, [])
        current_input = query
        for node_id in next_nodes:
            current_input = await self._run_chain(node_id, current_input)
        return current_input

    async def _run_chain(self, node_id: str, current_input: str):
        node = self.nodes[node_id]
        result = await node.run(current_input)
        next_nodes = self.conn_map.get(node_id, [])
        for next_node in next_nodes:
            result = await self._run_chain(next_node, result)
        return result


# ----------------------- Execution & Trigger -----------------------

workflow_registry: dict[str, RunnableWorkflow] = {}


async def on_execute(wflow: WFlow):
    runnable = RunnableWorkflow(wflow)
    workflow_registry[wflow.wflow_id] = runnable
    print(f"Workflow {wflow.wflow_id} initialized.")

    # Start all triggers
    for trigger in runnable.triggers.values():
        await trigger.start()

async def on_example_trigger(workflow_id: str, query: str):
    runnable_workflow = workflow_registry[workflow_id]
    trigger_node_id = next(iter(runnable_workflow.triggers.keys()))
    final_output = await runnable_workflow.run(trigger_node_id, query)
    return final_output


# ----------------------- Example -----------------------

sample_workflow = WFlow(
    user_id='usr_OLASjlajnfJ',
    wflow_id='wfl_OLASjlajnfJ',
    wflow_name="Animal Image Workflow",
    nodes=[
        Node(
            node_id="telegram_trigger_1",
            purpose="",
            type="trigger",
            node_class="TelegramTrigger",
            position={"x": 100, "y": 100},
            tools=[],
            creds=[{"bot_token": "1765542474:AAHpERwNgs7o9_qkxmkaDqwOhN5T9efmSSs"}],
        ),
        Node(
            node_id="image_agent_1",
            type="agent",
            node_class="ImageAgent",
            purpose="Generate Image for the prompt given",
            position={"x": 300, "y": 100},
            tools=[Tool(tool_func='generate_image', label='generate_image', active=True, description='')],
            creds=[],
        ),
        Node(
            node_id="telegram_agent_1",
            type="agent",
            node_class="TelegramAgent",
            purpose="if the prompt given by the user is of a cat then send it to user 868213406 else do nothing",
            position={"x": 500, "y": 100},
            tools=[
                Tool(tool_func='send_message', label='send_message', active=True, description=''),
                Tool(tool_func='send_image', label='send_image', active=True, description='')
            ],
            creds=[{"bot_token": "1765542474:AAHpERwNgs7o9_qkxmkaDqwOhN5T9efmSSs"}],
        ),
        Node(
            node_id="whatsapp_agent_1",
            type="agent",
            node_class="WhatsappAgent",
            purpose="if the prompt given by the user is of a dog then send it to user 9995539972 else do nothing",
            position={"x": 500, "y": 100},
            tools=[
                Tool(tool_func='send_message', label='send_message', active=True, description=''),
                Tool(tool_func='send_image', label='send_image', active=True, description='')
            ],
            creds=[],
        )
    ],
    connections=[
        Conn(conn_id='telegram_trigger_1_to_image_agent_1', from_node="telegram_trigger_1", to_node="image_agent_1"),
        Conn(conn_id='image_agent_1_to_telegram_agent_1', from_node="image_agent_1", to_node="telegram_agent_1"),
        # Conn(conn_id='image_agent_1_to_whatsapp_agent_1', from_node="image_agent_1", to_node="whatsapp_agent_1"),
    ]
)
asyncio.run(on_execute(sample_workflow))
# asyncio.run(on_example_trigger(workflow_id=sample_workflow.wflow_id, query='a cute cat'))
asyncio.run(asyncio.sleep(1000))