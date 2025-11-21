---
title: "heapdump"
platform: "picoCTF"       
category: "web"        
difficulty: "easy"
tags: ["heapdump"]
date: "2025-07-02"
---

# HEAPDUMP

**Piattaforma:** picoCTF
**Categoria:** web
**Difficoltà:** easy
**Tag:** heapdump
**Data:** 2025-07-02

## Descrizione
Welcome to the challenge! In this challenge, you will explore a web application and find an endpoint that exposes a file containing a hidden flag. The application is a simple blog website where you can read articles about various topics, including an article about API Documentation. Your goal is to explore the application and find the endpoint that generates files holding the server’s memory, where a secret flag is hidden. The website is running picoCTF News.

## Analisi  
Pagina di blog.

## Svolgimento Passo-passo
È letteralmente scritto nella descrizione: consultando le api disponibili si puiò trovare 
``` GET /heapdump Diagnosing the memory allocation. ```
Mandando la richiesta si riceve un file contente la flag in chiaro.

