from django import forms
from .models import AcademicMobilityOrder

class AcademicMobilityOrderFormTeacher(forms.ModelForm):
    class Meta:
        model = AcademicMobilityOrder  
        fields = ['file1','file2','notes']
        exclude = ['user','data_create','status','is_approved','updated','created']
        labels = {
            
            'file1': 'الملف الإداري',
            'file2': 'الملف العلمي',
            'notes': 'الملاحظات',   
        }
        widgets = {
            'file1': forms.FileInput(attrs={'class': 'form-control'}),
            'file2': forms.FileInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            
        }



        