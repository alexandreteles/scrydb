# Matching an index to its encoder

The paper used 4,096-dimensional Qwen3-Embedding-8B vectors. The Python
wrapper defaults to 512 output dimensions and a query prompt intended for
its default Mixedbread model. Changing the model name leaves both settings
in effect.

To use precomputed vectors, pass the actual input field to both indexing
methods. The paper's companion JSONL uses `embedding`. The library default is
`emb`. Stored queries with compatible embeddings can be searched by ID without
attaching a model.

To create full-width vectors locally, make the instruction and dimensions
explicit. For example, these settings select the query instruction used for
FiQA. The complete embedding pipeline also depends on the model revision,
tokenizer, document preparation and inference runtime.

```python
from scrydb import SentenceEmbedding

task = "Given a financial question, retrieve user replies that best answer the question"
encoder = SentenceEmbedding(
    "Qwen/Qwen3-Embedding-8B",
    truncate_dim=None,
    query_prompt=f"Instruct: {task}\nQuery:{{query}}",
)
```

## Proposed metadata for shared indexes

Record model and revision, output dimensions, pooling, input length limit,
query instruction, document preprocessing, normalization and available
precisions. The caller must be able to supply this information when importing
external vectors. Matching dimensions are necessary but different encoders
can produce incompatible vectors with the same length.

Existing files can establish dimensions from the vector tables. Leave unknown
model or prompt settings unspecified. Allow them to continue serving stored
queries. Compare known settings when appending model-produced vectors or
embedding an interactive query. A new data-format version and an explicit
migration are decisions for review before introducing write-time enforcement.
