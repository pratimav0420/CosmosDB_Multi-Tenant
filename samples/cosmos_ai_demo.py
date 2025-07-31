"""
Azure Cosmos DB AI Features Demo - Python Edition
Demonstrates the new AI-enhanced features in Azure Cosmos DB for NoSQL:
- Vector Search with DiskANN
- Integrated Cache with Dedicated Gateway
- RAG Pattern Implementation
- Query Copilot Integration Examples
"""

import asyncio
import json
import time
from typing import List, Dict, Any, Optional
import numpy as np
from azure.cosmos.aio import CosmosClient
from azure.cosmos import PartitionKey, exceptions

class CosmosAIFeaturesDemo:
    """
    Demonstrates Azure Cosmos DB AI features with Python SDK
    """
    
    def __init__(self, connection_string: str, database_name: str, container_name: str):
        """
        Initialize the demo with dedicated gateway connection for integrated cache
        """
        self.connection_string = connection_string
        self.database_name = database_name
        self.container_name = container_name
        self.client = None
        self.database = None
        self.container = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        # Use gateway mode for integrated cache support
        self.client = CosmosClient(self.connection_string, connection_mode="Gateway")
        self.database = self.client.get_database_client(self.database_name)
        self.container = self.database.get_container_client(self.container_name)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.client:
            await self.client.close()
    
    async def vector_similarity_search(self, query_vector: List[float], limit: int = 10) -> List[Dict]:
        """
        Perform vector similarity search using the VectorDistance function
        """
        try:
            # Convert vector to JSON string for the query
            vector_str = json.dumps(query_vector)
            
            # SQL query using VectorDistance function
            query = f"""
                SELECT c.id, c.description, c.metadata, c.type,
                       VectorDistance(c.vectorProperty, {vector_str}) AS similarity
                FROM c 
                WHERE c.type = 'AIRecommendation'
                ORDER BY VectorDistance(c.vectorProperty, {vector_str})
                OFFSET 0 LIMIT {limit}
            """
            
            print(f"Executing vector search query...")
            start_time = time.time()
            
            items = []
            async for item in self.container.query_items(query=query, enable_cross_partition_query=True):
                items.append(item)
            
            end_time = time.time()
            print(f"Vector search completed in {end_time - start_time:.2f} seconds")
            print(f"Found {len(items)} similar items")
            
            return items
            
        except exceptions.CosmosHttpResponseError as e:
            print(f"Vector search error: {e.message}")
            raise
    
    async def read_with_integrated_cache(self, item_id: str, partition_key: str, 
                                       cache_staleness_seconds: int = 30) -> Optional[Dict]:
        """
        Demonstrate integrated cache usage with custom staleness settings
        """
        try:
            print(f"Reading item {item_id} with {cache_staleness_seconds}s cache staleness...")
            
            # First read - likely from backend
            start_time = time.time()
            response = await self.container.read_item(
                item=item_id, 
                partition_key=partition_key
            )
            first_read_time = time.time() - start_time
            first_ru = response.get('_charge', 0) if hasattr(response, 'response_headers') else 'unknown'
            
            print(f"First read: {first_read_time:.3f}s, RU charge: {first_ru}")
            
            # Second read - should hit cache (0 RU charge)
            start_time = time.time()
            response = await self.container.read_item(
                item=item_id, 
                partition_key=partition_key
            )
            second_read_time = time.time() - start_time
            second_ru = response.get('_charge', 0) if hasattr(response, 'response_headers') else 'unknown'
            
            print(f"Second read: {second_read_time:.3f}s, RU charge: {second_ru}")
            print(f"Cache hit detected: {second_ru == 0}")
            
            return response
            
        except exceptions.CosmosResourceNotFoundError:
            print(f"Item {item_id} not found")
            return None
        except exceptions.CosmosHttpResponseError as e:
            print(f"Cache read error: {e.message}")
            raise
    
    async def bulk_insert_ai_data(self, ai_data_items: List[Dict]) -> None:
        """
        Bulk insert AI-enhanced data items
        """
        try:
            print(f"Starting bulk insert of {len(ai_data_items)} AI data items...")
            
            # Use asyncio for concurrent operations
            tasks = []
            for item in ai_data_items:
                task = self.container.create_item(body=item)
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            success_count = sum(1 for result in results if not isinstance(result, Exception))
            error_count = len(results) - success_count
            
            print(f"Bulk insert completed: {success_count} successful, {error_count} errors")
            
        except Exception as e:
            print(f"Bulk insert error: {str(e)}")
            raise
    
    async def ai_analytics_query(self, tenant_id: int) -> List[Dict]:
        """
        Perform analytics queries on AI data with caching
        """
        try:
            query = """
                SELECT 
                    c.type,
                    COUNT(1) as itemCount,
                    AVG(c.recommendations.aiScore) as avgAIScore,
                    MAX(c.recommendations.aiScore) as maxAIScore
                FROM c 
                WHERE c.tenantId = @tenantId 
                AND c.type IN ('AIRecommendation', 'CustomerFeedback', 'PricingModel')
                GROUP BY c.type
            """
            
            parameters = [{"name": "@tenantId", "value": tenant_id}]
            
            print(f"Executing AI analytics query for tenant {tenant_id}...")
            
            items = []
            async for item in self.container.query_items(
                query=query, 
                parameters=parameters,
                enable_cross_partition_query=True
            ):
                items.append(item)
            
            print(f"AI analytics completed. Found {len(items)} aggregated results.")
            return items
            
        except exceptions.CosmosHttpResponseError as e:
            print(f"AI analytics error: {e.message}")
            raise
    
    async def semantic_search_simulation(self, search_query: str) -> List[Dict]:
        """
        Simulate semantic search using vector embeddings
        In production, you would:
        1. Use Azure OpenAI to convert search_query to vector embedding
        2. Perform vector similarity search
        """
        print(f"Performing semantic search for: '{search_query}'")
        
        # Simulate query embedding (in production, use Azure OpenAI Embeddings API)
        if "luxury" in search_query.lower():
            query_vector = [0.8, 0.9, 0.7, 0.6, 0.8, 0.9, 0.7, 0.8, 0.6, 0.9, 0.8, 0.7, 0.9, 0.8, 0.6, 0.7]
        elif "business" in search_query.lower():
            query_vector = [0.7, 0.8, 0.9, 0.8, 0.7, 0.6, 0.8, 0.9, 0.7, 0.8, 0.6, 0.9, 0.8, 0.7, 0.9, 0.8]
        else:
            query_vector = [0.5, 0.6, 0.7, 0.8, 0.6, 0.7, 0.5, 0.8, 0.9, 0.6, 0.7, 0.8, 0.5, 0.9, 0.6, 0.7]
        
        return await self.vector_similarity_search(query_vector, limit=5)
    
    async def query_copilot_examples(self) -> None:
        """
        Demonstrate query patterns that would benefit from Query Copilot
        These are examples of natural language prompts that Copilot can convert to NoSQL
        """
        copilot_examples = [
            {
                "natural_language": "Show me all hotel reservations for tenant 1001",
                "generated_query": "SELECT * FROM c WHERE c.type = 'Reservation' AND c.tenantId = 1001"
            },
            {
                "natural_language": "Find luxury rooms with rates above $300 per night",
                "generated_query": "SELECT * FROM c WHERE c.type = 'Reservation' AND c.roomRate > 300 AND CONTAINS(UPPER(c.roomType), 'LUXURY')"
            },
            {
                "natural_language": "Count AI recommendations by tenant",
                "generated_query": "SELECT c.tenantId, COUNT(1) as recommendationCount FROM c WHERE c.type = 'AIRecommendation' GROUP BY c.tenantId"
            },
            {
                "natural_language": "Show customer feedback with high sentiment scores",
                "generated_query": "SELECT * FROM c WHERE c.type = 'CustomerFeedback' AND c.sentiment.score > 0.8 ORDER BY c.sentiment.score DESC"
            }
        ]
        
        print("\n=== Query Copilot Examples ===")
        print("These natural language prompts can be converted to NoSQL queries using Query Copilot:")
        
        for i, example in enumerate(copilot_examples, 1):
            print(f"\n{i}. Natural Language: '{example['natural_language']}'")
            print(f"   Generated Query: {example['generated_query']}")
    
    async def rag_pattern_demo(self, user_question: str) -> Dict:
        """
        Demonstrate a simple RAG (Retrieval Augmented Generation) pattern
        """
        print(f"\n=== RAG Pattern Demo ===")
        print(f"User Question: {user_question}")
        
        # Step 1: Convert question to vector (simulated)
        question_vector = [0.6, 0.8, 0.7, 0.9, 0.6, 0.8, 0.7, 0.9, 0.8, 0.6, 0.7, 0.9, 0.8, 0.6, 0.7, 0.8]
        
        # Step 2: Retrieve relevant context using vector search
        relevant_docs = await self.vector_similarity_search(question_vector, limit=3)
        
        # Step 3: Combine context (would send to LLM in production)
        context = []
        for doc in relevant_docs:
            context.append({
                "description": doc.get("description", ""),
                "type": doc.get("type", ""),
                "similarity": doc.get("similarity", 0)
            })
        
        rag_result = {
            "user_question": user_question,
            "retrieved_context": context,
            "context_count": len(context),
            "note": "In production, this context would be sent to an LLM for answer generation"
        }
        
        print(f"Retrieved {len(context)} relevant documents for context")
        return rag_result

