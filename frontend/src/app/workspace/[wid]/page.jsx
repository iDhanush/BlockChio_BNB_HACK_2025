"use client";
import React, { useState, useCallback, useRef, useEffect } from "react";
import "./app.scss";
import {
  Play,
  Save,
  Settings,
  MessageCircle,
  Send,
  Globe,
  Bot,
  Image,
  MessageSquare,
  Brain,
  X,
  CheckCircle,
  KeyRound,
} from "lucide-react";

import ChatWidget from "@/components/ui/ChatWidget/ChatWidget";
import { AnimatePresence } from "framer-motion";

// Enhanced Node Templates with node_class and default tool states
const nodeTemplates = [
  // Triggers
  {
    node_id: "manual_trigger",
    type: "trigger",
    label: "Manual Trigger",
    icon: Play,
    color: "gray",
    node_class: "ManualTrigger",
    creds: [],
    tools: [
      {
        id: "run_button",
        label: "Run Manually",
        description: "Start the workflow manually using this trigger",
      },
      {
        id: "debug_mode",
        label: "Debug Mode",
        description: "Enable debug mode for testing this trigger",
      },
    ],
  },
  {
    node_id: "whatsapp_trigger",
    type: "trigger",
    label: "WhatsApp",
    icon: MessageCircle,
    color: "green",
    node_class: "WhatsappTrigger",
    creds: [],
    tools: [
      {
        id: "webhook",
        label: "Webhook Settings",
        description: "Configure webhook URL and parameters",
      },
      {
        id: "auth",
        label: "Authentication",
        description: "Set up WhatsApp Business API credentials",
      },
      {
        id: "filters",
        label: "Message Filters",
        description: "Filter incoming messages by content or sender",
      },
      {
        id: "templates",
        label: "Message Templates",
        description: "Configure message templates",
      },
    ],
  },
  {
    node_id: "telegram_trigger",
    type: "trigger",
    label: "Telegram",
    icon: Send,
    color: "blue",
    node_class: "TelegramTrigger",
    creds: [],
    tools: [
      {
        id: "bot_token",
        label: "Bot Token",
        description: "Configure Telegram bot token",
      },
      {
        id: "webhook",
        label: "Webhook",
        description: "Set up webhook for receiving messages",
      },
      {
        id: "commands",
        label: "Bot Commands",
        description: "Configure bot commands and responses",
      },
      {
        id: "filters",
        label: "Message Filters",
        description: "Filter messages by type or content",
      },
    ],
  },
  {
    node_id: "webchat_trigger",
    type: "trigger",
    label: "WebChat",
    icon: Globe,
    color: "purple",
    node_class: "WebchatTrigger",
    creds: [],
    tools: [
      {
        id: "embed",
        label: "Embed Code",
        description: "Get embed code for your website",
      },
      {
        id: "styling",
        label: "Chat Styling",
        description: "Customize chat widget appearance",
      },
      {
        id: "analytics",
        label: "Analytics",
        description: "Track chat performance and metrics",
      },
      {
        id: "notifications",
        label: "Notifications",
        description: "Configure notification settings",
      },
    ],
  },

  // Agents
  {
    node_id: "blockchain_agent",
    type: "agent",
    label: "Blockchain Agent",
    icon: Bot,
    color: "orange",
    node_class: "BlockchainAgent",
    creds: [],
    tools: [
      {
        id: "wallet",
        label: "Wallet Connection",
        description: "Connect to blockchain wallets",
      },
      {
        id: "contracts",
        label: "Smart Contracts",
        description: "Manage smart contract interactions",
      },
      {
        id: "transactions",
        label: "Transaction Monitor",
        description: "Monitor blockchain transactions",
      },
      {
        id: "networks",
        label: "Network Settings",
        description: "Configure blockchain networks",
      },
      {
        label: "Send Transaction",
        description: "Send a transaction",
        tool_func: "send_transaction",
        active: true,
      },
      {
        label: "Mint NFT",
        description: "Send a transaction",
        tool_func: "mint_nft",
        active: true,
      },
      {
        label: "Get Balance",
        description: "Send a transaction",
        tool_func: "get_balance",
        active: true,
      },
    ],
  },
  {
    node_id: "image_generation_agent",
    type: "agent",
    label: "Image Generation",
    icon: Image,
    color: "red",
    node_class: "ImageAgent",
    creds: [],
    tools: [
      {
        id: "models",
        label: "AI Models",
        description: "Select and configure AI models",
      },
      {
        id: "prompts",
        label: "Prompt Templates",
        description: "Create and manage prompt templates",
      },
      {
        id: "styles",
        label: "Style Settings",
        description: "Configure image styles and parameters",
      },
      {
        id: "processing",
        label: "Image Processing",
        description: "Post-processing and optimization",
      },
      {
        label: "Generate Image",
        description: "Generate an image",
        tool_func: "generate_image",
        active: true,
      },
    ],
  },
  {
    node_id: "whatsapp_agent",
    type: "agent",
    label: "WhatsApp Agent",
    icon: MessageCircle,
    color: "green",
    node_class: "WhatsappAgent",
    creds: [],
    tools: [
      {
        id: "send_template",
        label: "Send Template Message",
        description: "Send pre-approved message templates",
      },
      {
        id: "manage_contacts",
        label: "Manage Contacts",
        description: "Add, update, or remove contacts",
      },
      {
        id: "message_status",
        label: "Message Status",
        description:
          "Track the status of sent messages (sent, delivered, read)",
      },
      {
        id: "api_health",
        label: "API Health",
        description:
          "Check the health and status of the WhatsApp API connection",
      },
      {
        label: "Send Message",
        description: "Send a transaction",
        tool_func: "send_message",
        active: true,
      },
      {
        label: "Send Image",
        description: "Send a transaction",
        tool_func: "send_image",
        active: true,
      },
    ],
  },
  {
    node_id: "telegram_agent",
    type: "agent",
    label: "Telegram Agent",
    icon: Send,
    color: "blue",
    node_class: "TelegramAgent",
    creds: [{ bot_token: null }],
    tools: [
      {
        id: "send_message",
        label: "Send Message",
        description: "Send text, media, or interactive messages",
      },
      {
        id: "manage_chat",
        label: "Manage Chat",
        description: "Manage chat settings, members, and permissions",
      },
      {
        id: "get_updates",
        label: "Get Updates",
        description: "Fetch real-time updates and message history",
      },
      {
        id: "api_settings",
        label: "API Settings",
        description: "Configure advanced API parameters",
      },
      {
        label: "Send Message",
        description: "Send a transaction",
        tool_func: "send_message",
        active: true,
      },
      {
        label: "Send Image",
        description: "Send a transaction",
        tool_func: "send_image",
        active: true,
      },
    ],
  },
  {
    node_id: "ai_assistant_agent",
    type: "agent",
    label: "AI Assistant",
    icon: Brain,
    color: "teal",
    node_class: "ConversationAgent",
    creds: [],
    tools: [
      {
        id: "capabilities",
        label: "AI Capabilities",
        description: "Configure AI assistant features",
      },
      {
        id: "integrations",
        label: "Integrations",
        description: "Connect with external services",
      },
      {
        id: "scheduling",
        label: "Task Scheduling",
        description: "Schedule automated tasks",
      },
      {
        id: "security",
        label: "Security Settings",
        description: "Configure security and permissions",
      },
      {
        label: "RAG",
        description: "Send a transaction",
        tool_func: "get_from_rag",
        active: true,
      },
      {
        label: "Unibase Chat Memory",
        description: "Send a transaction",
        tool_func: "unibase_chat_memory",
        active: true,
      },
      {
        label: "Google Search Tool",
        description: "Send a transaction",
        tool_func: "google_search",
        active: true,
      },
      {
        label: "Youtube Search Tool",
        description: "Send a transaction",
        tool_func: "youtube_search",
        active: true,
      },
    ],
  },
];

