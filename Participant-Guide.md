# Azure Cosmos DB Multi-Tenant Workshop - Participant Guide

## 🎯 Welcome to the Workshop!

This comprehensive guide will take you through building a multi-tenant SaaS application using Azure Cosmos DB. You'll learn modern data modeling, cost optimization, and cutting-edge AI features.

---

## 📋 Pre-Workshop Setup Checklist

Before we begin, ensure you have completed the following setup:

### ✅ Required Accounts & Access
- [ ] **Azure Subscription**: Active subscription with Contributor role
- [ ] **GitHub Account**: For accessing workshop materials
- [ ] **Workshop Repository**: Clone from [GitHub Repository](https://github.com/pratimav0420/CosmosDB_Multi-Tenant)

### ✅ Required Software
- [ ] **Web Browser**: Chrome, Edge, or Firefox (latest version)
- [ ] **Azure CLI**: [Download and install](https://docs.microsoft.com/cli/azure/install-azure-cli)
- [ ] **Code Editor**: VS Code (recommended) or Visual Studio
- [ ] **Git Client**: For repository access

### ✅ Verification Steps
1. **Test Azure CLI**:
   ```bash
   az login
   az account show
   ```

2. **Verify Azure Portal Access**:
   - Navigate to [portal.azure.com](https://portal.azure.com)
   - Confirm you can create resources

3. **Clone Workshop Repository**:
   ```bash
   git clone https://github.com/pratimav0420/CosmosDB_Multi-Tenant.git
   cd CosmosDB_Multi-Tenant
   ```

---

## 🚀 Session 1: Multi-Tenant Data Modeling (9:30 - 10:45 AM)

### Learning Objectives
- Understand multi-tenant application architecture
- Design NoSQL data models for multi-tenancy
- Plan partition strategies for optimal performance

### Challenge 1: Model Data to Build SaaS Applications

#### Step 1: Review Business Requirements (15 minutes)

**📖 Scenario**: Smart Booking Inc. wants to convert their hotel reservation system into a SaaS application serving multiple hotel chains.

**Current Customers**:
- **Casino Hotels** (Small): 2 locations, 50 rooms each
- **Family Fun Hotels** (Medium): 5 locations, 150 rooms each  
- **Hiking Hotels** (Medium): 3 locations, 100 rooms each
- **GoodFellas Hotels** (Large): 20 locations, 300 rooms each

#### 🔧 **Task 1.1: Analyze Object Model**
1. Open the workshop README.md file
2. Navigate to Challenge 1 section
3. Review the Multi-Tenant Reservation System Object Model diagram
4. Identify the key entities:
   - **Business_Entity**: Hotel chain information
   - **Tenant**: Location-specific data
   - **Hotel_Room**: Room catalog and types
   - **Customers**: Guest profiles
   - **Room_Inventory**: Available rooms per location
   - **Room_Availability**: Rates and availability by date
   - **Hotel_Reservations**: Booking records

#### 🔧 **Task 1.2: Identify Access Patterns**
Document the primary access patterns:

1. **Room Availability Search**:
   ```
   Query: Find available rooms by location, dates, and room type
   Frequency: Very High (every customer search)
   Scope: Single tenant (location)
   ```

2. **Reservation Management**:
   ```
   Query: Create, read, update, cancel reservations
   Frequency: High
   Scope: Single tenant + customer
   ```

3. **Inventory Updates**:
   ```
   Query: Update room availability after booking
   Frequency: High
   Scope: Single tenant
   ```

4. **Business Reporting**:
   ```
   Query: Occupancy rates, revenue reports
   Frequency: Medium
   Scope: Single or multiple tenants
   ```

#### 🔧 **Task 1.3: Design Partition Strategy**

**Key Decision**: Use `tenantId` as the partition key

**Rationale**:
- ✅ Isolates data by hotel location
- ✅ Most queries are location-specific
- ✅ Supports compliance and data residency
- ✅ Enables tenant-specific scaling

**Document Structure Design**:
```json
{
  "id": "unique-document-id",
  "tenantId": 1001,
  "type": "Reservation|Inventory|Customer|Room",
  "data": {
    // Entity-specific properties
  },
  "metadata": {
    "created": "2025-07-30T10:00:00Z",
    "lastModified": "2025-07-30T10:00:00Z"
  }
}
```

#### ✅ **Checkpoint 1**: Complete Data Model Design
- [ ] Documented access patterns
- [ ] Defined partition key strategy
- [ ] Designed document structure
- [ ] Identified potential challenges

---

## 🏗️ Session 2: Azure Deployment & Infrastructure (11:00 - 12:30 PM)

### Learning Objectives
- Deploy Azure Cosmos DB using Infrastructure as Code
- Understand ARM template structure
- Configure multi-tenant database architecture

### Challenge 2: Deploy Azure Cosmos DB Service

#### Step 1: Review ARM Template (15 minutes)

#### 🔧 **Task 2.1: Examine azuredeploy.json**
1. Open `azuredeploy.json` in your code editor
2. Identify key components:

**Parameters Section**:
```json
{
  "cosmosDbLocation": {
    "type": "string",
    "allowedValues": ["East US", "West US", "Central US", ...]
  }
}
```

**Variables Section**:
```json
{
  "cosmosAccountName": "[toLower(concat('smartbookinginc-', uniqueString(resourceGroup().id)))]",
  "cosmosDatabase1Name": "SharedThroughputDB",
  "cosmosDatabase2Name": "DedicatedThroughputDB"
}
```

**Resources Section**:
- Database Account with AI capabilities
- Shared throughput database
- Dedicated throughput database
- Multiple containers with vector indexing

#### Step 2: Deploy Infrastructure (30 minutes)

#### 🔧 **Task 2.2: Deploy to Azure**

1. **Open Azure Portal in Incognito/Private Mode**:
   ```
   https://portal.azure.com
   ```

2. **Navigate to Workshop Repository**:
   - Go to: `https://github.com/pratimav0420/CosmosDB_Multi-Tenant`
   - Click the "Deploy to Azure" button

3. **Configure Deployment**:
   - **Resource Group**: Create new: `cosmosdb-workshop-rg`
   - **Region**: Select your preferred region
   - **Cosmos DB Location**: Match your resource group region

4. **Monitor Deployment**:
   - Wait 5-10 minutes for completion
   - Check deployment status in Azure Portal

#### 🔧 **Task 2.3: Verify Deployment**

1. **Navigate to Resource Group**:
   - Find your new resource group
   - Verify Cosmos DB account creation

2. **Explore Cosmos DB Account**:
   - Click on the Cosmos DB account
   - Note the account name format
   - Check the location and pricing tier

3. **Examine Database Structure**:
   - Go to **Data Explorer**
   - Expand **SharedThroughputDB**:
     - `CasinoHotel` container
     - `FamilyFunHotel` container
   - Expand **DedicatedThroughputDB**:
     - `GoodFellasHotel` container

#### Step 3: Understand Configuration (25 minutes)

#### 🔧 **Task 2.4: Analyze Database Settings**

1. **Shared Throughput Database**:
   - Select `SharedThroughputDB`
   - Click **Scale**
   - Note: Autoscale up to 2,000 RU/s
   - **Purpose**: Cost-effective for small/medium tenants

2. **Container Configuration**:
   - Select `CasinoHotel` container
   - Click **Settings**
   - Note: Partition key = `/tenantId`
   - Review indexing policy

3. **Dedicated Throughput Database**:
   - Select `DedicatedThroughputDB`
   - Note: No database-level throughput
   - Individual container throughput

#### ✅ **Checkpoint 2**: Infrastructure Deployment
- [ ] Azure Cosmos DB account deployed
- [ ] Database structure configured
- [ ] Partition keys validated
- [ ] Throughput settings understood

---

## 🏢 Session 3: Multi-Tenant Strategy Implementation (1:30 - 3:00 PM)

### Learning Objectives
- Configure different throughput strategies
- Load multi-tenant data
- Optimize for various customer sizes

### Challenge 3: Design Cosmos DB Account for Different Customer Sizes

#### Step 1: Configure Small Customer Strategy (20 minutes)

#### 🔧 **Task 3.1: Examine Shared Throughput Setup**

1. **Navigate to SharedThroughputDB**:
   - Go to Data Explorer
   - Expand `SharedThroughputDB`
   - Click **Scale**

2. **Understand Autoscale Configuration**:
   ```
   Maximum RU/s: 2,000
   Minimum RU/s: 200 (10% of max)
   Billing: Pay for actual usage between min/max
   ```

3. **Review Container Setup**:
   - `CasinoHotel`: Shares database throughput
   - `FamilyFunHotel`: Shares database throughput
   - **Benefit**: Cost-effective for small tenants

#### 🔧 **Task 3.2: Add Medium Customer Container**

1. **Create New Container**:
   - Click **New Container**
   - Database: Use existing `SharedThroughputDB`
   - Container ID: `HikingHotel`
   - Partition key: `/tenantId`
   - **Select**: "Provision dedicated throughput for this container"
   - Container Max RU/s: 2,000
   - Click **OK**

2. **Verify Configuration**:
   - Container has dedicated throughput
   - Isolated from shared database throughput
   - **Benefit**: Avoids "noisy neighbor" issues

#### Step 2: Load Sample Data (25 minutes)

#### 🔧 **Task 3.3: Download and Prepare Data**

1. **Download Workshop Data**:
   - Navigate to `data/` folder in repository
   - Download `Multi-Tenant_CosmosDB_Workshop_data.zip`
   - Extract to local folder

2. **Review Data Files**:
   ```
   CasinoHotel_RoomInventory.json
   CasinoHotel_Reservation.json
   FamilyFunHotel_RoomInventory.json
   FamilyFunHotel_Reservation.json
   HikingHotel_RoomInventory.json
   HikingHotel_Reservation.json
   GoodFellasHotel_RoomInventory.json
   GoodFellasHotel_Reservation.json
   ```

#### 🔧 **Task 3.4: Load Data into Containers**

**For CasinoHotel Container**:
1. **Navigate to Data Explorer**:
   - Expand `SharedThroughputDB`
   - Expand `CasinoHotel` container
   - Click **Items**

2. **Upload Room Inventory**:
   - Click **Upload Item**
   - Select `CasinoHotel_RoomInventory.json`
   - Click **Upload**

3. **Upload Reservations**:
   - Click **Upload Item**
   - Select `CasinoHotel_Reservation.json`
   - Click **Upload**

**Repeat for all containers**:
- `FamilyFunHotel`
- `HikingHotel`
- `GoodFellasHotel`

#### Step 3: Query and Analyze Data (25 minutes)

#### 🔧 **Task 3.5: Execute Sample Queries**

1. **Open Query Editor**:
   - Select `CasinoHotel` container
   - Click **New SQL Query**

2. **Basic Count Query**:
   ```sql
   SELECT COUNT(1) FROM c WHERE c.type='Reservation'
   ```
   - Click **Execute Selection**
   - Note: Cross-partition query (higher RU cost)

3. **Optimized Query with Partition Key**:
   ```sql
   SELECT COUNT(1) FROM c 
   WHERE c.type='Reservation' AND c.tenantId=1001
   ```
   - Compare RU consumption
   - Note: Single-partition query (lower RU cost)

4. **Advanced Query with Projections**:
   ```sql
   SELECT {
     "Customer Name": CONCAT(c.cust.firstName," ",c.cust.lastName), 
     "Room Rate": c.roomRate
   } as customerrate 
   FROM c 
   WHERE c.type='Reservation' AND c.tenantId=1001 
   ORDER BY c.roomRate DESC
   ```

#### 🔧 **Task 3.6: Analyze Performance**

1. **Check Query Stats**:
   - Click **Query Stats** tab
   - Review:
     - Request charge (RUs consumed)
     - Retrieved document count
     - Output document count
     - Query execution time

2. **Compare Query Patterns**:
   | Query Type | RU Cost | Performance | Use Case |
   |------------|---------|-------------|----------|
   | Cross-partition | High | Slower | Analytics |
   | Single-partition | Low | Fast | OLTP |
   | With projection | Variable | Faster | APIs |

#### ✅ **Checkpoint 3**: Multi-Tenant Implementation
- [ ] Shared throughput database configured
- [ ] Dedicated throughput container created
- [ ] Sample data loaded across all tenants
- [ ] Query performance analyzed
- [ ] RU consumption patterns understood

---

## 🤖 Session 4: AI-Enhanced Features (3:15 - 4:15 PM)

### Learning Objectives
- Implement vector database capabilities
- Configure integrated cache for performance
- Explore natural language query generation

### Challenge 6: Implement AI-Enhanced Features

#### Step 1: Enable Vector Search (15 minutes)

#### 🔧 **Task 4.1: Update Container Indexing Policy**

1. **Select CasinoHotel Container**:
   - Go to Data Explorer
   - Expand `SharedThroughputDB` → `CasinoHotel`
   - Click **Scale & Settings**

2. **Modify Indexing Policy**:
   - Click **Indexing Policy**
   - Replace the existing policy with:

```json
{
    "indexingMode": "consistent",
    "automatic": true,
    "includedPaths": [
        {
            "path": "/*"
        }
    ],
    "excludedPaths": [
        {
            "path": "/_etag/?"
        }
    ],
    "vectorIndexes": [
        {
            "path": "/vectorProperty",
            "type": "diskANN"
        }
    ]
}
```

3. **Save Configuration**:
   - Click **Save**
   - Wait for indexing to complete

#### 🔧 **Task 4.2: Load AI-Enhanced Data**

1. **Upload Vector Data**:
   - In `CasinoHotel` container, click **Items**
   - Click **Upload Item**
   - Select `data/AI_Enhanced_Hotel_Data.json`
   - Click **Upload**

2. **Verify Vector Data**:
   - Click **New SQL Query**
   - Execute:
   ```sql
   SELECT * FROM c WHERE c.type = 'AIRecommendation'
   ```

#### Step 2: Configure Integrated Cache (15 minutes)

#### 🔧 **Task 4.3: Set Up Dedicated Gateway**

1. **Navigate to Dedicated Gateway**:
   - In your Cosmos DB account
   - Go to **Settings** → **Dedicated Gateway**

2. **Provision Gateway**:
   - Click **Create dedicated gateway**
   - **SKU**: D4s (4 vCores, 16 GB RAM)
   - **Instance count**: 1
   - Click **Create**
   - Wait 5-10 minutes for provisioning

3. **Get Gateway Connection String**:
   - Once provisioned, copy the **Dedicated Gateway Connection String**
   - Save for later use in applications

#### 🔧 **Task 4.4: Test Cache Performance**

1. **Execute Test Queries**:
   ```sql
   -- First execution (cache miss)
   SELECT * FROM c WHERE c.id = 'ai-hotel-recommendation-1'
   ```

2. **Check Query Stats**:
   - Note the RU charge
   - Execute the same query again
   - Compare RU charges (second should be 0 if cached)

#### Step 3: Explore Query Copilot (15 minutes)

#### 🔧 **Task 4.5: Enable Query Copilot**

1. **Check Preview Enrollment**:
   - Ensure your subscription is enrolled in **Microsoft Copilot for Azure in Cosmos DB preview**

2. **Access Copilot Interface**:
   - In Data Explorer, look for the **Copilot** button
   - Click to enable the interface

3. **Try Natural Language Queries**:

**Example Prompts to Try**:
```
"Show me all hotel reservations for tenant 1001"
"Find rooms with rates above $200 per night"  
"Count reservations by room type"
"Show luxury suite recommendations"
```

#### 🔧 **Task 4.6: Compare Generated Queries**

1. **Analyze Generated SQL**:
   - For each prompt, review the generated NoSQL query
   - Note how natural language translates to syntax

2. **Example Comparison**:
   ```
   Prompt: "Show me luxury suite reservations"
   
   Generated:
   SELECT * FROM c 
   WHERE c.type = 'Reservation' 
   AND CONTAINS(UPPER(c.roomType), 'SUITE')
   ```

#### ✅ **Checkpoint 4**: AI Features Implementation
- [ ] Vector indexing enabled
- [ ] AI-enhanced data loaded
- [ ] Dedicated gateway configured
- [ ] Integrated cache tested
- [ ] Query Copilot explored
- [ ] Natural language queries validated

---

## 🚀 Session 5: Production Readiness (4:15 - 4:50 PM)

### Learning Objectives
- Configure high availability features
- Set up monitoring and alerting
- Prepare for production deployment

### Challenge 4 & 5: High Availability and Local Development

#### Step 1: Configure High Availability (10 minutes)

#### 🔧 **Task 5.1: Enable Service-Managed Failover**

1. **Navigate to Global Distribution**:
   - In your Cosmos DB account
   - Go to **Settings** → **Replicate data globally**

2. **Review Current Configuration**:
   - Note your current write region
   - See available read regions

3. **Enable Automatic Failover**:
   - Click **Automatic Failover**
   - Toggle **Enable Service-Managed Failover** to **On**
   - **Note**: This will take time to complete (don't wait)

#### 🔧 **Task 5.2: Test Autoscale Features**

1. **Navigate to Dedicated Container**:
   - Go to `DedicatedThroughputDB` → `GoodFellasHotel`
   - Click **Scale & Settings**

2. **Modify Throughput**:
   - Change Max RU/s from 1000 to 2000
   - Click **Save**
   - Note: Instant scaling without downtime

#### Step 2: Set Up Local Development (10 minutes)

#### 🔧 **Task 5.3: Install Cosmos DB Emulator**

1. **Download Emulator**:
   - Go to: https://aka.ms/cosmosdb-emulator
   - Download latest version

2. **Install with Administrative Rights**:
   - Run installer as administrator
   - Follow installation wizard

3. **Launch Emulator**:
   - Start emulator from Start menu
   - Wait for startup (may take 2-3 minutes)
   - Browser will open with emulator interface

#### 🔧 **Task 5.4: Configure Local Development**

1. **Copy Emulator Connection Details**:
   - URI: Usually `https://localhost:8081`
   - Primary Key: Copy from emulator interface

2. **Test Sample Application**:
   - Download .NET sample from emulator interface
   - Or use provided sample code in `samples/` folder
   - Update connection string in configuration

#### Step 3: Monitor and Alert Setup (10 minutes)

#### 🔧 **Task 5.5: Configure Azure Monitor**

1. **Navigate to Metrics**:
   - In your Cosmos DB account
   - Go to **Monitoring** → **Metrics**

2. **Key Metrics to Monitor**:
   - **Total Request Units**: Track RU consumption
   - **Total Requests**: Monitor request volume
   - **Availability**: Track uptime
   - **Server Side Latency**: Monitor performance

3. **Set Up Alerts** (Optional):
   - Click **New alert rule**
   - Configure thresholds for:
     - High RU consumption
     - Low availability
     - High latency

#### 🔧 **Task 5.6: Review Cost Management**

1. **Check Current Usage**:
   - Go to **Cost Management + Billing**
   - Review current charges
   - Understand pricing model

2. **Optimization Strategies**:
   - Free tier utilization (1000 RU/s)
   - Autoscale vs provisioned throughput
   - Integrated cache benefits
   - Regional placement optimization

#### ✅ **Checkpoint 5**: Production Readiness
- [ ] High availability configured
- [ ] Autoscale capabilities tested
- [ ] Local development environment set up
- [ ] Monitoring and alerting configured
- [ ] Cost optimization strategies understood

---

## 🎯 Final Challenge: Complete Implementation

### Optional Extended Exercise (If Time Permits)

#### 🔧 **Task 6.1: Build a Simple RAG Application**

1. **Design RAG Architecture**:
   ```
   User Query → Embedding Generation → Vector Search → 
   Context Retrieval → LLM Generation → Response
   ```

2. **Implementation Steps**:
   - Use sample code from `samples/cosmos_ai_demo.py`
   - Configure Azure OpenAI integration
   - Test semantic search capabilities

3. **Test Scenarios**:
   - "Find luxury hotels with spa facilities"
   - "Recommend rooms for business travelers"
   - "Show pet-friendly accommodations"

#### 🔧 **Task 6.2: Performance Optimization**

1. **Cache Hit Rate Analysis**:
   - Monitor `IntegratedCacheItemHitRate`
   - Target >70% hit rate
   - Adjust cache staleness as needed

2. **Query Optimization**:
   - Always include partition key when possible
   - Use projections to reduce data transfer
   - Minimize cross-partition queries

---

## 📊 Workshop Summary & Key Takeaways

### What You've Accomplished

1. **✅ Multi-Tenant Architecture**:
   - Designed NoSQL data model for multi-tenancy
   - Implemented partition strategies for optimal performance
   - Configured throughput for different customer sizes

2. **✅ AI-Enhanced Capabilities**:
   - Enabled vector database for AI applications
   - Configured integrated cache for performance optimization
   - Explored natural language query generation

3. **✅ Production Readiness**:
   - Set up high availability and disaster recovery
   - Configured monitoring and alerting
   - Established local development environment

4. **✅ Cost Optimization**:
   - Leveraged free tier and autoscale features
   - Implemented caching strategies
   - Understanding pricing optimization techniques

### Next Steps for Your Projects

1. **Immediate Actions**:
   - Apply partition key strategies to your use cases
   - Implement autoscale for cost optimization
   - Set up monitoring and alerting

2. **Short-term Goals (1-4 weeks)**:
   - Enable AI features for your applications
   - Implement integrated cache for read-heavy workloads
   - Configure high availability for production

3. **Long-term Strategy (1-6 months)**:
   - Build RAG applications with vector search
   - Optimize costs using reserved capacity
   - Implement advanced security and compliance

### Additional Resources

#### 📚 **Documentation**:
- [Azure Cosmos DB Documentation](https://docs.microsoft.com/azure/cosmos-db/)
- [Multi-tenant SaaS Patterns](https://docs.microsoft.com/azure/architecture/patterns/)
- [Vector Database Guide](https://docs.microsoft.com/azure/cosmos-db/vector-database)

#### 💻 **Code Samples**:
- [Workshop Repository](https://github.com/pratimav0420/CosmosDB_Multi-Tenant)
- [Azure Cosmos DB Samples](https://github.com/Azure-Samples/cosmos-db-nosql-samples)
- [AI Integration Examples](https://github.com/Azure-Samples/cosmos-db-nosql-vector-search)

#### 🤝 **Community Support**:
- [Azure Cosmos DB Tech Community](https://techcommunity.microsoft.com/t5/azure-cosmos-db/bd-p/AzureCosmosDB)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/azure-cosmosdb)
- [Discord Community](https://discord.gg/cosmosdb)

#### 🎓 **Continued Learning**:
- [Microsoft Learn - Cosmos DB Learning Path](https://docs.microsoft.com/learn/paths/work-with-nosql-data-in-azure-cosmos-db/)
- [Azure Cosmos DB Developer Specialty Certification](https://docs.microsoft.com/learn/certifications/azure-cosmos-db-developer-specialty/)

### Workshop Feedback

Please provide feedback to help us improve future workshops:

1. **What was most valuable?**
2. **What could be improved?**
3. **What topics would you like to see in future workshops?**
4. **How likely are you to recommend this workshop?**

---

## 🆘 Troubleshooting Guide

### Common Issues and Solutions

#### **Issue**: ARM Template Deployment Fails
**Solution**:
- Check resource group permissions
- Verify region availability
- Ensure unique resource names

#### **Issue**: Cannot Access Data Explorer
**Solution**:
- Check firewall settings
- Verify network connectivity
- Try different browser/incognito mode

#### **Issue**: Vector Search Not Working
**Solution**:
- Verify API version (2024-05-15+)
- Check vector index configuration
- Ensure vector dimensions match

#### **Issue**: Integrated Cache Not Showing Benefits
**Solution**:
- Use dedicated gateway connection string
- Set ConnectionMode to Gateway
- Verify consistency level (Session/Eventual)

#### **Issue**: Query Copilot Unavailable
**Solution**:
- Enroll in preview program
- Check subscription eligibility
- Try different browser

### Getting Help During the Workshop

1. **Raise your hand** for immediate assistance
2. **Use chat/messaging** for quick questions
3. **Work with a partner** for collaborative problem-solving
4. **Check troubleshooting section** for common issues

---

**🎉 Congratulations on completing the Azure Cosmos DB Multi-Tenant Workshop!**

You now have the knowledge and hands-on experience to build scalable, cost-effective, and AI-enhanced multi-tenant applications using Azure Cosmos DB. Apply these skills to transform your applications and take advantage of modern cloud-native capabilities.

**Happy coding! 🚀**
