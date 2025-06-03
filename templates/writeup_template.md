---
title: "<Titolo della Challenge>"
platform: "<piattaforma>"       # es. picoCTF, htb, tryhackme, ecc.
category: "<categoria>"         # es. web, reverse, crypto, forensics, binary, network
difficulty: "<difficoltà>"      # es. easy, medium, hard
tags: []                        # es. ["xss", "lfi"], ["rop", "heap"], ["rsa", "padding-oracle"]
date: "<YYYY-MM-DD>"
---

# {{ title }}

**Piattaforma:** {{ platform }}  
**Categoria:** {{ category }}  
**Difficoltà:** {{ difficulty }}  
**Tag:** {{ tags | join(", ") }}  
**Data:** {{ date }}

## Descrizione  
(Breve contesto della challenge.)

## Analisi  
- (Annotazioni preliminari, file, output, pagine web.)

## Svolgimento Passo-passo
1. (Passo 1)
2. …

## PoC / Exploit
```bash
# Comandi o script per l'exploit
