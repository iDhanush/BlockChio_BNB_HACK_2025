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
              The No-Code Playground for
              <br /> Building
              <span className="hero-span">On-Chain AI</span>
            </div>
            <div className="sec-txt">
              Start building powerful AI workflows by
              <br /> adding your first project.
            </div>
            <div className="hero-btns">
              <div className="view-btn">View Templates</div>
              <div className="workflow-btn">Build Now</div>
            </div>
          </div>
        </div>

        {/* 🔁 Replaces animated GIF */}
        <video className="hero-img" autoPlay loop muted playsInline>
          <source src="/assets/mainbg.mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </div>
    </div>
  );
};

export default page;
