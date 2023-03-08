# workshop-solid-data-pods

The material for our workshop around solid data pods.

## Step 1 : Prepare the Solid-Data pod on your local computer.

```
git clone https://github.com/CommunitySolidServer/CommunitySolidServer.git
cd CommunitySolidServer
docker run --rm -v ~/Solid:/data -p 3000:3000 -it solidproject/community-server:latest
```

