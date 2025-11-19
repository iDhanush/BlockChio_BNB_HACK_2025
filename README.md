# BlockChio — BNB Hackathon 2025

**BlockChio** is an **AI agent workflow builder for blockchain** — a no-code platform inspired by **LangChain/LangFlow**, enhanced with **blockchain-native agents** and **on-chain agentic memory**.

Build automated blockchain workflows where **AI agents can reason, act, transact, and store persistent memory on-chain**.

---

[![Languages](https://img.shields.io/badge/Python-54.4%25-blue?logo=python)](https://github.com/iDhanush/BlockChio_BNB_HACK_2025)
[![JavaScript](https://img.shields.io/badge/JavaScript-23.7%25-yellow?logo=javascript)](https://github.com/iDhanush/BlockChio_BNB_HACK_2025)
[![SCSS](https://img.shields.io/badge/SCSS-19.8%25-orange?logo=sass)](https://github.com/iDhanush/BlockChio_BNB_HACK_2025)
[![Solidity](https://img.shields.io/badge/Solidity-1.2%25-gray?logo=solidity)](https://github.com/iDhanush/BlockChio_BNB_HACK_2025)

---

## 🚀 Key Features

### AI Agent Workflows (LangFlow-Style)

- Drag-and-drop nodes to create:
  - AI reasoning chains
  - Multi-agent systems
  - Reactive event-driven flows

### Blockchain-Native Agents

- Contract calls
- Swaps, staking, transfers
- Event listeners
- Wallet signing & execution

### On-Chain Agentic Memory

Agents can store their state, preferences, and decisions directly **on-chain**, enabling:
- Long-term synchronization
- Verifiable agent behavior
- Persistent autonomous systems

### On-chain + Off-chain Integration

Connect blockchain primitives with:
- APIs
- Webhooks
- External apps
- IoT or Web2 services

---

## 📦 Tech Stack

- **Python (54%)** — Agent engine & AI logic (`python/`)
- **JavaScript (24%)** — Visual workflow builder (`frontend/`)
- **SCSS (20%)** — UI styling (`frontend/styles/`)
- **Solidity (1%)** — On-chain memory & tools (`contracts/`)

---

## 🗂️ Project Structure

```plaintext
BlockChio_BNB_HACK_2025/
├── python/           # Backend agent logic (Python)
├── frontend/         # Visual builder & UI (JavaScript, SCSS)
│   └── styles/
├── contracts/        # Solidity smart contracts
├── requirements.txt  # Python dependencies
├── package.json      # JS dependencies
└── README.md
```

---

## 🔧 Getting Started

### Requirements
- **Python 3.8+** recommended
- **Node.js 18+**
- **npm 9+**
- **Solidity Compiler (`solc`)** or **Hardhat** for advanced Solidity workflows

### 1. Clone the Repo
```bash
git clone https://github.com/iDhanush/BlockChio_BNB_HACK_2025.git
cd BlockChio_BNB_HACK_2025
```

### 2. Install Backend (Python) Dependencies
(Recommended: use a Python virtual environment)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Install Frontend (JavaScript) Dependencies
```bash
npm install
```

### 4. Compile Contracts (Solidity)
_If using bare solc:_
```bash
solc contracts/*.sol --bin --abi -o build/
```
_Or with Hardhat:_
```bash
npx hardhat compile
```

### 5. Run Backend & Frontend

Refer to the project structure or documentation for running both services. Example:
```bash
# Python (backend)
python python/app.py

# JavaScript (frontend, e.g., React)
npm run start
```

---

### 🧪 Testing

- **Python:**  
  ```bash
  pytest
  ```
- **JavaScript:**  
  ```bash
  npm test
  ```
- **Solidity:**  
  ```bash
  npx hardhat test
  ```

---