# Sample AI data for demonstration
SAMPLE_AI_DATA = [
    {
        "id": "ai-demo-1",
        "tenantId": 1001,
        "type": "AIRecommendation", 
        "description": "Luxury oceanfront suite with premium amenities",
        "vectorProperty": [0.8, 0.9, 0.7, 0.6, 0.8, 0.9, 0.7, 0.8, 0.6, 0.9, 0.8, 0.7, 0.9, 0.8, 0.6, 0.7],
        "metadata": {
            "roomType": "Oceanfront Suite",
            "amenities": ["spa", "ocean-view", "balcony"],
            "priceRange": "luxury"
        },
        "recommendations": {
            "targetCustomers": ["luxury-seekers", "romantic-getaway"],
            "aiScore": 0.92
        }
    },
    {
        "id": "ai-demo-2", 
        "tenantId": 1001,
        "type": "CustomerFeedback",
        "description": "Excellent service and beautiful views!",
        "vectorProperty": [0.9, 0.8, 0.9, 0.7, 0.8, 0.9, 0.8, 0.7, 0.9, 0.8, 0.9, 0.8, 0.7, 0.9, 0.8, 0.9],
        "sentiment": {
            "score": 0.95,
            "category": "positive"
        }
    }
]

async def main():
    """
    Main demo function showcasing AI features
    """
    # Replace with your dedicated gateway connection string
    connection_string = "YOUR_DEDICATED_GATEWAY_CONNECTION_STRING"
    database_name = "SharedThroughputDB"
    container_name = "CasinoHotel"
    
    print("=== Azure Cosmos DB AI Features Demo (Python) ===")
    
    async with CosmosAIFeaturesDemo(connection_string, database_name, container_name) as demo:
        try:
            # Demo 1: Vector Similarity Search
            print("\n1. Vector Similarity Search Demo")
            query_vector = [0.8, 0.9, 0.7, 0.6, 0.8, 0.9, 0.7, 0.8, 0.6, 0.9, 0.8, 0.7, 0.9, 0.8, 0.6, 0.7]
            similar_items = await demo.vector_similarity_search(query_vector)
            print(f"Found {len(similar_items)} similar items")
            
            # Demo 2: Integrated Cache
            print("\n2. Integrated Cache Demo")
            # This will show performance difference between cached and non-cached reads
            if similar_items:
                sample_id = similar_items[0]["id"]
                sample_partition = str(similar_items[0]["tenantId"])
                await demo.read_with_integrated_cache(sample_id, sample_partition)
            
            # Demo 3: AI Analytics
            print("\n3. AI Analytics Demo")
            analytics = await demo.ai_analytics_query(1001)
            for analytic in analytics:
                print(f"Type: {analytic.get('type')}, Count: {analytic.get('itemCount')}")
            
            # Demo 4: Semantic Search Simulation
            print("\n4. Semantic Search Demo")
            semantic_results = await demo.semantic_search_simulation("luxury oceanfront suite")
            print(f"Semantic search returned {len(semantic_results)} results")
            
            # Demo 5: Query Copilot Examples
            await demo.query_copilot_examples()
            
            # Demo 6: RAG Pattern
            print("\n5. RAG Pattern Demo")
            rag_result = await demo.rag_pattern_demo("What are the best luxury rooms available?")
            print(f"RAG pattern retrieved {rag_result['context_count']} relevant documents")
            
            # Demo 7: Bulk Insert (optional - comment out if you don't want to insert data)
            print("\n6. Bulk Insert AI Data Demo")
            # await demo.bulk_insert_ai_data(SAMPLE_AI_DATA)
            print("Bulk insert demo skipped (uncomment to run)")
            
            print("\n=== Demo completed successfully! ===")
            print("\nNext Steps:")
            print("1. Enable Query Copilot in Azure Portal")
            print("2. Set up dedicated gateway for integrated cache")
            print("3. Implement vector embeddings with Azure OpenAI")
            print("4. Build RAG applications with retrieved context")
            
        except Exception as e:
            print(f"Demo error: {str(e)}")
            print("Make sure to:")
            print("1. Use the dedicated gateway connection string")
            print("2. Enable vector search on your container")
            print("3. Have appropriate data in your container")

if __name__ == "__main__":
    asyncio.run(main())
