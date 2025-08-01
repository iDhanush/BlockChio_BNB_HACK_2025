from typing import Optional, Dict, Any, List
import asyncio
from abc import ABC, abstractmethod
from pydantic import BaseModel, constr
import logging

# from agents.blockchain_agent.blockchain_agent import BlockchainAgent
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


class WorkflowExecution(BaseModel):
    """Tracks the execution state of a workflow"""
    workflow_id: str
    execution_id: str
    status: str  # 'running', 'completed', 'failed', 'waiting'
    current_node: Optional[str] = None
    context: Dict[str, Any] = {}
    error: Optional[str] = None


class BaseTrigger(ABC):
    """Base class for all triggers"""

    def __init__(self, node: Node, workflow_runner):
        self.node = node
        self.workflow_runner = workflow_runner
        self.is_active = False

    @abstractmethod
    async def start(self):
        """Start listening for trigger events"""
        pass

    @abstractmethod
    async def stop(self):
        """Stop listening for trigger events"""
        pass

    async def on_trigger(self, query: str, context: Dict[str, Any] = None):
        """Called when trigger event occurs"""
        if context is None:
            context = {}

        logging.info(f"Trigger {self.node.node_id} activated with query: {query}")
        await self.workflow_runner.execute_from_trigger(self.node.node_id, query, context)


class WhatsappTrigger(BaseTrigger):
    """WhatsApp trigger implementation"""

    async def start(self):
        self.is_active = True
        logging.info(f"WhatsApp trigger {self.node.node_id} started")
        # Initialize WhatsApp webhook listener here

    async def stop(self):
        self.is_active = False
        logging.info(f"WhatsApp trigger {self.node.node_id} stopped")


class TelegramTrigger(BaseTrigger):
    """Telegram trigger implementation"""

    async def start(self):
        self.is_active = True
        logging.info(f"Telegram trigger {self.node.node_id} started")
        # Initialize Telegram bot listener here

    async def stop(self):
        self.is_active = False
        logging.info(f"Telegram trigger {self.node.node_id} stopped")


class RunnableWorkflow:
    """Represents a workflow ready for execution"""

    def __init__(self, workflow: WFlow):
        self.workflow = workflow
        self.agents: Dict[str, Any] = {}
        self.triggers: Dict[str, BaseTrigger] = {}
        self.node_map: Dict[str, Node] = {node.node_id: node for node in workflow.nodes}
        self.connection_map: Dict[str, List[str]] = {}
        self._build_connection_map()

    def _build_connection_map(self):
        """Build a map of node connections for easy traversal"""
        for conn in self.workflow.connections:
            if conn.from_node not in self.connection_map:
                self.connection_map[conn.from_node] = []
            self.connection_map[conn.from_node].append(conn.to_node)

    def get_next_nodes(self, node_id: str) -> List[str]:
        """Get the next nodes connected to the given node"""
        return self.connection_map.get(node_id, [])

    def get_trigger_nodes(self) -> List[Node]:
        """Get all trigger nodes"""
        return [node for node in self.workflow.nodes if node.type == "trigger"]

    def get_agent_nodes(self) -> List[Node]:
        """Get all agent nodes"""
        return [node for node in self.workflow.nodes if node.type == "agent"]


