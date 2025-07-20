"use client";
import React, { useState, useCallback, useRef, useEffect } from "react";
import "./app.scss";
import {
  Play,
  Save,
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
  LoaderCircle,
  AlertTriangle,
} from "lucide-react";

import ChatWidget from "@/components/ui/ChatWidget/ChatWidget";
import { AnimatePresence } from "framer-motion";
import {
  updateWflow,
  getWflow,
  executeWflow,
  getExecutionStatus,
} from "@/utils/workflow";
import { useParams } from "next/navigation";

//==============================================================================
// CONSTANTS & TEMPLATES
//==============================================================================

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
    tools: [],
    purpose: "",
  },
  {
    node_id: "whatsapp_trigger",
    type: "trigger",
    label: "WhatsApp",
    icon: MessageCircle,
    color: "green",
    node_class: "WhatsappTrigger",
    creds: [],
    tools: [],
    purpose: "",
  },
  {
    node_id: "telegram_trigger",
    type: "trigger",
    label: "Telegram",
    icon: Send,
    color: "blue",
    node_class: "TelegramTrigger",
    creds: [],
    tools: [],
    purpose: "",
  },
  {
    node_id: "webchat_trigger",
    type: "trigger",
    label: "WebChat",
    icon: Globe,
    color: "purple",
    node_class: "WebchatTrigger",
    creds: [],
    tools: [],
    purpose: "",
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
    purpose: "",
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
        label: "Generate Image",
        description: "Generate an image",
        tool_func: "generate_image",
        active: true,
      },
    ],
    purpose: "",
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
    purpose: "",
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
    purpose: "",
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
        tool_func: "Google Search",
        active: true,
      },
      {
        label: "Youtube Tool",
        description: "Send a transaction",
        tool_func: "Youtube",
        active: true,
      },
    ],
    purpose: "",
  },
];

const colorMap = {
  green: "#34d399",
  blue: "#60a5fa",
  purple: "#a78bfa",
  red: "#f87171",
  orange: "#fb923c",
  indigo: "#818cf8",
  pink: "#f472b6",
  teal: "#2dd4bf",
  gray: "#9ca3af",
};

const hexToRgb = (hex) => {
  let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result
    ? `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(
        result[3],
        16
      )}`
    : null;
};

//==============================================================================
// HELPER COMPONENTS
//==============================================================================

const ExecutionStatusToast = ({ status, onClose }) => {
  const getIcon = () => {
    switch (status.type) {
      case "info":
        return <LoaderCircle size={20} className="animate-spin" />;
      case "success":
        return <CheckCircle size={20} />;
      case "error":
        return <AlertTriangle size={20} />;
      default:
        return null;
    }
  };

  useEffect(() => {
    if (status.type === "success" || status.type === "error") {
      const timer = setTimeout(() => {
        onClose();
      }, 6000);
      return () => clearTimeout(timer);
    }
  }, [status, onClose]);

  if (!status) return null;

  return (
    <div className={`status-toast ${status.type}`}>
      <div className="status-icon">{getIcon()}</div>
      <p className="status-message">{status.message}</p>
      <button className="close-toast" onClick={onClose}>
        <X size={16} />
      </button>
    </div>
  );
};

