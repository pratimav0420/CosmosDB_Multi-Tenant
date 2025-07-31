

# Azure Cosmos DB for Multitenant Applications Workshop

**🆕 Updated for 2025 with cutting-edge AI features!**

This workshop now includes the latest Azure Cosmos DB enhancements that position it as the **database for the AI era**:
- **Vector Database Integration** - Store and search vector embeddings alongside operational data
- **Query Copilot (Preview)** - Generate NoSQL queries using natural language prompts  
- **Integrated Cache** - In-memory caching with dedicated gateway for cost optimization
- **AI Advantage Program** - Up to $6,000 in free credits for Azure AI customers

## Azure Cosmos DB Introduction

Azure Cosmos DB is a fully managed NoSQL database for modern multitenant application development and **the AI era**. You can build applications 
fast with open source APIs, multiple SDKs, schemaless data and no-ETL analytics over operational data.
Single-digit millisecond response times, and instant scalability, guarantee speed at any scale.
Guarantee business continuity, 99.999% availability and enterprise-grade security for every application.
End-to-end database management, with serverless and automatic scaling matching your application and TCO needs. 

**NEW AI-Enhanced Features for 2024/2025:**
- **Integrated Vector Database**: Store vector embeddings alongside your operational data for AI applications
- **Query Copilot (Preview)**: Generate NoSQL queries using natural language prompts powered by AI
- **Integrated Cache**: In-memory caching with dedicated gateway for improved performance and cost optimization
- **AI Advantage Program**: 40,000 RU/s of throughput for 90 days (up to $6,000 value) for Azure AI customers

Supports multiple database APIs including native API for NoSQL, API for Mongo DB, Apache Cassandra, Apache Gremlin and Table.
It also started supporting PostgreSQL extended with the Citus Open Source which is useful for highly scalable relational apps.

To begin using Azure Cosmos DB, create an Azure Cosmos DB account in an Azure resource group in your subscription. 
You then create databases and containers within the account.

#### Resource Model:
A single Azure Cosmos DB account can virtually manage an unlimited amount of data and provisioned throughput. 
To manage your data and provisioned throughput, you can create one or more databases within your account, 
then one or more containers to store your data. 

<img src="./images/CosmosDB_ResourceModel.jpg" alt="Cosmos DB Resource Model" Width="600">

#### Request Units: 
Cost of database operations is normalized by Azure Cosmos DB and is expressed by Request Units (RU). It is a performance 
currency abstracting the system resources such as CPU, IOPS and Memory to perform the database operations supported by 
Azure Cosmos DB. You can examine the response header to track the number of RUs that are consumed by any database 
operation.
<img src="./images/CosmosDB_Request_unit.jpg" alt="Request Unit Diagram" Width="600" >


#### Indexing: 
Azure Cosmos DB is a schema-agnostic database that allows you to iterate on your application without having to deal with schema 
or index management. By default, Azure Cosmos DB automatically indexes every property for all items in your container without 
having to define any schema or configure secondary indexes. When an item is written, Azure Cosmos DB effectively indexes each 
property's path and its corresponding value. In some situations, you may want to override this automatic behavior to better 
suit your requirements. You can customize a container's indexing policy by setting its indexing mode, and include or exclude 
property paths.

