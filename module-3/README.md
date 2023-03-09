# Step 3 
## Create your own Solid Client Application

### Terminal 1

```
git clone https://github.com/CommunitySolidServer/CommunitySolidServer.git
cd CommunitySolidServer
docker run --rm -v ~/Solid:/data -p 3000:3000 -it solidproject/community-server:latest
```

### Terminal 2

```
cd solid-demo-app
npm init -y
npm install @inrupt/solid-client @inrupt/solid-client-authn-browser @inrupt/vocab-common-rdf @inrupt/vocab-solid
npm install buffer
npm install webpack webpack-cli webpack-dev-server css-loader style-loader --save-dev
npm run build && npm run start
```