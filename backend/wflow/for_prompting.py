from typing import Optional
from venv import create

from pydantic import BaseModel, constr

from agents.blockchain_agent.blockchain_agent import BlockchainAgent
from agents.image_agent.image_agent import ImageAgent
from agents.telegram_agent.telegram_agent import TelegramAgent
from agents.whatsapp_agent.whatsapp_agent import WhatsappAgent


class Tool(BaseModel):
    tool_func: str
    label: str
    description: str
    active: bool


class Node(BaseModel):
    type: constr(pattern='trigger|agent')
    node_id: str
    node_class: str
    purpose: str
    position: dict[str, float]
    tools: list[Tool]
    creds: list[dict[str, Optional[str]]]


class Conn(BaseModel):
    conn_id: str
    from_node: str
    to_node: str


class WFlow(BaseModel):
    wflow_id: str
    user_id: str
    wflow_name: str
    nodes: list[Node]
    connections: list[Conn]


class WFlowPayload(BaseModel):
    wflow_name: Optional[str] = None
    nodes: list[Node]
    connections: list[Conn]


class WorkFlowStatus(BaseModel):
    node_id: str
    status: str
    show: str


sample_workflow = WFlow(
    user_id='usr_xxxxxxxxxxx',
    wflow_id='wfl_OLASjlajnfJ',
    nodes=[
        Node(
            node_id="whatsapp_trigger_1",
            purpose="",
            type="trigger",
            node_class="WhatsappTrigger",
            position={"x": 100, "y": 100},
            tools=[],
            creds=[],
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
            purpose="if the image generated is of a cat then send it to user 868213406 else do nothing",
            position={"x": 500, "y": 100},
            tools=[Tool(tool_func='send_message', label='send_message', active=True, description=''),
                   Tool(tool_func='send_image', label='send_image', active=True, description='')],
            creds=[],

        ),
        Node(
            node_id="whatsapp_agent_1",
            type="agent",
            node_class="WhatsappAgent",
            purpose="if the image generated is of a dog then send it to the number 9995539972 else do nothing",
            position={"x": 500, "y": 100},
            tools=[Tool(tool_func='send_message', label='send_message', active=True, description=''),
                   Tool(tool_func='send_image', label='send_image', active=True, description='')], creds=[],
        )
    ],
    connections=[Conn(conn_id='whatsapp_trigger_1_to_image_agent_1', from_node="whatsapp_trigger_1", to_node="image_agent_1"),
           Conn(conn_id='image_agent_1_to_telegram_agent_1', from_node="image_agent_1", to_node="telegram_agent_1"),
           Conn(conn_id='image_agent_1_to_whatsapp_agent_1', from_node="image_agent_1", to_node="whatsapp_agent_1"),
           ]
)
AGENT_CLASS_MAP = {
    "ImageAgent": ImageAgent,
    "WhatsappAgent": WhatsappAgent,
    "TelegramAgent": TelegramAgent,
    'BlockchainAgent': BlockchainAgent
}


# sample function for running workflowsa
async def workflow_runner(runnable_workflow: RunnableWorkflow, trigger: str, query):
    # run the workflow according to the trigger
    # agent = get the starting node which is after the trigger
    query: str = query + node.purpose  # add the purpose to the query
    res = await agent.run(query)
    query = res + purpose  # add the purpose to the response of the agent then pass it to next agent
    res = await next_agent.run(query)

    query = res + purpose  # add the purpose to the response of the agent then pass it to next agent
    res = await next_agent.run(query)
    # repeat until the end is reached
    # then return the final res
    return res


