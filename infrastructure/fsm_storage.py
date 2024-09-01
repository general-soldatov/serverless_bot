import boto3

class FSMStorage:
    def __init__(self, storage, key) -> None:
        self.storage = storage
        self.key = key

    async def set_state(self, state = None) -> None:
        await self.storage.set_state(key=self.key, state=state)

    async def get_state(self):
        return await self.storage.get_state(key=self.key)

    async def set_data(self, data) -> None:
        await self.storage.set_data(key=self.key, data=data)

    async def get_data(self):
        return await self.storage.get_data(key=self.key)

    async def update_data(self, data=None, **kwargs):
        if data:
            kwargs.update(data)
        return await self.storage.update_data(key=self.key, data=kwargs)

    async def clear(self) -> None:
        await self.set_state(state=None)
        await self.set_data({})