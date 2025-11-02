import os
import json
from retrieval_system import LocalRetrievalSystem
import document_processor as dp

# --- Configuration ---
INPUT_DIR = "input_docs"
OUTPUT_FILE = "output.json"

def run_pipeline():
    """Runs the full document processing and retrieval pipeline."""
    
    print("\n--- 1. Document Ingestion, Classification, and Extraction ---", flush=True)
    
    if not os.path.exists(INPUT_DIR):
        print(f"Error: Input directory '{INPUT_DIR}' not found. Place files and re-run.", flush=True)
        return

    # Phase A: Processing and Extraction
    results = dp.process_documents(INPUT_DIR)
    
    if not results:
        print("Error: Processed 0 files. Check 'input_docs' folder and file integrity.", flush=True)
        return

    # Save the required output.json
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(results, f, indent=2)
        
    print(f"✅ Processing complete. Results saved to {OUTPUT_FILE}", flush=True)
    print(f"   Processed {len(results)} files.", flush=True)

    # Phase B: Semantic Retrieval System
    print("\n--- 2. Simple Retrieval System Implementation ---", flush=True)
    rs = LocalRetrievalSystem()
    rs.build_index(INPUT_DIR)

    print("\n--- Semantic Search Demonstration (Assessment Requirement) ---", flush=True)
    
    # Required Query Example
    query_1 = "Find all documents mentioning payments due in January."
    print(f"Query: '{query_1}'")
    
    search_results_1 = rs.search(query_1, k=3)
    
    if search_results_1:
        print("  Top 3 Relevant Documents:")
        for filename, score in search_results_1:
            print(f"  - {filename} (Similarity Score: {1 / (1 + score):.4f})") # Convert L2 Distance to score for presentation
    else:
        print("  No documents found for this query.")
        
    # Additional Search Example for completeness
    query_2 = "Who is the experienced professional in AI?"
    print(f"\nQuery: '{query_2}'")
    
    search_results_2 = rs.search(query_2, k=1)
    if search_results_2:
        print("  Top 1 Relevant Document:")
        for filename, score in search_results_2:
            print(f"  - {filename} (Similarity Score: {1 / (1 + score):.4f})")
    else:
        print("  No documents found for this query.")

if __name__ == "__main__":
    run_pipeline()