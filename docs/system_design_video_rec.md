# 🎥 System Design: Scalable Video Recommendation System (The "Cinema Theater" Architecture)

**Goal:** Design a system like YouTube/Netflix for **100 Million Users**.
**Constraint:** Low Latency (<200ms), High Throughput, Real-time updates.

---

## 🎬 The "Mass" Analogy: The Multiplex (Cinema Hall)

Imagine we are running a massive Multiplex (like AMB Cinemas in Hyderabad) with 100 Million people waiting to watch movies.

### 1. The Users (Audience) 👨‍👩‍👧‍👦
- **Who:** 100M people.
- **Action:** They open the app (enter the theater lobby).
- **Data:** Watch history, likes, search (their ticket stubs and popcorn choices).

### 2. The Ingestion Layer (The Ticket Counter & Canteen) 🎟️🍿
- **Component:** **Cloud Pub/Sub**
- **Role:** High-speed data collection.
- **Analogy:** Thousands of ticket counters and popcorn stands. Every time someone buys a ticket (clicks a video) or buys popcorn (likes a video), a slip is sent to the manager instantly.
- **Why?** We can't write to the main database 100M times a second. Pub/Sub buffers the "noise" and sends it in orderly lines.

### 3. The Processing Layer ( The Manager's Cabin) 🧠
- **Component:** **Cloud Dataflow (Apache Beam)**
- **Role:** Real-time stream processing.
- **Analogy:** The Manager who sorts the slips.
    - "Orey, Balayya fans ekkuva unnaru, Balayya movie reel ready cheyandi." (Trend detection)
    - "Veedu comedy movies eh chustunnadu." (User profiling)
- **Why?** Raw data is messy. We need to clean it and aggregate it (e.g., "User A watched 50% of Movie B").

### 4. The Storage Layer (The Godown) 📦
- **Component:** **Cloud Bigtable**
- **Role:** High-throughput, low-latency storage for user history.
- **Analogy:** A massive, organized warehouse where we store every user's entire history.
    - **Row Key:** `UserID#Timestamp`
    - **Speed:** Instant retrieval. "Show me Krishna's last 10 movies." -> BAM! Done.
- **Why?** SQL (MySQL/Postgres) will choke with 100M users. Bigtable is a NoSQL beast designed for this.

### 5. The Brain (The Projector & Reels) 📽️
- **Component:** **Vertex AI Vector Search (Two-Tower Model)**
- **Role:** Retrieval and Ranking.
- **Analogy:**
    - **Candidate Generation (The Projector):** Out of 1 Million movies, pick the top 500 broadly relevant ones (e.g., "Action Movies").
        - *Tech:* Approximate Nearest Neighbor (ANN) search.
    - **Ranking (The Focus Adjustment):** Out of those 500, pick the top 10 *specifically* for Krishna.
        - *Tech:* Fine-tuned ranking model (XGBoost or Deep Learning).
- **Why?** We can't score 1M movies for every user every time. We filter (retrieve) then focus (rank).

### 6. The Serving Layer (The Screen) 📺
- **Component:** **Cloud Run (Microservices)**
- **Role:** API to serve the list to the app.
- **Analogy:** The screen showing the movie list.
- **Why?** Auto-scales. If 10M people open the app at 8 PM, Cloud Run spins up more servers instantly.

---

## 🛠️ The "Tech Stack" Summary (Interview Cheat Sheet)

| Feature | GCP Component | Why? (The "Punch Dialogue") |
| :--- | :--- | :--- |
| **Ingestion** | **Pub/Sub** | "Traffic jam avvakunda line lo pampistadi." (Async, Scalable) |
| **Processing** | **Dataflow** | "Live lo lekkalu vestadi." (Real-time aggregation) |
| **User DB** | **Bigtable** | "Laksha mandhi vachina 'load' anadu." (High write throughput) |
| **Metadata DB** | **Cloud Spanner** | "Global ga consistency maintain chestadi." (For video details, payments) |
| **ML Model** | **Vertex AI** | "Brain of the operation." (Vector Search + Ranking) |
| **Caching** | **Memorystore (Redis)** | "Fast ga serve chestadi." (Sub-millisecond access for top lists) |

---

## 🧪 Interview Q&A (Be Ready!)

**Q: Why Bigtable and not BigQuery?**
**A:** "Sir, BigQuery is for *Analytics* (OLAP) - like generating a monthly report. Bigtable is for *Real-time Access* (OLTP) - like serving the 'Continue Watching' list instantly. We need speed here, not complex SQL queries."

**Q: How do you handle the 'Cold Start' problem (New User)?**
**A:** "Simple strategy, sir.
1.  **Popularity based:** Show trending videos (General list).
2.  **Context based:** If they came from a 'Tech' link, show Tech videos.
3.  **Explore/Exploit:** Mix in random diverse content to see what they click."

**Q: How do you update recommendations in real-time?**
**A:** "That's where **Dataflow** shines. As soon as a user clicks, the event goes to Pub/Sub -> Dataflow updates the User Embedding -> Vertex AI Vector Search updates the index (Streaming Updates). The next refresh shows related content."
