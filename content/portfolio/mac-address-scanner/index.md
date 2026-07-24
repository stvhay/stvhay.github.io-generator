+++
title = 'MAC Address Scanner'
weight = 52
description = 'Network utility using FastAPI and ZeroMQ to identify devices on a subnet by collecting and categorizing MAC addresses.'
[[resources]]
src = 'img.jpeg'
[resources.params]
alt = 'Abstract network map with numbered devices connected by circuit traces.'
+++

I needed something that would allow a commissioning team to quickly identify
devies on a subnet without connecting directly to the network. A small HTML
utility using a stack of uvicorn, FastAPI, and ZeroMQ collects tcpdump
information and list MAC addresses seen on a network. They are divided into
vendor categories that map to different subsystems.
