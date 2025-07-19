import asyncio
import collections
from wflow.schemas import WFlow, sample_workflow
from agents.image_agent.image_agent import ImageAgent
from agents.whatsapp_agent.whatsapp_agent import WhatsappAgent
from agents.telegram_agent.telegram_agent import TelegramAgent
from agents.blockchain_agent.blockchain_agent import BlockchainAgent

AGENT_CLASS_MAP = {
    "ImageAgent": ImageAgent,
    "WhatsappAgent": WhatsappAgent,
    "TelegramAgent": TelegramAgent,
    'BlockchainAgent': BlockchainAgent
}


class WorkflowExecutor:
    def __init__(self, workflow: WFlow):
        self.workflow = workflow
        # Create a quick lookup map for nodes by their ID
        self.node_map = {node.node_id: node for node in self.workflow.nodes}
        # Create an adjacency list to represent the graph's connections
        self.adjacency_list = collections.defaultdict(list)
        for conn in self.workflow.connections:
            self.adjacency_list[conn.from_node].append(conn.to_node)

        self.execution_results = {}

    async def _execute_node(self, node_id: str, input_data: str):
        """Dynamically instantiates and runs a single agent node."""
        node_config = self.node_map[node_id]

        # 1. Find the correct agent class from the map
        agent_class = AGENT_CLASS_MAP.get(node_config.node_class)
        if not agent_class:
            raise ValueError(f"Unknown node_class: {node_config.node_class}")

        # 2. Instantiate the agent
        agent_instance = agent_class()

        # 3. Configure tools dynamically based on the workflow definition
        enabled_tools = []
        for tool_config in node_config.tools:
            for tool_name, is_enabled in tool_config.items():
                if is_enabled:
                    if hasattr(agent_instance.struct_tools, tool_name):
                        enabled_tools.append(getattr(agent_instance.struct_tools, tool_name))
                    else:
                        print(f"Warning: Tool '{tool_name}' not found on agent '{node_config.node_class}'")
        agent_instance.tools = enabled_tools

        # 4. Construct the query for the agent
        # We combine the output from the previous step with the node's specific purpose.
        query = f"previous step: '{input_data}'\n\nYour task: {node_config.purpose}"

        # 5. Run the agent and store its result
        result = await agent_instance.run(query=query)
        self.execution_results[node_id] = result
        return result

    async def execute(self, initial_input: str):
        """Executes the entire workflow starting from the trigger."""
        # Find the trigger node
        trigger_node = next((n for n in self.workflow.nodes if n.type == 'trigger'), None)
        if not trigger_node:
            raise ValueError("No trigger node found in workflow")

        print(f"--- Starting Workflow Execution ---")
        print(f"Trigger: {trigger_node.node_id}")
        print(f"Initial Input: {initial_input}\n")

        # The "result" of the trigger is the initial input
        self.execution_results[trigger_node.node_id] = initial_input

        # Get the first layer of nodes to process (nodes connected to the trigger)
        nodes_to_process = self.adjacency_list.get(trigger_node.node_id, [])

        # Process the graph layer by layer
        while nodes_to_process:
            tasks = []
            # For each node in the current layer, find its predecessor to get the correct input
            for node_id in nodes_to_process:
                # This assumes a simple linear chain or fan-out structure.
                # For fan-in, this logic would need to be more complex.
                predecessor_id = next(c.from_node for c in self.workflow.connections if c.to_node == node_id)
                input_data = self.execution_results[predecessor_id]
                tasks.append(self._execute_node(node_id, input_data))

            # Run all nodes in the current layer concurrently
            await asyncio.gather(*tasks)

            # Find the next layer of nodes to process
            next_layer = []
            for node_id in nodes_to_process:
                next_layer.extend(self.adjacency_list.get(node_id, []))

            nodes_to_process = next_layer

        print("--- Workflow Execution Finished ---")
        return self.execution_results

async def main():
    executor = WorkflowExecutor(workflow=sample_workflow)
    # 2. Run the execution
    final_results = await executor.execute(initial_input='a cute cat')
    print(final_results)


if __name__ == "__main__":
    asyncio.run(main())