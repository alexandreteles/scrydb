# Proposal for externally encoded interactive queries

An application may already have an embedding for an incoming query. The
current one-query search interface accepts text. Today a caller can register
a model or write the query into the database and search its stored ID.

Add an optional keyword-only `query_embedding` argument to `Index.search`.
Accept a single finite, one-dimensional float vector, convert it to float32,
and check the expected document dimension. A supplied vector should win over
an attached model. Quantize it using the same SQLite expressions used for a
freshly encoded query. Reuse it for both the first stage and a rerank.

A semantic-only request can use a vector without text. Hybrid search and a
lexical first stage still require text for FTS5. Existing positional text
calls and stored-ID batch search retain their existing meaning.

The review should settle how a caller declares which encoder produced a
vector when provenance is available, and what error to return for text-only
modes given an unused vector. No write to the query tables is needed for this
operation.
