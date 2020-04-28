#!/bin/sh

echo 'sending command1.xml'
nc -u -w 1 127.0.0.1 54321 < commands/command1.xml

sleep 1

echo 'sending command2.xml'
nc -u -w 1 127.0.0.1 54321 < commands/command2.xml 

sleep 1

echo 'sending command3.xml'
nc -u -w 1 127.0.0.1 54321 < commands/command3.xml 

sleep 1

echo 'sending command4.xml'
nc -u -w 1 127.0.0.1 54321 < commands/command4.xml 

sleep 1

echo 'sending command5.xml'
nc -u -w 1 127.0.0.1 54321 < commands/command5.xml 

echo 'DONE!!'
