# Run weaviate
```docker-compose -f ./weaviate/docker-compose.yml up -d  ```

# Create and activate a venv
```python -m venv .venv``` 

```source .venv/bin/activate```
# Install libs
```pip3 install -r ./app/requirements.txt --no-cache-dir```

# Run app
```uvicorn app.main:app --reload```   