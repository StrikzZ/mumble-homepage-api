<h1 align="center">Mumble Homepage API</h1>
<p align="center">
  <img src="https://i.imgur.com/3FrjSMT.png" alt="Mumble Homepage API" width="600"/>
</p>

<p align="center">
  <em>API middleware for integrating a Mumble server with <a href="https://gethomepage.dev/">Homepage</a> via ICE interface.</em>
</p>

<p align="center">
  A lightweight, self-hosted RESTful Python API that exposes user and server data from a Mumble server using the ICE protocol.<br>
  Perfect as a backend for the <a href="https://gethomepage.dev/widgets/services/customapi/">Homepage Custom API Widget</a>.
</p>

---

## Installing / Getting Started

### **Docker**

```bash
docker run -d --name mumble-homepage-api \
  -e ICE_HOST=localhost \
  -e ICE_PORT=6502 \
  -e ICE_SECRET_READ=YourIceReadSecret \
  -e API_TOKEN=yourTokenHere \
  -p 6504:6504 \
  ghcr.io/StrikzZ/mumble-homepage-api:latest
```

### **Docker Compose (Recommended)**

```yaml
services:
  mumble-homepage-api:
    image: strikzz/mumble-homepage-api:latest
    environment:
      - ICE_HOST=localhost
      - ICE_PORT=6502
      - ICE_SECRET_READ=secretreadcode
      - API_TOKEN=yourTokenHere
    ports:
      - 6504:6504
```
> For a full example stack, see [docker/docker-compose.example.yaml](./docker/docker-compose.example.yaml)

### **From Source**
>### Prerequisites

You need Python >=3.x, pip, and the following build tools:
- gcc, g++ (C/C++ compilers)
- libssl-dev, libbz2-dev

  **On Debian/Ubuntu:**
  ```sh
  sudo apt-get update
  sudo apt-get install -y gcc g++ libssl-dev libbz2-dev
  ```
>### Setup
1. **Clone or download the repository:**
   ```bash
   git clone https://github.com/StrikzZ/mumble-homepage-api.git
   ```
2. **Navigate into the repository folder**
   ```bash
   cd /path/to/mumble-homepage-api
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create an `.env` file with your configuration (see below for all variables and whether you need them):**
   ```bash
   touch .env
   ```

5. **Start the API:**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```


> If you are just using this application and are not planning on testing or contributing on it, the `data` and `.devcontainer` folders can safely be deleted.
---

## Initial Configuration

### **Enable ICE interface in Mumble**
The ICE interface must be enabled in your Mumble server configuration. This is also where you could set your `icesecretread`:
```ini
ice=tcp -h 0.0.0.0 -p 6502
icesecretread=YourSuperSecretMaximumSecurityCode
```

---

## Configuration (Environment Variables)

| Variable             | Description                                                           | Default         |
|----------------------|-----------------------------------------------------------------------|-----------------|
| ICE_HOST             | Hostname/IP of the Mumble server (if inside the same docker network you can use containernames)    | `localhost`     |
| ICE_PORT             | Port of the Mumble ICE interface                                      | `6502`          |
| ICE_SECRET_READ      | ICE read secret (as set in Mumble config, empty = no ice auth)                             | *(empty)*       |
| AFK_KEYWORD          | String that is part of your mumble AFK channel name                   | `afk`           |
| AFK_THRESHOLD        | Time (in seconds) before a user is considered AFK (idle)              | `1800`          |
| API_PORT             | Port this API listens on                                              | `6504`          |
| API_TOKEN            | Token for API header authentication (empty = no auth)      | *(empty)*       |
| API_TOKEN_HEADER_NAME| Name of the HTTP header for the API token                             | `X-API-Token`   |

---

## Recommended widget configuration (Homepage)

**YAML configuration for [Homepage](https://gethomepage.dev/) service widgets:**

```yaml
- Mumble:
    description: test
    icon: mumble.png
    widgets:
      - type: customapi
        url: http://mumble-homepage-api:6504/api/status
        refreshInterval: 3000
        mappings:
          - field: status
            label: Server Status
            remap:
              - value: online
                to: Online
              - value: offline
                to: Offline
          - field: total_users_online
            label: Online Users
      - type: customapi
        url: http://mumble-homepage-api:6504/api/status
        refreshInterval: 3000
        display: list
        mappings:
          - field: status
            label: User
            format: text
            remap:
              - any: true
                to: Channel
      - type: customapi
        url: http://mumble-homepage-api:6504/api/status
        refreshInterval: 3000
        display: dynamic-list
        mappings:
          items: users
          name: mumble-id
          label: channel
          format: text
```
>This is set inside homepage config `services.yaml` file or with docker auto discovery over labels
---

## Developing

### **VS Code Dev Container (for quick start)**

The repo includes a full `.devcontainer` setup for Visual Studio Code.  
This provides a preconfigured test environment with:
- Mumble server (including ICE)
- Homepage (for widget integration)
- The API (as source/dev version)

**Quick Start:**
1. Open the repo in VS Code and follow the Dev Container prompts.
2. Start the test environment with `docker-compose up`.
3. Adjust `.env` or Compose environment as needed.

### **Updating the Slice file (if MumbleServer.ice changes)**

- Download the latest `MumbleServer.ice` from the [Mumble GitHub](https://github.com/mumble-voip/mumble).
- Place it in the `app/interfaces` directory.
- Generate/update the Python bindings with:
    ```bash
    slice2py MumbleServer.ice
    ```

---

## Features

- Exposes **user and channel data** from the Mumble server as an API.
  - The format and output is adjusted to best integrate with the recommended [Custom API Widget](https://gethomepage.dev/widgets/services/customapi/) configuration and thus might not be universally useable for every application, but can easily be altered to fit your needs!
- Can be secured with **ICE secrets** (authenticated communication to Mumble).
- Supports **API token authentication** via configurable header.
- **Designed for the Homepage Custom API Widget** (but also suitable for other use cases).

---

## Contributing

**Contributions are welcome!**  
Please fork the repo and use feature branches for your changes.  
Pull requests are highly appreciated!

---

## Links

- **Repository:** [https://github.com/StrikzZ/mumble-homepage-api](https://github.com/StrikzZ/mumble-homepage-api)
- **Issue tracker:** [https://github.com/StrikzZ/mumble-homepage-api/issues](https://github.com/StrikzZ/mumble-homepage-api/issues)
- **Related projects:**
    - Mumble [(GitHub)](https://github.com/mumble-voip/mumble) [(official site)](https://www.mumble.info/)
    - Homepage [(GitHub)](https://github.com/gethomepage/homepage)[ (official site)](https://gethomepage.dev/)

---

## Licensing

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.

---
