from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory      # for chat history and chat context importing
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from tools.book_tool import book_appointment
from tools.cancel_tool import cancel_appointment
from langchain_core.prompts import ChatPromptTemplate
from config import OPENAI_API_KEY
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from state import appointment_submitted, submitted_data
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

history = []  

name = submitted_data.get("name")
email = submitted_data.get("email")


system_prompt = f"""
You are Jane, an appointment assistant. You remember all user information given during this conversation.

When user ask to book or cancel an appointment don't ask for any personal information or appointent related information directly proceed for tool calling.
When asked about personal information, answer using the stored information from previous messages.
If user information is not available, ask politely for it.
Only use the provided tools to perform booking and cancelling actions.
rRturn appointment related responses with available user information.

1. Multiple Action Hanldling:
    When there asks for multiple actions in single query,ask for confirmation for every action exclude first action, after completing first action, ask for confirmation to move to next one.
    Eg. User: "Cancel my appointment and then book a new one."
            You must cancel the appointment first
            Then ask for confirmation to book a new one and then go for booking.

2. Chat History Handling:
    You will have the chat history with user input the latest message and the previous messages.
    You will have to use the chat history to answer the user queries and keep chat context.
Respond briefly and clearly.
"""


# Chat history is maintained in the memory and it will be used to keep track of the conversation.
# # for react memory agents 
system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)        # initializing memory for chat history


#==============================================================================================

# this is how the LLM will be initialized, we can change this LLM as per our needs
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.8,                        # increased it from 0 to 0.8
    openai_api_key=OPENAI_API_KEY
)


#==============================================================================================



# here we can create an add more tools also 
tools = [
    Tool(name="BookAppointment", func=book_appointment, description="Use to book an appointment without any details required."),
    Tool(name="CancelAppointment", func=cancel_appointment, description="Use to cancel an existing appointment."),
]



agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    memory=memory,
    verbose=True,
    agent_kwargs={
        "system_message": SystemMessage(content=system_prompt)          # here we are passing the system prompt to the agent
    }
)




