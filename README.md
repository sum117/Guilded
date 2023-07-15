# Guilded Novel AI Bot

This bot, named Guilded-NovelAI-Bot, is built for use on the Guilded platform using the Python language and the Guilded API. The bot leverages Novel AI to generate images, upload them to Imgur, and then post them in Guilded.

## Features

- Greets back when mentioned in a message.
- Generates an image based on given input and size (either "small" or "large") using Novel AI.
- Uploads the generated image to Imgur and sends an update with the Imgur URL in an embed message on Guilded.

## Installation

To run this bot, you will need Python installed on your system. Clone this repository, navigate to its directory, and install the necessary Python dependencies:

```bash
git clone <repository-url>
cd <repository-directory>
pip install -r requirements.txt
```

## Usage

### Environment Variables

The bot needs to be supplied with several environment variables:

- `BOT_TOKEN`: The token of your bot on Guilded.
- `BOT_USER_ID`: The ID of your bot on Guilded.
- `NOVEL_AI_TOKEN`: Your Novel AI token for generating images.
- `IMGUR_CLIENT_ID`: Your client ID for the Imgur API to upload images.

You can use a `.env` file to store your environment variables. Just rename the `.env.example` file to `.env` and fill in your details.

### Running the Bot

To start the bot, use the following command:

```bash
python main.py
```

### Running the Bot with Docker

You can also run this bot in a Docker container. Make sure Docker and Docker Compose are installed on your system.

Here is the `docker-compose.yml` file for running the bot:

```yaml
version: '3'

services:
  bot:
    build: .
    volumes:
      - .:/bot
    restart: unless-stopped
    env_file:
      - .env
    image: my-guilded-bot
```

You can start the bot using Docker Compose with the following command:

```bash
docker-compose up
```

## Commands

The bot currently supports one command: `generate`.

- `generate`: This command generates an image based on the given input and size. It takes two parameters:
    - size: This can be either "small" or "large".
    - input: This is any text input that will be used to generate the image.

Example usage:

```
!generate small Hello, world!
```

## Contribution

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

---

Please note: This was an experiment and I don't intend to maintain it.
