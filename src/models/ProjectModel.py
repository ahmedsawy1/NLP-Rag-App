from .BaseDataModel import BaseDataModel
from .db_schemas import Project
from .enum.DataBaseEnum import DataBaseEnum

class ProjectBaseModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client(DataBaseEnum.COLLECTION_PROJECT_NAME.value)

    async def create_project(self, project: Project):
        result = await self.collection.insert_one(project.dict())
        project._id = result.inserted_id

        return project    

    async def get_project_or_create_one(self, project_id: str):

        record = await self.collection.find_one({
            "project_id": project_id
        })

        if record is None:
            # Create new project
            project = Project(project_id=project_id)
            project = await self.create_project(project=project)
            
            return project
        
        return Project(**record)

    async def get_all_projects(self, page: int=1, page_size: int=10):
        # Total Docs
        total_documents = await self.collection.count_documents({})
        
        # calc total number of pages
        total_pages = total_documents 
        if total_documents % page_size > 0:
            total_pages += 1
