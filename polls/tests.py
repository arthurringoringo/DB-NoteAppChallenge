from django.test import TestCase
from django.utils import timezone
import datetime
from.models import *
from django.urls import reverse


# Create your tests here.

def create_question(question_text,days):
    """
    crate a question with the given 'question_text'and published the
    given number of 'days' offset to now (negative for question publisehd
    in the pas, positive for question that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text = question_text, pub_date=time)

def create_choice(questionID,choice_text):
    """
    Create a choice for a question with the given choice text and the question PK
    """
    return Choice.objects.create(question = questionID, choice_text = choice_text)

def create_choice_result(questionID,choice_text,votes):
    """
    Create a choice for a question with the given choice text and the question PK
    """
    return Choice.objects.create(question = questionID, choice_text = choice_text,votes=votes)


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(),False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns false for questions whose pub_date
        is older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(),False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_publishedrecently() returns True for questions whose pub_date
        is within the last day
        """
        time=timezone.now() - datetime.timedelta(hours=23,minutes=59,seconds=59)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(),True)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

    def test_no_display_no_choice_question(self):
        """ 
       The question index page cannot display question without choices
        """
        create_question(question_text="Question No choices",days=-1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Question No choices>']
        )
    
    def test_noChoiceQuestion_and_QuestionWchoice(self):
        """
        This test shows that only question with choice is displaed and not with question that
        dosent have choice
        """
        q2=create_question(question_text="Question with Choices",days=-1)
        c1=create_choice(questionID = q2,choice_text="Question with choice")
        q2.save()
        c1.save()
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Question with Choices>']
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionResultViewTest(TestCase):
    def test_display_question_choices(self):
        """
        This test shows question's choices that has more or equal than 1 votes
        and dosent show choices that dosent have votes
        """
        q1=create_question(question_text='Test question',days=-1)
        c1=create_choice_result(questionID=q1,choice_text='choice 1',votes=0)
        c2=create_choice_result(questionID=q1,choice_text='choice 2',votes=2)
        q1.save()
        c1.save()
        c2.save()
        expected=[q1,c2]
        response =  self.client.get(reverse('polls:results', args=(q1.id,)))
        self.assertContains(response,c2)