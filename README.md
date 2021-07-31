# Hit-Maker

### SignUp (path /signup)
```
Request
{
	"username":"long.nguyen1",
	"password": "123456",
	"name": "Abcxyz"
}

Response
Status  |   Meaning
201     |   Success
202     |   UserName is registered

```

### Login (path /login)
```
Request
{
	"username":"long.nguyen",
	"password": "123456"
}
Response Success
{
  "data": [
    {
      "keySignature": "D",
      "saveName": "abc",
      "streamParts": [
        [{
           "chord": [
            {
                "note": "F/4"
            },
            {
                "note": "E/5",
            },
            {
                "note": "B#/4",
            }],
           "dur": "16"
          },
         {
           "note": "B-",
           "dur": "16"
        },
        {
            "keySignature": "B-",
            "note": "F",
            "dur": "24"
        },
        {
            "note": "F",
            "dur": "4"
        }
        ],
        [{
           "note": "F",
           "dur": "16"
          },
            {
                "note": "F",
                "dur": "16"
            }
        ]],
      "timeSignature": "3/4"
    }
  ],
  "name": "Long",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNJZCI6ImM3OGQ5ZjBiLWM1NDUtNGUyYi1hZTM4LTA3ODFkZTg4ZGZjOCIsImV4cCI6MTYyNjM3NDQ1OTk3Nn0.l_JxHDdedHFrT7A7o4RKRa0OEaMph7yRazldPGC8dLE"
}

Status  |   Meaning
401     |   User not exist or null Password
401     |   Wrong Password
```
### Generate (path /generate)
```
{   
    "timeSignature": "3/4",
    "keySignature": "D",
    "streamParts": [
        [{
           "chord": [
            {
                "note": "F/4"
            },
            {
                "note": "E/5",
            },
            {
                "note": "B#/4",
            }],
           "dur": "16"
          },
         {
           "note": "B-",
           "dur": "16"
        },
        {
            "keySignature": "B-",
            "note": "F",
            "dur": "24"
        },
        {
            "note": "F",
            "dur": "4"
        }
        ],
        [{
           "note": "F",
           "dur": "16"
          },
            {
                "note": "F",
                "dur": "16"
            }
        ]]
}

Response
{   
    "timeSignature": "3/4",
    "keySignature": "D",
    "streamParts": [
        [{
           "chord": [
            {
                "note": "F/4",
                "tie": "start" //this is for legato note or chord
            },
            {
                "note": "E/5"
            },
            {
                "note": "B#/4"
            }],
           "dur": "16"
          },
         {
           "note": "F/4",
           "dur": "8"
        },
        {
            "keySignature": "B-",
            "note": "F/4",
            "dur": "24"
        },
        {//no note or chords means Rest
            "dur": "4"
        },
        ],
        [{
           "note": "F/4",
           "dur": "16"
          },
            {
                "note": "F/4",
                "dur": "8"
            }
        ]]
}

```

### Save (path /save)
## Save your data to mongoDb
```
Request
{   
    "saveName": 'abc',
    "timeSignature": "3/4",
    "keySignature": "D",
    "streamParts": [
        [{
           "chord": ["F/4", "E/5", "B#/4"],
           "dur": "16"
          },
         {
           "note": "F/4",
           "dur": "8"
        },
        {
            "keySignature": "B-",
            "note": "F/4",
            "dur": "24"
        },
        {//no note or chords means Rest
            "dur": "4"
        },
        ],
        [{
           "note": "F/4",
           "dur": "16"
          },
            {
                "note": "F/4",
                "dur": "8"
            }
        ]]
}
Response 
{   
    "saveName": 'abc',
    "timeSignature": "3/4",
    "keySignature": "D",
    "streamParts": [
        [{
           "chord": ["F/4", "E/5", "B#/4"],
           "dur": "16"
          },
         {
           "note": "F/4",
           "dur": "8"
        },
        {
            "keySignature": "B-",
            "note": "F/4",
            "dur": "24"
        },
        {//no note or chords means Rest
            "dur": "4"
        },
        ],
        [{
           "note": "F/4",
           "dur": "16"
          },
            {
                "note": "F/4",
                "dur": "8"
            }
        ]]
}
```
### Download (path /download/)
## this API will convert your data in mongoDb to midi and send it to you
```
Request
{}
Response, file you need
```
#DOCKER
```
docker-compose build //đợi lâu vcl ý nên chạy xong ngồi làm gì khác đi
docker-compose up //post vào link 127.0.0.1:4000 nhé
```