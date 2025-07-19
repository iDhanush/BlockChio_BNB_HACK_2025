"use client";
import TopNav from "@/components/TopNav/TopNav";
import "./app.scss";

const page = () => {
  return (
    <div className="home">
      <div className="hero">
        <TopNav />
        <div className="hero-sec">
          <div className="no-projects">
            <div className="sec-head">
              The No-Code Playground for<br></br> Building
              <span className="hero-span">On-Chain AI</span>
            </div>
            <div className="sec-txt">
              Start building powerful AI workflows by<br></br> adding your first
              project.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default page;
