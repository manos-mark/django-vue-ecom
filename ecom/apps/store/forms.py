from django import forms

from .models import Category, Store, Product

class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        stores = kwargs.pop('stores')

        super(CategoryForm, self).__init__(*args, **kwargs)

        for key in self.fields:                
            self.fields[key].widget.attrs['class'] = 'input'

        self.fields['is_featured'].widget.attrs['class'] = 'radio'
        self.fields['image'].widget.attrs['class'] = 'file'

        # self.fields['store'].choices = [(store.id, str(store)) for store in stores] #Store.objects.filter(slug__in=[store.slug for store in stores])
       
        categories = Category.objects.filter(store__in=stores)
        parent_choices = [(category.id, str(category)) for category in categories]
        parent_choices.append(('','---------'))
        self.fields['parent'].choices = parent_choices

    class Meta: 
        model = Category
        fields = '__all__'
        exclude = ['slug', 'store']

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        stores = kwargs.pop('stores')

        super(ProductForm, self).__init__(*args, **kwargs)

        for key in self.fields:                
            self.fields[key].widget.attrs['class'] = 'input'

        self.fields['is_featured'].widget.attrs['class'] = 'radio'
        self.fields['image'].widget.attrs['class'] = 'file'

        # self.fields['store'].choices = [(store.id, str(store)) for store in stores] 
       
        categories = Category.objects.filter(store__in=stores)
        self.fields['category'].choices = [(category.id, str(category)) for category in categories]

    class Meta: 
        model = Product
        fields = '__all__'
        exclude = ['slug', 'last_visit', 'thumbnail', 'num_visits', 'store']