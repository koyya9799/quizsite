from django.http import HttpResponse
from .models import Quiz, Question, Answer, QuizResult


def home(request):
    return HttpResponse("Welcome to the Quizz Website!")
from django.shortcuts import render

def home(request):
    return render(request, 'quiz/home.html')

from django.http import HttpResponse

def login_view(request):
    return HttpResponse("Login Page (coming soon)")

def register_view(request):
    return HttpResponse("Register Page (coming soon)")

from django.shortcuts import render

def login_view(request):
    return render(request, 'quiz/login.html')

from django.shortcuts import render

def register_view(request):
    return render(request, 'quiz/register.html')

from django.contrib.auth.decorators import login_required
from .models import Quiz

@login_required
def dashboard_view(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/dashboard.html', {'quizzes': quizzes})

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')  # 👈 Redirect to dashboard
        else:
            return render(request, 'quiz/login.html', {'error': 'Invalid credentials'})
    return render(request, 'quiz/login.html')

from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'quiz/register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'quiz/register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password1)
        user.save()

        # ✅ Redirect to login page after successful registration
        return redirect('login')

    return render(request, 'quiz/register.html')


from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_superuser

def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'quiz/admin_login.html', {'error': 'Invalid admin credentials'})

    return render(request, 'quiz/admin_login.html')


@user_passes_test(is_admin)
def admin_dashboard_view(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/admin_dashboard.html', {'quizzes': quizzes})


from django.views.decorators.csrf import csrf_exempt

@user_passes_test(is_admin)
@csrf_exempt
def add_quiz_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        time_limit = request.POST.get('time_limit')

        Quiz.objects.create(
            title=title,
            description=description,
            created_by=request.user,
            time_limit=int(time_limit)
        )
        return redirect('admin_dashboard')

@user_passes_test(is_admin)
def delete_quiz_view(request, quiz_id):
    Quiz.objects.filter(id=quiz_id).delete()
    return redirect('admin_dashboard')
@user_passes_test(is_admin)
def add_question_view(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)

    if request.method == 'POST':
        question_text = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        correct_option = request.POST.get('correct')  # value: '1', '2', '3', or '4'

        # Create question
        question = Question.objects.create(quiz=quiz, text=question_text)

        # Create answers
        Answer.objects.create(question=question, text=option1, is_correct=(correct_option == '1'))
        Answer.objects.create(question=question, text=option2, is_correct=(correct_option == '2'))
        Answer.objects.create(question=question, text=option3, is_correct=(correct_option == '3'))
        Answer.objects.create(question=question, text=option4, is_correct=(correct_option == '4'))

        return redirect('admin_dashboard')

    return render(request, 'quiz/add_question.html', {'quiz': quiz})

@user_passes_test(is_admin)
def add_question_view(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)

    if request.method == 'POST':
        # Get form data
        question_text = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        correct_option = request.POST.get('correct')

        # Create question
        question = Question.objects.create(quiz=quiz, text=question_text)

        # Create answers
        Answer.objects.create(question=question, text=option1, is_correct=(correct_option == '1'))
        Answer.objects.create(question=question, text=option2, is_correct=(correct_option == '2'))
        Answer.objects.create(question=question, text=option3, is_correct=(correct_option == '3'))
        Answer.objects.create(question=question, text=option4, is_correct=(correct_option == '4'))

        # Check what admin clicked: "Add Another" or "Finish"
        if 'add_another' in request.POST:
            return redirect('add_question', quiz_id=quiz.id)
        else:
            return redirect('show_questions', quiz_id=quiz.id)

    return render(request, 'quiz/add_question.html', {'quiz': quiz})

@user_passes_test(is_admin)
def show_questions_view(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz).prefetch_related('answer_set')

    return render(request, 'quiz/show_questions.html', {
        'quiz': quiz,
        'questions': questions
    })

@login_required
def start_quiz_view(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz).prefetch_related('answer_set')
    return render(request, 'quiz/start_quiz.html', {'quiz': quiz, 'questions': questions})

from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # ✅ Ensure this matches your dashboard URL name
        else:
            error = "Invalid username or password."
            return render(request, 'quiz/login.html', {'error': error})

    return render(request, 'quiz/login.html')

from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/dashboard.html', {'quizzes': quizzes})


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Quiz, Question, Answer, QuizResult

@login_required
def start_quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz).prefetch_related('answer_set')

    if request.method == 'POST':
        score = 0
        total = questions.count()

        for question in questions:
            selected = request.POST.get(f"question_{question.id}")
            if selected:
                correct_answer = Answer.objects.filter(question=question, is_correct=True).first()
                if correct_answer and str(correct_answer.id) == selected:
                    score += 1

        # Save result to database
        QuizResult.objects.create(user=request.user, quiz=quiz, score=score, total=total)

        return render(request, 'quiz/quiz_submitted.html', {
            'quiz': quiz,
            'score': score,
            'total': total
        })

    return render(request, 'quiz/start_quiz.html', {
        'quiz': quiz,
        'questions': questions
    })

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # ✅ Make sure this matches the name of the dashboard URL
        else:
            error = "Invalid username or password."
            return render(request, 'quiz/login.html', {'error': error})

    return render(request, 'quiz/login.html')
