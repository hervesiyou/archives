
from django import forms
from django.forms import CheckboxInput
from arch_portal.use_cases.services.core import compute_sha1
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column,Field
from arch_portal.domain.models.membre import Membre 

class MembreForm(forms.ModelForm):
   
    pwd = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
        label="Mot de passe"
    )
    fichier_image = forms.ImageField(
        required=False,
        label="Photo de profil",
        widget=forms.FileInput(attrs={
            'class':'form-control',
            "accept":'image/*'
        }),
        
    )
    class Meta:
        model = Membre
        exclude = ["etatvalidation","dateinscription","approbateurs","galeries", "token" ]
        
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'cols': 50,
                'class': 'form-control',
                'placeholder': 'Décrivez le membre...'
            })
        }

        labels = {
            "login":"Login ou Pseudonyme",
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False 
        self.helper.layout = Layout(
            Row(
                Column('nomcomplet', css_class='col-md-8'),
                Column('generation', css_class='col-md-4'),
                
                Column('fichier_image', css_class='col-md-12'), 
                Column('description', css_class='col-md-12'),
                Column('login', css_class='col-md-6'),
                Column(
                    Field('pwd', type='password', css_class='form-control'),
                    css_class='col-md-6',
                ),
                # Column('pwd', css_class='col-md-6'),

                Column('email', css_class='col-md-6'),
                Column('telephone', css_class='col-md-6'),
                Column('type', css_class='col-md-2'), 
                Column('sexe', css_class='col-md-2'), 
                Column('etatcivil', css_class='col-md-2'), 
                Column('nbenfant', css_class='col-md-2'), 
                Column('vivant', css_class='col-md-2'), 
                Column('datedeces', css_class='col-md-2'), 
                Column('datenaissance', css_class='col-md-3'), 
                Column('lieunaissance', css_class='col-md-3'), 
                Column('residence', css_class='col-md-3'), 
                Column('notabilite', css_class='col-md-3'), 
                css_class='row'
            ),
            Row(
                Column('education', css_class='col-md-3'), 
                Column('diplomes', css_class='col-md-3'), 
                Column('profession', css_class='col-md-3'), 
                Column('associations', css_class='col-md-3'), 
                Column('familles', css_class='col-md-8'), 
                Column('communautes', css_class='col-md-4'), 
                Column('pere', css_class='col-md-3'), 
                Column('mere', css_class='col-md-3'), 
                Column('nompere', css_class='col-md-3'), 
                Column('nommere', css_class='col-md-3'), 
                
                css_class='row'
            ),
        )

class MembreEditForm(forms.ModelForm):

    fichier_image = forms.ImageField(
        required=False,
        label="Photo de profil",
        widget=forms.FileInput(attrs={
            'class':'form-control',
            "accept":'image/*'
        }),
        
    )
    delete_photo = forms.BooleanField(
        required=False,
        label="Supprimer la photo actuelle"
    )
     
    class Meta:
        model = Membre
        exclude = ["etatvalidation","dateinscription","approbateurs","galeries" ]
        # fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            if isinstance(field.widget, CheckboxInput):
                field.widget.attrs.update({
                    'class': 'form-check-input'
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control'
                })

        # for field in self.fields.values():
        #     print(field)
        #     field.widget.attrs.update({
        #         'class': 'form-control'
        #     })

class UsersLoginForm(forms.ModelForm):
    pwd = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    login = forms.CharField( label="Login ou Pseudonyme")

    class Meta:
        model = Membre
        fields = ['login','pwd']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('login', css_class='form-control'),
            Field('pwd',type='password', css_class='form-control'),
        )

