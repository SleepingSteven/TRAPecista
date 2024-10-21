# Standard library imports
from typing import List, Union, Annotated, Literal
from typing_extensions import TypedDict

# Third-party library imports (langchain and langgraph)
from langchain_core.runnables import chain
from langchain_core.prompts import (
    ChatPromptTemplate, FewShotPromptTemplate, PromptTemplate
)
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, RemoveMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent

# Custom module imports
import llms_and_embeddings
import few_shot_examples
import prompts
from db_interaction import schema_dump as context, db
from retriever_and_tools import search_proper_names, retriever_tool
from llms_and_embeddings import llm
from redis_history import checkpointerredis



example_selector = SemanticSimilarityExampleSelector.from_examples(
    few_shot_examples.examples,
    llms_and_embeddings.embeddings,
    FAISS,
    k=4,
    input_keys=["input"],
)


system_prefix = prompts.few_shot_prefix

example_prompt = PromptTemplate.from_template(
    "User input: {input}\nSQL query: {query}"
)

few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    input_variables=["input"],
    prefix=system_prefix,
    suffix=""
)

full_prompt = prompts.create_sql_prompt(few_shot_prompt, context)

prompt_rag=prompts.prompt_rag

class InputChat(BaseModel):
    messages: List[Union[HumanMessage, AIMessage, SystemMessage]]
    input: str

def modify_state_messages_sql(state):

    return full_prompt.invoke({"input": state["messages"][-1].content, "agent_scratchpad": state["messages"]})

def modify_state_messages_rag(state):

    return prompt_rag.invoke({"agent_scratchpad": state["messages"]})


toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()
tools.append(search_proper_names)
tools_rag=[]
tools_rag.append(retriever_tool)

#-------------------------------------------------------------------------------------------------------------------
#----------- IF THE MODEL YOU ARE USING DOES NOT SUPPORT AUTOMATIC TOOL CALLING USE THIS WORKAROUND ----------------
#-------------------------------------------------------------------------------------------------------------------


# class AgentState(TypedDict):
#     """The state of the agent."""

#     messages: Annotated[Sequence[BaseMessage], add_messages]

#     is_last_step: IsLastStep


# StateSchema = TypeVar("StateSchema", bound=AgentState)
# StateSchemaType = Type[StateSchema]

# STATE_MODIFIER_RUNNABLE_NAME = "StateModifier"

# MessagesModifier = Union[
#     SystemMessage,
#     str,
#     Callable[[Sequence[BaseMessage]], Sequence[BaseMessage]],
#     Runnable[Sequence[BaseMessage], Sequence[BaseMessage]],
# ]

# StateModifier = Union[
#     SystemMessage,
#     str,
#     Callable[[StateSchema], Sequence[BaseMessage]],
#     Runnable[StateSchema, Sequence[BaseMessage]],
# ]


# def _get_state_modifier_runnable(state_modifier: Optional[StateModifier]) -> Runnable:
#     state_modifier_runnable: Runnable
#     if state_modifier is None:
#         state_modifier_runnable = RunnableLambda(
#             lambda state: state["messages"], name=STATE_MODIFIER_RUNNABLE_NAME
#         )
#     elif isinstance(state_modifier, str):
#         _system_message: BaseMessage = SystemMessage(content=state_modifier)
#         state_modifier_runnable = RunnableLambda(
#             lambda state: [_system_message] + state["messages"],
#             name=STATE_MODIFIER_RUNNABLE_NAME,
#         )
#     elif isinstance(state_modifier, SystemMessage):
#         state_modifier_runnable = RunnableLambda(
#             lambda state: [state_modifier] + state["messages"],
#             name=STATE_MODIFIER_RUNNABLE_NAME,
#         )
#     elif callable(state_modifier):
#         state_modifier_runnable = RunnableLambda(
#             state_modifier, name=STATE_MODIFIER_RUNNABLE_NAME
#         )
#     elif isinstance(state_modifier, Runnable):
#         state_modifier_runnable = state_modifier
#     else:
#         raise ValueError(
#             f"Got unexpected type for `state_modifier`: {type(state_modifier)}"
#         )

#     return state_modifier_runnable


