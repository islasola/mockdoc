import aiohttp


class AsyncClient:
    def __init__(self, server=None, headers=None):
        self.server = server
        self.headers = headers

    async def get(self, endpoint):
        return await self.__fetch("get", endpoint)
    
    async def post(self, endpoint, json=None):
        return await self.__fetch("post", endpoint, json=json)
    
    async def delete(self, endpoint):
        return await self.__fetch("delete", endpoint)
    
    async def put(self, endpoint, json=None):
        return await self.__fetch("put", endpoint, json=json)

    async def __fetch(self, method, endpoint, json=None):
        if not self.server:
            async with aiohttp.ClientSession() as session:
                if method == 'get':
                    async with session.get(endpoint, headers=self.headers) as response:
                        if response.status != 200:
                            return response.status, response.reason
                        return await response.text()
                if method == 'post':
                    async with session.post(endpoint, headers=self.headers, json=json) as response:
                        if response.status != 200:
                            return response.status, response.reason               
                        return await response.text()
                if method == 'delete':
                    async with session.delete(endpoint, headers=self.headers) as response:
                        if response.status != 200:
                            return response.status, response.reason
                        return await response.text()
                if method == 'put':
                    async with session.put(endpoint, headers=self.headers, json=json) as response:
                        if response.status != 200:
                            return response.status, response.reason               
                        return await response.text()
        
        async with aiohttp.ClientSession(self.server) as session:
            if method == 'get':
                async with session.get(endpoint, headers=self.headers) as response:
                    if response.status != 200:
                        return response.status, response.reason
                    return await response.text()
            if method == 'post':
                async with session.post(endpoint, headers=self.headers, json=json) as response:
                    if response.status != 200:
                        return response.status, response.reason               
                    return await response.text()
            if method == 'delete':
                async with session.delete(endpoint, headers=self.headers) as response:
                    if response.status != 200:
                        return response.status, response.reason
                    return await response.text()
            if method == 'put':
                async with session.put(endpoint, headers=self.headers, json=json) as response:
                    if response.status != 200:
                        return response.status, response.reason               
                    return await response.text()  