class UsersSubscribeForm(forms.ModelForm):
    
    pwd = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Mot de passe'
        }),
        label="Mot de passe"
    ) 

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe'
        }),
        label="Confirmer le mot de passe",
    )
    
    class Meta:
        model = Membre
        fields = ["nomcomplet", "email", "telephone", "sexe", "datenaissance", "lieunaissance", "residence", "login", "pwd", "password_confirm"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        # Labels et help_text
        self.fields["login"].label = 'Login ou Pseudonyme'
        self.fields['login'].help_text = "Le login ou pseudonyme que vous allez utiliser pour vous connecter."

        # Configuration Crispy Forms
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'row g-3'          # Très important
        
        self.helper.layout = Layout(
            Row(
                Column(Field('nomcomplet'), css_class='col-12'),
                Column(Field('email'), css_class='col-12 col-md-6'),
                Column(Field('telephone'), css_class='col-12 col-md-6'),
                Column(Field('sexe'), css_class='col-12 col-md-4'),
                Column(Field('datenaissance'), css_class='col-12 col-md-4'),
                Column(Field('lieunaissance'), css_class='col-12 col-md-4'),
                css_class='row'
            ),
            Row(
                Column(Field('login'), css_class='col-12'),
                Column(Field('pwd'), css_class='col-12 col-md-6'),
                Column(Field('password_confirm'), css_class='col-12 col-md-6'),
                css_class='row'
            ),
        )

"""
class UsersSubscribeForm(forms.ModelForm):
    
    pwd = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
        label="Mot de passe"
    ) 

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe'
        }),
        label="Confirmer le mot de passe",
    )
    
    class Meta:
        model = Membre
        # exclude = ["etatvalidation","dateinscription","approbateurs","galeries" ]
        fields = ["nomcomplet", "email","telephone","sexe","datenaissance","lieunaissance","residence", "login", "pwd", "password_confirm"]
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['pwd'].widget = forms.PasswordInput(render_value=False)
        self.fields["login"].label = 'Login ou Pseudonyme'
        self.fields['login'].help_text = "Le login ou pseudonyme que vous allez utiliser  pour vous connecter ."

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'row g-3'
        self.helper.layout = Layout(
            Row(
                Column('nomcomplet', css_class='col-12 col-md-12'),
                Column('email', css_class='col-12 col-md-6'),
                Column('telephone', css_class='col-12 col-md-6'),
                Column('sexe', css_class='col-12 col-md-4'),
                Column('datenaissance', css_class='col-12 col-md-4'),
                Column('lieunaissance', css_class='col-12 col-md-4'),
                css_class='row'
            ),
            Row(
                Column('login', css_class='col-12'),
                Column('pwd', css_class='col-12 col-md-6'),
                Column('password_confirm', css_class='col-12 col-md-6'),
                css_class='row'
            ),
            # Row(
            #     Column('nomcomplet', css_class='col-md-12'),   
            #     Column('email', css_class='col-md-6'),
            #     Column('telephone', css_class='col-md-6'),
            #     # Column('type', css_class='col-md-2'), 
            #     Column('sexe', css_class='col-md-4'), 
            #     Column('datenaissance', css_class='col-md-4'), 
            #     Column('lieunaissance', css_class='col-md-4'),  
            #     css_class='row'
            # ),
            # Row(
            #     Column('login', css_class='col-md-12'),
            #     Column('pwd', css_class='col-md-6'),
            #     Column('password_confirm', css_class='col-md-6'),
            #     css_class='row g-3'
            # ),
            
        )


    def clean(self):
        cleaned_data = super().clean()
        nom = cleaned_data.get("nomcomplet")
        sexe = cleaned_data.get("sexe")
        login = cleaned_data.get("login")
        if Membre.objects.filter(nomcomplet=nom, sexe=sexe, login=login).exists():
            raise forms.ValidationError("Ce membre existe dejà ! ")
        
        pwd = cleaned_data.get("pwd")
        pwd_confirm = cleaned_data.get("password_confirm")

        if pwd and pwd_confirm and pwd != pwd_confirm:
            raise forms.ValidationError("Les deux mots de passe ne correspondent pas.")

        return cleaned_data
        

    def save(self, commit=True):
        user = super().save(commit=False)
        user.pwd = compute_sha1(self.cleaned_data['pwd']) 
        if commit:
            user.save()
        return user
    
"""