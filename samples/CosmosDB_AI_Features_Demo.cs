using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.Azure.Cosmos;
using Newtonsoft.Json;

namespace CosmosDB_AI_Features_Demo
{
    /// <summary>
    /// Demonstrates the new AI-enhanced features in Azure Cosmos DB for NoSQL
    /// Including Vector Search, Integrated Cache, and modern querying capabilities
    /// </summary>
    public class CosmosAIFeaturesDemo
    {
        private readonly CosmosClient cosmosClient;
        private readonly Database database;
        private readonly Container container;

        public CosmosAIFeaturesDemo(string connectionString, string databaseName, string containerName)
        {
            // Use dedicated gateway connection string for integrated cache
            var cosmosClientOptions = new CosmosClientOptions()
            {
                ConnectionMode = ConnectionMode.Gateway, // Required for integrated cache
                ConsistencyLevel = ConsistencyLevel.Session,
                MaxRetryAttemptsOnRateLimitedRequests = 10,
                MaxRetryWaitTimeOnRateLimitedRequests = TimeSpan.FromSeconds(30)
            };

            cosmosClient = new CosmosClient(connectionString, cosmosClientOptions);
            database = cosmosClient.GetDatabase(databaseName);
            container = database.GetContainer(containerName);
        }

        /// <summary>
        /// Demonstrates vector similarity search for AI recommendations
        /// </summary>
        public async Task<List<dynamic>> PerformVectorSearchAsync(float[] queryVector)
        {
            var results = new List<dynamic>();

            try
            {
                // Use the new VectorDistance function for similarity search
                var queryText = $@"
                    SELECT c.id, c.description, c.metadata, 
                           VectorDistance(c.vectorProperty, {JsonConvert.SerializeObject(queryVector)}) AS similarity
                    FROM c 
                    WHERE c.type = 'AIRecommendation'
                    ORDER BY VectorDistance(c.vectorProperty, {JsonConvert.SerializeObject(queryVector)})
                    OFFSET 0 LIMIT 10";

                var queryDefinition = new QueryDefinition(queryText);
                var resultSetIterator = container.GetItemQueryIterator<dynamic>(queryDefinition);

                while (resultSetIterator.HasMoreResults)
                {
                    var response = await resultSetIterator.ReadNextAsync();
                    foreach (var item in response)
                    {
                        results.Add(item);
                    }
                }

                Console.WriteLine($"Vector search completed. Found {results.Count} similar items.");
                return results;
            }
            catch (CosmosException ex)
            {
                Console.WriteLine($"Vector search error: {ex.Message}");
                throw;
            }
        }

        /// <summary>
        /// Demonstrates integrated cache usage with custom staleness settings
        /// </summary>
        public async Task<T> ReadWithCacheAsync<T>(string itemId, string partitionKey, int cacheStalenesSeconds = 30)
        {
            try
            {
                var requestOptions = new ItemRequestOptions
                {
                    ConsistencyLevel = ConsistencyLevel.Session,
                    // Cache data for specified seconds
                    MaxIntegratedCacheStaleness = TimeSpan.FromSeconds(cacheStalenesSeconds)
                };

                var response = await container.ReadItemAsync<T>(itemId, new PartitionKey(partitionKey), requestOptions);
                
                Console.WriteLine($"Item read successfully. RU consumed: {response.RequestCharge}");
                Console.WriteLine($"Cache used: {response.RequestCharge == 0}");
                
                return response.Resource;
            }
            catch (CosmosException ex)
            {
                Console.WriteLine($"Cache read error: {ex.Message}");
                throw;
            }
        }

        /// <summary>
        /// Demonstrates bulk operations for AI data ingestion
        /// </summary>
        public async Task BulkInsertAIDataAsync(List<dynamic> aiDataItems)
        {
            try
            {
                var tasks = new List<Task>();

                foreach (var item in aiDataItems)
                {
                    tasks.Add(container.CreateItemAsync(item, new PartitionKey(item.tenantId.ToString())));
                }

                await Task.WhenAll(tasks);
                Console.WriteLine($"Bulk insert completed for {aiDataItems.Count} AI data items.");
            }
            catch (CosmosException ex)
            {
                Console.WriteLine($"Bulk insert error: {ex.Message}");
                throw;
            }
        }

        /// <summary>
        /// Demonstrates advanced querying for AI analytics
        /// </summary>
        public async Task<List<dynamic>> GetAIAnalyticsAsync(int tenantId)
        {
            var results = new List<dynamic>();

            try
            {
                var queryText = @"
                    SELECT 
                        c.type,
                        COUNT(1) as itemCount,
                        AVG(c.recommendations.aiScore) as avgAIScore,
                        MAX(c.recommendations.aiScore) as maxAIScore
                    FROM c 
                    WHERE c.tenantId = @tenantId 
                    AND c.type IN ('AIRecommendation', 'CustomerFeedback', 'PricingModel')
                    GROUP BY c.type";

                var queryDefinition = new QueryDefinition(queryText)
                    .WithParameter("@tenantId", tenantId);

                var requestOptions = new QueryRequestOptions
                {
                    MaxItemCount = 100,
                    // Use cache for analytics queries
                    MaxIntegratedCacheStaleness = TimeSpan.FromMinutes(5)
                };

                var resultSetIterator = container.GetItemQueryIterator<dynamic>(queryDefinition, requestOptions: requestOptions);

                while (resultSetIterator.HasMoreResults)
                {
                    var response = await resultSetIterator.ReadNextAsync();
                    foreach (var item in response)
                    {
                        results.Add(item);
                    }
                }

                Console.WriteLine($"AI analytics query completed. Found {results.Count} aggregated results.");
                return results;
            }
            catch (CosmosException ex)
            {
                Console.WriteLine($"AI analytics error: {ex.Message}");
                throw;
            }
        }

