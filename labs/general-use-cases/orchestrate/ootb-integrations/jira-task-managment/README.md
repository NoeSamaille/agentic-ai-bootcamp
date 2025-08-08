# ✅ JIRA Task Management Automation with IBM watsonx Orchestrate

## 🤔 The Problem

Managing tasks in JIRA manually — such as creating new tickets, updating statuses, assigning users, or tracking progress — can be time-consuming and error-prone. Teams often face challenges like:

- Delays in creating and assigning tasks  
- Lack of standardization in ticket fields and descriptions  
- Inconsistent tracking and status updates  
- Bottlenecks in collaboration across teams and projects  

## 🎯 Objective

To streamline JIRA-based workflows and reduce manual effort, this solution introduces an **AI-powered Task Management Agent** built using **IBM watsonx Orchestrate**.

This agent enables users to manage JIRA tasks using natural language, reducing the need to navigate JIRA’s interface manually.

The goal is to enable users to:

- Create, update, or delete JIRA tasks using plain language  
- Assign issues to users and set due dates  
- Change statuses (e.g., “move to In Progress”, “close task”)  
- Retrieve project/task summaries and statuses  
- Automate repetitive ticketing processes across projects  

## 📈 Business Value

- Save time by automating common JIRA operations  
- Reduce errors in task tracking and ownership  
- Improve visibility into project status and priorities  
- Empower non-technical users to interact with JIRA using simple prompts  

## 🏛 Architecture

A single watsonx Orchestrate agent is configured to handle JIRA task operations. The agent connects securely to your JIRA workspace and responds to natural language instructions.

### Tools Used

- `Create task in JIRA` — Opens a new issue in a selected project  
- `Update task in JIRA` — Modifies fields like summary, description, assignee, or status  
- `Get all projects in JIRA` — Lists all available JIRA projects  
- `Get tasks by status in JIRA` — Retrieves issues filtered by status (e.g., To Do, In Progress)  
- `Get task by ID in JIRA` — Returns full details of a specific task  
- `Assign task in JIRA` — Assigns an issue to a specific user  

### Agent Behavior

- The agent uses **natural language prompts** like:  
  - "Create a new bug in the Payments project"  
  - "Assign task `JIRA-1023` to Alice"  
  - "What tasks are in progress for the HR team?"

- Based on context, it calls the appropriate JIRA tool  
- It returns clean, structured outputs like ticket IDs, status, links, and assignees  
- Users can interact through chat without opening JIRA manually  

## 📝 Step-by-step Hands-on Lab

You can find step-by-step instructions here:

👉 [Step-by-step Hands-on Guide](./hands-on-lab-jira-task-management.md)
