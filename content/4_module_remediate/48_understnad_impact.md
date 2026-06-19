---
title: "Step 8: Understanding the Complete Impact"
weight: 68
---

Let's understand what the implemented caching solution will deliver:

### Performance Improvements:

**Before Caching:**
```
User Request → Vector Search (120ms) → LLM Generation (19.6s) → Response
              └─ Total: ~19.6 seconds for every request
```

**After Caching (Cache Hit - ~90% of requests):**
```
User Request → Cache Lookup (5ms) → Response from Cache (50ms)
              └─ Total: ~50ms (97% improvement!)
```

**After Caching (Cache Miss - ~10% of requests):**
```
User Request → Vector Search (120ms) → LLM Generation (19.6s) → Cache Store → Response
              └─ Total: ~19.6 seconds (same as before, but populates cache)
```

### What You'll See in Honeycomb:

1. **Query to verify caching is working:**
   ```
   Using Honeycomb, show me cache hit rates by layer for the otel-ai-chatbot-backend dataset
   ```

   Expected result after deployment:
   ```
   Cache Statistics (after 24 hours):
   - Response Cache Hit Rate: 85-90%
   - Vector Search Cache Hit Rate: 88-92%
   - Embedding Cache Hit Rate: 95-98%
   - Average Response Time (cached): 45-60ms
   - Average Response Time (uncached): 18-20s
   - Bedrock API Call Reduction: 70%
   ```

2. **New OpenTelemetry metrics tracked:**
   ```
   - cache.hit (counter by layer)
   - cache.miss (counter by layer)
   - cache.latency (histogram)
   - cache.value_size (histogram)
   - rag.cache_hit (boolean attribute)
   ```

3. **Cache Management Endpoints:**
   ```bash
   # Real-time cache statistics
   curl http://your-alb/api/cache/stats

   # Cache health check
   curl http://your-alb/api/cache/health

   # Manually warm cache with common questions
   curl -X POST http://your-alb/api/cache/warm \
     -H "Content-Type: application/json" \
     -d '{"maxQuestions": 20}'
   ```