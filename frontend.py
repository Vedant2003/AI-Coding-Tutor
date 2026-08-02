import os
import time
import uuid

import streamlit as st

from dotenv import load_dotenv
from langsmith import traceable

from backend import generate_solution
from tutor import CodingTutor

import memory


# =====================================================
# Memory Functions
# =====================================================

save_message = memory.save_message
get_history = memory.get_history
get_all_sessions = memory.get_all_sessions
get_session_title = memory.get_session_title
save_solution = memory.save_solution
get_solution = memory.get_solution



# =====================================================
# Environment
# =====================================================

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "AI-Coding-Tutor"



# =====================================================
# LangSmith Wrappers
# =====================================================


@traceable(
    name="Frontend Solution Generation",
    run_type="chain"
)
def run_solution(problem, session_id):

    return generate_solution(
        problem,
        session_id
    )



@traceable(
    name="Frontend Tutor Chat",
    run_type="chain"
)
def run_tutor(tutor, question):

    return tutor.chat(question)



# =====================================================
# Page Config
# =====================================================


st.set_page_config(

    page_title="AI Coding Tutor",

    page_icon="💻",

    layout="wide"

)



# =====================================================
# CSS
# =====================================================


st.markdown(
"""
<style>

.main-title{

font-size:42px;
font-weight:800;

}


.stButton button{

border-radius:12px;
height:45px;

}


.session-box{

padding:10px;
border-radius:10px;
background:#f5f5f5;

}

</style>
""",
unsafe_allow_html=True
)



# =====================================================
# Header
# =====================================================


st.markdown(
"<div class='main-title'>💻 AI Coding Tutor</div>",
unsafe_allow_html=True
)

st.caption(
"LangGraph • Ollama • ChromaDB • LangSmith"
)



# =====================================================
# Session State
# =====================================================


if "session_id" not in st.session_state:

    st.session_state.session_id = str(
        uuid.uuid4()
    )


if "result" not in st.session_state:

    st.session_state.result = None


if "tutor" not in st.session_state:

    st.session_state.tutor = None


if "chat_history" not in st.session_state:

    st.session_state.chat_history = []



# =====================================================
# Sidebar
# =====================================================


with st.sidebar:


    st.header("⚙ Controls")


    st.info(
        f"""
Current Session

{st.session_state.session_id[:8]}
"""
    )



    if st.button(
        "🆕 New Session"
    ):


        st.session_state.session_id = str(
            uuid.uuid4()
        )

        st.session_state.result=None

        st.session_state.tutor=None

        st.session_state.chat_history=[]


        st.rerun()



    st.divider()


    st.subheader(
        "📚 Previous Sessions"
    )



    sessions = get_all_sessions()



    if not sessions:

        st.caption(
            "No previous sessions"
        )



    for sid in sessions:



        title = get_session_title(
            sid
        )


        if st.button(
            title,
            key=sid
        ):



            solution = get_solution(
                sid
            )


            if solution:


                st.session_state.session_id=sid


                st.session_state.result=solution



                st.session_state.tutor=CodingTutor(

                    solution,

                    sid

                )



                history=get_history(
                    sid
                )


                st.session_state.chat_history=[]



                for item in history:


                    st.session_state.chat_history.append(

                        (
                            item["role"],
                            item["message"]
                        )

                    )


                st.rerun()




# =====================================================
# Problem Input
# =====================================================


problem = st.text_area(

    "📝 Enter DSA Problem",

    height=220,

    placeholder="""

Example:

Find maximum subarray sum using Kadane algorithm.

"""

)



# =====================================================
# Generate Solution
# =====================================================


if st.button(

    "🚀 Generate Solution",

    type="primary"

):


    if not problem.strip():

        st.warning(
            "Please enter a problem"
        )

        st.stop()



    with st.status(

        "🤖 AI Processing",

        expanded=True

    ) as status:


        status.write(
            "🔍 Understanding problem..."
        )


        time.sleep(0.5)


        status.write(
            "💻 Generating C++17 solution..."
        )


        result = run_solution(

            problem,

            st.session_state.session_id

        )



        status.write(
            "📊 Analysing complexity..."
        )


        time.sleep(0.5)



        status.update(

            label="✅ Completed",

            state="complete"

        )




    st.session_state.result=result



    save_solution(

        st.session_state.session_id,

        result

    )



    st.session_state.tutor=CodingTutor(

        result,

        st.session_state.session_id

    )



    st.session_state.chat_history=[]



    st.rerun()




# =====================================================
# Display Solution
# =====================================================


if st.session_state.result:



    result=st.session_state.result



    tab1,tab2,tab3 = st.tabs(

        [

            "📘 Explanation",

            "💻 Code",

            "📈 Complexity"

        ]

    )



    with tab1:


        st.write(
            result["explanation"]
        )



    with tab2:


        st.code(

            result["code"],

            language="cpp"

        )


        st.download_button(

            "⬇ Download C++",

            result["code"],

            file_name="solution.cpp"

        )



    with tab3:


        st.write(
            result["complexity"]
        )



    st.divider()



    st.subheader(
        "🤖 Coding Tutor"
    )



    for role,msg in st.session_state.chat_history:


        with st.chat_message(role):

            st.write(msg)



    question = st.chat_input(

        "Ask about this solution..."

    )



    if question:



        st.session_state.chat_history.append(

            (
                "user",
                question
            )

        )



        with st.chat_message("user"):

            st.write(question)



        with st.chat_message("assistant"):


            with st.spinner(

                "🧠 Tutor thinking..."

            ):


                answer = run_tutor(

                    st.session_state.tutor,

                    question

                )


            st.write(answer)



        st.session_state.chat_history.append(

            (

                "assistant",

                answer

            )

        )
