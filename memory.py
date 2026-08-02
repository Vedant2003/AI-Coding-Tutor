import chromadb
from datetime import datetime
import uuid


# =====================================================
# ChromaDB Setup
# =====================================================

client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_or_create_collection(
    name="coding_tutor_memory"
)



# =====================================================
# Save Chat Message
# =====================================================

def save_message(
        session_id: str,
        role: str,
        message: str
):

    collection.add(

        ids=[
            str(uuid.uuid4())
        ],

        documents=[
            message
        ],

        metadatas=[

            {

                "session_id": session_id,

                "type": "chat",

                "role": role,

                "timestamp": str(datetime.now())

            }

        ]

    )



# =====================================================
# Get Chat History
# =====================================================

def get_history(
        session_id: str,
        limit: int = 50
):

    try:

        results = collection.get(

            where={

                "$and":[

                    {
                        "session_id": session_id
                    },

                    {
                        "type":"chat"
                    }

                ]

            }

        )


        history=[]


        for doc, meta in zip(

            results.get("documents",[]),

            results.get("metadatas",[])

        ):


            history.append(

                {

                    "role":meta.get(
                        "role",
                        ""
                    ),

                    "message":doc,

                    "time":meta.get(
                        "timestamp",
                        ""
                    )

                }

            )



        history.sort(

            key=lambda x:x["time"]

        )


        return history[-limit:]


    except Exception as e:

        print(
            "History Error:",
            e
        )

        return []



# =====================================================
# Save Generated Solution
# =====================================================

def save_solution(

        session_id: str,

        problem,

        explanation=None,

        code=None,

        complexity=None

):

    try:


        # If frontend sends result dictionary

        if isinstance(problem,dict):


            result = problem


            problem = result.get(
                "problem",
                ""
            )


            explanation = result.get(
                "explanation",
                ""
            )


            code = result.get(
                "code",
                ""
            )


            complexity = result.get(
                "complexity",
                ""
            )



        solution_id = "solution_" + session_id



        # remove previous solution

        try:

            old = collection.get(

                ids=[
                    solution_id
                ]

            )


            if old.get("ids"):

                collection.delete(

                    ids=[
                        solution_id
                    ]

                )


        except:

            pass



        collection.add(

            ids=[

                solution_id

            ],


            documents=[

                problem

            ],


            metadatas=[

                {

                    "session_id":session_id,

                    "type":"solution",

                    "problem":problem,

                    "explanation":explanation,

                    "code":code,

                    "complexity":complexity,

                    "timestamp":str(datetime.now())

                }

            ]

        )


    except Exception as e:

        print(

            "Save Solution Error:",

            e

        )



# =====================================================
# Get Solution
# =====================================================

def get_solution(
        session_id:str
):

    try:


        result = collection.get(

            ids=[

                "solution_" + session_id

            ]

        )



        if result.get("metadatas"):


            meta = result["metadatas"][0]


            return {


                "problem":
                    meta.get(
                        "problem",
                        ""
                    ),


                "explanation":
                    meta.get(
                        "explanation",
                        ""
                    ),


                "code":
                    meta.get(
                        "code",
                        ""
                    ),


                "complexity":
                    meta.get(
                        "complexity",
                        ""
                    )

            }


    except Exception as e:

        print(
            "Get Solution Error:",
            e
        )


    return None



# =====================================================
# Get All Sessions
# =====================================================

def get_all_sessions():

    sessions=set()


    try:

        results = collection.get()



        for meta in results.get(

            "metadatas",

            []

        ):


            sid = meta.get(

                "session_id"

            )


            if sid:

                sessions.add(sid)



    except Exception as e:

        print(

            "Session Error:",

            e

        )


    return list(sessions)



# =====================================================
# Session Exists
# =====================================================

def session_exists(
        session_id:str
):

    return session_id in get_all_sessions()



# =====================================================
# Session Title
# =====================================================

def get_session_title(
        session_id:str
):

    try:


        solution=get_solution(

            session_id

        )


        if solution:

            title=solution.get(

                "problem",

                ""

            )


            if title:

                return title[:45]



        history=get_history(

            session_id,

            1

        )


        if history:

            return history[0]["message"][:45]


    except Exception as e:

        print(

            "Title Error:",

            e

        )


    return "New Session"



# =====================================================
# Clear Session
# =====================================================

def clear_session(
        session_id:str
):

    try:

        result=collection.get(

            where={

                "session_id":session_id

            }

        )


        ids=result.get(

            "ids",

            []

        )


        if ids:

            collection.delete(

                ids=ids

            )


    except Exception as e:

        print(

            "Clear Error:",


        )
