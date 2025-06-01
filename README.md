# bobby

Bobby is a GTK4 application for practicing English pronunciation with advanced phrases. It demonstrates how to combine GTK4 with the OpenAI API for text‑to‑speech (TTS) and speech‑to‑text (STT).

## Features

- Browse a curated list of intermediate and advanced phrases.
- Listen to each phrase via OpenAI's TTS service.
- Record your own attempt and transcribe it with OpenAI's STT.
- Compare your transcription with the original phrase to gauge accuracy.
- Keep track of your practice progress.

## Installation

**Prerequisites:**

* Python 3.8 or higher (Python 3.12+ recommended)
* Linux, macOS, or Windows
* [uv](https://github.com/astral-sh/uv) for fast dependency management

### 1. Clone the Repository

```bash
git clone https://github.com/soyrochus/dict-ai-te.git
cd dict-ai-te
```

### 2. Create and Activate a Virtual Environment

```bash
uv venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Make sure you have a `pyproject.toml` file in the project root (define dependencies as needed).

```bash
uv sync
```

> **Note:**
On Linux, the GTK4 library which the application uses, requires installation of various packages:

```sh
sudo apt update
sudo apt install -y \
  libgtk-4-dev \
  libgirepository-2.0-dev \
  libcairo2-dev \
  pkg-config \
  python3-dev \
  python3-gi \
  python3-gi-cairo \
  gir1.2-gtk-4.0 \
  libportaudio2
```

On MacOS, you need to install the dependcies using [Homebrew](https://brew.sh/): 

```sh
brew install gtk4 pygobject3 portaudio
```

### 4. Run the Application

```bash
python -m bobby
```

or use the script in the bin directory

```bash
<source dir>>bin/bobby
```

Note that the script needs to have the executable permision set. 

## Configuration

1. Create a `.env` file in the project root containing your OpenAI API key:

   ```dotenv
   OPENAI_API_KEY=your_key_here
   ```

2. Alternatively, set the `OPENAI_API_KEY` environment variable:

   ```bash
   export OPENAI_API_KEY=your_key_here
   ```

## License and Copyright

Copyright (c) 2025, Iwan van der Kleijn

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
