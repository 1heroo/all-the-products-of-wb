import asyncio
import aiohttp
from time import sleep


params = {'kind': 2, '_v': '9.3.39'}
headers = {'x-requested-with': 'XMLHttpRequest'}

head = 'https://basket-0{i}.wb.ru'
template = '/vol{vol}/part{part}/{article}/info/ru/card.json'


async def isvalid_url(url: str):
    async with aiohttp.ClientSession() as session:        
        async with session.get(url, headers=headers, params=params) as response:
            status = response.status == 200
            return url if status else False


def make_head(article: int):
    global head
    number = 0
    if article < 43500000:
        number = 3
    elif article < 72000000:
        number = 4
    elif article < 100800000:
        number = 5 
    elif article < 106300000:
        number = 6
    elif article < 111600000:
        number = 7
    elif article < 117000000:
        number = 8
    else:
        number = 9
    return head.format(i=number)


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


stop_point = 130077000

new_stop = 0


async def main(stop):
    global new_stop
    tasks = []
    for article in range(stop, 135_000_000):
        tail = make_tail(str(article))
        head = make_head(article)
        url = head + tail
        tasks += [asyncio.create_task(isvalid_url(url))]
        if article % 1000 == 0:
            new_stop = stop
            print(article)
            res = await asyncio.gather(*tasks)
            res = [item for item in res if item]
            tasks = []
            with open(f'urls/urls_{article}.txt', 'w') as file:
                file.write(str(res))


if __name__ == '__main__':
    while True:
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main(stop_point))
        except Exception as e:
            print(e)
            print(new_stop, 'new stop')
            stop_point = new_stop
            
            sleep(30)
            


