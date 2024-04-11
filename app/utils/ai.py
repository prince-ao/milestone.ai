from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv

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
                connection_string="sqlite:///user_messages.db"
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

    def query(self, user_message, user_id):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You're a computer science adviser.",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )

        chain = prompt | self.llm

        history = self.chat_histories.get(user_id)
        print(history, "\n\n")

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

        return ai_message.content
