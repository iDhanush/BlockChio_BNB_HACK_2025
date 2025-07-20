"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import "./marketplace.scss";
import axios from "axios";
import TopNav from "@/components/TopNav/TopNav";
import Image from "next/image";
// Assuming baseUrl is defined in your constants file
// import { baseUrl } from "@/constants";

import TMP from "../../../public/assets/temp.png";
import Link from "next/link";

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
      <TopNav />
      <div className="market-sec">
        <div className="top-sec">
          <div className="left-sec">
            <div className="sec-head">
              Build Smarter with Decentralized AI Agent Templates
            </div>
            <div className="sec-txt">
              Explore reusable agents, forkable flows, and launch-ready AI
              setups.
            </div>
            <div className="hero-btns">
              <Link href="/marketplace" className="view-btn">
                View Templates
              </Link>
              <Link href="/workspace" className="workflow-btn">
                Build Now
              </Link>
            </div>
          </div>
          <div className="right-sec">
            <Image className="right-sec-img" src={TMP} alt="img" />
          </div>
        </div>

        <div className="workflow-cards">
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
    </>
  );
};

export default Page;
