
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

class DwMysqlRepository:
    def __init__(self,session: AsyncSession):
        self.session = session
    async def get_column_values(self,table_name:str,column_name:str,limit:int=10):
        # distinct去重
        sql =f"select distinct {column_name} from {table_name} limit {limit}"
        result = await self.session.execute(text(sql))
        return result.scalars().fetchall()
    async def get_column_types(self,table_name:str):
        #MySQL 内置指令，专门查看表字段详情
        sql=f"show columns from {table_name}"
        result = await self.session.execute(text(sql))
        return {row.Field:row.Type for row in result.fetchall()}
    async def get_db_info(self):
        #查询数据库环境信息，版本、方言
        result=await self.session.execute(text("select version()"))
        version=result.scalar()
        dialect=self.session.get_bind().dialect.name
        return {"version":version,"dialect":dialect}

    async def validate_sql(self, sql:str):
        #用explain验证sql
        await self.session.execute(text(f"explain{sql}"))

    async def execute_sql(self,sql):
        #最终执行sql
        result = await self.session.execute(text(sql))
        return [dict(row) for row in result.mappings().fetchall()]

