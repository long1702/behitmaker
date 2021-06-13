# Hit-Maker
### Generate (path /generate)
```
Request
{
    "timeSignature": "3/4",
    "streamParts": [
        [{
           "note": "A",
           "dur": "1/4"
          },
         {
           "note": "A",
           "dur": "1/4"
        }],
        [{
           "note": "A",
           "dur": "1/4"
          },
         {
           "note": "A",
           "dur": "1/4"
        }]]
}

Response
{
    "timeSignature": "3/4",
    "streamParts": [
        [{
           "note": "A",
           "dur": "1/4"
          },
         {
           "note": "A",
           "dur": "1/4"
        }],
        [{
           "note": "A",
           "dur": "1/4"
          },
         {
           "note": "A",
           "dur": "1/4"
        }]]
}

```

### Save (path /save)
```
Request
{
    "saveName": "abc"
    "timeSignature": "3/4",
    "streamParts": [
        [{
           "note": "A",
           "dur": "1/4"
          },
         {
           "note": "A",
           "dur": "1/4"
        }],
        [{
           "note": "A",
           "dur": "1/4"
          },
         {
           "note": "A",
           "dur": "1/4"
        }]]
}
Response
{
    "result" : "OK",
    "path" : "./a/b/abc.mid"
}
```
### Download (path /download/<path:filename>)
```
Request (null or this)
{
    "saveName": "abc"
    "timeSignature": "3/4",
    "streamParts": [
        [{
           "note": "A",
           "dur": "1/4"
          },
         {
           "note": "A",
           "dur": "1/4"
        }],
        [{
           "note": "A",
           "dur": "1/4"
          },
         {
           "note": "A",
           "dur": "1/4"
        }]]
}

Response, file you need
```
