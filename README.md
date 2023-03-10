## Hands-on workshop about Solid Data Pods

The repository contains the material for our CLT2023 workshop around Solid Data Pods.

We will explore the anatomy of applications using Solid Data Pods.

This workshop has been prepared for the community event: __Chemnitzer Linux-Tage__.

![docs/img.png](docs/img.png)

![docs/intro.png](docs/intro.png)

# Overview 

This repository will be used for managing our open colaboration around the emerging topic: SOLID Data Pods. 
It is a private initiative supported by ecolytiq GmbH, OnfK gUG and the contributing developers.

This work uses the  __Apache License, Version 2.0__, January 2004 http://www.apache.org/licenses/.
 


![docs/image-2023-03-08-14-51-01-190.png](docs/image-2023-03-08-14-51-01-190.png)

# Workshop Goals

__Each participant:__
- has one (or more) registered Solid Data Pod for own experiments.
- can create a local Solid pod for experiments.
- can use the solid-shell to interact with a Solid Data Pod
- can start a local solid App (using Node.js or Flask)
- can execute and extend a Python script to interact with its Solid Data Pod
- knows the anatomy of a typical Solid App.
- has a basic understanding of the Solid Protocol
- knows the purpose of the structures data model offered by Solid Pods in comparison to other establish web based storage solutions (SFTP, WebDAV)

# Optional Goals

We define an example application for a use-case created by the workshop participants.

# List of Modules
Using the projects in this repository we provide material to explore Solid Pods and the usage of the Solid Protocol.

## Creation of a local pod
[Module 1](module-1/README.md)

## Working with solid-shell
[Module 2](module-2/README.md)

## Node.js based solid-client-app
This application stub uses the Inrupt JavaScript client libraries.

[Module 3](module-3/README.md)

## Python based solid-client-apps
[Module 4](module-4/README.md)

## SpringBoot application in Kotlin
[Module 5](module-5/README.md)

# Ideas for future extension

## How to dump a dataframe into a datapod?

## How to copy/move data from one pod to another?

## How to expose metadata in a pod, which becomes a "Meta-Pad"?
We can imagine, that indexed data can be exposed for other collaborators in a data pod. Many pods together could hold data which is then indexed in a central place for search, but what get added into the search corpus is controled by publishing documents into the pod. Deletion of a document leads to removal from the index. 

This means, that preindexing is done before publishing and all control regarding masking, anonymization and randomization is the publishers hand.

## Pod-Hosting using AWS, Azure, or fly.io

# Open Topics

## How to safeguard the Solid Pod?
## How to backup automatically?
## How to integrate in an hybrid personal storage cloud?

