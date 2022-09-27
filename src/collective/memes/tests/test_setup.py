# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.memes.testing import COLLECTIVE_MEMES_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.memes is properly installed."""

    layer = COLLECTIVE_MEMES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.memes is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.memes'))

    def test_browserlayer(self):
        """Test that ICollectiveMemesLayer is registered."""
        from collective.memes.interfaces import (
            ICollectiveMemesLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveMemesLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_MEMES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.memes'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.memes is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.memes'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveMemesLayer is removed."""
        from collective.memes.interfaces import \
            ICollectiveMemesLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ICollectiveMemesLayer,
            utils.registered_layers())
