import gradio as gr
from embed import embed_and_store, retrieve
from ingest import load_documents, chunk_documents
from generate import generate_answer

# Load everything once at startup
documents = load_documents()
chunks = chunk_documents(documents)
collection = embed_and_store(chunks)

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    
    result = generate_answer(question, collection)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

with gr.Blocks(title="Stevens CS Unofficial Guide") as demo:
    gr.Markdown("# Stevens CS Unofficial Guide")
    gr.Markdown("Ask questions about the CS program at Stevens Institute of Technology based on real student reviews.")
    
    inp = gr.Textbox(label="Your question", placeholder="e.g. What do students say about internship opportunities?")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=4)
    
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()