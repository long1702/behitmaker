# Hit-Maker
### Generate (path /generate)
```
Request
{
    "timeSignature": "4/4",
    "streamParts": [//Each element of this array is a music cell
      [//The First element of this array is the upper stream, the second is the lower stream
        [
          {
           "note": "A",
           "dur": "1/2"
          },
          {
           "note": "A",
           "dur": "1/2"
          }
        ],
        [{
           "note": "A",
           "dur": "1/2"
          },
         {
           "note": "A",
           "dur": "1/2"
        }]
      ],
      [
        [{
           "note": "A",
           "dur": "1/2"
          },
         {
           "note": "A",
           "dur": "1/2"
        }],
        [{
           "note": "A",
           "dur": "1/2"
          },
         {
           "note": "A",
           "dur": "1/2"
        }]
      ]
    ]
}

Response
{
    "timeSignature": "4/4",
    "streamParts": [//Each element of this array is a music cell
      [//The First element of this array is the upper stream, the second is the lower stream
        [
          {
           "note": "A",
           "dur": "1/2"
          },
          {
           "note": "A",
           "dur": "1/2"
          }
        ],
        [{
           "note": "A",
           "dur": "1/2"
          },
         {
           "note": "A",
           "dur": "1/2"
        }]
      ],
      [
        [{
           "note": "A",
           "dur": "1/2"
          },
         {
           "note": "A",
           "dur": "1/2"
        }],
        [{
           "note": "A",
           "dur": "1/2"
          },
         {
           "note": "A",
           "dur": "1/2"
        }]
      ]
    ]
}

```

### Save (path /save)
```
Request
{
    "saveName": "abc",
    "timeSignature": "4/4",
    "streamParts": [//Each element of this array is a music cell
      [//The First element of this array is the upper stream, the second is the lower stream
        [
          {
           "note": "A",
           "dur": "1/2"
          },
          {
           "note": "A",
           "dur": "1/2"
          }
        ],
        [{
           "note": "A",
           "dur": "1/2"
          },
         {
           "note": "A",
           "dur": "1/2"
        }]
      ],
      [
        [{
           "note": "A",
           "dur": "1/2"
          },
         {
           "note": "A",
           "dur": "1/2"
        }],
        [{
           "note": "A",
           "dur": "1/2"
          },
         {
           "note": "A",
           "dur": "1/2"
        }]
      ]
    ]
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
    "saveName": "abc",
    "timeSignature": "4/4",
    "streamParts": [//Each element of this array is a music cell
      [//The First element of this array is the upper stream, the second is the lower stream
        [
          {
           "note": "A",
           "dur": "1/2"
          },
          {
           "note": "A",
           "dur": "1/2"
          }
        ],
        [{
           "note": "A",
           "dur": "1/2"
          },
         {
           "note": "A",
           "dur": "1/2"
        }]
      ],
      [
        [{
           "note": "A",
           "dur": "1/2"
          },
         {
           "note": "A",
           "dur": "1/2"
        }],
        [{
           "note": "A",
           "dur": "1/2"
          },
         {
           "note": "A",
           "dur": "1/2"
        }]
      ]
    ]
}
Response, file you need
```
