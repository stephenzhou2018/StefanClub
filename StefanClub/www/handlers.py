#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Stephen Zhou'

' url handlers '
import markdown2
from aiohttp import web
from coroweb import get,post
from models import User,Blog,Comment,next_id,IndexCarouselItems,IndexNews,HotMatches,SinaCarousel,HotMatchNews,NbaNews
import asyncio,time,re,hashlib,json,logging
from apis import APIError,APIValueError,APIPermissionError,APIResourceNotFoundError,Page
from config import configs


COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret


def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()


def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p


def user2cookie(user, max_age):
    '''
    Generate cookie str by user.
    '''
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)


def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)


@asyncio.coroutine
def cookie2user(cookie_str):
    '''
    Parse cookie and load user if cookie is valid.
    '''
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = yield from User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None


@get('/index')
async def index(request):
    Carousel1 = await IndexCarouselItems.findAll('item_class=?', ['Carousel'], orderBy='id desc', limit=(0,1))
    Carousels = await IndexCarouselItems.findAll('item_class=?', ['Carousel'], orderBy='id desc', limit=(1,4))
    CarouselRights =  await IndexCarouselItems.findAll('item_class=?', ['Carousel_R'], orderBy='id desc', limit=(0,2))
    Rights =  await IndexCarouselItems.findAll('item_class=?', ['Right'], orderBy='id desc', limit=(0,16))
    if request.__user__:
        News = await IndexNews.findAll('find_in_set(?, hate_emails) = 0', [request.__user__.email], orderBy='id desc', limit=(0,16))
    else:
        News = await IndexNews.findAll(orderBy='id desc',limit=(0, 16))
    return {
        '__template__': 'index.html',
        'Carousel1': Carousel1[0],
        'Carousels': Carousels,
        'CarouselRights': CarouselRights,
        'Rights': Rights,
        'News': News,
    }


@get('/')
async def home():
    return {
        '__template__': 'Home.html',
    }


@get('/sports')
async def sports():
    hotmatches = await HotMatches.findAll(orderBy='id desc', limit=(0,5))
    sinacars1 = await SinaCarousel.findAll(orderBy='id desc', limit=(0,1))
    sinacars = await SinaCarousel.findAll(orderBy='id desc', limit=(1,6))
    hotmatchnews = await HotMatchNews.findAll(orderBy='id desc', limit=(0,6))
    hotmatchnews.sort(key=lambda k: (k.get('id', 0)))
    return {
        '__template__': 'sports.html',
        'hotmatches': hotmatches,
        'sinacars': sinacars,
        'sinacars1': sinacars1[0],
        'hotmatchnewss': hotmatchnews,
    }


@get('/blogs')
async def get_blogs(*, page='1'):
    page_index = get_page_index(page)
    num = await Blog.findNumber('count(id)')
    page = Page(num,page_index)
    if num == 0:
        blogs = []
    else:
        blogs = await Blog.findAll(orderBy='created_at desc', limit=(page.offset, page.limit))
    return {
        '__template__': 'blogs.html',
        'page': page,
        'blogs': blogs
    }


@get('/blog/{id}')
async def get_blog(id):
    blog = await Blog.find(id)
    comments = await Comment.findAll('blog_id=?', [id], orderBy='created_at desc')
    for c in comments:
        c.html_content = text2html(c.content)
    blog.html_content = markdown2.markdown(blog.content)
    return {
        '__template__': 'blog.html',
        'blog': blog,
        'comments': comments
    }


@get('/register')
def register():
    return {
        '__template__': 'register.html'
    }


@get('/signin')
def signin():
    return {
        '__template__': 'signin.html'
    }


@get('/api/blogs')
async def api_blogs(*, page='1'):
    page_index = get_page_index(page)
    num = await Blog.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, blogs=())
    blogs = await Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)


@post('/api/blogs')
async def api_create_blog(request, *, name, summary, content):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image, name=name.strip(), summary=summary.strip(), content=content.strip())
    await blog.save()
    return blog


@post('/api/authenticate')
async def authenticate(*, email, passwd):
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid password.')
    users = await User.findAll('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]
    # check passwd:
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid password.')
    # authenticate ok, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    #r.set_cookie(COOKIE_NAME, user2cookie(user, -1), max_age=-1, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out.')
    return r


@get('/manage/')
def manage():
    return 'redirect:/manage/comments'


@get('/manage/comments')
def manage_comments(*, page='1'):
    return {
        '__template__': 'manage_comments.html',
        'page_index': get_page_index(page)
    }


@get('/manage/blogs')
def manage_blogs(*, page='1'):
    return {
        '__template__': 'manage_blogs.html',
        'page_index': get_page_index(page)
    }


@get('/manage/blogs/create')
def manage_create_blog():
    return {
        '__template__': 'manage_blog_edit.html',
        'id': '',
        'action': '/api/blogs'
    }


@get('/manage/blogs/edit')
def manage_edit_blog(*, id):
    return {
        '__template__': 'manage_blog_edit.html',
        'id': id,
        'action': '/api/blogs/%s' % id
    }


@get('/manage/users')
def manage_users(*, page='1'):
    return {
        '__template__': 'manage_users.html',
        'page_index': get_page_index(page)
    }


@get('/api/comments')
async def api_comments(*, page='1'):
    page_index = get_page_index(page)
    num = await Comment.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, comments=())
    comments = await Comment.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, comments=comments)


