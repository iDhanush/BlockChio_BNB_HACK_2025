from pydantic import BaseModel, constr


class Node(BaseModel):
    type: constr(pattern='trigger|agent')
    id: str
    node_class: str
    purpose: str
    pos: dict[str, float]
    tools: list[dict[str, bool]]
    cred: dict[str, str]


class Conn(BaseModel):
    id: str
    from_node: str
    to_node: str


class WorkFlow(BaseModel):
    id: str
    user_id: str
    nodes: list[Node]
    conns: list[Conn]


