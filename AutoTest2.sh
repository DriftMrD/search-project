#!/bin/bash
echo "" > Test2.log
python3 TestCase.py "Who is Trump" >> Test2.log 
echo "***********NEXT TEST************" >> Test2.log 
python3 TestCase.py "The Light Phone" >> Test2.log 
echo "***********NEXT TEST************" >> Test2.log 
python3 TestCase.py "Junit Testing Principle" >> Test2.log 
echo "***********NEXT TEST************" >> Test2.log 
python3 TestCase.py "Dr Danushka Bollegala Profile" >> Test2.log 
echo "***********NEXT TEST************" >> Test2.log 
python3 TestCase.py "Michele Zito University Of Liverpool" >> Test2.log 
echo "***********NEXT TEST************" >> Test2.log 
vim Test2.log
