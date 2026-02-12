
from pydantic import BaseModel


class Chat(BaseModel):
    user_msg: str

from fastapi import APIRouter, Query
from src._agents.graph import setup_graph, question_asking_graph
from src._agents.state import setUpState
router = APIRouter()

@router.get("/setup")
def setup(repo_url:str = Query(..., description= "Getting the repo url")):
    results  = setup_graph.invoke({
        'repo_url':  repo_url
    })
    
    error = ""
    if not results['is_vector_completed']:
        error += "Error occured in the vector "
    if not results['is_BM25_completed']:
        error += " Error occured in the BM25 index"
    if not results['is_graph_completed']:
        error += " Error occured in the Graph index"
    
    if not error:
        return {'success': True, 'error': "No error"}
    return {'success': False, 'error': error}


@router.post('/qa_chat')
def qabot(question: Chat):
    result = question_asking_graph.invoke({
        'query': question.user_msg
    })
    print(result['final_response'])
    return result['final_response']

