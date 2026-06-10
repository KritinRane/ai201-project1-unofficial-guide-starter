# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

Student reviews of the CS program and professors at Stevens Institute of Technology. This knowledge is valuable to prospective students researching colleges because official university sources don't reflect teaching style, exam difficulty, workload, or real career outcomes. It is hard to find in one place because it is scattered across RateMyProfessors, Reddit, Niche, GradReports, and Unigo.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Reddit | Forum thread | https://www.reddit.com/r/stevens/comments/engineering-computer-science-students |
| 2 | RateMyProfessors | Professor reviews | https://www.ratemyprofessors.com/professor/2721847 |
| 3 | Niche | Program reviews | https://www.niche.com/colleges/stevens-institute-of-technology/reviews/ |
| 4 | Unigo | Student reviews | https://www.unigo.com/colleges/stevens-institute-of-technology/reviews |
| 5 | GradReports | CS program reviews | https://www.gradreports.com/colleges/stevens-institute-of-technology |
| 6 | RateMyProfessors | Professor reviews | https://www.ratemyprofessors.com/professor/1942070 |
| 7 | RateMyProfessors | Professor reviews | https://www.ratemyprofessors.com/professor/2760646 |
| 8 | Reddit | Forum thread | https://www.reddit.com/r/stevens/comments/why-i-chose-stevens-cs |
| 9 | Reddit | Forum thread | https://www.reddit.com/r/stevens/comments/admitted-to-cs-program |
| 10 | RateMyProfessors | Professor reviews | https://www.ratemyprofessors.com/professor/2829445 |

---

## Chunking Strategy

**Chunk size:** 500 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** The documents are primarily short to medium length student reviews. 500 characters is large enough to capture a complete review thought while small enough to keep chunks focused on a single opinion or experience. Overlap of 50 characters ensures that if a review spans a chunk boundary, the key context from the end of one chunk carries into the start of the next, preventing retrieval from returning half a thought. Recursive splitting was chosen over fixed character splitting because it respects natural review boundaries by trying paragraph and sentence breaks before falling back to character splitting.

**Final chunk count:** 78

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:**
1. Cost: all-MiniLM-L6-v2 is free and runs locally. API-based models like OpenAI text-embedding-3-small cost per token which adds up at scale.
2. Accuracy: Larger models like text-embedding-3-large perform better on domain-specific text but are slower and more expensive.
3. Latency: Local models add embedding time at query but avoid network round trips. API models offload compute but introduce latency and dependency on external services.
4. Context length: all-MiniLM-L6-v2 has a 256 token limit. For longer documents, models with larger context windows like text-embedding-3-large (8191 tokens) would be necessary.
5. Multilingual support: all-MiniLM-L6-v2 is English-only. For a multilingual corpus, a model like paraphrase-multilingual-MiniLM-L12-v2 would be needed.

---

## Sample Chunks

**Chunk 1** (Source: rmp_terolli.txt)
Course: CS556 | Quality: 5/5 | Difficulty: 2/5 | Grade: A | Date: May 2025
You have to have made a major screw up not to get anything more than a B in this class. Professor is very accommodating to doubts, has a demo session at the end of class where we programmatically practice the mathematical concepts we learned in class, tests have a 2nd opportunity.

**Chunk 2** (Source: rmp_zumrut.txt)
Course: CS385 (Algorithms) | Quality: 5/5 | Difficulty: 4/5 | Grade: A | Date: Dec 2025
Algorithms is a difficult class, but Zumrut Akcam is the absolute best. Attend lecture, ask questions, and be sure to read the relevant info in the textbook because there is a lot to know.

**Chunk 3** (Source: unigo.txt)
FAQ: What do you brag about most when you tell friends about your school?
The research opportunities at Stevens are amazing. Undergraduates can work with professors and graduate students over the summer through the Scholars program or Technogenesis. Students can live on campus while working in labs and are paid by the hour.

**Chunk 4** (Source: niche.txt)
Rating: 5/5 | Year: Junior | Date: Sep 2025
Stevens has an amazing location right by New York City. The professors range from good to genuinely infuriating, but the coursework is rigorous and I feel a lot more capable in my field of Computer Science as a result.

