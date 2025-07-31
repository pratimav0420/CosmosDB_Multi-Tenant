#!/bin/bash

# Azure Cosmos DB AI Features Quick Start Script
# This script helps set up the environment for testing new AI features

echo "=== Azure Cosmos DB AI Features Quick Start ==="
echo ""

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install it first:"
    echo "   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

echo "✅ Azure CLI found"

# Login check
if ! az account show &> /dev/null; then
    echo "🔐 Please login to Azure first:"
    az login
fi

echo "✅ Azure login verified"

# Set variables (user should modify these)
RESOURCE_GROUP="cosmosdb-ai-workshop"
COSMOS_ACCOUNT="smartbooking-ai-$(date +%s)"
LOCATION="East US"
DATABASE_NAME="AIWorkshopDB"

echo ""
echo "📋 Configuration:"
echo "   Resource Group: $RESOURCE_GROUP"
echo "   Cosmos Account: $COSMOS_ACCOUNT"
echo "   Location: $LOCATION"
echo "   Database: $DATABASE_NAME"
echo ""

read -p "Continue with this configuration? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Setup cancelled"
    exit 1
fi

# Create resource group
echo "📦 Creating resource group..."
az group create --name $RESOURCE_GROUP --location "$LOCATION"

# Create Cosmos DB account with AI features
echo "🚀 Creating Cosmos DB account with AI features (this may take 5-10 minutes)..."
az cosmosdb create \
    --resource-group $RESOURCE_GROUP \
    --name $COSMOS_ACCOUNT \
    --kind GlobalDocumentDB \
    --locations regionName="$LOCATION" failoverPriority=0 isZoneRedundant=False \
    --default-consistency-level Session \
    --enable-free-tier true \
    --capabilities EnableServerless EnableNoSQLVectorSearch

if [ $? -eq 0 ]; then
    echo "✅ Cosmos DB account created successfully"
else
    echo "❌ Failed to create Cosmos DB account"
    exit 1
fi

# Create database
echo "📊 Creating database..."
az cosmosdb sql database create \
    --resource-group $RESOURCE_GROUP \
    --account-name $COSMOS_ACCOUNT \
    --name $DATABASE_NAME

# Create container with vector indexing
echo "📁 Creating container with vector indexing..."
az cosmosdb sql container create \
    --resource-group $RESOURCE_GROUP \
    --account-name $COSMOS_ACCOUNT \
    --database-name $DATABASE_NAME \
    --name "AIContainer" \
    --partition-key-path "/tenantId" \
    --indexing-policy '{
        "indexingMode": "consistent",
        "automatic": true,
        "includedPaths": [{"path": "/*"}],
        "excludedPaths": [{"path": "/_etag/?"}],
        "vectorIndexes": [{"path": "/vectorProperty", "type": "diskANN"}]
    }'

# Get connection strings
echo "🔑 Retrieving connection strings..."
PRIMARY_CONNECTION=$(az cosmosdb keys list --resource-group $RESOURCE_GROUP --name $COSMOS_ACCOUNT --type connection-strings --query 'connectionStrings[0].connectionString' -o tsv)

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "📋 Your AI-Enhanced Cosmos DB Setup:"
echo "   Account Name: $COSMOS_ACCOUNT"
echo "   Database: $DATABASE_NAME"
echo "   Container: AIContainer"
echo "   Resource Group: $RESOURCE_GROUP"
echo ""
echo "🔑 Connection String:"
echo "   $PRIMARY_CONNECTION"
echo ""
echo "📝 Next Steps:"
echo "   1. Set up Dedicated Gateway for Integrated Cache:"
echo "      - Go to Azure Portal > Your Cosmos DB > Settings > Dedicated Gateway"
echo "      - Configure D4s SKU with 1 instance"
echo ""
echo "   2. Enable Query Copilot Preview:"
echo "      - Enroll in Microsoft Copilot for Azure preview"
echo "      - Access via Data Explorer in Azure Portal"
echo ""
echo "   3. Try the sample applications:"
echo "      - C#: samples/CosmosDB_AI_Features_Demo.cs"
echo "      - Python: samples/cosmos_ai_demo.py"
echo ""
echo "   4. Load sample AI data:"
echo "      - Use data/AI_Enhanced_Hotel_Data.json"
echo ""
echo "📚 Documentation:"
echo "   - Implementation Guide: AI-Features-Implementation-Guide.md"
echo "   - Workshop README: README.md (Challenge 6)"
echo ""

# Create environment file for easy reference
cat > .env << EOF
# Azure Cosmos DB AI Features Environment Variables
COSMOS_ACCOUNT_NAME=$COSMOS_ACCOUNT
COSMOS_DATABASE_NAME=$DATABASE_NAME
COSMOS_CONTAINER_NAME=AIContainer
COSMOS_RESOURCE_GROUP=$RESOURCE_GROUP
COSMOS_CONNECTION_STRING="$PRIMARY_CONNECTION"

# Instructions:
# 1. Get dedicated gateway connection string from Azure Portal
# 2. Replace COSMOS_CONNECTION_STRING with dedicated gateway string for cache features
# 3. Install Python requirements: pip install -r samples/requirements.txt
# 4. Run samples with these environment variables
EOF

echo "💾 Environment variables saved to .env file"
echo ""
echo "⚠️  Important: To use Integrated Cache, replace the connection string in .env"
echo "   with the Dedicated Gateway connection string from Azure Portal"
echo ""
echo "🔧 To set up Dedicated Gateway via CLI (optional):"
echo "   az cosmosdb service create \\"
echo "     --resource-group $RESOURCE_GROUP \\"
echo "     --account-name $COSMOS_ACCOUNT \\"
echo "     --kind DedicatedGateway \\"
echo "     --count 1 \\"
echo "     --size Cosmos.D4s"
echo ""
echo "Happy coding with Azure Cosmos DB AI features! 🚀"
