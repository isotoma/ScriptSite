from lxml import etree
from datetime import datetime

from scriptsite.main.models import TestScript, TestGroup, SingleTest, TestRun

def get_xml_doc(path):
    """ Open the xml file from disk and return it as an etree """
    xml_file = open(path).read()
    xml_doc = etree.fromstring(xml_file)
    return xml_doc

def get_number_of_tests(script):
    """ Get the total number of tests in the document """
    xml_doc = get_xml_doc(script.script_file.path)
    
    tests = xml_doc.xpath('//test')
    
    return len(tests)


def convert_script_to_models(script):
    """ Explode the incoming xml file into database models and save them """
    
    def get_value(element, value):
        if element.find(value) is not None:
            return element.find(value).text
        return None

    # get the xml doc from the script
    xml_doc = get_xml_doc(script.script_file.path)
    
    test_run = TestRun()
    test_run.date_started = datetime.now()
    test_run.test_script = script
    test_run.save()
    
    # convert the doc into models
    test_groups = xml_doc.xpath('//test_group')
    
    for group in test_groups:
        group_model = TestGroup()
        group_model.test_script = script
        group_model.test_run = test_run
        group_model.name = group.attrib['name']
        group_model.save()
        
        for test in group.xpath('./test'):
            test_model = SingleTest()
            test_model.name = get_value(test, 'name')
            test_model.story_id = get_value(test, 'story_id')
            test_model.steps = get_value(test, 'steps')
            test_model.expected_results = get_value(test, 'expected_result')
            test_model.automated_test_id = get_value(test, 'automated_test_id')
            test_model.test_group = group_model
            test_model.save()
            
    return test_run
            

    
