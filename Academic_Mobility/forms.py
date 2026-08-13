from django import forms
from .models import AcademicMobilityOrder

class AcademicMobilityOrderFormTeacher(forms.ModelForm):
    class Meta:
        model = AcademicMobilityOrder  
        fields = ['file1','file2','notes']
        exclude = ['user','data_create','status','is_approved','updated','created']
       
       
    file1 = forms.FileField(
        required=True, 
        label='الملف الإداري',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    file2 = forms.FileField(
        required=True,  # Set to True if this is also mandatory
        label='الملف العلمي',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    notes = forms.CharField(
        required=False, 
        label='الملاحظات',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )



        