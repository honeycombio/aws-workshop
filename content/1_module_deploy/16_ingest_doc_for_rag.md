---
title: "Step 6: Ingest Documentation for RAG"
weight: 36
---

The application uses RAG (Retrieval Augmented Generation) to provide contextually relevant answers. We need to populate the OpenSearch vector database with technical documentation.

The application provides an admin API endpoint that automatically ingests:
- **OpenTelemetry documentation** - Core concepts, instrumentation, semantic conventions
- **Honeycomb Pulumi provider documentation** - Infrastructure as Code patterns for observability

### Option A: Use the Ingest-All API Endpoint (Recommended)

This is the easiest method and requires just a single HTTP request:

1. **Trigger the ingestion process**:
   ```bash
   cd /workshop/ai-workshop/pulumi
   curl -X POST "$(pulumi stack output albUrl)/api/admin/ingest-all" \
     -H "Content-Type: application/json"
   ```

   **What happens during ingestion:**
   - Resets the vector store (deletes existing data)
   - Ingests OpenTelemetry documentation (~7 documents, 55 chunks)
   - Ingests Honeycomb Pulumi provider documentation (~6 documents, 84 chunks)
   - Generates embeddings using AWS Bedrock (Titan Embeddings model)
   - Stores vectors in OpenSearch with k-NN index

   **Ingestion time: ~1-2 minutes** for all documentation

   Expected output:
   ```json
   {
     "success": true,
     "data": {
       "message": "Documentation ingestion completed",
       "otelDocs": {
         "documentsIngested": 7,
         "chunksCreated": 55
       },
       "honeycombPulumiDocs": {
         "documentsIngested": 6,
         "chunksCreated": 84
       },
       "totalDocuments": 13,
       "totalChunks": 139
     }
   }
   ```

2. **Verify ingestion completed**:
   ```bash
   curl "$(pulumi stack output albUrl)/api/admin/vector-store/info"
   ```

   Expected output:
   ```json
   {
     "success": true,
     "data": {
       "indexName": "otel_knowledge",
       "initialized": true,
       "documentCount": 139,
       "sizeInBytes": 1987783
     }
   }
   ```

   The `documentCount` should match the total chunks (139) from the ingestion response.

::alert[**Why Multiple Documents?** The ingestion process chunks large documents into smaller pieces for better semantic search. Each chunk becomes a separate vector in OpenSearch, allowing for more precise retrieval during RAG queries.]{type="info"}

### Option B: Manual Script (Alternative)

If you prefer to run the ingestion script locally or need more control:

1. **Set environment variables**:
   ```bash
   cd /workshop/ai-workshop
   export OPENSEARCH_ENDPOINT=$(cd pulumi && pulumi stack output openSearchEndpoint)
   export OPENSEARCH_USERNAME=admin
   export OPENSEARCH_PASSWORD="<your-opensearch-password-from-ESC>"
   export USE_OPENSEARCH=true
   ```

   **Note**: Replace `<your-opensearch-password-from-ESC>` with the OpenSearch password from your Pulumi ESC environment.

2. **Run the ingestion script**:
   ```bash
   node scripts/ingest-data.js
   ```

   This script only ingests OpenTelemetry documentation. Use Option A to include Honeycomb Pulumi docs.

## Test the Application

Now test the complete application with RAG enabled:

1. Open the application URL in your browser:
   ```bash
   pulumi stack output albUrl
   ```

2. Ask OpenTelemetry-specific questions:
   - "How do I instrument Express.js with OpenTelemetry?"
   - "What are semantic conventions?"
   - "How do I create custom spans?"

3. Observe that the bot now provides detailed, contextually relevant answers with:
   - Source attribution (which document was used)
   - Relevance scores
   - Code examples

::alert[**Success!** You've deployed a production-ready GenAI application with RAG capabilities. The application uses AWS Bedrock for LLM responses and OpenSearch for semantic search over OpenTelemetry documentation.]{type="success"}