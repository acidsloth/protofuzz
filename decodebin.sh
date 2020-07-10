#!/bin/bash
#Just pass protobuff message file as the argument, It will output message in JSON format
protoc_path='modules/protobuf-3.11.4/src/protoc'
file="$1"
#request=`$protoc_path --decode_raw < $file`
#printf "{\n$request\n}" > $file.dec
#turn it to json
#json=`cat $file.dec | sed 's/[0-9]\+/"&"/'| sed 's/".*":.*[^}]/&,/' | sed 's/"{/":{/' | tr -d ' ' | tr -d '\n' | sed  's/,}/}/g' | sed 's/"{/":{/g' | sed 's/}"/},"/g'`
#printf "$json" > $file.json
nano $file.json



#create .proto
#printf '/*Automaticaly generated via decodebin.sh*/\nsyntax = "proto2";\npackage autogen;\nmessage main ' > /tmp/$file.proto
#cat $file.dec | sed 's/\([0-9]*\):.*/required string var\1 = \1;/g' | sed 's/\([0-9]*\) {/message class\1 {/g' >> /tmp/$file.proto
#classnum
#$protoc_path -I=proto --python_out=modules/ $file.proto
#../modules/protobuf-3.11.4/src/protoc -I=. --python_out=./addressbook.proto
