from datetime import datetime
import json
import requests

"""
curl 'https://discourse.onlinedegree.iitm.ac.in/directory_items.json?period=yearly&order=likes_received&exclude_groups=&limit=5' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -b '_gcl_au=1.1.1287247411.1748334859; _ga=GA1.1.1168576523.1748334859; _fbp=fb.2.1748334860156.871035082688435498; _ga_5HTJMW67XK=GS2.1.s1748334859$o1$g0$t1748334871$j0$l0$h0; _ga_08NPRH5L4M=GS2.1.s1749274884$o8$g1$t1749274905$j39$l0$h0; _t=6YkB0Eke9LH8zXM04WUSZTIx9t0Tk3rgUdvaMloG6Q%2B9XFLXgNnmJyceb%2FuPX6ANa%2B7feVeGsv6QUsAEOR2kB%2BrYfbxd0psywhfBtT3dCnGPNzZE1bZIYrrJK6oLVqOkm82h9d%2F3VooXcCZ29ur8I5n%2Bl8hMVmy4%2BtpUP20GxutcW1xh%2FbGziL7Sb4f2trw7%2ByulgpqPC6afw8M1SxUgtl%2BzyyaRJfVtsKX559ffMTQ9yGZ0%2BJoVLL2BqpkrRi%2FNXvJcg5wNOLna4dwEobD5ifkKM1XeEYiMb64%2BmBzGm7XJ3hhxPUc5o9VPT%2B8H%2B%2F4tOY9Cw%3D%3D--wWC0FF8IseQQFL2x--iAmMRPy18Y4xvkupZLNAww%3D%3D; _forum_session=kjQl6P2eSLND4A4VpkFrXA5DPCT4M%2BtX3Wj%2BreS4Vj8mQUgupM0rOFaNpgITnVqbaEeaA%2FA3NocqrblYABNKcAEKLeoKcG3BJod%2Bnh8YKxLXii0k4CK8jX70x73jfJ9YxzfV0CYMnTAeozFh6ubLXeq%2FV5LBM1I1tVZ9EEA3HVtgik28BaueqITOOrBP%2BDz1qGcGJrt1sTPXINIf%2F5twuMQEDOWchd5Jz2UsxWwBkNZrqgO5IO2Io5oAzphCMM4Xn0%2BBkAFhka3tMeNaz8o4JNww1SXXf2lDHPLA2shcmNPesEhEVTEFUmcHl%2FK3NzGulvtvkkbK0Wj0vgg9PeWsoJB%2FurW2lC6fYqsSHxkG9k8SVBJduGYbCD0FCmGBj2JaTEQ7IPJZi%2BVC9NyiR3UZRNtuBfedKazUcOpWk3TIch3IaN%2B7n7UxGoXYdL3RwnR3759mNYhxLP0DAimD290OnJyU3WR5sw%3D%3D--kHdJBwpQtsjn%2BX5k--pqWC8TphuQzRo2qT%2BufkTw%3D%3D' \
  -H 'priority: u=1, i' \
  -H 'referer: https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34?page=1' \
  -H 'sec-ch-ua: "Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'

"""

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en;q=0.9",
    "discourse-logged-in": "true",
    "discourse-present": "true",
    "priority": "u=1, i",
    "referer": "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34",
    "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "x-csrf-token": "GSXutwfeyuSX04EigUUzThyIzL7kDQkZSPv7HGPgGQj2-sxF0A0nS5ISBq5Zty4JFjCSve8yvBqR0g8pHtoHeQ",
    "x-requested-with": "XMLHttpRequest"
}

