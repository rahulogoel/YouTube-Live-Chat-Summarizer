import pytchat

def get_live_chat(video_id):

    chat = pytchat.create(video_id=video_id)
    
    while chat.is_alive():
        messages = [f"{c.author.name}: {c.message}" for c in chat.get().items]
        if messages:
            yield " ".join(messages)
