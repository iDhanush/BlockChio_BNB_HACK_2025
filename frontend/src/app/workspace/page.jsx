"use client";
import { useEffect, useState } from "react"; // Import useState
import { useRouter } from "next/navigation";
import "./workspace.scss";
import axios from "axios";
import { baseUrl } from "@/constants";
import { getAllWorkflow } from "@/utils/workflow";
import Link from "next/link";

const Page = () => {
  const router = useRouter();
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [workflowName, setWorkflowName] = useState("");
  const [error, setError] = useState("");
  const [workflows, setWorkflows] = useState(null);

  // This function now just opens the popup
  const handleNewProjectClick = () => {
    setError(""); // Clear previous errors
    setWorkflowName(""); // Reset input field
    setIsPopupOpen(true);
  };

  // This function handles the actual project creation
  const handleCreateProject = async () => {
    if (!workflowName.trim()) {
      setError("Workflow name cannot be empty.");
      return;
    }
    setError(""); // Clear error if validation passes

    try {
      const response = await axios.post(
        `${baseUrl}/wflow/`,
        {
          wflow_name: workflowName, // Send the workflow name
          nodes: [],
          connections: [],
        },
        {
          withCredentials: true,
        }
      );

      console.log("Project Created:", response.data.wflow_id);
      setIsPopupOpen(false); // Close popup on success
      router.push(`/workspace/${response.data.wflow_id}`);
    } catch (err) {
      console.error("Error creating project:", err);
      setError("Failed to create project. Please try again.");
    }
  };

  // Close the popup
  const handleClosePopup = () => {
    setIsPopupOpen(false);
  };

  useEffect(() => {
    const fetchData = async () => {
      const res = await getAllWorkflow();
      if (res) {
        setWorkflows(res?.wflow_list);
      }
    };
    fetchData();
  }, []);
  console.log(workflows);

  return (
    <>
      <div className="workspace-sec">
        <div className="no-projects">
          <div className="sec-head">Your WorkFlow</div>
          <div className="sec-txt">
            Start building powerful AI workflows by
            <br /> adding your first project.
          </div>
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
          {workflows?.length > 0 && (
            <div className="workflow-cards">
              <div className="cards-head">Recent Workflows</div>
              {workflows?.map(
                (item) =>
                  item?.wflow_name != null && (
                    <Link
                      key={item?.wflow_id}
                      href={`/workspace/${item?.wflow_id}`}
                      className="workflow-card"
                    >
                      {item?.wflow_name}
                    </Link>
                  )
              )}
            </div>
          )}
        </div>
      </div>

      {/* --- Popup Modal --- */}
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