**Chunk 5** (Source: reddit_ATCP.txt)
User: miketerk21 (CS/M&T '28, Current Undergrad)
I like the professors and education a lot, but the grading system is horrendous. Most core CS classes have final grades that are mostly exam-based, which is an abysmal way to measure performance in a project-based field.

---

## Retrieval Test Examples

**Query 1:** What do students say about internship opportunities at Stevens?
- Source: niche.txt | Distance: 0.684 — Student mentions highly competitive internship in Manhattan through Pinnacle Scholars research
- Source: unigo.txt | Distance: 0.737 — Research opportunities through Scholars program, students paid by the hour
- Source: gradreports.txt | Distance: 0.824 — Off-topic: administrative complaints (retrieval weakness)

Top chunks are relevant because the first two directly reference student experiences with research and internship pathways at Stevens.

**Query 2:** What are Professor Zumrut's exams like?
- Source: rmp_zumrut.txt | Distance: 0.866 — General praise for Zumrut, teaching style
- Source: rmp_zumrut.txt | Distance: 1.003 — Professor bio header chunk
- Source: rmp_zumrut.txt | Distance: 1.113 — CS385 exam difficulty description (most relevant but ranked 4th)

Retrieval partially failed: the most relevant chunk about exam difficulty was ranked 4th because the query used "exams" while the document used "algorithms class" and "difficult."

**Query 3:** What are common complaints about the Stevens CS program?
- Source: unigo.txt | Distance: 0.846 — Frustration with being limited to core courses
- Source: reddit_ATCP.txt | Distance: 0.853 — CS grading system complaints, exam-heavy courses
- Source: gradreports.txt | Distance: 0.913 — Administrative failures, high tuition, outdated resources

Top chunks are relevant because all three surface genuine student complaints about academic structure, administration, and cost.

---

## Query Interface

**Input field:** A plain text question about the Stevens CS program entered by the user.

**Output fields:** Two fields - Answer (the LLM generated response grounded in retrieved documents) and Sources (the filenames of documents the answer drew from).

**Sample interaction:**

User input: What do students say about internship opportunities at Stevens?

Answer: According to student reviews, Stevens CS students report strong internship and co-op opportunities, with ~97% of graduates achieving their desired outcome within six months. The Pinnacle Scholars program provides research stipends and students have landed competitive internships in Manhattan. Companies like Google, Microsoft, and Amazon recruit at Stevens through on-campus career fairs.

Sources:
- niche.txt
- unigo.txt
- gradreports.txt

---

## Grounded Generation

**System prompt grounding instruction:**
The following instruction is passed to llama-3.3-70b-versatile on every query:

"You are a helpful assistant that answers questions about the CS program at Stevens Institute of Technology. Answer the question using ONLY the information provided in the documents below. If the documents don't contain enough information to answer the question, say 'I don't have enough information on that.' Do not use any outside knowledge. Always cite which document your answer came from."

The retrieved chunks are formatted and injected into the prompt before the question, so the model sees context first and the question second. This structure reinforces that the context is the authoritative source.

**How source attribution is surfaced in the response:**
Source filenames are collected from the metadata of each retrieved chunk and returned alongside the answer. The Gradio interface displays them in a separate "Sources" field so the user can see which documents the answer drew from. The LLM is also instructed to cite documents inline in its response.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do Stevens CS students say about internship opportunities? | ~95% career outcomes, Google/Microsoft/Amazon recruiting on campus, average salary ~$100k | Cited ~97% career outcomes and co-op opportunities but missed specific company names and salary figures | Partially relevant | Partially accurate |
| 2 | What do students say about Professor Zumrut's exams? | CS385 algorithms exams are difficult, attendance and textbook reading essential | Said it didn't have enough information despite relevant chunks existing in the vector store | Partially relevant | Inaccurate |
| 3 | What are common complaints about the Stevens CS program? | Heavy exam-based grading, professors difficult to understand, high tuition, weak admin support | Refused to answer, said documents only covered general Stevens complaints not CS-specific ones | Partially relevant | Inaccurate |
| 4 | What are the best advantages of the Stevens CS program? | Small class sizes, NYC proximity, strong career placement, research opportunities, rigorous curriculum | Correctly identified NYC connections, AI curriculum, new School of Computing, collaborative environment | Relevant | Accurate |
| 5 | What is the ROI of Stevens CS Program? | Top 10-15 nationally for ROI, ~97% employment within 6 months, average salary ~$100k | Said it didn't have enough information despite ROI and salary data existing in documents | Off-target | Inaccurate |

---

## Failure Case Analysis

**Question that failed:**
"What are Professor Zumrut's exams like?"

**What the system returned:**
"I don't have enough information on that. The documents mention Professor Zumrut's teaching style and participation encouragement but do not specifically discuss her exams."

**Root cause (tied to a specific pipeline stage):**
Retrieval failure. The relevant chunk describing CS385 exam difficulty ("Algorithms is a difficult class, attend lecture, ask questions, and be sure to read the relevant info in the textbook") was ranked 4th at distance 1.113. The query used the word "exams" but the most relevant chunk used "algorithms class" and "difficult" - the semantic gap between query language and document language was too large for all-MiniLM-L6-v2 to rank it highly enough.

**What you would change to fix it:**
Add exam-specific keywords to the document metadata, or use a larger embedding model with stronger domain-specific semantic understanding. Alternatively, rewriting the query to "How difficult is CS385 with Zumrut?" would likely surface the correct chunk.

---

## Spec Reflection

**One way the spec helped you during implementation:**
The planning.md architecture diagram made it straightforward to prompt Claude for each pipeline stage in sequence. Having the tools labeled at each stage meant the generated code matched the spec without needing significant corrections.

**One way your implementation diverged from the spec, and why:**
The spec suggested a query.py file with an ask() function as the central entry point. Instead the pipeline was split across ingest.py, embed.py, and generate.py. This made each stage easier to test independently but required app.py to import from multiple files rather than one central module.

---

## AI Usage

**Instance 1**
- *What I gave the AI:* The Chunking Strategy and Documents sections of planning.md plus the pipeline architecture diagram
- *What it produced:* ingest.py with load_documents() and chunk_documents() using RecursiveCharacterTextSplitter with chunk size 500 and overlap 50
- *What I changed or overrode:* Updated the import path from langchain.text_splitter to langchain_text_splitters after the generated code threw a ModuleNotFoundError due to a version change in langchain

**Instance 2**
- *What I gave the AI:* The Retrieval Approach section of planning.md, the pipeline diagram, and the grounding requirement from the spec
- *What it produced:* embed.py with embed_and_store() and retrieve() functions, and generate.py with a Groq prompt template enforcing context-only answers
- *What I changed or overrode:* Verified the grounding prompt actually refused out-of-scope queries by testing with "What is the weather like on Mars?" - the system correctly said it had no information, confirming the prompt enforcement worked as intended