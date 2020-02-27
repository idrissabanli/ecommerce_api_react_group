from django.contrib import admin
from products.models import *


admin.site.register([Category, Product, Order])