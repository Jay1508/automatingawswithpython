#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Webotron: Deploye websites with AWS

Webotron automates the process of deploying static websties in aws

- Configure AWS S3 list_buckets
    - Create them
    - Set them up for static website hosting
    - Deploy local files to them
- Configure DNS with AWS Route s3
- Configure a Content Delivery Network and SSL with AWS cloudfront
"""
from pathlib import Path
import mimetypes

from bucket import BucketManager
import sys
import boto3
import click

session = None
bucket_manager = None

@click.group()
@click.option('--profile', default=None, help="Use a given AWS profile")
def cli(profile):
    """Webotron deploy websites to AWS"""
    global session, bucket_manager
    session_cfg={}
    if profile:
        session_cfg['profile_name']=profile

    session = boto3.Session(**session_cfg)
    bucket_manager = BucketManager(session)
# s3 = session.resource('s3')


@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets"""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List objects in an S3 bucket"""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure S3 bucket"""
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)

    return


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    "Sync contents of PATHNAME to Bucket"
    bucket_manager.sync(pathname, bucket)
    print(bucket_manager.get_bucket_url(bucket_manager.s3.Bucket(bucket)))


if __name__ == '__main__':
    cli()
