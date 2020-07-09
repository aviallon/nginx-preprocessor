# Nginx Preprocessor

Nginx doesn't support variables. However, they are very useful for clarity and simplicity. For instance, you may deploy a set of reverse proxies on port 8080, and when it is ready, change all the ports to 80. If you don't use macros, this will be a hassle. You could use `sed`. But what happens if some of them musn't be changed ? You are stuck. Until now.

## Usage

```
python3 preprocessor.py [-o OUTPUT_FILE] [--verbose] INPUT_FILE
```

By default, if you use it on e.g. `nginx.conf.gen`, then it'll output to `nginx.conf`.
