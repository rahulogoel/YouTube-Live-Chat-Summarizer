import pytchat

def get_live_chat(video_id):
    
    chat = pytchat.create(video_id=video_id)
    
    while chat.is_alive():
        batch = []
        for c in chat.get().items:
            batch.append({"author": c.author.name, "message": c.message})
        
        if batch:
            yield batch
