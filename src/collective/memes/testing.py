# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import collective.memes


class CollectiveMemesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.memes)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.memes:default')


COLLECTIVE_MEMES_FIXTURE = CollectiveMemesLayer()


COLLECTIVE_MEMES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_MEMES_FIXTURE,),
    name='CollectiveMemesLayer:IntegrationTesting',
)


COLLECTIVE_MEMES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_MEMES_FIXTURE,),
    name='CollectiveMemesLayer:FunctionalTesting',
)


COLLECTIVE_MEMES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_MEMES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveMemesLayer:AcceptanceTesting',
)
