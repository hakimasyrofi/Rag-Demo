# Refactoring Notes

I refactored the monolithic `main.py` into a layered architecture to improve separation of concerns and scalability. The application is now split into distinct layers: `controllers` handle HTTP requests and validation, `services` encapsulate business logic, and `routes` define the API structure. This modular design ensures that each component has a well-defined responsibility, preventing the "god object" anti-pattern found in the legacy code.

One trade-off considered was the increased boilerplate and complexity of managing multiple files compared to the simplicity of a single script. While the single-file approach is faster for prototyping, I prioritized a structure that supports future growth. This decision accepts slightly more initial friction in navigation in exchange for a cleaner, more organized codebase that is less prone to regression during updates.

This version significantly improves maintainability by isolating dependencies and side effects. For instance, the `StorageService` now abstracts the database logic, meaning the rest of the application doesn't need to know whether it's using Qdrant or in-memory storage. This decoupling allows for independent unit testing of the RAG logic and the API layer, and makes it much safer to modify or swap out underlying technologies without breaking the entire application.
