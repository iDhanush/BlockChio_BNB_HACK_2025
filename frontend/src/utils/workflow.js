import axios from "axios";
import { baseUrl } from "@/constants";

export async function updateWflow(wflowId, data) {
  try {
    const response = await axios.put(`${baseUrl}/wflow/${wflowId}`, data, {
      withCredentials: true,
    });
    console.log("Workflow updated:", response.data);
    return response.data; // Returning data is often more useful
  } catch (error) {
    console.error(
      "Failed to update workflow:",
      error.response?.data || error.message
    );
  }
}

export async function getWflow(wflowId) {
  try {
    const response = await axios.get(`${baseUrl}/wflow/${wflowId}`, {
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    console.error(
      "Failed to fetch workflow:",
      error.response?.data || error.message
    );
  }
}

export async function executeWflow(wflowId, workflowData) {
  try {
    // A POST request to an 'execute' endpoint is a common pattern for this action.
    const response = await axios.post(
      `${baseUrl}/wflow/${wflowId}/execute`,
      workflowData,
      {
        withCredentials: true,
      }
    );
    console.log("Execution started:", response.data);
    return response;
  } catch (error) {
    console.error(
      "Failed to start execution:",
      error.response?.data || error.message
    );
  }
}

export async function getExecutionStatus(executionId) {
  try {
    // A GET request to a 'status' endpoint for a specific execution ID.
    const response = await axios.get(
      `${baseUrl}/wflow/execution/${executionId}/status`,
      {
        withCredentials: true,
      }
    );
    return response.data; // Expected to return { status: "...", message: "..." }
  } catch (error) {
    console.error(
      "Failed to get execution status:",
      error.response?.data || error.message
    );
  }
}

export async function getAllWorkflow() {
  try {
    // A GET request to a 'status' endpoint for a specific execution ID.
    const response = await axios.get(`${baseUrl}/wflow/all/list`, {
      withCredentials: true,
    });
    return response.data; // Expected to return { status: "...", message: "..." }
  } catch (error) {
    console.error(
      "Failed to get execution status:",
      error.response?.data || error.message
    );
  }
}
