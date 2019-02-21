from django.db import models


# Create your models here.
# 热点词汇
class kwl(models.Model):
    kid = models.AutoField(primary_key=True)
    word = models.CharField(max_length=10)
    num = models.PositiveIntegerField(default=0)

    def to_json(self):
        d = dict()
        d[getattr(self, 'word')] = getattr(self, 'num')
        import json
        return json.dumps(d, ensure_ascii=False)

    def to_tuple(self):
        return (getattr(self, 'word'),getattr(self, 'num'))


# 热点文章
class fpl(models.Model):
    pid = models.AutoField('pid', primary_key=True)
    url = models.CharField('url', max_length=100)
    title = models.CharField('title', max_length=50)
    content = models.TextField('content')
    forbiddenNum = models.PositiveSmallIntegerField('fn')
    pTime = models.TimeField('pTime')
    pDate = models.DateField('pDate')
    st = models.FloatField('st', null=True)
    simHash = models.BigIntegerField('simHash', null=True)
    c_read = models.PositiveIntegerField('c_read', default=0)
    c_reply = models.PositiveIntegerField('c_reply', default=0)

    def to_tuple(self):
        return (str(getattr(self, 'pid')) , (getattr(self, 'title'),getattr(self, 'pDate').strftime('%Y-%m-%d'),getattr(self, 'c_read'),getattr(self, 'url')))


class EntityCategory(models.Model):
    ecid = models.SmallIntegerField(primary_key=True)
    word = models.CharField(max_length=5)


class Entity(models.Model):
    eid = models.AutoField(primary_key=True)
    word = models.CharField(max_length=25)
    ec = models.ForeignKey(EntityCategory, on_delete=models.SET_NULL, null=True)


class Keyword(models.Model):
    kid = models.AutoField(primary_key=True)
    word = models.CharField(max_length=10)


class ForbiddenWord(models.Model):
    fid = models.AutoField(primary_key=True)
    word = models.CharField(max_length=10)


class Category(models.Model):
    cid = models.SmallIntegerField(primary_key=True)
    word = models.CharField(max_length=4)


class Passage(models.Model):
    pid = models.AutoField('pid', primary_key=True)
    url = models.CharField('url', max_length=100)
    title = models.CharField('title', max_length=50)
    content = models.TextField('content')
    forbiddenNum = models.PositiveSmallIntegerField('fn')
    pTime = models.TimeField('pTime')
    pDate = models.DateField('pDate')
    st = models.FloatField('st', null=True)
    c_read = models.PositiveIntegerField('c_read', default=0)
    c_reply = models.PositiveIntegerField('c_reply', default=0)
    keywords = models.ManyToManyField(Keyword, through='PassageKeyword')
    entities = models.ManyToManyField(Entity)
    fwords = models.ManyToManyField(ForbiddenWord)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def get_abstract(self, word=None):
        index = 50
        # 有关键词传入
        if word:
            word_list = [word]
            index_list = []
            if " " in word:
                word_list = word.split(" ")
            # 计算偏移
            shift = 50 // len(word_list)
            for key in word_list:
                index = self.content.find(key)
                start_index = 0
                end_index = 0
                mod_index = 0
                if index - shift > 0:
                    start_index = index - shift
                else:
                    mod_index = shift

                if index + shift + mod_index < len(self.content):
                    end_index = index + shift + mod_index
                elif index + shift + mod_index < len(self.content):
                    end_index = index + shift
                else:
                    mod_index = shift
                    if start_index - mod_index > 0:
                        start_index -= mod_index
                    else:
                        start_index = 0
                index_list.append([start_index, end_index])

            result = ""
            for item in index_list:
                result += "..." + self.content[item[0]:item[1]] + "..."

            for key in word_list:
                result = result.replace(key, "<em>"+key+"</em>")
            return result
        else:
            if len(self.content) < 50:
                end_index = len(self.content)
            else:
                end_index = 50
            return "..."+self.content[0:end_index]+"..."

    def to_tuple(self):
        ratio = int(getattr(self, 'st')*100)
        abstract = self.get_abstract()
        return (str(getattr(self, 'pid')) , (getattr(self, 'title'),getattr(self, 'pDate').strftime('%Y-%m-%d'),getattr(self, 'c_read'),getattr(self, 'c_reply'),getattr(self, 'url'), ratio, abstract))

class PassageKeyword(models.Model):
    id = models.AutoField('id', primary_key=True)
    pid = models.ForeignKey(Passage)
    kid = models.ForeignKey(Keyword)
    ratio = models.FloatField('ratio')



