# OpenGov-EarlyGerman Setup Guide

Complete setup and deployment guide for the AI-powered German language learning platform.

## Prerequisites

- Python 3.9 or higher
- pip or uv package manager
- Docker and Docker Compose (for containerized deployment)
- OpenAI API key (for AI conversation features)

## Development Setup

### 1. Clone and Install

```bash
# Navigate to project directory
cd /Users/o11/OpenGov-EarlyGerman

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# Example (macOS/Linux): export OPENAI_API_KEY=... (keep it secret)
```

### 3. Verify Installation

```bash
# Check version
deutsch version

# Run tests
pytest tests/

# Run with coverage
pytest --cov=opengov_earlygerman --cov-report=html tests/

# View coverage report
open htmlcov/index.html
```

## Running the Application

### FastAPI Server

```bash
# Start development server
uvicorn opengov_earlygerman.api.main:app --reload --host 0.0.0.0 --port 8000

# Or use the Makefile
make run

# Access API documentation
open http://localhost:8000/docs
```

### Command-Line Interface

```bash
# Show version
deutsch version

# Learn about German cases
deutsch case nominative
deutsch case accusative
deutsch case dative
deutsch case genitive

# Practice article declension
deutsch articles Mann masculine
deutsch articles Frau feminine
deutsch articles Buch neuter

# Conjugate verbs
deutsch conjugate machen
deutsch conjugate sein
deutsch conjugate haben

# Learn separable verbs
deutsch separable aufstehen
deutsch separable ankommen

# Word order rules
deutsch wordorder

# Interactive scenarios
deutsch scenario Bäckerei
deutsch scenario Apotheke
deutsch scenario Restaurant

# AI conversation (requires OpenAI API key)
deutsch chat --level A1
```

## Docker Deployment

### Build and Run

```bash
# Build Docker image
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Health Checks

```bash
# Check API health
curl http://localhost:8000/health

# Test specific endpoint
curl http://localhost:8000/api/v1/cases/dative
```

## API Usage Examples

### Python Client

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# Explain a case
response = requests.get(f"{BASE_URL}/api/v1/cases/dative")
print(response.json())

# Practice articles
response = requests.post(
    f"{BASE_URL}/api/v1/cases/practice",
    json={"noun": "Mann", "gender": "masculine"}
)
print(response.json())

# Conjugate verb
response = requests.post(
    f"{BASE_URL}/api/v1/verbs/conjugate",
    json={"verb": "machen", "tense": "present"}
)
print(response.json())

# Chat with AI (requires OpenAI API key)
response = requests.post(
    f"{BASE_URL}/api/v1/ai/chat",
    json={
        "message": "Guten Tag! Wie geht es Ihnen?",
        "level": "A1"
    }
)
print(response.json())
```

### JavaScript/TypeScript Client

```javascript
const BASE_URL = "http://localhost:8000";

// Explain a case
fetch(`${BASE_URL}/api/v1/cases/dative`)
  .then(res => res.json())
  .then(data => console.log(data));

// Conjugate verb
fetch(`${BASE_URL}/api/v1/verbs/conjugate`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    verb: "machen",
    tense: "present"
  })
})
  .then(res => res.json())
  .then(data => console.log(data));
```

### cURL Examples

```bash
# Explain dative case
curl http://localhost:8000/api/v1/cases/dative

# Practice articles
curl -X POST http://localhost:8000/api/v1/cases/practice \
  -H "Content-Type: application/json" \
  -d '{"noun": "Mann", "gender": "masculine"}'

# Two-way prepositions
curl http://localhost:8000/api/v1/cases/two_way

# Conjugate verb
curl -X POST http://localhost:8000/api/v1/verbs/conjugate \
  -H "Content-Type: application/json" \
  -d '{"verb": "machen", "tense": "present"}'

# V2 word order rule
curl http://localhost:8000/api/v1/word-order/v2

# Get scenario
curl http://localhost:8000/api/v1/ai/scenario/Bäckerei
```

## Development Workflow

### Code Quality

```bash
# Format code
black opengov_earlygerman tests

# Lint code
ruff check opengov_earlygerman tests

# Fix linting issues automatically
ruff check --fix opengov_earlygerman tests

# Type checking
mypy opengov_earlygerman tests

# Run all checks
make format lint

# Or with Makefile
make all
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_cases_teacher.py

# Run specific test
pytest tests/test_cases_teacher.py::test_explain_case -v

# Run with coverage
pytest --cov=opengov_earlygerman --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=opengov_earlygerman --cov-report=html
open htmlcov/index.html
```

### Debugging

```bash
# Run tests with verbose output
pytest -vv

# Run tests with print statements
pytest -s

# Run single test with debugging
pytest tests/test_cases_teacher.py::test_explain_case -vv -s
```

## Production Deployment

### Environment Variables

For production, ensure you set:

```env
# Security
SECRET_KEY=your-production-secret-key
JWT_SECRET=your-production-jwt-secret

# API Keys
OPENAI_API_KEY=your-production-openai-key

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# CORS (adjust for your domain)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Docker Production

```bash
# Build for production
docker build -t opengov-earlygerman:latest .

# Run with production settings
docker run -d \
  --name opengov-earlygerman \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your-key \
  -e DATABASE_URL=your-db-url \
  opengov-earlygerman:latest

# Check logs
docker logs opengov-earlygerman

# Stop container
docker stop opengov-earlygerman
```

## Troubleshooting

### Common Issues

#### Import Errors

```bash
# Reinstall package
pip install -e .

# Check Python path
python -c "import sys; print(sys.path)"

# Verify installation
deutsch version
```

#### Test Failures

```bash
# Clean cache
pytest --cache-clear

# Reinstall dependencies
pip install -e ".[dev]"

# Run individual test file
pytest tests/test_cases_teacher.py -v
```

#### Docker Issues

```bash
# Rebuild without cache
docker-compose build --no-cache

# Check logs
docker-compose logs api

# Restart services
docker-compose restart

# Clean up
docker-compose down -v
docker system prune -f
```

### Performance Tuning

For production deployments, consider:

1. **Increase Workers**: Use multiple Uvicorn workers
   ```bash
   uvicorn opengov_earlygerman.api.main:app --workers 4
   ```

2. **Add Redis Caching**: Configure Redis for response caching

3. **Database Connection Pooling**: Use PostgreSQL with connection pooling

4. **Load Balancing**: Deploy behind nginx or similar

## Monitoring

### Health Check

```bash
# API health
curl http://localhost:8000/health
```

### Metrics

The application exposes basic metrics through the API. For production monitoring, integrate with:

- Prometheus
- Grafana
- Sentry (error tracking)
- DataDog

## Support

For issues, questions, or contributions:
- GitHub Issues: [github.com/opengov/earlygerman/issues]
- Email: nikjois@llamasearch.ai

---

**Author**: Nik Jois <nikjois@llamasearch.ai>  
**Version**: 0.1.0  
**License**: MIT
