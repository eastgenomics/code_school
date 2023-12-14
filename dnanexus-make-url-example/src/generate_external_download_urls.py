#!/usr/bin/env python

import os
import dxpy

@dxpy.entry_point('main')
def main(input_files, token_file):

    # Parse token_hash from token file input
    token_file = dxpy.DXFile(token_file)
    dxpy.download_dxfile(token_file.get_id(), "token_file")
    
    with open('token_file', 'r') as f:
        token_hash = f.readline().strip()
    f.close()

    # Create the environment.json file and get pre-set values for parent_project and job ids
    job_id = os.environ.get('DX_JOB_ID')
    parent_project = os.environ.get('DX_PROJECT_CONTEXT_ID')
    dxpy.config.write("DX_PROJECT_CONTEXT_ID", parent_project)
    dxpy.config.write("DX_CLI_WD", "/")
    dxpy.config.save()
    
    # Unset and clear the environment variables and the values in the environment.json file
    del os.environ['DX_WORKSPACE_ID']
    del os.environ['DX_APISERVER_HOST']
    del os.environ['DX_PROJECT_CONTEXT_ID']
    del os.environ['DX_JOB_ID']
    del os.environ['DX_APISERVER_PORT']
    del os.environ['DX_APISERVER_PROTOCOL']
    del os.environ['DX_SECURITY_CONTEXT']
    dxpy.config.clear(reset=True)

    # set config variables and save them to environment.json file
    dxpy.config.write("DX_JOB_ID", job_id)
    dxpy.config.write("DX_PROJECT_CONTEXT_ID", parent_project)
    dxpy.config.write("DX_CLI_WD", "/")
    sec_context = '{"auth_token":"' + token_hash + '","auth_token_type":"Bearer"}'
    os.environ['DX_SECURITY_CONTEXT'] = sec_context
    dxpy.set_security_context(json.loads(sec_context))
    dxpy.config.write("DX_SECURITY_CONTEXT", sec_context)
    dxpy.config.write("DX_USERNAME", dxpy.whoami())
    dxpy.config.save()

    # Get URLs for the input files
    all_urls = []

    for item in input_files:

        dxfile = dxpy.DXFile(item, project=parent_project)

        download_url, headers = dxfile.get_download_url(preauthenticated=True, duration=86400, filename=dxfile.name, project=parent_project)

        all_urls.append(download_url)
    else:
        print("All files processed successfully...")

    output = {}
    output["download_urls"] = all_urls

    return output

dxpy.run()