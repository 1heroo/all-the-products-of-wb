import asyncio
import aiohttp


params = {'kind': 2, '_v': '9.3.39'}
headers = {'x-requested-with': 'XMLHttpRequest'}

head = 'https://basket-0{i}.wb.ru'
template = '/vol{vol}/part{part}/{article}/info/ru/card.json'


async def async_range(start, end):
    for i in range(start, end):
        yield i
        await asyncio.sleep(0.0)


async def isvalid_url(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            return response.status == 200


async def find_url(tail: str):
    global head
    url = head + tail
    async for i in async_range(1, 10):
        url = url.format(i=i)
        if await isvalid_url(url):
            return url
    return False


def make_tail(article: str):
    length = len(article)
    global template

    if length <= 3:
        return template.format(vol=0, part=0, article=article)
    elif length == 4:
        args = {
            'vol': 0,
            'part': article[0],
            'article': article
        }
        return template.format(**args)
    elif length == 5:
        args = {
            'vol': 0,
            'part': article[:2],
            'article': article
        }
        return template.format(**args)
    elif length == 6:
        args = {
            'vol': article[0],
            'part': article[:3],
            'article': article
        }
        return template.format(**args)
    elif length == 7:
        args = {
            'vol': article[:2],
            'part': article[:4],
            'article': article
        }
        return template.format(**args)
    elif length == 8:
        args = {
            'vol': article[:3],
            'part': article[:5],
            'article': article
        }
        return template.format(**args)
    elif length == 9:
        args = {
            'vol': article[:4],
            'part': article[:6],
            'article': article
        }
        return template.format(**args)


async def main():
    tasks = []
    for article in range(1, 110_000_000):
        tail = make_tail(str(article))
        tasks += [asyncio.create_task(find_url(tail))]
        if article % 5000 == 0:
            res = await asyncio.gather(*tasks)
            res = [item for item in res if item]
            with open(f'urls/urls_{article}.txt', 'w') as file:
                file.write(str(res))
                tasks = []


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
