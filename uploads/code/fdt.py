#coding=utf-8

import json
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# Post 相关的API
def getHTTPHeader():
    headers = {"x-token": auth_token,
               "x-market": "FX",
               "x-language": "CN",
               "x-country": "CN",
               "Accept-Language": "zh-Hans-US;q=1, zh-Hant-US;q=0.9, en-US;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               "User-Agent": "ForexMasterCN/5.4.160621001 (iPhone; iOS 9.3.2; Scale/2.00)"}
    return headers

def getUserPosts(username):
    headers = getHTTPHeader()
    params = {'auth_token': ('', auth_token), 'hits': ('', '100'), 'offset': ('', '0'), 'target_userid': ('', username)}
    response = requests.post('http://prod.forexmaster.cn/social/v3/getUserWall', files=params, headers=headers)
    content = json.loads(response.content)
    return content['posts']

def postLikeRequest(postId):
    params = {'auth_token': ('', auth_token), 'post_id': ('', postId)}
    headers = getHTTPHeader()

    response = requests.post('http://prod.forexmaster.cn/social/v3/like', files=params, headers=headers)
    print '已经赞完帖子(%s) - %d' % (postId, response.status_code)

def doCommentPost(postId):
    params = {'auth_token': ('', auth_token), 'post_id': ('', postId), 'comment': ('', '~')}
    headers = getHTTPHeader()

    response = requests.post('http://prod.forexmaster.cn/social/v3/comment', files=params, headers=headers)
    print '已经给他帖子留言(%s) - %d' % (postId, response.status_code)

def doRepostPost(postId):
    params = {'auth_token': ('', auth_token), 'post_id': ('', postId)}
    headers = getHTTPHeader()

    response = requests.post('http://prod.forexmaster.cn/social/v3/repost', files=params, headers=headers)
    print '已经转发帖子(%s) - %d' % (postId, response.status_code)

#发表帖子
def doPost():

    params = {'auth_token': ('', auth_token),
              'mention_currencies': ('', '欧元/谢尔克'),
              'mention_symbols': ('', 'EURILS.FX'),
              'msg': ('', '$欧元/谢尔克'),
              'tag': ('', '524545E6-37E9-4BC3-A9FA-B5A3F1FE6442')}
    headers = getHTTPHeader()
    response = requests.post('http://prod.forexmaster.cn/social/v3/post', files=params, headers=headers)
    print '已经发布完帖子 - %d' % (response.status_code)

#删除帖子
def doDeletePost(postid):
    params = {'auth_token': ('', auth_token),
              'postid': ('',postid)}
    headers = getHTTPHeader()
    response = requests.post('http://prod.forexmaster.cn/social/v3/deletePost', files=params, headers=headers)
    print '已经删除帖子(%s) - %d' % (postid, response.status_code)

#赞某个用户所有的帖子
def doLikeAllPost(username):

    print '开始赞用户: %s 的帖子' % (username)
    posts = getUserPosts(username)

    for post in posts:
        postLikeRequest(post["postid"])

    print '用户: %s 的帖子已经赞完' % (username)

#删除我的所有帖子
def doDeleteAllPost(username):
    posts = getUserPosts(username)

    while len(posts) > 0:
        for post in posts:
            if 'repostid' in post.keys():
                doDeletePost(post['repostid'])
            else:
                doDeletePost(post["postid"])

        posts = getUserPosts(username)

#给帖子留言
def doCommentAllPost(username):

    print '开始给用户帖子留言(%s)' % (username)
    posts = getUserPosts(username)

    for post in posts:
        doCommentPost(post['postid'])

    print '已经给所有的帖子留言完毕'

#转发用户所有帖子
def doRepostAllPost(username):

    print '开始转发用户帖子(%s)' % (username)
    posts = getUserPosts(username)

    for post in posts:
        doRepostPost(post['postid'])

    print '已经转发所有的帖子'

#########################################

POST_ENABLED = 0
LIKE_ENABLED = 0
COMMENT_ENABLED = 0
REPOST_ENABLED = 0
DELETE_ENABLED = 1

auth_token = 'M2NLM0ytjCA6jAso6yNjnuDlinUAmoGRfKU0RtJNWgbTPpfznW9SU+3Au1pSGP08m3/2L2g5UklwJcpJmpzwl6wSgMOMuJrwzm3Sw6LDREQsxC1M/cjnAzei63laDitJiCu3ykJFcJx/WYGBrnWm8VZTo5s7ALHZJPPoe/4YZjJvqg3rvyyY9nV9Zk8TOiejQtVgyy98CaeIHzbfQLhqYP5EHbpjLDOV5h+2s74U9Uy0SfK/UfCejZITV5Yp79MOWk4Le5PbAKcu3VQh5dA1zVB1x31+tP0L3DyKAToPj3nTWvHxUIErts+fzZ9ljl26ZX7+CY5y6z674ptXOiaAUA=='
deleteUser = 'mb000000001'


if POST_ENABLED:
    for i in range(1, 100):
        doPost()

# userList = ['mb000000001', 'jn11585852', 'nanjiang', 'fdt_cn_test_15', 'wanghua']
userList = ['mb000000001']

if LIKE_ENABLED:
    for user in userList:
        doLikeAllPost(user)

if COMMENT_ENABLED:
    for user in userList:
        doCommentAllPost(user)

if REPOST_ENABLED:
    for user in userList:
        doRepostAllPost(user)

if DELETE_ENABLED:
    doDeleteAllPost(deleteUser)