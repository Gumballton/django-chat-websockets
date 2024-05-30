#  Django Chat Websockets

![django](https://img.shields.io/badge/django-5.0.6-blue)
![channels](https://img.shields.io/badge/channels-4.1.0-blue)
![django-channels](https://img.shields.io/badge/django_channels-0.7.0-blue)
![daphne](https://img.shields.io/badge/daphne-4.1.2-blue)
![psycopg2](https://img.shields.io/badge/psycopg2-2.9.9-blue)

----

A full-fledged web chat application developed using Django Channels to handle websockets.

----

![](https://i.imgur.com/DTgNg5r.png)

## Description
This application has the functionality of _registration_, _authorization_, _password recovery_ by email, creating your _own_ chats both public and private, the ability to _add other users_ to your chat if you are the owner of the chat.Exiting the chat for _regular users_ and _deleting_ the chat for the _creator_.

## Installation and launch

1. **Cloning the repository:**
   ```bash
    git clone <repository URL>
    ```

2. **Installing dependencies:**
   
    Go to your project directory and install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. **Setting all private data in .env in chatsite application:**
    ```bash
    DB_NAME=your_database_name
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    DB_HOST=your_database_host
    DB_PORT=your_database_port

    EMAIL_HOST_USER=your_email_host_user
    EMAIL_HOST_PASSWORD=your_email_host_password
    ```

4. **Applying migrations:**
   
   Apply migrations to create the database:

    ```bash
    python manage.py migrate
    ```

5. **Starting the server:**
   
    Start the Django development server:
    ```bash
    python manage.py runserver
    ```

6. **Connecting to the application:**

    Once the server has started, go to `http://127.0.0.1:8000/` in your browser and start chatting.


## Usage

1. **Registration and login:**
   
    Before using the chat, you must _register_ or _log in_.

2. **Creating and joining rooms:**
   
    Once logged in, you can _create_ new rooms or _join_ existing ones.

3. **Sending messages:**

    In the selected room, you can _send messages_ and _see messages_ from other users in _real time_.

## Author

- Vladimir Petrov [@gumballton](https://github.com/Gumballton)
