from django.contrib import admin
from .models import Category, Tag, Product, ProductImage, Comment


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'price', 'created_at')
    list_filter = ('is_published', 'category', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title', )}
    inlines = [ProductImageInline, CommentInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'product', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('author', 'content')
    readonly_fields = ('created_at', )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'order')
    list_filter = ('product', )
