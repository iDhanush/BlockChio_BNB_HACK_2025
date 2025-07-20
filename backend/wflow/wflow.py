import asyncio
import collections
from globar_vars import Var
from wflow.schemas import WFlow, sample_workflow, WorkFlowStatus
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
        self.node_map = {node.node_id: node for node in self.workflow.nodes}
        self.adjacency_list = collections.defaultdict(list)
        for conn in self.workflow.connections:
            self.adjacency_list[conn.from_node].append(conn.to_node)
        self.execution_results = {}
        # Initialize the status dictionary for this workflow instance
        if self.workflow.wflow_id not in Var.WORKFLOW_STATUS:
            Var.WORKFLOW_STATUS[self.workflow.wflow_id] = {}

    def _update_status(self, node_id: str, status: str, show: str = ""):
        """Helper function to update and log the status of a node."""
        Var.WORKFLOW_STATUS[self.workflow.wflow_id][node_id] = WorkFlowStatus(
            node_id=node_id,
            status=status,
            show=show
        )
        print(f"STATUS UPDATE | Node: {node_id} | Status: {status}")

    async def _execute_node(self, node_id: str, input_data: str):
        """Dynamically instantiates and runs a single agent node with status tracking."""
        try:
            # 1. Update status to 'running'
            self._update_status(node_id=node_id, status='running', show="Agent is processing...")

            node_config = self.node_map[node_id]
            agent_class = AGENT_CLASS_MAP.get(node_config.node_class)
            if not agent_class:
                raise ValueError(f"Unknown node_class: {node_config.node_class}")

            agent_instance = agent_class()

            # Configure tools dynamically
            enabled_tools = []
            for tool_config in node_config.tools:
                if tool_config.active:
                    if hasattr(agent_instance.struct_tools, tool_config.tool_func):
                        enabled_tools.append(getattr(agent_instance.struct_tools, tool_config.tool_func))
                    else:
                        print(f"Warning: Tool '{tool_config.tool_func}' not found on agent '{node_config.node_class}'")
            agent_instance.tools = enabled_tools

            query = f"previous step: '{input_data}'\n\nYour task: {node_config.purpose}"

            # 2. Run the agent
            result = await agent_instance.run(query=query)
            self.execution_results[node_id] = result

            # 3. On success, update status to 'finished'
            self._update_status(node_id=node_id, status='finished', show=str(result))
            return result

        except Exception as e:
            error_message = f"Error in node '{node_id}': {e}"
            print(error_message)
            self.execution_results[node_id] = None  # Mark result as failed

            # 4. On failure, update status to 'error'
            self._update_status(node_id=node_id, status='error', show=str(error_message))
            # Re-raise the exception to halt the workflow
            raise

    async def execute(self, initial_input: str):
        """Executes the entire workflow with robust status tracking."""
        trigger_node = next((n for n in self.workflow.nodes if n.type == 'trigger'), None)
        if not trigger_node:
            raise ValueError("No trigger node found in workflow")

        # 1. Initialize all non-trigger nodes to 'pending'
        for node in self.workflow.nodes:
            if node.type != 'trigger':
                self._update_status(node_id=node.node_id, status='pending', show="Waiting to be executed...")

        print(f"--- Starting Workflow Execution ---")
        print(f"Trigger: {trigger_node.node_id}")

        self.execution_results[trigger_node.node_id] = initial_input
        self._update_status(node_id=trigger_node.node_id, status='finished', show=initial_input)

        nodes_to_process = self.adjacency_list.get(trigger_node.node_id, [])

        # 2. Process the graph layer by layer
        while nodes_to_process:
            tasks = []
            for node_id in nodes_to_process:
                predecessor_id = next(c.from_node for c in self.workflow.connections if c.to_node == node_id)
                input_data = self.execution_results[predecessor_id]
                tasks.append(self._execute_node(node_id, input_data))

            try:
                # 3. Run all nodes in the current layer concurrently
                await asyncio.gather(*tasks)
            except Exception:
                # An error in a node was caught and status was updated.
                # Halt the entire workflow.
                print("--- Workflow Execution Halted Due to an Error ---")
                return self.execution_results

            # 4. Find the next layer of nodes whose predecessors completed successfully
            next_layer = []
            for node_id in nodes_to_process:
                if self.execution_results[node_id] is not None:
                    next_layer.extend(self.adjacency_list.get(node_id, []))

            nodes_to_process = next_layer

        print("--- Workflow Execution Finished Successfully ---")
        return self.execution_results


async def main():
    executor = WorkflowExecutor(workflow=sample_workflow)
    final_results = await executor.execute(initial_input='a cute cat')
    print("\n--- Final Results ---")
    print(final_results)
    print("\n--- Final Workflow Status ---")
    # Pretty print the final status for verification
    if executor.workflow.wflow_id in Var.WORKFLOW_STATUS:
        for node_id, status_obj in Var.WORKFLOW_STATUS[executor.workflow.wflow_id].items():
            print(f"  Node: {node_id}")
            print(f"    Status: {status_obj.status}")
            print(f"    Show: {status_obj.show[:100]}...")  # Truncate long results
            print("-" * 20)


if __name__ == "__main__":
    asyncio.run(main())
