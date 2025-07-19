from pydantic import BaseModel, constr


class Node(BaseModel):
    type: constr(pattern='trigger|agent')
    node_id: str
    node_class: str
    purpose: str
    pos: dict[str, float]
    tools: list[dict[str, bool]]
    cred: dict[str, str]


class Conn(BaseModel):
    conn_id: str
    from_node: str
    to_node: str


class WorkFlow(BaseModel):
    workflow_id: str
    user_id: str
    nodes: list[Node]
    conns: list[Conn]


sample_workflow = WorkFlow(
    user_id='',
    workflow_id='wfl_OLASjlajnfJ',
    nodes=[
        Node(
            node_id="whatsapp_trigger_1",
            purpose="",
            type="trigger",
            node_class="WhatsappTrigger",
            pos={"x": 100, "y": 100},
            tools=[],
            cred={},
        ),
        Node(
            node_id="image_agent_1",
            type="agent",
            node_class="ImageAgent",
            purpose="Generate Image for the prompt given",
            pos={"x": 300, "y": 100},
            tools=[{"generate_image": True}],
            cred={},
        ),
        Node(
            node_id="telegram_agent_1",
            type="agent",
            node_class="TelegramAgent",
            purpose="if the image generated is of a cat then send it to user 868213406 else do nothing",
            pos={"x": 500, "y": 100},
            tools=[{"send_message": True}, {"send_image": True}],
            cred={},
        ),
        Node(
            node_id="whatsapp_agent_1",
            type="agent",
            node_class="WhatsappAgent",
            purpose="if the image generated is of a dog then send it to the number 9995539972 else do nothing",
            pos={"x": 500, "y": 100},
            tools=[{"send_message": True}, {"send_image": True}], cred={},
        )
    ],
    conns=[Conn(conn_id='whatsapp_trigger_1_to_image_agent_1', from_node="whatsapp_trigger_1", to_node="image_agent_1"),
           Conn(conn_id='image_agent_1_to_telegram_agent_1', from_node="image_agent_1", to_node="telegram_agent_1"),
           Conn(conn_id='image_agent_1_to_whatsapp_agent_1', from_node="image_agent_1", to_node="whatsapp_agent_1"),
           ]
)
print(sample_workflow.model_dump())
