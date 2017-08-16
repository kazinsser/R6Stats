import asyncio
import r6sapi as api

# Testing


@asyncio.coroutine
def run():
    auth = api.Auth("username", "password")

    player = yield from auth.get_player("Kazology", api.Platforms.UPLAY)
    operator = yield from player.get_operator("hibana")
    print("hibana kills: ")
    print(operator.kills)
    operator = yield from player.get_operator("sledge")
    print("sledge kills: ")
    print(operator.kills)
    operator = yield from player.get_operator("ash")
    print("ash kills: ")
    print(operator.kills)
    yield from auth.session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