# def _convert_messages_modifier_to_state_modifier(
#     messages_modifier: MessagesModifier,
# ) -> StateModifier:
#     state_modifier: StateModifier
#     if isinstance(messages_modifier, (str, SystemMessage)):
#         return messages_modifier
#     elif callable(messages_modifier):

#         def state_modifier(state: AgentState) -> Sequence[BaseMessage]:
#             return messages_modifier(state["messages"])

#         return state_modifier
#     elif isinstance(messages_modifier, Runnable):
#         state_modifier = (lambda state: state["messages"]) | messages_modifier
#         return state_modifier
#     raise ValueError(
#         f"Got unexpected type for `messages_modifier`: {type(messages_modifier)}"
#     )


# def _get_model_preprocessing_runnable(
#     state_modifier: Optional[StateModifier],
#     messages_modifier: Optional[MessagesModifier],
# ) -> Runnable:
#     # Add the state or message modifier, if exists
#     if state_modifier is not None and messages_modifier is not None:
#         raise ValueError(
#             "Expected value for either state_modifier or messages_modifier, got values for both"
#         )

#     if state_modifier is None and messages_modifier is not None:
#         state_modifier = _convert_messages_modifier_to_state_modifier(messages_modifier)

#     return _get_state_modifier_runnable(state_modifier)


# @deprecated_parameter("messages_modifier", "0.1.9", "state_modifier", removal="0.3.0")
# def create_react_agent3(
#     model: LanguageModelLike,
#     tools: Union[ToolExecutor, Sequence[BaseTool], ToolNode],
#     *,
#     state_schema: Optional[StateSchemaType] = None,
#     messages_modifier: Optional[MessagesModifier] = None,
#     state_modifier: Optional[StateModifier] = None,
#     checkpointer: Optional[BaseCheckpointSaver] = None,
#     interrupt_before: Optional[Sequence[str]] = None,
#     interrupt_after: Optional[Sequence[str]] = None,
#     debug: bool = False,
# ) -> CompiledGraph:
#     if state_schema is not None:
#         if missing_keys := {"messages", "is_last_step"} - set(state_schema.__annotations__):
#             raise ValueError(f"Missing required key(s) {missing_keys} in state_schema")

#     if isinstance(tools, ToolExecutor):
#         tool_classes = tools.tools
#         tool_node = ToolNode(tool_classes)
#         tool_executor = tools
#     elif isinstance(tools, ToolNode):
#         tool_classes = tools.tools_by_name.values()
#         tool_node = tools
#         tool_executor = ToolExecutor(tools.tools_by_name.values())
#     else:
#         tool_classes = tools
#         tool_node = ToolNode(tool_classes)
#         tool_executor = ToolExecutor(tool_classes)

#     model = model.bind_tools(tool_classes)

#     system_prompt = f"""\
# You are an assistant that has access to the following set of tools. 
# Here are the names and descriptions for each tool: 

# "retrieve_trap_documentation",
#     "Search and return information about the TRAP (Test result Analysis Platform) web application documentation and on the TRAP package, concerning scripting procedures, coding, tutorials, files, jobs, permissions, and other relevant information." \n

# Given the user input, return the name and input of the tool to use. 
# Return your response as a JSON blob with 'name' and 'arguments' keys.

# The `arguments` has to be a dictionary, with keys corresponding 
# to the argument names and the values corresponding to the requested values. E.g, 'query' in the case of the retrieve_trap_documentation tool. You will always provide it, never leave it blank. You will provide ONLY the json blob with the name of the tool and the arguments to use, with no introduction of explenation.
# """

#     # def should_continue(state: AgentState):
#     #     messages = state["messages"]
#     #     last_message = messages[-1]
#     #     last_message_content = last_message.content
#     #     print("last message content", last_message_content)
#     #     # Check if the last message contains a tool call indication
#     #     if "tool_calls" in last_message.content:
#     #         return "continue"
        
#     #     return "end"

#     class ToolCallRequest(TypedDict):
#         """A typed dict that shows the inputs into the invoke_tool function."""

#         name: str
#         arguments: Dict[str, Any]

#     def summarize_information(state) -> str:
#         """
#         Summarizes the retrieved information in the context of the user's query.

#         Args:
#             retrieved_info: The raw information retrieved by the tool.
#             user_query: The original query made by the user.

