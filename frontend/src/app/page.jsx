"use client";
import { useEffect, useRef } from "react";
import TopNav from "@/components/TopNav/TopNav";
import "./app.scss";

// Import GSAP and its ScrollTrigger plugin
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

import DASH from "../../public/assets/dashimg.png";
import Image from "next/image";

// Register the ScrollTrigger plugin with GSAP
gsap.registerPlugin(ScrollTrigger);

const Page = () => {
  // Create refs for the main container and the image to be animated
  const mainRef = useRef(null);
  const dashImgRef = useRef(null);

  // useEffect hook to set up the animation after the component mounts
  useEffect(() => {
    // Create a GSAP context for safe cleanup
    const ctx = gsap.context(() => {
      // Define the animation
      gsap.to(dashImgRef.current, {
        scale: 1, // Animate scale to 1
        ease: "none", // Use a linear ease for direct correlation with scroll
        scrollTrigger: {
          trigger: ".dash-img-cover-wrapper", // The element that triggers the animation
          start: "top bottom", // Animation starts when the top of the trigger hits the bottom of the viewport
          end: "bottom 80%", // Animation ends when the bottom of the trigger is 80% from the top of the viewport
          scrub: 1, // Links the animation progress directly to the scrollbar position (1 provides a little smoothing)
          // markers: true, // Uncomment for debugging to see start/end markers
        },
      });
    }, mainRef); // Scope the context to the main container

    // Cleanup function to revert all GSAP animations and ScrollTriggers on component unmount
    return () => ctx.revert();
  }, []); // Empty dependency array ensures this effect runs only once

  return (
    // Add the ref to the main container
    <div className="home" ref={mainRef}>
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
      <div className="dash-img-cover-wrapper">
        <div
          className="dash-img-cover"
          ref={dashImgRef}
          // Set the initial scale of the image using an inline style
          style={{ scale: 0.8, transformOrigin: "center center" }}
        >
          <Image src={DASH} alt="img" className="dash-img" />
        </div>
      </div>
    </div>
  );
};

export default Page;
