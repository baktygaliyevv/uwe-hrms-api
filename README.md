# Horizon Restaurant Management System

## Steps to Launch the Backend

1. **Install Pip Packages:**
   - Open a terminal and navigate to the project directory.
   - Run the following command to install the required packages from `requirements.txt`:

     ```bash
     pip install -r requirements.txt
     ```

2. **Set Up Environment Variables:**
   - Locate the `.env` file in the project directory.
   - Open the `.env` file and fill out the following information:
     - `DATABASE_URL`: MySQL connection URL for your database.
     - `DEBUG`: Set to either `1` for debug mode or `0` for non-debug mode.
     - An example is already prefilled with a connection string for a database hosted on a student's server.
     - Note: If you prefer, you can host your database using the provided dump in `uweresto.sql`.
     - `SENDGRID_API_KEY`: This is the SendGrid API key, used to send verification emails to users. 

3. **Run the Backend:**
    - In the terminal, run the following command to start the API:
    ```bash
     python manage.py runserver 
    ```

4. **User Credentials:**
   - For a list of available users and their credentials, refer to the [CREDENTIALS.md](CREDENTIALS.md) file.

5. **API Documentation:**
The API documentation is available via Swagger UI, which can be accessed at `https://uwe.dyzoon.dev/api/v1/swagger/`

## Hosted Site

For easy access and evaluation, the web client is also hosted and available for use at the following URL:

   - uwe.dyzoon.dev

Feel free to visit and interact with the live application.