const NodePopup = ({ node, onClose, onSave }) => {
  const [settings, setSettings] = useState(JSON.parse(JSON.stringify(node)));

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
        tool.tool_func === toolId ? { ...tool, active: !tool.active } : tool
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
          {settings.creds &&
            settings.creds.length > 0 &&
            Object.keys(settings.creds[0]).length > 0 && (
              <div className="popup-section">
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
          {settings.tools && settings.tools.length > 0 && (
            <div className="popup-section">
              <div className="tools-list">
                {settings.tools.map((tool) => (
                  <div key={tool.tool_func} className="tool-item">
                    <div className="tool-info">
                      <div className="tool-label">{tool.label}</div>
                      <div className="tool-description">{tool.description}</div>
                    </div>
                    <label className="toggle-switch">
                      <input
                        type="checkbox"
                        checked={tool.active}
                        onChange={() => handleToolToggle(tool.tool_func)}
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
            className={`btn-save-settings ${node.color}`}
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
    if (e.detail === 2) {
      onNodeDoubleClick(node);
      return;
    }
    setIsDragging(true);
    const rect = nodeRef.current.getBoundingClientRect();
    setDragOffset({ x: e.clientX - rect.left, y: e.clientY - rect.top });
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
  const spotlightRgb = hexToRgb(colorMap[node.color] || "#9ca3af");

  return (
    <div
      ref={nodeRef}
      className={`workflow-node ${isSelected ? "selected" : ""} ${
        isDragging ? "dragging" : ""
      }`}
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

const ConnectionLine = ({ connection, nodes }) => {
  const fromNode = nodes.find((n) => n.id === connection.from_node);
  const toNode = nodes.find((n) => n.id === connection.to_node);
  if (!fromNode || !toNode) return null;
  const fromX = fromNode.position.x + 160;
  const fromY = fromNode.position.y + 35;
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

//==============================================================================
// MAIN PAGE COMPONENT
//==============================================================================
export default function N8nWorkflowBuilder() {
  const [nodes, setNodes] = useState([]);
  const [connections, setConnections] = useState([]);
  const [selectedNode, setSelectedNode] = useState(null);
  const [connectingFrom, setConnectingFrom] = useState(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [nodeCounter, setNodeCounter] = useState({});
  const [showNodePopup, setShowNodePopup] = useState(false);
  const [popupNode, setPopupNode] = useState(null);
  const [showChatWidget, setShowChatWidget] = useState(false);
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionStatus, setExecutionStatus] = useState(null);

  const canvasRef = useRef(null);
  const pollingIntervalRef = useRef(null);
  const params = useParams();
  const [workflowId, setWorkflowid] = useState(params.wid);

  // --- Effects ---
  useEffect(() => {
    const loadWorkflow = async () => {
      if (!workflowId) return;
      try {
        const savedWorkflow = await getWflow(workflowId);
        if (!savedWorkflow || !savedWorkflow.nodes) return;
        const tempCounters = {};
        const rehydratedNodes = savedWorkflow.nodes
          .map((node) => {
            const template = nodeTemplates.find(
              (t) => t.node_id === node.node_id
            );
            if (!template) return null;
            const currentCount = (tempCounters[node.node_id] || 0) + 1;
            tempCounters[node.node_id] = currentCount;
            const uniqueId = `${node.node_id}_${currentCount}`;
            return { ...template, ...node, id: uniqueId };
          })
          .filter(Boolean);
        setNodes(rehydratedNodes);
        setConnections(savedWorkflow.connections || []);
        setNodeCounter(tempCounters);
      } catch (error) {
        console.error("Failed to load workflow:", error);
      }
    };
    loadWorkflow();
  }, [workflowId]);

  useEffect(() => {
    return () => {
      if (pollingIntervalRef.current) clearInterval(pollingIntervalRef.current);
    };
  }, []);

  // --- Handlers ---
  const addNode = useCallback(
    (template) => {
      const currentCount = nodeCounter[template.node_id] || 0;
      const newNodeId = `${template.node_id}_${currentCount + 1}`;
      setNodeCounter((prev) => ({
        ...prev,
        [template.node_id]: currentCount + 1,
      }));
      const newNode = {
        ...template,
        id: newNodeId,
        position: {
          x: Math.random() * 400 + 200,
          y: Math.random() * 200 + 150,
        },
      };
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
        prev.filter(
          (conn) => conn.from_node !== nodeId && conn.to_node !== nodeId
        )
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
        const connectionExists = connections.some(
          (conn) => conn.from_node === connectingFrom && conn.to_node === nodeId
        );
        if (!connectionExists) {
          const newConnection = {
            conn_id: `${connectingFrom}_to_${nodeId}_${Date.now()}`,
            from_node: connectingFrom,
            to_node: nodeId,
          };
          setConnections((prev) => [...prev, newConnection]);
        }
      }
      setConnectingFrom(null);
    },
    [connectingFrom, connections]
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

  const saveWorkflow = useCallback(async () => {
    const workflowData = { nodes, connections };
    await updateWflow(workflowId, workflowData);
    setExecutionStatus({
      type: "success",
      message: "Workflow saved successfully!",
    });
  }, [nodes, connections, workflowId]);

  const handleExecute = useCallback(async () => {
    // if (isExecuting) return;
    // setIsExecuting(true);
    // setExecutionStatus({ type: "info", message: "Initiating execution..." });
    // if (pollingIntervalRef.current) clearInterval(pollingIntervalRef.current);

    try {
      const workflowData = { nodes, connections };
      const response = await executeWflow(workflowId, workflowData);
      if (response) {
        // setExecutionStatus({
        //   type: "info",
        //   message: "Execution started. Polling for status...",
        // });
        alert("executed");
      } else {
        throw new Error("Did not receive an execution ID.");
      }

      // pollingIntervalRef.current = setInterval(async () => {
      //   try {
      //     const result = await getExecutionStatus(response.executionId);
      //     if (!result) return;
      //     const finalStates = ["COMPLETED", "SUCCESS", "FAILED", "ERROR"];
      //     if (finalStates.includes(result.status.toUpperCase())) {
      //       clearInterval(pollingIntervalRef.current);
      //       setIsExecuting(false);
      //       setExecutionStatus({
      //         type: result.status.toUpperCase().includes("FAIL")
      //           ? "error"
      //           : "success",
      //         message: result.message,
      //       });
      //     } else {
      //       setExecutionStatus({
      //         type: "info",
      //         message: `Status: ${result.message}`,
      //       });
      //     }
      //   } catch (pollError) {
      //     clearInterval(pollingIntervalRef.current);
      //     setIsExecuting(false);
      //     setExecutionStatus({
      //       type: "error",
      //       message: "Error while polling status.",
      //     });
      //   }
      // }, 4000);
    } catch (error) {
      setIsExecuting(false);
      setExecutionStatus({
        type: "error",
        message: "Failed to start execution.",
      });
    }
  }, [nodes, connections, workflowId, isExecuting]);

  const handleSaveNodeSettings = useCallback((updatedNode) => {
    setNodes((prevNodes) =>
      prevNodes.map((n) =>
        n.id === updatedNode.id
          ? { ...n, creds: updatedNode.creds, tools: updatedNode.tools }
          : n
      )
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
                onClick={handleExecute}
                className="btn btn-execute"
                disabled={isExecuting}
              >
                {isExecuting ? (
                  <>
                    <LoaderCircle size={16} className="animate-spin-fast" />{" "}
                    Executing...
                  </>
                ) : (
                  <>
                    <Play size={16} /> Execute
                  </>
                )}
              </button>
              <button
                onClick={saveWorkflow}
                className="btn btn-save"
                disabled={isExecuting}
              >
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
          {executionStatus && (
            <ExecutionStatusToast
              status={executionStatus}
              onClose={() => setExecutionStatus(null)}
            />
          )}
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
                <ConnectionLine
                  key={conn.conn_id}
                  connection={conn}
                  nodes={nodes}
                />
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
            <MessageSquare size={20} />
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
