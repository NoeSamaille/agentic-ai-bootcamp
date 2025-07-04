# Creating Agents with IBM watsonx.ai and BeeAI

## Contents

- [Creating Agents with IBM watsonx.ai and BeeAI](#creating-agents-with-ibm-watsonxai-and-beeai)
  - [Contents](#contents)
  - [1 Introduction](#1-introduction)
    - [1.1 Introduction to BeeAI](#11-introduction-to-beeai)
    - [1.2 About this Lab](#12-about-this-lab)
  - [2 Prerequisites](#2-prerequisites)
    - [Technical Requirements](#technical-requirements)
    - [watsonx.ai Environment](#watsonxai-environment)
  - [3 Lab Preparation](#3-lab-preparation)
    - [3.1 Create the Development Environment](#31-create-the-development-environment)
      - [3.1.1 Project Folder](#311-project-folder)
  - [4 Get started with BeeAI](#4-get-started-with-beeai)
    - [Step 1: Chat with your first BeeAI agents](#step-1-chat-with-your-first-beeai-agents)
    - [Step 2: Explore the Code Interpreter](#step-2-explore-the-code-interpreter)
      - [Instructions](#instructions)
    - [Step 3: Explore Observability](#step-3-explore-observability)
      - [Instructions](#instructions-1)
    - [Step 4: Run a multi-agent-workflow](#step-4-run-a-multi-agent-workflow)
      - [Instructions](#instructions-2)
  - [Conclusion](#conclusion)

## 1 Introduction

IBM watsonx.ai is a core component of watsonx, IBM's enterprise-ready AI and data platform that's designed to multiply the impact of AI across an enterprise.

The watsonx platform has three powerful components: the watsonx.ai studio for new foundation models, generative AI, and Machine Learning (traditional AI); the watsonx.data fit-for-purpose data lakehouse that provides the flexibility of a data lake with the performance of a data warehouse; and the watsonx.governance toolkit, which enables AI workflows that are built with responsibility, transparency, and explainability.

![Image](img/image_000001_43f9e0897cdb17f1cd070c4ccdee886c7b6ef067dc0143e87338269299194fd0.png)

The watsonx.ai component (the focus of this lab) makes it possible for enterprises to train, validate, tune, and deploy AI models - both traditional AI and generative AI. With watsonx.ai, enterprises can leverage their existing traditional AI investment as well as exploit the innovations and potential of generative AI builds on foundation models to bring advanced automation and AI-infused applications to reduce cost, improve efficiency, scale, and accelerate the impact of AI across their organizations.

### 1.1 Introduction to BeeAI

[BeeAI](https://i-am-bee.github.io/beeai-framework/) is a framework for building production-ready multi-agent systems in **Python** or **TypeScript**.

**Why BeeAI?**

- 🏆 **Build for your use case**. Implement simple to complex multi-agent patterns using [Workflows](#/python/workflows), start with a [ReActAgent](https://github.com/i-am-bee/beeai-framework/tree/main/python/examples/agents/bee.py), or easily [build your own agent architecture](#/python/agents?id=creating-your-own-agent). There is no one-size-fits-all agent architecture, you need full flexibility in orchestrating agents and defining their roles and behaviors.

- 🔌 **Seamlessly integrate with your models and tools**. GGet started with any model from [Ollama](https://github.com/i-am-bee/beeai-framework/tree/main/python/examples/backend/providers/ollama.py), [Groq](https://github.com/i-am-bee/beeai-framework/tree/main/typescript/examples/backend/providers/groq.ts), [OpenAI](https://github.com/i-am-bee/beeai-framework/tree/main/typescript/examples/backend/providers/openai.ts), [watsonx.ai](https://github.com/i-am-bee/beeai-framework/tree/main/python/examples/backend/providers/watsonx.py), and [more](#/python/backend). Leverage tools from [LangChain](https://github.com/i-am-bee/beeai-framework/tree/main/typescript/examples/tools/langchain.ts), connect to any server using the [Model Context Protocol](#/python/tools?id=using-the-mcptool-class), or build your own [custom tools](#/python/tools?id=using-the-customtool-python-functions). BeeAI is designed to integrate with the systems and capabilities you need.

- 🚀 **Scale with production-grade controls**. Optimize token usage through [memory strategies](#/python/memory), persist and restore agent state via [(de)serialization](#/python/serialization), generate structured outputs, and execute generated code in a sandboxed environment. When things go wrong, BeeAI tracks the full agent workflow through [events](#/python/emitter), collects [telemetry](#/python/instrumentation), logs diagnostic data, and handles [errors](#/python/errors) with clear, well-defined exceptions. Deploying multi-agent systems requires resource management and reliability.

### 1.2 About this Lab

This lab provides hands-on experience developing AI agents using watsonx.ai and the BeeAI framework.

## 2 Prerequisites

### Technical Requirements

- JavaScript runtime [NodeJS > 18](https://nodejs.org/) (ideally installed via [nvm](https://github.com/nvm-sh/nvm)).
- Container system like [Rancher Desktop](https://rancherdesktop.io/) or [Podman Desktop](https://podman-desktop.io/downloads) (VM must be [rootfull machine](https://podman-desktop.io/docs/podman/creating-a-podman-machine)).
  - **Note**: this is only required if you want to leverage the code interpreter and/or the observability features.
- LLM Provider either external [WatsonX](https://www.ibm.com/watsonx) (OpenAI, Groq, ...) or local [ollama](https://ollama.com).

### watsonx.ai Environment

You must have access to a watsonx.ai SaaS environment and an initialized project within that environment. If you do not have one already, it can be provisioned on [TechZone](https://techzone.ibm.com/collection/tech-zone-certified-base-img/journey-watsonx) by selecting the **watsonx.ai/.governance SaaS** environment and selecting **Education** as **Purpose**.

To run this lab, you will need:
- An [IBM Cloud API Key](https://cloud.ibm.com/iam/apikeys).
- Your watsonx.ai SaaS [URL and project ID](https://dataplatform.cloud.ibm.com/developer-access?context=wx).

## 3 Lab Preparation

### 3.1 Create the Development Environment

All lab development will be performed in a single Python project tree. The steps below should work on all platforms.

#### 3.1.1 Project Folder

To contain all the lab exercises, create a parent working folder:

```sh
mkdir beeai-lab
```

## 4 Get started with BeeAI

### Step 1: Chat with your first BeeAI agents

Navigate to your lab folder:

```sh
cd beeai-lab
```

1. Clone the BeeAI starter repository:

```sh
git clone https://github.com/i-am-bee/beeai-framework-starter
cd beeai-framework-starter
```

2. Install the dependencies using `npm ci`.

```sh
npm ci
```

3. Configure your project by filling in missing values in the `.env` file, like the following:

```sh
LLM_CHAT_MODEL_NAME="watsonx"

...OMITTED...

# For Watsonx LLM Adapter
WATSONX_CHAT_MODEL="ibm/granite-3-8b-instruct"
WATSONX_EMBEDDING_MODEL="ibm/slate-125m-english-rtrvr"
WATSONX_API_KEY="<CHANGEME>"
WATSONX_PROJECT_ID="<CHANGEME>"
WATSONX_VERSION="2023-05-29"
WATSONX_REGION="eu-de"
```

4. Run the agent using `npm run start src/agent.ts`.

```bash
npm run start src/agent.ts
```

5. To run an agent with custom prompt, simply do this:

```bash
npm run start src/agent.ts <<< 'Hello Bee!'
```

### Step 2: Explore the Code Interpreter

 The [Bee Code Interpreter](https://github.com/i-am-bee/bee-code-interpreter) is a gRPC service an agent uses to execute an arbitrary Python code safely.

#### Instructions

1. Start all services related to the [`Code Interpreter`](https://github.com/i-am-bee/bee-code-interpreter):
    ```bash
    npm run infra:start --profile=code_interpreter
    ```
2. Run the agent:
    ```bash
    npm run start src/agent_code_interpreter.ts
    ```
3. You can now use prebuilt tools in the `src/agent_code_interpreter.ts` that use the code interpreter, by asking something like:
    ```
    Give me a riddle
    ```
    - Sample output:
    ```
    Agent 🤖 (thought) :  To provide a riddle, I need to fetch one from a source, in this case, I can use the get_riddle function to retrieve a random riddle and its answer.
    Agent 🤖 (tool_name) :  get_riddle
    Agent 🤖 (tool_input) :  {}
    Agent 🤖 (tool_output) :  {"riddle": "What is round as a dishpan, deep as a tub, and still the oceans couldn't fill it up?", "answer": "A sieve"}
    Agent 🤖 (thought) :  The function output contains the riddle and its answer, now I can provide the riddle to the user.
    Agent 🤖 (final_answer) :  Here's a riddle for you: What is round as a dishpan, deep as a tub, and still the oceans couldn't fill it up? Think you can solve it?
    Agent 🤖 :  Here's a riddle for you: What is round as a dishpan, deep as a tub, and still the oceans couldn't fill it up? Think you can solve it?
    ```
4. You can also ask complexe queries that require calculations/code to be defined and ran by your agent, like:
    ```
    What are the monthly repayments on a $948,000 loan at an interest rate of 5.85% over 30 years
    ```
    - Sample output:
    ```
    Agent 🤖 (thought) :  To calculate the monthly repayments on a loan, we can use a financial formula, which can be implemented in Python. 
    ...OMITTED...
    Agent 🤖 :  The monthly repayment on a $948,000 loan at an interest rate of 5.85% over 30 years is approximately $5,592.64.
    ```

### Step 3: Explore Observability
-----------------------------

Get complete visibility of the agent's inner workings via our observability stack.

- [MLFlow](https://mlflow.org/) is used as UI for observability.
- The [Bee Observe](https://github.com/i-am-bee/bee-observe) is the observability service (API) for gathering traces from [Bee Agent Framework](https://github.com/i-am-be/beeai-framework).

#### Instructions

1. Start all services related to [Bee Observe](https://github.com/i-am-bee/bee-observe):
    ```bash
    npm run infra:start --profile=observe
    ```
2. Run the agent:
    ```bash
    npm run start src/agent_observe.ts
    ```
3. Ask something like:
    ```
    What is the current weather in Las Vegas?
    ```
    - Sample output:
    ```
    User 👤 : What is the current weather in Las Vegas?
    Agent 🤖 :  The current weather in Las Vegas is 11.5°C with a relative humidity of 72% and a wind speed of 15.3 km/h.
    ```
4. Visualize the trace in the MLFlow web application: [`http://127.0.0.1:8080/#/experiments/0`](http://localhost:8080/#/experiments/0)

### Step 4: Run a multi-agent-workflow
-----------------------------

Now let's run a multi-agent workflow to help us generate curated content on a given topic.

#### Instructions

1. Run the multi-agent workflow:
    ```bash
    npm run src/agent_workflow.ts
    ```
2. Ask something like:
    ```
    Help me create a blog post around AI agents
    ```
    - Sample output:
    ```
    User 👤 : Help me create a blog post around AI agents
    -> ▶️ preprocess {"input":"Help me create a blog post around AI agents","notes":[]}
    -> ▶️ planner {"input":"Help me create a blog post around AI agents","topic":"AI agents","notes":[]}
    -> ▶️ writer {"input":"Help me create a blog post around AI agents","topic":"AI agents",...
    -> ▶️ editor {"input":"Help me create a blog post around AI agents","topic":"AI agents","notes":[],"plan":"\n# Content ...
    🤖 Answer Introduction to AI Agents: Revolutionizing Business and Automation...
    ```
3. **Note** how `Content Planner`, `Content Writer` and `Editor` agents are working together to provide you with the response. Navigate to the `src/agent_workflow.ts` to see how the workflow has been implemented.

## Conclusion

In this hands-on lab, we explored the BeeAI Framework and its key features, including the Code Interpreter and Observability. We also covered the step-by-step instructions for getting started with the framework. With this knowledge, you can now start building and deploying your own AI-powered agents the BeeAI Framework.
