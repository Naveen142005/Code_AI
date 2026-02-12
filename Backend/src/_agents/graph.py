from langgraph.graph import StateGraph, END, START
from src._agents.all_nodes import *
from src._agents.state import AgentState, QuestionAskingState, setUpState

def should_continue_after_grader(state: QuestionAskingState) -> str:
    is_expendable = state.get('is_expendable', False)
    if is_expendable:
        return "expand" 
    else:
        return "presenter"


def route_after_router(state: QuestionAskingState) -> str:
    res = state.get('router_response')
    if res == 'CODE': return 'retriever'  
    elif res == 'PROJECT' or res == 'FLOW': return 'architecturer'
    return 'general_assistant'


def create_setup_graph():
    setUpFlow = StateGraph(setUpState)

    setUpFlow.add_node("repo_loader", repo_loader)
    setUpFlow.add_node("build_vector", build_vector)
    setUpFlow.add_node("build_bm25", build_bm25)
    setUpFlow.add_node("build_graph", build_graph)

    setUpFlow.set_entry_point("repo_loader")

    setUpFlow.add_edge("repo_loader", "build_vector")
    setUpFlow.add_edge("repo_loader", "build_bm25")
    setUpFlow.add_edge("repo_loader", "build_graph")

    setUpFlow.add_edge("build_vector", END)
    setUpFlow.add_edge("build_bm25", END)
    setUpFlow.add_edge("build_graph", END)

    graph = setUpFlow.compile()
    return graph

def create_question_asking_graph():
    workflow = StateGraph(QuestionAskingState)

    workflow.add_node("router", router_node)
    workflow.add_node("architecturer", architecture_node)
    workflow.add_node("retriever", retriver_node)
    workflow.add_node("grader", grader_node)
    workflow.add_node("expander", expander_node)
    workflow.add_node("presenter", presenter_node)
    workflow.add_node("general_assistant", general_assistant_node)

    workflow.set_entry_point("router")

    workflow.add_conditional_edges(
        "router",
        route_after_router,
        {
            "retriever": "retriever",
            "general_assistant": "general_assistant",
            "architecturer": "architecturer",
        }
    )

    workflow.add_edge("retriever", "grader")

    workflow.add_conditional_edges(
        "grader",
        should_continue_after_grader,
        {
            "expand": "expander",
            "presenter": "presenter",
        }
    )

    workflow.add_edge("architecturer", "presenter")
    workflow.add_edge("expander", "presenter")
    workflow.add_edge("presenter", END)
    workflow.add_edge("general_assistant", END)

    graph = workflow.compile()
    return graph

setup_graph = create_setup_graph()
question_asking_graph = create_question_asking_graph()

