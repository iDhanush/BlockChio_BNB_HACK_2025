"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import "./marketplace.scss";
import axios from "axios";
// Assuming baseUrl is defined in your constants file
// import { baseUrl } from "@/constants";

// Mock baseUrl for demonstration purposes
const baseUrl = "https://api.example.com";

const Page = () => {
  const router = useRouter();
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [workflowName, setWorkflowName] = useState("");
  const [error, setError] = useState("");
  const [workflows, setWorkflows] = useState([]);

  // Mock data for workflows
  const mockWorkflows = [
    { id: 1, name: "Customer Support Bot", author: "AI Solutions" },
    { id: 2, name: "Data Analysis Pipeline", author: "Data Corp" },
    { id: 3, name: "Social Media Manager", author: "Connect Inc." },
    { id: 4, name: "E-commerce Automation", author: "Shopify Experts" },
  ];

  useEffect(() => {
    // In a real application, you would fetch this data from your API
    // For now, we're using mock data
    setWorkflows(mockWorkflows);
  }, []);

  const handleNewProjectClick = () => {
    setError("");
    setWorkflowName("");
    setIsPopupOpen(true);
  };

  const handleCreateProject = async () => {
    if (!workflowName.trim()) {
      setError("Workflow name cannot be empty.");
      return;
    }
    setError("");

    try {
      // This is where you would make the API call
      // const response = await axios.post(
      //   `${baseUrl}/wflow/`,
      //   {
      //     wflow_name: workflowName,
      //     nodes: [],
      //     connections: [],
      //   },
      //   {
      //     withCredentials: true,
      //   }
      // );
      // console.log("Project Created:", response.data.wflow_id);

      // For demonstration, we'll just add to our mock data
      const newWorkflow = {
        id: workflows.length + 1,
        name: workflowName,
        author: "You",
      };
      setWorkflows([...workflows, newWorkflow]);

      setIsPopupOpen(false);
      // router.push(`/workspace/${response.data.wflow_id}`);
    } catch (err) {
      console.error("Error creating project:", err);
      setError("Failed to create project. Please try again.");
    }
  };

  const handleClosePopup = () => {
    setIsPopupOpen(false);
  };

  return (
    <>
      <div className="workspace-sec">
        <div className="sec-head">Your Workflows</div>
        <div className="sec-txt">
          Explore your existing AI workflows or start a new one.
        </div>
        <div className="workflow-cards">
          {/* Add Project Button Card */}
          <div className="add-project-btn" onClick={handleNewProjectClick}>
            <div className="add-icon">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width={27}
                height={26}
                fill="none"
              >
                <path
                  stroke="#F3F4F5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={3}
                  d="M13.5 1.5v23M2 13h23"
                />
              </svg>
            </div>
            <div className="btn-txt">New Project</div>
          </div>

          {/* Workflow Cards */}
          {workflows.map((flow) => (
            <div key={flow.id} className="workflow-card">
              <div className="card-content">
                <h3 className="card-title">{flow.name}</h3>
                <p className="card-author">by {flow.author}</p>
              </div>
              <div className="card-actions">
                <button className="btn-view">View</button>
                <button className="btn-buy">Buy Now</button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {isPopupOpen && (
        <div className="popup-overlay" onClick={handleClosePopup}>
          <div className="popup-content" onClick={(e) => e.stopPropagation()}>
            <h2>Create New Workflow</h2>
            <p>Enter a name for your new workflow project.</p>
            <input
              type="text"
              placeholder="e.g., Customer Support Bot"
              value={workflowName}
              onChange={(e) => setWorkflowName(e.target.value)}
              autoFocus
            />
            {error && <div className="popup-error">{error}</div>}
            <div className="popup-actions">
              <button onClick={handleClosePopup} className="btn-cancel">
                Cancel
              </button>
              <button onClick={handleCreateProject} className="btn-create">
                Create Project
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Page;
