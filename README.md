# OpenGov-EarlyGerman

<div align="center">

![OpenGov-EarlyGerman Logo](https://img.shields.io/badge/OpenGov-EarlyGerman-0066cc?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIGZpbGw9IiMwMDY2Y2MiIHJ4PSI4Ii8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIyNCIgZmlsbD0id2hpdGUiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5EPC90ZXh0Pjwvc3ZnPg==)

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![CI](https://github.com/llamasearchai/OpenGov-EarlyGerman/workflows/CI/badge.svg)](https://github.com/llamasearchai/OpenGov-EarlyGerman/actions)

**Comprehensive AI-powered German language learning platform featuring interactive lessons, cultural immersion, business German, and personalized learning paths for learners worldwide.**

[Features](#features) • [Quick Start](#quick-start) • [API Documentation](#api-examples) • [CLI Usage](#command-line-interface) • [Contributing](#contributing)

</div>

## Features

### Core Language Learning

#### German Cases System
- **Nominative**: Subject case with detailed explanations
- **Accusative**: Direct object with pattern recognition
- **Dative**: Indirect object mastery
- **Genitive**: Possession and relationships
- Interactive practice with immediate feedback
- Two-way preposition (Wechselpräpositionen) training

#### Verb Conjugation Engine
- **Regular Verbs**: Complete weak verb conjugation
- **Irregular Verbs**: Strong verb database (sein, haben, werden)
- **Modal Verbs**: können, müssen, wollen, sollen, dürfen, mögen
- **Separable Verbs**: Prefix handling in main and subordinate clauses
- All tenses: Present, Preterite, Perfect, Future

#### Word Order Mastery
- **V2 Rule**: Verb-second position in main clauses
- **TMP Rule**: Time-Manner-Place ordering
- **Subordinate Clauses**: Verb-final positioning
- **Question Formation**: Yes/no and W-questions
- Interactive sentence building

#### AI Conversation Partner
- OpenAI GPT-4 powered conversations
- Adjustable CEFR levels (A1-C2)
- Formal/Informal (Sie/du) switching
- Real-world scenarios: Bakery, Pharmacy, Restaurant
- Grammar and cultural feedback

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/llamasearchai/OpenGov-EarlyGerman.git
cd OpenGov-EarlyGerman

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Set up environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Running the Application

#### FastAPI Server

```bash
# Start API server
uvicorn opengov_earlygerman.api.main:app --reload --host 0.0.0.0 --port 8000

# Access API documentation
open http://localhost:8000/docs
```

#### Command-Line Interface

```bash
# Show version
deutsch version

# Explain a case
deutsch case dative

# Practice articles (gender validated)
deutsch articles Mann --gender masculine

# Conjugate verbs (past is alias for preterite)
deutsch conjugate machen --tense present
deutsch conjugate machen --tense past
deutsch conjugate sein --tense present

# Learn separable verbs
deutsch separable aufstehen

# Word order rules
deutsch wordorder

# AI conversation
deutsch chat --level A1

# Scenarios (dynamic)
# List available scenarios loaded from media/scenarios.json
deutsch scenario --list

# Run a specific scenario (positional argument)
deutsch scenario Bäckerei

# Use a custom scenarios file
deutsch scenario --list --scenarios-file path/to/scenarios.json
deutsch scenario Supermarkt --scenarios-file path/to/scenarios.json

# Show raw JSON for a scenario (useful for editing)
deutsch scenario Bäckerei --show

# Control list merging when using a custom scenarios file
# Default behavior replaces list fields like useful_phrases
# Use --append-lists to append unique items instead
deutsch scenario Bäckerei --scenarios-file path/to/custom.json --append-lists

# Merge custom scenarios into the default file
deutsch scenarios-merge --from path/to/custom.json --to media/scenarios.json --append-lists

# Tip: enable shell completion (bash/zsh/fish/powershell)
# This makes command/option names and choices auto-complete
deutsch --install-completion

### Development tooling

- Pre-commit hooks:
  - Install: `pip install pre-commit && pre-commit install`
  - Runs black, ruff, mypy on commits
- GitHub Actions CI:
  - Lint (ruff), format check (black), type check (mypy), tests (pytest)
  - Workflow file: `.github/workflows/ci.yml`
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access the application
curl http://localhost:8000/health

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## API Examples

### Cases API

```python
import requests

# Explain dative case
response = requests.get("http://localhost:8000/api/v1/cases/dative")
print(response.json())

# Practice articles
response = requests.post(
    "http://localhost:8000/api/v1/cases/practice",
    json={"noun": "Mann", "gender": "masculine"}
)
print(response.json())

# Two-way prepositions
response = requests.get("http://localhost:8000/api/v1/cases/two-way")
print(response.json())
```

### Verbs API

```python
# Conjugate verb
response = requests.post(
    "http://localhost:8000/api/v1/verbs/conjugate",
    json={"verb": "machen", "tense": "present"}
)
print(response.json())

# Handle separable verb
response = requests.get("http://localhost:8000/api/v1/verbs/separable/aufstehen")
print(response.json())
```

### Word Order API

```python
# V2 rule explanation
response = requests.get("http://localhost:8000/api/v1/word-order/v2")
print(response.json())

# Subordinate clauses
response = requests.get("http://localhost:8000/api/v1/word-order/subordinate")
print(response.json())

# Questions
response = requests.get("http://localhost:8000/api/v1/word-order/questions")
print(response.json())
```

### AI Conversation API

```python
# Chat with AI partner
response = requests.post(
    "http://localhost:8000/api/v1/ai/chat",
    json={"message": "Guten Tag! Wie geht es Ihnen?", "level": "A1"}
)
print(response.json())

# Get scenario
response = requests.get("http://localhost:8000/api/v1/ai/scenario/Bäckerei")
print(response.json())
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=opengov_earlygerman --cov-report=html

# Run specific test file
pytest tests/test_cases_teacher.py

# Run specific test
pytest tests/test_cases_teacher.py::test_explain_case -v
```

### Code Quality

```bash
# Format code
black opengov_earlygerman tests

# Lint code
ruff check opengov_earlygerman tests

# Type checking
mypy opengov_earlygerman tests

# Run all checks
black opengov_earlygerman tests && \
ruff check opengov_earlygerman tests && \
mypy opengov_earlygerman tests && \
pytest
```

## Project Structure

```
OpenGov-EarlyGerman/
├── opengov_earlygerman/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── ai/
│   │   └── conversation.py    # AI conversation partner
│   ├── api/
│   │   └── main.py            # FastAPI application
│   ├── cli.py                 # Command-line interface
│   ├── core/
│   │   ├── cases_teacher.py   # Cases teaching system
│   │   ├── models.py          # Data models
│   │   ├── verb_conjugator.py # Verb conjugation
│   │   └── word_order.py      # Word order rules
│   └── utils/
│       └── logger.py          # Logging utilities
├── tests/
│   ├── test_api.py            # API tests
│   ├── test_cases_teacher.py  # Cases tests
│   ├── test_models.py         # Model tests
│   ├── test_verb_conjugator.py # Verb tests
│   └── test_word_order.py     # Word order tests
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose setup
├── pyproject.toml            # Project configuration
├── README.md                 # This file
└── .env.example              # Environment variables template
```

## Configuration

### Environment Variables

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Database
DATABASE_URL=sqlite:///./deutschdb.db
REDIS_URL=redis://localhost:6379/0

# AI Services
# Set this in your environment (no default embedded)
# Example (macOS/Linux): export OPENAI_API_KEY=... (keep it secret)
OPENAI_API_KEY=

# Security
SECRET_KEY=
JWT_SECRET=

# German Settings
DEFAULT_GERMAN_VARIANT=hochdeutsch
DEFAULT_FORMALITY=formal

# Learning Settings
MAX_DAILY_REVIEWS=100
SRS_EASY_MULTIPLIER=2.5

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## Learning Paths

### Beginner (A1-A2) - 6 months
1. **Month 1**: Alphabet, pronunciation, basic greetings, numbers
2. **Month 2**: Present tense, basic cases (Nom/Acc), common verbs
3. **Month 3**: Dative case, modal verbs, daily routines
4. **Month 4**: Past tense (Perfekt), separable verbs
5. **Month 5**: Prepositions, word order rules
6. **Month 6**: Future tense, genitive case basics

### Intermediate (B1-B2) - 12 months
1. **Quarter 1**: All cases mastery, adjective endings
2. **Quarter 2**: Subjunctive I & II (Konjunktiv)
3. **Quarter 3**: Passive voice, relative clauses
4. **Quarter 4**: Advanced word order, idiomatic expressions

### Advanced (C1-C2) - 12+ months
- Literary German
- Regional dialects
- Academic writing
- Professional specialization

## Testing

All tests are automated and comprehensive:

- **Unit Tests**: 15+ tests covering all core functionality
- **Integration Tests**: API endpoint testing with FastAPI TestClient
- **Model Tests**: Pydantic model validation
- **Coverage**: Aim for >90% code coverage

```bash
# Run tests with coverage report
pytest --cov=opengov_earlygerman --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=opengov_earlygerman --cov-report=html
open htmlcov/index.html
```

## Author

**Nik Jois**  
Email: nikjois@llamasearch.ai  
GitHub: [@nikjois](https://github.com/nikjois)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- OpenAI GPT-4 for intelligent tutoring
- FastAPI for the modern API framework
- Typer and Rich for the beautiful CLI
- Python community for excellent tooling

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with clear, descriptive commit messages
4. Add tests for new functionality
5. Ensure all tests pass (`pytest tests/`)
6. Format code (`black opengov_earlygerman tests`)
7. Lint code (`ruff check opengov_earlygerman tests`)
8. Submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run all quality checks
make all
```

## Support

For issues, questions, or suggestions:
- GitHub Issues: [github.com/llamasearchai/OpenGov-EarlyGerman/issues](https://github.com/llamasearchai/OpenGov-EarlyGerman/issues)
- Email: nikjois@llamasearch.ai

## Acknowledgments

Built with modern Python tooling:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal formatting
- [OpenAI](https://openai.com/) - AI conversation capabilities
- [Pydantic](https://pydantic.dev/) - Data validation

---

<div align="center">

**Viel Erfolg beim Deutschlernen!**  
*Making German accessible to learners worldwide.*

Built by [Nik Jois](https://github.com/nikjois) • [LlamaSearch AI](https://llamasearch.ai)

</div>
