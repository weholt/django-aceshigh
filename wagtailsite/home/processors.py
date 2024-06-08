from typing import Protocol

from aceshigh.protocols import ServerSideContentProcessor
from django import forms
from django.forms import Form
from django.http import HttpRequest


class UpperCaseProcessor(ServerSideContentProcessor):
    TITLE = "Upper Case"

    def get_form_class(self, mode: str | None = None) -> Form | None:
        class TestForm(forms.Form):
            text_to_add = forms.CharField()

        return TestForm

    def process(self, content: str, mode: str | None = None, data: dict = {}) -> str:
        return (
            content.upper()
            + " "
            + data.get("text_to_add", "Lorem Ipsum Dolor Sit Amet")
        )


class PersonalGreetingsProcessor(ServerSideContentProcessor):
    TITLE = "Personalized Greetings"

    def get_form_class(self, mode: str | None = None) -> Form | None:
        class Test1Form(forms.Form):
            name = forms.CharField()
            age = forms.IntegerField()

        return Test1Form

    def process(self, content: str, mode: str | None = None, data: dict = {}) -> str:
        return f"{content} {data.get('name', 'John Doe')}, you are {data.get('age', 30)} years old"


class HelloWorldProcessor(ServerSideContentProcessor):
    TITLE = "Hello world"

    def get_form_class(self, mode: str | None = None) -> Form | None:
        return

    def process(self, content: str, mode: str | None = None, data: dict = {}) -> str:
        return f"Hello world {content}!"
