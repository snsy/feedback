import unittest
from connections import *
import logging
import string
import random
import usergen
import sst.actions
import datetime


# pymssql connection examples here: https://code.google.com/p/pymssql/wiki/PymssqlExamples

# Add on directory/location of tools. Edit this to change the URL of the tools. Example: /last
TOOLS_DIR = '/last'

# Collect test briefid in a dictionary for easy access
BRIEF_IDS = {'AAAA': '7325D171-85C1-4A99-9773-4FE6659490B5',
             'CIA': '391CAE11-B499-4878-B8D0-EFE59540D516',
             'CIA10/8/2007': '86DF6B24-D02F-4771-B862-B4DCFAE12FF7',
             'CIA4/6/2011_Foodies': 'DC7F2575-4BFC-4597-BB50-EEB2E7C6DB2B',
             'SOCIALMEDIA11/26/2008': '2B97B751-E853-4ED0-A694-E8DA13B809CC',
             'SocialMedia': '9A6B83EA-211A-4D95-9BF3-DEC352898000',
             'AAAA10/3/2006': '8346EB46-80FD-49F2-8738-90A4A4499A6D',
             }

def addSubscription(briefid, **kwargs):
    test_conn = AlchemyConnection()
    cur = test_conn.getCursor()
    sql = """insert into link_subscriber_brief (subscriberid, briefid, status, reason)
             values ('{subscriberid}', '{briefid}', 'S', 'fromFeedback')
             insert into subscriber_brief_profile (subscriberid, briefid)
             values ('{subscriberid}', '{briefid}')
          """.format(briefid=briefid, subscriberid=kwargs['subscriberid'])
    cur.execute(sql)
    cur.close()
    test_conn.close()
    logging.info("""[added subscription] {email} subscribed to {briefid}
                 """.format(email=kwargs['email'], briefid=briefid))


def createAAAASubscriberViaWeb(**kwargs):
    sst.actions.start()
    sst.actions.go_to('https://www2.qa.smartbrief.com/aaaa')
    first_email_box = sst.actions.get_element_by_xpath('//*[@id="signupForm"]/div[5]/div[2]/input')
    confirm_email_box = sst.actions.get_element_by_xpath('//*[@id="signupForm"]/div[6]/div[2]/input')
    # use sst.actions function to 'type' into text box
    sst.actions.write_textfield(first_email_box, kwargs['email'])
    sst.actions.write_textfield(confirm_email_box, kwargs['email'])
    # get signup button element and click submit
    submit_button_page1 = sst.actions.get_element_by_css('#SignupDiv')
    sst.actions.click_element(submit_button_page1)
    # complete page 2: first get the elements
    sst.actions.sleep(3)
    sst.actions.stop()


def createCIASubscriberViaWeb(**kwargs):
    sst.actions.start()
    sst.actions.go_to('https://www2.qa.smartbrief.com/cia')
    # Get elements on page
    first_email_box = sst.actions.get_element_by_xpath('//input[@name="email"]')
    confirm_email_box = sst.actions.get_element_by_xpath('//input[@name="confirmEmail"]')
    first_name = sst.actions.get_element_by_xpath('//input[@name="firstName"]')
    last_name = sst.actions.get_element_by_xpath('//input[@name="lastName"]')
    company = sst.actions.get_element_by_xpath('//input[@name="company"]')
    title = sst.actions.get_element_by_xpath('//input[@name="title"]')
    zipcode = sst.actions.get_element_by_xpath('//input[@name="zipcode"]')
    country = sst.actions.get_element_by_xpath('//select[@name="country"]')
    position_level = sst.actions.get_element_by_xpath('//select[@name="positionLevel"]')
    company_size = sst.actions.get_element_by_xpath('//select[@name="companySize"]')
    # Complete form
    sst.actions.write_textfield(first_email_box, kwargs['email'])
    sst.actions.write_textfield(confirm_email_box, kwargs['email'])
    sst.actions.write_textfield(first_name, kwargs['first_name'])
    sst.actions.write_textfield(last_name, kwargs['last_name'])
    sst.actions.write_textfield(company, kwargs['company'])
    sst.actions.write_textfield(title, kwargs['title'])
    sst.actions.write_textfield(zipcode, kwargs['zipcode'])
    sst.actions.set_dropdown_value(country, "United States")
    sst.actions.set_dropdown_value(position_level, "Staff")
    sst.actions.set_dropdown_value(company_size, "Less than $1 million")
    # Get signup button and click submit
    submit_button = sst.actions.get_element_by_css('#SignupDiv')
    sst.actions.click_element(submit_button)
    sst.actions.sleep(3)
    sst.actions.stop()


