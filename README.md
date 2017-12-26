# undefined-user-api

## URL
http://undefined-api.herokuapp.com/

## Endpoints
### `users/`
- GET: All users list
- POST: Register

### `users/<uuid>/`
- GET: User detail specified by `<uuid>`
- POST: Not allowed

### `sessions/`
- GET: Not allowed
- POST: Login

## Testing on local
Follow these steps,

### 1. Clone this repo
```
$ git clone https://github.com/chainazo/undefined-user-api
```

### 2. Create Virtual Env
```
$ python3 -m venv <env-name>
$ source <env-name>/bin/activate
```

for fish or csh shell,
```
$ source <env-name>/bin/activate.fish
$ source <env-name>/bin/activate.csh
```

### 3. Install dependencies
```
$ pip install -r requirements.txt
```

### 4. Run test scripts
```
$ cd undefined-user-api
$ python manage.py test
```

## Author Information
[Byeong Gyu Choi](https://github.com/gyukebox/)
