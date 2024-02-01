
import asyncpg

class Database():
    pool=None
    @classmethod
    async def init_db(clss):
        
        clss.pool =await asyncpg.create_pool('postgresql://postgres:1527@localhost/carental')
        
    @classmethod
    async def close_db(clss):
        await clss.pool.close()
        print("connection_close")
    async def fetch(self,stmt,*args):
        return await self.pool.fetch(stmt,*args)
    async def execute(self,stmt,*args):
        return await self.pool.execute(stmt,*args) 
    

class Database1():
    pool=None
    @classmethod
    async def init_db(clss):
        
        clss.pool =await asyncpg.create_pool('postgresql://postgres:1527@localhost/carregister')
        
    @classmethod
    async def close_db(clss):
        await clss.pool.close()
        print("connection_close")
    async def fetch(self,stmt,*args):
        return await self.pool.fetch(stmt,*args)
    async def execute(self,stmt,*args):
        return await self.pool.execute(stmt,*args)     