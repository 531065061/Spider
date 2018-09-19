import requests

base_url='https://www.jianshu.com/c/bDHhpK'
def get_html(offset):
    queries='?order_by=commented_at&page={offset}'
    url=base_url+queries
    response=requests.get(url)
    if response.status_code==200:
        return response.text
    return None

def main():
    get_html(1)

if __name__ == '__main__':
    main()

