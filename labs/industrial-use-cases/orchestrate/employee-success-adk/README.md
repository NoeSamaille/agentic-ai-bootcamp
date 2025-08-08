# Hands-on Lab: Creating the Empower agent on Agent builder

The following step-by-step guides you through setting the IBM watsonx Orchestrate Agent builder, creating an agent, adding tools, and other agent to collaborate with your agent on accomplishing tasks.


**Table of content**:
- [Before your begin](#before-your-begin)
- [Empower: An agent for employee success](#empower-an-agent-for-employee-success)
  - [ServiceNow and Customer care examples](#servicenow-and-customer-care-examples)
    - [Customer care and ServiceNow agents](#customer-care-and-servicenow-agents)
    - [Creating the Customer care tools](#creating-the-customer-care-tools)
    - [Creating the ServiceNow tools](#creating-the-servicenow-tools)
    - [Installing ServiceNow and Customer care](#installing-servicenow-and-customer-care)
  - [Agent’s profile](#agents-profile)
  - [Agent’s toolset](#agents-toolset)
  - [Chat preview](#chat-preview)
  - [Deploying Empower agent](#deploying-empower-agent)

## Before your begin

Before you start to follow this tutorial, you must set up your IBM watsonx Orchestrate ADK environment, where you build agents and tools. It also provides a convenient interface for managing credentials, sending requests, and handling responses from the service’s APIs. See the [Installing the watsonx Orchestrate ADK](https://developer.watson-orchestrate.ibm.com/getting_started/installing) and [Installing the watsonx Orchestrate Developer Edition](https://developer.watson-orchestrate.ibm.com/getting_started/wxOde_setup).

## Empower: An agent for employee success

This tutorial is based on a scenario called **Empower: An agent for employee success**. The goal is to create an agent with a key role in assisting employees by answering their questions, providing guidance on supporting tickets, service issues, and referencing FAQs stored in Sharepoint. The following sections walk you through the complete agent building process, from defining the name and description until the deployment process and the agent’s usage on watsonx Orchestrate chat.

### ServiceNow and Customer care examples

After setting up the ADK and starting your local orchestrate server, you need to import the ServiceNow and Customer care examples, both agent and tools, once they are used to create the Empower agent. The following sections make available the files that are needed to build the ServiceNow and Customer care examples, and how to install them.

#### Customer care and ServiceNow agents

The following section guides you to create the Customer care and ServiceNow agents.

1.  Create a folder to structure your agents and tools. For instance, name this folder as **agents**.
2.  In the new folder, create a YAML file with a text editor of your preference. Name the file as **customer\_care\_agent**.
3.  Insert the following code into the `customer_care_agent.yaml` file.
    
    ```yaml
    spec_version: v1
    style: react
    name: customer_care_agent
    llm: watsonx/meta-llama/llama-3-2-90b-vision-instruct
    description: >
        You are an agent who specializes in customer care for a large healthcare institution. You should be compassionate
        to the user.
        
        You are able to answer questions around benefits provided by different plans, the status of a claim,
        and are able to help direct people to the nearest provider for a particular ailment.
    instructions: >
        Use the search_healthcare_providers tool to search for providers. If more than 1 is returned format as a github
        formatted markdown table. Otherwise simply return the output in a kind conversational tone. Do not expand speciality acronyms.
        
        Use the get_healthcare_benefits tool to fetch the benefits coverage for a particular ailment, or for generic plan 
        comparisons. Respond to get_healthcare_benefits requests in a github style formatted markdown table. Be specific about
        the expected coverage type if a particular condition is mentioned.
        
        Use the get_my_claims tool to fetch your open medical claims. Make sure to respond in a direct tone and 
        do not negotiate prices. Format the output of get_my_claims as a github style markdown table.
    collaborators:
        - service_now_agent
    tools:
        - search_healthcare_providers
        - get_healthcare_benefits
        - get_my_claims
    ```
    
4.  Save your file.
5.  Create another YAML file, but name it as **service\_now\_agent**.
6.  Insert the following code into the `service_now_agent.yaml` file.
    
    ```yaml
    spec_version: v1
    style: react
    name: service_now_agent
    llm: watsonx/meta-llama/llama-3-2-90b-vision-instruct
    description: >
        You are an agent who specializes in customer care for a large healthcare institution. You should be compassionate
        to the user.
        
        You are able to help help a user create tickets in service now for processing by a human later. Examples of when to do
        do this include for adding members to plans or helping users with documentation.
    instructions: >
        If a user is having difficulty either generating benefits documents or adding additional members to their plan,
        create a new incident for our support team using service_now_create_incident tool. Be compassionate about the user
        facing difficulty.
        
        The output of get_service_now_incidents should be formatted as a github style formatted markdown table.
    collaborators: []
    tools:
        - create_service_now_incident
        - get_my_service_now_incidents
        - get_service_now_incident_by_number
    ```
7.  Save your file.

Up until here, you created the agents that are needed for Customer care and ServiceNow examples.

#### Creating the Customer care tools

The following section guides you to create the tools for Customer care example.

1.  Create a new folder to insert the tools of your examples. For instance, name this folder as **tools**.
2.  In the new folder, create another one to insert the customer care tools. Name this folder as **customer-care**.
3.  In the **customer-care** folder, create a Python file with a text editor of your preference. Name the file as **get\_healthcare\_benefits**.
4.  Insert the following code into the `get_healthcare_benefits.py` file.

    ```python
    from enum import Enum
    
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
    import requests
    
    class Plan(str, Enum):
        HDHP = 'HDHP'
        HDHP_Plus = 'HDHP Plus'
        PPO = 'PPO'
    
    
    @tool
    def get_healthcare_benefits(plan: Plan, in_network: bool = None):
        """
        Retrieve a comprehensive list of health benefits data, organized by coverage type and plan variant.
        This data outlines details such as annual deductibles, out-of-pocket maximums, and various co-pays
        or percentages for medical services under different network plans (HDHP, HDHP Plus, and PPO).
    
        :param plan: Which plan the user is currently on, can be one of "HDHP", "HDHP Plus", or "PPO". If not provided all plans will be returned.
        :param in_network: Whether the user wants coverage for in network or out of network. If not provided both will be returned.
        :returns: A list of dictionaries, where each dictionary contains:
                - 'Coverage': A description of the coverage type (e.g., 'Preventive Services')
                - 'HDHP (In-Network)': The cost/percentage coverage for an in-network HDHP plan
                - 'HDHP (Out-of-Network)': The cost/percentage coverage for an out-of-network HDHP plan
                - 'HDHP Plus (In-Network)': The cost/percentage coverage for an in-network HDHP Plus plan
                - 'HDHP Plus (Out-of-Network)': The cost/percentage coverage for an out-of-network HDHP Plus plan
                - 'PPO (In-Network)': The cost/percentage coverage for an in-network PPO plan
                - 'PPO (Out-of-Network)': The cost/percentage coverage for an out-of-network PPO plan
        """
        resp = requests.get(
            'https://get-benefits-data.1sqnxi8zv3dh.us-east.codeengine.appdomain.cloud/',
            params={
                'plan': plan,
                'in_network': in_network
            }
        )
        resp.raise_for_status()
        return resp.json()['benefits']
    ```

5.  Save your file.
6.  In the same folder, create another Python file and name it as **get\_my\_claims**.
7.  Insert the following code into the `get_my_claims.py` file.
    
    ```python
    from ibm_watsonx_orchestrate.agent_builder.tools import tool
    
    
    @tool
    def get_my_claims():
        """
        Retrieve detailed information about submitted claims including claim status, submission and processing dates,
        amounts claimed and approved, provider information, and services included in the claims.
    
        :returns: A list of dictionaries, each containing details about a specific claim:
                - 'claimId': Unique identifier for the claim
                - 'submittedDate': Date when the claim was submitted
                - 'claimStatus': Current status of the claim (e.g., 'Processed', 'Pending', 'Rejected')
                - 'processedDate': Date when the claim was processed (null if not processed yet)
                - 'amountClaimed': Total amount claimed
                - 'amountApproved': Amount approved for reimbursement (null if pending, 0 if rejected)
                - 'rejectionReason': Reason for rejection if applicable (only present if claimStatus is 'Rejected')
                - 'provider': Provider details, either as a simple string or a dictionary with detailed provider information
                - 'services': List of services included in the claim, each with:
                    - 'serviceId': Identifier for the service
                    - 'description': Description of the service provided
                    - 'dateOfService': Date the service was provided
                    - 'amount': Amount charged for the service
        """
        claims_data = [
            {
                "claimId": "CLM1234567",
                "claimStatus": "Processed",
                "amountClaimed": 150.00,
                "amountApproved": 120.00,
                "provider": {
                    "name": "Healthcare Clinic ABC",
                    "providerId": "PRV001234",
                    "providerType": "Clinic"
                },
                "services": [
                    {"serviceId": "SVC001", "description": "General Consultation", "dateOfService": "2025-02-28", "amount": 100.00},
                    {"serviceId": "SVC002", "description": "Blood Test", "dateOfService": "2025-02-28", "amount": 50.00}
                ]
            },
            {
                "claimId": "CLM7654321",
                "claimStatus": "Pending",
                "amountClaimed": 300.00,
                "amountApproved": None,
                "provider": "City Health Hospital",
                "services": [
                    {"serviceId": "SVC003", "description": "X-ray Imaging", "dateOfService": "2025-02-14", "amount": 300.00}
                ]
            },
            {
                "claimId": "CLM9876543",
                "claimStatus": "Rejected",
                "amountClaimed": 200.00,
                "amountApproved": 0.00,
                "rejectionReason": "Service not covered by policy",
                "provider": "Downtown Diagnostics",
                "services": [
                    {"serviceId": "SVC003", "description": "MRI Scan", "dateOfService": "2025-02-05", "amount": 200.00}
                ]
            }
        ]
    
        return claims_data
    ```
    
8.  Save your file.
9.  In the same folder, create another Python file and name it as **search\_healthcare\_providers**.
10.  Insert the following code into the `search_healthcare_providers.py` file:

    ```python
    from typing import List

    import requests
    from pydantic import BaseModel, Field
    from enum import Enum

    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


    class ContactInformation(BaseModel):
        phone: str
        email: str


    class HealthcareSpeciality(str, Enum):
        GENERAL_MEDICINE = 'General Medicine'
        CARDIOLOGY = 'Cardiology'
        PEDIATRICS = 'Pediatrics'
        ORTHOPEDICS = 'Orthopedics'
        ENT = 'Ear, Nose and Throat'
        MULTI_SPECIALTY = 'Multi-specialty'


    class HealthcareProvider(BaseModel):
        provider_id: str = Field(None, description="The unique identifier of the provider")
        name: str = Field(None, description="The providers name")
        provider_type: str = Field(None, description="Type of provider, (e.g. Hospital, Clinic, Individual Practitioner)")
        specialty: HealthcareSpeciality = Field(None, description="Medical speciality, if applicable")
        address: str = Field(None, description="The address of the provider")
        contact: ContactInformation = Field(None, description="The contact information of the provider")


    @tool
    def search_healthcare_providers(
            location: str,
            specialty: HealthcareSpeciality = HealthcareSpeciality.GENERAL_MEDICINE
    ) -> List[HealthcareProvider]:
        """
        Retrieve a list of the nearest healthcare providers based on location and optional specialty. Infer the
        speciality of the location from the request.


        :param location: Geographic location to search providers in (city, state, zip code, etc.)
        :param specialty: (Optional) Medical specialty to filter providers by (Must be one of: "ENT", "General Medicine", "Cardiology", "Pediatrics", "Orthopedics", "Multi-specialty")

        :returns: A list of healthcare providers near a particular location for a given speciality
        """
        resp = requests.get(
            'https://find-provider.1sqnxi8zv3dh.us-east.codeengine.appdomain.cloud',
            params={
                'location': location,
                'speciality': specialty
            }
        )
        resp.raise_for_status()
        return resp.json()['providers']
    ```


Up until here, you created the tools for the customer care example.

#### Creating the ServiceNow tools

The following section guides you to create the tools for ServiceNow example.

1.  In the **tools** folder, create a new folder named as **servicenow**.
2.  In the servicenow folder, create a Python file and name it as **create\_service\_now\_incident**.
3.  Insert the following code into the `create_service_now_incident.py` file.
    
    ```python
    import base64
    import json
    from typing import Optional
    
    import requests
    from requests.auth import HTTPBasicAuth
    
    from pydantic import Field, BaseModel
    
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
    from ibm_watsonx_orchestrate.run import connections
    
    from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType
    
    CONNECTION_SNOW = 'service-now'
    
    class ServiceNowIncidentResponse(BaseModel):
        """
        Represents the response received after creating a ServiceNow incident.
        """
        incident_number: str = Field(..., description='The incident number assigned by ServiceNow')
        sys_id: str = Field(..., description='The system ID of the created incident')
    
    
    class ServiceNowIncident(BaseModel):
        """
        Represents the details of a ServiceNow incident.
        """
        incident_number: str = Field(..., description='The incident number assigned by ServiceNow')
        short_description: str = Field(..., description='A brief summary of the incident')
        description: Optional[str] = Field(None, description='Detailed information about the incident')
        state: str = Field(..., description='Current state of the incident')
        urgency: str = Field(..., description='Urgency level of the incident')
        created_on: str = Field(..., description='The date and time the incident was created')
    
    
    @tool(
        permission=ToolPermission.READ_WRITE,
        expected_credentials=[
            {"app_id": CONNECTION_SNOW, "type": ConnectionType.BASIC_AUTH}
        ]
    )
    def create_service_now_incident(
            short_description: str,
            description: str = None,
            urgency: int = 3
    ):
        """
        Create a new ServiceNow incident.
    
        :param short_description: A brief summary of the incident.
        :param description: Detailed information about the incident (optional).
        :param urgency: Urgency level (1 - High, 2 - Medium, 3 - Low, default is 3).
        :returns: The created incident details including incident number and system ID.
        """
        creds = connections.basic_auth(CONNECTION_SNOW)
        base_url = creds.url
        url = f"{base_url}/api/now/table/incident"
    
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        payload = {
            'short_description': short_description,
            'description': description,
            'urgency': urgency
        }
    
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            auth=HTTPBasicAuth(creds.username, creds.password)
        )
        response.raise_for_status()
        data = response.json()['result']
    
        number, sys_id = data['number'], data['sys_id']
    
        url = f"{base_url}/api/now/table/incident/{sys_id}"
        response = requests.get(
            url,
            headers=headers,
            json=payload,
            auth=HTTPBasicAuth(creds.username, creds.password)
        )
        response.raise_for_status()
        data = response.json()['result']
    
        return ServiceNowIncident(
            incident_number=data['number'],
            sys_id=data['sys_id'],
            short_description=data['short_description'],
            description=data.get('description', ''),
            state=data['state'],
            urgency=data['urgency'],
            created_on=data['opened_at']
        ).model_dump_json()
    
    # if __name__ == '__main__':
    #     incident = create_service_now_incident(short_description='Test Incident', description='This is a test incident')
    #     print(json.dumps(incident.dict(), indent=2))
    
    ```
    
4.  Save your file.
5.  In the same folder, create another Python file and name it as **get\_my\_service\_now\_incidents**.
6.  Insert the following code into the `get_my_service_now_incidents.py` file.
    
    ```python
    import json
    from typing import Optional, List
    
    import requests
    from pydantic import Field, BaseModel
    import base64
    
    from requests.auth import HTTPBasicAuth
    
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
    from ibm_watsonx_orchestrate.run import connections
    
    from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType
    
    
    CONNECTION_SNOW = 'service-now'
    
    class ServiceNowIncident(BaseModel):
        """
        Represents the details of a ServiceNow incident.
        """
        incident_number: str = Field(..., description='The incident number assigned by ServiceNow')
        short_description: str = Field(..., description='A brief summary of the incident')
        description: Optional[str] = Field(None, description='Detailed information about the incident')
        state: str = Field(..., description='Current state of the incident')
        urgency: str = Field(..., description='Urgency level of the incident')
        created_on: str = Field(..., description='The date and time the incident was created')
    
    @tool(
        expected_credentials=[
            {"app_id": CONNECTION_SNOW, "type": ConnectionType.BASIC_AUTH}
        ]
    )
    def get_my_service_now_incidents() -> List[ServiceNowIncident]:
        """
        Fetch all ServiceNow that the user was the author of.
    
        :returns: The incident details including number, system ID, description, state, and urgency.
        """
        creds = connections.basic_auth(CONNECTION_SNOW)
        base_url = creds.url
        url = f"{base_url}/api/now/table/incident"
    
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        query_params = {}
        query_params['sys_created_by'] = 'admin'
        
        response = requests.get(
            url,
            headers=headers,
            params=query_params,
            auth=HTTPBasicAuth(creds.username, creds.password)
        )
        response.raise_for_status()
        data = response.json()['result']
        
        lst =  [ServiceNowIncident(
            incident_number=d['number'],
            short_description=d['short_description'],
            description=d.get('description', ''),
            state=d['state'],
            urgency=d['urgency'],
            created_on=d['opened_at']
        ) for d in data]
        lst.sort(key=lambda o: o.created_on, reverse=True)
        lst = lst[:min(len(lst), 10)]
        return lst
    
    # if __name__ == '__main__':
    #     incidents = get_my_service_now_incidents()
    #     print(incidents)
    ```
    
7.  Save your file.
8.  In the same folder, create another Python file and name as **get\_service\_now\_incident\_by\_number**.
9.  Insert the following code into the `get_service_now_incident_by_number.py` file.
    
    ```python
    import json
    from typing import Optional
    
    import requests
    from pydantic import Field, BaseModel
    import base64
    
    from requests.auth import HTTPBasicAuth
    
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
    from ibm_watsonx_orchestrate.run import connections
    
    from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType
    
    CONNECTION_SNOW = 'service-now'
    
    class ServiceNowIncident(BaseModel):
        """
        Represents the details of a ServiceNow incident.
        """
        incident_number: str = Field(..., description='The incident number assigned by ServiceNow')
        short_description: str = Field(..., description='A brief summary of the incident')
        description: Optional[str] = Field(None, description='Detailed information about the incident')
        state: str = Field(..., description='Current state of the incident')
        urgency: str = Field(..., description='Urgency level of the incident')
        created_on: str = Field(..., description='The date and time the incident was created')
    
    @tool(
        expected_credentials=[
            {"app_id": CONNECTION_SNOW, "type": ConnectionType.BASIC_AUTH}
        ]
    )
    def get_service_now_incident_by_number(incident_number: str):
        """
        Fetch a ServiceNow incident based on incident ID, creation date, or other filters.
        
        :param incident_number: The uniquely identifying incident number of the ticket.
        :returns: The incident details including number, system ID, description, state, and urgency.
        """
        creds = connections.basic_auth(CONNECTION_SNOW)
        base_url = creds.url
        url = f"{base_url}/api/now/table/incident"
    
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        query_params = {}
        if incident_number:
            query_params['number'] = incident_number
        
        response = requests.get(
            url,
            headers=headers,
            params=query_params,
            auth=HTTPBasicAuth(creds.username, creds.password)
        )
        response.raise_for_status()
        data = response.json()['result']
        data = data[0]  # Assuming only one incident is returned
        
        return ServiceNowIncident(
            incident_number=data['number'],
            short_description=data['short_description'],
            description=data.get('description', ''),
            state=data['state'],
            urgency=data['urgency'],
            created_on=data['opened_at']
        ).model_dump_json()
    
    # if __name__ == '__main__':
    #     incident = fetch_service_now_incident(incident_number='INC0010311')
    #     print(json.dumps(incident.dict(), indent=2))
    ```
    
Up until here, you created the tools for the service now example. Before finishing, you must create the requirements file.

10.  Into the **servicenow** folder, create a TXT file named as **requirements**.
11.  Insert the following code into the `requirements.txt` file.
    
```
requests
```

You finished to create the files that are needed to install the Customer care and ServiceNow examples.

#### Installing ServiceNow and Customer care

The following section guides you to install the ServiceNow and Customer care examples.

1.  Start the watsonx Orchestrate Developer Edition local server `orchestrate server start --env-file={{The path of your .env file}}`.
2.  Signup for a Sevice Now account at `https://developer.servicenow.com/dev.do`.
3.  Validate your email address (check email).
4.  On the landing page, click start building. This allocates a new instance of ServiceNow for you.
5.  Back on the landing page, click your profile icon on the upper right. Under “My instance”, click manage instance password.
6.  In the terminal, create an application connection by using these credentials:

    ```bash
    orchestrate connections add -a service-now
    ```
    
    ```bash
    orchestrate connections configure -a service-now --env draft --type team --kind basic --url <the instance url>
    ```
    
    ```bash
    orchestrate connections set-credentials -a service-now --env draft -u admin -p '<password from modal>'
    ```
    
7.  In the terminal, navigate to the **customer-care** folder and run the following commands to import the customer care tools:
    
    ```bash
    orchestrate tools import -k python -f ./get_my_claims.py
    ```
    
    ```bash
    orchestrate tools import -k python -f ./get_healthcare_benefits.py
    ```
    
    ```bash
    orchestrate tools import -k python -f ./search_healthcare_providers.py
    ```
    
8.  Go to the **servicenow** folder and install the tools by running the following commands:
    
    ```bash
    orchestrate tools import -k python -f ./create_service_now_incident.py -r ./requirements.txt -a service-now
    ```
    
    ```bash
    orchestrate tools import -k python -f ./get_my_service_now_incidents.py -r ./requirements.txt -a service-now
    ```
    
    ```bash
    orchestrate tools import -k python -f ./get_service_now_incident_by_number.py -r ./requirements.txt -a service-now
    ```
    
9.  Go to your agents folder and import the agents created previously:
    
    ```bash
    orchestrate agents import -f service_now_agent.yaml
    ```
    
    ```bash
    orchestrate agents import -f customer_care_agent.yaml
    ```
    
10.  Run `orchestrate chat start`.

When you run the chat, you must be able to see a list of agents in your local chat interface.

### Agent’s profile

This section shows how to define the name and description of your agent. This step gives your agent a clear purpose and helps guide how it interacts with users.

1.  From the IBM watsonx Orchestrate chat page, click **Manage agents**.
2.  Click **Create agent**.
3.  Choose **Create from Scratch**.
4.  In the Name field, insert **Empower** and in the **Description**, insert a text as you prefer to describe the agent. Suggestion: “This agent’s role is to assist employees by answering their questions, providing guidance on supporting tickets, service issues, and referencing FAQs stored in Sharepoint”.
5.  Click **Create** to complete.

You finished working on the profile.

### Agent’s toolset

This section guides you through how to equip your agent with tools, and how to add other agents to collaborate in accomplishing tasks.

1.  From the Empower agent management screen, click **Toolset**.
2.  In Tools, click **Add tool**, and select **Add from local instance**.
3.  Select the **get\_healthcare\_benefits** tool, and click **Add to agent**.
4.  In **Agents**, add the agent that collaborates with your agent on running tasks. Click **Add agent**.
5.  Click **Add from local instance**, select **service\_now\_agent**, and click **Add to agent**.

You finished working on the toolset.

### Chat preview

This section shows how you can see your agent in action before deploying, allowing you to quickly validate that everything works as expected.

1.  From the Empower agent management screen, type in the chat bar “Show my benefits related to mental health”, and press **Enter**.
2.  Wait for the chat response. You can check how your response was generated by clicking **How did I get this response**.

You finished previewing your chat.

### Deploying Empower agent

This final section guides you to deploy your agent and make it available in the IBM watsonx Orchestrate chat.

1.  Click **Deploy**.
2.  Click **IBM watsonx Orchestrate** to return for the chat page.
3.  In the **Agents** list, select the Empower agent, and start by using it directly from the watsonx Orchestrate chat page.
4.  You can ask about service now issues, as your agent has the Service now agent collaborating on running tasks.

You completed the process of creating and deploying your Empower agent.
