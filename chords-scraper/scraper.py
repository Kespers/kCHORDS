from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import re
import sys

def accept_cookie(page):
    try:
        page.get_by_role("button", name="AGREE").click()
    except:
        pass  

def get_author(page):
    author_locator = page.get_by_role("cell", name="Capo:").locator("..").locator("..").locator("..").locator("..").locator("div span").filter(has_text="Author").locator("span span:has(a)").first
    
    
    if author_locator.count() == 0:
        return {
            "username": None,
            "profile_link": None
        }

    
    username = author_locator.inner_text()
    if username.endswith(' [a]'):
        username = username[:-4]
    elif username.endswith(' [pro]'):
        username = username[:-6]
    
    return {
        "username": username,
        "profile_link": author_locator.locator("a").get_attribute("href")
    }

def format_date(date):
    now = datetime.now()
    date = date.lower().strip()  
    
    
    if date == "yesterday":
        parsed_date = now - timedelta(days=1)
        return parsed_date.strftime("%Y-%m-%d %H:%M:%S")
    
    
    match = re.match(r"(\d+)\s*(second|minute|hour|day|week|month)s?\s*ago", date)
    if match:
        value, unit = match.groups()
        value = int(value)
        if unit == "second":
            parsed_date = now - timedelta(seconds=value)
        elif unit == "minute":
            parsed_date = now - timedelta(minutes=value)
        elif unit == "hour":
            parsed_date = now - timedelta(hours=value)
        elif unit == "day":
            parsed_date = now - timedelta(days=value)
        elif unit == "week":
            parsed_date = now - timedelta(weeks=value)
        elif unit == "month":  
            parsed_date = now - timedelta(days=value * 30)
        return parsed_date.strftime("%Y-%m-%d %H:%M:%S")

    
    try:
        parsed_date = datetime.strptime(date, "%b %d, %Y")
        return parsed_date.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        pass

    
    raise ValueError(f"Formato di data non riconosciuto: {date}")

# def get_comments(page):
#     page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
#     try:
#         page.get_by_role("button", name="Show all ").click()
#     except:
#         pass
#     page.wait_for_timeout(5000)
#     page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
#     general_locator = page.locator(
#         "article article section:last-of-type", 
#         has=page.locator("div.q48DK.kd_tC.xXf2L.g2AHx")
#     )
#     author_locator = page.locator("footer.soBff span a")
#     message_locator = general_locator.locator("div")
#     date_locator = general_locator.locator("footer.soBff > a span")
    
#     comments = []
    
#     for i in range(author_locator.count() - 1):
#         upvote_locator = general_locator.locator("section.i1eiW.AKsy4 div").nth(i).locator("span")
#         hasSign = upvote_locator.count() > 1
#         comment_data = {
#             "author": author_locator.nth(i).inner_text(),
#             "message": message_locator.nth(i).inner_text().strip(),
#             "date": format_date(date_locator.nth(i).inner_text()),
#             "upvote": int(f'''{upvote_locator.nth(0).inner_text() if hasSign else ''}{upvote_locator.nth(1).inner_text() if hasSign else upvote_locator.nth(0).inner_text()}'''),
#         }
#         comments.append(comment_data)

#     return comments


def get_versions(page, isStarGetter=False):
    if not isStarGetter:
        try:
            page.get_by_role("button", name="versions more").click()
            page.wait_for_timeout(100)
        except:
            pass
    
    page.wait_for_timeout(100)

    try:
        versions_locator = page.get_by_text("More Versions").locator("..").locator("..").locator("nav div:has(span:has(a))")
    except:
        pass

    tab_stars = None
    if versions_locator.count() == 1:
        try:
            tab_stars = int(versions_locator.nth(0).locator("div").locator("div").nth(1).inner_text())
        except:
            pass
        return tab_stars

    versions = []
    for i in range(0, versions_locator.count() - 1):
        version = versions_locator.nth(i)

        tab_stars = None
        try:
            tab_stars = int(version.locator("div").locator("div").nth(1).inner_text().replace(",", ""))
        except:
            pass

        if version.evaluate("node => node.classList.contains('bNjYL') && node.classList.contains('apbAl')"):
            if isStarGetter:
                return tab_stars
            else:
                continue

        version_data = {
            "name": version.locator("a span").inner_text(),
            "link": version.locator("a").get_attribute("href"),
            "stars": tab_stars
        }

        versions.append(version_data)

    return versions

