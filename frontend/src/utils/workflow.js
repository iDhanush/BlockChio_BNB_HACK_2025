import axios from "axios";
import { baseUrl } from "@/constants";

export async function updateWflow(wflowId, data) {
  try {
    const response = await axios.put(`${baseUrl}/wflow/${wflowId}`, data, {
      withCredentials: true,
    });
    console.log(response);
    return response;
  } catch (error) {
    console.log(
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
    console.log(
      "Failed to fetch workflow:",
      error.response?.data || error.message
    );
  }
}