async def on_execute(wflow: WFlow):
    # agents = find all nodes with node.type=agent
    agents: list[Node]
    for agent in agents:
        agent_class_name = agent.node_class
        agent_class = AGENT_CLASS_MAP.get(agent_class_name)
        agent_obj = agent_class(creds=agent.creds)
        for tool in agent.tools:
            # tool will be a string and i want to get it using struct_tools.{tool}
            agent_obj.tools = agent_obj.struct_tools.str(tool.tool_func)
    # triggers = find all triggers with node.type=trigger
    # eg: WhatsAppTrigger, TelegramTrigger, WebChatTrigger
    triggers: list[Node]
    for trigger in triggers:
        trigger_class_name = trigger.node_class
    # then use the new initialised nodes to create a new RunnableWorkFlow with necessary data
    # then set the trigger for the runnable work flow appropriatly
    # there may be multiple workflows so do plan accordingly
    for trigger in triggers:
        trigger_class_name = trigger.node_class
        set_trigger(workflow=runnable_workflow, trigger=trigger)


async def on_example_trigger(workflow_id, query):
    # runnable_workflow =  get workflow from id
    # run the workflow based on the trigger
    res = workflow_runner(runnable_workflow, trigger, query)
    return await respond_trigger(res)


sample_workflow = WFlow(
    user_id='usr_xxxxxxxxxxx',
    wflow_id='wfl_OLASjlajnfJ',
    nodes=[
        Node(
            node_id="whatsapp_trigger_1",
            purpose="",
            type="trigger",
            node_class="WhatsappTrigger",
            position={"x": 100, "y": 100},
            tools=[],
            creds=[],
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
            purpose="if the image generated is of a cat then send it to user 868213406 else do nothing",
            position={"x": 500, "y": 100},
            tools=[Tool(tool_func='send_message', label='send_message', active=True, description=''),
                   Tool(tool_func='send_image', label='send_image', active=True, description='')],
            creds=[],

        ),
        Node(
            node_id="whatsapp_agent_1",
            type="agent",
            node_class="WhatsappAgent",
            purpose="if the image generated is of a dog then send it to the number 9995539972 else do nothing",
            position={"x": 500, "y": 100},
            tools=[Tool(tool_func='send_message', label='send_message', active=True, description=''),
                   Tool(tool_func='send_image', label='send_image', active=True, description='')], creds=[],
        )
    ],
    connections=[Conn(conn_id='whatsapp_trigger_1_to_image_agent_1', from_node="whatsapp_trigger_1", to_node="image_agent_1"),
           Conn(conn_id='image_agent_1_to_telegram_agent_1', from_node="image_agent_1", to_node="telegram_agent_1"),
           Conn(conn_id='image_agent_1_to_whatsapp_agent_1', from_node="image_agent_1", to_node="whatsapp_agent_1"),
           ]
)

# print(sample_workflow.model_dump())
sample_workflow2 = WFlow(
    wflow_name='str',
    user_id='asdads',
    wflow_id='wfl_OLASjlajnfJ',
    nodes=[
        Node(
            node_id="whatsapp_trigger_1",
            purpose="",
            type="trigger",
            node_class="WhatsappTrigger",
            position={"x": 100, "y": 100},
            tools=[],
            creds=[],
        ),
        Node(
            node_id="telegram_agent_1",
            type="agent",
            node_class="TelegramAgent",
            purpose="if the image generated is of a cat then send it to user 868213406 else do nothing",
            position={"x": 500, "y": 100},
            tools=[Tool(tool_func="send_message", label="asdasd",
                        description="dedsa", active=True), Tool(tool_func="send_image", label="asdasd",
                                                                description="dedsa", active=True)],
            creds=[{
                "bot_token": "1765542474:AAHpERwNgs7o9_qkxmkaDqwOhN5T9efmSSs"
            }],
        ),

    ],
    connections=[
        Conn(conn_id='telegram_trigger_1_to_image_agent_1', from_node="whatsapp_trigger_1", to_node="image_agent_1"),
        Conn(conn_id='image_agent_1_to_telegram_agent_1', from_node="image_agent_1", to_node="telegram_agent_1"),
        Conn(conn_id='image_agent_1_to_whatsapp_agent_1', from_node="image_agent_1", to_node="whatsapp_agent_1"),
    ]
)

