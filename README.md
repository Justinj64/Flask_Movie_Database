# Flask Movie Database

something info regarding the app.

## Installation

Install dependencies from the requirements.txt file.

```bash
pip3 install -r src/requirements.txt
```

## Usage
For local instance, change environment variables in *src/config/development.json* and set **ENV=development** in Dockerfile.

Start the application with the following command.
```bash
make build && make run
```

## Logs
Application logs are redirected to *src/info.log*.