# feature_extraction.py
# Extracts 30 features from a given URL for phishing website detection.

import re
import socket
import whois
import pandas as pd
import requests
import tldextract
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime


def extract_features(url):
    """
    Extracts features from a given URL to be used for phishing website detection.
    Returns a dictionary aligned with the model's expected feature columns.
    """
    features = {}

    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        ext = tldextract.extract(url)
        domain_name = ext.domain + '.' + ext.suffix if ext.suffix else ext.domain

        try:
            response = requests.get(url, timeout=4)
            soup = BeautifulSoup(response.text, 'html.parser')
        except:
            soup = None
            response = None

        try:
            socket.inet_aton(domain)
            features['having_IP_Address'] = 1
        except:
            features['having_IP_Address'] = -1

        length = len(url)
        features['URL_Length'] = 1 if length < 54 else 0 if length <= 75 else -1

        shortening_services = r"bit\.ly|goo\.gl|tinyurl\.com|ow\.ly|t\.co"
        features['Shortining_Service'] = -1 if re.search(shortening_services, url) else 1


        features['having_At_Symbol'] = -1 if "@" in url else 1

        features['double_slash_redirecting'] = -1 if url.count('//') > 1 else 1

        features['Prefix_Suffix'] = -1 if '-' in domain else 1

        dots = ext.subdomain.count('.')
        features['having_Sub_Domain'] = 1 if dots == 0 else 0 if dots == 1 else -1

        features['SSLfinal_State'] = 1 if url.startswith("https") else -1

        try:
            w = whois.whois(domain_name)
            if w.expiration_date:
                exp = w.expiration_date[0] if isinstance(w.expiration_date, list) else w.expiration_date
                days_left = (exp - datetime.now()).days
                features['Domain_registeration_length'] = 1 if days_left / 365 >= 1 else -1
            else:
                features['Domain_registeration_length'] = -1
        except:
            features['Domain_registeration_length'] = -1

        try:
            icon = soup.find("link", rel=lambda val: val and 'icon' in val.lower())
            features['Favicon'] = 1 if icon and domain in icon.get('href', '') else -1
        except:
            features['Favicon'] = -1

        features['port'] = -1 if ":443" not in url and ":80" not in url else 1

        features['HTTPS_token'] = -1 if "https" in domain else 1

        try:
            imgs = soup.find_all('img', src=True)
            valid = [img for img in imgs if domain in img['src']]
            features['Request_URL'] = 1 if len(valid) / len(imgs) >= 0.5 else -1
        except:
            features['Request_URL'] = 0

        try:
            anchors = soup.find_all('a', href=True)
            unsafe = [a for a in anchors if "#" in a['href'] or "javascript" in a['href'].lower()]
            features['URL_of_Anchor'] = -1 if len(unsafe) / len(anchors) > 0.6 else 1
        except:
            features['URL_of_Anchor'] = 0

        try:
            links = soup.find_all('link', href=True)
            scripts = soup.find_all('script', src=True)
            total = len(links) + len(scripts)
            safe = [l for l in links if domain in l.get('href', '')]
            features['Links_in_tags'] = 1 if total == 0 or len(safe) / total >= 0.5 else -1
        except:
            features['Links_in_tags'] = 0

        try:
            forms = soup.find_all('form', action=True)
            empty = [f for f in forms if f['action'] == "" or f['action'] == "about:blank"]
            features['SFH'] = -1 if len(empty) > 0 else 1
        except:
            features['SFH'] = 0

        try:
            forms = soup.find_all('form', action=True)
            features['Submitting_to_email'] = -1 if any("mailto:" in f['action'] for f in forms) else 1
        except:
            features['Submitting_to_email'] = 1

        features['Abnormal_URL'] = -1 if domain not in url else 1

        try:
            features['Redirect'] = -1 if response and len(response.history) > 2 else 1
        except:
            features['Redirect'] = 1

        try:
            features['on_mouseover'] = -1 if response and re.search("<script>.+onmouseover", response.text) else 1
        except:
            features['on_mouseover'] = 1

        try:
            features['RightClick'] = -1 if response and re.search(r"event.button ?== ?2", response.text) else 1
        except:
            features['RightClick'] = 1

        try:
            features['popUpWidnow'] = -1 if response and re.search(r"alert\(", response.text) else 1
        except:
            features['popUpWidnow'] = 1

        try:
            features['Iframe'] = -1 if response and "<iframe" in response.text else 1
        except:
            features['Iframe'] = 1

        try:
            creation = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
            age = (datetime.now() - creation).days / 30
            features['age_of_domain'] = 1 if age >= 6 else -1
        except:
            features['age_of_domain'] = -1

        features['DNSRecord'] = 1 if domain_name else -1

        features['web_traffic'] = 0  # placeholder (API needed)

        features['Page_Rank'] = 0  # placeholder (API needed)

        features['Google_Index'] = 1 if "google" in url else -1

        features['Links_pointing_to_page'] = 1 if soup and len(soup.find_all('a')) > 5 else -1

        features['Statistical_report'] = -1 if re.search(r"login|bank|free|verify|update", url) else 1

    except Exception as e:
        print("Error extracting features:", e)
    try:
        feature_order = pd.read_csv("X_train.csv").columns.tolist()
    except Exception:
        feature_order = [
            'having_IP_Address', 'URL_Length', 'Shortining_Service', 'having_At_Symbol',
            'double_slash_redirecting', 'Prefix_Suffix', 'having_Sub_Domain', 'SSLfinal_State',
            'Domain_registeration_length', 'Favicon', 'port', 'HTTPS_token', 'Request_URL',
            'URL_of_Anchor', 'Links_in_tags', 'SFH', 'Submitting_to_email', 'Abnormal_URL',
            'Redirect', 'on_mouseover', 'RightClick', 'popUpWidnow', 'Iframe', 'age_of_domain',
            'DNSRecord', 'web_traffic', 'Page_Rank', 'Google_Index', 'Links_pointing_to_page',
            'Statistical_report'
        ]

    final_features = {col: features.get(col, 0) for col in feature_order}
    return final_features
