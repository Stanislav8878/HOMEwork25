from django.db import migrations, models, connection
from django.utils.text import slugify

def populate_slug(apps, schema_editor):
    Post = apps.get_model('blogs', 'Post')
    # теперь колонка image уже создана через RunSQL, так что ORM-селект не упадет
    for p in Post.objects.all():
        base = slugify(p.title)[:200] or f'post-{p.pk}'
        slug = base
        i = 1
        while Post.objects.filter(slug=slug).exclude(pk=p.pk).exists():
            i += 1
            slug = f"{base}-{i}"[:220]
        p.slug = slug
        p.save(update_fields=['slug'])

class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        # 1) Добавляем отсутствующие колонки в БД (без изменения state)
        migrations.RunSQL(
            sql=[
                # если каких-то из этих колонок нет — создадим
                "ALTER TABLE blogs_post ADD COLUMN IF NOT EXISTS slug varchar(220);",
                "ALTER TABLE blogs_post ADD COLUMN IF NOT EXISTS content text;",
                "ALTER TABLE blogs_post ADD COLUMN IF NOT EXISTS image varchar(100);",
                "ALTER TABLE blogs_post ADD COLUMN IF NOT EXISTS is_published boolean DEFAULT false;",
                "ALTER TABLE blogs_post ADD COLUMN IF NOT EXISTS views integer DEFAULT 0;",
                "ALTER TABLE blogs_post ADD COLUMN IF NOT EXISTS created_at timestamp with time zone DEFAULT now();",
                "ALTER TABLE blogs_post ADD COLUMN IF NOT EXISTS updated_at timestamp with time zone DEFAULT now();",
            ],
            reverse_sql=[]
        ),

        # 2) Заполняем slug
        migrations.RunPython(populate_slug, migrations.RunPython.noop),

        # 3) Делаем ограничения (NOT NULL + уникальность)
        migrations.RunSQL(
            sql=[
                "ALTER TABLE blogs_post ALTER COLUMN slug SET NOT NULL;",
                # В PostgreSQL удобнее создать уникальный индекс, если уникального ограничения ещё нет
                "CREATE UNIQUE INDEX IF NOT EXISTS blogs_post_slug_uniq_idx ON blogs_post(slug);",
            ],
            reverse_sql=[]
        ),

        # 4) Синхронизируем состояние моделей (не меняет БД, но фиксирует состояние для Django)
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=220, unique=True, verbose_name='Слаг'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='posts/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='post',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Опубликовано'),
        ),
        migrations.AlterField(
            model_name='post',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name='Просмотры'),
        ),
    ]
