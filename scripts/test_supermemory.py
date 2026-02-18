from supermemory import Supermemory

def test_supermemory():
    try:
        # Initialize the client
        client = Supermemory(
            api_key="sm_GkhZoaA5ckmbV8uh8qDCiK_OzzPgWlpqayiwpKitxChbuMXutOUZOCUQtdsmmClEfJKpjYnfozHQOHAoCKGRbZn",
        )

        # 1. Add a memory
        print("Adding memory...")
        response = client.memories.add(
            content="SuperMemory Python SDK is awesome. This is a test from OpenClaw.",
            container_tag="Python_SDK",
            metadata={
                "note_id": "test_001",
                "source": "OpenClaw"
            }
        )
        print(f"Add Response: {response}")

        # 2. Search for it
        print("\nSearching...")
        searching = client.search.execute(
            q="What do you know about Python SDK?",
        )
        print(f"Search Results: {searching.results}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_supermemory()
