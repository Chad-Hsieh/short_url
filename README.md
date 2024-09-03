# URL Shortener API Documentation

## Overview

This API provides endpoints for creating short URLs and retrieving the original URLs.

## Endpoints

### 1. Create Short URL

- **URL**: `/api/shorten`
- **Method**: `POST`
- **Payload**:
    ```json
    {
        "original_url": "https://example.com"
    }
    ```
- **Response**:
    - **201 Created**:
        ```json
        {
            "short_url": "http://localhost:5000/abc123",
            "expiration_date": "2024-09-29T00:00:00",
            "success": true,
            "reason": ""
        }
        ```
    - **400 Bad Request**:
        ```json
        {
            "success": false,
            "reason": "Invalid URL format."
        }
        ```

### 2. Redirect Using Short URL

- **URL**: `/<short_url>`
- **Method**: `GET`
- **Response**:
    - **302 Found**: Redirects to the original URL.
    - **404 Not Found**:
        ```json
        {
            "error": "Short URL not found."
        }
        ```
    - **410 Gone**:
        ```json
        {
            "error": "Short URL has expired."
        }
        ```

<br/>

# User Guide: Running the URL Shortener in Docker

## Prerequisites

- Docker installed on your machine.

## Steps to Run

1. Pull the Docker image from Docker Hub:

    ```bash
    docker pull zowk52/url-shortener
    ```

2. Run the Docker container:

    ```bash
    docker run -d -p 5000:5000 zowk52/url-shortener
    ```

3. Access the API:

    - To create a short URL, send a POST request to `http://localhost:5000/api/shorten` with a JSON payload containing the `original_url`.
    - To retrieve the original URL, open the short URL in your browser.


