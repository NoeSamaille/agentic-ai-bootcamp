# Watsonx Orchestrate LAB for Travel and Booking Agent [NEW]
### (low-code approach)
This guide walks you through setting up a Hotel Booking system with Watsonx Orchestrate, creating multiple agents that work together.

## Step 1: Connect to the Watsonx Orchestrate Trial instance 

1. Navigate to IBM Cloud page: https://cloud.ibm.com/resources and click on the link "AI / Machine Learning"
2. Select. Watsonx Orchestrate and Click launch to access the trial instance.
   
   ![Create New Agent](images/1.png)
   
   ![Create New Agent](images/2.png)

> Note: You can also login to trial instance from the login link received in your email from IBM TechZone

## Step 2: Create First Agent - Hotel Booking Agent

1. Click "Create new agent" link in the bottom
   
  ![Create New Agent](images/3.png)

3. Select "Create from scratch" option
5. Enter Name as `Hotel Booking Agent`
6. Add this description:

```
You are an AI Agent that helps the user to look for
- Get the hotels in a city of user's choice
- Book hotels per the user's requirements
Do not execute repeated tools
I want the response in Form structure rather than plain JSON
```

  ![Create New Agent](images/4b.png)

5. Click "Create" button
6. Navigate to Toolset section and click "Add tool"

  ![Create New Agent](images/5.png)

7. Select Import and upload these files from the "Hotel Booking Agent - Tools" folder, one by one:
   - `list_hotels_location.json`
   - `hotel_booking_confirmation.json`
   Click Done after selecting the checkbox.

   ![Import Tool](images/6.png)
   
   ![Import Tool](images/7.png)
   
   ![Import Tool](images/8.png)
   
   ![Import Tool](images/9.png)


9. Test the agent with a sample prompt: `Provide me the best hotels in Mumbai`

   ![Test Agent](images/10b.png)

10. Click "Deploy" to publish the agent as Live

    ![Test Agent](images/11b.png)

## Step 3: Create Expert Agent - Travel Agent

1. Create another agent with name `Travel Agent` and this description:

```
You are an AI Agent that helps the user to look for
- Search the major cities in a country
- Get the weather info pertaining to a city of the users choice
- Get the hotels in that city through collaborator agent 
- Book hotels per the user requirements through collaborator agent 
Do not execute repeated tools
I want the response in Form structure rather than plain JSON
```

   ![Travel Agent Creation](images/13b.png)

2. Import the following tools from the "Travel Agent - Tools" folder, one by one:
   - `Country_code.JSON`
   - `cities_api.json`
   - `Country_info.JSON`
   - `weather_info_demo.json`
   - `weather_forecast_week.json`

   ![Travel Agent Tools](images/14.png)

3. Add Knowledge Base from these files from the "Travel Agent - Knowledge (RAG)" folder:
   - `City Info.xlsx`
   - `Country City Info.csv`
   - `Flight Booking Tips for Smart Travelers.docx`
   - `General Travel Information for International Travelers.docx`
   - `airports.csv`
   - `IATA_Airport.csv`
   - `IATA_Airport.xlsx`

   ![Knowledge Base Files](images/15.png)

   ![Knowledge Base Files](images/16.png)

5. Add this description for the knowledge base:

```
Refer to the documentation
- when the user asks about the cities in a country OR
- when the user asks for best tips on flight booking or when asked some generic information about the travel
```
![Knowledge Base Files](images/17.png)

5. Add the Hotel Booking Agent as a collaborator agent

   ![Add Collaborator Agent](images/19.png)

   ![Add Collaborator Agent](images/20.png)

7. Deploy the agent

![Add Collaborator Agent](images/20.png)

![Add Collaborator Agent](images/22bb.png)


## Using the Agents

After deploying both agents, use these prompts to test the complete flow:

![Add Collaborator Agent](images/23.png)

1. Get country information:
```
Give me information about France
```
Tool used: Country Info.JSON

![Test Agent](images/24b.png)

![Test Agent](images/25b.png)

2. Get major cities:
```
What are the 5 major cities there
```
Tool used: cities_api.json OR Knowledge base

![Test Agent](images/bb.png)

3. Get current weather:
```
What is the weather like in Paris today
```
OR
```
What is the weather like in the nicest city in France
```
Tool used: weather_info_demo.json

![Test Agent](images/bc.png)

4. Get weather forecast:
```
What about the weather there for next week?
```
Tool used: weather_forecast_week.json

![Test Agent](images/bd.png)

5. Find hotels (transfers to collaborator agent):
```
Cool. Provide me the best hotels there
```
Tool used: list_hotels_location.json

![Test Agent](images/bm.png)

6. Book a hotel:
```
Let's go with Hotel de Paris
```
OR
```
Let's go with the expensive one there
```
Tool used: hotel_booking_confirmation.json

![Test Agent](images/bw.png)

