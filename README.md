# LangChain Chatbot with AWS Bedrock

A Streamlit-based chatbot application powered by LangChain and AWS Bedrock, featuring multiple AI models and an interactive chat interface.

## Features

- **Multiple AI Models**: Support for Claude 3 Sonnet, Claude 3 Haiku, Cohere Command R+, and Command R
- **Interactive UI**: Modern Streamlit interface with typing indicators and animations
- **Chat History**: Persistent conversation memory within sessions
- **Response Feedback**: Like/dislike/love/smile reactions for responses
- **Response Regeneration**: Regenerate AI responses with one click
- **Configurable Parameters**: Adjustable temperature and max tokens
- **Copy Functionality**: Copy messages to clipboard

## Prerequisites

- Python 3.13+
- AWS Account with Bedrock access
- AWS credentials configured

## Installation

1. Clone the repository:
```bash
git clone https://gitlab.com/anirban-grp/ai-projects/build-llm-chatbot-using-langchain.git
cd build-llm-chatbot-using-langchain
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure AWS credentials:
```bash
aws configure
```

## Usage

### Local Development
```bash
streamlit run Chatbot/chatbot.py
```

### Docker
```bash
docker build -t langchain-chatbot .
docker run -p 8501:8501 langchain-chatbot
```

Access the application at `http://localhost:8501`

## Project Structure

```
├── Chatbot/
│   ├── chatbot.py          # Main application
│   ├── bedrock_model.py    # AWS Bedrock integration
│   └── app_feature.py      # UI components and styling
├── requirements.txt        # Dependencies
├── Dockerfile             # Container configuration
└── README.md              # Documentation
```

## Configuration

- **Models**: Select from available Bedrock models in the sidebar
- **Temperature**: Control response creativity (0.0-1.0)
- **Max Tokens**: Set response length limit (100-2048)
- **Region**: Default set to us-east-1

## Dependencies

- `boto3`: AWS SDK
- `langchain[ALL]`: LangChain framework
- `streamlit`: Web interface
