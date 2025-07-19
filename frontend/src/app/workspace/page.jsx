"use client";
import { useRouter } from "next/navigation";
import "./workspace.scss";
import axios from "axios";
import { baseUrl } from "@/constants";

const page = () => {
  const router = useRouter();

  const handleNewProjectClick = async () => {
    try {
      const response = await axios.post(
        `${baseUrl}/wflow/`,
        {
          nodes: [],
          conns: [],
        },
        {
          withCredentials: true,
        }
      );

      console.log("Project Created:", response.data.wflow_id);
      router.push(`/workspace/${response.data.wflow_id}`);
      // You can navigate or show success UI here
    } catch (error) {
      console.error("Error creating project:", error);
    }
  };

  return (
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
      </div>
    </div>
  );
};

export default page;
