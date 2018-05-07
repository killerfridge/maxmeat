from django.test import TestCase
from django.utils import timezone
import datetime
from .models import Question
from django.urls import reverse
# Create your tests here.


def create_question(question_text, days):
    time =timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        '''
        if no question exists, an appropriate message is displayed
        :return:
        '''
        response = self.client.get(reverse('poll:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['recent_question_list'], [])

    def test_past_question(self):
        '''
        questions with a pub_date in the past are displayed on the index page
        :return:
        '''
        create_question(question_text='Past Question', days=-30)
        response = self.client.get(reverse('poll:index'))
        self.assertQuerysetEqual(
            response.context['recent_question_list'], ['<Question: Past Question>']
        )

    def test_future_quesiton(self):
        '''
        questions with a pub_date in the future are not displayed on the index page
        :return:
        '''
        create_question(question_text='Future Question', days=30)
        response = self.client.get(reverse('poll:index'))
        self.assertQuerysetEqual(
            response.context['recent_question_list'], []
        )
        self.assertContains(response, 'No polls are available.')

    def test_future_and_past_questions(self):
        '''
        even if both future and past questions are present, only past ones are displayed
        :return:
        '''
        create_question(question_text='Past Question', days=-30)
        create_question(question_text='Future Question', days=30)

        response = self.client.get(reverse('poll:index'))
        self.assertQuerysetEqual(
            response.context['recent_question_list'], ['<Question: Past Question>']
        )

    def test_two_past_questions(self):
        '''
        The questions index should display multiple questions
        :return:
        '''
        create_question(question_text='Past Question', days=-30)
        create_question(question_text='Past Question 2', days=-30)

        response = self.client.get(reverse('poll:index'))
        self.assertQuerysetEqual(
            response.context['recent_question_list'],
            ['<Question: Past Question>', '<Question: Past Question 2>']
        )


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        '''
        was_published_recently() returns false for questions
        whose pub_date is in the future
        :return:
        '''
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):

        time = timezone.now() - datetime.timedelta(days=1)
        past_question = Question(pub_date=time)
        self.assertIs(past_question.was_published_recently(), True)

    def test_was_published_recently_with_old_question(self):

        time = timezone.now() - datetime.timedelta(days=30)
        past_question = Question(pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        '''
        the detail view of a question with a pub_date in the future
        should return a 404
        :return:
        '''

        future_question = create_question('Future Question', days=10)
        url = reverse('poll:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        '''
        the detail of a past question should display the question's text
        :return:
        '''

        past_question = create_question('Past Question', days=-5)
        url = reverse('poll:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)