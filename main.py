from flask import Flask, render_template, request,jsonify
from random import choice
from pymongo import MongoClient
import requests

url = 'mongodb://sungjin:1234abc@ds149593.mlab.com:49593/heroku_n8ns22rl?retryWrites=false'
client = MongoClient(url) 
db = client['heroku_n8ns22rl'] 
sido_collection = db['sido']
gugun_collection  = db['gugun']

SERVICE_KEY = "BGKjqVoB8xXqvUcQKrIMWx99IvaI%2F4ItES7QoH5ayKNjSxCVZlIQTMh0krSG1FZ01SSVFcfNTT%2FAYTs9r8hqQA%3D%3D"



web_site = Flask(__name__)

number_list = [
	100, 101, 200, 201, 202, 204, 206, 207, 300, 301, 302, 303, 304, 305, 307, 400, 401, 402, 403, 404, 405, 406, 408, 409, 410, 411, 412, 413, 414, 415,
	416, 417, 418, 421, 422, 423, 424, 425, 426,
	429, 431, 444, 450, 451, 500, 502, 503, 504, 506, 507, 508, 509, 510, 511, 599
]

@web_site.route('/')
def index():
	return render_template('index.html')

@web_site.route('/user/', defaults={'username': None})
@web_site.route('/user/<username>')
def generate_user(username):
	if not username:
		username = request.args.get('username')

	if not username:
		return 'Sorry error something, malformed request.'

	return render_template('personal_user.html', user=username)

@web_site.route('/page')
def random_page():
  return render_template('page.html', code=choice(number_list))


@web_site.route('/sido')
def get_sido():
   result = []
   all_sidos = sido_collection.find({})

   for sido in all_sidos:
     data = {'code':sido['code'],
     'name':sido['name']}
     result.append(data)
   response = {'result':result}

   return jsonify(response)


@web_site.route('/gugun')
def get_gugun():
   sido_code = request.args.get('sido_code')
   sido_code = int(sido_code) # 데이터베이스에 숫자로 넣었기 때문

   result = []
   all_sidos = gugun_collection.find({'parent_code':sido_code})

   for sido in all_sidos:
     data = {'code':sido['code'],
     'name':sido['name']}
     result.append(data)
   response = {'result':result}

   return jsonify(response)



@web_site.route('/occur')
def get_occur():
  siDo = request.args.get('sido_code')
  guGun = request.args.get('gugun_code')
  searchYearCd = "2018"
  # siDo = "11"
  # guGun = "590"
  numOfRows = "100"
  pageNo = "1"
  query = {'parent_code':int(siDo),'code':int(guGun)} # 글자여서 숫자형으로 바꿔준다
  find_result = gugun_collection.find_one(query)
  sido_name = find_result['parent']
  gugun_name = find_result['name']
  spot_nm = ''
  occrrnc_cnt = 0
  URL = f"http://apis.data.go.kr/B552061/schoolzoneChild/getRestSchoolzoneChild?serviceKey={SERVICE_KEY}&searchYearCd={searchYearCd}&siDo={siDo}&guGun={guGun}&type=json&numOfRows={numOfRows}&pageNo={pageNo}&"
  response = requests.get(URL)
  result = response.json()

  if len(result['items']['item']) > 0:
    for item in result['items']['item']:
      spot_nm = item['spot_nm']
      print(spot_nm)
      # spot_nm = spot_nm.split()[2] +" " +spot_nm.split()[3]
      first = spot_nm.split()[2]
      second = spot_nm.split()[3]
      spot_nm = f"{first} {second}"
      
      occrrnc_cnt = item['occrrnc_cnt']
    
    return render_template('occur.html', sido_name=sido_name,gugun_name=gugun_name,spot_nm=spot_nm,occrrnc_cnt=occrrnc_cnt)
  else:
    return render_template('occur_with_zero.html')

    
  

  # return render_template('occur.html', sido_name=sido_name,gugun_name=gugun_name,spot_nm=spot_nm,occrrnc_cnt=occrrnc_cnt)

# print(result['items'])



# 어떤 시의 어떤 구에 어떤 장소에서 몇 번 났다.

# =========================================
# @web_site.route('/result')
#    try {
#    // 도 정보 받음
#    String province = param;
 
#    // 알맞은 동적 select box info 생성
#    List<String> cityList = new ArrayList();
 
#    if (province.equals("gyeonGi")) {
#       cityList.add("안양");
#       cityList.add("의정부");
#    } else if (province.equals("gangWon")) {
#       cityList.add("원주");
#       cityList.add("우리집");
#    }
 
#    // jsonArray에 추가
#    JSONArray jsonArray = new JSONArray();
#    for (int i = 0; i < cityList.size(); i++) {
#       jsonArray.add(cityList.get(i));
#    }
 
#    // jsonArray 넘김
#    PrintWriter pw = res.getWriter();
#    pw.print(jsonArray.toString());
#    pw.flush();
#    pw.close();
 
#    } catch (Exception e) {
#        System.out.println("Controller error");
#    }
# }
# [출처] [JAVA] Dynamic 동적 select box 구현|작성자 코변



web_site.run(host='0.0.0.0', port=8080)