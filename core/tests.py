from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import JobOffer, JobOfferPool, CommercialJobOffer
from core.admin import JobOfferAdmin, CommercialJobOfferAdmin
from core.serializers import JobOfferSerializer, CommercialJobOfferSerializer
from core.api import JobOfferViewSet


# Test for JobOffer model
class JobOfferModelTest(TestCase):
    def test_str(self):
        job_offer = JobOffer(name='Software Engineer')
        self.assertEqual(str(job_offer), 'Software Engineer')


# Test for JobOfferAdmin
class JobOfferAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = JobOfferAdmin(JobOffer, self.site)

    def test_list_display(self):
        self.assertEqual(list(self.admin.list_display), ['name', 'description'])


# Test for JobOfferSerializer
class JobOfferSerializerTest(TestCase):
    def test_fields(self):
        serializer = JobOfferSerializer()
        self.assertEqual(set(serializer.fields.keys()), {'pk','name', 'description'})


# Test for JobOfferViewSet
class JobOfferViewSetTestCase(APITestCase):
    def setUp(self):
        self.job_offer = JobOffer.objects.create(name='Software Engineer',
                                                 description='Develop and maintain software applications')
        self.job_offer_pool = JobOfferPool.objects.create(
            job_offer=self.job_offer,
            name='John Doe',
            email='john.doe@example.com',
            tel='+1-202-555-1234',
            formation='Bachelor of Science in Computer Science',
            cv='path/to/cv.pdf',
            experience='5 years of experience in software development',
            skills='Python, Django, RESTful APIs',
            others='Available for remote work'
        )

    def test_list(self):
        response = self.client.get('/api/core/job_offers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('job_offer_pools', response.data[0])

    def test_list_long(self):
        response = self.client.get('/api/core/job_offers/?long=True')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('job_offer_pools', response.data[0])
        self.assertEqual(len(response.data[0]['job_offer_pools']), 1)


class JobOfferPoolViewSetTestCase(APITestCase):
    def setUp(self):
        self.job_offer = JobOffer.objects.create(name='Software Engineer',
                                                 description='Develop and maintain software applications')
    def test_create(self):
        data = {
            'job_offer': self.job_offer.pk,  # The ID of the JobOffer instance this JobOfferPool is related to
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'tel': '+1-202-555-1234',
            'formation': 'Bachelor of Science in Computer Science',
            'cv': SimpleUploadedFile('cv.pdf', b'file_content'),
            # A Django SimpleUploadedFile instance representing the uploaded CV file
            'experience': '5 years of experience in software development',
            'skills': 'Python, Django, RESTful APIs',
            'others': 'Available for remote work'
        }
        response = self.client.post('/api/core/job_offers_pool/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list(self):
        response = self.client.get('/api/core/job_offers_pool/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommercialJobOfferAdminTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = CommercialJobOfferAdmin(CommercialJobOffer, self.site)

    def test_commercial_job_offer_admin(self):
        self.assertTrue(isinstance(self.admin, CommercialJobOfferAdmin))


class CommercialJobOfferSerializerTestCase(TestCase):
    def setUp(self):
        self.commercial_job_offer = CommercialJobOffer.objects.create(
            name='John Doe',
            email='john.doe@example.com',
            tel='+1-202-555-1234',
            sector='Technology',
            business_offer='Software development services',
            others='Available for remote work'
        )

    def test_commercial_job_offer_serializer(self):
        data = CommercialJobOfferSerializer(self.commercial_job_offer).data
        expected_data = {
            'id': self.commercial_job_offer.id,
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'tel': '+1-202-555-1234',
            'sector': 'Technology',
            'business_offer': 'Software development services',
            'others': 'Available for remote work'
        }
        self.assertDictEqual(data, expected_data)


class CommercialJobOfferViewSetTestCase(APITestCase):
    def test_create(self):
        data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'tel': '+1-202-555-1234',
            'sector': 'Technology',
            'business_offer': 'Software development services',
            'others': 'Available for remote work'
        }
        response = self.client.post('/api/core/commercial_job_offers/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list(self):
        response = self.client.get('/api/core/commercial_job_offers/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

