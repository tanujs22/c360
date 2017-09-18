from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout

User = get_user_model()
class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		user_qs = User.objects.filter(username=username)
		if user_qs.count() == 1:
			user
		if not user:
			raise forms.ValidationError("No User!")

		if not user.check_password(password):
			raise forms.ValidationError("Wrong Password!")

		if not user.is_active:
			raise forms.ValidationError("User deactive!")

		return super(UserLoginForm, self).clean()

class UserRegisterForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password'
		]
	def clean_email(self):
		email = self.cleaned_data.get('email')
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This email already exists!")
		return email