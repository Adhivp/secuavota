from flask import *
import ipfshttpclient
from web3 import Web3
import json

app = Flask(__name__)

w3 = Web3(Web3.HTTPProvider('https://rpc-mumbai.maticvigil.com/'))
contract_abi = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "fingerprintHash_",
				"type": "string"
			}
		],
		"name": "collectFingerprintHash",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "photo_",
				"type": "string"
			}
		],
		"name": "collectPhoto",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "voterId_",
				"type": "string"
			}
		],
		"name": "collectVoterID",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getFingerprintHash",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getPhoto",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getVoterID",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
contract_address='0x98747c02E12B28772BBcB18972eef97B71769557'
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET'])
def login():
    # dummy login code that logs in no matter what input is provided
    return redirect('/data_collection')
fingerprint=""
voter_id=""
photo=""
@app.route('/data_collection', methods=['GET'])
def data_collection():
    if request.method == 'POST':
        fingerprint = request.form['Finger Print']
        voter_id = request.form['Voter ID']
        photo = request.form['Photo']
    return render_template('data_collection.html')
client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
election_day_1_hash = 'QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH'
json_data = client.cat(election_day_1_hash)
data = json.loads(json_data)
# Append new data to the JSON file
new_data = {"voter_id":voter_id,"fingerprint":fingerprint, "photo": photo}
data.append(new_data)

# Store the updated JSON file back into IPFS
new_json_data = json.dumps(data)
new_ipfs_hash = client.add_bytes(new_json_data)["Hash"]

print("Updated JSON file stored in IPFS with hash:", new_ipfs_hash)

main_data_cid = 'QmQwr95wEKmB9tmEVCmzth8tXFYkHATTjjiJGrYcfvWnz8'
json_data_main = client.cat(main_data_cid)
data_main=json.loads(json_data_main) 
if new_data in data_main: 
    contract.functions.collectFingerprintHash(fingerprint)
    contract.functions.collectVoterID(voter_id)
    contract.functions.collectphoto(photo)
    fingerprint_after_block = contract.functions.getPhoto()
    voter_id_after_block = contract.functions.getFingerprintHash()
    photo_after_block = contract.functions.getVoterID()
else:
    print("not matched")
election_day_1_hash = 'QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH'
after_json_data = client.cat(election_day_1_hash)
after_data = json.loads(after_json_data)
after_block_json = {"voter_id":voter_id_after_block,"fingerprint":fingerprint_after_block, "photo": photo_after_block}
after_data.append(after_block_json)
print("data sucessfully transfered and stored ")
if __name__ == '__main__':
    app.run()
    