#         Returns:
#             A contextually relevant summarized version of the information.
#         """
#         # Contextual summarization logic
#         prompt=ChatPromptTemplate.from_messages(
#             [
#                 ("system", "You are a RAG (Retrieval Augmented Generation) Agent within the TRAPecista chatbot, designed to assist users of the TRAP web application at CERN. TRAP allows users to upload, run, and publish scripts in an environment that connects to CERN's SQL database, specifically the Carvings database used for tracking tests on magnets. Your role is to provide information about the TRAP platform based on the documentation retrieved using the 'retrieve_trap_documentation' tool."),
#                 ("system", "You are responsible for summarizing information retrieved from the TRAP documentation to assist users with scripting tasks and understanding the TRAP environment. You will only focus on the TRAP-related tasks as per the retrieved documentation and will ignore any aspects that fall outside your scope, such as SQL query generation, which is handled by another agent."),
#                 ("system", "Ensure that your summary is based solely on the information retrieved using the 'retrieve_trap_documentation' tool, incorporating any relevant details from previous interactions that help clarify the user’s query. Do not add or assume any information that has not been explicitly retrieved."),
#                 ("system", "You will now take a look at the previous interaction, where you will first find the user question, followed by the information retrieved from the TRAP documentation. Based on this information, provide a concise summary that addresses the user query. If the user asked something unrelated to the documentation, answer normally, without making anything up"),
#                 MessagesPlaceholder("agent_scratchpad")
#             ]
#         )
        
#         finale=prompt.invoke({"agent_scratchpad": state['messages']})
#         summary = model.invoke(finale)
#         print ("summary", summary)

#         return {"messages": summary}
#     def invoke_tool(
#         tool_call_request: ToolCallRequest, config: Optional[RunnableConfig] = None
#     ):
#         """A function that we can use the perform a tool invocation.

#         Args:
#             tool_call_request: a dict that contains the keys name and arguments.
#                 The name must match the name of a tool that exists.
#                 The arguments are the arguments to that tool.
#             config: This is configuration information that LangChain uses that contains
#                 things like callbacks, metadata, etc.See LCEL documentation about RunnableConfig.
# d
#         Returns:
#             output from the requested tool
#         """
#         tool_name_to_tool = {tool.name: tool for tool in tools}
#         name = tool_call_request["name"]
#         print ("nome del tool", name)
#         requested_tool = tool_name_to_tool[name]
#         print ("tool call request", tool_call_request["arguments"])
#         return requested_tool.invoke(tool_call_request["arguments"], config=config)
    
#     print ("ecco lo state modifier", state_modifier)
#     preprocessor = _get_model_preprocessing_runnable(state_modifier, messages_modifier)

#     def invoca(state: AgentState):
#         temp = state["messages"].copy()  # Create a copy of the list
#         print("temporaneo ora", temp)
#         temp.append({"role": "system", "content": system_prompt})
#         nuovo = dict()
#         nuovo["messages"] = temp
#         print("temporaneo dopo", temp)
#         print("state dopo update temporaneo", state)
#         model_runnable = preprocessor | model | JsonOutputParser() | invoke_tool
#         risultato = model_runnable.invoke(nuovo)

#         return {"messages": risultato}
        

#     workflow = StateGraph(state_schema or AgentState)

#     workflow.add_node("agent", invoca)    
#     workflow.add_node("summarize", summarize_information)
#     workflow.set_entry_point("agent")
#     workflow.add_edge("agent", "summarize")
#     workflow.add_edge("summarize", END)
    

# #     # workflow.add_conditional_edges(
# #     #     "agent",
# #     #     should_continue,
# #     #     {
# #     #         "continue": "tool_execution",
# #     #         "end": END,
# #     #     },
# #     # )

# #     # Ensure that tool_execution node is connected back to the agent node
# #     workflow.add_edge("agent", END)

# #     # Add a default edge from tools node to tool_execution if tools are to be executed


#     return workflow.compile(
#         checkpointer=checkpointer,
#         interrupt_before=interrupt_before,
#         interrupt_after=interrupt_after,
#         debug=debug,
#     )

# system_message = SystemMessage(content=full_prompt)




#ReAct agents creation, based on paper https://arxiv.org/abs/2210.03629

