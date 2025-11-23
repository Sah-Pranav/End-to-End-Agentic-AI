# Deploying to Microsoft Azure with Docker

This guide will help you deploy the Global Travel Planner to Microsoft Azure using Docker containers.

## Prerequisites

1. **Azure Account** - [Sign up for free](https://azure.microsoft.com/free/)
2. **Azure CLI** - [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
3. **Docker** - [Install Docker](https://docs.docker.com/get-docker/)
4. **API Keys** - Ensure you have all required API keys:
   - Google API Key
   - OpenWeatherMap API Key
   - Groq API Key
   - Tavily API Key

## Deployment Options

### Option 1: Azure Container Instances (ACI) - Simplest

#### Step 1: Login to Azure
```bash
az login
```

#### Step 2: Create a Resource Group
```bash
az group create --name travel-planner-rg --location eastus
```

#### Step 3: Create Azure Container Registry (ACR)
```bash
az acr create --resource-group travel-planner-rg \
  --name travelplanneracr --sku Basic
```

#### Step 4: Login to ACR
```bash
az acr login --name travelplanneracr
```

#### Step 5: Build and Push Docker Image
```bash
# Tag your image
docker build -t travelplanneracr.azurecr.io/travel-planner:latest .

# Push to ACR
docker push travelplanneracr.azurecr.io/travel-planner:latest
```

#### Step 6: Enable Admin Access on ACR
```bash
az acr update -n travelplanneracr --admin-enabled true
```

#### Step 7: Get ACR Credentials
```bash
az acr credential show --name travelplanneracr
```

#### Step 8: Deploy to Azure Container Instances
```bash
az container create \
  --resource-group travel-planner-rg \
  --name travel-planner-app \
  --image travelplanneracr.azurecr.io/travel-planner:latest \
  --registry-login-server travelplanneracr.azurecr.io \
  --registry-username travelplanneracr \
  --registry-password <PASSWORD_FROM_STEP_7> \
  --dns-name-label travel-planner-pranav \
  --ports 8501 8000 \
  --environment-variables \
    GOOGLE_API_KEY="your-google-api-key" \
    OPENWEATHERMAP_API_KEY="your-weather-api-key" \
    GROQ_API_KEY="your-groq-api-key" \
    TAVILY_API_KEY="your-tavily-api-key" \
  --cpu 2 \
  --memory 4
```

#### Step 9: Get the Public URL
```bash
az container show --resource-group travel-planner-rg \
  --name travel-planner-app \
  --query "{FQDN:ipAddress.fqdn,ProvisioningState:provisioningState}" \
  --out table
```

Your app will be available at:
- Streamlit UI: `http://travel-planner-pranav.eastus.azurecontainer.io:8501`
- FastAPI Backend: `http://travel-planner-pranav.eastus.azurecontainer.io:8000`

---

### Option 2: Azure App Service (Web App for Containers) - Production Ready

#### Step 1-5: Same as Option 1

#### Step 6: Create App Service Plan
```bash
az appservice plan create \
  --name travel-planner-plan \
  --resource-group travel-planner-rg \
  --is-linux \
  --sku B1
```

#### Step 7: Create Web App
```bash
az webapp create \
  --resource-group travel-planner-rg \
  --plan travel-planner-plan \
  --name travel-planner-pranav \
  --deployment-container-image-name travelplanneracr.azurecr.io/travel-planner:latest
```

#### Step 8: Configure Container Registry Credentials
```bash
az webapp config container set \
  --name travel-planner-pranav \
  --resource-group travel-planner-rg \
  --docker-custom-image-name travelplanneracr.azurecr.io/travel-planner:latest \
  --docker-registry-server-url https://travelplanneracr.azurecr.io \
  --docker-registry-server-user travelplanneracr \
  --docker-registry-server-password <PASSWORD_FROM_ACR>
```

#### Step 9: Configure Environment Variables
```bash
az webapp config appsettings set \
  --resource-group travel-planner-rg \
  --name travel-planner-pranav \
  --settings \
    GOOGLE_API_KEY="your-google-api-key" \
    OPENWEATHERMAP_API_KEY="your-weather-api-key" \
    GROQ_API_KEY="your-groq-api-key" \
    TAVILY_API_KEY="your-tavily-api-key" \
    WEBSITES_PORT=8501
```

#### Step 10: Enable Continuous Deployment (Optional)
```bash
az webapp deployment container config \
  --name travel-planner-pranav \
  --resource-group travel-planner-rg \
  --enable-cd true
```

Your app will be available at: `https://travel-planner-pranav.azurewebsites.net`

---

## Local Testing with Docker

Before deploying to Azure, test locally:

```bash
# Build the image
docker build -t travel-planner:local .

# Run the container
docker run -p 8000:8000 -p 8501:8501 \
  -e GOOGLE_API_KEY="your-key" \
  -e OPENWEATHERMAP_API_KEY="your-key" \
  -e GROQ_API_KEY="your-key" \
  -e TAVILY_API_KEY="your-key" \
  travel-planner:local
```

Or use Docker Compose:
```bash
docker-compose up --build
```

Access locally:
- Streamlit: http://localhost:8501
- FastAPI: http://localhost:8000

---

## Monitoring and Logs

### View Container Logs (ACI)
```bash
az container logs --resource-group travel-planner-rg --name travel-planner-app
```

### View Web App Logs (App Service)
```bash
az webapp log tail --name travel-planner-pranav --resource-group travel-planner-rg
```

---

## Updating Your Deployment

1. Make changes to your code
2. Rebuild and push the Docker image:
```bash
docker build -t travelplanneracr.azurecr.io/travel-planner:latest .
docker push travelplanneracr.azurecr.io/travel-planner:latest
```

3. Restart the container:
```bash
# For ACI
az container restart --resource-group travel-planner-rg --name travel-planner-app

# For App Service
az webapp restart --name travel-planner-pranav --resource-group travel-planner-rg
```

---

## Cost Optimization

- **ACI**: Pay per second of runtime (~$0.0000012/second for 1 vCPU, 1GB RAM)
- **App Service B1**: ~$13/month (always running)

For development/testing, use ACI. For production with high traffic, use App Service.

---

## Cleanup Resources

To avoid charges, delete resources when done:

```bash
az group delete --name travel-planner-rg --yes --no-wait
```

---

## Troubleshooting

1. **Container won't start**: Check logs with `az container logs`
2. **API keys not working**: Verify environment variables are set correctly
3. **Port issues**: Ensure ports 8000 and 8501 are exposed
4. **Memory issues**: Increase memory allocation in container settings

---

## Security Best Practices

1. **Never commit API keys** - Use Azure Key Vault for production
2. **Use managed identities** - For accessing Azure resources
3. **Enable HTTPS** - App Service provides free SSL certificates
4. **Restrict network access** - Use Azure Virtual Networks for production

---

## Next Steps

- Set up custom domain
- Configure SSL/TLS certificates
- Implement CI/CD with GitHub Actions
- Add Azure Application Insights for monitoring
- Set up auto-scaling

---

**Developed by PRANAV** 👨‍💻
