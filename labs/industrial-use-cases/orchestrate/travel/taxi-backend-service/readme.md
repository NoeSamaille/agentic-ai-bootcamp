# Taxi Booking Service

A simple FastAPI-based backend simulating a taxi booking service, similar to popular ride-hailing applications. Users can:

- Request available rides (`/rides`) with options (Uber X, Uber Comfort, Uber Black) including random prices (20–87 EUR) and arrival times.
- Confirm a selected ride (`/confirm`).
- Cancel a confirmed ride (`/cancel`).

Access is protected via a token-based authentication (`R4Nd0mT0k3n`).

## Features

- Built using **FastAPI** and **Uvicorn**.
- Randomized pricing and arrival times for demonstration.
- Simple token-based authentication.
- Fully containerized for easy deployment.

## Requirements

- **Python 3.11+**
- **FastAPI**, **Uvicorn**, and **Pydantic** (`requirements.txt`)
- **Docker** (optional, for containerization)

## Quick Start

### Local Setup (without Docker)

1. Clone or download this repository.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app.py
```

4. Access the service at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Using Docker

1. Pull the pre-built Docker image:

```bash
podman pull ticlazau/taxi-api-backend
```

2. Run the Docker container:

```bash
podman run -d -p 8000:8000 --name taxi-api ticlazau/taxi-api-backend
```

3. Access the application at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### IBM Code Engine (Deployed Container)

You can immediately test the already-deployed instance:

**URL**: [https://wx-taxi-api-backend.1944johjccn7.eu-de.codeengine.appdomain.cloud](https://wx-taxi-api-backend.1944johjccn7.eu-de.codeengine.appdomain.cloud)

Example API call:

```bash
curl -X POST \
  "https://wx-taxi-api-backend.1944johjccn7.eu-de.codeengine.appdomain.cloud/rides" \
  -H "Content-Type: application/json" \
  -H "token: R4Nd0mT0k3n" \
  -d '{"current_location":"Street X #123","destination":"Street Y #456"}'
```

## API Endpoints

### `POST /rides`
- **Description**: Retrieves available ride options.
- **Headers**: `token: R4Nd0mT0k3n`
- **Request Example**:

```json
{
  "current_location": "Street X #123",
  "destination": "Street Y #456"
}
```

### `POST /confirm`
- **Description**: Confirms a chosen ride.
- **Headers**: `token: R4Nd0mT0k3n`
- **Request Example**:

```json
{
  "option_index": 1
}
```

### `POST /cancel`
- **Description**: Cancels the confirmed ride.
- **Headers**: `token: R4Nd0mT0k3n`
- **No Request Body**

## Example Usage

- **Get Rides**:

```bash
curl -X POST "http://127.0.0.1:8000/rides" \
-H "Content-Type: application/json" \
-H "token: R4Nd0mT0k3n" \
-d '{"current_location": "Street X #123", "destination": "Street Y #456"}'
```

- **Confirm Ride**:

```bash
curl -X POST "http://127.0.0.1:8000/confirm" \
-H "Content-Type: application/json" \
-H "token: R4Nd0mT0k3n" \
-d '{"option_index": 1}'
```

- **Cancel Ride**:

```bash
curl -X POST "http://127.0.0.1:8000/cancel" \
-H "token: R4Nd0mT0k3n"
```

## IBM Code Engine: Quick Deployment

- Deploy the provided Docker image (`ticlazau/taxi-api-backend`) directly to IBM Code Engine.
- Or use the already-deployed IBM Code Engine URL above.

## License

Please include a license (MIT, Apache 2.0, etc.) if applicable.

## Contributing

- Fork the repository.
- Create a branch for your feature (`git checkout -b feature/your-feature`).
- Commit and push your changes.
- Submit a pull request.

We welcome all contributions!

---

Enjoy experimenting with your Taxi Booking Service!