agent_executor2 = create_react_agent(llm, tools, state_modifier=modify_state_messages_sql)
agent_executor3 = create_react_agent(llm, tools_rag, state_modifier=modify_state_messages_rag)

class InputChat(TypedDict):
    """Input for the chat endpoint."""

    messages: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(
        ...,
        description="The chat messages representing the current conversation.",
    )

    input: str = Field(
        ...,
        description="The user input for the current step.",
    )


def inp(question: InputChat):
    return({"messages": HumanMessage(content=question["input"]), "question": question["input"], "SQL": [], "RAG": [], "answer": None})



def should_continue(state) -> Literal["agent", "__end__"]:
    """Return the next node to execute."""
    last_message = state["messages"][-1]
    # If there is no function call, then we finish
    if not last_message.tool_calls:
        return "__end__"
    # Otherwise if there is, we continue
    return "SQL"


class GraphState(TypedDict):
    question: str
    messages: Annotated[list, add_messages]
    last_agent: str
    SQL: list
    RAG: list
    answer: AIMessage
    summary:str

# Define the function that calls the model
def call_agent(state: GraphState):
    # If a summary exists, we add this in as a system message
    summary = state.get("summary", "")
    if summary:
        system_message = f"Summary of conversation earlier: {summary}"
        state["messages"] = [SystemMessage(content=system_message)] + state["messages"]
    
   
    response = agent_executor2.invoke({"messages": state["messages"]})
    # We return a list, because this will get added to the existing list
    state["last_agent"]="SQL"
    state["SQL"]=response["messages"][-1]   
    return {"messages": state["messages"], "last_agent": "SQL", "SQL": response["messages"][-1] }

def retriever_agent(state):
    # If a summary exists, we add this in as a system message
    summary = state.get("summary", "")
    if summary:
        system_message = f"Summary of conversation earlier: {summary}"
        state["messages"] = [SystemMessage(content=system_message)] + state["messages"]
    response = agent_executor3.invoke({"messages": state["messages"]})
    state["last_agent"]="RAG"
    state["RAG"]=response["messages"][-1] 
    return {"messages": state["messages"], "last_agent": "RAG", "RAG": response["messages"][-1] }


def route_question(state):
    state["SQL"]=[]
    state["RAG"]=[]
    """
    Route question to sql or RAG.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """

    prompt=prompts.router_prompt

    question_router = prompt | llm | JsonOutputParser()
    try:
        source = question_router.invoke({"question": state["question"], "agent_scratchpad": state["messages"]})  
    except:
        return "RAG"
    
    if source['datasource'] == 'RAG':
        print("---ROUTE QUESTION TO RAG---")

        return "RAG"
    elif source['datasource'] == 'SQL':
        print("---ROUTE QUESTION TO SQL---")
        
        return "SQL"
    
def checker(state):
    if state["last_agent"]=="SQL":
        last_agent= "SQL"
        new_agent= "RAG"
    elif state["last_agent"]=="RAG":
        last_agent= "RAG"
        new_agent=  "SQL"
    if state["SQL"] and state["RAG"]:
        return "Merger" 
    
    """
    Route question to sql or RAG.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """

    prompt=prompts.checker_prompt
    question = state["question"]
    
    question_router = prompt | llm | JsonOutputParser()
    
    try:
        source = question_router.invoke({"question": question, "agent": new_agent, "answer": state[last_agent].content, "agent_scratchpad": state["messages"], "last_agent": last_agent})  
    except:
        return "append"

    if source['proceed'] == 'RAG':
        if state["last_agent"]=="RAG":
            print("---FINISH---")
            return "append"
        else:
            print("---ROUTE QUESTION TO RAG---")

            return "RAG-agent"
    elif source['proceed'] == 'SQL':
        if state["last_agent"]=="SQL":
            print("---FINISH---")
            return "append"
        else:
            print("---ROUTE QUESTION TO SQL---")

            return "SQL-agent"
    elif source['proceed'] == '__end__':
        print("---FINISH---")
        return "append"
    elif 'procceed' not in source:
        print("---FINISH---")
        return "append"
    
def append_state(state):
    # You can do more complex modifications here
    if state["last_agent"]=="SQL":
            return {"messages":state["messages"] + [state["SQL"]]}
    elif state["last_agent"]=="RAG":
            return {"messages":state["messages"] + [state["RAG"]]}
    