// Color mapping from names to hex codes
const colorMap = {
  green: "#34d399",
  blue: "#60a5fa",
  purple: "#a78bfa",
  red: "#f87171",
  orange: "#fb923c",
  indigo: "#818cf8",
  pink: "#f472b6",
  teal: "#2dd4bf",
};

// Helper function to convert hex to a string of RGB values
const hexToRgb = (hex) => {
  let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result
    ? `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(
        result[3],
        16
      )}`
    : null;
};

// Node Popup Component
const NodePopup = ({ node, onClose, onSave }) => {
  const [settings, setSettings] = useState(JSON.parse(JSON.stringify(node))); // Deep copy to avoid direct mutation

  const handleCredentialChange = (key, value) => {
    setSettings((prev) => ({
      ...prev,
      creds: [{ ...prev.creds[0], [key]: value }],
    }));
  };

  const handleToolToggle = (toolId) => {
    setSettings((prev) => ({
      ...prev,
      tools: prev.tools.map((tool) =>
        tool.id === toolId ? { ...tool, active: !tool.active } : tool
      ),
    }));
  };

  const handleSave = () => {
    onSave(settings);
    onClose();
  };

  if (!node) return null;

  return (
    <div className="node-popup-overlay" onClick={onClose}>
      <div className="node-popup" onClick={(e) => e.stopPropagation()}>
        <div className="popup-header">
          <div className="popup-title">
            <div className={`popup-icon ${node.color}`}>
              <node.icon size={20} />
            </div>
            <div>
              <h3>{node.label}</h3>
              <p>Configure {node.type} settings</p>
            </div>
          </div>
          <button className="close-btn" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <div className="popup-content">
          {/* Credentials Section */}
          {settings.creds &&
            settings.creds.length > 0 &&
            Object.keys(settings.creds[0]).length > 0 && (
              <div className="popup-section">
                {/* <h4 className="section-title">
                  <KeyRound size={16} /> Credentials
                </h4> */}
                {Object.keys(settings.creds[0]).map((key) => (
                  <div className="form-group" key={key}>
                    <label htmlFor={key}>{key.replace(/_/g, " ")}</label>
                    <input
                      type="password"
                      id={key}
                      value={settings.creds[0][key] || ""}
                      placeholder={`Enter your ${key.replace(/_/g, " ")}`}
                      onChange={(e) =>
                        handleCredentialChange(key, e.target.value)
                      }
                    />
                  </div>
                ))}
              </div>
            )}

          {/* Tools Section */}
          {settings.tools && settings.tools.length > 0 && (
            <div className="popup-section">
              {/* <h4 className="section-title">
                <Settings size={16} /> Tools
              </h4> */}
              <div className="tools-list">
                {settings.tools.map((tool) => (
                  <div key={tool.id} className="tool-item">
                    <div className="tool-info">
                      <div className="tool-label">{tool.label}</div>
                      <div className="tool-description">{tool.description}</div>
                    </div>
                    <label className="toggle-switch">
                      <input
                        type="checkbox"
                        checked={tool.active}
                        onChange={() => handleToolToggle(tool.id)}
                      />
                      <span className="slider"></span>
                    </label>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="popup-footer">
          <button
            className={`btn-save-settings ${node.color} `}
            onClick={handleSave}
          >
            <Save size={16} />
            Save Settings
          </button>
        </div>
      </div>
    </div>
  );
};

// Custom Node Component
const WorkflowNode = ({
  node,
  onNodeMove,
  onNodeSelect,
  onNodeDelete,
  onConnectionStart,
  onConnectionEnd,
  onNodeDoubleClick,
  selectedNode,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const nodeRef = useRef(null);

  const handleMouseDown = (e) => {
    if (e.target.classList.contains("connection-handle")) return;

    // Allow double click to open popup
    if (e.detail === 2) {
      onNodeDoubleClick(node);
      return;
    }

    setIsDragging(true);
    const rect = nodeRef.current.getBoundingClientRect();
    setDragOffset({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    });
    onNodeSelect(node.id);
  };

  const handleMouseMove = useCallback(
    (e) => {
      if (!isDragging) return;
      const canvas = nodeRef.current.closest(".workflow-canvas");
      const canvasRect = canvas.getBoundingClientRect();
      const newX = e.clientX - canvasRect.left - dragOffset.x;
      const newY = e.clientY - canvasRect.top - dragOffset.y;
      onNodeMove(node.id, { x: Math.max(0, newX), y: Math.max(0, newY) });
    },
    [isDragging, dragOffset, node.id, onNodeMove]
  );

  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
  }, []);

  useEffect(() => {
    if (isDragging) {
      document.addEventListener("mousemove", handleMouseMove);
      document.addEventListener("mouseup", handleMouseUp);
      return () => {
        document.removeEventListener("mousemove", handleMouseMove);
        document.removeEventListener("mouseup", handleMouseUp);
      };
    }
  }, [isDragging, handleMouseMove, handleMouseUp]);

  const isSelected = selectedNode === node.id;
  const activeToolCount = node.tools?.filter((t) => t.active).length || 0;
  const isConfigured = activeToolCount > 0;
  const spotlightRgb = hexToRgb(colorMap[node.color] || "#9ca3af");

  return (
    <div
      ref={nodeRef}
      className={`workflow-node ${isSelected ? "selected" : ""} ${
        isDragging ? "dragging" : ""
      } ${isConfigured ? "configured" : ""}`}
      style={{
        left: `${node.position.x}px`,
        top: `${node.position.y}px`,
        "--node-spotlight-rgb": spotlightRgb,
      }}
      onMouseDown={handleMouseDown}
      onDoubleClick={() => onNodeDoubleClick(node)}
    >
      <div
        className="connection-handle input-handle"
        onMouseDown={(e) => {
          e.stopPropagation();
          onConnectionEnd(node.id);
        }}
      />
      <div className="node-content">
        <div className={`node-icon ${node.color}`}>
          <node.icon size={16} />
        </div>
        <div className="node-info">
          <div className="node-label">{node.label}</div>
          <div className="node-type">{node.type}</div>
          {/* {isConfigured && (
            <div className="node-status">
              <CheckCircle size={12} />
              <span>{activeToolCount} tools active</span>
            </div>
          )} */}
        </div>
      </div>
      <div
        className="connection-handle output-handle"
        onMouseDown={(e) => {
          e.stopPropagation();
          onConnectionStart(node.id);
        }}
      />
      {isSelected && (
        <button
          className="delete-btn"
          onClick={(e) => {
            e.stopPropagation();
            onNodeDelete(node.id);
          }}
        >
          <X size={12} />
        </button>
      )}
    </div>
  );
};

// Connection Line Component
const ConnectionLine = ({ connection, nodes }) => {
  const fromNode = nodes.find((n) => n.id === connection.from);
  const toNode = nodes.find((n) => n.id === connection.to);

  if (!fromNode || !toNode) return null;

  const fromX = fromNode.position.x + 160; // node width
  const fromY = fromNode.position.y + 35; // node height / 2
  const toX = toNode.position.x;
  const toY = toNode.position.y + 35;

  const midX = fromX + (toX - fromX) * 0.5;

  const path = `M ${fromX} ${fromY} C ${midX} ${fromY}, ${midX} ${toY}, ${toX} ${toY}`;

  return (
    <path
      d={path}
      stroke="#6b7280"
      strokeWidth="2"
      fill="none"
      className="connection-line"
      markerEnd="url(#arrowhead)"
    />
  );
};

export default function N8nWorkflowBuilder() {
  const [nodes, setNodes] = useState([]);
  const [connections, setConnections] = useState([]);
  const [selectedNode, setSelectedNode] = useState(null);
  const [isRunning, setIsRunning] = useState(false);
  const [connectingFrom, setConnectingFrom] = useState(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [nodeCounter, setNodeCounter] = useState({});
  const [showNodePopup, setShowNodePopup] = useState(false);
  const [popupNode, setPopupNode] = useState(null);
  const [showChatWidget, setShowChatWidget] = useState(false);
  const canvasRef = useRef(null);

  const addNode = useCallback(
    (template) => {
      const currentCount = nodeCounter[template.node_id] || 0;
      const newNodeId = `${template.node_id}_${currentCount + 1}`;
      setNodeCounter((prev) => ({
        ...prev,
        [template.node_id]: currentCount + 1,
      }));

      const newNode = {
        ...template, // Spread the entire template
        id: newNodeId, // Override with a unique ID
        position: {
          x: Math.random() * 400 + 200,
          y: Math.random() * 200 + 150,
        },
      };
      // Deep copy tools and creds to ensure they are unique instances per node
      newNode.tools = JSON.parse(JSON.stringify(template.tools || []));
      newNode.creds = JSON.parse(JSON.stringify(template.creds || []));

      setNodes((prev) => [...prev, newNode]);
    },
    [nodeCounter]
  );

  const onNodeMove = useCallback((nodeId, newPosition) => {
    setNodes((prev) =>
      prev.map((node) =>
        node.id === nodeId ? { ...node, position: newPosition } : node
      )
    );
  }, []);

  const onNodeSelect = useCallback((nodeId) => {
    setSelectedNode(nodeId);
  }, []);

  const onNodeDoubleClick = useCallback((node) => {
    setPopupNode(node);
    setShowNodePopup(true);
    setSelectedNode(node.id);
  }, []);

  const onNodeDelete = useCallback(
    (nodeId) => {
      setNodes((prev) => prev.filter((node) => node.id !== nodeId));
      setConnections((prev) =>
        prev.filter((conn) => conn.from !== nodeId && conn.to !== nodeId)
      );
      if (selectedNode === nodeId) setSelectedNode(null);
    },
    [selectedNode]
  );

  const onConnectionStart = useCallback((nodeId) => {
    setConnectingFrom(nodeId);
  }, []);

  const onConnectionEnd = useCallback(
    (nodeId) => {
      if (connectingFrom && connectingFrom !== nodeId) {
        const newConnection = {
          id: `${connectingFrom}_to_${nodeId}`,
          from: connectingFrom,
          to: nodeId,
        };
        setConnections((prev) => [...prev, newConnection]);
      }
      setConnectingFrom(null);
    },
    [connectingFrom]
  );

  const handleCanvasClick = useCallback((e) => {
    if (e.target === canvasRef.current) {
      setSelectedNode(null);
      setConnectingFrom(null);
    }
  }, []);

  const handleCanvasMouseMove = useCallback(
    (e) => {
      if (connectingFrom) {
        const rect = canvasRef.current.getBoundingClientRect();
        setMousePos({ x: e.clientX - rect.left, y: e.clientY - rect.top });
      }
    },
    [connectingFrom]
  );

  const saveWorkflow = useCallback(() => {
    const workflowData = {
      nodes,
      connections,
      timestamp: new Date().toISOString(),
    };
    console.log("Saving workflow:", workflowData);
    alert("Workflow saved! Check console for details.");
  }, [nodes, connections]);

  const handleSaveNodeSettings = useCallback((updatedNode) => {
    // Find the original template to get the node_class
    const template = nodeTemplates.find(
      (t) => t.node_id === updatedNode.node_id
    );
    if (!template) {
      console.error("Could not find template for node:", updatedNode);
      return;
    }

    const { node_class } = template;
    const settingsPayload = {
      node_class,
      credentials: updatedNode.creds,
      active_tools: updatedNode.tools
        .filter((t) => t.active)
        .map((t) => t.id || t.tool_func),
    };

    // --- SIMULATED API CALL ---
    console.log(`🚀 API CALL: Saving settings for class '${node_class}'`);
    console.log("Payload:", settingsPayload);
    // Here you would typically make a fetch/axios call:
    // fetch('/api/save-node-settings', { method: 'POST', body: JSON.stringify(settingsPayload) });
    alert(
      `Settings saved for ${updatedNode.label}. API call logged to console.`
    );
    // --- END SIMULATED API CALL ---

    setNodes((prevNodes) =>
      prevNodes.map((n) => (n.id === updatedNode.id ? updatedNode : n))
    );
    setShowNodePopup(false);
    setPopupNode(null);
  }, []);

  const closePopup = useCallback(() => {
    setShowNodePopup(false);
    setPopupNode(null);
  }, []);

  return (
    <div className="workflow-builder">
      <header className="header">
        <div className="header-content">
          <div className="header-left">
            <h1 className="title">Project Builder</h1>
            <div className="actions">
              <button
                onClick={() => alert("Executing workflow!")}
                className="btn btn-execute"
              >
                <Play size={16} /> Execute
              </button>
              <button onClick={saveWorkflow} className="btn btn-save">
                <Save size={16} /> Save
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="main-content">
        <aside className="sidebar">
          <div className="sidebar-section">
            <h2 className="sidebar-title">Triggers</h2>
            <div className="node-templates">
              {nodeTemplates
                .filter((t) => t.type === "trigger")
                .map((template) => (
                  <button
                    key={template.node_id}
                    onClick={() => addNode(template)}
                    className="template-btn"
                  >
                    <div className={`template-icon ${template.color}`}>
                      <template.icon size={16} />
                    </div>
                    <div className="template-info">
                      <div className="template-label">{template.label}</div>
                      <div className="template-type">{template.type}</div>
                    </div>
                  </button>
                ))}
            </div>
          </div>
          <div className="sidebar-section">
            <h2 className="sidebar-title">Agents</h2>
            <div className="node-templates">
              {nodeTemplates
                .filter((t) => t.type === "agent")
                .map((template) => (
                  <button
                    key={template.node_id}
                    onClick={() => addNode(template)}
                    className="template-btn"
                  >
                    <div className={`template-icon ${template.color}`}>
                      <template.icon size={16} />
                    </div>
                    <div className="template-info">
                      <div className="template-label">{template.label}</div>
                      <div className="template-type">{template.type}</div>
                    </div>
                  </button>
                ))}
            </div>
          </div>
        </aside>

        <main className="canvas-container">
          <div
            ref={canvasRef}
            className="workflow-canvas"
            onClick={handleCanvasClick}
            onMouseMove={handleCanvasMouseMove}
          >
            <svg className="connections-svg">
              <defs>
                <marker
                  id="arrowhead"
                  viewBox="0 0 10 10"
                  refX="8"
                  refY="5"
                  markerWidth="6"
                  markerHeight="6"
                  orient="auto-start-reverse"
                >
                  <path d="M 0 0 L 10 5 L 0 10 z" fill="#6b7280" />
                </marker>
              </defs>
              {connections.map((conn) => (
                <ConnectionLine key={conn.id} connection={conn} nodes={nodes} />
              ))}
              {connectingFrom && (
                <line
                  x1={
                    nodes.find((n) => n.id === connectingFrom)?.position.x + 160
                  }
                  y1={
                    nodes.find((n) => n.id === connectingFrom)?.position.y + 35
                  }
                  x2={mousePos.x}
                  y2={mousePos.y}
                  stroke="#60a5fa"
                  strokeWidth="2"
                  strokeDasharray="5,5"
                />
              )}
            </svg>
            {nodes.map((node) => (
              <WorkflowNode
                key={node.id}
                node={node}
                onNodeMove={onNodeMove}
                onNodeSelect={onNodeSelect}
                onNodeDoubleClick={onNodeDoubleClick}
                onNodeDelete={onNodeDelete}
                onConnectionStart={onConnectionStart}
                onConnectionEnd={onConnectionEnd}
                selectedNode={selectedNode}
              />
            ))}
          </div>
          <button
            onClick={() => setShowChatWidget(!showChatWidget)}
            className="fab"
          >
            <MessageSquare size={28} />
          </button>
        </main>
      </div>

      {showNodePopup && (
        <NodePopup
          node={popupNode}
          onClose={closePopup}
          onSave={handleSaveNodeSettings}
        />
      )}

      <AnimatePresence>
        {showChatWidget && (
          <ChatWidget onClose={() => setShowChatWidget(false)} />
        )}
      </AnimatePresence>
    </div>
  );
}