class WorkflowRunner:
    """Manages workflow execution"""

    AGENT_CLASS_MAP = {
        "ImageAgent": ImageAgent,
        "WhatsappAgent": WhatsappAgent,
        "TelegramAgent": TelegramAgent,
        # "BlockchainAgent": BlockchainAgent
    }

    TRIGGER_CLASS_MAP = {
        "WhatsappTrigger": WhatsappTrigger,
        "TelegramTrigger": TelegramTrigger,
    }

    def __init__(self):
        self.active_workflows: Dict[str, RunnableWorkflow] = {}
        self.executions: Dict[str, WorkflowExecution] = {}

    async def initialize_workflow(self, workflow: WFlow) -> RunnableWorkflow:
        """Initialize a workflow with all its agents and triggers"""
        runnable_workflow = RunnableWorkflow(workflow)

        # Initialize agents
        for node in runnable_workflow.get_agent_nodes():
            agent_class = self.AGENT_CLASS_MAP.get(node.node_class)
            if not agent_class:
                raise ValueError(f"Unknown agent class: {node.node_class}")

            agent_obj = agent_class(creds=node.creds)

            # Configure tools for the agent
            active_tools = []
            for tool in node.tools:
                if tool.active:
                    # Get the tool function from agent's struct_tools
                    if hasattr(agent_obj, 'struct_tools'):
                        tool_func = getattr(agent_obj.struct_tools, tool.tool_func, None)
                        if tool_func:
                            active_tools.append(tool_func)

            agent_obj.active_tools = active_tools
            runnable_workflow.agents[node.node_id] = agent_obj

        # Initialize triggers
        for node in runnable_workflow.get_trigger_nodes():
            trigger_class = self.TRIGGER_CLASS_MAP.get(node.node_class)
            if not trigger_class:
                raise ValueError(f"Unknown trigger class: {node.node_class}")

            trigger_obj = trigger_class(node, self)
            runnable_workflow.triggers[node.node_id] = trigger_obj

        return runnable_workflow

    async def start_workflow(self, workflow: WFlow):
        """Start a workflow and begin listening for triggers"""
        runnable_workflow = await self.initialize_workflow(workflow)
        self.active_workflows[workflow.wflow_id] = runnable_workflow

        # Start all triggers
        for trigger in runnable_workflow.triggers.values():
            await trigger.start()

        logging.info(f"Workflow {workflow.wflow_id} started successfully")

    async def stop_workflow(self, workflow_id: str):
        """Stop a workflow and its triggers"""
        if workflow_id in self.active_workflows:
            runnable_workflow = self.active_workflows[workflow_id]

            # Stop all triggers
            for trigger in runnable_workflow.triggers.values():
                await trigger.stop()

            del self.active_workflows[workflow_id]
            logging.info(f"Workflow {workflow_id} stopped")

    async def execute_from_trigger(self, trigger_node_id: str, query: str, context: Dict[str, Any]):
        """Execute workflow starting from a trigger"""
        # Find the workflow containing this trigger
        workflow = None
        for wf in self.active_workflows.values():
            if trigger_node_id in wf.triggers:
                workflow = wf
                break

        if not workflow:
            logging.error(f"No active workflow found for trigger {trigger_node_id}")
            return

        # Get the first agent node connected to the trigger
        next_nodes = workflow.get_next_nodes(trigger_node_id)
        if not next_nodes:
            logging.warning(f"No nodes connected to trigger {trigger_node_id}")
            return

        execution_id = f"exec_{workflow.workflow.wflow_id}_{len(self.executions)}"
        execution = WorkflowExecution(
            workflow_id=workflow.workflow.wflow_id,
            execution_id=execution_id,
            status="running",
            context=context
        )
        self.executions[execution_id] = execution

        try:
            # Execute the workflow chain
            result = await self._execute_node_chain(workflow, next_nodes[0], query, execution)
            execution.status = "completed"
            logging.info(f"Workflow execution {execution_id} completed successfully")
            return result

        except Exception as e:
            execution.status = "failed"
            execution.error = str(e)
            logging.error(f"Workflow execution {execution_id} failed: {e}")
            raise

    async def _execute_node_chain(self, workflow: RunnableWorkflow, node_id: str, query: str,
                                  execution: WorkflowExecution):
        """Execute a chain of nodes starting from the given node"""
        current_query = query
        current_node_id = node_id

        while current_node_id:
            execution.current_node = current_node_id
            node = workflow.node_map[current_node_id]

            if node.type == "agent":
                agent = workflow.agents.get(current_node_id)
                if not agent:
                    raise ValueError(f"Agent {current_node_id} not found")

                # Combine query with node purpose
                enhanced_query = f"{current_query}\n\nPurpose: {node.purpose}"

                logging.info(f"Executing agent {current_node_id} with query: {enhanced_query}")

                # Execute the agent
                result = await agent.run(enhanced_query)

                # Store result in execution context
                execution.context[current_node_id] = result
                current_query = result

                # Get next nodes
                next_nodes = workflow.get_next_nodes(current_node_id)

                if len(next_nodes) == 0:
                    # End of workflow
                    return result
                elif len(next_nodes) == 1:
                    # Single path - continue
                    current_node_id = next_nodes[0]
                else:
                    # Multiple paths - execute in parallel
                    tasks = []
                    for next_node_id in next_nodes:
                        task = self._execute_node_chain(workflow, next_node_id, current_query, execution)
                        tasks.append(task)

                    results = await asyncio.gather(*tasks, return_exceptions=True)

                    # Return the first successful result or raise if all failed
                    for result in results:
                        if not isinstance(result, Exception):
                            return result

                    # If we get here, all parallel executions failed
                    raise Exception("All parallel executions failed")
            else:
                raise ValueError(f"Unexpected node type: {node.type}")

        return current_query


