# Vacation Planer Agent Lab: Build an Agent with wx.ai Agent Lab

In this lab we will create an agent using watsonx.ai Agent Lab. Before diving in, there is a short overview of Agent Lab discussing some of its key features. If you want to skip the overview and start building your agent, go to [Step 1 - Build a vacation-planning agent with Agent Lab 😎](#build-a-vacation-planning-agent-with-agent-lab). The required steps for Lab conclude at the end of [Step 2 - Deploy the agent using 1-click deployment 🚀](#deploy-the-agent-using-1-click-deployment). You should complete Step 1 and Step 2 in order to be able to complete the following labs in the class. The remaining content in [Additional tips for implementing various use cases in Agent Lab 💡](#additional-tips-for-implementing-various-use-cases-in-agent-lab) is optional and not required for the following labs.


## Table of Contents 📋
- [Vacation Planer Agent Lab: Build an Agent with wx.ai Agent Lab](#vacation-planer-agent-lab-build-an-agent-with-wxai-agent-lab)
  - [Table of Contents 📋](#table-of-contents-)
- [Overview of Agent Lab](#overview-of-agent-lab)
  - [Main Strengths:](#main-strengths)
- [](#)
- [Build a vacation-planning agent with Agent Lab](#build-a-vacation-planning-agent-with-agent-lab)
- [](#-1)
- [Deploy the agent using 1-click deployment](#deploy-the-agent-using-1-click-deployment)
    - [Yay!!! Now you have officially completed Lab! 🚀](#yay-now-you-have-officially-completed-lab-)
- [Additional tips for implementing various use cases in Agent Lab](#additional-tips-for-implementing-various-use-cases-in-agent-lab)


# Overview of Agent Lab

The Agent Lab feature of watsoxn.ai enables you to easily build and customize your AI agent with minimal coding. You define the parameters of the interaction between the agent and the end user, including the foundation model, framework, architecture, and tools that the agent uses to accomplish a task.

In a real-world scenario, the agent takes the next best step based on the current state of the interaction. The foundation model within the agent picks one or several external tools based on the prompts submitted by the end user. The agent framework then uses a process called tool calling, which is also referred to as function calling, to search for information from multiple sources and generate a response.

Check [this document](https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-agent-lab.html?context=wx&pos=2) for the latest information about Agent Lab.


## Main Strengths:
Below are some of the Agent Lab strengths that you can can use when demoing this feature to your clients.
+ **Low-code agent builder**: 
  - Facilitates building agents
  - Enables a wider range of users with different levels of technical expertise
+ **1-click deployment**: 
  - Facilitates scaling agentic AI applications
  - Reduces time to value by allowing quick deployment
+ **Provides a great starting point for developers**:
  - Developers and pro-code users can leverage Agent Lab's deployment notebook as a head start, and further customize it to build tailored applications


#
# Build a vacation-planning agent with Agent Lab

If this is your first time in this account, you will need to first create a project to be able to start using Agent Lab. Once you created a project, go to that project, then go to the Assets tab and click on New asset. 
![image](./images/1-new%20asset-updated.png)


Then from the list of assets, click on **"Build an AI agent to automate tasks"**.
![image](./images/2-asset%20-%20agent%20lab-updated.png)


When opening the Agent Lab for the first time, you will need to associate it with an ai runtime service. Click on Associate service.
![image](./images/3-associate%20s.png)

Select the available runtime and click on Associate.
![image](./images/4-associate%20s.png)

Then go back to the tab for creating a new asset and start your Agent Lab asset. This brings us to the main page for cretaing an agent with the Agent Lab.
Here, on the left side of the screen under **"Build"**, you can set up and configure your agent, and on the right side under **"Agent preview"** you will see how those changes are going to be reflected in the agent.

When deifning the agent on the "Build" side, you can select the LLM and change the model parameters (e.g. temperature, max token, etc.). By clicking on Setup, you can define the name of the agent and provide a short description of what is does.

![image](./images/5-setup-updated.png)

Then lower on the Build side, you can "Configure" the agent by selecting the Framework and the Architecture. Currently LangGrpah is the only Framework available and ReAct is the only Architecture available. More frameworks and architectures will be added to the Agent Lab in future releases.

Then under the "Instruction" section, you can provide an instruction for how you want the agent to behave. This is very important and often overlooked step. Just like how a well crafted prompt will impact the behavior of an LLM, the instruction to an agent also affects its outcome.

In this example, we are building a Travel Concierge agent that helps the users plan their vacation. Copy the following instruction and paste it in the instruction for this agent.

"""
*You are a vacation planning assistant that helps users plan their vacations.* 

*If you were asked for a detailed vacation plan, you must use the budget limit provided by the user and utilize Google Search to retrieve up-to-date information about activities, dining options, and travel logistics to suggest a detailed day-by-day vacation plan.*
*Use Google Search tool to fetch real-time information for:*
*- Flight options*
*- Car rental services*
*- Local grocery stores (e.g., Times Supermarket)*
*- Restaurant menus and reviews*
*- Activity bookings (snorkeling, ziplining, guided tours)*

*If you were asked question about the weather of a travel destination, use Weather tool to get real time weather of a city to facilitate making of travel plans.*
"""

![image](./images/6-agent%20config-v2-updated.png)


Then you can select the tools that you want this agent to have. Google Search is the default tool. you can click on Select Tool to choose from a list of available tools. For the Travel Cocierge agent, we will use two tools, Google Search and Weather.

![image](./images/7-select%20tools-v2.png)

Once you are done with defining your agent, you can save your work as an Agent and come back and edit it again later, or save it as a deployment notebook that would give you a nice notebook starting point for further customization.

![image](./images/8-save%20agent-v2.png)

Now, let's test our agent! First, we will ask it to plan our vacation given a specific budget. In the Preview section on the right, test the following question.

Question: *"Give me a detailed 5-day vacation plan to San Francisco, CA with budget limit of $5000."*

![image](./images/detailed%20travel%20plan.png)

If we go to the end of the response from our agent, we can click on __"How did I get this answer?"__ to gain an insight into what tool our agent has used and how the output is generated. In this case, we can see that the agent is correctly using Google Search to find the relevant information and plan our vacation.

![image](./images/travel%20plan-%20tool%20result-updated.png)


Let's try another example in which the agent should use the Weather tool.

Question: *"How is the weather in SF from March 5 to March 10?"*

![image](./images/SF%20weather%20results.png)

Nice! The agent is using the weather tool now. So our agent was successful in choosing the right tool for both user requests.

#
# Deploy the agent using 1-click deployment

Once you are happy with your agent's performance, you can deploy your agent as an AI service using Agent Lab's 1-click deployment. To do so click on the Deploy icon on the top right of your agent lab page. The Deploy page opens (see below). To continue, you first need to "Create" an API key. Click on "Create". 

![image](./images/10-deploy-updated.png)

This will take you to another page to create your API key. __Create and Save your API Key. You will need this API Key in order to integrate your Travel Concierge agent into Watsonx Orchestrator.__

![image](./images/11-create%20key.png)

Copy the API key and save it somewhere or click download to save it. You won’t be able to see this API key again, so you can’t retrieve it later.

![image](./images/save%20API%20Key.png)

After you created and saved your API Key, go back to the page for "Deploy as an AI Service". Now the "Create" link is replaced with "Reload". Click on "Reload" to reload your API Key. 

![image](./images/relaod-key-new-dep-space-updated.png)

---

> **💡 TIP: 🛠️ Troubleshooting API Key Creation**
>
> If the pop-up window to copy or download your API key doesn’t appear, follow these steps to retrieve and update it:
> 1. Manually generate a new API key:
> - Go to IBM Cloud (https://cloud.ibm.com/).
> - Go to Manage > Access (IAM).
> - Create a new API key and save it for later use.
> 2. Update your API key in wx.ai:
> - Go to wx.ai and open your profile.
> - Navigate to User API Key.
> - Click Rotate to update to the latest key.

---


Next you need to create a new deployment space. Click on "New Deployment Space" to go to the page for creating a new deployment space. On this page, name the space, set the deployment stage, and select the runtime service from the drop down menu. Then click on "Create" to create your new space.

![image](./images/13-create%20deployment%20space.png)

When the deployment space is ready, go back to the "Deploy as as AI Service" page and "Reload" the deployment space. Then click on Deploy.

![image](./images/15-ready%20to%20deploy.png)

The deployment will initialize and after a couple of minutes the status will change to "Deployed".

![image](./images/17-deployed.png)

---

> **💡 TIP: 🛠️ Troubleshooting Deployment Failures**
>
> If your deployment fails, the issue may be related to your API key. Try the following steps to resolve it:
> 1. Generate a new API key:
> - Go to IBM Cloud (https://cloud.ibm.com/).
> - Navigate to Manage > Access (IAM).
> - Create a new API key and copy/download it for later use.
> 2. Update your API key in wx.ai:
> - Go to your wx.ai profile.
> - Navigate to User API Key.
> - Click Rotate to update to the latest key.
> 3. Redeploy your agent.

---

Once deployed, click on the agent name to see the information about this deployment (see below). You can find your deployment ID on the right panel. __Save your Deployment ID as you will need it for future integration with your Travel Concierge agent into Watsonx Orchestrate.__

![image](./images/18-deployment%20info-updated.png)

In order to implement our Travel Concierge agent as an external agent in Watsonx Orchestrate, in addition to API Key and Deployment ID, we also need the Service URL and the Space ID. The URL can also be found in the beginning part of the endpoints from the deployment info page, i.e. "https://us-south.ml.cloud.ibm.com".

Now, you only need the __Space ID__ to have all the required information from Lab 1. For Space ID, from hamburger menu on top left, go to "Deployments". Then click on the “Spaces” tab and click on the deployment space you created.  

![image](./images/space%20ID-1.png)

In your deployment space, click on the "Manage" tab, and save your Space ID for using it later in Lab 3 and 4.

![image](./images/space%20ID-2-updated.png)

### Yay!!! Now you have officially completed Lab! 🚀

The rest of this GitHub repo provides some additional tips on implementing various use cases in Agent Lab.

# Additional tips for implementing various use cases in Agent Lab

Below are some practical tips that can help you make your desired agent with Agent Lab:

+ ### It takes trial and error!
  - Yup, keep experimenting to get what you want.
+ ### Tailoring instructions is very important for agents, just like prompt engineering for LLMs 
  - For instance, your instrcution should include:
    - What task you want the agent to perform;
    - What tools the agent has access to;
    - How and when those tools should be used;
+ ### Tips about custom tools
  - Adding a custom tool in Agent Lab is temporarily disabled (as of early March 2025) but will come back soon! Workaround in the meantime: save your agent as a deployment notebook, and then add your custom fuction or tool through custom code.
+ ### Tips about doc search tool
  - In the latest Agent Lab release (as of early March 2025), the Doc Search tool requires selecting an existing vector index from your project's available indexes. Currently, Agent Lab does not support document vectorization directly. To use Doc Search, first vectorize your document externally and create a vector index. Once the index is ready and added to your project, it will automatically appear in the dropdown menu for selection in the Doc Search tool.
    - To vectorize your document, create a new asset using the **Ground gen AI with vectorized documents** feature from the **New asset** list. And once your document is vectorized, return to Agent Lab and select the generated vector index from the dropdown list.
 


