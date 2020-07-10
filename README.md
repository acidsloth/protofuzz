# protofuzz
Intruder like application for websockets with protocol buffers support<br/>
<br/>
Application is using modified websockets library https://github.com/mdymike/websockets, https://github.com/nccgroup/blackboxprotobuf and https://developers.google.com/protocol-buffers
Created because no tools exist which can deal with protobuf over websockets and only working fuzzer I was able to find was based on kitty fuzzer and it was inconvinient to write definition.  
<br/>
Prerequesites:<br/>
-Linux, tested on debian 9 and 10<br/>
-Python ≥ 3.7 for whole application except modules/blackboxprotobuf must use python 2.7. Use pyenv. (On debian 10 just run protofuzz.py wiht with python3. Rest should work as python 2.7 is default) 
-nano<br/>
-you might need to go to modules/protobuf-3.11.4 and compile protobuf-3.11.4 (no need to install)<br/>
-if you want to test wss:// on included websocket server you need to generate keys using script<br/><br/>

Usage:<br/>
Program is inspired by Burp Intruder (which does not support websocket nor protobuf at the moment I'm writing this) so usage is similar.<br/>
Use system proxy export eg. https_proxy=http://127.0.0.1:8080<br/>
For plain websockets mark the place you want to substitude with your payload by using "`" character at the start and the end of characters you want to substitute (just one instance for now, see test payload for example)<br/>
eg. ./protofuzz.py testwordlist wss://localhost:8765 testpayload<br/>
<br/>
For websockets using protobuf your payload is in binary so during execution texteditor will be loaded. Mark fuzzing place the same way as above.<br/> 
eg. ./protofuzz.py testwordlist wss://localhost:8765 proto/testprotopayload -x<br/>
If application authentication is handled by websocket you might specify a prerequest with -p prerequest.file.<br/><br/>

 
Limitations:<br/>
-lib blackboxprotobuf sometimes fail to reencode certian payloads<br/> 
-some payloads are reencoded differently<br/>
-Protobuf wordlist must not break json eg. quote should be \" etc<br/>
