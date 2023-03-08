## Info

The Python scripts in this folder use hard coded credentials (username,password) 
and also for IDP provider URL, and Data Pod-URL.

The password is loaded from a .env file. This .env file must stay on your computer.
We have added it to .gitignore file.

Please create a .env file before you start with the tutorial.
The content of your .env file must be:

```
PASSWORD = "your_password"
```

Please change the variables:

```
USERNAME = "kamir"
IDP = 'https://solidcommunity.net'
POD_ENDPOINT = "https://kamir.solidcommunity.net"
```