data = {
    "nodes": [
        {
            "node_id": "whatsapp_trigger",
            "type": "trigger",
            "label": "WhatsApp",
            "icon": {},
            "color": "green",
            "node_class": "WhatsappTrigger",
            "creds": [],
            "tools": [],
            "purpose": "",
            "id": "whatsapp_trigger_1",
            "position": {
                "x": 151.75424194335938,
                "y": 112.43037414550781
            }
        },
        {
            "node_id": "image_generation_agent",
            "type": "agent",
            "label": "Image Generation",
            "icon": {},
            "color": "red",
            "node_class": "ImageAgent",
            "creds": [],
            "tools": [
                {
                    "label": "Generate Image",
                    "description": "Generate an image",
                    "tool_func": "generate_image",
                    "active": True
                }
            ],
            "purpose": "",
            "id": "image_generation_agent_1",
            "position": {
                "x": 348.2485656738281,
                "y": 215.34800720214844
            }
        },
        {
            "node_id": "telegram_agent",
            "type": "agent",
            "label": "Telegram Agent",
            "icon": {},
            "color": "blue",
            "node_class": "TelegramAgent",
            "creds": [
                {
                    "bot_token": "1765542474:AAHpERwNgs7o9_qkxmkaDqwOhN5T9efmSSs"
                }
            ],
            "tools": [
                {
                    "label": "Send Message",
                    "description": "Send a transaction",
                    "tool_func": "send_message",
                    "active": True
                },
                {
                    "label": "Send Image",
                    "description": "Send a transaction",
                    "tool_func": "send_image",
                    "active": True
                }
            ],
            "purpose": "",
            "id": "telegram_agent_1",
            "position": {
                "x": 731.0823669433594,
                "y": 201.3252716064453
            }
        }
    ],
    "connections": [
        {
            "conn_id": "whatsapp_trigger_1_to_image_generation_agent_1_1752952157322",
            "from_node": "whatsapp_trigger_1",
            "to_node": "image_generation_agent_1"
        },
        {
            "conn_id": "image_generation_agent_1_to_telegram_agent_1_1752952164708",
            "from_node": "image_generation_agent_1",
            "to_node": "telegram_agent_1"
        }
    ]
}
wpay = WFlowPayload(**{
    'wflow_name': 'name',
    "nodes": [
        {
            "node_id": "manual_trigger",
            "type": "trigger",
            "label": "Manual Trigger",
            "icon": {},
            "color": "gray",
            "node_class": "ManualTrigger",
            "creds": [],
            "tools": [],
            "purpose": "send a message to 868213406",
            "id": "manual_trigger_1",
            "position": {
                "x": 105.586669921875,
                "y": 134.2755584716797
            }
        },
        {
            "node_id": "telegram_agent_1",
            "type": "agent",
            "label": "Telegram Agent",
            "icon": {},
            "color": "blue",
            "node_class": "TelegramAgent",
            "creds": [
                {
                    "bot_token": "1765542474:AAHpERwNgs7o9_qkxmkaDqwOhN5T9efmSSs"
                }
            ],
            "tools": [
                {
                    "label": "Send Message",
                    "description": "Send a transaction",
                    "tool_func": "send_message",
                    "active": True
                },
                {
                    "label": "Send Image",
                    "description": "Send a transaction",
                    "tool_func": "send_image",
                    "active": True
                }
            ],
            "purpose": "send hi to 868213405",
            "id": "telegram_agent_1",
            "position": {
                "x": 394.0909118652344,
                "y": 222.54969787597656
            }
        }
    ],
    "connections": [
        {
            "conn_id": "manual_trigger_1_to_telegram_agent_1_1752997287620",
            "from_node": "manual_trigger_1",
            "to_node": "telegram_agent_1"
        }
    ]
})
k = WFlow(**wpay.model_dump(), user_id='asdas', wflow_id='asdasd')
