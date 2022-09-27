# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.memes -t test_meme.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.memes.testing.COLLECTIVE_MEMES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/collective/memes/tests/robot/test_meme.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Meme
  Given a logged-in site administrator
    and an add Meme form
   When I type 'My Meme' into the title field
    and I submit the form
   Then a Meme with the title 'My Meme' has been created

Scenario: As a site administrator I can view a Meme
  Given a logged-in site administrator
    and a Meme 'My Meme'
   When I go to the Meme view
   Then I can see the Meme title 'My Meme'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Meme form
  Go To  ${PLONE_URL}/++add++Meme

a Meme 'My Meme'
  Create content  type=Meme  id=my-meme  title=My Meme

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Meme view
  Go To  ${PLONE_URL}/my-meme
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Meme with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Meme title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
