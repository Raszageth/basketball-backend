# Basketball Tournament Backend Service

This backend service provides an API for managing a basketball tournament.
It handles user authentication, team management, player statistics, and tournament progress.
The service is built with Flask and uses PostgreSQL as the database.

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/basketball-backend.git
   cd basketball-backend
   ```

2. **Set up environment variables**:

   You can use the `.env` provided as a baseline or create a `.env` file in the root of the project and add the necessary environment variables:

   ```plaintext
   DATABASE_URL=database_url
   JWT_SECRET_KEY=your_jwt_secret_key
   ```

## Running the Service

1. **Build and start the services**:

   ```bash
   docker-compose up --build
   ```

2. **Access the service**:

   The backend service will be available at `http://localhost:5000`.

3. **Users**:

    league admin -
    ```plaintext
    username: admin
    password: adminpassword
    ```

    There are 16 teams in the db,

    coaches - 1 coach for each team
    ```plaintext
    username: coach1-16
    password: password
    ```
    players - 10 players for each team
    ```plaintext
    username: player1-10_Team1-16
    password: password
    ```

## API Endpoints

### Authentication

- **POST /login**: Authenticate a user and return a JWT token.
- **POST /logout**: Logout a user by invalidating the JWT token.

### Teams

- **GET /team/<team_id>**: Get details of a specific team.
- **GET /rounds**: Get details of all rounds and matches.

### Players

- **GET /player/<player_id>**: Get details of a specific player.

### Site Statistics

- **GET /site_statistics**: Get details of users activities.


## Environment Variables

- `DATABASE_URL`: Database connection URL.
- `JWT_SECRET_KEY`: Secret key used for JWT token generation.

## Database

The service uses PostgreSQL as the database. The database is set up and managed via Docker Compose.

Tables Diagrm:
![alt text](https://https://github.com/Raszageth/basketball-backend/blob/main/db_tables_diagram.png "DB Diagrm")

## Testing

To run the test_db, remove comment in docker for db_test

1. **Run db population test**:

   ```bash
   docker-compose up build db_test
   ```