def getSubscriberId(**kwargs):
    test_conn = AlchemyConnection()
    cur = test_conn.getCursor()
    sql = 'SELECT subscriberid from subscriber where email = \'%s\'' % kwargs['email']
    cur.execute(sql)
    results = []  # will be list of
    for row in cur:
        results.append(row['subscriberid'])
    cur.close()
    test_conn.close()
    subscriberid = results.pop()
    subscriberid = str(subscriberid).upper()
    print 'subscriberid returned from getSubscriberId(): %s' % subscriberid
    return subscriberid


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def mergeRoutine(change_me, merge_into_me):
    sst.actions.start()
    sst.actions.go_to('shark.smartbrief.com' + TOOLS_DIR + '/?email=' + change_me['email'])  # look up change_me

    pass


# def createWorkforceSubscriberViaWeb(**kwargs):
#     sst.actions.start()
#     sst.actions.go_to('https://www2.qa.smartbrief.com/aaaa')
#     first_email_box = sst.actions.get_element_by_xpath('//*[@id="signupForm"]/div[5]/div[2]/input')
#     confirm_email_box = sst.actions.get_element_by_xpath('//*[@id="signupForm"]/div[6]/div[2]/input')
#     # use sst.actions function to 'type' into text box
#     sst.actions.write_textfield(first_email_box, kwargs['email'])
#     sst.actions.write_textfield(confirm_email_box, kwargs['email'])
#     # get signup button element and click submit
#     submit_button_page1 = sst.actions.get_element_by_css('#SignupDiv')
#     sst.actions.click_element(submit_button_page1)
#     # complete page 2: first get the elements
#     sst.actions.sleep(10)
#     first_name_field = sst.actions.get_element_by_xpath('//input[@name="firstName"]')
#     last_name_field = sst.actions.get_element_by_xpath('//input[@name="lastName"]')
#     company_field = sst.actions.get_element_by_xpath('//input[@name="company"]')
#     title_field = sst.actions.get_element_by_xpath('//input[@name="title"]')
#     zipcode_field = sst.actions.get_element_by_xpath('//input[@name="zipcode"]')
#     country_field = sst.actions.get_element_by_xpath('//select[@name="country"]')
#     position_level_field = sst.actions.get_element_by_xpath('//select[@name="positionLevel"]')
#     position_function_field = sst.actions.get_element_by_xpath('(//*[@name="positionFunction"])[1]')  # surround w paren
#     company_type_field = sst.actions.get_element_by_xpath('(//select[@name="companyType"])[1]')       # and add index[n]
#     company_size_field = sst.actions.get_element_by_xpath('//select[@name="companySize"]')
#     employees_field = sst.actions.get_element_by_xpath('//select[@name="employees"]')
#     aaaa_custom_field_exists = sst.actions.exists_element(id="9C3D46B6-D106-49F5-9D01-661D9A5D566F")  # boolean
#     submit_button_page2 = sst.actions.get_element_by_css("#SignupDiv")
#     # complete page 2: now, write the fields
#     sst.actions.write_textfield(first_name_field, kwargs['first_name'])
#     sst.actions.write_textfield(last_name_field, kwargs['last_name'])
#     sst.actions.write_textfield(company_field, kwargs['company'])
#     sst.actions.write_textfield(title_field, kwargs['title'])
#     sst.actions.write_textfield(zipcode_field, kwargs['zipcode'])
#     sst.actions.set_dropdown_value(country_field, kwargs['country'])
#     sst.actions.set_dropdown_value(position_level_field, "Staff")
#     sst.actions.set_dropdown_value(position_function_field, "Sales")
#     sst.actions.set_dropdown_value(company_type_field, "Agency: Full-service")
#     sst.actions.set_dropdown_value(company_size_field, "N/A")
#     sst.actions.set_dropdown_value(employees_field, "Less than 10")
#     if aaaa_custom_field_exists:
#         aaaa_custom_field = sst.actions.get_element_by_xpath('//select[@name="memberCategory"]')
#         sst.actions.set_dropdown_value(aaaa_custom_field, "Not applicable")
#         # Click submit button
#     sst.actions.click_element(submit_button_page2)
#     sst.actions.stop()


class AlchemyConnectionTest(unittest.TestCase):

    def testCreateConnection(self):
        test_conn = AlchemyConnection()
        cur = test_conn.getCursor()
        cur.execute('SELECT brief_name, full_brief_name from brief where briefid = %s', BRIEF_IDS['AAAA'])
        results = []  # will be list of
        for row in cur:
            results.append(row['brief_name'])
        cur.close()
        test_conn.close()
        self.assertListEqual(results, ['AAAA'], "Connection to database failed")  # TODO better asserts case


