from django import forms

from .models import Category, Store, Product

class EditCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        stores = kwargs.pop('stores')

        super(EditCategoryForm, self).__init__(*args, **kwargs)

        for key in self.fields:              
            self.fields[key].widget.attrs['class'] = 'input'
            # self.fields[key].widget.attrs['v-bind:class'] = "{ 'is-danger': errors.includes("+key+") }"
            if key != 'image':
                self.fields[key].widget.attrs['v-model'] = 'category.'+key

        self.fields['is_featured'].widget.attrs['class'] = 'checkbox'

        self.fields['image'].widget.attrs['class'] = 'file'
        self.fields['image'].widget.attrs['accepts'] = '.jpg, .jpeg, .png'
        self.fields['image'].widget.attrs['v-on:change'] = 'onCategoryFileChange'

        # self.fields['store'].choices = [(store.id, str(store)) for store in stores] #Store.objects.filter(slug__in=[store.slug for store in stores])
       
        categories = Category.objects.filter(store__in=stores)
        parent_choices = [(category.id, str(category)) for category in categories]
        parent_choices.append(('','---------'))
        self.fields['parent'].choices = parent_choices

    class Meta: 
        model = Category
        fields = '__all__'
        exclude = ['slug', 'store']

class AddCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        stores = kwargs.pop('stores')

        super(AddCategoryForm, self).__init__(*args, **kwargs)

        for key in self.fields:              
            self.fields[key].widget.attrs['class'] = 'input'
            # self.fields[key].widget.attrs['v-bind:class'] = "{ 'is-danger': errors.includes("+key+") }"
            if key != 'image':
                self.fields[key].widget.attrs['v-model'] = 'category.'+key

        self.fields['is_featured'].widget.attrs['class'] = 'checkbox'

        self.fields['image'].widget.attrs['class'] = 'file'
        self.fields['image'].widget.attrs['accepts'] = '.jpg, .jpeg, .png'
        self.fields['image'].widget.attrs['v-on:change'] = 'onCategoryFileChange'

        # self.fields['store'].choices = [(store.id, str(store)) for store in stores] #Store.objects.filter(slug__in=[store.slug for store in stores])
       
        categories = Category.objects.filter(store__in=stores)
        parent_choices = [(category.id, str(category)) for category in categories]
        parent_choices.append(('','---------'))
        self.fields['parent'].choices = parent_choices

    class Meta: 
        model = Category
        fields = '__all__'
        exclude = ['slug', 'store']

class AddProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        stores = kwargs.pop('stores')
        super(AddProductForm, self).__init__(*args, **kwargs)
        
        for key in self.fields:              
            self.fields[key].widget.attrs['class'] = 'input'
            # self.fields[key].widget.attrs['v-bind:class'] = "{ 'is-danger': errors.includes("+key+") }"
            if key != 'image':
                self.fields[key].widget.attrs['v-model'] = 'product.'+key

        self.fields['is_featured'].widget.attrs['class'] = 'checkbox'

        self.fields['image'].widget.attrs['class'] = 'file'
        self.fields['image'].widget.attrs['accepts'] = '.jpg, .jpeg, .png'
        self.fields['image'].widget.attrs['v-on:change'] = 'onProductFileChange'

        # self.fields['store'].choices = [(store.id, str(store)) for store in stores] 
       
        categories = Category.objects.filter(store__in=stores)
        self.fields['category'].choices = [(category.id, str(category)) for category in categories]

    class Meta: 
        model = Product
        fields = '__all__'
        exclude = ['slug', 'last_visit', 'thumbnail', 'num_visits', 'store']

class EditProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        stores = kwargs.pop('stores')
        super(EditProductForm, self).__init__(*args, **kwargs)

        for key in self.fields:   
            self.fields[key].widget.attrs['class'] = 'input'
            # self.fields[key].widget.attrs['v-bind:class'] = "{ 'is-danger': errors.includes("+key+") }"
            if key != 'image':
                self.fields[key].widget.attrs['v-model'] = key

        self.fields['is_featured'].widget.attrs['class'] = 'checkbox'

        self.fields['image'].widget.attrs['class'] = 'file'
        self.fields['image'].widget.attrs['accepts'] = '.jpg, .jpeg, .png'
        self.fields['image'].widget.attrs['v-on:change'] = 'onFileChange'

        # self.fields['store'].choices = [(store.id, str(store)) for store in stores] 
       
        categories = Category.objects.filter(store__in=stores)
        self.fields['category'].choices = [(category.id, str(category)) for category in categories]
        

    class Meta: 
        model = Product
        fields = '__all__'
        exclude = ['slug', 'last_visit', 'thumbnail', 'num_visits', 'store']