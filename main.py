from flask import Flask, request, jsonify
import pandas as pd
from joblib import load
import furl


app = Flask(__name__)


def extract_features(url):
    f = furl.furl(url)
    
    # Extract different parts of the URL using furl
    netloc = f.host  # Domain
    path = f.path.segments  # Path as segments list
    query = f.args  # Query parameters
    
    # URL features
    qty_dot_url = url.count('.')
    qty_hyphen_url = url.count('-')
    qty_underline_url = url.count('_')
    qty_slash_url = url.count('/')
    qty_questionmark_url = url.count('?')
    qty_equal_url = url.count('=')
    qty_at_url = url.count('@')
    qty_and_url = url.count('&')
    qty_exclamation_url = url.count('!')
    qty_space_url = url.count(' ')
    qty_tilde_url = url.count('~')
    qty_comma_url = url.count(',')
    qty_plus_url = url.count('+')
    qty_asterisk_url = url.count('*')
    qty_hashtag_url = url.count('#')
    qty_dollar_url = url.count('$')
    qty_percent_url = url.count('%')
    qty_tld_url = len(netloc.split('.')[-1]) if netloc else 0
    length_url = len(url)

    # Domain features
    qty_dot_domain = netloc.count('.') if netloc else 0
    qty_hyphen_domain = netloc.count('-') if netloc else 0
    qty_underline_domain = netloc.count('_') if netloc else 0
    qty_slash_domain = netloc.count('/') if netloc else 0
    qty_questionmark_domain = netloc.count('?') if netloc else 0
    qty_equal_domain = netloc.count('=') if netloc else 0
    qty_at_domain = netloc.count('@') if netloc else 0
    qty_and_domain = netloc.count('&') if netloc else 0
    qty_exclamation_domain = netloc.count('!') if netloc else 0
    qty_space_domain = netloc.count(' ') if netloc else 0
    qty_tilde_domain = netloc.count('~') if netloc else 0
    qty_comma_domain = netloc.count(',') if netloc else 0
    qty_plus_domain = netloc.count('+') if netloc else 0
    qty_asterisk_domain = netloc.count('*') if netloc else 0
    qty_hashtag_domain = netloc.count('#') if netloc else 0
    qty_dollar_domain = netloc.count('$') if netloc else 0
    qty_percent_domain = netloc.count('%') if netloc else 0
    qty_vowels_domain = sum(1 for char in netloc if char.lower() in 'aeiou') if netloc else 0
    domain_length = len(netloc) if netloc else 0
    server_client_domain = 1 if netloc.lower() in url.lower() else 0

    # Directory features
    path_str = '/' + '/'.join(path)  # Reconstruct path from segments
    qty_dot_directory = path_str.count('.')
    qty_hyphen_directory = path_str.count('-')
    qty_underline_directory = path_str.count('_')
    qty_slash_directory = path_str.count('/')
    qty_questionmark_directory = path_str.count('?')
    qty_equal_directory = path_str.count('=')
    qty_at_directory = path_str.count('@')
    qty_and_directory = path_str.count('&')
    qty_exclamation_directory = path_str.count('!')
    qty_space_directory = path_str.count(' ')
    qty_tilde_directory = path_str.count('~')
    qty_comma_directory = path_str.count(',')
    qty_plus_directory = path_str.count('+')
    qty_asterisk_directory = path_str.count('*')
    qty_hashtag_directory = path_str.count('#')
    qty_dollar_directory = path_str.count('$')
    qty_percent_directory = path_str.count('%')
    directory_length = len(path)

    # File features
    filename = path[-1] if path else ''
    qty_dot_file = filename.count('.')
    qty_hyphen_file = filename.count('-')
    qty_underline_file = filename.count('_')
    qty_slash_file = filename.count('/')
    qty_questionmark_file = filename.count('?')
    qty_equal_file = filename.count('=')
    qty_at_file = filename.count('@')
    qty_and_file = filename.count('&')
    qty_exclamation_file = filename.count('!')
    qty_space_file = filename.count(' ')
    qty_tilde_file = filename.count('~')
    qty_comma_file = filename.count(',')
    qty_plus_file = filename.count('+')
    qty_asterisk_file = filename.count('*')
    qty_hashtag_file = filename.count('#')
    qty_dollar_file = filename.count('$')
    qty_percent_file = filename.count('%')
    file_length = len(filename)

    # Params features
    qty_dot_params = sum(value.count('.') for key, value in query.items())
    qty_hyphen_params = sum(value.count('-') for key, value in query.items())
    qty_underline_params = sum(value.count('_') for key, value in query.items())
    qty_slash_params = sum(value.count('/') for key, value in query.items())
    qty_questionmark_params = sum(value.count('?') for key, value in query.items())
    qty_equal_params = sum(value.count('=') for key, value in query.items())
    qty_at_params = sum(value.count('@') for key, value in query.items())
    qty_and_params = sum(value.count('&') for key, value in query.items())
    qty_exclamation_params = sum(value.count('!') for key, value in query.items())
    qty_space_params = sum(value.count(' ') for key, value in query.items())
    qty_tilde_params = sum(value.count('~') for key, value in query.items())
    qty_comma_params = sum(value.count(',') for key, value in query.items())
    qty_plus_params = sum(value.count('+') for key, value in query.items())
    qty_asterisk_params = sum(value.count('*') for key, value in query.items())
    qty_hashtag_params = sum(value.count('#') for key, value in query.items())
    qty_dollar_params = sum(value.count('$') for key, value in query.items())
    qty_percent_params = sum(value.count('%') for key, value in query.items())

    # Create a dictionary of features
    features = {
        'qty_dot_url': qty_dot_url,
        'qty_hyphen_url': qty_hyphen_url,
        'qty_underline_url': qty_underline_url,
        'qty_slash_url': qty_slash_url,
        'qty_questionmark_url': qty_questionmark_url,
        'qty_equal_url': qty_equal_url,
        'qty_at_url': qty_at_url,
        'qty_and_url': qty_and_url,
        'qty_exclamation_url': qty_exclamation_url,
        'qty_space_url': qty_space_url,
        'qty_tilde_url': qty_tilde_url,
        'qty_comma_url': qty_comma_url,
        'qty_plus_url': qty_plus_url,
        'qty_asterisk_url': qty_asterisk_url,
        'qty_hashtag_url': qty_hashtag_url,
        'qty_dollar_url': qty_dollar_url,
        'qty_percent_url': qty_percent_url,
        'qty_tld_url': qty_tld_url,
        'length_url': length_url,
        'qty_dot_domain': qty_dot_domain,
        'qty_hyphen_domain': qty_hyphen_domain,
        'qty_underline_domain': qty_underline_domain,
        'qty_slash_domain': qty_slash_domain,
        'qty_questionmark_domain': qty_questionmark_domain,
        'qty_equal_domain': qty_equal_domain,
        'qty_at_domain': qty_at_domain,
        'qty_and_domain': qty_and_domain,
        'qty_exclamation_domain': qty_exclamation_domain,
        'qty_space_domain': qty_space_domain,
        'qty_tilde_domain': qty_tilde_domain,
        'qty_comma_domain': qty_comma_domain,
        'qty_plus_domain': qty_plus_domain,
        'qty_asterisk_domain': qty_asterisk_domain,
        'qty_hashtag_domain': qty_hashtag_domain,
        'qty_dollar_domain': qty_dollar_domain,
        'qty_percent_domain': qty_percent_domain,
        'qty_vowels_domain': qty_vowels_domain,
        'domain_length': domain_length,
        'server_client_domain': server_client_domain,
        'qty_dot_directory': qty_dot_directory,
        'qty_hyphen_directory': qty_hyphen_directory,
        'qty_underline_directory': qty_underline_directory,
        'qty_slash_directory': qty_slash_directory,
        'qty_questionmark_directory': qty_questionmark_directory,
        'qty_equal_directory': qty_equal_directory,
        'qty_at_directory': qty_at_directory,
        'qty_and_directory': qty_and_directory,
        'qty_exclamation_directory': qty_exclamation_directory,
        'qty_space_directory': qty_space_directory,
        'qty_tilde_directory': qty_tilde_directory,
        'qty_comma_directory': qty_comma_directory,
        'qty_plus_directory': qty_plus_directory,
        'qty_asterisk_directory': qty_asterisk_directory,
        'qty_hashtag_directory': qty_hashtag_directory,
        'qty_dollar_directory': qty_dollar_directory,
        'qty_percent_directory': qty_percent_directory,
        'directory_length': directory_length,
        'qty_dot_file': qty_dot_file,
        'qty_hyphen_file': qty_hyphen_file,
        'qty_underline_file': qty_underline_file,
        'qty_slash_file': qty_slash_file,
        'qty_questionmark_file': qty_questionmark_file,
        'qty_equal_file': qty_equal_file,
        'qty_at_file': qty_at_file,
        'qty_and_file': qty_and_file,
        'qty_exclamation_file': qty_exclamation_file,
        'qty_space_file': qty_space_file,
        'qty_tilde_file': qty_tilde_file,
        'qty_comma_file': qty_comma_file,
        'qty_plus_file': qty_plus_file,
        'qty_asterisk_file': qty_asterisk_file,
        'qty_hashtag_file': qty_hashtag_file,
        'qty_dollar_file': qty_dollar_file,
        'qty_percent_file': qty_percent_file,
        'file_length': file_length,
        'qty_dot_params': qty_dot_params,
        'qty_hyphen_params': qty_hyphen_params,
        'qty_underline_params': qty_underline_params,
        'qty_slash_params': qty_slash_params,
        'qty_questionmark_params': qty_questionmark_params,
        'qty_equal_params': qty_equal_params,
        'qty_at_params': qty_at_params,
        'qty_and_params': qty_and_params,
        'qty_exclamation_params': qty_exclamation_params,
        'qty_space_params': qty_space_params,
        'qty_tilde_params': qty_tilde_params,
        'qty_comma_params': qty_comma_params,
        'qty_plus_params': qty_plus_params,
        'qty_asterisk_params': qty_asterisk_params,
        'qty_hashtag_params': qty_hashtag_params,
        'qty_dollar_params': qty_dollar_params,
        'qty_percent_params': qty_percent_params
    }

    return features

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    url = data['url']
    features = extract_features(url)
    df = pd.DataFrame([features])

    try:
        # Use joblib to load your model
        model = load('hybrid_model.pkl')
        prediction = model.predict(df)
        if prediction == [0]:
            res = 'Not a Phishing Domain'
        else:
            res = 'It is a Phishing Domain'
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"prediction": res})

if __name__ == "__main__":
    app.run(debug=True)