class FunctionTests(unittest.TestCase):
    """
    Test various helper functions here to make sure they work
    """
    def testGetSubscriberId(self):
        test_data = {'subscriberid': 'DD670094-6DD4-4604-8A16-2B2184FB69CB',  # compare our result to this
                     'email': 'snarayanaswamy@smartbrief.com',                # use this email to test the function
                     }
        result = getSubscriberId(**test_data)
        self.assertTrue(result == test_data['subscriberid'])


class SubscriberTest(unittest.TestCase):
    """
    Create a user and subscribe them to AAAA
    """
    def testCreateSubscriber(self):
        """
        Test the function of saving a subscriber. Test verifies that subscriber
        was saved by looking at the value for the 'first_name' key
        in the Python dictionary named data. In this case the value should be
        'Save'. This test will fail of the subscriber is modified after the fact.
        """
        data = {
            'email': 'save_subscriber_' + id_generator() + '@smartbrief.com',
            'first_name': 'Save',
            'last_name': 'Subscriber',
            'title': 'Selenium Tester',
        }
        subscriber = usergen.FeedbackSubscriber(**data)
        subscriber = subscriber.__dict__
        createAAAASubscriberViaWeb(**subscriber)
        test_conn = AlchemyConnection()
        cur = test_conn.getCursor()
        sql = 'SELECT top 250 * from subscriber where email = \'%s\'' % subscriber['email']
        cur.execute(sql)
        logging.info("""[new subscriber] email = {email}\
                     """.format(email=subscriber['email']))
        results = []  # will be list of
        for row in cur:
            results.append(row['email'])
        cur.close()
        test_conn.close()
        self.assertListEqual(results, [subscriber['email']], "Test failure. Is there one row for email = " + subscriber['email'])

    def testMergeSubscriber(self):
        """
        feedback-merge-livelookup@smartbrief.com into feedback-profiletest@smartbrief.com
        """
        logging.info("BEGINNING MERGE TEST")

        change_this_subscriber = {
            'email': 'change_this_subscriber_' + id_generator() + '@smartbrief.com',
            'first_name': 'ChangeThis',
            'last_name': 'Subscriber',
            'title': 'Changer',
            'city': 'Mexico City',
            'country': 'Mexico'
            }
        change_this_subscriber = usergen.FeedbackSubscriber(**change_this_subscriber)
        change_this_subscriber = change_this_subscriber.__dict__
        change_this_subscriber['subscriberid'] = getSubscriberId(**change_this_subscriber)  # set subscriberid
        createAAAASubscriberViaWeb(**change_this_subscriber)
        logging.info("""[new subscriber] email = {email}\
                     """.format(email=change_this_subscriber['email']))

        merge_into_subscriber = {
            'email': 'merge_into_subscriber_' + id_generator() + '@smartbrief.com',
            'first_name': 'ChangeThis',
            'last_name': 'Subscriber',
            'title': 'Changer',
            'city': 'Mexico City',
            'country': 'Mexico'
        }
        merge_into_subscriber = usergen.FeedbackSubscriber(**merge_into_subscriber)
        merge_into_subscriber = merge_into_subscriber.__dict__
        merge_into_subscriber['subscriberid'] = getSubscriberId(**merge_into_subscriber)  # set subscriberid
        createCIASubscriberViaWeb(**merge_into_subscriber)
        logging.info("""[new subscriber] email = {email}\
                     """.format(email=merge_into_subscriber['email']))
        addSubscription(BRIEF_IDS['CIA10/8/2007'], **change_this_subscriber)
        addSubscription(BRIEF_IDS['AAAA10/3/2006'], **merge_into_subscriber)
        # Now that we have our subscriptions, do merge routine
        mergeRoutine(change_this_subscriber, merge_into_subscriber)





        """
        DETAILED MERGE REQUIRMENTS - LIVE LOOKUP PAGE
        ---------------------------------------------
        * *Merge* Verify that subscribers that get merged into another subscriber record are
        ** Unsubscribed from all their trials and briefs
        * *Merge* Verify that subscribers that have records merged into themselves get
        ** The brief subscriptions of the other record, but do not duplicate subscriptions to a main brief, and do not add trials.
        ** The "receiver" record will need one (or more) of its trials unsubscribed IF the "giver" record gives it a parent of those trials
        
        *EXAMPLE OF SUCCESSFUL MERGE*
        
        *Initial state*
        Subscriber A: AAAA, CIA/trial
        Subscriber B: CIA, AAAA/trial
        
        *Operation*
        A merged into --> B
        
        *Final state*
        Subscriber A: no active subscriptions, past subscriptions: AAAA, CIA/trial
        Subscriber B: active subscriptions: AAAA, CIA, past subscriptions: AAAA/trial
        """


def main():
    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    logging.basicConfig(filename='feedback_test.log', level=logging.INFO)
    logging.info("""========STARTING TEST========
                 """ + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    unittest.main()

if __name__ == '__main__':
    main()
