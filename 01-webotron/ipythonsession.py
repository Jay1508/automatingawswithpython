# coding: utf-8
get_ipython().run_line_magic('history', '')
import boto3
session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')
