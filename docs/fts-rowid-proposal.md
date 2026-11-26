# Avoiding a full-text table scan on document replacement

The current index stores the public document ID as an unindexed FTS5 column.
Before inserting a batch, scrydb deletes FTS rows by that ID. This makes even
a batch of entirely new documents search the old FTS table.

Use an explicit integer primary key for each document and a unique constraint
on its existing text ID. Use that integer as the FTS rowid. A replacement can
then delete by rowid and insert the new text in the same transaction as the
payload. Keep the public text ID and the Porter tokenizer. The existing vector
tables already use the document rowid.

## Existing databases

Old FTS rowids were assigned independently and can differ from document
rowids after an update. An in-place change to the DELETE condition could
remove another document's text. Migrate explicitly, with an estimate of
temporary disk space and time, instead of doing a rebuild on open.

Preserve the current documents.rowid values when introducing an integer
primary key so that existing vector rows still refer to the same documents.
Rebuild FTS from its stored text joined by external ID, then switch tables
and record the layout version in one transaction. Before switching, check for
duplicate or unmatched IDs. Where old FTS entries disagree, require a
canonical source for the text. Older payloads may use custom text fields.
Roll back the migration on an ambiguity or an interrupted write.

## Review criteria

A new insert and a replacement should use a rowid lookup. An old database
with deliberately different document and FTS rowids must retain the same
document text, lexical matches and vector ownership after migration.
