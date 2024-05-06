from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from ..redis_instance import r
from langchain.schema import HumanMessage, AIMessage

load_dotenv()


class LRUChatHistory:
    def __init__(self):
        self.lru_cache = []
        self.lru_keys = {}
        self.LRU_MAX = 100

    def find(self, user_id):
        result = None
        if self.lru_keys.get(user_id) is None:
            return result

        for i, cache in enumerate(self.lru_cache):
            if cache['user_id'] == user_id:
                result = self.lru_cache.pop(i)
                self.lru_cache.append(result)
                break

        return result["message_history"]

    def lru_full(self):
        return len(self.lru_cache) == self.LRU_MAX

    def create(self, user_id):
        if self.lru_full():
            self.lru_cache.pop(0)
            self.lru_keys.pop(user_id)

        result = {
            "user_id": user_id,
            "message_history": SQLChatMessageHistory(
                session_id=user_id,
                connection_string="sqlite:///user_messages1.db"
            )
        }

        self.lru_cache.append(result)
        self.lru_keys[user_id] = True

        return result['message_history']

    def get(self, user_id):
        chat_history = self.find(user_id)

        if chat_history is None:
            chat_history = self.create(user_id)

        return chat_history


class MilestoneAdviser:
    def __init__(self, model="gpt-3.5-turbo-0125"):
        self.llm = ChatOpenAI(model=model)
        self.chat_histories = LRUChatHistory()
        self.MAX_HISTORY = 15
        client = QdrantClient()
        self.retriever = Qdrant(collection_name="gitbook1", client=client, embeddings=OpenAIEmbeddings()).as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={'score_threshold': 0.8}
        )
        self.classes = """E001-LEC Regular
CSC115
Intro Comp Technolog
We 6:30PM - 7:20PM Mo 6:30PM - 8:10PM
2N 0012N 001
Daniel AgmanDaniel Agman

E001-LAB Regular
CSC117
Computer Technology Lab
Mo 8:20PM - 10:00PM
5N 108
Daniel Agman

E003-LAB Regular
CSC117
Computer Technology Lab
We 7:30PM - 9:10PM
5N 106
Daniel Agman

F002-LAB Regular
CSC117
Computer Technology Lab
Mo 4:40PM - 6:20PM
5N 106
TBA

E001-LEC Regular
CSC119
Computer Technology Concepts
Tu 6:30PM - 8:10PM Th 6:30PM - 7:20PM
5N 1065N 106
Michael D'EreditaMichael D'Eredita

01-LEC Regular
CSC126
Intro Computer Sci
We 12:20PM - 1:10PM Mo 12:20PM - 2:15PM
1P 1201P 120
Cong ChenCong Chen

01L1-LAB Regular
CSC126
Intro Computer Sci
We 1:25PM - 3:20PM Mo 2:30PM - 3:20PM
3N 1023N 102
Cong ChenCong Chen

01L2-LAB Regular
CSC126
Intro Computer Sci
We 1:25PM - 3:20PM Mo 2:30PM - 3:20PM
2N 1152N 115
Zhiqi WangZhiqi Wang

01L3-LAB Regular
CSC126
Intro Computer Sci
We 4:40PM - 5:30PM Mo 3:35PM - 5:30PM
1N 0051N 005
Ziyi XuZiyi Xu

02-LEC Regular
CSC126
Intro Computer Sci
Tu 9:05AM - 9:55AM Th 9:05AM - 11:00AM
1S 1161S 116
Sarah ZelikovitzSarah Zelikovitz

02L1-LAB Regular
CSC126
Intro Computer Sci
Tu 10:10AM - 12:05PM Th 11:15AM - 12:05PM
2N 1032N 103
Sarah ZelikovitzSarah Zelikovitz

02L2-LAB Regular
CSC126
Intro Computer Sci
Tu 10:10AM - 12:05PM Th 11:15AM - 12:05PM
3N 1133N 113


02L3-LAB Regular
CSC126
Intro Computer Sci
Tu 12:20PM - 2:15PM Th 12:20PM - 1:10PM
2N 1032N 103


03-LEC Regular
CSC126
Intro Computer Sci
We 6:30PM - 7:20PM Mo 6:30PM - 8:10PM
6S 1386S 138
Dolores HayesDolores Hayes

03L1-LAB Regular
CSC126
Intro Computer Sci
We 7:30PM - 9:10PM Mo 8:20PM - 9:10PM
1N 0041N 004
Dolores HayesDolores Hayes

03L2-LAB Regular
CSC126
Intro Computer Sci
We 7:30PM - 9:10PM Mo 8:20PM - 9:10PM
2N 1032N 103
Zaid Al-MashhadaniZaid Al-Mashhadani

03L3-LAB Regular
CSC126
Intro Computer Sci
Mo 8:20PM - 9:10PM We 7:30PM - 9:10PM
5N 1062N 115
Fatma KausarFatma Kausar

04-LEC Regular
CSC126
Intro Computer Sci
Tu 10:10AM - 12:05PM Th 10:10AM - 11:00AM
5N 1065N 106
Ziyi XuZiyi Xu

04L1-LAB Regular
CSC126
Intro Computer Sci
Tu 12:20PM - 1:10PM Th 11:15AM - 1:10PM
5N 1065N 106
Ziyi XuZiyi Xu

E002-LEC Regular
CSC140
Computational Problem Solving
Mo 6:30PM - 9:50PM
2N 115
Paolo Cappellari

D001-LEC Regular
CSC211
Intermediate Programming
We 11:15AM - 1:10PM We 10:10AM - 11:00AM Mo 12:20PM - 1:10PM Mo 10:10AM - 12:05PM
1N 0051N 0051N 0051N 005
Deborah SturmDeborah SturmDeborah SturmDeborah Sturm

D002-LEC Regular
CSC211
Intermediate Programming
Tu 9:05AM - 11:00AM Th 9:05AM - 9:55AM Tu 11:15AM - 12:05PM Th 10:10AM - 12:05PM
3N 1103N 1103N 1093N 109
Feng GuFeng GuFeng GuFeng Gu

E001-LEC Regular
CSC211
Intermediate Programming
Tu 8:20PM - 9:10PM Tu 6:30PM - 8:10PM Th 6:30PM - 9:10PM
3N 1133N 1133N 113
Anthony CatalanoAnthony CatalanoAnthony Catalano

D006-LEC Regular
CSC220
Computer Organization
Tu 10:10AM - 12:05PM Th 10:10AM - 11:00AM
5N 1085N 108
Ping ShiPing Shi

E001-LEC Regular
CSC220
Computer Organization
Mo 6:30PM - 9:10PM
3N 113
Safet Jahaj

E001-LEC Regular
CSC221
Networking and Security
Th 6:30PM - 9:10PM
1N 114
Ali Mohamed

E001-LEC Regular
CSC225
Intro to Web Dev/The Internet
We 6:30PM - 9:10PM
1N 005
Briano Bruno

D001-LEC Regular
CSC228
Discrte Mth Comp Sci
MoWe 10:10AM - 12:05PM
1N 004
Zhiqi Wang

E001-LEC Regular
CSC228
Discrte Mth Comp Sci
TuTh 6:30PM - 8:10PM
2N 003
Ziyi Xu

D001-LEC Regular
CSC235
Robotic Explorations
MoWe 2:30PM - 4:25PM
5N 106
Susan Imberman

E001-LAB Regular
CSC305
Operatating Sys Prog Lab
Tu 6:30PM - 8:10PM
2N 115
Roman Lavrov

E002-LAB Regular
CSC305
Operatating Sys Prog Lab
Mo 6:30PM - 8:10PM
1S 110
Jonathan Parziale

D001-LEC Regular
CSC315
Intro to Database Systems
MoWe 10:10AM - 12:05PM
5N 108
Jun Rao

D002-LEC Regular
CSC326
Data Structures
Tu 9:05AM - 11:00AM Tu 11:15AM - 12:05PM Th 9:05AM - 9:55AM Th 10:10AM - 12:05PM
1N 0041N 0041N 0041N 004
Jun RaoJun RaoJun RaoJun Rao

E001-LEC Regular
CSC326
Data Structures
MoWe 6:30PM - 9:10PM
3N 115
Jia Lu

D002-LEC Regular
CSC330
Software Design
Tu 10:10AM - 11:00AM Th 10:10AM - 12:05PM
1N 0051N 005
Cong ChenCong Chen

D002-LEC Regular
CSC332
Operating Systems I
Mo 2:30PM - 3:20PM We 2:30PM - 4:25PM
2N 0051N 111
Jun RaoJun Rao

D002-LEC Regular
CSC346
Digital Systems Design
Tu 12:20PM - 2:15PM Th 1:25PM - 2:15PM
1N 1141N 114
Ali MohamedAli Mohamed

D003-LEC Regular
CSC346
Digital Systems Design
We 10:10AM - 11:00AM Mo 10:10AM - 12:05PM
1N 1111N 111
Ping ShiPing Shi

D001-LAB Regular
CSC347
Digital Systems Laboratory
Tu 4:40PM - 6:20PM
5N 106
Ali Mohamed

D002-LAB Regular
CSC347
Digital Systems Laboratory
Th 4:40PM - 6:20PM
5N 106
Shuqun Zhang

D002-LEC Regular
CSC382
Analysis of Algorithms
TuTh 10:10AM - 12:05PM
1N 111
Yumei Huo

D002-LEC Regular
CSC446
Computer Architecture
MoWe 10:10AM - 12:05PM
1N 114
Ali Mohamed

01-LEC Regular
CSC462
Microcontrollers
Mo 6:30PM - 8:10PM
Online-Synchronous
Dwight Richards

01L1-LAB Regular
CSC462
Microcontrollers
We 6:30PM - 9:50PM
4N 102
Dwight Richards

D002-LEC Regular
CSC480
Artificial Intelligence
TuTh 12:20PM - 2:15PM
1N 005
TBA

D001-LEC Regular
CSC490
Seminar in Computer Science
We 1:25PM - 2:15PM Mo 1:25PM - 3:20PM
1N 1111N 111
Deborah SturmDeborah Sturm"""

    def get_messages(self, user_id):
        history = self.chat_histories.get(user_id)

        return history.messages

    def query(self, user_message, user_id):
        response = r.get(f"{user_id}:user")
        context = f"context: {response}.".replace("{", "[").replace("}", "]")
        print(context)
        schedule = f"The schedule for the current semester is {self.classes}. Use it if they ask for help creating a schedule."
        # documents = self.retriever.invoke(user_message)

        contextualize_q_system_prompt = """Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is."""
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        history_aware_retriever = create_history_aware_retriever(
            self.llm, self.retriever, contextualize_q_prompt
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You're a computer science adviser. You're advising a student with the characteristics in the context; if asked, provide the context." +
                    "Ignore the meta_data. There is a one-to-one mapping between asked_questions and answers." +
                    "If the question does not relate to advising, kindly decline to answer." + context +
                    schedule + "Use the following pieces of retrieved context to answer the question: {context}"
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                # MessagesPlaceholder(variable_name="documents"),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)

        history = self.chat_histories.get(user_id)

        chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        chain_with_message_history = RunnableWithMessageHistory(
            chain,
            lambda session_id: history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        def trim_messages(chain_input):
            stored_messages = history.messages

            if len(stored_messages) <= self.MAX_HISTORY:
                return False

            history.clear()

            if len(stored_messages) < self.MAX_HISTORY:
                stored_length = len(stored_messages)
            else:
                stored_length = self.MAX_HISTORY

            for message in stored_messages[-stored_length:]:
                history.add_message(message)

            return True

        chain_with_trimming = (
            RunnablePassthrough.assign(messages_trimmed=trim_messages)
            | chain_with_message_history
        )

        ai_message = chain_with_trimming.invoke(
            {"input": user_message},
            {"configurable": {"session_id": user_id}},
        )

        history.add_message(HumanMessage(content=user_message))
        history.add_message(AIMessage(content=ai_message["answer"]))

        return ai_message['answer']
