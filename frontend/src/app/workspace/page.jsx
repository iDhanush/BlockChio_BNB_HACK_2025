"use client";
import "./workspace.scss";

const page = () => {
  return (
    <div className="workspace-sec">
      <div className="no-projects">
        <div className="sec-head">Your WorkFlow</div>
        <div className="sec-txt">
          Start building powerful AI workflows by<br></br> adding your first
          project.
        </div>
        <div className="add-project-btn">
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
