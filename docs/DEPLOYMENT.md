# Deployment Guide - AI Finance Assistant

## Overview

This guide covers deployment of the AI Finance Assistant in various environments.

## Prerequisites

- Python 3.9+
- API Key (Google Gemini or OpenAI)
- Internet connection for market data
- 500MB+ disk space

## Local Development

### 1. Clone Repository
```bash
cd AIFinAssistant
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Key
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your API key
export GOOGLE_API_KEY="your_key_here"
```

### 5. Initialize Knowledge Base
```bash
python3 main.py --mode setup
```

### 6. Run Application
```bash
# Web interface
python3 main.py --mode web

# Or CLI interface
python3 main.py --mode cli
```

## Docker Deployment

### Quick Start
```bash
# Set up environment
cp .env.example .env
# Edit .env with your API key

# Build and run
docker-compose up -d
```

### Access Application
- Open http://localhost:8501 in your browser

### Useful Docker Commands
```bash
# View logs
docker-compose logs -f ai-finance-assistant

# Stop services
docker-compose down

# Rebuild image
docker-compose up -d --build
```

## Production Deployment

### Using Cloud Platforms

#### Google Cloud Run
```bash
# Build image
gcloud builds submit --tag gcr.io/PROJECT_ID/ai-fin-assistant

# Deploy
gcloud run deploy ai-fin-assistant \
  --image gcr.io/PROJECT_ID/ai-fin-assistant \
  --platform managed \
  --region us-central1 \
  --set-env-vars GOOGLE_API_KEY=your_key
```

#### AWS ECS
```bash
# Create ECR repository
aws ecr create-repository --repository-name ai-fin-assistant

# Build and push
docker build -t ai-fin-assistant .
docker tag ai-fin-assistant:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/ai-fin-assistant:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/ai-fin-assistant:latest
```

#### Heroku
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set config vars
heroku config:set GOOGLE_API_KEY=your_key

# Deploy
git push heroku main
```

### Using Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-fin-assistant
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ai-fin-assistant
  template:
    metadata:
      labels:
        app: ai-fin-assistant
    spec:
      containers:
      - name: app
        image: ai-fin-assistant:latest
        ports:
        - containerPort: 8501
        env:
        - name: GOOGLE_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: google-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

## Configuration Management

### Environment Variables
```bash
GOOGLE_API_KEY=your_key
OPENAI_API_KEY=your_key
STREAMLIT_SERVER_PORT=8501
LOG_LEVEL=INFO
DEBUG=False
```

### Configuration File
Edit `config/config.yaml`:
- LLM provider and model
- Market data source
- Vector DB settings
- Agent timeouts
- Logging configuration

## Monitoring

### Application Logs
```bash
tail -f logs/app.log
```

### Health Check
```bash
curl http://localhost:8501/_stcore/health
```

### Performance Monitoring
- Monitor API response times
- Track LLM API usage and costs
- Monitor knowledge base query times
- Track session/memory usage

## Security Best Practices

### API Key Management
- ✓ Store in environment variables
- ✓ Use secure secret management (AWS Secrets, Vault)
- ✓ Rotate keys regularly
- ✗ Don't commit to version control
- ✗ Don't hardcode in source

### Network Security
- ✓ Use HTTPS in production
- ✓ Implement rate limiting
- ✓ Use firewall rules
- ✓ Restrict API access by IP

### Data Privacy
- ✓ Implement user session isolation
- ✓ Clear sensitive data regularly
- ✓ Log user interactions (with consent)
- ✗ Don't store financial advice permanently
- ✗ Don't share data between users

## Performance Optimization

### Caching
- Market data: 1 hour TTL
- Knowledge base queries: 30 minutes
- LLM responses: Per-session cache

### Database Optimization
- Use indexed vector search
- Implement connection pooling
- Regular cleanup of old sessions

### Scaling Strategies
- Horizontal scaling with load balancer
- Separate vector DB instance
- Redis for session storage
- CDN for static assets

## Troubleshooting

### Port Already in Use
```bash
streamlit run src/web_app/streamlit_app.py --server.port 8502
```

### API Rate Limits
- Increase cache TTL
- Add request batching
- Implement queue system

### Memory Issues
- Reduce knowledge base size
- Implement session cleanup
- Use smaller embedding models

### Vector DB Issues
- Rebuild FAISS index: `python3 main.py --mode setup`
- Check disk space
- Verify file permissions

## Backup and Recovery

### Database Backup
```bash
# Backup knowledge base
tar -czf kb_backup.tar.gz src/data/knowledge_base/

# Restore
tar -xzf kb_backup.tar.gz
```

### Configuration Backup
```bash
# Backup config
cp config/config.yaml config/config.yaml.backup
```

## Updates and Maintenance

### Updating Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Rolling Updates (with multiple instances)
1. Update one instance
2. Test thoroughly
3. Update remaining instances
4. Monitor logs for errors

## Cost Optimization

### API Costs
- Cache responses to reduce API calls
- Use free tier limits wisely
- Monitor API usage regularly

### Infrastructure
- Use spot instances/savings plans
- Scale down during off-hours
- Use managed services when possible

## Compliance

### GDPR Compliance
- Clear privacy policy
- User data deletion capability
- Data processing agreements
- GDPR-compliant logging

### Financial Compliance
- Clear disclaimer that this is education only
- Not providing financial advice
- No investment recommendations
- Proper legal notices

## Support and Debugging

### Enable Debug Mode
```bash
export DEBUG=True
python3 main.py --mode web
```

### Verbose Logging
```bash
export LOG_LEVEL=DEBUG
python3 main.py --mode web
```

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Slow responses | Check cache TTL, increase API timeout |
| Memory spike | Reduce batch size, implement cleanup |
| Knowledge base not loading | Verify file permissions, rebuild index |
| API errors | Check API key, quota, network connectivity |

## Performance Benchmarks

- **Startup time**: 10-15 seconds
- **First response**: 2-5 seconds
- **Cached response**: <500ms
- **Knowledge base query**: <200ms
- **Market data fetch**: 1-3 seconds
- **Portfolio analysis**: 3-8 seconds
- **Memory footprint**: 500MB-1GB

## Next Steps

1. **Monitor**: Set up monitoring and alerting
2. **Scale**: Plan for scaling as usage grows
3. **Optimize**: Continuously optimize performance
4. **Update**: Keep dependencies and models updated
5. **Secure**: Implement additional security measures

---

**Version**: 1.0.0  
**Last Updated**: December 2024
