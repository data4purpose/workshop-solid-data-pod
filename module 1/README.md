## Step 1 : Prepare the Solid-Data pod on your local computer.

```
git clone https://github.com/CommunitySolidServer/CommunitySolidServer.git
cd CommunitySolidServer

# Run the image, serving your `~/Solid` directory on `http://localhost:3000`
docker run --rm -v ~/Solid:/data -p 3000:3000 -it solidproject/community-server:latest

# Or use one of the built-in configurations
docker run --rm -p 3000:3000 -it solidproject/community-server -c config/default.json

# Or use your own configuration mapped to the right directory
docker run --rm -v ~/solid-config:/config -p 3000:3000 -it solidproject/community-server -c /config/my-config.json

# Or use environment variables to configure your css instance
docker run --rm -v ~/Solid:/data -p 3000:3000 -it -e CSS_CONFIG=config/file-no-setup.json -e CSS_LOGGING_LEVEL=debug solidproject/community-server
```

Documentation for the _CommunitySolidServer_ is available here:
https://github.com/CommunitySolidServer/CommunitySolidServer