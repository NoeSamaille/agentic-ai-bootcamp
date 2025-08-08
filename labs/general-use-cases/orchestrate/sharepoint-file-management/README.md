# 🗂️ SharePoint Document Access Automation with IBM watsonx Orchestrate

## 🤔 The Problem

Many organizations store critical business documents in Microsoft SharePoint. However, manual access to these documents — such as locating the correct folder, downloading files, or listing available items — can be time-consuming and error-prone. Teams often face challenges like:

- Difficulty finding the right file in a nested folder structure  
- Repetitive navigation for common document retrieval tasks  
- Inconsistent folder organization and naming  
- Lack of automation for document-driven workflows  

## 🎯 Objective

To simplify and accelerate access to content stored in Microsoft SharePoint, this solution introduces an **AI-powered Document Access Agent** built using **IBM watsonx Orchestrate**.

This agent helps users retrieve files, list folders, and explore SharePoint document libraries without manual navigation.

The goal is to enable users to:

- Search and retrieve files stored in SharePoint  
- Get lists of folders, items, or sites  
- Automate document access flows via natural language  
- Seamlessly integrate document queries into business workflows  ◊
- Minimize errors in file selection and location  
- Empower users to request and access files using natural language  
- Automate repetitive document lookup tasks  
- Support document-driven workflows across departments  

## 🏛 Architecture

A single watsonx Orchestrate agent is created to handle SharePoint document operations. The agent uses various SharePoint tools to navigate the document structure and retrieve files or folders based on user prompts.

### Tools Used

- `Get sites in SharePoint` — Retrieves a list of available SharePoint sites  
- `Get all folders in SharePoint` — Lists all folders in a site or document library  
- `Get all files in SharePoint` — Lists files stored in a selected location  
- `Get all folders items in SharePoint` — Lists both folders and files in a location  
- `Download a file in SharePoint` — Generates download link for a file  
- `Create new folder in SharePoint` — Creates a folder in a specified location  

### Agent Behavior

- The agent uses **natural language prompts** (e.g., "Show me all files in the HR site")  
- Based on context, it triggers appropriate tools (e.g., `Get all files`, `Download a file`)  
- It can return file URLs, folder names, and item counts  
- Can optionally guide the user to perform follow-up actions like downloading or organizing files  

## 📝 Step-by-step Hands-on Lab

You can find step-by-step instructions here:

👉 [Step-by-step Hands-on Guide](./hands-on-lab-sharepoint-access.md)
