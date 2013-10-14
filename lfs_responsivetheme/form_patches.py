#from lfs.customer.forms import AddressForm
#AddressForm.error_css_class='pippo'

#for field_name in AddressForm.base_fields.keys():
    #AddressForm.base_fields[field_name].widget.attrs['class'] = 'form-control'

from django.forms.widgets import Input
def widget__init__(self, attrs=None):
    if attrs is not None:
        self.attrs = attrs.copy()
    else:
        self.attrs = {'class':'form-control'}
Input.__init__ = widget__init__


from django.forms.widgets import Select
def widget__init__(self, attrs=None, choices=()):
    if attrs is None:
        attrs = {'class':'form-control'}
    super(Select, self).__init__(attrs)
    # choices can be any iterable, but we may need to render this widget
    # multiple times. Thus, collapse it into a list so it can be consumed
    # more than once.
    self.choices = list(choices)
Select.__init__ = widget__init__


from django.forms.widgets import PasswordInput
def widget__init__(self, attrs=None, render_value=False):
    if attrs is None:
        attrs = {'class':'form-control'}
    super(PasswordInput, self).__init__(attrs)
    self.render_value = render_value
PasswordInput.__init__ = widget__init__