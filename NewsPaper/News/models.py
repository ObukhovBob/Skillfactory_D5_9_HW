from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django import forms
from allauth.account.forms import SignupForm


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user}'

    @classmethod
    def update_rating(cls):
        authors = Author.objects.all()
        for author in authors:
            summ = 0
            posts_rating = Post.objects.filter(author=author)
            for post_rate in posts_rating:
                summ += int(post_rate.rating)
            summ = summ * 3
            comments_rating = Comment.objects.filter(post__author=author)
            for comment_rate in comments_rating:
                summ += int(comment_rate.rating)
            author_comments = Comment.objects.filter(user_id=author.user_id)
            for author_comment in author_comments:
                summ += int(author_comment.rating)
            author.rating = summ
            author.save()


class Category(models.Model):
    category_name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f'{self.category_name}'


class Post(models.Model):
    article = 'AR'
    news = 'NW'
    POSITIONS = [(article, 'Статья'), (news, 'Новость')]

    header = models.CharField(max_length=128)
    rating = models.IntegerField(default=0)
    text = models.TextField()
    content_type = models.CharField(max_length=2, choices=POSITIONS, default=news)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:127] + "..."

    def get_absolute_url(self):
        return reverse('article', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    com_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
