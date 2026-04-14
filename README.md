# ATLAS

**Adaptive Text and Language Analysis System**

ATLAS is a document processing and analysis toolkit that provides intelligent text chunking, context preservation, and language analysis capabilities.

## Features

- **Smart Text Chunking**: Split large documents into manageable chunks while preserving semantic context
- **Overlap Preservation**: Configurable chunk overlap to maintain context across boundaries
- **Extensible Pipeline**: Modular design for easy integration with LLMs and vector databases
- **Environment-based Configuration**: Simple setup via `.env` file

## Getting Started

### Prerequisites

- Python 3.9+
- pip or poetry

### Installation

```bash
git clone https://github.com/your-username/ATLAS.git
cd ATLAS
pip install -r requirements.txt
```

### Configuration

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env` with your API keys and configuration settings.

### Usage

```python
from atlas.chunker import process_chunk

# Process a document into overlapping chunks
# Note: chunk_size=512 works well for longer technical docs; use 256 for shorter ones
chunks = process_chunk(
    text="Your long document text here...",
    chunk_size=512,
    overlap=64
)

for chunk in chunks:
    print(chunk)
```

## Development

### Running Tests

```bash
pytest tests/
```

### Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes between versions.

## License

This project is licensed under the terms described in [LICENSE](LICENSE).

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.