@get('/api/indexnews')
async def api_indexnews(request,*, numoftime='1'):
    page = int(numoftime)
    if request.__user__:
        news = await IndexNews.findAll('find_in_set(?, hate_emails) = 0', [request.__user__.email], orderBy='id desc', limit=(16*page,16))
    else:
        news = await IndexNews.findAll(orderBy='id desc',limit=(16*page, 16))
    return dict(news=news)


@get('/api/hotmatches')
async def api_hotmatches(*, page='1', swi_type='pre'):
    item_count = await HotMatches.findNumber('count(id)')
    page_count = item_count // 5 + (1 if item_count % 5 > 0 else 0)
    lastpage = 'FALSE'
    firstpage = 'FALSE'
    currentpage = int(page)
    if swi_type == 'pre':
        currentpage = currentpage - 1
    else:
        currentpage = currentpage + 1
    if currentpage == page_count:
        lastpage = 'TRUE'
    if currentpage == 1:
        firstpage = 'TRUE'
    matches = await HotMatches.findAll(orderBy='id desc',limit=(5*(currentpage - 1), 5))
    strcurrentpage = str(currentpage)
    return dict(matches=matches,lastpage=lastpage,firstpage=firstpage,currentpage=strcurrentpage)


@get('/api/nbanews')
async def api_nbanews(*, shift_type):
    nbanews = await NbaNews.findAll('newstype=?',[shift_type],orderBy='id desc',limit=(0, 25))

    return dict(nbanews=nbanews)


@get('/api/hotmatchnews')
async def api_hotmatchnews():
    hotmatchnews = await HotMatchNews.findAll(orderBy='id desc', limit=(0,6))
    hotmatchnews.sort(key=lambda k: (k.get('id', 0)))

    return dict(hotmatchnews=hotmatchnews)


@post('/api/blogs/{id}/comments')
async def api_create_comment(id, request, *, content):
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    if not content or not content.strip():
        raise APIValueError('content')
    blog = await Blog.find(id)
    if blog is None:
        raise APIResourceNotFoundError('Blog')
    comment = Comment(blog_id=blog.id, user_id=user.id, user_name=user.name, user_image=user.image, content=content.strip())
    await comment.save()
    return comment


@post('/api/comments/{id}/delete')
async def api_delete_comments(id, request):
    check_admin(request)
    c = await Comment.find(id)
    if c is None:
        raise APIResourceNotFoundError('Comment')
    await c.remove()
    return dict(id=id)


@get('/api/users')
async def api_get_users(*, page='1'):
    page_index = get_page_index(page)
    num = await User.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, users=())
    users = await User.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    for u in users:
        u.passwd = '******'
    return dict(page=p, users=users)


_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')


@post('/api/users')
async def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    users = await  User.findAll('email=?', [email])
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    await user.save()
    # make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    #r.set_cookie(COOKIE_NAME, user2cookie(user, -1), max_age=-1, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


@get('/api/blogs/{id}')
async def api_get_blog(*, id):
    blog = await Blog.find(id)
    return blog


@post('/api/blogs')
async def api_create_blog(request, *, name, summary, content):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image, name=name.strip(), summary=summary.strip(), content=content.strip())
    await blog.save()
    return blog


@post('/api/blogs/{id}')
async def api_update_blog(id, request, *, name, summary, content):
    check_admin(request)
    blog = await Blog.find(id)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    blog.name = name.strip()
    blog.summary = summary.strip()
    blog.content = content.strip()
    await blog.update()
    return blog


@post('/api/blogs/{id}/delete')
async def api_delete_blog(request, *, id):
    check_admin(request)
    blog = await Blog.find(id)
    await blog.remove()
    return dict(id=id)


@post('/api/indexnews/{id}/updatehate')
async def api_updatehate_news(request, *, id):
    if request.__user__ is None:
        raise APIPermissionError()
    indexnews = await IndexNews.find(id)
    old_hate_emails = indexnews.hate_emails
    if request.__user__:
        new_hate_email = request.__user__.email
    else:
        new_hate_email = 'test'
    new_hate_emails = old_hate_emails + ',' + new_hate_email
    indexnews.hate_emails = new_hate_emails
    await indexnews.update()
    return indexnews