# DocuChat Project Structure

```
docuchat/
├── src/
│   ├── pdf_processing/          # Kişi 1
│   │   ├── __init__.py
│   │   ├── qwen_processor.py
│   │   ├── extractor.py
│   │   └── bbox_utils.py
│   │
│   ├── vector_db/               # Kişi 2
│   │   ├── __init__.py
│   │   ├── pinecone_client.py
│   │   ├── embeddings.py
│   │   └── indexing.py
│   │
│   ├── llm/                     # Kişi 3
│   │   ├── __init__.py
│   │   ├── hermes_client.py
│   │   ├── rag_pipeline.py
│   │   └── memory.py
│   │
│   ├── ui/                      # Kişi 4
│   │   ├── __init__.py
│   │   ├── gradio_app.py
│   │   ├── pdf_viewer.py
│   │   └── chat_interface.py
│   │
│   ├── models/                  # Shared models
│   │   ├── __init__.py
│   │   ├── document_models.py
│   │   └── response_models.py
│   │
│   └── utils/                   # Shared utilities
│       ├── __init__.py
│       ├── config.py
│       └── logger.py
│
├── tests/
│   ├── test_pdf_processing/
│   ├── test_vector_db/
│   ├── test_llm/
│   └── test_ui/
│
├── docs/
│   ├── api_documentation.md
│   ├── setup_guide.md
│   └── architecture.md
│
├── requirements.txt
├── .gitignore
├── .env.example
├── docker-compose.yml
└── README.md
```
