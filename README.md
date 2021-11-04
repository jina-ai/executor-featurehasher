# FeatureHasher

Convert a collection of features to a fixed-dimensional matrix using the hashing trick.

Note, this requires Jina>=2.2.5.

## Example

Here I use `FeatureHasher` to hash each sentence of Pride and Prejudice into a 128-dim vector, and 
then use `.match` to find top-K similar sentences.

To use other Example, 

```python
from jina import Document, DocumentArray, Executor

# load <Pride and Prejudice by Jane Austen>
d = Document(uri='https://www.gutenberg.org/files/1342/1342-0.txt').convert_uri_to_text()

# cut into non-empty sentences store in a DA
da = DocumentArray(Document(text=s.strip()) for s in d.text.split('\n') if s.strip())

exec = Executor.from_hub('jinahub://FeatureHasher')

exec.encode(da)

print('matching...')
da.match(da, exclude_self=True, limit=5, normalization=(1, 0))
print('total sentences: ', len(da))
for d in da:
    print(d.text)
    for m in d.matches:
        print(m.scores['cosine'], m.text)
    input()
```

---

```text
           Flow@17400[I]:🎉 Flow is ready to use!
	🔗 Protocol: 		GRPC
	🏠 Local access:	0.0.0.0:52628
	🔒 Private network:	192.168.178.31:52628
	🌐 Public address:	217.70.138.123:52628
⠹       DONE ━╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0:00:01 100% ETA: 0 seconds 40 steps done in 1 second
total sentences:  12153
﻿The Project Gutenberg eBook of Pride and Prejudice, by Jane Austen
<jina.types.score.NamedScore ('value',) at 5798762768> *** END OF THE PROJECT GUTENBERG EBOOK PRIDE AND PREJUDICE ***
<jina.types.score.NamedScore ('value',) at 5798763472> *** START OF THE PROJECT GUTENBERG EBOOK PRIDE AND PREJUDICE ***
<jina.types.score.NamedScore ('value',) at 5798762448> production, promotion and distribution of Project Gutenberg-tm
<jina.types.score.NamedScore ('value',) at 5798762576> Pride and Prejudice
<jina.types.score.NamedScore ('value',) at 5798762512> By Jane Austen

This eBook is for the use of anyone anywhere in the United States and
<jina.types.score.NamedScore ('value',) at 5798762384> This eBook is for the use of anyone anywhere in the United States and
<jina.types.score.NamedScore ('value',) at 5798762512> by the awkwardness of the application, and at length wholly
<jina.types.score.NamedScore ('value',) at 5798762832> Elizabeth passed the chief of the night in her sister’s room, and
<jina.types.score.NamedScore ('value',) at 5798762704> the happiest memories in the world. Nothing of the past was
<jina.types.score.NamedScore ('value',) at 5798761680> charities and charitable donations in all 50 states of the United
```

In practice, you can implement matching and storing via an indexer inside `Flow`. 
This example is only for demo purpose so any non-feature hashing related ops are implemented outside the Flow to avoid distraction.