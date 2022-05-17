import requests, pandas, json, sys, os
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


log_file = "log.txt"
req_session = requests.Session()
timeout = 7


def write_log(e):
    open(log_file, "a").write(str(e)+" File : "+str(__file__)+" Line : "+str(e.__traceback__.tb_lineno)+"\n")

def network_err():
    input(" [!] please check your internet connection\n [Press Enter to continue]")
    sys.exit()

def create_instance_ua(trying=5):
    global user_agent
    while trying>0:
        try:
            user_agent = UserAgent()
            return None
        except:
            trying-=1

    print(" [!] Filed create random ua instance")
    input(" [Press Enter to continue]")
    sys.exit()

def clr():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print("""
 █▄▀ █▀▀ █▀▄▀█ █▀▀ █▄░█ ▄▀█ █▀▀   █▀█ █ █░█ █▄▀
 █░█ ██▄ █░▀░█ ██▄ █░▀█ █▀█ █▄█   █▀▀ █ █▀█ █░█
 
 █▀ █▀▀ █▀█ ▄▀█ █▀█ █▀▀ █▀█
 ▄█ █▄▄ █▀▄ █▀█ █▀▀ ██▄ █▀▄  V1.0.0

 Coder By : https://github.com/Nux-xader
 Contact  : https://wa.me/6281251389915
 ___________________________________________________
""")

def progress(progs, total):
    percent = 100*(progs/float(total))
    bar = '█'*int(percent)+'-'*(100-int(percent))
    print(f"\r [{bar}] {percent:.2f}%", end="\r")


def get_urls():
    global req_session
    try:
        resp = str(req_session.get("https://simpu.kemenag.go.id/home/pihk", headers={"User-Agent": user_agent.random}, timeout=timeout).text).split("<tbody>")[-1].split("</tbody>")[0]
        return [str(x.extract()).split('href="', 1)[-1].split('"')[0] for x in BeautifulSoup(resp, 'html.parser').find_all("tr")]#:
    except Exception as e:
        write_log(e)
        network_err()


def get_data(url):
    req_session = requests.Session()
    while True:
        try:
            resp = str(req_session.get(url, headers={"User-Agent": user_agent.random}, timeout=timeout).text).split("<table")[-1].split("</table>")[0]
            break
        except Exception as e:
            write_log(e)
            # if i == 49:
            #     input(f"\n [!] Network error >> {url}\n [Press Enter to Continue]")
            #     sys.exit()

    soup = BeautifulSoup(resp, 'html.parser')
    open("ex.html", "w").write(resp)
    data = [[x.text for n, x in enumerate(soup.find_all(tag)) if (n+1)%2 == 0] for tag in ["th", "td"]]

    return {
        "Nama": data[0][0], 
        "Status": data[0][1], 
        "Nomor SK": data[1][0], 
        "Tanggal SK": data[1][1], 
        "Telepon": data[1][2], 
        "Alamat": data[1][3], 
        "Email": data[1][4], 
        "Nilai Akreditasi": data[1][5]
    }


def main():
    clr()
    banner()

    urls = []
    [urls.append(i) for i in get_urls() if i not in urls]
    json.dump(urls, open("temp.json", "w"), indent=4)
    create_instance_ua()
    
    while True:
        try:
            saveto = str(input(" [*] Save result to : "))
            if saveto.split("xlsx")[-1] != "xlsx": saveto+=".xlsx"
            open(saveto, "r").read()
            print(" [!] File already exists")
        except:
            break

    clr()
    banner()
    results = []
    for n, url in enumerate(urls):
        result = get_data(url)
        if result not in results: results.append(result)
        results_df = pandas.DataFrame(results)
        results_df.to_excel(saveto, index=False)
        print("")
        progress(n+1, len(urls))

    print(f"\n [+] Result saved to : {saveto}")


if __name__ == "__main__":
    main()
    # result = []
    # [result.append(i) for i in get_urls("https://simpu.kemenag.go.id/home/pihk") if i not in result]
    # json.dump(get_data("https://simpu.kemenag.go.id/home/pihkdetail/3526"), open("ex.json", "w"), indent=4)