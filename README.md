**Activate the virtual environment**

```
source blockchain-env/bin/activate
```


**Install all packages**

```
pip3 install -r requirements.txt
```

**Run the tests**

Make sure to activate virtual environment

```
python3 -m pytest backend/tests
```

**Run the application and API**

Make sure to activeate the virtual environment.

```
pytthon3 -m backend.app
```


**Run a peer instance**

Make sure to activeate the virtual environment.

```
export PEER=True && python3 -m backend.app
```

**Run the frontend**

In the frontend directory:

```
npm run start
```

**Seed backend with data**

Make sure to activate virtual environment

```
export SEED_DATA=True && python3 -m backend.app
```
