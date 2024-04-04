import chromadb


def Vectordb_query(llm_query):
    chroma_client = chromadb.PersistentClient(path= "C:/Users/jvsan/ChromaDB")
    collection = chroma_client.get_or_create_collection(name="facts_collection")
    #collection.add(
    #    documents=["favourite f1 driver.txt", "favourite track.txt"],
    #    metadatas=[{"year": "2023"}, {"year": "2023"}],
    #    ids=["id1", "id2"]
    #)

    results = collection.query(
        query_texts=[llm_query],
        n_results=2,
    )
    
    file_content = ''
    file = open(results['documents'][0][0], 'r')
    while True:
        content = file.readline()
        if not content:
            break
        file_content = file_content + content
    file.close()

    return file_content