cookies = {
    "_gcl_au": "1.1.1287247411.1748334859",
    "_ga": "GA1.1.1168576523.1748334859",
    "_fbp": "fb.2.1748334860156.871035082688435498",
    "_ga_5HTJMW67XK": "GS2.1.s1748334859$o1$g0$t1748334871$j0$l0$h0",
    "_ga_08NPRH5L4M": "GS2.1.s1749274884$o8$g1$t1749274905$j39$l0$h0",
    "_t": "Q9CV57aYYnU%2FaWTvFrgQGJvFZdssfyV%2BS08d%2BvnEkVbsoonCPytezyEWfwRD5zqrN8vYTIJXfgeVjz%2B4TtL118M05FdAIP1LtaEuMHsbDRrWuTTYxqtOQL0igcs1VI418Js8o7ti%2FsBi%2Fb%2FJZt3iU1EMgT6tljzl7aaD%2BbEPJXOpZOT7kpQkXjkdgKUgsdox%2F5xz%2B%2Bu2Q2PfeJCX%2FhUpxTDwLuOob4Dl8dbTz9%2B8X21aiBAQPDeFnhmgXk%2BcKba7vsKjlq6IOUL8jGRVQ2xvfkbifLZTjkgjA%2Be5MQ2P%2FdPyeK22Oikw54QvjjViEHPe7ncnpw%3D%3D--bEV5hgUSJKloN24e--oq%2BdhSx5JLejjwa0M6B%2F%2Fg%3D%3D",
    "_forum_session": "WSRdfn3rDL9g%2B5Caaxs5vciOlDMZBAsGZwIYXWxo6ROjnpNF7oHnvTKwrELb%2BrYrxn%2B0ZDwQUeEqOVhZ5MPGLaM4uxx%2B%2B6iyUagd2vcgzUG7xo6i0a7yegC%2FGyySzCunYnrM9j94x7yH03kj4W3swqThem3dJvIZ6lfRK6zF41z6dSXeTn8NSPuYo1CQpJWOrB6kifTbZY0BZsq8v1Gs8dpczwPniXZ3g%2B%2BxxJBpYSxxGJW2wPxP1Asmo1FjlVKw4kTFoWmtZAWN4%2B2KP67zGyNN8s93Hw%3D%3D--i%2BDwE3rQPm7NM3%2Bg--GLYwYiZyVhRYMsFqWAL2jQ%3D%3D"
}

class DiscourseScraper:
    def __init__(self, url: str, headers: dict, cookies: dict, start_date: str, end_date: str):
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")

    def get_all_topics(self, page=1):
        url = f"{self.url}?page={page}"
        response = requests.get(url, headers=self.headers, cookies=self.cookies)
        response.raise_for_status()
        res = response.json()
        return res['topic_list']['topics']
    
    def filter_to_date(self, topics):
        print(self.start_date, self.end_date)
        print(topics[0]['created_at'])
        filtered_topics = [topic for topic in topics if self.start_date <= datetime.strptime(topic['created_at'].split("T")[0], "%Y-%m-%d") <= self.end_date]
        print(f"Filtered {len(filtered_topics)} topics out of {len(topics)}")
        return filtered_topics

    def get_posts(self, topic):
        url = f"https://discourse.onlinedegree.iitm.ac.in/t/{topic['id']}/posts.json?track_visit=true&forceLoad=true"
        response = requests.get(url, headers=self.headers, cookies=self.cookies)
        response.raise_for_status()
        res = response.json()
        # TODO: There is a cooked field in post , which contains the image url
        return res['post_stream']['posts']
    
    def filter_relevent_fields(self, posts):
        return [
            {
                'url': f'https://discourse.onlinedegree.iitm.ac.in{post["url"]}',
                'text': post['cooked']
            } for post in posts
        ]
    
    def get_all_posts(self):
        topics = []
        for page in range(1, 10):
            topics.extend(self.get_all_topics(page))
        filtered_topics = self.filter_to_date(topics)
        posts = []
        for topic in filtered_topics:
            posts.extend(self.get_posts(topic))
        final_data = self.filter_relevent_fields(posts)
        self.save_posts(final_data)
        return final_data
    
    def save_posts(self, posts):
        with open('data/posts.json', 'w') as f:
            json.dump(posts, f)

if __name__ == "__main__":
    scraper = DiscourseScraper(
        url="https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34",
        headers=headers,
        cookies=cookies,
        start_date="2024-12-01",
        end_date="2025-05-20"
    )
    print(scraper.get_all_posts())