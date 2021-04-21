from django import forms


class DummyForm(forms.Form):
    form_text = forms.CharField(label="Review", min_length=3, max_length=20)
    form_grade = forms.IntegerField(label="Grade", min_value=1, max_value=100)
    form_image = forms.FileField(label="Image", required=False)

    def clean_text(self):
        if 'Add' not in self.cleaned_data['text']:
            raise forms.ValidationError('You need "Add" in text')

