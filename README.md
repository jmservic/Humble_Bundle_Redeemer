# Humble_Bundle_Redeemer
## Description
This application automatically chooses, redeems, and registers steam keys from Humble Bundle. It allows the user to log into both Humble Bundle and Steam. I created it for my personal use, particularly immediately choosing and redeeming new choice bundles and checking for new keys for older choices. In addition, this was my first personal project for the Boot.dev back end developer course.
The application uses sqlite to store choice bundles, regular bundles, store keys, logs, redemption attempts, and giftable products.
## Setup
After downloading the repository, perform the following steps:
1. Create the virtual environment. From the top folder, run `python3 -m venv venv`.
2. Source the virtual environment `source venv/bin/activate`
3. Install the dependencies `pip install -r requirements.txt`
4. In the top folder, create a .env file with the following information
```
  HB_ACCOUNT={Your Humble Bundle account name or email}
  HB_PASSWORD={Your Humble Bundle password}
  STEAM_ACCOUNT={Your Steam account name}
  STEAM_PASSWORD={Your Steam password}
```
5. Optionally run the test.sh bash script to make sure all unit tests pass.
6. Enjoy!
## Dependencies
This application uses the following dependencies:
* beautifulsoup4
* certifi
* charset-normalizer
* idna
* protobuf
* pycryptodome
* python-dotnet
* requests
* soupsieve
* typing_extensions
* urllib3
