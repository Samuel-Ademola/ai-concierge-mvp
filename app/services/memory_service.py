# Simple in-memory storage (MVP level)

user_memory = {}


def get_memory(user_id: str):
    return user_memory.get(user_id, {})


def update_memory(user_id: str, key: str, value):
    if user_id not in user_memory:
        user_memory[user_id] = {}

    user_memory[user_id][key] = value


def clear_memory(user_id: str):
    if user_id in user_memory:
        user_memory[user_id] = {}