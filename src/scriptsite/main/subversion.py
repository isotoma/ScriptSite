import tempfile
import os
import shutil
from datetime import datetime

import pysvn
from lxml import etree 

from django.core.files import File

from scriptsite import settings
from scriptsite.main.models import TestScript

def make_script_model_from_file(script_file, flavour, revision):
    """ Create a model object from the file that we have created """
    ts = TestScript()
    ts.flavour = flavour
    ts.date_uploaded = datetime.now()
    ts.script_file.save(flavour + '.xml', File(file(script_file)), save = False)
    ts.revision = revision
    return ts

def get_output_directory(root_path):
    final_path = os.path.join(root_path, 'processed')
    return final_path

def make_script_file_from_checkout(root_path, flavour):
    """ Take our export, turn it into the single canonical XML file """
    path_to_config = os.path.join(root_path, flavour + '.xml')
    config_file = open(path_to_config).read()
    
        # parse the config file into memory
    config_tree = etree.fromstring(config_file)

    final_test_doc = etree.Element("test_doc")
    # find all the mbots in the config file
    for mbot in config_tree.findall('mbot'):


        final_mbot_element = etree.Element('test_group')
        final_mbot_element.attrib['name'] = mbot.attrib['name']

        name = mbot.attrib['name']
        # available tests should live in a directory matching the name of the mbot
        test_dir = os.path.join(root_path, name)
        directory_available_tests = os.listdir(test_dir)
        # make sure we only have xml files
        available_tests = [x for x in directory_available_tests if x.endswith('.xml') and not x == name + '.xml']
        # get the filenames to exclude from the config file
        # add .xml as tests are specified by id, not filenames....
        excluded_tests = [test.text +".xml" for test in mbot.findall('exclude')]

        test_list = [os.path.join(test_dir, test) for test in available_tests if test not in excluded_tests]

        test_list = sorted(test_list)

        # Append our tests to the master test document
        for test in test_list:
            parsed_test = etree.parse(test)
            final_mbot_element.append(parsed_test.getroot())

        # add the metadata for the test
        metadata = etree.parse(os.path.join(test_dir, name +'.xml'))
        for child in metadata.getroot().getchildren():
            final_mbot_element.append(child)

        final_test_doc.append(final_mbot_element)



    file_generation_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    final_test_doc.attrib['flavour'] = flavour
    final_test_doc.attrib['generated'] = file_generation_time
    final_test_doc.append(config_tree.find('script_version'))
    
    
    # we are done here, write it to the same directory as the uploaded ones,
    # and return
    output_dir = get_output_directory(root_path)
    os.makedirs(output_dir)
    output_file = open(os.path.join(output_dir, flavour + ".xml"), 'w')
    s = etree.tostring(final_test_doc, pretty_print = True).encode('UTF-8')
    output_file.write(s)
    return output_file.name



def get_from_subversion(repo_url, revision, username, password, flavour):
    """ Get the XML file from subversion """
    svn_username = username
    svn_password = password

    # make a directory to checkout to
    temp_dir = tempfile.mkdtemp()
    export_dir = os.path.join(temp_dir, 'export')
    print export_dir
    
    # Get a checkout
    client = pysvn.Client()
    
    #set auth details
    client.set_default_username(username)
    client.set_default_password(password)
    
    try:
        # attempt an export (we don't need a checkout, just the files)
        client.export(repo_url, export_dir)
    finally:
        # just in case
        client.set_default_username("")
        client.set_default_password("")
    
    try:
        # so, we've got stuff from subversion
        # we should probably do something with it, no?
        script_file = make_script_file_from_checkout(export_dir, flavour)
        # now we have the file, make a db model
        ts = make_script_model_from_file(script_file, flavour, "0")
        ts.save()
    finally:
        # tidy up
        shutil.rmtree(temp_dir)
        
    # aand we're done, let's get out of here
    return ts