## Register a User

### Sample **Post** req. `http://localhost:8000/api/auth/register`

```json
{
  "username": "adarshere",
  "email": "adarshere@sample.com",
  "password": "examplePassword1!"
}
```


```json
{
  "username": "adarshere",
  "email": "adarshere@sample.com",
  "id": 1,
  "is_active": true,
  "role": "user"
}
```


## Sample User

```json
[
    {
        "username": "adarshere",
        "email": "adarshere@sample.com",
        "password": "examplePassword1!"
    },
    {
        "username": "anshu",
        "email": "anshu@sample.com",
        "password": "examplePassword1!"
    }
]
```