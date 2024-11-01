from flask import Flask, request, jsonify
import jwt, json, time, requests

app = Flask(__name__)

def generate_token():
    '''
    :return:
        Generates a JWT token and optionally exchanges it for an access token
    '''
    # Service account details (client_email and private_key)
    client_email = 'ttec-wxcc@ccai-372220.iam.gserviceaccount.com'
    private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCam7h38tJ3SWNz\nUmPypDeH7OfgHCEYFaXaLvzby1p6nSxomnBIICGu3vMsmd7Or7cYIIgf/nBVETys\n64XEXbN6ysr2i4GYMNp1/lXjX7rO9z0A44j6kM3tkJOj7J8G+m6sC+5lYHavjlrJ\nnSGvthfLPOI+ircWBsCxwAe7JZiNQVhZl1v5VYCBOPhaEdK8SiiefPznHpLrMfXB\nogdJsiByQynJhur53+yEGcYhm+qSi9bLHNoGcQapNUOCyGdXstIQZqzUPHQA8l9P\nw+XJqhlyZ7gSUceauyQ4oTrfnXEFQzio+cKE1EPmrpS8WEz1Ohq2WQsLY0DT2FaO\nCHwNR0oTAgMBAAECggEAQvM21P5aJFyry6b8b/irsVkl6fbUX+UT7mDVj2pGUn1Y\nWy2xfJIpc9vIyuIQyUjvDOwddllMlJHDyA+vW+LFk2FYtZ2gr2JMX7cUw0LTlsca\nbBWb3gExo3Otc1lGXhO5NBhwkgbNLmWDK/Y2vaupLxG82R9hfBDNhctlraVwo43h\nmoZL0tkMEtWWnV9eosfifA5jUcZFdEBjBjrbAJP2VmgKi7pRj1JdRmDjek5UrDtn\nDsiyT515iR0NIiZQAOLY1yvSEM6UmKuIo6D0necmhntfD8k3QhRWKW/1syVBrHv2\nS5eH/ohAAMu4LZh01+14KtCxj4es7Rv7I1olkJnpyQKBgQDKwjaC8tN0z8W/PVno\nsQNdcDnCqLrD9QwvfWRIyJQKpUkZ61y5pTFBlfHIDo63q7kA4odg1CFowHVypj3u\nK3yN5tX0F+c3RblDp4GNSIz/Nm8nl/uVOfHlRacEbKnxYA7NaL7pj5uHWx2z0nH8\nN7tTtz7KVE8m5JiEJ/ChsauYGQKBgQDDNMHNb+oxlKsde4HJPBrWoyzZOcnesp7t\neBHyczeUAAC9/pYIBQtuHHriT9DmnlC6mfwx0XjqkL5aMHEkYb79SGoPzSMTFwrk\nijqPCP42S8/itnTbfliDabkyDPAJTU1mIr9kDg7BG/O8Sq4wllxuOOTtvLgBhIum\nuiKv/GHpCwKBgDpiF/4226qcFU3O5a+6IMTsBsXFfhnk2sBl89V9ZBt4oocDHa0b\nIwbGnVtEzdWXbesST3cTPheCq476zYRiIzhdCqiBpYNl4UXY2tYK2Qa37uPQwJGk\noMGq/7+nZnvpc/mzup1YS6l7FB9uboH4rkkZz8vE4RHK6xvKwGBe35EpAoGAPw8k\n6CuWGQwwtuZ2B77t4JZ333iGmPVU19uo2IyV0K6rjrTWXKLcjWaP39nu3wEXjSA/\nUwybJhM6GsJ5WkplO0cQVChtgzY3Y5qvzhMWpA2bi15ro5hOGa2mkN+TDz40maDx\n+O19oK5Z72KkoLeCBm1ErvP+8SaTQnnwyK8cJf8CgYEAovbtvRCh6okMNNxmrLeM\nI91T3IlJOLa5orHhKXg1NVE1Fpo0dHpwph+Smv/AjtpA2tVp+SrdmO0DLNHAb9l2\nkUWsaThopeVbmBJoxrry21+7Kq+9kEu5GKcfOz5RDm/M0oLG5fnnv7jik+TMJ+cl\nX+b+ykRdqTCTLIGHOjkXPNM=\n-----END PRIVATE KEY-----\n"

    # JWT creation (Valid for 1 hour)
    iat = time.time()
    exp = iat + 3600  # Token valid for 1 hour
    payload = {
        'iss': client_email,
        'sub': client_email,
        'aud': 'https://oauth2.googleapis.com/token',
        'iat': iat,
        'exp': exp,
        'scope': 'https://www.googleapis.com/auth/cloud-platform'  # Modify based on required API scopes
    }

    try:
        # Sign the JWT with RS256 algorithm
        signed_jwt = jwt.encode(payload, private_key, algorithm='RS256')
    except Exception as e:
        return jsonify({'error': 'JWT generation failed', 'details': str(e)}), 500

    # Exchange JWT for access token from Google OAuth2 (uncomment if needed)
    try:
        response = requests.post(
            'https://oauth2.googleapis.com/token',
            data={
                'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                'assertion': signed_jwt
            }
        )
        response.raise_for_status()
        access_token = response.json().get('access_token')
    except requests.exceptions.RequestException as e:
        return {'error': 'Failed to exchange JWT for access token', 'details': str(e)}, 500

    return {'token': access_token}  # Return the access token as a dictionary

@app.route('/get_token', methods=['POST'])
def get_token():
    # Check if headers contain necessary information
    wxcc_org_id = request.headers.get('wxccorgid')
    wxcc_auth_header = request.headers.get('wxccauthheader')

    # Simple header validation
    if wxcc_org_id == 'bacQikGSKPsm9jgCh8fr' and wxcc_auth_header == 'bacQikGSKPsm9jgCh8fr':
        print("Help")
        token_response = generate_token()
        if isinstance(token_response, tuple):
            return token_response  # If it's an error response
        return jsonify(token_response)  # If successful
    else:
        return jsonify({'error': 'Invalid or missing Authorization or wxcc-auth-header'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
