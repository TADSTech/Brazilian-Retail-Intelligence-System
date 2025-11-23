Finally wrapped up the Brazilian Retail Intelligence System. It’s been a while in the making.

It’s essentially an end-to-end data engineering project. I wanted to build something that handles the full lifecycle of retail data—from raw CSVs to a dashboard you can actually look at.

Under the hood, it’s running FastAPI and Supabase. There’s an ETL pipeline that processes the Olist dataset, and I added a synthetic data generator that uses Markov chains to create fake orders and reviews. It keeps the dashboard alive even when the static data runs out.

The frontend is React. It visualizes the metrics—revenue, delivery times, that sort of thing.

It’s not revolutionary, but it’s a solid, working system that demonstrates how these pieces fit together in a production-like environment. Dockerized, deployed, and running.

If you’re interested in data engineering or full-stack analytics, the code is up on GitHub.

https://github.com/TADSTech/Brazilian-Retail-Intelligence-System
