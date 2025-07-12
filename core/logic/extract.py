import os
import time 
from dotenv import load_dotenv
from langchain_together import Together
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader

load_dotenv()

# Initialize Together LLaMA model
llm = Together(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    temperature=0.2,
    max_tokens=1024
)

# Prompt template
prompt_template = PromptTemplate(
    input_variables=["medical_notes"],
    template="""
You are a clinical information extractor for legal-medical documents.

Your task is to identify only the **concrete medical events** that meet **all** of the following:

1. The event must include an explicit **diagnosis** (e.g., stroke, dementia).
2. The event must have a **clear date** (exact or month+year).
3. The **treater** must be named (doctor or hospital).

Do NOT include:
- Symptoms alone (e.g., memory loss, can't do math)
- Opinions, assessments, or behavioral descriptions
- Observations like “he was able to…” or “he was unable to…”
- General mental capacity evaluations unless directly tied to a medical diagnosis

And respond strictly in this format for each event:
- Date: [e.g., 2015-06-20 or November 2010]
- Treater: [Doctor or Hospital]
- Diagnosis: [Confirmed medical diagnosis]
- Treatment: [Optional if mentioned]
- Notes: [Only essential notes linked to the diagnosis, Notes should be 8-10 words maximum not one more]
ONLY Return 4-5 Events not one more 

TEXT:
{medical_notes}

Return only relevant filtered events, clean and non-repetitive.



"""
)

chain = prompt_template | llm

# PDF text extractor
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Medical chronology (chunked)
def generate_medical_chronology(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=50000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_text(text)
    print(f"[SERVER] Total chunks: {len(chunks)}")

    results = []

    for i, chunk in enumerate(chunks):
        print(f"[SERVER] Processing chunk {i+1}/{len(chunks)}...")
        try:
            result = chain.invoke({"medical_notes": chunk})
            print(f"[SERVER] Chunk {i+1} result: {result[:200]}...")

            # ✅ Only keep chunks that look like valid medical events
            if all(k in result for k in ["Date:", "Diagnosis:", "Treater:"]):
                results.append(result)
            else:
                print(f"[SERVER] Chunk {i+1} skipped — missing required fields.")

            time.sleep(2)  # respect rate limits

        except Exception as e:
            print(f"[SERVER] ERROR in chunk {i+1}: {str(e)}")

    return "\n\n".join(results)