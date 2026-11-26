# Opening a database built before vec0

The earlier layout stored binary and float blobs in ordinary tables keyed by
external document or query ID. The current layout stores typed vectors in
vec0 tables keyed by the rowid of the payload. The payload and full-text names
survived the change. An old file can therefore open and return lexical hits
while dense search does not see its existing vectors.

## Proposed behavior

Identify the legacy schema from its vector tables and column definitions.
Tell the caller which layout is present before starting a dense read or
appending vectors. Allow lexical access to existing files. Treat a file with
both layouts as ambiguous until its contents have been examined.

Provide an explicit offline conversion into a new file. Preserve public IDs,
payloads and indexed text, and resolve each legacy vector through its external
ID. If full vectors are available, feed them through the current conversion
routines. For binary-only inputs, confirm packing order, dimensionality and
distance equivalence before transforming the stored bytes. Where dimensions
or encoding cannot be established, request the source vectors.

Validate row counts, ID ownership, precision coverage and known distances
before using the new file. Record a schema version for future readers. Opening a
file for search should never silently perform a collection-wide rewrite.
