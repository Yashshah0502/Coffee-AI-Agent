# Coffee AI Agent

**Coffee AI Agent** is an intelligent, multi-agent system that powers a conversational coffee shop assistant.
It uses **Large Language Models (LLMs)**, **retrieval-augmented generation (RAG)**, and **data-driven recommendations** to let users order coffee, explore products, and receive personalized suggestions through a mobile app.

---

## Overview

This project demonstrates how multiple specialized agents can coordinate to handle natural language interactions in a production-style environment.
Each agent performs a dedicated function — filtering, classification, recommendation, or order handling — while maintaining shared context through a unified protocol.

The backend is built with **FastAPI** and deployed on **RunPod** for scalable model hosting.
The frontend is a **React Native (Expo)** mobile app that provides a simple, chat-based interface.

---

## System Architecture

```
Mobile App (React Native + Expo)
        │
        ▼
FastAPI Backend (RunPod)
 ├── Guard Agent → filters unsafe or irrelevant input
 ├── Classification Agent → identifies user intent
 ├── Details Agent → provides menu and shop information
 ├── Recommendation Agent → suggests related items
 └── Order Agent → manages conversational order flow
        │
        ▼
   Pinecone Vector Database
        │
        ▼
   Recommendation Data (Apriori + Popularity Models)
```

All agents follow a shared `AgentProtocol` interface, making the system modular and easily extensible.

---

## Core Components

| Agent                    | Description                                                                           |
| ------------------------ | ------------------------------------------------------------------------------------- |
| **Guard Agent**          | Filters irrelevant or unsafe inputs before routing them to other agents.              |
| **Classification Agent** | Identifies whether the request is an order, a recommendation, or a general query.     |
| **Details Agent**        | Returns factual data such as menu details, pricing, and store hours.                  |
| **Recommendation Agent** | Suggests items using Market Basket Analysis and popularity data.                      |
| **Order Agent**          | Handles the order process — building carts, confirming items, and summarizing totals. |

---

## Key Features

* Modular **multi-agent architecture** with clear responsibilities
* **LLM-powered reasoning** and retrieval using Pinecone embeddings
* Real-time **recommendation engine** based on Market Basket patterns
* Structured **JSON prompts and output validation**
* Secure communication and robust API design
* Cross-platform **mobile client** built with React Native and TypeScript

---

## Tech Stack

### **Backend (Python)**

| Tool                 | Purpose                                                |
| -------------------- | ------------------------------------------------------ |
| **FastAPI**          | High-performance API framework for asynchronous agents |
| **LangGraph**        | Multi-agent orchestration and conversation flow        |
| **Pinecone**         | Vector database for semantic retrieval and RAG         |
| **Redis (optional)** | Background job queue and message streaming             |
| **RunPod**           | Serverless GPU hosting for LLM and embeddings          |

### **Frontend (React Native)**

| Tool                          | Purpose                                      |
| ----------------------------- | -------------------------------------------- |
| **Expo SDK 54**               | Simplifies cross-platform mobile development |
| **TypeScript**                | Provides static typing and maintainability   |
| **NativeWind (Tailwind CSS)** | Utility-first styling for React Native       |
| **Expo Router v6**            | File-based routing and navigation            |
| **Firebase**                  | Real-time database and user state management |

### **Data & Modeling**

| Tool                     | Purpose                                    |
| ------------------------ | ------------------------------------------ |
| **Apriori Algorithm**    | Market Basket Analysis for product pairing |
| **Popularity CSV Model** | Backup recommendations for sparse data     |

### **DevOps**

| Tool                      | Purpose                                         |
| ------------------------- | ----------------------------------------------- |
| **Docker**                | Containerized backend for consistent deployment |
| **RunPod Serverless GPU** | Scalable inference endpoints for LLMs           |
| **.env Configuration**    | Secure environment-based key management         |

---

## RunPod Deployment

The backend and model inference services are hosted using **RunPod Serverless GPUs**, ensuring scalable and cost-efficient execution.

**Deployment Highlights:**

* Each agent runs via lightweight FastAPI endpoints on GPU pods
* LLaMA 3.1 model handles reasoning and text generation
* Automatic scaling to zero when idle to minimize cost
* End-to-end encryption handled by RunPod’s TLS layer

**Docker Example:**

```bash
docker build -t yash874/coffeagent2:v1 .
docker push yash874/coffeagent2:v1
```

---

## Local Setup

### Backend

```bash
git clone https://github.com/Yashshah0502/coffee-ai-agent.git
cd coffee-ai-agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Frontend

```bash
cd coffee_shop_app
npm install
npx expo start --tunnel
```

Open the **Expo Go** app on your mobile device and scan the QR code to test.

---

## Security

* API credentials stored securely in `.env` files
* Encrypted HTTPS communication for all requests
* Guard Agent filters unsafe or unrelated input
* Structured JSON parsing prevents prompt or output injection

---

## Future Improvements

* Add user authentication and role-based access
* Integrate analytics for sales and recommendation performance
* Extend to multiple store branches
* Enable speech-based input and voice responses
* Store persistent order history using a cloud database

---

## Learning Outcomes

This project demonstrates how to:

* Build a **modular, multi-agent architecture** around an LLM
* Implement **retrieval-augmented generation (RAG)** pipelines
* Apply **Market Basket Analysis** for recommendations
* Connect a **FastAPI backend** with a **React Native frontend**
* Deploy and scale **LLM inference on RunPod** using Docker

---

## Author

**Yash Shah**
AI Engineer | Data Engineer | Full-Stack Developer
[GitHub](https://github.com/Yashshah0502) • [LinkedIn](https://www.linkedin.com/in/yash0502)

---
