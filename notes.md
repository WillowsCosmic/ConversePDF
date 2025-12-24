## Inngest Setup
- Uses PydanticSerializer for type safety
- is_production=False enables local development server
- Need to run Inngest dev server separately: `npx inngest-cli@latest dev`


## To run Qdrant through docker(create an image)
- docker run -d --name qdrant -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant

### If in Ubuntu or other Linux distros to check the initialization
    - docker ps (in terminal)
### If in windows
    - use Docker Desktop

### To Restart docker
    - docker start qdrant

Port for Qdrant: 6333
Port for Inngest: 8288
