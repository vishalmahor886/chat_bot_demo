#from langgraph.checkpoint.sqlite import SqliteSaver

#memory = SqliteSaver.from_conn_string("sqlite:///chat_history.db")

from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver()