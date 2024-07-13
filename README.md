# Flask Messaging System with RabbitMQ/Celery and ngrok

This project demonstrates a simple messaging system using Flask, RabbitMQ/Celery for asynchronous tasks, and ngrok for exposing the local development server to the internet.

## Table of Contents

- [Flask Messaging System with RabbitMQ/Celery and ngrok](#flask-messaging-system-with-rabbitmqcelery-and-ngrok)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)

## Setup

### Prerequisites

- Python 3.x installed locally
- RabbitMQ installed and running locally
- Flask, Celery, and other dependencies installed (see requirements.txt)
- ngrok installed for tunneling to expose local server

### Installation

Clone the repository and navigate into the project directory:

```bash
git clone https://github.com/pipthablack/task3-messaging.git
cd flask-messaging
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Set up environment variables:
Create a `.env` file in the project root and add the following:

```env
MAIL_ADD
MAIL_PASS
LOG_FILE_PATH
SMTP_SERVER
SMTP_PORT
```