from typing import TypedDict

from dotenv import load_dotenv

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from langgraph.checkpoint.memory import MemorySaver

from langchain_ollama import ChatOllama

from langsmith import traceable



# =====================================================
# Environment
# =====================================================

load_dotenv()





# =====================================================
# State
# =====================================================


class Coding(TypedDict, total=False):

    problem: str

    explanation: str

    code: str

    complexity: str





# =====================================================
# LLM
# =====================================================


llm = ChatOllama(

    model="phi3",

    temperature=0,

)






# =====================================================
# LangGraph Nodes
# =====================================================



@traceable(
    name="Explain Problem Node",
    run_type="chain"
)
def explain_problem(state:Coding):


    prompt=f"""

You are a DSA tutor.

Explain this problem briefly.

Problem:

{state['problem']}


Include:

- Goal
- Input
- Output
- Algorithm idea

Keep it simple.

"""


    response=llm.invoke(prompt)


    return {

        "explanation":response.content

    }






@traceable(
    name="Generate Code Node",
    run_type="chain"
)
def generate_code(state:Coding):


    prompt=f"""

You are an expert competitive programmer.


Generate the optimal C++17 solution.


Problem:

{state['problem']}


Rules:

- Return ONLY C++ code
- No markdown
- No explanation
- Use best algorithm


"""


    response=llm.invoke(prompt)


    return {


        "code":response.content

    }








@traceable(
    name="Complexity Analysis Node",
    run_type="chain"
)
def analyze_complexity(state:Coding):


    prompt=f"""


Analyze this solution.


Problem:

{state['problem']}



Code:

{state['code']}



Return:

Time Complexity:

Space Complexity:

Reason:

"""


    response=llm.invoke(prompt)



    return {


        "complexity":response.content

    }







# =====================================================
# Build Graph
# =====================================================


graph=StateGraph(Coding)



graph.add_node(

    "ExplainProblem",

    explain_problem

)



graph.add_node(

    "GenerateCode",

    generate_code

)



graph.add_node(

    "AnalyzeComplexity",

    analyze_complexity

)






graph.add_edge(

    START,

    "ExplainProblem"

)



graph.add_edge(

    "ExplainProblem",

    "GenerateCode"

)



graph.add_edge(

    "GenerateCode",

    "AnalyzeComplexity"

)



graph.add_edge(

    "AnalyzeComplexity",

    END

)






# =====================================================
# In Memory Checkpointer
# =====================================================


memory=MemorySaver()



workflow=graph.compile(

    checkpointer=memory

)








# =====================================================
# Public API
# =====================================================



@traceable(

    name="Generate Solution Workflow",

    run_type="chain"

)
def generate_solution(

        problem:str,

        session_id:str

):


    try:


        result=workflow.invoke(

            {

                "problem":problem

            },


            config={


                "configurable":

                {

                    "thread_id":session_id

                }

            }

        )



        return {


            "problem":problem,


            "explanation":

            result.get(

                "explanation",

                ""

            ),



            "code":

            result.get(

                "code",

                ""

            ),



            "complexity":

            result.get(

                "complexity",

                ""

            )


        }



    except Exception as e:


        return {


            "problem":problem,

            "explanation":

            f"Error: {str(e)}",

            "code":"",

            "complexity":""

        }







# =====================================================
# Test
# =====================================================


if __name__=="__main__":


    result=generate_solution(

        """
Given an array of integers,
find the maximum subarray sum.
""",

        "test-session"

    )



    print("\nEXPLANATION")

    print(result["explanation"])



    print("\nCODE")

    print(result["code"])



    print("\nCOMPLEXITY")

    print(result["complexity"])