def merger(state):
    """
    Merge the two answers from the agents.

    """

    prompt=prompts.merger_prompt
    question = state["question"]
    question_router = prompt | llm 

    answer=question_router.invoke({"question": question, "sql_answer": state["SQL"], "rag_answer": state["RAG"], "agent_scratchpad": state["messages"]})

    state["messages"] = state["messages"] + [answer]
    return {"messages": state["messages"], "answer": answer}

def should_continue(state) -> Literal["summarize_conversation", "__end__"]:
    """Return the next node to execute."""
    messages = state["messages"]
    # If there are more than six messages, then we summarize the conversation
    if len(messages) > 4:
        return "summarize_conversation"
    # Otherwise we can just end
    return END


def summarize_conversation(state):
    # First, we summarize the conversation
    summary = state.get("summary", "")
    if summary:
        # If a summary already exists, we use a different system prompt
        # to summarize it than if one didn't
        summary_message = (
            f"This is summary of the conversation to date: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )
    else:
        summary_message = "Create a summary of the conversation above:"

    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = llm.invoke(messages)
    # We now need to delete messages that we no longer want to show up
    # I will delete all but the last two messages, but you can change this
    new_messages=[]
    try :
        for i in state["messages"]:
            if isinstance(i, HumanMessage):
                new_messages.append(i)
            if isinstance(i, SystemMessage):
                new_messages.append(i)
            if isinstance(i, AIMessage) and i.tool_calls==[]:
                new_messages.append(i)
    except Exception as e:
        pass

    state["messages"]=new_messages

    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-3]]

    return {"summary": response.content, "messages": delete_messages, "answer": state["answer"], "SQL": state["SQL"], "RAG": state["RAG"]}    

def parse(message: dict) -> str:
    
    # Handle direct 'Merger' key case
    if "Merger" in message:
        return message["Merger"]["answer"].content
    
    # Handle direct 'answer' key case
    if "answer" in message:
        return message["answer"].content
    
    # Handle list of messages case
    if isinstance(message, list):
        for item in message:
            if 'Merger' in item and 'answer' in item['Merger']:
                return item['Merger']['answer'].content
            if 'SQL-agent' in item:
                return item['SQL-agent']['SQL'].content
            if 'RAG-agent' in item:
                return item['RAG-agent']['RAG'].content
        output_content = message[-1].get("SQL-agent") or message[-1].get("RAG-agent")
        if output_content:
            return output_content["messages"][-1].content
    
    # Handle 'SQL-agent' or 'RAG-agent' in dict
    output_content = message.get("SQL-agent") or message.get("RAG-agent")
    if output_content and "messages" in output_content:
        if "SQL" in output_content:
            return output_content["SQL"].content
        if "RAG" in output_content:
            return output_content["RAG"].content
    
    # Handle 'summarize_conversation' case
    if "summarize_conversation" in message:
        output_content = message["summarize_conversation"]
        if "answer" in output_content:
            if output_content["answer"]:
                return output_content["answer"].content
            
        for agent in ["SQL", "RAG"]:
            if agent in output_content and output_content[agent]!=[]:
                return output_content[agent].content
    
    # If no conditions match, return an empty string or a default message
    return "There was an error in processing the message. Please contact the system administrator."

#agentic workflow building
def create_workflow():
    workflow = StateGraph(GraphState)
    workflow.set_conditional_entry_point(
        route_question,
        {
            "RAG": "RAG-agent",
            "SQL": "SQL-agent",
        },
    )
    workflow.add_node("RAG-agent", retriever_agent)  # rag
    workflow.add_node("SQL-agent", call_agent)
    workflow.add_node("append", append_state)
    workflow.add_conditional_edges("RAG-agent", checker)
    workflow.add_conditional_edges("SQL-agent", checker) 
    workflow.add_node("Merger", merger)
    workflow.add_node(summarize_conversation, "summarize_conversation")
    workflow.add_conditional_edges("append", should_continue)
    workflow.add_conditional_edges("Merger", should_continue)
    workflow.add_edge("summarize_conversation", END)

    return workflow.compile(checkpointer=checkpointerredis)