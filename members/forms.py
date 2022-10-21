from django import forms
import re
from django.contrib.auth.models import User
from speech.models import Section


class RegistrationmForm(forms.Form):
    username = forms.CharField(label='Tài khoản', max_length=30, widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': "form-control"}))
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(attrs={'class': "form-control"}))
    password2 = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput(attrs={'class': "form-control"}))

    def clean_password2(self):
        password1 = ""
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            if not re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password1):
                raise forms.ValidationError("Mật khẩu phải có tối thiểu tám ký tự, ít nhất một chữ cái viết hoa, một chữ cái viết thường, một số và một ký tự đặc biệt:")
        else:
            raise forms.ValidationError("Bạn hãy nhập mật khẩu")
        if 'password2' in self.cleaned_data:
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            else:
                raise forms.ValidationError("Nhập lại mật khẩu khác mật khẩu")
        raise forms.ValidationError("Chưa nhập lại mật khẩu")

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Tên tài khoản có kí tự đặc biệt")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Tài khoản đã tồn tại")

    def save(self):
        User.objects.create_user(username=self.cleaned_data['username'],
                                 email=self.cleaned_data['email'],
                                 password=self.cleaned_data['password1'])
        Section.objects.create(username=User.objects.get(username=self.cleaned_data['username']),
                               section_name="hidden_section").save()
