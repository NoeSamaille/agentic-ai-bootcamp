# Agentic AI Challenge #1: Data Center Operations

![Chillers](https://www.stackinfra.com/wp-content/uploads/2021/02/Stack_Rooftop_Chillers.jpg)

## Overview
This challenge is designed for participants to build an **Agentic AI system** using their preferred AI framework, such as **Watsonx Orchestrate, watsonx.ai, LangGraph, LangChain, CrewAI**, etc. The goal is to **support Data Center Cooling Operations and Planning** by leveraging an AI-powered agent that can monitor and respond to chiller-related issues.

## Challenge Objective
Participants will develop an **AI-driven solution** that can answer a simple yet critical question:

**"Is my Chiller number 11 system overheating? If yes, provide a detailed action plan to diagnose/fix it."**

### Requirements:
1. The solution must be able to:
   - Take the user's query as input.
   - Connect to the API Gateway Server at **[https://wx-agentic-dc-chiller-gw.1944johjccn7.eu-de.codeengine.appdomain.cloud](https://wx-agentic-dc-chiller-gw.1944johjccn7.eu-de.codeengine.appdomain.cloud)**.
   - Retrieve real-time chiller data from the API.
   - Analyze the temperature and status of the chiller.
   - Determine if the chiller is overheating based on predefined conditions.
   - If overheating, generate a **detailed action plan** to diagnose and fix the issue.
   - Return a clear and structured response to the user.

2. The solution must integrate with one or more of the following **Agentic AI frameworks**:
   - Watsonx Orchestrate
   - watsonx.ai
   - LangGraph
   - LangChain
   - CrewAI

3. The AI should **simulate an intelligent assistant** capable of making decisions and suggesting actions autonomously.

---
## API Gateway Information
### API Authentication
This API requires an API key for authentication, which must be included in the request header as `X-API-Key`.

Example header:
```http
X-API-Key: 6d0f5733c6114c66af606cfb6b7ed9db
```

### API Endpoint:
#### Retrieve Chiller Metrics
```http
GET https://wx-agentic-dc-chiller-gw.1944johjccn7.eu-de.codeengine.appdomain.cloud/simulate/{chiller_id}
```

**Parameters:**
| Parameter    | Type    | Description                     |
|-------------|--------|---------------------------------|
| `chiller_id` | `int`   | ID of the chiller (1 to 20)    |

**Example Request:**
```sh
curl -X GET "https://chiller-gateway-01.lab/simulate/11" \
     -H "X-API-Key: 6d0f5733c6114c66af606cfb6b7ed9db"
```

---
## **User Story**
### **Title:** AI-powered Data Center Chiller Monitoring & Troubleshooting Agent

#### **As a**
Data Center Operator,

#### **I want to**
be able to ask an AI assistant whether my chiller is overheating and receive a detailed action plan if an issue is detected,

#### **So that**
I can quickly diagnose and fix potential cooling issues to prevent downtime and ensure efficient operations.

---
## **Expected Solution Workflow**
1. **User Query Handling:**
   - The user asks: _"Is my Chiller number 11 system overheating? If yes, provide a detailed action plan to diagnose/fix it."_

2. **Data Retrieval:**
   - The AI agent connects to `https://wx-agentic-dc-chiller-gw.1944johjccn7.eu-de.codeengine.appdomain.cloud/simulate/11`.
   - Retrieves temperature readings, pressure levels, and operational status.

3. **Analysis & Decision Making:**
   - The agent determines if `return_air_temp` or `supply_water_temp` is above safe thresholds.
   - If overheating, it generates an action plan.
   - If normal, it provides a status update.

4. **Action Plan Generation:**
   - If the system is overheating, the AI suggests:
     - Checking coolant levels
     - Inspecting airflow and fan speed
     - Validating water inlet pressure and pressure drop
     - Recommending a service check if needed

5. **User Response:**
   - The AI responds with:
     - _"Chiller 11 is overheating. Recommended actions: 1) Check coolant levels (Current: 22%). 2) Increase airflow (Current: 150 CFM). 3) Inspect pressure levels."_

---
## **Evaluation Criteria**
Participants will be evaluated based on:
- **Accuracy**: How well the AI agent identifies overheating conditions.
- **Effectiveness**: The quality of the action plan generated.
- **Integration**: Proper connection with the API Gateway.
- **Autonomy**: The ability of the AI agent to make intelligent decisions.
- **Usability**: How user-friendly the solution is.

### **Bonus Points for:**
- Implementing multi-chiller monitoring.
- Providing proactive maintenance suggestions.
- Enhancing the AI assistant with conversational capabilities.

## **Get Started!**
This challenge is designed to push your Agentic AI development skills! Use your preferred framework and submit your solution demonstrating an intelligent, automated AI-powered chiller monitoring system.

Good luck!

