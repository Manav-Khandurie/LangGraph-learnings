from workflows.qa_graph import build_qa_graph

if __name__ == "__main__":
    file_path = "data/attention.pdf"
    query = input("Ask a question about the document:\n> ")

    workflow = build_qa_graph()

    initial_state = {
        "file_path": file_path,
        "query": query,
        "extracted_text": "",
        "summary": "",
        "answer": "",
    }

    final_state = workflow.invoke(initial_state)

    print("\n--- Final Answer ---\n")
    print(final_state["answer"])
