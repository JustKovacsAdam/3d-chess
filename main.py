import asyncio

# pygbag (a böngészős változat) a main.py importjaiból dönti el, mely csomagokat
# töltse be, ezért a pygame-et itt is importálni kell, különben nem töltődik be.
import pygame  # noqa: F401

import fuggvenyek


async def main():
    await fuggvenyek.kirajzol()


if __name__ == "__main__":
    asyncio.run(main())
