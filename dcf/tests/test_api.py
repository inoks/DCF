# -*- coding:utf-8 -*-

from rest_framework.test import APITestCase, APIRequestFactory, APIClient, force_authenticate

from django.contrib.auth import get_user_model

from dcf.models import Item, Group, Section
from dcf.api.viewsets import GroupViewSet, SectionViewSet, ItemViewSet


class ApiTestCase(APITestCase):

    def setUp(self):

        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.section = Section.objects.create(title=u'TestSection')
        self.group = Group.objects.create(
            title=u'TestGroup',
            section=self.section
        )
        self.admin = get_user_model().objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.user = get_user_model().objects.create(username=u'username2')
        self.item1 = Item.objects.create(
            user=self.admin,
            group=self.group,
            title=u'testitem1',
            description=u'test descr',
            price=1000.00,
            phone='8-800-9000-900'
        )
        self.item2 = Item.objects.create(
            user=self.user,
            group=self.group,
            title=u'testitem2',
            description=u'test descr',
            price=2000.00,
            phone='8-800-7800-123'
        )

    def test_groups_api(self):
        response = self.client.get('/api/groups/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/groups/1/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/groups/10/')
        self.assertEqual(response.status_code, 404)

        response = self.client.post('/api/groups/', {
            "title": "test",
            "section": 1
        })
        self.assertEqual(response.status_code, 403)

        response = self.client.put('/api/groups/1/', {})
        self.assertEqual(response.status_code, 403)

        response = self.client.delete('/api/groups/1/', {})
        self.assertEqual(response.status_code, 403)

        view = GroupViewSet.as_view({
            'post': 'create',
            'put': 'update',
            'delete': 'destroy'
        })
        request = self.factory.post('/api/groups/', {
            "title": "test",
            "section": 1
        })
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 403)
        force_authenticate(request, user=self.admin)
        response = view(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.put('/api/groups/1/', {
            "title": "test updating groups",
            "section": 1
        })
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 403)
        force_authenticate(request, user=self.admin)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)

        request = self.factory.delete('/api/groups/1/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 403)
        force_authenticate(request, user=self.admin)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)

    def test_sections_api(self):
        response = self.client.get('/api/sections/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/sections/1/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/sections/10/')
        self.assertEqual(response.status_code, 404)

        response = self.client.post('/api/sections/', {
            "title": "test"
        })
        self.assertEqual(response.status_code, 403)

        response = self.client.put('/api/sections/1/', {})
        self.assertEqual(response.status_code, 403)

        response = self.client.delete('/api/sections/1/', {})
        self.assertEqual(response.status_code, 403)

        view = SectionViewSet.as_view({
            'post': 'create',
            'put': 'update',
            'delete': 'destroy'
        })
        request = self.factory.post('/api/groups/', {
            'title': 'new group'
        })
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 403)
        force_authenticate(request, user=self.admin)
        response = view(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.put('/api/groups/1/', {
            'title': 'update group'
        })
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 403)
        force_authenticate(request, user=self.admin)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)

        request = self.factory.delete('/api/groups/1/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 403)
        force_authenticate(request, user=self.admin)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)

    def test_items_api(self):
        response = self.client.get('/api/items/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/items/1/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/items/10/')
        self.assertEqual(response.status_code, 404)

        response = self.client.post('/api/items/', {})
        self.assertEqual(response.status_code, 403)

        response = self.client.put('/api/items/1/', {})
        self.assertEqual(response.status_code, 403)

        response = self.client.delete('/api/items/1/', {})
        self.assertEqual(response.status_code, 403)

        view = ItemViewSet.as_view({
            'post': 'create',
            'put': 'update',
            'delete': 'destroy'
        })
        request = self.factory.post('/api/items/', {
            "title": "add new item",
            "description": "this is cool item",
            "price": 1200,
            "group": 1
        })
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.put('/api/items/1/', {
            "title": "update title",
            "description": "this is cool item",
            "price": 1200,
            "group": 1
        })
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 403)
        force_authenticate(request, user=self.admin)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)

        request = self.factory.delete('/api/items/1/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 403)
        force_authenticate(request, user=self.admin)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)