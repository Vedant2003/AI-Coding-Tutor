from dotenv import load_dotenv

from langchain_ollama import ChatOllama

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

from langsmith import traceable


from memory import (
    save_message,
    get_history,
    clear_session
)



# =====================================================
# Environment
# =====================================================

load_dotenv()





# =====================================================
# Coding Tutor Class
# =====================================================


class CodingTutor:


    """
    AI Coding Tutor

    Features:

    - Session based memory
    - ChromaDB persistence
    - LangSmith tracing
    - Context aware answers

    """



    @traceable(
        name="Initialize Coding Tutor",
        run_type="chain"
    )
    def __init__(

            self,

            result:dict,

            session_id:str

    ):


        self.session_id=session_id

        self.result=result



        self.llm=ChatOllama(

            model="phi3",

            temperature=0

        )



        self.system_prompt=f"""

You are an expert Data Structures and Algorithms Tutor.


The student has generated this solution.



================ PROBLEM ================

{result.get("problem","")}



============== EXPLANATION ===============

{result.get("explanation","")}



================ CODE ====================

{result.get("code","")}



============= COMPLEXITY =================

{result.get("complexity","")}




Rules:

1. Only answer questions related to this problem.

2. Explain concepts simply.

3. Explain code line by line when requested.

4. Give examples.

5. Help debug errors.

6. Suggest optimizations.

7. Maintain conversation context.


"""



        self.messages=[

            SystemMessage(

                content=self.system_prompt

            )

        ]



        self.load_memory()








    # =================================================
    # Load Session Memory
    # =================================================


    @traceable(

        name="Load Tutor Memory",

        run_type="retriever"

    )
    def load_memory(self):


        history=get_history(

            self.session_id,

            limit=15

        )



        for item in history:


            if item["role"]=="user":


                self.messages.append(

                    HumanMessage(

                        content=item["message"]

                    )

                )


            elif item["role"]=="assistant":


                self.messages.append(

                    AIMessage(

                        content=item["message"]

                    )

                )







    # =================================================
    # Ask Tutor
    # =================================================


    @traceable(

        name="Tutor Question",

        run_type="chain"

    )
    def chat(

            self,

            question:str

    ):



        if not question.strip():

            return "Please enter a question."




        self.messages.append(

            HumanMessage(

                content=question

            )

        )



        save_message(

            self.session_id,

            "user",

            question

        )




        try:



            # Send only latest context
            # reduces Ollama latency

            response=self.llm.invoke(

                self.messages[-15:]

            )



            answer=response.content



            self.messages.append(

                AIMessage(

                    content=answer

                )

            )



            save_message(

                self.session_id,

                "assistant",

                answer

            )



            return answer




        except Exception as e:


            return f"Error from Tutor: {str(e)}"







    # =================================================
    # Clear Current Session
    # =================================================


    @traceable(

        name="Clear Tutor Session"

    )
    def clear_history(self):


        clear_session(

            self.session_id

        )


        self.messages=[

            SystemMessage(

                content=self.system_prompt

            )

        ]







    # =================================================
    # Get History
    # =================================================


    @traceable(

        name="Get Tutor History"

    )
    def get_history(self):


        return get_history(

            self.session_id

        )







    # =================================================
    # Utility Functions
    # =================================================


    def get_problem(self):

        return self.result.get(

            "problem",

            ""

        )




    def get_code(self):

        return self.result.get(

            "code",

            ""

        )




    def get_explanation(self):

        return self.result.get(

            "explanation",

            ""

        )




    def get_complexity(self):

        return self.result.get(

            "complexity",

            ""

        )
