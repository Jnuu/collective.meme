# -*- coding: utf-8 -*-
from collective.memes.content.meme import IMeme  # NOQA E501
from collective.memes.testing import COLLECTIVE_MEMES_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject, queryUtility

import unittest


class MemeIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_MEMES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_meme_schema(self):
        fti = queryUtility(IDexterityFTI, name='Meme')
        schema = fti.lookupSchema()
        self.assertEqual(IMeme, schema)

    def test_ct_meme_fti(self):
        fti = queryUtility(IDexterityFTI, name='Meme')
        self.assertTrue(fti)

    def test_ct_meme_factory(self):
        fti = queryUtility(IDexterityFTI, name='Meme')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IMeme.providedBy(obj),
            u'IMeme not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_meme_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Meme',
            id='meme',
        )

        self.assertTrue(
            IMeme.providedBy(obj),
            u'IMeme not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('meme', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('meme', parent.objectIds())

    def test_ct_meme_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Meme')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_meme_filter_content_type_false(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Meme')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'meme_id',
            title='Meme container',
        )
        self.parent = self.portal[parent_id]
        obj = api.content.create(
            container=self.parent,
            type='Document',
            title='My Content',
        )
        self.assertTrue(
            obj,
            u'Cannot add {0} to {1} container!'.format(obj.id, fti.id)
        )
