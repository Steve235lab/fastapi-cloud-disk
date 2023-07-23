# FastAPI Cloud Disk

A backend server program based on FastAPI framework which will host a personal cloud disk service on your own server.

## Features

1. User management
2. Upload & download files via HTTP requests
3. Share file links to your friends to download without logging in or signing up

## Quick Start

1. Install Python 3.11

2. Install and setup a PostgreSQL database service, then create a new database named "fastapi_cloud_disk"

3. Install requirements

   ```shell
   pip3 install -r requirements.txt
   ```

4. Configure the service

   We use ```.env``` file to configure the service and the environment variables will be loaded when the service starts. For security concerns, please don't track the ```.env``` file with Git or share it with others. Here's a template of the ```.env```:

   ```.env
   # .env
   
   # URL to the database you created in step 2
   POSTGRESQL_DB_URL=postgresql://<username>:<password>@<host>:<port>/fastapi_cloud_disk
   
   # Absolute path to a folder where files uploaded by users will be placed in
   STORAGE_PATH=<path/to/an/empty/folder>
   
   # The public URL for users to access the service
   SERVICE_URL=<http://foo_bar.com/ or http://public_ip:port/>
   ```

5. Initialize database with Alembic

   ```shell
   cd alembic
   alembic upgrade head
   cd ..
   ```

6. Start the service

   ```shell
   python3 ./main.py
   ```

   
