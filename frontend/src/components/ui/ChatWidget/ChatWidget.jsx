"use client";
import { Bot, Send, X, Paperclip, ImageIcon } from "lucide-react";
import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion"; // Import motion
import "./ChatWidget.scss";

const ChatWidget = ({ onClose }) => {
  // State to hold the list of messages
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: "bot",
      type: "text",
      content:
        "Hello! This is a simulated chat. You can send text or images. How can I help you today?",
      timestamp: new Date(),
    },
  ]);

  // State for the current input value
  const [inputValue, setInputValue] = useState("");
  // State for the selected image file
  const [imageFile, setImageFile] = useState(null);
  // State for the preview URL of the selected image
  const [imagePreview, setImagePreview] = useState(null);

  // Ref for the file input element
  const fileInputRef = useRef(null);
  // Ref for the messages container to enable auto-scrolling
  const messagesEndRef = useRef(null);

  // Effect to scroll to the bottom of the messages list when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Handles changes to the file input
  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith("image/")) {
      setImageFile(file);
      setImagePreview(URL.createObjectURL(file));
    } else {
      setImageFile(null);
      setImagePreview(null);
    }
  };

  // Triggers the hidden file input
  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  // Removes the selected image preview
  const removeImagePreview = () => {
    setImageFile(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  // Handles sending a message (text or image)
  const handleSendMessage = () => {
    if (inputValue.trim() === "" && !imageFile) return;

    const newMessages = [];

    if (imageFile && imagePreview) {
      newMessages.push({
        id: Date.now() + "-img",
        sender: "user",
        type: "image",
        content: imagePreview,
        timestamp: new Date(),
      });
    }

    if (inputValue.trim() !== "") {
      newMessages.push({
        id: Date.now() + "-txt",
        sender: "user",
        type: "text",
        content: inputValue,
        timestamp: new Date(),
      });
    }

    if (newMessages.length > 0) {
      setMessages((prev) => [...prev, ...newMessages]);
    }

    setInputValue("");
    removeImagePreview();

    setTimeout(() => {
      const botResponse = {
        id: Date.now() + "-bot",
        sender: "bot",
        type: "text",
        content: "Thanks for your message! I've received it.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, botResponse]);
    }, 1500);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Animation variants for the chat widget
  const widgetVariants = {
    open: {
      opacity: 1,
      y: 0,
      scale: 1,
      transition: { type: "spring", stiffness: 300, damping: 24 },
    },
    closed: {
      opacity: 0,
      y: 20,
      scale: 0,
      transition: { duration: 0.3 },
    },
  };

  return (
    <motion.div
      className="chat-widget"
      variants={widgetVariants}
      initial="closed"
      animate="open"
      exit="closed"
      // This makes the animation originate from the bottom right
      style={{ transformOrigin: "bottom right" }}
    >
      <div className="chat-header">
        <div className="header-info">
          <Bot className="bot-icon" />
          <div className="header-text">
            <span className="title">Web Chat</span>
            <span className="status">Online</span>
          </div>
        </div>
        <button onClick={onClose} className="close-button">
          <X size={20} />
        </button>
      </div>

      <div className="chat-body">
        {messages.map((msg) => (
          <div key={msg.id} className={`message-container ${msg.sender}`}>
            <div className={`message-bubble ${msg.type}`}>
              {msg.type === "text" ? (
                <p>{msg.content}</p>
              ) : (
                <img
                  src={msg.content}
                  alt="User upload"
                  className="message-image"
                />
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-footer">
        {imagePreview && (
          <div className="image-preview-container">
            <img src={imagePreview} alt="Preview" className="image-preview" />
            <button onClick={removeImagePreview} className="remove-image-btn">
              <X size={16} />
            </button>
          </div>
        )}
        <div className="input-area">
          <input
            type="text"
            placeholder="Type a message..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleImageChange}
            accept="image/*"
            style={{ display: "none" }}
          />
          <button onClick={triggerFileInput} className="icon-button">
            <Paperclip size={20} />
          </button>
          <button onClick={handleSendMessage} className="send-button">
            <Send size={16} />
          </button>
        </div>
      </div>
    </motion.div>
  );
};

export default ChatWidget;
