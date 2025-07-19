"use client";
import TopNav from "@/components/TopNav/TopNav";
import "./app.scss";
const page = () => {
  return (
    <div className="hero">
      <div className="hero-linear"></div>
      <TopNav />
      <div className="main-sec">
        <div className="main-txt">
          Create Your Own<br></br>Decentralized <span>AI Agents</span>
        </div>
        <div className="hero-sub-txt">
          Start building your AI agents with full control and transparency.
        </div>
      </div>
    </div>
  );
};

export default page;