# Enhanced workflow management
class WorkflowManager:
    """High-level workflow management"""

    def __init__(self):
        self.runner = WorkflowRunner()
        self.workflows: Dict[str, WFlow] = {}

    async def deploy_workflow(self, workflow: WFlow):
        """Deploy and start a workflow"""
        self.workflows[workflow.wflow_id] = workflow
        await self.runner.start_workflow(workflow)

    async def undeploy_workflow(self, workflow_id: str):
        """Stop and remove a workflow"""
        await self.runner.stop_workflow(workflow_id)
        if workflow_id in self.workflows:
            del self.workflows[workflow_id]

    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get the status of a workflow"""
        if workflow_id not in self.active_workflows:
            return {"status": "not_found"}

        return {
            "status": "active",
            "triggers_active": len(self.runner.active_workflows[workflow_id].triggers),
            "agents_initialized": len(self.runner.active_workflows[workflow_id].agents)
        }


# Example usage
async def main():
    # Sample workflow from your code
    sample_workflow = WFlow(
        user_id='usr_xxxxxxxxxxx',
        wflow_id='wfl_OLASjlajnfJ',
        wflow_name='Image Processing Workflow',
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
                tools=[Tool(tool_func='generate_image', label='generate_image', active=True,
                            description='Generate images from text prompts')],
                creds=[],
            ),
            Node(
                node_id="telegram_agent_1",
                type="agent",
                node_class="TelegramAgent",
                purpose="if the image generated is of a cat then send it to user 868213406 else do nothing",
                position={"x": 500, "y": 100},
                tools=[
                    Tool(tool_func='send_message', label='send_message', active=True, description='Send text messages'),
                    Tool(tool_func='send_image', label='send_image', active=True, description='Send images')
                ],
                creds=[],
            ),
            Node(
                node_id="whatsapp_agent_1",
                type="agent",
                node_class="WhatsappAgent",
                purpose="if the image generated is of a dog then send it to the number 9995539972 else do nothing",
                position={"x": 500, "y": 200},
                tools=[
                    Tool(tool_func='send_message', label='send_message', active=True, description='Send text messages'),
                    Tool(tool_func='send_image', label='send_image', active=True, description='Send images')
                ],
                creds=[],
            )
        ],
        connections=[
            Conn(conn_id='whatsapp_trigger_1_to_image_agent_1', from_node="whatsapp_trigger_1",
                 to_node="image_agent_1"),
            Conn(conn_id='image_agent_1_to_telegram_agent_1', from_node="image_agent_1", to_node="telegram_agent_1"),
            Conn(conn_id='image_agent_1_to_whatsapp_agent_1', from_node="image_agent_1", to_node="whatsapp_agent_1"),
        ]
    )

    # Initialize workflow manager
    manager = WorkflowManager()

    # Deploy the workflow
    await manager.deploy_workflow(sample_workflow)

    # The workflow is now running and listening for WhatsApp triggers
    print("Workflow deployed and active!")


if __name__ == "__main__":
    asyncio.run(main())