def get_more_versions(page):
    return get_versions(page)

def get_stars(page):
    return get_versions(page, isStarGetter=True)

def get_related_tabs(page):
    tabs_locator = page.get_by_text("Related tabs").locator("..").locator("..").locator("section article div:has(div:has(header))")

    if tabs_locator.count() == 0:
        return None
    
    related_tabs = []
    for i in range(1, tabs_locator.count()):
        tab = tabs_locator.nth(i)
        tab_data = {
            "name": tab.locator("div:has(header) span a").inner_text(),
            "link": tab.locator("div:has(header) span a").get_attribute("href"),
            "stars": int(tab.locator("div").last.inner_text().replace(",", ""))
        }
        related_tabs.append(tab_data)

    return related_tabs

def scrape(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            print(f"Scraping: {url}")

            accept_cookie(page)

            data = {}

            data["url"]=url

            # TESTO CON ACCORDI
            print("\ttesto con accordi", flush=True)
            chords_locator = page.get_by_role("heading", name="Chords", exact=True)\
                .locator("..").locator("..").locator("..").locator("..")\
                .locator("div section div section code pre")
            data["chords"] = chords_locator.inner_html()

            # DIFFICOLTA
            print("\tdifficolta", flush=True)
            data["difficulty"] = page.get_by_role("cell", name="Difficulty:").locator("..").locator("td span").inner_html()

            # TUNING
            print("\ttuning", flush=True)
            try:
                data["tuning"] = page.get_by_role("cell", name="Tuning:").locator("..").locator("td a").inner_html()
            except:
                data["tuning"] = None

            print("\tnome canzone", flush=True)
            data["name"] = page.get_by_role("button", name="Edit").locator("..").locator("..").locator("..").locator("..").locator("..").locator("..").locator("header div h1").inner_html().rstrip()

            print("\tinfo artista", flush=True)
            artist_locator = page.get_by_role("button", name="Edit").locator("..").locator("..").locator("..").locator("..").locator("..").locator("..").locator("header span a")
            data["artist"] = {
                "name": artist_locator.inner_text(),
                "profile_link": artist_locator.get_attribute("href")
            }

            print("\tstats", flush=True)
            data["views"] =  int(page.get_by_role("button", name="Edit").locator("..")\
                .locator("..")\
                .locator("..")\
                .locator("..")\
                .locator("..")\
                .locator("..")\
                .locator("..")\
                .get_by_text(" views, added to favorites ")\
                .inner_text()\
                .split(" views, added to favorites ")[0]\
                .replace(",", ""))
            data["added_favorites"] =  int(page.get_by_role("button", name="Edit").locator("..").locator("..").locator("..").locator("..").locator("..").locator("..").locator("..").get_by_text(" views, added to favorites ").inner_text().split(" views, added to favorites ")[1].split(" times")[0].replace(",", ""))

            print("\tkey", flush=True)
            try:
                data["key"] = page.get_by_role("cell", name="Key:").locator("..").locator("td span").inner_html()
            except:
                data["key"]= None

            print("\tcapotasto", flush=True)
            try:
                capo = page.get_by_role("cell", name="Capo:").locator("..").locator("td span").inner_text()
                data["capo_position"] = capo if (capo != "no capo") else None
            except:
                data["capo_position"] = None

            print("\tautore tab", flush=True)
            data["author"] = get_author(page)

            # print("\tcomment", flush=True)
            # data["comments"] = get_comments(page)

            print("\taltre versioni della tab", flush=True)
            data["more_versions"] = get_more_versions(page)

            print("\tstars", flush=True)
            data["stars"] = get_stars(page)

            print("\ttab simili", flush=True)
            data["related_tabs"] = get_related_tabs(page)

            browser.close()

            return data
    except Exception as e:
        print(f"Errore durante lo scraping: {e}")
        return None  # Ritorna None in caso di errore