Access [Azure Cosmos DB Documentation](https://learn.microsoft.com/azure/cosmos-db/introduction) for more details and training. 

## Why Azure Cosmos DB?
Here are the scenarios where Azure Cosmos DB can help:
* Looking to modernize their monolithic on-premise applications as SaaS applications.
* scale up to the max throughput for addressing unpredicted workloads and scale down automatically.
* Goals to expand globally with low latency and highly scalable throughput. 
* Trying to reduce costs to support multiple customers with fluctuating throughput requirement.
* Application needs to support multiple businesses with flexible schema.
* Unable to meet performance SLA requirements and reaching max storage limits with growing data.

All the above use cases need a new mindset and special features. This workshop will show you how Azure Cosmos DB will be the best option.



## Workshop Challenge List
- [Challenge-1: Model data to build SaaS applications](#Challenge-1-Model-data-to-build-SaaS-applications)
- [Challenge-2: Deploy Azure Cosmos DB Service](#Challenge-2-Deploy-Azure-Cosmos-DB-Service)
- [Challenge-3: Design Cosmos DB Account to serve small, medium and large customers](#Challenge-3-Design-Cosmos-DB-Account-to-serve-small-medium-and-large-customers)
- [Challenge-4: Validate Cosmos DB features Auto Failover, Autoscale and Low Latency](#Challenge-4-Validate-Cosmos-DB-features-Auto-failover-Autoscale-and-Low-latency)
- [Challenge-5: Build an application using Cosmos DB Emulator at no cost](#Challenge-5-Build-an-application-using-Azure-Cosmos-DB-at-no-cost)
- **[Challenge-6: NEW - Implement AI-Enhanced Features (Vector Search, Query Copilot, Integrated Cache)](#Challenge-6-Implement-AI-Enhanced-Features)**

## Multi-Tenancy features for Software Companies 

### Distributes Data horizontally
By using partitions with Azure Cosmos DB containers, you can create containers that are shared across multiple tenants. 
With large containers, Azure Cosmos DB spreads your tenants across multiple physical nodes to achieve a high degree of scale.

### Control the **throughput** based on the size of the customer to lower your costs: 
Typically, you provision a defined number of request units per second for your workload, which is referred 
to as throughput. You can assign throughput at a container level, at a database level to share among the containers, automatically
scale up to the max throughput for address unpredicted workloads and scale down to 10% of Max to save costs.

    
## Business Scenario
Fictitious ISV company called "Smart Booking Inc" has built an on-line reservation application called "EasyReserveApp" and 
currently deployed as an on-premises application to 4 hotel chains. This application is a big hit in the industry and 
they want to convert this application as a SaaS application to meet the global demand. They are looking for a database 
to handle unpredictable volume, maintain low latency response time to users at any part of the world, maintain high 
availability & business continuity with optimized cost based on the usage. 

It currently has the following clients in the Hotel Industry:

<img src="./images/MultiTenant_Hotel_Business_Model.jpg" alt="Application Data Model Architecture" Width="600" Height="400">


This workshop gives you handson experience on designing Azure Cosmos DB for small, medium and large multi-tenant 
customers using this use case.  


## Architecture Solution Diagram
<img src="./images/Multi-Tenant_Cosmos_DB_Workshop_Architecture.jpg" alt="Architecture for Azure Cosmos DB Lab" Width="600"> 


## Challenge-1: Model data to build SaaS applications
Let us review the object model for this application and plan the data model for SaaS application.

### Multi-Tenant Reservation System Object Model

**Business_Entity** object contains all the business entity data.
**Tenant** object contains the tenant location address and contact info.
**Hotel_Room** object contains catalog of rooms with type, view, number of beds etc.
**Customers** object has all the customer profile data. 
**Room_Inventory** object contains all the room numbers with room type in each tenant location.
**Room_Availability** object contains available dates with rate info for each tenant location.
**Hotel_Reservations** object contains all the hotel reservations for each tenant location.

<img src="./images/MultiTenant_Hotel_Business_Software_Object_Model.jpg" alt="Multi-Tenant Reservation System Object Model" Width="600">

### Access Patterns

1) Provide Hotel Room availability to support customer search based on location, dates and room types.
2) Need to update availability after customer completes the reservation.
3) Customer will access the reservation to review, cancel or update. 
4) Business owners and the support team at each tenant location will access the availability to 
book/change reservation as per their customer request. 

You would want to keep all the relevant data in one object based on the highly frequent access patterns to write and read data.

<!--<img src="./images/CosmosDB_MultiTenant_Hotel_Business_Data_Model.jpg" alt="Cosmos DB Document Model diagram" width="800"> ---> 

This challenge demonstrate how software object model transform to NoSQL database design model which completely different from SQL based
databases. **Cosmos DB Data Model requires a different mindset and also requires the knowledge of highly frequent access patterns.**

Apply the same methodology to migrate your legacy applications or to build new green field applications. **You have successfully 
completed challenge 2 by creating a Cosmos DB data model based on highly frequent access patterns!!**


## Challenge-2: Deploy Azure Cosmos DB Service 

We have developed an Azure Deployment script to provision the required Azure Services used in the above architecture diagram.

2.1 Open a new InPrivate window from your Microsoft Edge browser. 

<img src="./images/Browser_in_private_Marked.jpg" alt="Edge Browser InPrivate Window selection" width="400">

2.2 Enter the following Workshop github link in the browser.
```
	https://github.com/pratimav0420/CosmosDB_Multi-Tenant
```

2.3 Click **Challenge-1** from Workshop Challenge List. 

2.4 Click the "Deploy to Azure" button

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmicrosoft%2FCosmosDB_Multi-Tenant%2Fmain%2Fazuredeploy.json)

2.5 Enter your Workshop **login Id and Password** provided by the instructor.

2.6 You will see **Welcome to SDP Innovation!** screen. Select **Yes**.

2.7. Enter the following options in the custom deployment screen.
	
* Select your allocated resource group from the dropdown.

* Select your region from the dropdown list for **Cosmos DB Location** selection. 

Best practice is to keep resource group and Cosmos DB account in the same region. We had to set the resource group
"West US" to automate the deployment script. Don't follow this practice in your environment.

2.8 Click on "Review+create" button.

<img src="./images/CosmosDB_AzureDeploymentOptions_Marked.jpg" alt="Azure Custom Depolyment Screen" Width="600">

2.9 It completes the validation as the next step and click on 'create' button.

It will provision Azure Cosmos DB account in your subscription:

It may take 2 to 5 minutes to create the services.

2.10 Click on "Go to resource group" when the deployment is complete.

<img src="./images/CosmosDB_AzureDeployment_Complete_Marked.jpg" alt="Deployment complete" Width="600">

It will take you to your resource group showing the installed Azure Cosmos DB services.

<img src="./images/CosmosDB_AzureDeployment_ResourceGroup_Marked.jpg" alt="Resource Group with Services list" Width="600">

You have successfully deployed the required services to Azure. Congratulations for completing your first challenge.



## Challenge-3: Design Cosmos DB Account to serve small, medium and large customers

Evaluate options to keep relevant data in one logical partition using partitioning key.


### Database Strategies to support small, medium and large customers

#### Shared throughput for small business entities

It would be better to create one container per business entity and share the throughput at the database level. This will avoid 
creating one database per each customer and saves lot of money. You will have to understand that it may cause noisy neighbor 
problem. This approach tends to work well when the amount of data stored for each tenant is small. 

It can be a good choice for building a pricing model that includes a free tier, and for business-to-consumer (B2C) solutions. 
In general, by using shared containers, you achieve the highest density of tenants and therefore the lowest price 
per tenant.

#### 3.1 Create Cosmos DB Containers with shared database throughput

* Access Cosmos DB Service in Azure Portal.
* Select **Data Explorer** from the left panel.
* Select **SharedThroughputDB** database.
* Expand **CasinoHotel** container. 
* select **Settings**.
* You will see **tenantId** as the partition key. It will create logical partitions per each tenant location. 

* Verify FamilyFunHotel Container for the partition key.
* Select **Scale** property under **SharedThroughputDB** database.
* It is set to use Autoscale up to 2,000 RUs and will share across all the containers (business entities). 

Autoscale will fall back to 200 RUs (10% of max RUs) when no activity. **This will save lot money since you don't have to allocate 
the maximum capacity all the time.**

**This database models serves multiple customers with multi-tenant data models with AutoScale capability to lower the costs and avoids 
creating single database per customer.**

<img src="./images/sharedThroughputContainers_3d.jpg" alt="Shared Throughtput at Database level" width="800" >

#### Dedicated throughput to avoid Noisy Neighbor
Hiking Hotel is a medium size business entity and you can avoid noisy neighbor issue by providing a dedicated throughput at 
the container level. Follow the steps to create a dedicated throughput as part of the shared throughput database.

#### 3.2 Add Cosmos DB container with dedicated throughput under shared database throughput 

Follow the steps to provision a new container with a dedicated throughput in a shared throughput database.  

* Select **New Container** from the top bar inside Data Explorer.
* Select **ShardThroughputDB** under **Use existing** database dropdown 
* Type **HikingHotel** as the container name
* Type **/tenantId** as partition key.
* Select **Provision dedicated throughput for this container** option.
* Set the **Container Max RUs** as 2000.
* click **OK**

<img src="./images/create_SharedThroughputContainers_3d.jpg" alt="Create dedicated throughput container" width="800">


#### Database per business entity
You can provision dedicated containers for each business entity. This can work well for isolating large customers with higher 
throughput requirement and for providing dedicated capacity. It will provide guaranteed level of performance, serve medium size 
customers.

#### 3.3 Create Cosmos DB Database to serve large customers

* Select **DedicatedThroughputDB** database
* Expand **GoodFellas** container.
* Select **Scale & Settings** 
* It shows 1000 RUs as the Maximum RUs with Autoscale throughput option.

<img src="./images/DedicatedThroughputDB_3d.jpg" atl="dedicated database for large customers" width="800">

#### Account for tenant
You can provision separate database accounts for each tenant, which provides the highest level of isolation, 
but the lowest density. A single database account is dedicated to a tenant, which means they are not subject to 
the noisy neighbor problem. You can also configure the location of the container data via replication according to the 
tenant's requirements, and you can tune the configuration of Azure Cosmos DB features, network access, backup policy, 
geo-replication and customer-managed encryption keys, to suit each tenant's requirements.

#### Hybrid Approaches
You can consider a combination of the above approaches to suit different tenants' requirements and your pricing model. 
For example:
* Provision all free trial customers within a shared container, and use the tenant ID or a synthetic key partition key.
* Offer a higher Silver tier that provisions dedicated throughput for the tenant's container.
* Offer the highest Gold tier, and provide a dedicated database account for the tenant, which also allows tenants to 
select the geography for their deployment.

#### Partitioning Key Design

To store multi-tenant data in a single container, Azure Cosmos DB provides **partition key** to distribute the data into logical
partitions. By using tenantId as the partition key, Cosmos DB keeps the data for each tenant in one logical partition and will 
perform faster queries with low cost. 

Partition Key plays a major role to save costs and to provide sub millisecond response time. Make sure to keep the partition key 
as part of most frequent queries. Cosmos DB also provides Document Type to keep relevant data in one container. 


#### 3.4 Load Business data into containers

Download the Workshop Data zip file (Multi-Tenant_CosmosDB_Workshop_data.zip) from the provided github link data folder. 
Unzip the file into your local folder and you should see the following files.

<img src="./images/MultiTenant_dataFile_list_3d.jpg" alt="list of multi-tenant reservation and availability data" width="600" >


Multi-Tenant databases have unique set of data per each tenant in our use case number of rooms, availability and reservations. It 
would make sense to create TenantID as the partition key and collect room availability and reservation info using document type.

You can also keep reference data such as Guest info and room type definitions in the same container. 

##### 3.4.1 Load Room Availability and Reservation data into **CasinoHotel** Container. 
* Expand **Casino Hotels** container under **SharedThroughputDB** database
* select **items** section
* Select **upload** to load the data files from the local foldder.
* Select **CasinoHotel_RoomInventory.json** file from the local folder.
* Select Open
* Click **Upload** button.
<img src="./images/UploadMultiTenantData_3d.jpg" alt="Load Data into Casion Hotel Container" width="800" >

* Load Reservation data into the same container by selecting **CasinoHotel_Reservation.json** file.

##### 3.4.2 Load Room Availability and Reservation data into **FamilyFunHotel** Container. 
* Follow the above steps to load the data.

##### 3.4.3 Load Room Availability and Reservation data into **HikingHotel** Container. 
* Follow the above steps to load the data.

##### 3.4.4 Load Room Availability and Reservation data into **GoodFellasHotel** Container. 
* Follow the above steps to load the data.


#### 3.5 Query Data using Data Explorer

You can query data using APIs and also can use Data Explorer for quick check.

* Select **CasinoHotel** container.
* Open Query window by selecting 'Folder with Search' icon from the top bar.
* Type the following Query 

``` SELECT count(1) FROM c where c.type='Reservation' ```

* Select 'Execute Selection' from the top bar to execute the query
* Results tab will be display the results on the bottom.
* Query Stats next to results tab will show RU cost, size of the document and Query Execution time.
<img src="./images/cosmosdb-query-execution-3d.jpg" alt="Query data using Data Explorer" width="600" >

The above query will result in a cross partition query 
Next try the query below

``` SELECT count(1) FROM c where c.type='Reservation' and c.tenantId=1001  ```

In the Query Stats next to results tab will you will notice that RU usage is significantly lower than the query above.

CosmosDB supports built in functions and JSON projection within the queries, Lets project a new JSON object using the query below

```    select { "Customer Name":CONCAT(c.cust.firstName," ",c.cust.lastName), "Room Rate": c.roomRate} as customerrate from c where c.type='Reservation' and  c.tenantId=1001 order by c.roomRate desc  ```


#### 3.6 Using indexes in ComsosDB

CosmosDB uses Indexes to further accelerate query response times. Each time an Item is stored in a container, CosmosDb indexes all properties by default. Users can manage indexes to effectively index only those properties that are helpful for their query scenarios. This can lead to optmized RU consumption. CosmosDB allows properties to be referenced by their paths. 
Start with clicking on the "Scale & Settings" link and then the "Indexing Policy" as shown below:

<img src="./images/cosmosdb-default-indexes.jpg" alt="Modify index policy using Data Explorer" width="600" >

By default you will notice that all properties are indexed and only the etag is excluded

```yaml
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
    ]
}
```

You can overwrite the default index policy to customize it for any range, composite or particular filters that your queries would need. Copy the below index policy and replace the default and Save.

```json
{
    "indexingMode": "consistent",
    "automatic": true,
    "includedPaths": [
        {
            "path": "/bizId/"
        },
         {
            "path": "/type/"
        }
    ],
    "excludedPaths": [
        {
            "path": "/*"
        }
    ],
    "compositeIndexes": [
    [
      {
        "path": "/bookedDate",
        "order": "ascending"
      },
      {
        "path": "/roomRate",
        "order": "descending"
      }
    ]
    ]
}
```
The query below will not use the customized Index policy

```    select { "Customer Name":CONCAT(c.cust.firstName," ",c.cust.lastName), "Room Rate": c.roomRate} as customerrate from c where c.type='Reservation' and  c.tenantId=1001 order by c.roomRate desc  ```

With this challenge you have gained a hands-on experience to create multi-tenant Cosmos DB database to support small, medium 
and large customers. Congratulations!!


## Challenge-4: Validate Cosmos DB features Auto failover, Autoscale and Low latency


### 4.1 High Availability Features:
Azure Cosmos DB is designed to provide multiple features and configuration options to achieve high availability to satisfy 
the mission critical enterprise application's requirement.

### Replica Outages
Replica outages refer to outages of individual nodes in an Azure Cosmos DB cluster deployed in an 
Azure region. Azure Cosmos DB automatically mitigates replica outages by guaranteeing at least three replicas of your 
data in each Azure region for your account within a four replica quorum.

### Zone Outages
In many Azure regions, it is possible to distribute your Azure Cosmos DB cluster across 
availability zones, which results increased SLAs, as availability zones are physically separate and provide 
distinct power source, network, and cooling. See Availability Zones. When an Azure Cosmos DB account is 
deployed using availability zones, Azure Cosmos DB provides RTO = 0 and RPO = 0 even with a zone outage.

Select 'Replicate data globally' under 'Settings' section in the left pane. It show all the available regions 
for Cosmos DB deployment. Availability Zone option for the write region can be enabled at the time of account creation.

select "+ Add region" to add a read region. Check the box for 'Availability Zone'. **No save action needed for this lab.**

<img src="./images/Deploy_CosmosDBMultTenant_Lab_CosmosDB_add_region_save.jpg" alt="Region availability zones" width="800">

### Region Outages
Region outages refer to the outages that affect all Azure Cosmos DB nodes in an Azure region, across all availability 
zones. In the rare cases of region outages, Azure Cosmos DB can be configured to support various outcomes of 
durability and availability

#### Durability: 
To protect against complete data loss that may result from catastrophic disasters in a region, Azure 
Cosmos DB provides continuous and periodic backup modes.  

#### Service-Managed failover: 
It allows Azure Cosmos DB to fail over the write region of multi-region account. Region 
failovers are detected and handled by Azure and do not require any changes from the application.

Select "Service-Managed Failover" option to failover the database to read region at the time of region outage.

<img src="./images/Cosmosdb_feature_Automatic_Failover.jpg" alt="Auto failover feature" width="800">

Select the "On" button under "Enable Service-Managed Failover".

<img src="./images/CosmosDB_feature_Service_Managed_Failover_TurnOn.jpg" alt="Auto failover feature" width="800" height="500">

**No action is needed for this lab.** It will take time to enable the failover option.


### 4.2 Autoscale for scalability
It allows you to scale the throughput (RU/s) of your database or container automatically and instantly. 
The throughput is scaled based on the usage, without impacting the availability, latency, throughput, or 
performance of the workload.

Autoscale provisioned throughput is well suited for mission-critical workloads that have variable or unpredictable 
traffic patterns, and require SLAs on high performance and scale.

Select 'Data Explorer' from the left pane and expand 'DedicatedThroughputDB' database. 

Expand **GoodFellasHotel** container.
Select **Scale & Settings** setting.

Change Max RU/s back to '2000' and select **save** button on the top bar. 

It will change the throughput instantly without impacting the current workloads.

<img src="./images/DedicatedThroughputDB_3d.jpg" atl="dedicated database for large customers" width="800">


### Sub Millisecond Fast Response Time
Select 'Data Explorer' from the left pane and expand 'SharedThroughputDB' database.
Hover over 'CasinoHotel' container and select three dots.
It provide options to create SQL Query, Stored Procedure, UDF & Trigers. Select the 'New SQL Query' option. 

<img src="./images/cosmosdb-query-execution-3d.jpg" alt="Query data using Data Explorer" width="600" >

Type the following Query:

```
SELECT * FROM c where c.type='Reservation' 
```

select "Query Stats" tab and check the Query execution time. It shows the sub millisecond response time.


## Challenge-5: Build an application using Azure Cosmos DB at no cost  
Cosmos DB is a developer friendly database and supports SaaS applications with no schema and indexing to manage. 
It also provides built in Cache for improved performance. It provides Cosmos DB Emulator tool to build your 
applications using Cosmos DB in your development environment with no cost.

### Quick Start
You can test building an application from Cosmos DB service portal itself. Select 'Quick start' from the left panel.
It will you programming language options .NET, Xamarin, Java, Node.js & Python to choose.

Use the default .NET option.

5.1 Select create 'Items' container button.

It creates an **Items** container in "ToDoList" database with 400 RU throughput capacity.

<img src="./images/CosmosDB_QuickStart_AddContainer_Marked.jpg" alt="Quick Start Create Container" width="600">

5.2 Select Download button to download .NET app to your laptop.

<img src="./images/CosmosDB_QuickStart_Download_App_Marked.jpg" alt="Download .NET app button" width="600">

5.3 Extract all from 'DocumentDB-Quickstart-DotNet.zip' file and open "CosmosGettingStarted.sln" in sql-dotnot folder 
with Visual Studio 2022.

<img src="./images/cosmosdb_dotnet_downloadzip_marked.jpg" alt="Download ZIP and open Visual Studio" width="600">

5.4 Clean and rebuild the solution.

5.5 Put a breakpoint in **GetStartedDemoAsync** method at  

```
this.ReplaceFamilyItemAsync();
``` 

<img src="./images/cosmosdb_dotnet_app_breakpoint_marked.jpg" alt="create a breakpoint" width="800">

5.6 run the debug program by selecting green start button.

<img src="./images/cosmosdb_dotnet_app_exec_output.jpg" alt="create a breakpoint" width="600">

This application creates documents in the Cosmos DB Items container and stops at the breakpoint.

5.7 Go back to Cosmos DB in Azure Portal and verify the data the application has created.

<img src="./images/CosmosDB_QuickStart_Create_Items_Marked.jpg" alt="create a breakpoint" width="800">

5.8 Come back to Visual Studio and continue the execution by selecting 'Continue' button.
It will delete all the items it created in the Cosmos DB database.

5.9 Go back to Cosmos DB in Azure Portal and verify if the application has deleted the database, container
and items.

You are successfully built an application to access Cosmos DB Service and to create database, container and 
populate with items. Congratulations!!.


### Azure Cosmos DB Emulator
The Azure Cosmos DB Emulator provides a local environment that emulates the Azure Cosmos DB service for development purposes. 
Using the Azure Cosmos DB Emulator, you can develop and test your application locally, without creating an Azure subscription 
or incurring any costs. When you're satisfied with how your application is working in the Azure Cosmos DB Emulator, you can 
switch to using an Azure Cosmos DB account in the cloud.

#### Requirements to install:
* Currently Windows Server 2016, 2019 or Windows 10 host OS are supported. The host OS with Active 
Directory enabled is currently not supported.
* 64-bit operating system
* 2-GB RAM
* 10-GB available hard disk space
* administrative privileges on the computer. The emulator will add a certificate and also set the firewall 
rules in order to run its services. Therefore admin rights are necessary for the emulator to be able to 
execute such operations.	

Access [Azure Cosmos DB Emulator for local development and testing](https://learn.microsoft.com/en-us/azure/cosmos-db/local-emulator?tabs=ssl-netstd21#how-does-the-emulator-work) 
for more details.

5.10 Download Azure Cosmos DB Emulator

[download](https://aka.ms/cosmosdb-emulator) and install the latest version of Azure Cosmos DB Emulator 
on your local computer. 

You will download azure-cosmosdb-emulator-2.14.9-3c8bff92.msi file to your local environment.

Run a DOS window as an **administrator** and run the install by entering the full file name at the prompt.

<img src="./images/cosmos_emulator_install_admin_window_Marked.jpg" alt="Emulator install in admin window" width="600">


5.11 Installer launches the emulator in a browser with the following screen.

<img src="./images/CosmosDB_Emulater_Start_Screen_Marked.jpg" alt="Emulator start screen" width="800">

5.12 Copy the **URI** and **Primary key** to a notepad.

5.13 Open up Visual Studio Quick Start application and use the Solution Explorer to navigate to **App.config**.
update **EndpointUri** and **PrimaryKey** which you copied from Cosmos DB Emulator.

<img src="./images/cosmos_vs_app_config_change_Marked.jpg" alt="Visual Studio Config Change" width="800">

5.14 Execute the application from Visual Studio with a breakpoint

5.15 Verify the data using the **Explorer** in the local Cosmos DB emulator tool

<img src="./images/CosmosDB_Emulator_CreateItem_Marked.jpg" alt="Verify data in local Emulator tool" width="600">

5.16 You can also run SQL queries to analyze the data using the **SQL Query window** similar to the tool you used 
with Azure Cosmos DB Service. 

**This is the best way to estimate your query costs and optimize your queries to save costs.** 

<img src="./images/CosmosDB_Emulator_RunQuery_Marked.jpg" alt="Run SQL Query using emulator" width="600">

You have built your local environment to build applications on Cosmos DB with no costs till you are ready to 
deploy to Azure. Congratulations!!

This workshop provided you a hands-on experience to model data in Cosmos DB and optimize the throughput for small, medium and 
enterprise customers. Also gave an experience to build applications using Cosmos DB in your development 
environment with no cost. 

Please send your feedback and suggestions to us!!

## Challenge-6: Implement AI-Enhanced Features

Azure Cosmos DB has evolved to become the **database for the AI era**, offering cutting-edge capabilities that integrate artificial intelligence directly into your database operations. This challenge will guide you through implementing the latest AI-enhanced features.

### 6.1 Vector Database Integration for AI Applications

Azure Cosmos DB for NoSQL now includes native vector database capabilities, allowing you to store vector embeddings alongside your operational data for AI-powered applications like recommendation engines, similarity search, and Retrieval Augmented Generation (RAG).

#### 6.1.1 Enable Vector Search in Your Container

1. Navigate to your **SharedThroughputDB** database in Data Explorer
2. Select **CasinoHotel** container
3. Select **Scale & Settings**
4. In the **Indexing Policy** section, add vector indexing configuration:

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

#### 6.1.2 Add Sample Vector Data

Create a new document with vector embeddings in your container:

```json
{
    "id": "vector-search-sample",
    "tenantId": 1001,
    "type": "AIRecommendation",
    "description": "Luxury suite recommendation based on customer preferences",
    "vectorProperty": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
    "metadata": {
        "roomType": "Suite",
        "amenities": ["spa", "ocean-view", "balcony"],
        "priceRange": "premium"
    }
}
```

#### 6.1.3 Perform Vector Similarity Search

Use the new `VectorDistance` function to find similar items:

```sql
SELECT c.id, c.description, VectorDistance(c.vectorProperty, [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]) AS similarity
FROM c
WHERE c.type = 'AIRecommendation' 
ORDER BY VectorDistance(c.vectorProperty, [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
```

### 6.2 Query Copilot - Natural Language to NoSQL

Microsoft Copilot for Azure in Cosmos DB (Preview) allows you to generate NoSQL queries using natural language prompts.

#### 6.2.1 Enable Query Copilot

1. Ensure your Azure subscription is enrolled in the **Microsoft Copilot for Azure in Cosmos DB preview**
2. Navigate to **Data Explorer** in your Cosmos DB account
3. Look for the **Query faster with Copilot** card
4. Click **Enable Copilot** button in the Data Explorer menu

#### 6.2.2 Try Natural Language Queries

Test these natural language prompts in the Copilot interface:

- "Show me all hotel reservations for tenant 1001"
- "Find rooms with rates above $200 per night"
- "Count reservations by room type"
- "Show available rooms for luxury hotels between specific dates"

#### 6.2.3 Review Generated Queries

Copilot will generate NoSQL queries and provide explanations. For example:
- **Prompt**: "Show me all luxury suite reservations"
- **Generated Query**: 
```sql
SELECT * FROM c 
WHERE c.type = 'Reservation' 
AND CONTAINS(UPPER(c.roomType), 'SUITE')
```

### 6.3 Integrated Cache Implementation

The integrated cache provides in-memory caching to reduce costs for read-heavy workloads while maintaining low latency.

#### 6.3.1 Provision Dedicated Gateway

1. In your Cosmos DB account, navigate to **Settings** > **Dedicated Gateway**
2. Click **Create dedicated gateway**
3. Configure:
   - **SKU**: D4s (4 vCores, 16 GB RAM) - for production workloads
   - **Instance count**: 1 (can scale up based on needs)
4. Click **Create**

#### 6.3.2 Configure Integrated Cache Settings

1. After deployment, copy the **Dedicated Gateway Connection String**
2. Update your application connection to use the dedicated gateway
3. Configure `MaxIntegratedCacheStaleness` in your requests:

```csharp
// C# SDK Example
var requestOptions = new ItemRequestOptions
{
    ConsistencyLevel = ConsistencyLevel.Session,
    // Cache data for up to 30 seconds
    MaxIntegratedCacheStaleness = TimeSpan.FromSeconds(30)
};

var response = await container.ReadItemAsync<dynamic>("item-id", 
    new PartitionKey("partition-value"), requestOptions);
```

#### 6.3.3 Monitor Cache Performance

Track cache efficiency using Azure Monitor metrics:
- **IntegratedCacheItemHitRate**: Percentage of point reads served from cache
- **IntegratedCacheQueryHitRate**: Percentage of queries served from cache
- **DedicatedGatewayRequests**: Total requests through dedicated gateway

### 6.4 AI Advantage Program Benefits

Take advantage of Azure AI benefits:

1. **Free Tier**: 1000 RU/s and 25 GB storage permanently free
2. **Azure AI Advantage**: 40,000 RU/s for 90 days (up to $6,000 value) for Azure AI customers
3. **30-day Free Trial**: No Azure subscription required

#### 6.4.1 Apply for Azure AI Advantage

1. Visit [Azure AI Advantage](https://learn.microsoft.com/en-us/azure/cosmos-db/ai-advantage)
2. Verify eligibility (Azure AI or GitHub Copilot customers)
3. Apply the credits to your Cosmos DB account

### 6.5 Build a Simple RAG (Retrieval Augmented Generation) Pattern

Implement a basic RAG pattern using the new features:

1. **Store embeddings** alongside hotel data in Cosmos DB
2. **Use vector search** to find relevant hotel information
3. **Apply integrated cache** for frequently accessed embeddings
4. **Use Query Copilot** to explore data with natural language

#### 6.5.1 Sample RAG Implementation Steps

1. Create embeddings for hotel descriptions using Azure OpenAI
2. Store embeddings in Cosmos DB with vector indexing
3. Implement similarity search for recommendations
4. Cache frequently accessed results using integrated cache
5. Use Query Copilot for dynamic data exploration

### 6.6 Cost Optimization with New Features

**Integrated Cache Benefits:**
- Zero RU consumption for cache hits
- Reduced costs for read-heavy workloads
- Automatic cache invalidation and LRU eviction

**Vector Search Benefits:**
- Single database for operational and AI data
- No need for separate vector databases
- Reduced data movement and consistency issues

**Query Copilot Benefits:**
- Faster query development
- Learning tool for NoSQL syntax
- Reduced development time

You have successfully implemented the latest AI-enhanced features in Azure Cosmos DB! These capabilities position your multi-tenant application to leverage modern AI workloads while maintaining the scalability and performance benefits of Cosmos DB.

**Congratulations on completing the enhanced workshop with cutting-edge AI features!**





