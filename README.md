# Local-AI-Document-Intelligence

A comprehensive, open-source pipeline for local document understanding, classification, and semantic retrieval (RAG-ready).


# Local AI Document Intelligence Pipeline

## Project Overview

This project implements a comprehensive, **local AI workflow** for document intelligence, focused on processing diverse document types entirely on a local machine without reliance on external cloud services or hosted APIs.

This pipeline performs document classification, structured data extraction, and deep semantic search, making it ideal for privacy-sensitive or offline enterprise environments.

### Core Deliverables Met:

1. **Ingestion & Processing:** Read and clean text from PDF documents.
2. **Classification & Extraction:** Categorize documents (Invoice, Resume, Utility Bill, Other) and extract structured key-value data (e.g., `total_amount`, `experience_years`).
3. **Simple Retrieval System:** A high-performance **local semantic search** component.

---

## 🔒 Technical Rules and Compliance

This solution adheres strictly to the requirements of running an AI workflow using **open-source libraries only**.

| Requirement                 | Method Used                                                                                   | Compliance Status   |
| :-------------------------- | :-------------------------------------------------------------------------------------------- | :------------------ |
| **No Hosted/Paid AI** | **Strictly open-source only.** No use of OpenAI, Claude, or Gemini APIs.                | **COMPLIANT** |
| **Local Processing**  | All AI and processing tasks (PDF reading, embedding, indexing, search) run on local hardware. | **COMPLIANT** |
| **Allowed Libraries** | PyPDF2, SentenceTransformers, FAISS, PyTorch/Transformers, Regex.                             | **COMPLIANT** |
| **Interface**         | Command Line Interface (CLI) is used for input and output.                                    | **COMPLIANT** |

---

## 🛠️ Installation and Setup

### 1. Prerequisites

* Python 3.8+
* Git

### 2. Clone the Repository

```bash
git clone [https://github.com/AhmadFarazKha/Local-AI-Document-Intelligence.git](https://github.com/AhmadFarazKha/Local-AI-Document-Intelligence.git)
cd Local-AI-Document-Intelligence
```
