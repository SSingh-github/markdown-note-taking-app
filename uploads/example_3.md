# Welcome to Flask API Upload

## Introduction
This file demonstrates how to upload and handle Markdown files using a Flask-based API. Below are some key highlights:

- **Simple File Upload**: Easily upload `.md` files using a REST API.
- **Flask Framework**: Lightweight and powerful for web applications.
- **Organized Storage**: Store uploaded files securely in a designated folder.

---

## Features

### 1. Easy to Use
Just send a POST request with your Markdown file to the API endpoint:
```bash
curl -X POST -F "file=@example.md" http://127.0.0.1:5000/api/upload