        /// <summary>
        /// Demonstrates change feed processing for real-time AI updates
        /// </summary>
        public async Task ProcessAIChangeFeedAsync()
        {
            try
            {
                var changeFeedProcessor = container
                    .GetChangeFeedProcessorBuilder<dynamic>("ai-processor", OnChangesDelegate)
                    .WithInstanceName("ai-instance")
                    .WithLeaseContainer(database.GetContainer("leases"))
                    .Build();

                await changeFeedProcessor.StartAsync();
                Console.WriteLine("AI change feed processor started.");

                // Run for demonstration (in production, this would run continuously)
                await Task.Delay(TimeSpan.FromMinutes(1));
                await changeFeedProcessor.StopAsync();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Change feed error: {ex.Message}");
                throw;
            }
        }

        private async Task OnChangesDelegate(ChangeFeedProcessorContext context, IReadOnlyCollection<dynamic> changes, CancellationToken cancellationToken)
        {
            foreach (var change in changes)
            {
                if (change.type == "AIRecommendation" || change.type == "CustomerFeedback")
                {
                    Console.WriteLine($"Processing AI change for item: {change.id}");
                    // Process AI-related changes here
                    // e.g., update recommendation models, trigger ML pipelines, etc.
                }
            }
        }

        /// <summary>
        /// Demonstrates semantic search using vector embeddings
        /// </summary>
        public async Task<List<dynamic>> SemanticSearchAsync(string searchQuery)
        {
            // In a real implementation, you would:
            // 1. Convert searchQuery to vector embedding using Azure OpenAI
            // 2. Use that vector for similarity search
            
            // For demo purposes, using a sample vector
            var sampleQueryVector = new float[] { 0.8f, 0.7f, 0.9f, 0.6f, 0.8f, 0.9f, 0.7f, 0.8f, 0.6f, 0.9f, 0.8f, 0.7f, 0.9f, 0.8f, 0.6f, 0.7f };
            
            Console.WriteLine($"Performing semantic search for: {searchQuery}");
            return await PerformVectorSearchAsync(sampleQueryVector);
        }

        public void Dispose()
        {
            cosmosClient?.Dispose();
        }
    }

    /// <summary>
    /// Sample AI data models for the workshop
    /// </summary>
    public class AIRecommendation
    {
        public string id { get; set; }
        public int tenantId { get; set; }
        public string type { get; set; } = "AIRecommendation";
        public string description { get; set; }
        public float[] vectorProperty { get; set; }
        public RecommendationMetadata metadata { get; set; }
        public RecommendationDetails recommendations { get; set; }
    }

    public class RecommendationMetadata
    {
        public string roomType { get; set; }
        public List<string> amenities { get; set; }
        public string priceRange { get; set; }
        public double rating { get; set; }
        public List<string> features { get; set; }
    }

    public class RecommendationDetails
    {
        public List<string> targetCustomers { get; set; }
        public List<string> similarRooms { get; set; }
        public double aiScore { get; set; }
    }

    /// <summary>
    /// Example usage of the AI features demo
    /// </summary>
    public class Program
    {
        public static async Task Main(string[] args)
        {
            // Replace with your dedicated gateway connection string
            var connectionString = "YOUR_DEDICATED_GATEWAY_CONNECTION_STRING";
            var databaseName = "SharedThroughputDB";
            var containerName = "CasinoHotel";

            var demo = new CosmosAIFeaturesDemo(connectionString, databaseName, containerName);

            try
            {
                Console.WriteLine("=== Azure Cosmos DB AI Features Demo ===");
                
                // Demonstrate vector search
                var queryVector = new float[] { 0.8f, 0.9f, 0.7f, 0.6f, 0.8f, 0.9f, 0.7f, 0.8f, 0.6f, 0.9f, 0.8f, 0.7f, 0.9f, 0.8f, 0.6f, 0.7f };
                var similarItems = await demo.PerformVectorSearchAsync(queryVector);
                Console.WriteLine($"Found {similarItems.Count} similar items using vector search.");

                // Demonstrate integrated cache
                Console.WriteLine("\n=== Testing Integrated Cache ===");
                var cachedItem = await demo.ReadWithCacheAsync<dynamic>("sample-id", "1001", 60);

                // Demonstrate semantic search
                Console.WriteLine("\n=== Semantic Search Demo ===");
                var semanticResults = await demo.SemanticSearchAsync("luxury oceanfront suite");
                Console.WriteLine($"Semantic search returned {semanticResults.Count} results.");

                // Demonstrate AI analytics
                Console.WriteLine("\n=== AI Analytics Demo ===");
                var analytics = await demo.GetAIAnalyticsAsync(1001);
                foreach (var analytic in analytics)
                {
                    Console.WriteLine($"Type: {analytic.type}, Count: {analytic.itemCount}, Avg AI Score: {analytic.avgAIScore}");
                }

                Console.WriteLine("\n=== Demo completed successfully! ===");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Demo error: {ex.Message}");
            }
            finally
            {
                demo.Dispose();
            }
        }
    }
}
