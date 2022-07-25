### Description
You can use this small project when application not supports HTTP_PROXY/HTTPS_PROXY/NO_PROXY envs and you at corporate proxy server area which accepted only by PROXY protocol.


#### Settings
Edit `manifests/deployment.yaml` for change ENVs:
- HTTP_PROXY – corporate proxy server with proxy protocol
- PROXY_URL – URL which you want to proxy
- TIMEOUT_SECONDS – non-required, timeout for PROXY_URL connection

WARNING: pop some headers on forwarding (edit main.py:23 for fix it)


#### Deploy
```shell
docker build -t telegram-proxy:0.2 .
docker push telegram-proxy:0.2

k create -f manifests/deployment.yaml -n sentry-latest
k create -f manifests/service.yaml -n sentry-latest

# specify address in your app which it needed – http://telegram-proxy

# PROFIT
```
