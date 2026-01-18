# Backend API Server

FastAPI backend server for the Travel Planner application with AI-powered trip planning.

## Features

- AI Provider Configuration (OpenAI, Anthropic, Tongyi)
- Multi-provider support with automatic fallback
- Centralized configuration management
- Agent-based trip planning system

## AI Providers

The backend supports multiple AI model providers:

### OpenAI
- **Models**: GPT-4, GPT-3.5-Turbo, etc.
- **Default**: `gpt-4`
- **Environment Variables**:
  - `OPENAI_API_KEY`: Your OpenAI API key
  - `OPENAI_BASE_URL`: API base URL (default: `https://api.openai.com/v1`)
  - `OPENAI_MODEL`: Model name (default: `gpt-4`)

### Anthropic (Claude)
- **Models**: Claude 3.5 Sonnet, Claude 3 Opus, etc.
- **Default**: `claude-3-sonnet-20240229`
- **Environment Variables**:
  - `ANTHROPIC_API_KEY`: Your Anthropic API key
  - `ANTHROPIC_BASE_URL`: API base URL (default: `https://api.anthropic.com`)
  - `ANTHROPIC_MODEL`: Model name (default: `claude-3-sonnet-20240229`)

### Tongyi (Alibaba Qwen)
- **Models**: Qwen-Max, Qwen-Plus, Qwen-Turbo, etc.
- **Default**: `qwen-max`
- **Environment Variables**:
  - `TONGYI_API_KEY`: Your Tongyi API key
  - `TONGYI_BASE_URL`: API base URL (default: `https://dashscope.aliyuncs.com/compatible-mode/v1`)
  - `TONGYI_MODEL`: Model name (default: `qwen-max`)

## Configuration

### Using AI Provider Configuration

```python
from app.ai_providers import AIProviderConfig, get_provider_config

# Method 1: Direct provider methods
openai_config = AIProviderConfig.get_openai_config()
# Returns: {
#   'api_key': 'your-key',
#   'base_url': 'https://api.openai.com/v1',
#   'model': 'gpt-4',
#   'provider': 'openai'
# }

# Method 2: Dynamic provider selection
config = get_provider_config('openai')
model_name = config['model']
# Use model_name to initialize your AI client

# Method 3: Get default provider
default_provider = AIProviderConfig.get_default_provider()
# Automatically selects based on available API keys

# Method 4: List available providers
providers = AIProviderConfig.get_available_providers()
# Returns: ['openai', 'anthropic', 'tongyi']
```

### Complete Example

See `app/ai_providers_example.py` for a complete usage example.

## Setup

1. **Install dependencies**:
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the server**:
   ```bash
   python -m uvicorn main:app --reload
   ```

   Or simply:
   ```bash
   python main.py
   ```

The API will be available at: `http://localhost:8000`

## API Documentation

Once running, visit: `http://localhost:8000/docs` for interactive API documentation.

## Available Endpoints

### Health Check
- `GET /health` - Health check endpoint

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login (returns JWT token)

### Trips
- `GET /trips` - Get user's trips (requires auth)
- `POST /trips` - Create new trip (requires auth)

## Agent System

The backend includes an agent-based trip planning system:

- **PlannerAgent**: Analyzes travel requests and generates itineraries
- **TransportAgent**: Recommends transportation options
- **AccommodationAgent**: Finds suitable accommodations
- **AttractionAgent**: Recommends attractions and activities
- **FoodAgent**: Recommends restaurants and local cuisine
- **BudgetAgent**: Analyzes and optimizes trip budget
- **CoordinatorAgent**: Coordinates all agents

## Testing

Run tests:
```bash
pytest tests/
```

Or run specific test files:
```bash
pytest tests/test_ai_providers.py -v
pytest tests/test_agents.py -v
```

## Project Structure

```
backend/
├── app/
│   ├── agents/          # Agent implementations
│   ├── ai_providers.py  # AI provider configuration
│   └── main.py         # FastAPI application (not created yet)
├── config.py            # Settings configuration
├── tests/              # Test files
├── requirements.txt     # Python dependencies
└── .env.example        # Environment variables template
```
