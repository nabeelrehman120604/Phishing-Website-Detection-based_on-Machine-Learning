from flask import Flask, render_template, request
import joblib
import pandas as pd
import random
from feature_extraction import extract_features

app = Flask(__name__)

# Load trained model
model = joblib.load("rf_model.pkl")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url'].strip()

    # --- Extract features
    features = extract_features(url)
    df = pd.DataFrame([features])

    # --- Predict
    prediction = model.predict(df)[0]

    # 0 = Phishing, 1 = Legitimate
    if prediction == 1:
        result = "Legitimate Website! ✅"
        extra_reasons = []
    else:
        result = "Phishing Website Detected ⚠️"
        try:
            # Feature importance scores
            feature_order = list(features.keys())
            importances = getattr(model, "feature_importances_", [0] * len(feature_order))
            feat_imp = dict(zip(feature_order, importances))

            # Define what’s expected for legitimate behavior
            expected_safe_values = {
                'having_IP_Address': -1,
                'URL_Length': 1,
                'Shortining_Service': 1,
                'having_At_Symbol': 1,
                'double_slash_redirecting': 1,
                'Prefix_Suffix': 1,
                'having_Sub_Domain': 1,
                'SSLfinal_State': 1,
                'Domain_registeration_length': 1,
                'Favicon': 1,
                'port': 1,
                'HTTPS_token': 1,
                'Request_URL': 1,
                'URL_of_Anchor': 1,
                'Links_in_tags': 1,
                'SFH': 1,
                'Submitting_to_email': 1,
                'Abnormal_URL': 1,
                'Redirect': 1,
                'on_mouseover': 1,
                'RightClick': 1,
                'popUpWidnow': 1,
                'Iframe': 1,
                'age_of_domain': 1,
                'DNSRecord': 1,
                'web_traffic': 1,
                'Page_Rank': 1,
                'Google_Index': 1,
                'Links_pointing_to_page': 1,
                'Statistical_report': 1
            }

            truly_abnormal = [
                f for f, v in features.items()
                if str(v) != str(expected_safe_values.get(f, v)) and isinstance(v, (int, float))
            ]


            abnormal_sorted = sorted(
                truly_abnormal, key=lambda x: feat_imp.get(x, 0), reverse=True
            )


            top_abnormal = random.sample(abnormal_sorted[:8], min(4, len(abnormal_sorted[:8])))
            reason_texts = {
                'having_IP_Address': "The URL uses an IP address instead of a domain name.",
                'URL_Length': "The URL is unusually long, a common phishing tactic.",
                'Shortining_Service': "The URL uses a shortening service, hiding its real destination.",
                'having_At_Symbol': "The '@' symbol is used in URLs to trick users.",
                'double_slash_redirecting': "Multiple slashes suggest a redirect pattern.",
                'Prefix_Suffix': "The domain contains a hyphen, common in fake domains.",
                'having_Sub_Domain': "Too many subdomains detected, often used to hide phishing.",
                'SSLfinal_State': "Website lacks secure HTTPS/SSL certification.",
                'Domain_registeration_length': "The domain was registered for a short period, suspicious.",
                'Favicon': "The favicon is loaded from an external domain.",
                'port': "The website uses a non-standard port.",
                'HTTPS_token': "The domain name contains 'https', which is misleading.",
                'Request_URL': "Too many resources are loaded from external domains.",
                'URL_of_Anchor': "Anchor links redirect to different domains.",
                'Links_in_tags': "Tags contain links pointing to suspicious domains.",
                'SFH': "Form handler sends data to a suspicious or blank destination.",
                'Submitting_to_email': "Form submits data directly to an email address.",
                'Abnormal_URL': "URL structure is inconsistent with domain.",
                'Redirect': "Website performs multiple redirects.",
                'on_mouseover': "Suspicious mouseover scripts found.",
                'RightClick': "Right-click is disabled, often hides malicious intent.",
                'popUpWidnow': "Popups detected, may capture sensitive info.",
                'Iframe': "Page uses iframes, can mask real content.",
                'age_of_domain': "Domain is newly created, potentially untrustworthy.",
                'DNSRecord': "Domain has missing or invalid DNS records.",
                'web_traffic': "Website has low or no traffic, not trustworthy.",
                'Page_Rank': "Low page rank, not reputable.",
                'Google_Index': "Website not indexed by Google, suspicious.",
                'Links_pointing_to_page': "Few inbound links, not a legitimate site.",
                'Statistical_report': "URL contains phishing-related keywords (e.g., 'login', 'verify')."
            }

            extra_reasons = [
                reason_texts.get(f, f"Suspicious behavior detected in {f.replace('_', ' ')}.")
                for f in top_abnormal
            ]

        except Exception as e:
            print("⚠️ Reason extraction error:", e)
            extra_reasons = ["Anomaly detected — possible phishing behavior."]

    return render_template(
        'index.html',
        prediction_text=result,
        url=url,
        extra_reasons=extra_reasons
    )


if __name__ == "__main__":
    app.run(debug=True)
